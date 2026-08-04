import json
import os

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.video import Video, BackgroundVideo
from app.models.lesson import Lesson
from app.models.concept import Concept
from app.schemas.video import VideoFeedResponse, VideoProgressUpdate
from app.api.v1.deps import get_current_user
from app.models.user import User

router = APIRouter()

_BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
_VIDEO_OUTPUT_DIR = os.path.join(_BASE_DIR, "video_pipeline", "output")
_BACKGROUNDS_DIR = os.path.join(_BASE_DIR, "video_pipeline", "backgrounds")
_FEED_BACKGROUNDS = ("gameplay_01.webm", "gameplay_01.mp4", "minecraft.mp4", "minecraft.webm")


def _video_file_url(output_id: str, filename: str) -> str:
    return f"/videos/{output_id}/{filename}"


def _pick_background_url(index: int) -> str | None:
    if not os.path.isdir(_BACKGROUNDS_DIR):
        return None

    backgrounds = sorted(
        [
            name
            for name in _FEED_BACKGROUNDS
            if os.path.isfile(os.path.join(_BACKGROUNDS_DIR, name))
        ],
        key=lambda name: os.path.getsize(os.path.join(_BACKGROUNDS_DIR, name)),
        reverse=True,
    )
    if not backgrounds:
        return None

    return f"/backgrounds/{backgrounds[0]}"


def _load_output_metadata(output_dir: str) -> dict:
    metadata_path = os.path.join(output_dir, "metadata.json")
    if not os.path.isfile(metadata_path):
        return {}

    try:
        with open(metadata_path, encoding="utf-8") as metadata_file:
            metadata = json.load(metadata_file)
    except (OSError, json.JSONDecodeError):
        return {}

    return metadata if isinstance(metadata, dict) else {}


@router.get("/feed", response_model=VideoFeedResponse)
async def get_video_feed(
    cursor: str | None = None,
    category: str | None = None,
    difficulty: int | None = None,
    limit: int = Query(default=10, le=50),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    from app.services.recommendation import RecommendationService
    service = RecommendationService(db)
    return await service.get_feed(user_id=user.id, cursor=cursor, category=category, difficulty=difficulty, limit=limit)


@router.get("/feed/anonymous", response_model=VideoFeedResponse)
async def get_anonymous_feed(
    cursor: str | None = None,
    category: str | None = None,
    difficulty: int | None = None,
    concept_id: str | None = None,
    limit: int = Query(default=10, le=50),
    db: AsyncSession = Depends(get_db),
):
    from app.services.recommendation import RecommendationService
    service = RecommendationService(db)
    return await service.get_anonymous_feed(cursor=cursor, category=category, difficulty=difficulty, concept_id=concept_id, limit=limit)


@router.get("/pipeline-outputs", response_model=list[dict])
async def list_pipeline_outputs(
    limit: int = Query(default=50, le=200),
    db: AsyncSession = Depends(get_db),
):
    """List generated videos directly from video_pipeline/output.

    A folder is playable if it has either a baked full.mp4 or the overlay pair
    mask.webm + audio.mp3. New pipeline renders appear here after refresh.
    """
    if not os.path.isdir(_VIDEO_OUTPUT_DIR):
        return []

    metadata_by_prefix = {}
    lessons_result = await db.execute(
        select(Lesson, Concept)
        .join(Concept, Concept.id == Lesson.concept_id)
        .where(Lesson.deleted_at.is_(None))
    )
    for lesson, concept in lessons_result.all():
        metadata_by_prefix[str(lesson.id)[:8]] = {
            "lesson_id": str(lesson.id),
            "concept_id": str(concept.id),
            "title": lesson.title,
            "hook": lesson.hook,
            "concept": concept.name,
            "category": concept.category,
            "difficulty": lesson.difficulty,
        }

    items = []
    for output_id in sorted(os.listdir(_VIDEO_OUTPUT_DIR)):
        output_dir = os.path.join(_VIDEO_OUTPUT_DIR, output_id)
        if not os.path.isdir(output_dir):
            continue

        mask_path = os.path.join(output_dir, "mask.webm")
        audio_path = os.path.join(output_dir, "audio.mp3")
        full_path = os.path.join(output_dir, "full.mp4")
        timing_path = os.path.join(output_dir, "timing.json")
        metadata_path = os.path.join(output_dir, "metadata.json")

        has_mask = os.path.getsize(mask_path) > 0 if os.path.isfile(mask_path) else False
        has_audio = os.path.getsize(audio_path) > 0 if os.path.isfile(audio_path) else False
        has_full = os.path.getsize(full_path) > 0 if os.path.isfile(full_path) else False

        if not has_full and not (has_mask and has_audio):
            continue

        updated_at = max(
            os.path.getmtime(path)
            for path in (mask_path, audio_path, full_path, timing_path, metadata_path)
            if os.path.exists(path)
        )
        size_bytes = sum(
            os.path.getsize(os.path.join(output_dir, name))
            for name in os.listdir(output_dir)
            if os.path.isfile(os.path.join(output_dir, name))
        )

        metadata = {
            **_load_output_metadata(output_dir),
            **metadata_by_prefix.get(output_id, {}),
        }

        items.append({
            "id": output_id,
            "title": metadata.get("title", output_id),
            "hook": metadata.get("hook"),
            "description": metadata.get("description"),
            "problem": metadata.get("problem"),
            "explanation": metadata.get("explanation"),
            "summary": metadata.get("summary"),
            "lesson_id": metadata.get("lesson_id"),
            "concept_id": metadata.get("concept_id"),
            "concept": metadata.get("concept"),
            "category": metadata.get("category"),
            "difficulty": metadata.get("difficulty"),
            "mask_url": _video_file_url(output_id, "mask.webm") if has_mask else None,
            "audio_url": _video_file_url(output_id, "audio.mp3") if has_audio else None,
            "full_url": _video_file_url(output_id, "full.mp4") if has_full else None,
            "timing_url": _video_file_url(output_id, "timing.json") if os.path.isfile(timing_path) else None,
            "background_url": _pick_background_url(len(items)),
            "updated_at": updated_at,
            "size_bytes": size_bytes,
        })

    items.sort(key=lambda item: item["updated_at"], reverse=True)
    return items[:limit]


@router.post("/{video_id}/progress")
async def update_video_progress(
    video_id: str,
    data: VideoProgressUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    from app.services.progress import ProgressService
    service = ProgressService(db)
    return await service.update_video_progress(user_id=user.id, video_id=video_id, data=data)


@router.get("/backgrounds", response_model=list[dict])
async def list_background_videos(
    category: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(BackgroundVideo).where(BackgroundVideo.is_active == True)
    if category:
        query = query.where(BackgroundVideo.category == category)
    result = await db.execute(query)
    backgrounds = result.scalars().all()
    return [
        {
            "id": b.id,
            "name": b.name,
            "category": b.category,
            "url": b.url,
            "duration_seconds": b.duration_seconds,
            "resolution": b.resolution,
        }
        for b in backgrounds
    ]


@router.post("/{video_id}/like")
async def like_video(
    video_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(select(Video).where(Video.id == video_id))
    video = result.scalar_one_or_none()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    video.likes += 1
    await db.commit()
    return {"likes": video.likes}

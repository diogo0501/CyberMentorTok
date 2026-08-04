from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import os
import asyncio
import shutil
from app.core.database import get_db
from app.api.v1.deps import get_current_admin_user
from app.models.user import User
from app.models.concept import Concept
from app.models.lesson import Lesson
from app.models.video import Video, BackgroundVideo
from app.models.rendering import RenderingJob

router = APIRouter()

VIDEO_OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
    "video_pipeline", "output"
)
DESKTOP_VIDEO = r"C:\Users\diogo\Desktop\Download.mp4"


@router.get("/dashboard")
async def admin_dashboard(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
):
    users_count = await db.execute(select(func.count(User.id)))
    concepts_count = await db.execute(select(func.count(Concept.id)))
    lessons_count = await db.execute(select(func.count(Lesson.id)))
    videos_count = await db.execute(select(func.count(Video.id)))

    return {
        "users": users_count.scalar(),
        "concepts": concepts_count.scalar(),
        "lessons": lessons_count.scalar(),
        "videos": videos_count.scalar(),
    }


@router.get("/lessons/pending")
async def pending_lessons(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
):
    result = await db.execute(
        select(Lesson).where(Lesson.approved == False, Lesson.ai_generated == True).order_by(Lesson.created_at.desc())
    )
    return result.scalars().all()


@router.post("/lessons/{lesson_id}/approve")
async def approve_lesson(
    lesson_id: str,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
):
    result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    lesson.approved = True
    lesson.approved_by = admin.id
    await db.commit()
    return {"status": "approved"}


@router.get("/rendering/jobs")
async def rendering_jobs(
    status: str | None = None,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
):
    query = select(RenderingJob).order_by(RenderingJob.created_at.desc())
    if status:
        query = query.where(RenderingJob.status == status)
    query = query.limit(50)
    result = await db.execute(query)
    return result.scalars().all()


async def _generate_video_task(lesson_id: str, lesson_title: str, dialogue: list):
    """Background task to generate a lesson video."""
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "video_pipeline"))
    import json
    from tts_generator import generate_dialogue_audio, concatenate_audio, timeline_to_seconds
    from compositor import compose_video
    from mask_generator import generate_mask

    temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "video_pipeline", "temp", f"{lesson_id[:8]}")
    temp_dir = os.path.normpath(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)

    timeline, chunks = await generate_dialogue_audio(dialogue, temp_dir)
    if not timeline:
        raise RuntimeError("No dialogue lines could be synthesized")
    timeline_s = timeline_to_seconds(timeline)
    audio_path = concatenate_audio(timeline, temp_dir)

    lesson_dir = os.path.join(VIDEO_OUTPUT_DIR, lesson_id[:8])
    os.makedirs(lesson_dir, exist_ok=True)

    timing_data = {
        "timeline": [
            {
                "speaker": entry["speaker"],
                "text": entry["text"],
                "start_s": entry["start_ms"] / 1000.0,
                "end_s": entry["end_ms"] / 1000.0,
            }
            for entry in timeline
        ],
        "chunks": chunks,
        "total_duration": timeline_s[-1]["end_s"],
    }
    with open(os.path.join(lesson_dir, "timing.json"), "w", encoding="utf-8") as f:
        json.dump(timing_data, f, indent=2)

    shutil.copy2(audio_path, os.path.join(lesson_dir, "audio.mp3"))

    mask_path = os.path.join(lesson_dir, "mask.webm")
    generate_mask(
        timeline=timeline_s,
        chunks=chunks,
        audio_path=audio_path,
        output_path=mask_path,
    )

    bg = DESKTOP_VIDEO if os.path.exists(DESKTOP_VIDEO) else None
    output_path = os.path.join(lesson_dir, "full.mp4")
    compose_video(
        timeline=timeline_s,
        chunks=chunks,
        audio_path=audio_path,
        output_path=output_path,
        background_video=bg,
    )
    return output_path


@router.post("/lessons/{lesson_id}/generate-video")
async def generate_lesson_video(
    lesson_id: str,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
):
    result = await db.execute(select(Lesson).where(Lesson.id == lesson_id, Lesson.deleted_at.is_(None)))
    lesson = result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    if not lesson.dialogue:
        raise HTTPException(status_code=400, detail="Lesson has no dialogue")

    background_tasks.add_task(_generate_video_task, lesson_id, lesson.title, lesson.dialogue)
    return {"status": "generating", "lesson_id": lesson_id}

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.lesson import Lesson
from app.models.video import Video
from app.schemas.lesson import LessonCreate, LessonResponse
from app.api.v1.deps import get_current_user, get_current_admin_user
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=list[LessonResponse])
async def list_lessons(
    concept_id: str | None = None,
    difficulty: int | None = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    query = select(Lesson).where(Lesson.deleted_at.is_(None))
    if concept_id:
        query = query.where(Lesson.concept_id == concept_id)
    if difficulty:
        query = query.where(Lesson.difficulty == difficulty)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{lesson_id}", response_model=LessonResponse)
async def get_lesson(lesson_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lesson).where(Lesson.id == lesson_id, Lesson.deleted_at.is_(None)))
    lesson = result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@router.post("/", response_model=LessonResponse, status_code=201)
async def create_lesson(
    data: LessonCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
):
    lesson = Lesson(**data.model_dump())
    db.add(lesson)
    await db.commit()
    await db.refresh(lesson)
    return lesson


@router.get("/{lesson_id}/feed")
async def get_lesson_feed(lesson_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lesson).where(Lesson.id == lesson_id, Lesson.deleted_at.is_(None)))
    lesson = result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    video_result = await db.execute(
        select(Video).where(Video.lesson_id == lesson_id, Video.status == "ready")
    )
    video = video_result.scalar_one_or_none()

    return {
        "lesson": LessonResponse.model_validate(lesson).model_dump(),
        "video_url": video.url if video else None,
        "thumbnail_url": video.thumbnail_url if video else None,
        "subtitles": [],
    }

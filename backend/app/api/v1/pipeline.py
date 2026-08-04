from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.v1.deps import get_current_admin_user
from app.models.user import User

router = APIRouter()


@router.post("/generate-lesson")
async def trigger_lesson_generation(
    concept_slug: str,
    difficulty: int = 1,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
):
    from app.services.pipeline.lesson_generator import LessonGenerator
    generator = LessonGenerator(db)
    result = await generator.generate(concept_slug=concept_slug, difficulty=difficulty)
    return result


@router.post("/generate-dialogue")
async def trigger_dialogue_generation(
    lesson_id: str,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
):
    from app.services.pipeline.dialogue_generator import DialogueGenerator
    generator = DialogueGenerator(db)
    result = await generator.generate(lesson_id=lesson_id)
    return result


@router.post("/validate/{lesson_id}")
async def validate_lesson(
    lesson_id: str,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
):
    from app.services.pipeline.fact_validator import FactValidator
    validator = FactValidator(db)
    result = await validator.validate(lesson_id=lesson_id)
    return result


@router.post("/render/{lesson_id}")
async def trigger_rendering(
    lesson_id: str,
    background_category: str = "minecraft_parkour",
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
):
    from app.services.pipeline.renderer import VideoRenderer
    renderer = VideoRenderer(db)
    result = await renderer.start_render(lesson_id=lesson_id, background_category=background_category)
    return result


@router.get("/status/{job_id}")
async def get_render_status(
    job_id: str,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
):
    from sqlalchemy import select
    from app.models.rendering import RenderingJob
    result = await db.execute(select(RenderingJob).where(RenderingJob.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {
        "status": job.status,
        "progress": job.progress_percent,
        "current_step": job.current_step,
        "error": job.error_message,
    }

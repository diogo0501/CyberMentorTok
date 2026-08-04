from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.progress import ProgressUpdate, ProgressResponse, MasteryResponse, LearningDashboard
from app.api.v1.deps import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/lesson/{lesson_id}", response_model=ProgressResponse)
async def get_lesson_progress(
    lesson_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    from app.services.progress import ProgressService
    service = ProgressService(db)
    return await service.get_lesson_progress(user_id=user.id, lesson_id=lesson_id)


@router.post("/lesson", response_model=ProgressResponse)
async def update_lesson_progress(
    data: ProgressUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    from app.services.progress import ProgressService
    service = ProgressService(db)
    return await service.update_lesson_progress(user_id=user.id, data=data)


@router.get("/concept/{concept_id}", response_model=MasteryResponse)
async def get_concept_mastery(
    concept_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    from app.services.progress import ProgressService
    service = ProgressService(db)
    return await service.get_concept_mastery(user_id=user.id, concept_id=concept_id)


@router.get("/dashboard", response_model=LearningDashboard)
async def get_dashboard(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    from app.services.progress import ProgressService
    service = ProgressService(db)
    return await service.get_dashboard(user_id=user.id)

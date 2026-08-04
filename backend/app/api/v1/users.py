from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserStats
from app.api.v1.deps import get_current_user

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/me/stats", response_model=UserStats)
async def get_my_stats(current_user: User = Depends(get_current_user)):
    return UserStats(
        total_hours_learned=current_user.total_hours_learned,
        concepts_mastered=current_user.concepts_mastered,
        current_streak=current_user.current_streak,
        longest_streak=current_user.longest_streak,
        average_quiz_score=current_user.average_quiz_score,
        strongest_domain=current_user.strongest_domain,
        weakest_domain=current_user.weakest_domain,
        xp=current_user.xp,
        level=current_user.level,
    )


@router.get("/me/dashboard")
async def get_learning_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from app.services.progress import ProgressService
    service = ProgressService(db)
    return await service.get_dashboard(current_user.id)

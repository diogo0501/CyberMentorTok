from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.v1.deps import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/event")
async def track_event(
    event_type: str,
    event_data: dict = {},
    video_id: str | None = None,
    lesson_id: str | None = None,
    concept_id: str | None = None,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    from app.models.analytics import AnalyticsEvent

    event = AnalyticsEvent(
        user_id=user.id,
        event_type=event_type,
        event_data=event_data,
        video_id=video_id,
        lesson_id=lesson_id,
        concept_id=concept_id,
    )
    db.add(event)
    await db.commit()
    return {"status": "tracked"}


@router.get("/heatmap")
async def get_learning_heatmap(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    from datetime import datetime, timedelta
    from sqlalchemy import select
    from app.models.analytics import AnalyticsEvent

    week_data = [[0] * 24 for _ in range(7)]

    result = await db.execute(
        select(AnalyticsEvent).where(
            AnalyticsEvent.user_id == user.id,
            AnalyticsEvent.event_type == "video_start",
            AnalyticsEvent.created_at >= datetime.utcnow() - timedelta(days=7),
        )
    )
    events = result.scalars().all()

    for event in events:
        day = event.created_at.weekday()
        hour = event.created_at.hour
        week_data[day][hour] += 1

    return {"heatmap": week_data}

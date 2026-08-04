import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, JSON
from app.core.database import Base


def gen_uuid():
    return str(uuid.uuid4())


class AnalyticsEvent(Base):
    __tablename__ = "analytics_events"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True, index=True)
    session_id = Column(String(100), index=True)

    event_type = Column(String(50), nullable=False, index=True)
    event_data = Column(JSON, default=dict)

    video_id = Column(String(36), nullable=True, index=True)
    lesson_id = Column(String(36), nullable=True, index=True)
    concept_id = Column(String(36), nullable=True, index=True)

    device_type = Column(String(20))
    platform = Column(String(20))
    app_version = Column(String(20))

    load_time_ms = Column(Float)
    buffer_time_ms = Column(Float)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


def gen_uuid():
    return str(uuid.uuid4())


class WatchHistory(Base):
    __tablename__ = "watch_history"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    video_id = Column(String(36), ForeignKey("videos.id"), nullable=False, index=True)
    lesson_id = Column(String(36), ForeignKey("lessons.id"), nullable=False, index=True)

    watched_seconds = Column(Float, default=0.0)
    completed = Column(Boolean, default=False)
    watch_percent = Column(Float, default=0.0)
    replay_count = Column(Integer, default=0)
    paused_count = Column(Integer, default=0)
    speed = Column(Float, default=1.0)
    muted = Column(Boolean, default=False)

    device_type = Column(String(20))
    session_id = Column(String(100))

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="history")

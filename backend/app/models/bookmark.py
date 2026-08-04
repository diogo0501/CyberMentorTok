import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


def gen_uuid():
    return str(uuid.uuid4())


class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    lesson_id = Column(String(36), ForeignKey("lessons.id"), nullable=False, index=True)
    video_id = Column(String(36), ForeignKey("videos.id"), nullable=True)

    timestamp_seconds = Column(Float)
    folder = Column(String(100), default="default")
    notes = Column(Text)
    tags = Column(JSON, default=list)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="bookmarks")

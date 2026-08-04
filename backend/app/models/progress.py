import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


def gen_uuid():
    return str(uuid.uuid4())


class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    lesson_id = Column(String(36), ForeignKey("lessons.id"), nullable=False, index=True)
    video_id = Column(String(36), ForeignKey("videos.id"), nullable=True)

    status = Column(String(20), default="unlocked")
    watch_progress = Column(Float, default=0.0)
    completed = Column(Boolean, default=False)
    watch_count = Column(Integer, default=0)
    total_watch_seconds = Column(Float, default=0.0)

    confidence_score = Column(Float, default=0.0)
    mastery_level = Column(String(20), default="locked")
    last_reviewed_at = Column(DateTime(timezone=True))
    next_review_at = Column(DateTime(timezone=True))

    best_quiz_score = Column(Float, default=0.0)
    quiz_attempts_count = Column(Integer, default=0)

    first_watched_at = Column(DateTime(timezone=True))
    last_watched_at = Column(DateTime(timezone=True))
    time_spent_seconds = Column(Float, default=0.0)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="progress")


class ConceptMastery(Base):
    __tablename__ = "concept_mastery"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    concept_id = Column(String(36), ForeignKey("concepts.id"), nullable=False, index=True)

    status = Column(String(20), default="locked")
    confidence_score = Column(Float, default=0.0)
    lessons_completed = Column(Integer, default=0)
    total_lessons = Column(Integer, default=0)
    completion_percent = Column(Float, default=0.0)

    last_reviewed_at = Column(DateTime(timezone=True))
    next_review_at = Column(DateTime(timezone=True))
    review_count = Column(Integer, default=0)

    average_quiz_score = Column(Float, default=0.0)
    total_time_seconds = Column(Float, default=0.0)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="mastery")

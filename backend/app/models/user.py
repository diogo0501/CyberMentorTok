import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, Integer, Float, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


def gen_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    display_name = Column(String(100))
    avatar_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_active_date = Column(DateTime(timezone=True))

    total_hours_learned = Column(Float, default=0.0)
    concepts_mastered = Column(Integer, default=0)
    average_quiz_score = Column(Float, default=0.0)
    learning_speed = Column(Float, default=1.0)
    strongest_domain = Column(String(100))
    weakest_domain = Column(String(100))

    preferred_difficulty = Column(Integer, default=1)
    daily_goal_minutes = Column(Integer, default=15)
    notifications_enabled = Column(Boolean, default=True)
    theme = Column(String(20), default="dark")

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    progress = relationship("UserProgress", back_populates="user", lazy="selectin")
    mastery = relationship("ConceptMastery", back_populates="user", lazy="selectin")
    bookmarks = relationship("Bookmark", back_populates="user", lazy="selectin")
    history = relationship("WatchHistory", back_populates="user", lazy="selectin")
    quiz_attempts = relationship("QuizAttempt", back_populates="user", lazy="selectin")

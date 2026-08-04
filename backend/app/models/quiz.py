import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, JSON, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


def gen_uuid():
    return str(uuid.uuid4())


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    lesson_id = Column(String(36), ForeignKey("lessons.id"), nullable=False, index=True)
    concept_id = Column(String(36), ForeignKey("concepts.id"), nullable=False, index=True)

    question = Column(Text, nullable=False)
    question_type = Column(String(20), default="multiple_choice")
    answers = Column(JSON, nullable=False)
    explanation = Column(Text)
    difficulty = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)

    total_attempts = Column(Integer, default=0)
    correct_attempts = Column(Integer, default=0)
    average_time_seconds = Column(Float, default=0.0)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    attempts = relationship("QuizAttempt", back_populates="quiz", lazy="selectin")


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    quiz_id = Column(String(36), ForeignKey("quizzes.id"), nullable=False, index=True)
    lesson_id = Column(String(36), ForeignKey("lessons.id"), nullable=False)

    selected_answer = Column(String(10), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    time_taken_seconds = Column(Float)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="quiz_attempts")
    quiz = relationship("Quiz", back_populates="attempts")

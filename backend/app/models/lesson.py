import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, JSON, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


def gen_uuid():
    return str(uuid.uuid4())


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    concept_id = Column(String(36), ForeignKey("concepts.id"), nullable=False, index=True)
    title = Column(String(300), nullable=False)
    slug = Column(String(300), nullable=False, index=True)
    description = Column(Text)

    difficulty = Column(Integer, nullable=False, default=1)
    hook = Column(Text)
    problem = Column(Text)
    explanation = Column(Text)
    real_world_example = Column(Text)
    summary = Column(Text)
    curiosity_hook = Column(Text)

    dialogue = Column(JSON, nullable=False, default=list)
    learning_objectives = Column(JSON, default=list)
    prerequisites_concepts = Column(JSON, default=list)
    related_concepts = Column(JSON, default=list)
    next_concepts = Column(JSON, default=list)
    quiz_questions = Column(JSON, default=list)

    estimated_duration_seconds = Column(Integer, default=90)
    ai_generated = Column(Boolean, default=False)
    ai_confidence = Column(Float)
    approved = Column(Boolean, default=False)
    approved_by = Column(String(36), nullable=True)

    total_watches = Column(Integer, default=0)
    average_completion = Column(Float, default=0.0)
    average_quiz_score = Column(Float, default=0.0)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    concept = relationship("Concept", back_populates="lessons")
    videos = relationship("Video", back_populates="lesson", lazy="selectin")

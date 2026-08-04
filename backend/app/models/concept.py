import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, JSON, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


def gen_uuid():
    return str(uuid.uuid4())


class Concept(Base):
    __tablename__ = "concepts"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    name = Column(String(200), nullable=False, index=True)
    slug = Column(String(200), unique=True, nullable=False, index=True)
    description = Column(Text)
    category = Column(String(100), nullable=False, index=True)
    difficulty = Column(Integer, nullable=False, default=1)
    estimated_mastery_minutes = Column(Integer, default=30)

    domain = Column(String(100), index=True)
    tags = Column(JSON, default=list)
    mitre_attack_id = Column(String(20))
    owasp_category = Column(String(50))

    is_published = Column(Boolean, default=False)
    total_lessons = Column(Integer, default=0)
    total_videos = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    prerequisites = relationship("ConceptPrerequisite", foreign_keys="ConceptPrerequisite.concept_id", back_populates="concept", lazy="selectin")
    dependents = relationship("ConceptPrerequisite", foreign_keys="ConceptPrerequisite.prerequisite_id", back_populates="prerequisite", lazy="selectin")
    lessons = relationship("Lesson", back_populates="concept", lazy="selectin")


class ConceptPrerequisite(Base):
    __tablename__ = "concept_prerequisites"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    concept_id = Column(String(36), ForeignKey("concepts.id"), nullable=False, index=True)
    prerequisite_id = Column(String(36), ForeignKey("concepts.id"), nullable=False, index=True)
    is_required = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    concept = relationship("Concept", foreign_keys=[concept_id], back_populates="prerequisites")
    prerequisite = relationship("Concept", foreign_keys=[prerequisite_id], back_populates="dependents")

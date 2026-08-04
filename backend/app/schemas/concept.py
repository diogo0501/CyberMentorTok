from pydantic import BaseModel
from datetime import datetime


class ConceptCreate(BaseModel):
    name: str
    slug: str
    description: str | None = None
    category: str
    difficulty: int = 1
    estimated_mastery_minutes: int = 30
    domain: str | None = None
    tags: list[str] = []
    mitre_attack_id: str | None = None
    owasp_category: str | None = None
    prerequisite_ids: list[str] = []


class ConceptResponse(BaseModel):
    id: str
    name: str
    slug: str
    description: str | None
    category: str
    difficulty: int
    estimated_mastery_minutes: int
    domain: str | None
    tags: list[str]
    mitre_attack_id: str | None
    owasp_category: str | None
    total_lessons: int
    total_videos: int
    is_published: bool
    created_at: datetime | None

    class Config:
        from_attributes = True


class ConceptWithPrerequisites(ConceptResponse):
    prerequisites: list[ConceptResponse] = []
    dependents: list[ConceptResponse] = []


class ConceptGraph(BaseModel):
    concepts: list[ConceptResponse]
    edges: list[dict]


class ConceptProgress(BaseModel):
    concept: ConceptResponse
    status: str
    confidence_score: float
    lessons_completed: int
    total_lessons: int
    completion_percent: float
    next_review_at: datetime | None

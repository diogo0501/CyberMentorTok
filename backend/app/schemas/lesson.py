from pydantic import BaseModel
from datetime import datetime


class DialogueLine(BaseModel):
    speaker: str
    text: str


class QuizQuestion(BaseModel):
    question: str
    answers: list[dict]
    explanation: str | None = None


class LessonCreate(BaseModel):
    concept_id: str
    title: str
    slug: str
    description: str | None = None
    difficulty: int = 1
    hook: str | None = None
    problem: str | None = None
    explanation: str | None = None
    real_world_example: str | None = None
    summary: str | None = None
    curiosity_hook: str | None = None
    dialogue: list[DialogueLine] = []
    learning_objectives: list[str] = []
    prerequisites_concepts: list[str] = []
    related_concepts: list[str] = []
    next_concepts: list[str] = []
    quiz_questions: list[QuizQuestion] = []
    estimated_duration_seconds: int = 90


class LessonResponse(BaseModel):
    id: str
    concept_id: str
    title: str
    slug: str
    description: str | None
    difficulty: int
    hook: str | None
    problem: str | None
    explanation: str | None
    real_world_example: str | None
    summary: str | None
    curiosity_hook: str | None
    dialogue: list[DialogueLine]
    learning_objectives: list[str]
    prerequisites_concepts: list[str]
    related_concepts: list[str]
    next_concepts: list[str]
    quiz_questions: list[QuizQuestion]
    estimated_duration_seconds: int
    ai_generated: bool
    ai_confidence: float | None
    approved: bool
    total_watches: int
    average_completion: float
    average_quiz_score: float
    created_at: datetime | None

    class Config:
        from_attributes = True


class LessonFeedItem(BaseModel):
    lesson: LessonResponse
    video_url: str | None
    background_video_url: str | None
    thumbnail_url: str | None
    subtitles: list[dict]
    user_progress: dict | None = None

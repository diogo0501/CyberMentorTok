from pydantic import BaseModel
from datetime import datetime


class QuizCreate(BaseModel):
    lesson_id: str
    concept_id: str
    question: str
    question_type: str = "multiple_choice"
    answers: list[dict]
    explanation: str | None = None
    difficulty: int = 1


class QuizResponse(BaseModel):
    id: str
    lesson_id: str
    concept_id: str
    question: str
    question_type: str
    answers: list[dict]
    explanation: str | None
    difficulty: int
    total_attempts: int
    correct_attempts: int

    class Config:
        from_attributes = True


class QuizSubmit(BaseModel):
    quiz_id: str
    selected_answer: str
    time_taken_seconds: float | None = None


class QuizResult(BaseModel):
    is_correct: bool
    correct_answer: str
    explanation: str | None
    confidence_change: float
    next_review_scheduled: datetime | None
    streak_maintained: bool
    xp_earned: int

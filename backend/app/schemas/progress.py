from pydantic import BaseModel
from datetime import datetime


class ProgressUpdate(BaseModel):
    lesson_id: str
    video_id: str | None = None
    watch_progress: float = 0.0
    completed: bool = False
    time_spent_seconds: float = 0.0


class ProgressResponse(BaseModel):
    lesson_id: str
    status: str
    watch_progress: float
    completed: bool
    watch_count: int
    confidence_score: float
    mastery_level: str
    best_quiz_score: float
    next_review_at: datetime | None
    time_spent_seconds: float

    class Config:
        from_attributes = True


class MasteryResponse(BaseModel):
    concept_id: str
    status: str
    confidence_score: float
    lessons_completed: int
    total_lessons: int
    completion_percent: float
    average_quiz_score: float
    next_review_at: datetime | None

    class Config:
        from_attributes = True


class LearningDashboard(BaseModel):
    total_hours_learned: float
    concepts_mastered: int
    concepts_in_progress: int
    current_streak: int
    daily_goal_progress: float
    recent_activity: list[dict]
    upcoming_reviews: list[dict]
    recommended_next: list[dict]
    domain_breakdown: list[dict]
    weekly_heatmap: list[list[int]]

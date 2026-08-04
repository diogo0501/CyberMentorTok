from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    email: str
    username: str
    password: str
    display_name: str | None = None


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    display_name: str | None
    avatar_url: str | None
    xp: int
    level: int
    current_streak: int
    total_hours_learned: float
    concepts_mastered: int
    average_quiz_score: float
    created_at: datetime | None

    class Config:
        from_attributes = True


class UserStats(BaseModel):
    total_hours_learned: float
    concepts_mastered: int
    current_streak: int
    longest_streak: int
    average_quiz_score: float
    strongest_domain: str | None
    weakest_domain: str | None
    xp: int
    level: int


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

from pydantic import BaseModel
from datetime import datetime


class BookmarkCreate(BaseModel):
    lesson_id: str
    video_id: str | None = None
    timestamp_seconds: float | None = None
    folder: str = "default"
    notes: str | None = None
    tags: list[str] = []


class BookmarkResponse(BaseModel):
    id: str
    user_id: str
    lesson_id: str
    video_id: str | None
    timestamp_seconds: float | None
    folder: str
    notes: str | None
    tags: list[str]
    created_at: datetime | None

    class Config:
        from_attributes = True


class BookmarkUpdate(BaseModel):
    folder: str | None = None
    notes: str | None = None
    tags: list[str] | None = None

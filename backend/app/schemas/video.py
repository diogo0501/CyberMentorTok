from pydantic import BaseModel
from datetime import datetime


class VideoResponse(BaseModel):
    id: str
    lesson_id: str
    url: str
    thumbnail_url: str | None
    duration_seconds: float
    resolution: str | None
    status: str
    views: int
    likes: int
    completions: int
    average_watch_percent: float
    created_at: datetime | None

    class Config:
        from_attributes = True


class BackgroundVideoResponse(BaseModel):
    id: str
    name: str
    category: str
    url: str
    thumbnail_url: str | None
    duration_seconds: float
    resolution: str | None
    loop_compatible: bool
    blur_safe: bool
    total_uses: int

    class Config:
        from_attributes = True


class VideoFeedResponse(BaseModel):
    items: list[dict]
    next_cursor: str | None
    has_more: bool


class VideoProgressUpdate(BaseModel):
    video_id: str
    watched_seconds: float
    completed: bool = False
    speed: float = 1.0
    muted: bool = False
    paused_count: int = 0

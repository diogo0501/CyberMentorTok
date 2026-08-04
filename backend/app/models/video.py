import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, JSON, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


def gen_uuid():
    return str(uuid.uuid4())


class Video(Base):
    __tablename__ = "videos"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    lesson_id = Column(String(36), ForeignKey("lessons.id"), nullable=False, index=True)
    background_video_id = Column(String(36), ForeignKey("background_videos.id"), nullable=True)

    url = Column(String(500), nullable=False)
    thumbnail_url = Column(String(500))
    duration_seconds = Column(Float, nullable=False)
    file_size_bytes = Column(Integer)
    resolution = Column(String(20))
    fps = Column(Integer, default=30)
    bitrate = Column(String(20))

    subtitle_url = Column(String(500))
    subtitle_format = Column(String(10), default="srt")

    voice_id = Column(String(36), nullable=True)
    voice_config = Column(JSON)

    status = Column(String(20), default="pending")
    rendering_job_id = Column(String(36), nullable=True)

    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    completions = Column(Integer, default=0)
    average_watch_percent = Column(Float, default=0.0)
    replay_count = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    lesson = relationship("Lesson", back_populates="videos")
    background_video = relationship("BackgroundVideo", back_populates="videos")
    subtitles = relationship("Subtitle", back_populates="video", lazy="selectin")


class BackgroundVideo(Base):
    __tablename__ = "background_videos"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    name = Column(String(200), nullable=False)
    category = Column(String(50), nullable=False, index=True)
    url = Column(String(500), nullable=False)
    thumbnail_url = Column(String(500))
    duration_seconds = Column(Float, nullable=False)
    file_size_bytes = Column(Integer)
    resolution = Column(String(20))
    loop_compatible = Column(Boolean, default=True)
    blur_safe = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)

    total_uses = Column(Integer, default=0)
    average_retention = Column(Float, default=0.0)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    videos = relationship("Video", back_populates="background_video")

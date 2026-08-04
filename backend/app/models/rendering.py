import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, JSON
from app.core.database import Base


def gen_uuid():
    return str(uuid.uuid4())


class RenderingJob(Base):
    __tablename__ = "rendering_jobs"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    lesson_id = Column(String(36), ForeignKey("lessons.id"), nullable=False, index=True)
    video_id = Column(String(36), ForeignKey("videos.id"), nullable=True)

    status = Column(String(20), default="queued")
    priority = Column(Integer, default=5)
    worker_id = Column(String(100))

    background_video_id = Column(String(36), nullable=True)
    voice_config = Column(JSON)
    subtitle_config = Column(JSON)
    render_config = Column(JSON)

    progress_percent = Column(Float, default=0.0)
    current_step = Column(String(50))

    output_url = Column(String(500))
    output_file_size = Column(Integer)
    output_duration = Column(Float)
    output_resolution = Column(String(20))

    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    estimated_completion = Column(DateTime(timezone=True))

    error_message = Column(Text)
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

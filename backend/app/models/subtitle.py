import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


def gen_uuid():
    return str(uuid.uuid4())


class Subtitle(Base):
    __tablename__ = "subtitles"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    video_id = Column(String(36), ForeignKey("videos.id"), nullable=False, index=True)

    start_time_ms = Column(Integer, nullable=False)
    end_time_ms = Column(Integer, nullable=False)
    sequence_number = Column(Integer, nullable=False)

    text = Column(Text, nullable=False)
    speaker = Column(String(20))
    is_keyword = Column(Boolean, default=False)
    keyword_type = Column(String(20))

    position_x = Column(Float, default=0.5)
    position_y = Column(Float, default=0.8)
    font_size = Column(Integer, default=24)
    color = Column(String(10), default="#FFFFFF")
    highlight_color = Column(String(10), default="#00FF00")

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    video = relationship("Video", back_populates="subtitles")

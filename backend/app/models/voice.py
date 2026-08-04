import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, Boolean
from app.core.database import Base


def gen_uuid():
    return str(uuid.uuid4())


class Voice(Base):
    __tablename__ = "voices"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    name = Column(String(100), nullable=False)
    character = Column(String(20), nullable=False)
    provider = Column(String(50))
    voice_id = Column(String(200))
    model = Column(String(100))

    language = Column(String(10), default="en")
    accent = Column(String(50))
    speed = Column(Float, default=1.0)
    pitch = Column(Float, default=1.0)
    stability = Column(Float, default=0.5)
    clarity = Column(Float, default=0.75)

    sample_rate = Column(Integer, default=44100)
    format = Column(String(10), default="mp3")
    target_lufs = Column(Float, default=-14.0)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

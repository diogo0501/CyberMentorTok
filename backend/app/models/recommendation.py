import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, JSON, Integer
from app.core.database import Base


def gen_uuid():
    return str(uuid.uuid4())


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    lesson_id = Column(String(36), ForeignKey("lessons.id"), nullable=False, index=True)

    score = Column(Float, nullable=False)
    reason = Column(String(100))
    algorithm_version = Column(String(20), default="v1")

    based_on_concept = Column(String(36), nullable=True)
    position_in_queue = Column(Integer, default=0)

    shown = Column(DateTime(timezone=True))
    clicked = Column(DateTime(timezone=True))
    completed = Column(DateTime(timezone=True))
    dismissed = Column(DateTime(timezone=True))

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime(timezone=True))

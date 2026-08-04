from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.lesson import Lesson
from app.core.config import get_settings

settings = get_settings()


class FactValidator:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def validate(self, lesson_id) -> dict:
        result = await self.db.execute(select(Lesson).where(Lesson.id == lesson_id))
        lesson = result.scalar_one_or_none()
        if not lesson:
            return {"error": "Lesson not found"}

        checks = {
            "dialogue_structure": self._check_dialogue_structure(lesson),
            "video_structure": self._check_video_structure(lesson),
            "no_lecturing": self._check_no_lecturing(lesson),
        }

        passed = sum(1 for v in checks.values() if v)
        total = len(checks)
        confidence = passed / total if total > 0 else 0.0

        lesson.ai_confidence = confidence
        if confidence >= settings.AI_FACT_CHECK_CONFIDENCE_THRESHOLD:
            lesson.approved = True
        await self.db.commit()

        return {"status": "approved" if lesson.approved else "needs_review", "confidence": confidence, "checks": checks}

    def _check_dialogue_structure(self, lesson: Lesson) -> bool:
        dialogue = lesson.dialogue
        if not dialogue or len(dialogue) < 6:
            return False
        has_peter = any(d["speaker"] == "Peter" for d in dialogue)
        has_stewie = any(d["speaker"] == "Stewie" for d in dialogue)
        alternating = all(dialogue[i]["speaker"] != dialogue[i+1]["speaker"] for i in range(len(dialogue)-1))
        return has_peter and has_stewie and alternating

    def _check_video_structure(self, lesson: Lesson) -> bool:
        return all(getattr(lesson, f) for f in ["hook", "problem", "explanation", "summary"])

    def _check_no_lecturing(self, lesson: Lesson) -> bool:
        dialogue = lesson.dialogue
        peter_asks = sum(1 for d in dialogue if d["speaker"] == "Peter" and "?" in d["text"])
        stewie_explains = sum(1 for d in dialogue if d["speaker"] == "Stewie" and len(d["text"]) > 50)
        return peter_asks >= 2 and stewie_explains >= 3

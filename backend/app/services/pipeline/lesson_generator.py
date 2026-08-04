from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.concept import Concept
from app.models.lesson import Lesson


class LessonGenerator:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate(self, concept_slug: str, difficulty: int = 1) -> dict:
        result = await self.db.execute(select(Concept).where(Concept.slug == concept_slug))
        concept = result.scalar_one_or_none()
        if not concept:
            return {"error": f"Concept '{concept_slug}' not found"}

        from app.services.pipeline.dialogue_generator import DialogueGenerator
        dg = DialogueGenerator(self.db)

        lesson = Lesson(
            concept_id=concept.id,
            title=f"What is {concept.name}?",
            slug=f"{concept.slug}-intro-d{difficulty}",
            description=f"Introduction to {concept.name}",
            difficulty=difficulty,
            hook=f"Did you know that {concept.name} is one of the most important concepts in cybersecurity?",
            problem=f"Most people don't understand how {concept.name} actually works, leaving them vulnerable.",
            explanation=f"Here's what {concept.name} really does and why it matters for security.",
            real_world_example=f"In 2023, a major breach was caused by poor {concept.name} configuration.",
            summary=f"So remember: {concept.name} is fundamental to understanding cybersecurity.",
            curiosity_hook=f"But wait until you see what happens when {concept.name} goes wrong...",
            dialogue=dg._build_dialogue_static(concept.name),
            learning_objectives=[
                f"Understand what {concept.name} is",
                f"Explain why {concept.name} matters for security",
            ],
            quiz_questions=[{
                "question": f"What is the primary purpose of {concept.name}?",
                "answers": [
                    {"id": "a", "text": "To make systems faster", "correct": False},
                    {"id": "b", "text": "To protect against unauthorized access", "correct": True},
                    {"id": "c", "text": "To store data permanently", "correct": False},
                ],
            }],
            estimated_duration_seconds=90,
            ai_generated=True,
            ai_confidence=0.0,
        )
        self.db.add(lesson)
        await self.db.commit()
        await self.db.refresh(lesson)

        return {"status": "generated", "lesson_id": lesson.id, "confidence": 0.0, "validation_needed": True}

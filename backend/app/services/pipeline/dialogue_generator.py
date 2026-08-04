from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.lesson import Lesson


class DialogueGenerator:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate(self, lesson_id) -> dict:
        result = await self.db.execute(select(Lesson).where(Lesson.id == lesson_id))
        lesson = result.scalar_one_or_none()
        if not lesson:
            return {"error": "Lesson not found"}

        dialogue = self._build_dialogue(lesson.title.replace("What is ", "").replace("?", ""))
        lesson.dialogue = dialogue
        await self.db.commit()
        return {"status": "generated", "dialogue": dialogue, "line_count": len(dialogue)}

    def _build_dialogue(self, concept_name: str) -> list[dict]:
        return [
            {"speaker": "Peter", "text": f"Stewie, I know the words {concept_name}, but I don't know what I should picture in my head."},
            {"speaker": "Stewie", "text": f"Good. Start there. {concept_name} is not trivia. It is a way to explain what the system is protecting, what can go wrong, and what control reduces the risk."},
            {"speaker": "Peter", "text": "So instead of memorizing a definition, I should ask what problem it solves?"},
            {"speaker": "Stewie", "text": "Exactly. First ask: what asset matters? Then ask: who could abuse it, how would they reach it, and what evidence would show it happened?"},
            {"speaker": "Peter", "text": "Give me a simple example before my brain starts buffering."},
            {"speaker": "Stewie", "text": f"Imagine a company app. With {concept_name}, you look at login, permissions, data flow, logging, and recovery. Each part either reduces risk or creates a blind spot."},
            {"speaker": "Peter", "text": "So security is not one giant shield. It's a bunch of smaller decisions that have to line up."},
            {"speaker": "Stewie", "text": "Precisely. Authentication proves who you are. Authorization limits what you can do. Encryption protects data. Monitoring tells you when something looks wrong."},
            {"speaker": "Peter", "text": "Where do people usually mess this up?"},
            {"speaker": "Stewie", "text": "They trust defaults, skip logging, give users too much access, and never test recovery. Those are boring mistakes, which is why they keep causing real breaches."},
            {"speaker": "Peter", "text": "What should I remember for a job interview?"},
            {"speaker": "Stewie", "text": f"Explain {concept_name} with three pieces: the risk, the control, and the tradeoff. If you can connect those, you sound like an engineer, not a flashcard."},
            {"speaker": "Peter", "text": "Risk, control, tradeoff. That actually sticks."},
            {"speaker": "Stewie", "text": f"Perfect. One sentence summary: {concept_name} helps you turn vague fear into specific decisions you can design, test, monitor, and improve."},
        ]

    def _build_dialogue_static(self, concept_name: str) -> list[dict]:
        return self._build_dialogue(concept_name)

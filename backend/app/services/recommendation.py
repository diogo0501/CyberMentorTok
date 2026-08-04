"""
Recommendation Engine Service.
Generates personalized content recommendations based on user progress and learning goals.
"""

import json
import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from uuid import UUID
from datetime import datetime, timezone
from app.models.concept import Concept, ConceptPrerequisite
from app.models.lesson import Lesson
from app.models.video import Video
from app.models.progress import UserProgress, ConceptMastery

_BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
_VIDEO_OUTPUT_DIR = os.path.join(_BASE, "video_pipeline", "output")
_BACKGROUNDS_DIR = os.path.join(_BASE, "video_pipeline", "backgrounds")
_FEED_BACKGROUNDS = ("gameplay_01.mp4", "minecraft.mp4")


def _available_backgrounds() -> list[str]:
    if not os.path.isdir(_BACKGROUNDS_DIR):
        return []
    return [
        name
        for name in _FEED_BACKGROUNDS
        if os.path.isfile(os.path.join(_BACKGROUNDS_DIR, name))
    ]


class RecommendationService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self._bg_index = 0

    def _mask_url_for(self, lesson_id: str) -> str | None:
        mask_path = os.path.join(_VIDEO_OUTPUT_DIR, lesson_id[:8], "mask.webm")
        return f"/videos/{lesson_id[:8]}/mask.webm" if os.path.isfile(mask_path) else None

    def _audio_url_for(self, lesson_id: str) -> str | None:
        audio_path = os.path.join(_VIDEO_OUTPUT_DIR, lesson_id[:8], "audio.mp3")
        return f"/videos/{lesson_id[:8]}/audio.mp3" if os.path.isfile(audio_path) else None

    def _timing_for(self, lesson_id: str) -> list[dict]:
        """Per-line timing (speaker, text, start_s, end_s) from timing.json."""
        timing_path = os.path.join(_VIDEO_OUTPUT_DIR, lesson_id[:8], "timing.json")
        if not os.path.isfile(timing_path):
            return []
        try:
            with open(timing_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("timeline", [])
        except Exception:
            return []

    def _background_url(self) -> str | None:
        backgrounds = _available_backgrounds()
        if not backgrounds:
            return None
        idx = self._bg_index % len(backgrounds)
        self._bg_index += 1
        return f"/backgrounds/{backgrounds[idx]}"

    async def get_feed(
        self, user_id: UUID, cursor: str | None = None,
        category: str | None = None, difficulty: int | None = None,
        limit: int = 10,
    ) -> dict:
        # Get user's mastered concepts
        mastery_result = await self.db.execute(
            select(ConceptMastery.concept_id).where(
                ConceptMastery.user_id == user_id,
                ConceptMastery.status.in_(["mastered", "learning", "practicing"]),
            )
        )
        mastered_ids = {row[0] for row in mastery_result.all()}

        # Find next recommended concepts
        concepts = await self._get_recommended_concepts(mastered_ids, category, difficulty, limit)

        items = []
        for concept in concepts:
            lesson_result = await self.db.execute(
                select(Lesson).where(
                    Lesson.concept_id == concept.id,
                    Lesson.deleted_at.is_(None),
                ).order_by(Lesson.difficulty.asc()).limit(1)
            )
            lesson = lesson_result.scalars().first()
            if not lesson:
                continue

            video_result = await self.db.execute(
                select(Video).where(
                    Video.lesson_id == lesson.id,
                    Video.status == "ready",
                ).limit(1)
            )
            video = video_result.scalars().first()

            # Only include video lessons - skip text-only lessons
            if not video:
                continue

            progress_result = await self.db.execute(
                select(UserProgress).where(
                    UserProgress.user_id == user_id,
                    UserProgress.lesson_id == lesson.id,
                )
            )
            progress = progress_result.scalars().first()

            items.append({
                "lesson_id": str(lesson.id),
                "concept": concept.name,
                "concept_slug": concept.slug,
                "title": lesson.title,
                "difficulty": lesson.difficulty,
                "category": concept.category,
                "video_url": video.url if video else None,
                "mask_url": self._mask_url_for(lesson.id),
                "audio_url": self._audio_url_for(lesson.id),
                "background_url": self._background_url(),
                "timing": self._timing_for(lesson.id),
                "thumbnail_url": video.thumbnail_url if video else None,
                "progress": {
                    "status": progress.status if progress else "locked",
                    "watch_progress": progress.watch_progress if progress else 0.0,
                    "completed": progress.completed if progress else False,
                } if progress else None,
                "reason": self._get_recommendation_reason(concept, mastered_ids),
            })

        return {
            "items": items,
            "next_cursor": str(concepts[-1].id) if concepts else None,
            "has_more": len(concepts) == limit,
        }

    async def get_anonymous_feed(
        self, cursor: str | None = None,
        category: str | None = None, difficulty: int | None = None,
        concept_id: str | None = None, limit: int = 10,
    ) -> dict:
        # Only published lessons that have a ready video (video lessons only)
        query = (
            select(Lesson)
            .join(Concept, Concept.id == Lesson.concept_id)
            .join(Video, and_(Video.lesson_id == Lesson.id, Video.status == "ready"))
            .where(
                Lesson.deleted_at.is_(None),
                Concept.is_published == True,
            )
        )
        if category:
            query = query.where(Concept.category == category)
        if concept_id:
            query = query.where(Lesson.concept_id == concept_id)
        if difficulty is not None:
            query = query.where(Lesson.difficulty == difficulty)
        if cursor:
            query = query.where(Lesson.id > cursor)
        query = query.order_by(Lesson.difficulty.asc(), Lesson.id.asc()).limit(limit)

        result = await self.db.execute(query)
        lessons = result.scalars().all()

        items = []
        for lesson in lessons:
            concept_result = await self.db.execute(
                select(Concept).where(Concept.id == lesson.concept_id)
            )
            concept = concept_result.scalars().first()

            video_result = await self.db.execute(
                select(Video).where(
                    Video.lesson_id == lesson.id,
                    Video.status == "ready",
                ).limit(1)
            )
            video = video_result.scalars().first()
            if not video:
                continue

            items.append({
                "id": str(lesson.id),
                "lesson_id": str(lesson.id),
                "concept_id": str(lesson.concept_id),
                "concept": concept.name if concept else "",
                "concept_slug": concept.slug if concept else "",
                "title": lesson.title,
                "slug": lesson.slug,
                "description": lesson.description,
                "difficulty": lesson.difficulty,
                "category": concept.category if concept else "",
                "hook": lesson.hook,
                "dialogue": lesson.dialogue,
                "learning_objectives": lesson.learning_objectives,
                "quiz_questions": lesson.quiz_questions,
                "estimated_duration_seconds": lesson.estimated_duration_seconds,
                "total_watches": lesson.total_watches,
                "average_completion": lesson.average_completion,
                "video_url": video.url,
                "mask_url": self._mask_url_for(lesson.id),
                "audio_url": self._audio_url_for(lesson.id),
                "background_url": self._background_url(),
                "timing": self._timing_for(lesson.id),
                "thumbnail_url": video.thumbnail_url,
            })

        return {
            "items": items,
            "next_cursor": str(lessons[-1].id) if len(lessons) == limit else None,
            "has_more": len(lessons) == limit,
        }

    async def _get_recommended_concepts(
        self, mastered_ids: set, category: str | None = None,
        difficulty: int | None = None, limit: int = 10,
    ) -> list[Concept]:
        # Get all concepts where all prerequisites are mastered
        all_concepts = await self.db.execute(select(Concept).where(Concept.is_published == True))
        all_concepts_list = all_concepts.scalars().all()

        recommended = []
        for concept in all_concepts_list:
            if category and concept.category != category:
                continue
            if difficulty and concept.difficulty != difficulty:
                continue

            prereq_result = await self.db.execute(
                select(ConceptPrerequisite.prerequisite_id).where(
                    ConceptPrerequisite.concept_id == concept.id,
                    ConceptPrerequisite.is_required == True,
                )
            )
            prereq_ids = {row[0] for row in prereq_result.all()}

            if prereq_ids.issubset(mastered_ids) or not prereq_ids:
                if concept.id not in mastered_ids:
                    recommended.append(concept)

        recommended.sort(key=lambda c: (c.difficulty, c.category))
        return recommended[:limit]

    def _get_recommendation_reason(self, concept: Concept, mastered_ids: set) -> str:
        if concept.difficulty <= 2:
            return "beginner_path"
        elif concept.difficulty <= 4:
            return "intermediate_path"
        else:
            return "advanced_path"

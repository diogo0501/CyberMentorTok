"""
Progress Tracking Service.
Manages learning progress, mastery scores, and spaced repetition.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID
from datetime import datetime, timezone, timedelta
from app.models.progress import UserProgress, ConceptMastery
from app.models.user import User
from app.models.concept import Concept, ConceptPrerequisite
from app.models.lesson import Lesson
from app.schemas.progress import ProgressUpdate, ProgressResponse, MasteryResponse, LearningDashboard


class ProgressService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_lesson_progress(self, user_id: UUID, lesson_id: UUID) -> ProgressResponse:
        result = await self.db.execute(
            select(UserProgress).where(
                UserProgress.user_id == user_id,
                UserProgress.lesson_id == lesson_id,
            )
        )
        progress = result.scalars().first()
        if not progress:
            return ProgressResponse(
                lesson_id=lesson_id,
                status="locked",
                watch_progress=0.0,
                completed=False,
                watch_count=0,
                confidence_score=0.0,
                mastery_level="locked",
                best_quiz_score=0.0,
                next_review_at=None,
                time_spent_seconds=0.0,
            )
        return ProgressResponse.model_validate(progress)

    async def update_lesson_progress(self, user_id: UUID, data: ProgressUpdate) -> ProgressResponse:
        result = await self.db.execute(
            select(UserProgress).where(
                UserProgress.user_id == user_id,
                UserProgress.lesson_id == data.lesson_id,
            )
        )
        progress = result.scalars().first()

        if not progress:
            progress = UserProgress(
                user_id=user_id,
                lesson_id=data.lesson_id,
                video_id=data.video_id,
                status="learning",
                first_watched_at=datetime.now(timezone.utc),
            )
            self.db.add(progress)

        progress.watch_progress = max(progress.watch_progress, data.watch_progress)
        progress.completed = data.completed or progress.completed
        progress.time_spent_seconds += data.time_spent_seconds
        progress.last_watched_at = datetime.now(timezone.utc)
        progress.watch_count += 1

        if data.completed:
            progress.status = "practicing"
            progress.confidence_score = min(100, progress.confidence_score + 20)

        # Update streak
        user_result = await self.db.execute(select(User).where(User.id == user_id))
        user = user_result.scalar_one()
        today = datetime.now(timezone.utc).date()
        if user.last_active_date and user.last_active_date.date() == today - timedelta(days=1):
            user.current_streak += 1
        elif user.last_active_date and user.last_active_date.date() != today:
            user.current_streak = 1
        user.last_active_date = datetime.now(timezone.utc)
        user.longest_streak = max(user.longest_streak, user.current_streak)

        # Award XP
        if data.completed:
            user.xp += 10
        user.total_hours_learned += data.time_spent_seconds / 3600

        await self.db.commit()
        await self.db.refresh(progress)
        return ProgressResponse.model_validate(progress)

    async def update_video_progress(self, user_id: UUID, video_id: UUID, data) -> dict:
        result = await self.db.execute(
            select(UserProgress).where(
                UserProgress.user_id == user_id,
                UserProgress.video_id == video_id,
            )
        )
        progress = result.scalars().first()

        if progress:
            progress.watch_progress = max(progress.watch_progress, data.watched_seconds / max(progress.time_spent_seconds, 1))
            progress.last_watched_at = datetime.now(timezone.utc)
        else:
            lesson_result = await self.db.execute(
                select(Video).where(Video.id == video_id)
            )
            video = lesson_result.scalars().first()
            if video:
                progress = UserProgress(
                    user_id=user_id,
                    lesson_id=video.lesson_id,
                    video_id=video_id,
                    status="learning",
                    watch_progress=min(1.0, data.watched_seconds / max(video.duration_seconds, 1)),
                    first_watched_at=datetime.now(timezone.utc),
                )
                self.db.add(progress)

        await self.db.commit()
        return {"status": "updated"}

    async def get_concept_mastery(self, user_id: UUID, concept_id: UUID) -> MasteryResponse:
        result = await self.db.execute(
            select(ConceptMastery).where(
                ConceptMastery.user_id == user_id,
                ConceptMastery.concept_id == concept_id,
            )
        )
        mastery = result.scalars().first()

        if not mastery:
            return MasteryResponse(
                concept_id=concept_id,
                status="locked",
                confidence_score=0.0,
                lessons_completed=0,
                total_lessons=0,
                completion_percent=0.0,
                average_quiz_score=0.0,
                next_review_at=None,
            )
        return MasteryResponse.model_validate(mastery)

    async def update_quiz_result(
        self, user_id: UUID, lesson_id: UUID,
        concept_id: UUID, is_correct: bool,
    ) -> float:
        result = await self.db.execute(
            select(ConceptMastery).where(
                ConceptMastery.user_id == user_id,
                ConceptMastery.concept_id == concept_id,
            )
        )
        mastery = result.scalars().first()

        if not mastery:
            mastery = ConceptMastery(
                user_id=user_id,
                concept_id=concept_id,
                status="learning",
            )
            self.db.add(mastery)

        confidence_change = 10.0 if is_correct else -5.0
        mastery.confidence_score = max(0, min(100, mastery.confidence_score + confidence_change))
        mastery.review_count += 1
        mastery.last_reviewed_at = datetime.now(timezone.utc)

        # Spaced repetition: increase interval based on performance
        days_until_review = min(30, 2 ** (mastery.review_count // 3))
        mastery.next_review_at = datetime.now(timezone.utc) + timedelta(days=days_until_review)

        # Update mastery level
        if mastery.confidence_score >= 80:
            mastery.status = "mastered"
        elif mastery.confidence_score >= 50:
            mastery.status = "practicing"
        elif mastery.confidence_score < 20:
            mastery.status = "needs_review"

        # Update quiz stats
        total_quizzes = mastery.review_count
        current_avg = mastery.average_quiz_score
        mastery.average_quiz_score = ((current_avg * (total_quizzes - 1)) + (100 if is_correct else 0)) / total_quizzes

        await self.db.commit()
        return confidence_change

    async def get_dashboard(self, user_id: UUID) -> LearningDashboard:
        user_result = await self.db.execute(select(User).where(User.id == user_id))
        user = user_result.scalar_one()

        mastery_result = await self.db.execute(
            select(ConceptMastery).where(ConceptMastery.user_id == user_id)
        )
        masteries = mastery_result.scalars().all()

        mastered_count = sum(1 for m in masteries if m.status == "mastered")
        in_progress_count = sum(1 for m in masteries if m.status in ["learning", "practicing"])

        progress_result = await self.db.execute(
            select(UserProgress).where(
                UserProgress.user_id == user_id,
                UserProgress.last_watched_at >= datetime.now(timezone.utc) - timedelta(days=7),
            )
        )
        recent = progress_result.scalars().all()

        reviews = [m for m in masteries if m.next_review_at and m.next_review_at <= datetime.now(timezone.utc) + timedelta(days=7)]

        daily_goal_minutes = user.daily_goal_minutes or 15
        today_seconds = sum(p.time_spent_seconds for p in recent if p.last_watched_at and p.last_watched_at.date() == datetime.now(timezone.utc).date())
        daily_progress = min(1.0, (today_seconds / 60) / daily_goal_minutes)

        return LearningDashboard(
            total_hours_learned=user.total_hours_learned,
            concepts_mastered=mastered_count,
            concepts_in_progress=in_progress_count,
            current_streak=user.current_streak,
            daily_goal_progress=daily_progress,
            recent_activity=[
                {
                    "lesson_id": str(p.lesson_id),
                    "status": p.status,
                    "completed": p.completed,
                    "watch_progress": p.watch_progress,
                    "timestamp": p.last_watched_at.isoformat() if p.last_watched_at else None,
                }
                for p in recent[:10]
            ],
            upcoming_reviews=[
                {
                    "concept_id": str(m.concept_id),
                    "review_at": m.next_review_at.isoformat(),
                    "confidence": m.confidence_score,
                }
                for m in reviews[:5]
            ],
            recommended_next=[],
            domain_breakdown=[],
            weekly_heatmap=[[0] * 24 for _ in range(7)],
        )

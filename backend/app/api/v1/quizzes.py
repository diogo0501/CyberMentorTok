from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.quiz import Quiz, QuizAttempt
from app.schemas.quiz import QuizResponse, QuizSubmit, QuizResult
from app.api.v1.deps import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/lesson/{lesson_id}", response_model=list[QuizResponse])
async def get_quizzes_for_lesson(lesson_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Quiz).where(Quiz.lesson_id == lesson_id, Quiz.is_active == True))
    return result.scalars().all()


@router.post("/submit", response_model=QuizResult)
async def submit_quiz(
    data: QuizSubmit,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(select(Quiz).where(Quiz.id == data.quiz_id))
    quiz = result.scalar_one_or_none()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    correct_answer = next((a["id"] for a in quiz.answers if a.get("correct")), None)
    is_correct = data.selected_answer == correct_answer

    attempt = QuizAttempt(
        user_id=user.id,
        quiz_id=quiz.id,
        lesson_id=quiz.lesson_id,
        selected_answer=data.selected_answer,
        is_correct=is_correct,
        time_taken_seconds=data.time_taken_seconds,
    )
    db.add(attempt)

    quiz.total_attempts += 1
    if is_correct:
        quiz.correct_attempts += 1

    xp_earned = 10 if is_correct else 2

    from app.services.progress import ProgressService
    service = ProgressService(db)
    confidence_change = await service.update_quiz_result(
        user_id=user.id,
        lesson_id=quiz.lesson_id,
        concept_id=quiz.concept_id,
        is_correct=is_correct,
    )

    await db.commit()

    return QuizResult(
        is_correct=is_correct,
        correct_answer=correct_answer or "",
        explanation=quiz.explanation,
        confidence_change=confidence_change,
        next_review_scheduled=None,
        streak_maintained=is_correct,
        xp_earned=xp_earned,
    )


@router.get("/random/{concept_id}", response_model=QuizResponse)
async def get_random_quiz(concept_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Quiz).where(Quiz.concept_id == concept_id, Quiz.is_active == True).order_by(Quiz.total_attempts.asc())
    )
    quiz = result.scalars().first()
    if not quiz:
        raise HTTPException(status_code=404, detail="No quizzes available for this concept")
    return quiz

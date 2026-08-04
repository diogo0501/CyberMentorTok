from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func, and_
from app.core.database import get_db
from app.models.concept import Concept
from app.models.lesson import Lesson
from app.models.video import Video

router = APIRouter()


@router.get("/")
async def search(
    q: str = Query(..., min_length=1),
    type: str = Query(default="all"),
    limit: int = Query(default=20, le=50),
    db: AsyncSession = Depends(get_db),
):
    results = []

    if type in ("all", "concepts"):
        concept_query = select(Concept).where(
            Concept.is_published == True,
            Concept.deleted_at.is_(None),
            or_(
                Concept.name.ilike(f"%{q}%"),
                Concept.description.ilike(f"%{q}%"),
            )
        ).limit(limit)
        concept_result = await db.execute(concept_query)
        concepts = concept_result.scalars().all()
        results.extend([
            {"type": "concept", "id": c.id, "name": c.name, "slug": c.slug, "category": c.category, "difficulty": c.difficulty}
            for c in concepts
        ])

    if type in ("all", "lessons"):
        lesson_query = (
            select(Lesson)
            .join(Video, and_(Video.lesson_id == Lesson.id, Video.status == "ready"))
            .where(
                Lesson.deleted_at.is_(None),
                or_(
                    Lesson.title.ilike(f"%{q}%"),
                    Lesson.description.ilike(f"%{q}%"),
                ),
            )
            .distinct()
            .limit(limit)
        )
        lesson_result = await db.execute(lesson_query)
        lessons = lesson_result.scalars().all()

        if lessons:
            lesson_ids = [l.id for l in lessons]
            video_result = await db.execute(
                select(Video).where(
                    Video.lesson_id.in_(lesson_ids),
                    Video.status == "ready",
                )
            )
            video_by_lesson = {}
            for v in video_result.scalars().all():
                video_by_lesson.setdefault(v.lesson_id, v)

            concept_ids = {l.concept_id for l in lessons}
            concept_result = await db.execute(
                select(Concept.id, Concept.name, Concept.category).where(Concept.id.in_(concept_ids))
            )
            concept_info = {row[0]: {"name": row[1], "category": row[2]} for row in concept_result.all()}

            results.extend([
                {
                    "type": "lesson",
                    "id": l.id,
                    "title": l.title,
                    "concept_id": l.concept_id,
                    "concept": concept_info.get(l.concept_id, {}).get("name", ""),
                    "category": concept_info.get(l.concept_id, {}).get("category", ""),
                    "difficulty": l.difficulty,
                    "video_url": video_by_lesson.get(l.id).url if video_by_lesson.get(l.id) else None,
                }
                for l in lessons
            ])

    return {"results": results[:limit], "query": q, "total": len(results)}


@router.get("/categories")
async def search_categories(
    db: AsyncSession = Depends(get_db),
):
    """List concept categories with counts of published concepts and ready video lessons."""
    concept_rows = (
        select(Concept.category, func.count(Concept.id))
        .where(
            Concept.is_published == True,
            Concept.deleted_at.is_(None),
            Concept.category.isnot(None),
        )
        .group_by(Concept.category)
    )
    concept_result = await db.execute(concept_rows)
    concept_counts = dict(concept_result.all())

    video_rows = (
        select(Concept.category, func.count(Video.id))
        .select_from(Video)
        .join(Lesson, Lesson.id == Video.lesson_id)
        .join(Concept, Concept.id == Lesson.concept_id)
        .where(
            Video.status == "ready",
            Lesson.deleted_at.is_(None),
            Concept.is_published == True,
        )
        .group_by(Concept.category)
    )
    video_result = await db.execute(video_rows)
    video_counts = dict(video_result.all())

    categories = []
    for category, concept_count in concept_counts.items():
        categories.append({
            "name": category,
            "concept_count": concept_count,
            "video_count": video_counts.get(category, 0),
        })

    categories.sort(key=lambda c: (-c["video_count"], c["name"]))
    return {"categories": categories}


@router.get("/autocomplete")
async def autocomplete(
    q: str = Query(..., min_length=1),
    limit: int = Query(default=10, le=20),
    db: AsyncSession = Depends(get_db),
):
    concept_query = select(Concept.name, Concept.slug).where(
        Concept.is_published == True,
        Concept.name.ilike(f"%{q}%"),
    ).limit(limit)
    result = await db.execute(concept_query)
    suggestions = [{"name": row[0], "slug": row[1]} for row in result.all()]
    return {"suggestions": suggestions}

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.concept import Concept, ConceptPrerequisite
from app.schemas.concept import ConceptCreate, ConceptResponse, ConceptWithPrerequisites, ConceptGraph
from app.api.v1.deps import get_current_user, get_current_admin_user
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=list[ConceptResponse])
async def list_concepts(
    category: str | None = None,
    difficulty: int | None = None,
    domain: str | None = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    query = select(Concept).where(Concept.is_published == True, Concept.deleted_at.is_(None))
    if category:
        query = query.where(Concept.category == category)
    if difficulty:
        query = query.where(Concept.difficulty == difficulty)
    if domain:
        query = query.where(Concept.domain == domain)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/graph", response_model=ConceptGraph)
async def get_knowledge_graph(
    category: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    from app.services.knowledge_graph.graph import KnowledgeGraphService
    service = KnowledgeGraphService(db)
    return await service.get_graph(category=category)


@router.get("/{concept_id}", response_model=ConceptWithPrerequisites)
async def get_concept(concept_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Concept).where(Concept.id == concept_id, Concept.deleted_at.is_(None)))
    concept = result.scalar_one_or_none()
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")

    prereqs_result = await db.execute(
        select(ConceptPrerequisite).where(ConceptPrerequisite.concept_id == concept_id)
    )
    prereq_ids = [p.prerequisite_id for p in prereqs_result.scalars().all()]

    prereqs = []
    if prereq_ids:
        prereqs_result = await db.execute(select(Concept).where(Concept.id.in_(prereq_ids)))
        prereqs = prereqs_result.scalars().all()

    deps_result = await db.execute(
        select(ConceptPrerequisite).where(ConceptPrerequisite.prerequisite_id == concept_id)
    )
    dep_ids = [p.concept_id for p in deps_result.scalars().all()]

    dependents = []
    if dep_ids:
        deps_result = await db.execute(select(Concept).where(Concept.id.in_(dep_ids)))
        dependents = deps_result.scalars().all()

    return ConceptWithPrerequisites(
        **ConceptResponse.model_validate(concept).model_dump(),
        prerequisites=[ConceptResponse.model_validate(p) for p in prereqs],
        dependents=[ConceptResponse.model_validate(d) for d in dependents],
    )


@router.post("/", response_model=ConceptResponse, status_code=201)
async def create_concept(
    data: ConceptCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
):
    concept = Concept(**data.model_dump())
    db.add(concept)
    await db.flush()

    for prereq_id in data.prerequisite_ids:
        edge = ConceptPrerequisite(concept_id=concept.id, prerequisite_id=prereq_id)
        db.add(edge)

    await db.commit()
    await db.refresh(concept)
    return concept

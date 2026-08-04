from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.concept import Concept, ConceptPrerequisite
from app.schemas.concept import ConceptGraph, ConceptResponse


class KnowledgeGraphService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_graph(self, category: str | None = None) -> ConceptGraph:
        query = select(Concept).where(Concept.is_published == True, Concept.deleted_at.is_(None))
        if category:
            query = query.where(Concept.category == category)
        result = await self.db.execute(query)
        concepts = result.scalars().all()

        edges_result = await self.db.execute(select(ConceptPrerequisite))
        edges = edges_result.scalars().all()

        return ConceptGraph(
            concepts=[ConceptResponse.model_validate(c) for c in concepts],
            edges=[
                {
                    "from": e.prerequisite_id,
                    "to": e.concept_id,
                    "type": "required" if e.is_required else "recommended",
                }
                for e in edges
            ],
        )

    async def get_prerequisites(self, concept_id) -> list[Concept]:
        result = await self.db.execute(
            select(Concept).join(ConceptPrerequisite, ConceptPrerequisite.prerequisite_id == Concept.id)
            .where(ConceptPrerequisite.concept_id == concept_id)
        )
        return result.scalars().all()

    async def get_dependents(self, concept_id) -> list[Concept]:
        result = await self.db.execute(
            select(Concept).join(ConceptPrerequisite, ConceptPrerequisite.concept_id == Concept.id)
            .where(ConceptPrerequisite.prerequisite_id == concept_id)
        )
        return result.scalars().all()

    async def get_next_concepts(self, user_id, mastered_concept_ids: list) -> list[Concept]:
        result = await self.db.execute(select(Concept).where(Concept.is_published == True))
        all_concepts = result.scalars().all()

        next_concepts = []
        mastered_set = set(mastered_concept_ids)

        for concept in all_concepts:
            if concept.id in mastered_set:
                continue

            prereqs = await self.get_prerequisites(concept.id)
            prereq_ids = {p.id for p in prereqs}

            if prereq_ids.issubset(mastered_set):
                next_concepts.append(concept)

        return sorted(next_concepts, key=lambda c: c.difficulty)[:10]

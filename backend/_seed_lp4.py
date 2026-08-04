"""Seed SC-100 LP4 lessons into the DB (standalone, no server needed)."""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import async_session, init_db
from app.services.knowledge_graph.seed import seed_knowledge_graph
from app.services.knowledge_graph.seed_lessons import seed_lessons


async def main() -> None:
    await init_db()
    async with async_session() as db:
        await seed_knowledge_graph(db)
        result = await seed_lessons(db)
        print(result)


if __name__ == "__main__":
    asyncio.run(main())

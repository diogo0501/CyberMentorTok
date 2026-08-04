"""
Seed the database with initial knowledge graph data.
Run: python -m scripts.seed_db
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.core.database import async_session, init_db
from app.services.knowledge_graph.seed import seed_knowledge_graph


async def main():
    await init_db()
    async with async_session() as db:
        result = await seed_knowledge_graph(db)
        print(f"Seeding result: {result}")


if __name__ == "__main__":
    asyncio.run(main())

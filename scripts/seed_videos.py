"""
Register video pipeline output into the database and remove text-only lessons.

For every lesson that has a rendered `full.mp4` in `video_pipeline/output/{lesson_id[:8]}/`,
a `Video` record is created/updated with status "ready" so the feed can serve it.

Lessons WITHOUT a rendered video (text/audio-only) are soft-deleted so the app
only shows video lessons.

Run: python -m scripts.seed_videos
"""
import asyncio
import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Pin the database to the backend copy regardless of CWD. The default
# DATABASE_URL is relative ("./cybermentortok.db"), so running this script from
# the repo root would otherwise open/create a wrong, duplicate DB.
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
os.environ['DATABASE_URL'] = f"sqlite+aiosqlite:///{os.path.join(BACKEND_DIR, 'cybermentortok.db').replace(os.sep, '/')}"

from sqlalchemy import select

from app.core.database import async_session, init_db
from app.models.lesson import Lesson
from app.models.video import Video

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUTPUT_DIR = os.path.join(BASE_DIR, 'video_pipeline', 'output')


def _read_duration(lesson_dir: str) -> float:
    timing_path = os.path.join(lesson_dir, 'timing.json')
    if os.path.isfile(timing_path):
        try:
            with open(timing_path, 'r', encoding='utf-8') as f:
                timing = json.load(f)
            total = timing.get('total_duration')
            if total:
                return float(total)
        except Exception:
            pass
    return 90.0


async def seed_videos() -> None:
    await init_db()
    async with async_session() as db:
        result = await db.execute(
            select(Lesson).where(Lesson.deleted_at.is_(None))
        )
        lessons = result.scalars().all()
        by_prefix = {lesson.id[:8]: lesson for lesson in lessons}

        created = 0
        updated = 0
        soft_deleted = 0
        now = datetime.now(timezone.utc)

        for prefix, lesson in by_prefix.items():
            lesson_dir = os.path.join(OUTPUT_DIR, prefix)
            full_path = os.path.join(lesson_dir, 'full.mp4')

            if os.path.isfile(full_path):
                url = f"/videos/{prefix}/full.mp4"
                duration = _read_duration(lesson_dir)

                existing = await db.execute(
                    select(Video).where(Video.lesson_id == lesson.id)
                )
                video = existing.scalars().first()

                if video:
                    video.url = url
                    video.status = 'ready'
                    video.duration_seconds = duration
                    updated += 1
                else:
                    db.add(Video(
                        lesson_id=lesson.id,
                        url=url,
                        status='ready',
                        duration_seconds=duration,
                        resolution='1080x1920',
                        fps=30,
                    ))
                    created += 1
            else:
                # Text/audio-only lesson with no rendered video -> remove it
                lesson.deleted_at = now
                soft_deleted += 1

        await db.commit()

        print(f"Videos created: {created}")
        print(f"Videos updated: {updated}")
        print(f"Text lessons soft-deleted: {soft_deleted}")
        print(f"Lessons remaining (non-deleted): {len(lessons) - soft_deleted}")


if __name__ == "__main__":
    asyncio.run(seed_videos())

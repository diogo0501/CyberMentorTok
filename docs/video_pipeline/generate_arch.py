"""Generate full composites (full.mp4 + mask.webm) for the architecture lessons
(sc100_arch_lessons.py). Run with the SYSTEM python (has edge_tts):
    python video_pipeline/generate_arch.py
"""

import asyncio
import json
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate_video import OUTPUT_DIR, generate_from_dialogue
from sc100_arch_lessons import LESSONS

DESKTOP_VIDEO = r"C:\Users\diogo\Desktop\Download.mp4"
DB_PATH = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend", "cybermentortok.db")
)


def db_ids_by_slug() -> dict:
    con = sqlite3.connect(DB_PATH)
    try:
        rows = con.execute("SELECT id, slug FROM lessons").fetchall()
    finally:
        con.close()
    return {slug: lesson_id for lesson_id, slug in rows}


def write_metadata(output_dir: str, lesson: dict) -> None:
    metadata = {
        "title": lesson["title"],
        "hook": lesson.get("hook"),
        "slug": lesson["slug"],
        "concept": lesson.get("concept_slug"),
        "category": lesson.get("category") or lesson.get("concept_slug"),
        "difficulty": lesson.get("difficulty"),
        "description": lesson.get("description"),
        "source": "cybersecurity-architecture awesome-list expansion",
    }
    with open(os.path.join(output_dir, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)


async def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    ids = db_ids_by_slug()
    for lesson in LESSONS:
        slug = lesson["slug"]
        lesson_id = ids.get(slug)
        if not lesson_id:
            print(f"SKIP (no DB row): {slug}")
            continue
        output_dir = os.path.join(OUTPUT_DIR, lesson_id[:8])
        os.makedirs(output_dir, exist_ok=True)

        print(f"\n=== {lesson['title']} -> {output_dir} ===")
        try:
            await generate_from_dialogue(
                dialogue=lesson["dialogue"],
                lesson_title=lesson["title"],
                output_dir=output_dir,
                background_video=DESKTOP_VIDEO,
                mask_only=False,
            )
            write_metadata(output_dir, lesson)
            print("OK")
        except Exception as e:  # noqa: BLE001
            print(f"FAILED: {e}")


if __name__ == "__main__":
    asyncio.run(main())

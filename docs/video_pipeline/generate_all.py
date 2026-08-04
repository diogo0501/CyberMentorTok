"""Batch-generate masks (and optionally full composites) for all lessons."""

import asyncio
import os
import sys
import httpx

sys.path.insert(0, r"C:\Users\diogo\CyberMentorTok\video_pipeline")
from generate_video import generate_from_dialogue

DESKTOP_BG = r"C:\Users\diogo\Desktop\Download.mp4"
OUTPUT_DIR = r"C:\Users\diogo\CyberMentorTok\video_pipeline\output"


async def main():
    mask_only = "--mask-only" in sys.argv

    async with httpx.AsyncClient() as c:
        lessons = (await c.get("http://localhost:8000/api/v1/lessons/?limit=200")).json()

    total = len(lessons)
    generated = 0
    skipped = 0
    failed = 0

    for i, lesson in enumerate(lessons):
        lid = lesson["id"][:8]
        title = lesson["title"]
        lesson_dir = os.path.join(OUTPUT_DIR, lid)

        timing_path = os.path.join(lesson_dir, "timing.json")
        if os.path.exists(timing_path):
            print(f"  [{i+1}/{total}] SKIP: {title}")
            skipped += 1
            continue

        print(f"\n[{i+1}/{total}] === {title} ===")
        try:
            await generate_from_dialogue(
                dialogue=lesson["dialogue"],
                lesson_title=title,
                output_dir=lesson_dir,
                background_video=DESKTOP_BG if not mask_only else None,
                mask_only=mask_only,
            )
            generated += 1
        except Exception as e:
            print(f"  FAILED: {e}")
            failed += 1

    print(f"\n{'='*50}")
    print(f"Results: {generated} generated, {skipped} skipped, {failed} failed (total: {total})")


if __name__ == "__main__":
    asyncio.run(main())

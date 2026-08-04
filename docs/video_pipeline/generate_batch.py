import asyncio
import os
import sys
import httpx

sys.path.insert(0, r"C:\Users\diogo\CyberMentorTok\video_pipeline")
from generate_video import generate_from_dialogue

DESKTOP_BG = r"C:\Users\diogo\Desktop\Download.mp4"
OUTPUT_DIR = r"C:\Users\diogo\CyberMentorTok\video_pipeline\output"

async def main():
    async with httpx.AsyncClient() as c:
        lessons = (await c.get("http://localhost:8000/api/v1/lessons/")).json()[:5]

    for lesson in lessons:
        lid = lesson["id"][:8]
        title = lesson["title"]
        out = os.path.join(OUTPUT_DIR, f"{lid}.mp4")

        if os.path.exists(out):
            print(f"  SKIP: {title} (already exists)")
            continue

        print(f"\n=== Generating: {title} ===")
        await generate_from_dialogue(lesson["dialogue"], title, out, DESKTOP_BG)

if __name__ == "__main__":
    asyncio.run(main())

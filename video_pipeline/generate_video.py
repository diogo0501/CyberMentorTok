"""CyberMentorTok Video Generator

Creates TikTok-style vertical videos with Peter/Stewie dialogue.
Produces two outputs per lesson:
  - full.mp4  — baked composite (background + characters + subs + audio)
  - mask.webm — transparent overlay (characters + subs + audio), works with any BG

Usage:
    python generate_video.py --lesson-json lesson.json
    python generate_video.py --lesson-id <uuid>
    python generate_video.py --demo
    python generate_video.py --mask-only --lesson-id <uuid>
"""

import argparse
import asyncio
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tts_generator import generate_dialogue_audio, concatenate_audio, timeline_to_seconds
from compositor import compose_video
from mask_generator import generate_mask

PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(PIPELINE_DIR, "temp")
OUTPUT_DIR = os.path.join(PIPELINE_DIR, "output")

API_BASE = "http://localhost:8000/api/v1"
DESKTOP_VIDEO = r"C:\Users\diogo\Desktop\Download.mp4"

DEMO_LESSON = {
    "id": "demo-001",
    "title": "What is DNS?",
    "dialogue": [
        {"speaker": "Peter", "text": "Hey Stewie, what exactly is DNS?"},
        {"speaker": "Stewie", "text": "Peter, DNS is like the phonebook of the internet. When you type google.com, DNS translates it to an IP address."},
        {"speaker": "Peter", "text": "So it's like when I look up a number in the yellow pages?"},
        {"speaker": "Stewie", "text": "Exactly! But here's the thing - if someone poisons that phonebook, they can redirect you to a fake website."},
        {"speaker": "Peter", "text": "Wait, that sounds dangerous!"},
        {"speaker": "Stewie", "text": "It is. DNS poisoning is a real attack vector. That's why DNSSEC was created - to digitally sign DNS records."},
        {"speaker": "Peter", "text": "Is this something I need to worry about at home?"},
        {"speaker": "Stewie", "text": "Absolutely. Use encrypted DNS like DoH or DoT. Your ISP can see every domain you visit through plain DNS queries."},
    ],
}


async def generate_from_dialogue(
    dialogue: list[dict],
    lesson_title: str,
    output_dir: str,
    background_video: str | None = None,
    mask_only: bool = False,
) -> dict:
    """Generate video(s) from dialogue.

    Always generates mask.webm (transparent overlay).
    Also generates full.mp4 (baked composite) unless mask_only=True.

    Returns dict with paths: {"mask": "path/to/mask.webm", "full": "path/to/full.mp4"}
    """
    safe_title = re.sub(r'[^\w\s-]', '', lesson_title).strip().replace(" ", "_")[:30]
    lesson_id = safe_title + "_" + str(int(time.time()))
    temp_dir = os.path.join(TEMP_DIR, lesson_id)
    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    results = {}

    print(f"[1/5] Generating TTS audio for {len(dialogue)} lines (max 90s)...")
    timeline, chunks = await generate_dialogue_audio(dialogue, temp_dir)
    if not timeline:
        raise ValueError("No dialogue lines fit within 90s limit")
    timeline_s = timeline_to_seconds(timeline)
    total_duration = timeline_s[-1]["end_s"]
    print(f"  Lines: {len(timeline)}/{len(dialogue)}, Chunks: {len(chunks)}, Duration: {total_duration:.1f}s")

    print(f"[2/5] Concatenating audio...")
    audio_path = concatenate_audio(timeline, temp_dir)

    # Save audio to output dir for CSS overlay playback
    import shutil
    output_audio = os.path.join(output_dir, "audio.mp3")
    shutil.copy2(audio_path, output_audio)
    print(f"  Audio saved: {output_audio}")

    # Save timing data for CSS overlay sync
    timing_data = {
        "timeline": [
            {"speaker": e["speaker"], "text": e["text"],
             "start_s": e["start_ms"] / 1000.0, "end_s": e["end_ms"] / 1000.0}
            for e in timeline
        ],
        "chunks": chunks,
        "total_duration": total_duration,
    }
    timing_path = os.path.join(output_dir, "timing.json")
    with open(timing_path, "w") as f:
        json.dump(timing_data, f, indent=2)
    print(f"  Timing saved: {timing_path}")

    # Always generate mask
    print(f"[3/5] Generating transparent mask (WebM VP9 alpha)...")
    mask_path = os.path.join(output_dir, "mask.webm")
    generate_mask(
        timeline=timeline_s,
        chunks=chunks,
        audio_path=audio_path,
        output_path=mask_path,
    )
    mask_size = os.path.getsize(mask_path) / (1024 * 1024)
    print(f"  Mask: {mask_path} ({mask_size:.1f} MB)")
    results["mask"] = mask_path

    if not mask_only:
        # Generate baked composite
        print(f"[4/5] Compositing full video (H.264 baked)...")
        bg = background_video or (DESKTOP_VIDEO if os.path.exists(DESKTOP_VIDEO) else None)
        if bg:
            full_path = os.path.join(output_dir, "full.mp4")
            compose_video(
                timeline=timeline_s,
                chunks=chunks,
                audio_path=audio_path,
                output_path=full_path,
                background_video=bg,
            )
            full_size = os.path.getsize(full_path) / (1024 * 1024)
            print(f"  Full: {full_path} ({full_size:.1f} MB)")
            results["full"] = full_path
        else:
            print(f"  [skip] No background video found, skipping full composite")
    else:
        print(f"[4/5] Skipping full composite (mask-only mode)")

    print(f"[5/5] Done!")
    print(f"  Duration: {total_duration:.1f}s")
    for k, v in results.items():
        sz = os.path.getsize(v) / (1024 * 1024)
        print(f"  {k}: {os.path.basename(v)} ({sz:.1f} MB)")

    return results


async def generate_from_lesson_id(
    lesson_id: str,
    output_dir: str,
    background_video: str | None = None,
    mask_only: bool = False,
) -> dict:
    import httpx
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_BASE}/lessons/{lesson_id}")
        resp.raise_for_status()
        lesson = resp.json()
    dialogue = lesson.get("dialogue", [])
    if not dialogue:
        raise ValueError(f"Lesson {lesson_id} has no dialogue")
    return await generate_from_dialogue(dialogue, lesson["title"], output_dir, background_video, mask_only)


async def main():
    parser = argparse.ArgumentParser(description="CyberMentorTok Video Generator")
    parser.add_argument("--lesson-json", help="Path to JSON file with dialogue")
    parser.add_argument("--lesson-id", help="Lesson ID to fetch from API")
    parser.add_argument("--demo", action="store_true", help="Generate demo video")
    parser.add_argument("--output-dir", "-o", default=None, help="Output directory")
    parser.add_argument("--background", "-b", default=None, help="Specific background video")
    parser.add_argument("--mask-only", action="store_true", help="Generate only the transparent mask (no baked composite)")
    args = parser.parse_args()

    output_dir = args.output_dir or OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    if args.demo:
        print("Generating DEMO video...")
        await generate_from_dialogue(DEMO_LESSON["dialogue"], DEMO_LESSON["title"], output_dir, args.background, args.mask_only)
    elif args.lesson_json:
        with open(args.lesson_json) as f:
            data = json.load(f)
        dialogue = data.get("dialogue", data) if isinstance(data, dict) else data
        title = data.get("title", "lesson") if isinstance(data, dict) else "lesson"
        await generate_from_dialogue(dialogue, title, output_dir, args.background, args.mask_only)
    elif args.lesson_id:
        await generate_from_lesson_id(args.lesson_id, output_dir, args.background, args.mask_only)
    else:
        print("No input specified. Use --demo, --lesson-json, or --lesson-id")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

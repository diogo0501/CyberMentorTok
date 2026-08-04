"""
Regenerate clean dialogue audio for existing videos and remux it into full.mp4.

The existing full.mp4 files were rendered with audio that has a mild echo/room
character (older TTS generation). This script:
  1. Re-synthesizes each lesson's dialogue with edge-tts (same +50% rate to
     preserve timing sync with the baked-in subtitles/characters).
  2. Concatenates the lines with the same pause spacing.
  3. Remuxes full.mp4, replacing ONLY the audio track (video + baked overlays
     are kept as-is) at higher quality (AAC 96k/44.1kHz).

Usage:
    python regenerate_audio.py --lesson <id-prefix>   # regenerate one lesson
    python regenerate_audio.py --all                  # regenerate all video lessons
    python regenerate_audio.py --dry-run --lesson <prefix>  # compare timings only

Run with the SYSTEM python that has edge_tts installed.
"""
import argparse
import asyncio
import json
import os
import shutil
import sqlite3
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tts_generator import generate_dialogue_audio, concatenate_audio

PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DB = os.path.join(PIPELINE_DIR, "..", "backend", "cybermentortok.db")
OUTPUT_DIR = os.path.join(PIPELINE_DIR, "output")
TEMP_DIR = os.path.join(PIPELINE_DIR, "temp", "regen")


def get_lessons():
    con = sqlite3.connect(BACKEND_DB)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        """
        SELECT l.id, l.dialogue
        FROM lessons l
        JOIN videos v ON v.lesson_id = l.id
        WHERE l.deleted_at IS NULL AND v.status = 'ready'
        """
    ).fetchall()
    con.close()
    return rows


def _get_duration(path: str) -> float:
    try:
        r = subprocess.run(
            ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", path],
            capture_output=True, text=True, timeout=20,
        )
        return float(json.loads(r.stdout)["format"]["duration"])
    except Exception:
        return 0.0


async def regenerate_audio(dialogue: list[dict], temp_dir: str) -> str:
    timeline, _chunks = await generate_dialogue_audio(dialogue, temp_dir)
    if not timeline:
        return None
    return concatenate_audio(timeline, temp_dir)


def remux(full_mp4: str, new_audio: str, out_mp4: str) -> None:
    cmd = [
        "ffmpeg", "-y", "-v", "quiet",
        "-i", full_mp4,
        "-i", new_audio,
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "96k", "-ac", "1", "-ar", "44100",
        "-af", "highpass=f=80,lowpass=f=15000",
        "-shortest",
        "-movflags", "+faststart",
        out_mp4,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"ffmpeg remux failed:\n{r.stderr[-800:]}")


async def process_lesson(lesson_id: str, dialogue, dry_run: bool) -> None:
    lid = lesson_id[:8]
    out_dir = os.path.join(OUTPUT_DIR, lid)
    full_mp4 = os.path.join(out_dir, "full.mp4")
    if not os.path.isfile(full_mp4):
        return "skip-no-video"

    temp_dir = os.path.join(TEMP_DIR, lid)
    os.makedirs(temp_dir, exist_ok=True)

    audio = await regenerate_audio(dialogue, temp_dir)
    if not audio:
        return "skip-no-audio"

    # audio.mp3 is what the app plays — always update it (even if full.mp4 is corrupt)
    shutil.copy2(audio, os.path.join(out_dir, "audio.mp3"))

    old_dur = _get_duration(full_mp4)
    new_dur = _get_duration(audio)
    delta = abs(old_dur - new_dur)

    if dry_run:
        print(f"[dry] {lid}: old={old_dur:.2f}s new_audio={new_dur:.2f}s delta={delta:.2f}s")
        return "dry-run"

    # Best-effort: remux audio into full.mp4 (may fail if the file is corrupt)
    try:
        tmp_out = full_mp4 + ".regen.mp4"
        remux(full_mp4, audio, tmp_out)
        os.replace(tmp_out, full_mp4)
        print(f"[ok] {lid}: remuxed audio (old={old_dur:.2f}s new={new_dur:.2f}s delta={delta:.2f}s)")
    except Exception as e:
        print(f"[warn] {lid}: full.mp4 remux failed ({e}); audio.mp3 updated only")
    return "done"


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lesson", default=None, help="Regenerate only lessons whose id starts with this prefix")
    parser.add_argument("--all", action="store_true", help="Regenerate all video lessons")
    parser.add_argument("--dry-run", action="store_true", help="Compare timings without remuxing")
    args = parser.parse_args()

    lessons = get_lessons()
    print(f"Found {len(lessons)} video lessons in DB")

    failed = []
    for lesson in lessons:
        lid = lesson["id"][:8]
        if args.lesson and not lesson["id"].startswith(args.lesson):
            continue
        if args.lesson is None and not args.all:
            continue
        dialogue = json.loads(lesson["dialogue"]) if isinstance(lesson["dialogue"], str) else lesson["dialogue"]
        status = "error"
        for attempt in range(4):  # retry transient edge-tts failures
            try:
                status = await process_lesson(lesson["id"], dialogue, args.dry_run)
                if status != "error":
                    break
            except Exception as e:
                status = "error"
                print(f"[ERR] {lid} (attempt {attempt+1}): {e}")
            import asyncio
            await asyncio.sleep(2 * (attempt + 1))
        if status == "error":
            failed.append(lid)
        print(f"  {lid} -> {status}")

    if failed:
        print(f"\nFailed lessons: {failed}")


if __name__ == "__main__":
    asyncio.run(main())

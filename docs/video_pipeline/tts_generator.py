import os
import subprocess
import json


PETER_VOICE = "en-US-GuyNeural"
STEWIE_VOICE = "en-US-ChristopherNeural"
PAUSE_BETWEEN_LINES_MS = 150
MAX_DURATION_S = 90.0
TTS_RATE = "+50%"
CHUNK_WORDS = 6


async def _generate_line(text: str, voice: str, output_path: str) -> None:
    import edge_tts
    communicate = edge_tts.Communicate(text, voice, rate=TTS_RATE)
    await communicate.save(output_path)


def _ffprobe_duration(path: str) -> float | None:
    try:
        r = subprocess.run(
            ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", path],
            capture_output=True, text=True, timeout=20,
        )
        return float(json.loads(r.stdout)["format"]["duration"]) * 1000.0
    except Exception:
        return None


def _words_to_chunks(words: list[str], start_ms: float, duration_ms: float) -> list[dict]:
    chunks = []
    total_chars = sum(len(w) for w in words)
    current_ms = 0.0

    for i in range(0, len(words), CHUNK_WORDS):
        group = words[i:i + CHUNK_WORDS]
        group_chars = sum(len(w) for w in group)
        chunk_duration = (group_chars / total_chars) * duration_ms if total_chars > 0 else duration_ms / len(words)

        chunks.append({
            "text": " ".join(group),
            "start_s": (start_ms + current_ms) / 1000.0,
            "end_s": (start_ms + current_ms + chunk_duration) / 1000.0,
        })
        current_ms += chunk_duration

    return chunks


async def generate_dialogue_audio(dialogue: list[dict], temp_dir: str) -> tuple[list[dict], list[dict]]:
    os.makedirs(temp_dir, exist_ok=True)

    # Phase 1: Generate ALL audio files in parallel (with retries for transient failures)
    import asyncio
    import edge_tts

    async def _gen(i, line):
        voice = PETER_VOICE if line["speaker"].lower() == "peter" else STEWIE_VOICE
        path = os.path.join(temp_dir, f"line_{i:03d}.mp3")
        for attempt in range(4):
            try:
                comm = edge_tts.Communicate(line["text"], voice, rate=TTS_RATE)
                await comm.save(path)
                if os.path.getsize(path) > 0:
                    return path
            except Exception as exc:
                print(f"TTS failed for line {i} attempt {attempt + 1}: {exc}")
            await asyncio.sleep(1 + attempt * 2)
        return path  # still empty -> will be skipped by the duration check below

    tasks = [_gen(i, line) for i, line in enumerate(dialogue)]
    audio_paths = await asyncio.gather(*tasks)

    # Phase 2: Build timeline (sequential — need cumulative timing)
    timeline = []
    all_chunks = []
    current_time_ms = 0

    for i, line in enumerate(dialogue):
        if current_time_ms >= MAX_DURATION_S * 1000:
            break
        duration_ms = _ffprobe_duration(audio_paths[i])
        if duration_ms is None or duration_ms <= 0:
            continue  # skip lines that failed to synthesize
        if current_time_ms + duration_ms > MAX_DURATION_S * 1000:
            break

        timeline.append({
            "speaker": line["speaker"],
            "text": line["text"],
            "audio_path": audio_paths[i],
            "start_ms": current_time_ms,
            "end_ms": current_time_ms + duration_ms,
        })

        words = line["text"].split()
        chunks = _words_to_chunks(words, current_time_ms, duration_ms)
        for c in chunks:
            c["speaker"] = line["speaker"]
        all_chunks.extend(chunks)

        current_time_ms += duration_ms + PAUSE_BETWEEN_LINES_MS

    return timeline, all_chunks


def concatenate_audio(timeline: list[dict], temp_dir: str) -> str:
    concat_path = os.path.join(temp_dir, "concat.txt")
    output_path = os.path.join(temp_dir, "full_audio.mp3")

    with open(concat_path, "w") as f:
        for i, entry in enumerate(timeline):
            abs_path = os.path.abspath(entry["audio_path"]).replace("\\", "/")
            f.write(f"file '{abs_path}'\n")
            if i < len(timeline) - 1:
                silence_path = os.path.join(temp_dir, f"silence_{i:03d}.mp3")
                if not os.path.exists(silence_path):
                    subprocess.run([
                        "ffmpeg", "-y", "-f", "lavfi", "-i",
                        f"anullsrc=r=24000:cl=mono", "-t",
                        f"{PAUSE_BETWEEN_LINES_MS / 1000.0:.3f}",
                        "-c:a", "libmp3lame", "-q:a", "9", silence_path,
                    ], capture_output=True)
                abs_silence = os.path.abspath(silence_path).replace("\\", "/")
                f.write(f"file '{abs_silence}'\n")

    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_path, "-c:a", "libmp3lame", "-q:a", "5", output_path,
    ], capture_output=True)

    return output_path


def timeline_to_seconds(timeline: list[dict]) -> list[dict]:
    return [
        {
            **entry,
            "start_s": entry["start_ms"] / 1000.0,
            "end_s": entry["end_ms"] / 1000.0,
        }
        for entry in timeline
    ]

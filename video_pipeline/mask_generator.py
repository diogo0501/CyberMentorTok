"""Transparent Overlay Mask Generator

Generates a WebM video (VP9 + alpha channel) containing:
  - Character PNGs (Peter/Stewie) appearing per speaker timeline
  - Subtitle text synced to speech chunks

The mask is designed to be layered on top of ANY background video
via a background video + transparent overlay stack in the app.

Output: ~1-3MB WebM (99% transparent pixels compress to near-zero)
"""

import json
import os
import subprocess

from layout import (
    CHARACTER_BOTTOM_OFFSET,
    CHARACTER_MARGIN,
    CHARACTER_SIZE,
    SUBTITLE_FONT_SIZE,
    SUBTITLE_Y_RATIO,
    VIDEO_HEIGHT,
    VIDEO_WIDTH,
)


def _get_duration(path: str) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", path],
        capture_output=True, text=True,
    )
    return float(json.loads(r.stdout)["format"]["duration"])


def _escape_dt(t: str) -> str:
    t = t.replace("\\", "\\\\")
    t = t.replace("'", "")
    t = t.replace(":", "\\:")
    t = t.replace(";", "\\;")
    t = t.replace("%", "%%")
    t = t.encode("ascii", "ignore").decode("ascii")
    return t


def _pre_scale_character(src: str, size: int, temp_dir: str) -> str:
    name = os.path.splitext(os.path.basename(src))[0]
    out = os.path.join(temp_dir, f"{name}_{size}x{size}.png")
    if os.path.exists(out):
        return out
    subprocess.run([
        "ffmpeg", "-y", "-i", src,
        "-vf", (
            f"scale={size}:{size}:force_original_aspect_ratio=decrease,"
            f"pad={size}:{size}:(ow-iw)/2:(oh-ih)/2:color=0x000000@0,"
            f"format=rgba"
        ),
        out,
    ], capture_output=True)
    return out


def generate_mask(
    timeline: list[dict],
    chunks: list[dict],
    audio_path: str,
    output_path: str,
    max_duration: float = 90.0,
) -> str:
    """Generate a transparent WebM overlay mask.

    Args:
        timeline: Speaker timeline with start_s/end_s (from timeline_to_seconds)
        chunks: Subtitle chunks with text/start_s/end_s
        audio_path: Path to concatenated audio file (MP3 or similar)
        output_path: Output path for mask.webm
        max_duration: Max duration cap

    Returns:
        Path to generated mask.webm
    """
    total_duration = min(_get_duration(audio_path), max_duration)

    pipeline_dir = os.path.dirname(os.path.abspath(__file__))
    peter_src = os.path.join(pipeline_dir, "characters", "peter.png")
    stewie_src = os.path.join(pipeline_dir, "characters", "stewie.png")
    out = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(out), exist_ok=True)

    temp_dir = os.path.join(pipeline_dir, "temp", "_scaled_chars")
    os.makedirs(temp_dir, exist_ok=True)
    peter = _pre_scale_character(peter_src, CHARACTER_SIZE, temp_dir)
    stewie = _pre_scale_character(stewie_src, CHARACTER_SIZE, temp_dir)

    x_peter = CHARACTER_MARGIN
    x_stewie = VIDEO_WIDTH - CHARACTER_SIZE - CHARACTER_MARGIN
    y = VIDEO_HEIGHT - CHARACTER_SIZE - CHARACTER_BOTTOM_OFFSET

    # Build speaker runs (merge consecutive same-speaker lines)
    runs = []
    if timeline:
        runs = [{"speaker": timeline[0]["speaker"], "start_s": timeline[0]["start_s"], "end_s": timeline[0]["end_s"]}]
        for e in timeline[1:]:
            if e["speaker"] == runs[-1]["speaker"]:
                runs[-1]["end_s"] = e["end_s"]
            else:
                runs.append({"speaker": e["speaker"], "start_s": e["start_s"], "end_s": e["end_s"]})

    peter_parts, stewie_parts = [], []
    for r in runs:
        expr = f"between(t\\,{r['start_s']:.3f}\\,{r['end_s']:.3f})"
        if r["speaker"].lower() == "peter":
            peter_parts.append(expr)
        else:
            stewie_parts.append(expr)

    peter_enable = "+".join(peter_parts) if peter_parts else "0"
    stewie_enable = "+".join(stewie_parts) if stewie_parts else "0"

    # Build drawtext filters for subtitle chunks
    dt_filters = []
    for chunk in chunks:
        escaped = _escape_dt(chunk["text"])
        dt_filters.append(
            f"drawtext=text='{escaped}'"
            f":font='Impact'"
            f":fontcolor=white:fontsize={SUBTITLE_FONT_SIZE}:borderw=4:bordercolor=black"
            f":x=(w-text_w)/2:y=(h*{SUBTITLE_Y_RATIO:.2f})-(text_h/2)"
            f":enable='between(t\\,{chunk['start_s']:.3f}\\,{chunk['end_s']:.3f})'"
        )

    vf_subs = ",".join(dt_filters) if dt_filters else "null"

    # Filter complex:
    # [0:v] = transparent canvas (color=black@0, rgba)
    # [1:v] = Peter character (pre-scaled PNG, looped)
    # [2:v] = Stewie character (pre-scaled PNG, looped)
    fc = (
        f"[0:v]fps=5,format=rgba[canvas];"
        f"[canvas][1:v]overlay=x={x_peter}:y={y}:enable='{peter_enable}':eof_action=pass[bp];"
        f"[bp][2:v]overlay=x={x_stewie}:y={y}:enable='{stewie_enable}':eof_action=pass[bp2];"
        f"[bp2]{vf_subs},format=yuva420p[outv]"
    )

    fc_path = out + ".fc.txt"
    with open(fc_path, "w") as f:
        f.write(fc)

    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i",
        f"color=c=black@0:size={VIDEO_WIDTH}x{VIDEO_HEIGHT}:duration={total_duration:.3f}:rate=5,format=rgba",
        "-loop", "1", "-i", peter,
        "-loop", "1", "-i", stewie,
        "-filter_complex_script", fc_path,
        "-map", "[outv]",
        "-t", f"{total_duration:.3f}",
        "-c:v", "libvpx-vp9",
        "-pix_fmt", "yuva420p",
        "-auto-alt-ref", "0",
        "-b:v", "1M",
        "-crf", "35",
        "-g", "5",
        "-cpu-used", "8",
        "-deadline", "realtime",
        "-threads", "4",
        "-an",
        out,
    ]

    print(f"  Encoding {total_duration:.1f}s mask (vp9 alpha, {VIDEO_WIDTH}x{VIDEO_HEIGHT}@5fps, realtime)...")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  FFmpeg stderr:\n{r.stderr[-1500:]}")
        raise RuntimeError("FFmpeg mask generation failed")

    try:
        os.remove(fc_path)
    except OSError:
        pass

    return out


def list_backgrounds(backgrounds_dir: str | None = None) -> list[str]:
    """List available background videos."""
    if backgrounds_dir is None:
        backgrounds_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backgrounds")
    if not os.path.isdir(backgrounds_dir):
        return []
    return sorted([
        f for f in os.listdir(backgrounds_dir)
        if f.lower().endswith((".mp4", ".mkv", ".webm", ".mov"))
    ])


def pick_background(backgrounds_dir: str | None = None) -> str | None:
    """Pick a random background video from the pool."""
    bgs = list_backgrounds(backgrounds_dir)
    if not bgs:
        return None
    import random
    return os.path.join(
        backgrounds_dir or os.path.join(os.path.dirname(os.path.abspath(__file__)), "backgrounds"),
        random.choice(bgs),
    )

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
        "-vf", f"scale={size}:{size}:force_original_aspect_ratio=decrease,pad={size}:{size}:(ow-iw)/2:(oh-ih)/2:color=0x000000@0,format=rgba",
        out,
    ], capture_output=True)
    return out


def compose_video(
    timeline: list[dict],
    chunks: list[dict],
    audio_path: str,
    output_path: str,
    background_video: str | None = None,
    max_duration: float = 90.0,
) -> str:
    total_duration = min(_get_duration(audio_path), max_duration)

    bg = os.path.abspath(background_video)
    peter_src = os.path.abspath(os.path.join(os.path.dirname(__file__), "characters", "peter.png"))
    stewie_src = os.path.abspath(os.path.join(os.path.dirname(__file__), "characters", "stewie.png"))
    out = os.path.abspath(output_path)
    aud = os.path.abspath(audio_path)
    os.makedirs(os.path.dirname(out), exist_ok=True)

    temp_dir = os.path.join(os.path.dirname(__file__), "temp", "_scaled_chars")
    os.makedirs(temp_dir, exist_ok=True)
    peter = _pre_scale_character(peter_src, CHARACTER_SIZE, temp_dir)
    stewie = _pre_scale_character(stewie_src, CHARACTER_SIZE, temp_dir)

    x_peter = CHARACTER_MARGIN
    x_stewie = VIDEO_WIDTH - CHARACTER_SIZE - CHARACTER_MARGIN
    y = VIDEO_HEIGHT - CHARACTER_SIZE - CHARACTER_BOTTOM_OFFSET

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

    fc = (
        f"[0:v]scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=increase,"
        f"crop={VIDEO_WIDTH}:{VIDEO_HEIGHT},"
        f"fps=30,"
        f"{vf_subs},"
        f"format=yuv420p[bg];"
        f"[bg][1:v]overlay=x={x_peter}:y={y}:enable='{peter_enable}':eof_action=pass[bp];"
        f"[bp][2:v]overlay=x={x_stewie}:y={y}:enable='{stewie_enable}':eof_action=pass[outv]"
    )

    fc_path = out + ".fc.txt"
    with open(fc_path, "w") as f:
        f.write(fc)

    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", bg,
        "-i", peter,
        "-i", stewie,
        "-i", aud,
        "-filter_complex_script", fc_path,
        "-map", "[outv]", "-map", "3:a",
        "-t", f"{total_duration:.3f}",
        "-c:v", "libx264", "-preset", "fast", "-crf", "45",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "96k",
        "-ac", "1", "-ar", "44100",
        "-af", "highpass=f=80,lowpass=f=15000",
        "-movflags", "+faststart",
        "-shortest",
        out,
    ]

    print(f"  Encoding {total_duration:.1f}s video (h264 fast, {VIDEO_WIDTH}x{VIDEO_HEIGHT}@60fps, crf45)...")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  FFmpeg stderr:\n{r.stderr[-1200:]}")
        raise RuntimeError("FFmpeg failed")

    try:
        os.remove(fc_path)
    except OSError:
        pass

    return out

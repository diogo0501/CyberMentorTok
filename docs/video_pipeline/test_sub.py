import asyncio
import os
import sys
import subprocess

sys.path.insert(0, r"C:\Users\diogo\CyberMentorTok\video_pipeline")
from tts_generator import generate_dialogue_audio, concatenate_audio, timeline_to_seconds, write_srt

TEMP = r"C:\Users\diogo\CyberMentorTok\video_pipeline\temp\test"
BG = r"C:\Users\diogo\Desktop\Download.mp4"
OUT = r"C:\Users\diogo\CyberMentorTok\video_pipeline\output\test_subs.mp4"

dialogue = [
    {"speaker": "Peter", "text": "Hey Stewie, what is DNS?"},
    {"speaker": "Stewie", "text": "DNS is the phonebook of the internet. It translates domain names to IP addresses."},
]

async def main():
    os.makedirs(TEMP, exist_ok=True)
    tl = await generate_dialogue_audio(dialogue, TEMP)
    tl_s = timeline_to_seconds(tl)
    audio = concatenate_audio(tl, TEMP)
    srt = os.path.join(TEMP, "subs.srt")
    write_srt(tl_s, srt)

    print("=== SRT content ===")
    with open(srt) as f:
        print(f.read())

    # Test 1: drawtext approach (known working)
    srt_fwd = srt.replace("\\", "/")
    srt_esc = srt_fwd.replace(":", "\\:")

    fc = (
        f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        f"subtitles='{srt_esc}':"
        f"force_style='FontName=Arial,FontSize=24,PrimaryColour=&H00FFFFFF,"
        f"OutlineColour=&H00000000,Outline=2,Alignment=2,MarginV=500',"
        f"format=yuv420p[outv]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-ss", "0", "-t", "10", "-i", BG,
        "-i", audio,
        "-filter_complex", fc,
        "-map", "[outv]", "-map", "1:a",
        "-c:v", "libx264", "-preset", "ultrafast",
        "-c:a", "aac", "-b:a", "64k",
        OUT,
    ]

    print("=== FFmpeg command ===")
    print(" ".join(cmd))
    print("\n=== FFmpeg filter_complex ===")
    print(fc)

    r = subprocess.run(cmd, capture_output=True, text=True)
    print(f"\n=== Return code: {r.returncode} ===")
    if r.stderr:
        # Show only relevant lines
        for line in r.stderr.split("\n"):
            if any(k in line.lower() for k in ["error", "subtitle", "libass", "font", "output", "parsed"]):
                print(line)

    if r.returncode == 0:
        size = os.path.getsize(OUT) / 1024
        print(f"\nSUCCESS: {size:.0f} KB")

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import os
import sys
import subprocess

sys.path.insert(0, r"C:\Users\diogo\CyberMentorTok\video_pipeline")
from tts_generator import generate_dialogue_audio, concatenate_audio, timeline_to_seconds, write_srt

TEMP = r"C:\Users\diogo\CyberMentorTok\video_pipeline\temp\debug"
BG = r"C:\Users\diogo\Desktop\Download.mp4"
OUT = r"C:\Users\diogo\CyberMentorTok\video_pipeline\output\debug.mp4"

dialogue = [
    {"speaker": "Peter", "text": "Hey Stewie, what is DNS?"},
    {"speaker": "Stewie", "text": "DNS is the phonebook of the internet. It translates domain names to IP addresses."},
    {"speaker": "Peter", "text": "So it is like a phone book for websites?"},
    {"speaker": "Stewie", "text": "Exactly. And when DNS is poisoned, you get redirected to malicious sites."},
]

async def main():
    os.makedirs(TEMP, exist_ok=True)
    tl = await generate_dialogue_audio(dialogue, TEMP)
    tl_s = timeline_to_seconds(tl)
    audio = concatenate_audio(tl, TEMP)
    srt_path = os.path.join(TEMP, "subs.srt")
    write_srt(tl_s, srt_path)

    # Use compositor
    from compositor import compose_video
    compose_video(
        timeline=tl_s,
        srt_path=srt_path,
        audio_path=audio,
        output_path=OUT,
        background_video=BG,
    )
    size = os.path.getsize(OUT) / (1024*1024)
    print(f"Done: {OUT} ({size:.1f} MB)")

if __name__ == "__main__":
    asyncio.run(main())

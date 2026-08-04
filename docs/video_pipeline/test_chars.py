import subprocess, os, json

bg = r"C:\Users\diogo\Desktop\Download.mp4"
peter = r"C:\Users\diogo\CyberMentorTok\video_pipeline\characters\peter.png"
stewie = r"C:\Users\diogo\CyberMentorTok\video_pipeline\characters\stewie.png"
out = r"C:\Users\diogo\CyberMentorTok\video_pipeline\output\char_test.mp4"

# Simple test: overlay peter.png at bottom-right for 3 seconds, no enable expression
cmd = [
    "ffmpeg", "-y",
    "-ss", "0", "-t", "5", "-i", bg,
    "-i", peter,
    "-filter_complex",
    "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
    "[1:v]scale=200:200:force_original_aspect_ratio=decrease,format=rgba,"
    "overlay=x=850:y=1520:format=auto[outv]",
    "-map", "[outv]",
    "-c:v", "libx264", "-preset", "ultrafast",
    "-frames:v", "1",
    r"C:\Users\diogo\CyberMentorTok\video_pipeline\output\char_frame.png",
]

print("Running simple overlay test...")
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode != 0:
    print(f"FAILED: {r.stderr[-500:]}")
else:
    size = os.path.getsize(r"C:\Users\diogo\CyberMentorTok\video_pipeline\output\char_frame.png")
    print(f"SUCCESS: char_frame.png ({size} bytes)")

# Now test with enable expression
cmd2 = [
    "ffmpeg", "-y",
    "-stream_loop", "-1", "-ss", "0", "-t", "5", "-i", bg,
    "-i", peter,
    "-filter_complex",
    "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
    "format=yuv420p[bg];"
    "[1:v]scale=200:200:force_original_aspect_ratio=decrease,format=rgba[p];"
    "[bg][p]overlay=x=850:y=1520:enable='between(t\,0\,5)':eof_action=pass[outv]",
    "-map", "[outv]",
    "-c:v", "libx264", "-preset", "ultrafast",
    "-frames:v", "1",
    r"C:\Users\diogo\CyberMentorTok\video_pipeline\output\char_frame2.png",
]

print("\nRunning overlay with enable expression...")
r2 = subprocess.run(cmd2, capture_output=True, text=True)
if r2.returncode != 0:
    print(f"FAILED: {r2.stderr[-500:]}")
else:
    size2 = os.path.getsize(r"C:\Users\diogo\CyberMentorTok\video_pipeline\output\char_frame2.png")
    print(f"SUCCESS: char_frame2.png ({size2} bytes)")

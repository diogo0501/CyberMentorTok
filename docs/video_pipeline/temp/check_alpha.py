import subprocess, os

base = "C:/Users/diogo/CyberMentorTok/video_pipeline"
mask = f"{base}/output/f037e2de/mask.webm"

# Decode first frame to raw RGBA
subprocess.run([
    'ffmpeg', '-y', '-i', mask,
    '-vf', 'format=rgba', '-frames:v', '1',
    '-f', 'rawvideo', '-pix_fmt', 'rgba',
    f'{base}/temp/mask_frame.raw'
], capture_output=True)

with open(f'{base}/temp/mask_frame.raw', 'rb') as f:
    data = f.read()

W = 1080
print(f"Frame size: {len(data)} bytes, expected {W*1920*4}")

samples = [
    ('top-left corner (50,50)', 50*W+50),
    ('center (960,540)', 960*W+540),
    ('char area bottom-left (1570,200)', 1570*W+200),
    ('char area bottom-right (1570,880)', 1570*W+880),
    ('very top (10,540)', 10*W+540),
]

for name, px in samples:
    off = px * 4
    if off + 3 < len(data):
        r, g, b, a = data[off], data[off+1], data[off+2], data[off+3]
        alpha_str = "TRANSPARENT" if a == 0 else f"opaque(A={a})"
        print(f"  {name}: R={r} G={g} B={b} A={a} -> {alpha_str}")

# Count transparent vs opaque pixels
total = len(data) // 4
transparent = sum(1 for i in range(0, len(data), 4) if data[i+3] == 0)
opaque = total - transparent
print(f"\nTotal pixels: {total}, Transparent: {transparent} ({transparent*100//total}%), Opaque: {opaque} ({opaque*100//total}%)")

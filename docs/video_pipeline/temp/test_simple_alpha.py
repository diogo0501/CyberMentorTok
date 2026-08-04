import subprocess, os

base = "C:/Users/diogo/CyberMentorTok/video_pipeline/temp"

# Create a known-good test: red square on transparent background
subprocess.run([
    'ffmpeg', '-y', '-f', 'lavfi', '-i',
    'color=c=red@0.5:size=50x50:duration=1:rate=1,format=rgba',
    '-vf', 'format=yuva420p',
    '-c:v', 'libvpx-vp9', '-pix_fmt', 'yuva420p',
    '-auto-alt-ref', '0', '-b:v', '1M', '-deadline', 'realtime', '-cpu-used', '8',
    '-t', '1', f'{base}/simple_alpha.webm'
], capture_output=True, text=True)

# Decode to PNG
subprocess.run([
    'ffmpeg', '-y', '-i', f'{base}/simple_alpha.webm',
    '-frames:v', '1', f'{base}/simple_alpha.png'
], capture_output=True, text=True)

# Check PNG alpha
subprocess.run([
    'ffmpeg', '-y', '-i', f'{base}/simple_alpha.webm',
    '-vf', 'format=rgba', '-frames:v', '1',
    '-f', 'rawvideo', '-pix_fmt', 'rgba', f'{base}/simple_alpha.raw'
], capture_output=True)

if os.path.exists(f'{base}/simple_alpha.raw'):
    with open(f'{base}/simple_alpha.raw', 'rb') as f:
        data = f.read()
    total = len(data) // 4
    transparent = sum(1 for i in range(0, len(data), 4) if data[i+3] == 0)
    print(f"Simple alpha test: {transparent}/{total} transparent ({transparent*100//total}%)")
    # Sample pixel at center
    if total > 0:
        off = (25 * 50 + 25) * 4
        r, g, b, a = data[off], data[off+1], data[off+2], data[off+3]
        print(f"  Center pixel: R={r} G={g} B={b} A={a}")
else:
    print("No raw output generated")

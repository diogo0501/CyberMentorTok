import subprocess, os, json

base = "C:/Users/diogo/CyberMentorTok/video_pipeline/temp"

# Test 1: transparent canvas WITHOUT drawtext -> check if overlay preserves alpha
fc1 = '[0:v]format=rgba[canvas];[canvas][1:v]overlay=0:0:format=auto[outv]'
with open(f'{base}/fc_nodt.txt', 'w') as f: f.write(fc1)
subprocess.run([
    'ffmpeg', '-y', '-f', 'lavfi', '-i', 'color=c=black@0:size=100x100:duration=1:rate=5,format=rgba',
    '-loop', '1', '-i', f'{base}/_scaled_chars/peter_350x350.png',
    '-filter_complex_script', f'{base}/fc_nodt.txt',
    '-map', '[outv]', '-c:v', 'libvpx-vp9', '-pix_fmt', 'yuva420p',
    '-auto-alt-ref', '0', '-b:v', '1M', '-deadline', 'realtime', '-cpu-used', '8',
    '-t', '1', f'{base}/test_nodt.webm'
], capture_output=True, text=True)

# Decode and check alpha
subprocess.run([
    'ffmpeg', '-y', '-i', f'{base}/test_nodt.webm',
    '-vf', 'format=rgba', '-frames:v', '1',
    '-f', 'rawvideo', '-pix_fmt', 'rgba', f'{base}/test_nodt.raw'
], capture_output=True)
with open(f'{base}/test_nodt.raw', 'rb') as f:
    data = f.read()
total = len(data) // 4
transparent = sum(1 for i in range(0, len(data), 4) if data[i+3] == 0)
print(f"Test 1 (overlay only, no drawtext): {transparent}/{total} transparent ({transparent*100//total}%)")

# Test 2: transparent canvas + drawtext only -> check alpha
fc2 = "[0:v]format=rgba[canvas];[canvas]drawtext=text=hello:font=Impact:fontcolor=white:fontsize=52:borderw=3:bordercolor=black:x=10:y=10:enable='between(t\\,0\\,1)',format=yuva420p[outv]"
with open(f'{base}/fc_dt.txt', 'w') as f: f.write(fc2)
subprocess.run([
    'ffmpeg', '-y', '-f', 'lavfi', '-i', 'color=c=black@0:size=100x100:duration=1:rate=5,format=rgba',
    '-filter_complex_script', f'{base}/fc_dt.txt',
    '-map', '[outv]', '-c:v', 'libvpx-vp9', '-pix_fmt', 'yuva420p',
    '-auto-alt-ref', '0', '-b:v', '1M', '-deadline', 'realtime', '-cpu-used', '8',
    '-t', '1', f'{base}/test_dt.webm'
], capture_output=True, text=True)
subprocess.run([
    'ffmpeg', '-y', '-i', f'{base}/test_dt.webm',
    '-vf', 'format=rgba', '-frames:v', '1',
    '-f', 'rawvideo', '-pix_fmt', 'rgba', f'{base}/test_dt.raw'
], capture_output=True)
with open(f'{base}/test_dt.raw', 'rb') as f:
    data = f.read()
total = len(data) // 4
transparent = sum(1 for i in range(0, len(data), 4) if data[i+3] == 0)
print(f"Test 2 (drawtext only, no overlay): {transparent}/{total} transparent ({transparent*100//total}%)")

# Test 3: transparent canvas + geq to set alpha + drawtext
fc3 = "[0:v]format=rgba[canvas];[canvas]drawtext=text=hello:font=Impact:fontcolor=white:fontsize=52:borderw=3:bordercolor=black:x=10:y=10:enable='between(t\\,0\\,1)',geq='lum_expr=clamp(lum(X,Y),0,255)':a_expr='if(gt(alpha(X,Y),0),alpha(X,Y),0)',format=yuva420p[outv]"
with open(f'{base}/fc_dt_geo.txt', 'w') as f: f.write(fc3)
subprocess.run([
    'ffmpeg', '-y', '-f', 'lavfi', '-i', 'color=c=black@0:size=100x100:duration=1:rate=5,format=rgba',
    '-filter_complex_script', f'{base}/fc_dt_geo.txt',
    '-map', '[outv]', '-c:v', 'libvpx-vp9', '-pix_fmt', 'yuva420p',
    '-auto-alt-ref', '0', '-b:v', '1M', '-deadline', 'realtime', '-cpu-used', '8',
    '-t', '1', f'{base}/test_dt_geo.webm'
], capture_output=True, text=True)
subprocess.run([
    'ffmpeg', '-y', '-i', f'{base}/test_dt_geo.webm',
    '-vf', 'format=rgba', '-frames:v', '1',
    '-f', 'rawvideo', '-pix_fmt', 'rgba', f'{base}/test_dt_geo.raw'
], capture_output=True)
with open(f'{base}/test_dt_geo.raw', 'rb') as f:
    data = f.read()
total = len(data) // 4
transparent = sum(1 for i in range(0, len(data), 4) if data[i+3] == 0)
print(f"Test 3 (drawtext + geq alpha fix): {transparent}/{total} transparent ({transparent*100//total}%)")

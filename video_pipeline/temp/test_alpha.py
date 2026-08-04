import subprocess, json

def test_ffmpeg(desc, input_args, vf, outfile):
    cmd = ['ffmpeg', '-y'] + input_args + [
        '-vf', vf,
        '-c:v', 'libvpx-vp9', '-pix_fmt', 'yuva420p',
        '-auto-alt-ref', '0', '-b:v', '1M', '-deadline', 'realtime', '-cpu-used', '8',
        '-t', '1', outfile]
    r = subprocess.run(cmd, capture_output=True, text=True)
    r2 = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=pix_fmt,tags', '-of', 'json', outfile], capture_output=True, text=True)
    d = json.loads(r2.stdout)['streams'][0]
    pf = d.get('pix_fmt', 'N/A')
    am = d.get('tags', {}).get('alpha_mode', 'no')
    print(f'{desc}: pix_fmt={pf} alpha_mode={am} rc={r.returncode}')

base = 'C:/Users/diogo/CyberMentorTok/video_pipeline/temp'

# 1. color + format=rgba
test_ffmpeg('color+format=rgba',
    ['-f', 'lavfi', '-i', 'color=c=black:s=100x100:d=1:r=5'],
    'format=rgba',
    f'{base}/a1.webm')

# 2. geq for full transparency
test_ffmpeg('geq a=0',
    ['-f', 'lavfi', '-i', 'color=c=black:s=100x100:d=1:r=5'],
    'geq=r=0:g=0:b=0:a=0,format=yuva420p',
    f'{base}/a2.webm')

# 3. colorchannelmixer
test_ffmpeg('colorchannelmixer aa=0',
    ['-f', 'lavfi', '-i', 'color=c=black:s=100x100:d=1:r=5'],
    'colorchannelmixer=aa=0,format=yuva420p',
    f'{base}/a3.webm')

# 4. color with @0
test_ffmpeg('color@0',
    ['-f', 'lavfi', '-i', 'color=c=black@0:s=100x100:d=1:r=5'],
    'format=rgba',
    f'{base}/a4.webm')

# 5. nullsrc + geq
test_ffmpeg('nullsrc+geq',
    ['-f', 'lavfi', '-i', 'nullsrc=s=100x100:d=1:r=5'],
    'geq=r=0:g=0:b=0:a=0,format=yuva420p',
    f'{base}/a5.webm')

# 6. Check raw pixel data from color=c=black@0
r = subprocess.run(['ffmpeg', '-y', '-f', 'lavfi', '-i', 'color=c=black@0:s=4x4:d=1:r=1,format=rgba',
    '-f', 'rawvideo', '-pix_fmt', 'rgba', '-frames:v', '1',
    f'{base}/raw_test.bin'], capture_output=True, text=True)
with open(f'{base}/raw_test.bin', 'rb') as f:
    data = f.read()
if len(data) >= 4:
    r, g, b, a = data[0], data[1], data[2], data[3]
    print(f'First pixel from color=c=black@0: R={r} G={g} B={b} A={a}')
else:
    print('No raw data')

# 7. Check raw pixel from geq a=0
r = subprocess.run(['ffmpeg', '-y', '-f', 'lavfi', '-i', 'color=c=black:s=4x4:d=1:r=1',
    '-vf', 'geq=r=0:g=0:b=0:a=0,format=rgba',
    '-f', 'rawvideo', '-pix_fmt', 'rgba', '-frames:v', '1',
    f'{base}/raw_geq.bin'], capture_output=True, text=True)
with open(f'{base}/raw_geq.bin', 'rb') as f:
    data = f.read()
if len(data) >= 4:
    r, g, b, a = data[0], data[1], data[2], data[3]
    print(f'First pixel from geq a=0: R={r} G={g} B={b} A={a}')
else:
    print('No raw geq data')

# 8. Test: does WebM actually contain alpha? Decode to PNG with alpha
r = subprocess.run(['ffmpeg', '-y',
    '-i', f'{base}/a2.webm',
    '-vf', 'format=rgba',
    '-frames:v', '1',
    f'{base}/a2_frame.png'], capture_output=True, text=True)
r2 = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=pix_fmt', '-of', 'json',
    f'{base}/a2_frame.png'], capture_output=True, text=True)
d = json.loads(r2.stdout)
print(f'Decoded a2.webm frame to PNG: {d["streams"][0].get("pix_fmt")}')

# 9. Test: does a1.webm contain alpha?
r = subprocess.run(['ffmpeg', '-y',
    '-i', f'{base}/a1.webm',
    '-vf', 'format=rgba',
    '-frames:v', '1',
    f'{base}/a1_frame.png'], capture_output=True, text=True)
r2 = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=pix_fmt', '-of', 'json',
    f'{base}/a1_frame.png'], capture_output=True, text=True)
d = json.loads(r2.stdout)
print(f'Decoded a1.webm frame to PNG: {d["streams"][0].get("pix_fmt")}')

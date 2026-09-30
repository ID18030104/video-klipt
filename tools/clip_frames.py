#!/usr/bin/env python3
"""Turn a local video clip (e.g. a Higgsfield clip) into a deterministic frame sequence for KK.footage().

  python3 tools/clip_frames.py pieces/<id>/assets/clip.mp4 --out pieces/<id>/footage/clip [--size 1080x1920] [--fps 30]
         [--start 0] [--dur 5] [--speed 1]
  → f0001.jpg … + info.json (frames, fps). In the page: KK.footage(img, {dir: 'footage/clip', frames: N, fps: 30, start: <t in piece>})
Use --start/--dur to cut one shot out of a multi-shot clip; --speed 0.8 slows it down (slow motion, smoother holds).
"""
import argparse, json, os, re, subprocess

a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
a.add_argument('clip'); a.add_argument('--out', required=True); a.add_argument('--size', default='1080x1920')
a.add_argument('--fps', type=int, default=30); a.add_argument('--start', type=float, default=0)
a.add_argument('--dur', type=float); a.add_argument('--speed', type=float, default=1)
a = a.parse_args()
W, H = map(int, a.size.lower().split('x'))
os.makedirs(a.out, exist_ok=True)
for x in os.listdir(a.out):
    if x.startswith('f') and x.endswith('.jpg'): os.unlink(os.path.join(a.out, x))
vf = f"setpts=PTS/{a.speed},scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},fps={a.fps}"
cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-ss', str(a.start)]
if a.dur: cmd += ['-t', str(a.dur)]
subprocess.run(cmd + ['-i', a.clip, '-vf', vf, '-q:v', '3', os.path.join(a.out, 'f%04d.jpg')], check=True)
n = len([x for x in os.listdir(a.out) if x.startswith('f') and x.endswith('.jpg')])
src = re.search(r'Video: .*?, (\d{3,4}x\d{3,4})', subprocess.run(['ffmpeg', '-i', a.clip], capture_output=True, text=True).stderr)
info = dict(clip=a.clip, source=src[1] if src else None, size=f'{W}x{H}', fps=a.fps, frames=n, start=a.start, dur=a.dur, speed=a.speed)
json.dump(info, open(os.path.join(a.out, 'info.json'), 'w'), indent=1)
print(json.dumps(info))

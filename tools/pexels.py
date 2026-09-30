#!/usr/bin/env python3
"""Pexels stock photos & videos for Klipt pieces (free license, no attribution required).

  python3 tools/pexels.py photos "<query>" --out pieces/<id>/assets/cands [--orientation portrait|landscape|square] [--n 15] [--color <name|hex>] [--page 2]
      → downloads previews + contact.jpg (numbered grid to look at) + results.json
  python3 tools/pexels.py photo-get <photo_id> --out pieces/<id>/assets/<name>.jpg [--max 2560]
      → full-resolution original, downscaled so the long side is ≤ --max (keeps 4K sharpness for zooms)
  python3 tools/pexels.py videos "<query>" --out pieces/<id>/assets/vcands [--orientation portrait] [--n 10]
      → poster previews + contact.jpg + results.json (duration, resolution)
  python3 tools/pexels.py video-get <video_id> --out pieces/<id>/footage/<name> --size 1080x1920 [--start 0] [--dur 4] [--fps 30] [--speed 1]
      → the clip as a numbered JPEG frame sequence (f0001.jpg…) cropped to fill --size, + info.json.
        Play it deterministically with KK.footage() from lib/klipt-kit.js.

API key: $PEXELS_API_KEY, else /root/klipt-state/pexels.key. Never print it, never write it into the repo.
Network: api.pexels.com, images.pexels.com and videos.pexels.com must be allowed by the environment.
"""
import argparse, json, os, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlencode

def key():
    k = os.environ.get('PEXELS_API_KEY')
    if not k and os.path.exists('/root/klipt-state/pexels.key'):
        k = open('/root/klipt-state/pexels.key').read().strip()
    if not k: sys.exit('No Pexels API key (set PEXELS_API_KEY).')
    return k

def curl(url, out=None, auth=False, timeout=120):
    cmd = ['curl', '-sfL', '-m', str(timeout)]
    if auth: cmd += ['-H', f'Authorization: {key()}']
    cmd += ['-o', out, url] if out else [url]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode:
        host = url.split('/')[2]
        sys.exit(f'download failed ({host}, curl exit {r.returncode}). If the host is blocked by the network policy, ask for {host} to be allowed.')
    return r.stdout

def api(path, **params):
    q = urlencode({k: v for k, v in params.items() if v not in (None, '')})
    return json.loads(curl(f'https://api.pexels.com/{path}?{q}', auth=True))

def contact(items, out_dir, label):
    from PIL import Image, ImageDraw, ImageFont
    thumbs = []
    for i, it in enumerate(items):
        p = os.path.join(out_dir, f'{i+1:02d}_{it["id"]}.jpg')
        if os.path.exists(p): thumbs.append((i + 1, it, Image.open(p).convert('RGB')))
    if not thumbs: return None
    W, H, cols = 300, 300, 5
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * W, rows * (H + 36)), (18, 18, 20))
    try: font = ImageFont.load_default(size=22)
    except TypeError: font = ImageFont.load_default()
    d = ImageDraw.Draw(sheet)
    for k, (n, it, im) in enumerate(thumbs):
        im.thumbnail((W - 8, H - 8))
        x, y = (k % cols) * W, (k // cols) * (H + 36)
        sheet.paste(im, (x + (W - im.width) // 2, y + (H - im.height) // 2))
        d.text((x + 8, y + H + 6), f'#{n}  {label(it)}', fill=(235, 235, 235), font=font)
    p = os.path.join(out_dir, 'contact.jpg'); sheet.save(p, quality=85)
    return p

def photos(a):
    os.makedirs(a.out, exist_ok=True)
    r = api('v1/search', query=a.query, orientation=a.orientation, color=a.color, per_page=a.n, page=a.page, size='large')
    items = r.get('photos', [])
    with ThreadPoolExecutor(8) as ex:
        list(ex.map(lambda x: curl(x[1]['src']['medium'], os.path.join(a.out, f'{x[0]+1:02d}_{x[1]["id"]}.jpg'), timeout=60), enumerate(items)))
    res = [dict(n=i + 1, id=p['id'], w=p['width'], h=p['height'], alt=p.get('alt'), avg_color=p.get('avg_color'), photographer=p.get('photographer'), url=p.get('url')) for i, p in enumerate(items)]
    json.dump(res, open(os.path.join(a.out, 'results.json'), 'w'), indent=1)
    sheet = contact(items, a.out, lambda p: f'{p["id"]} · {p["width"]}×{p["height"]}')
    print(json.dumps(dict(query=a.query, found=r.get('total_results'), shown=len(res), contact_sheet=sheet), ensure_ascii=False))
    for x in res: print(f'#{x["n"]:>2} id={x["id"]} {x["w"]}x{x["h"]} {x["avg_color"]} — {(x["alt"] or "")[:90]}')

def photo_get(a):
    from PIL import Image
    p = api(f'v1/photos/{a.id}')
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    tmp = tempfile.mktemp(suffix='.jpg'); curl(p['src']['original'], tmp, timeout=300)
    im = Image.open(tmp).convert('RGB'); w0, h0 = im.size
    s = min(1.0, a.max / max(w0, h0))
    if s < 1: im = im.resize((round(w0 * s), round(h0 * s)), Image.LANCZOS)
    im.save(a.out, quality=92, optimize=True); os.unlink(tmp)
    print(json.dumps(dict(out=a.out, id=a.id, original=f'{w0}x{h0}', saved=f'{im.width}x{im.height}', avg_color=p.get('avg_color'), alt=p.get('alt'))))

def videos(a):
    os.makedirs(a.out, exist_ok=True)
    r = api('videos/search', query=a.query, orientation=a.orientation, per_page=a.n, page=a.page)
    items = r.get('videos', [])
    with ThreadPoolExecutor(8) as ex:
        list(ex.map(lambda x: curl(x[1]['image'], os.path.join(a.out, f'{x[0]+1:02d}_{x[1]["id"]}.jpg'), timeout=60), enumerate(items)))
    res = [dict(n=i + 1, id=v['id'], w=v['width'], h=v['height'], duration=v['duration'], url=v.get('url')) for i, v in enumerate(items)]
    json.dump(res, open(os.path.join(a.out, 'results.json'), 'w'), indent=1)
    sheet = contact(items, a.out, lambda v: f'{v["id"]} · {v["duration"]}s · {v["width"]}×{v["height"]}')
    print(json.dumps(dict(query=a.query, found=r.get('total_results'), shown=len(res), contact_sheet=sheet), ensure_ascii=False))
    for x in res: print(f'#{x["n"]:>2} id={x["id"]} {x["w"]}x{x["h"]} {x["duration"]}s — {x["url"]}')

def video_get(a):
    W, H = map(int, a.size.lower().split('x'))
    v = api(f'videos/videos/{a.id}')
    files = [f for f in v['video_files'] if f.get('file_type') == 'video/mp4' and f.get('width')]
    need = min(W, H)
    ok = sorted([f for f in files if min(f['width'], f['height']) >= need], key=lambda f: f['width'] * f['height'])
    f = ok[0] if ok else max(files, key=lambda f: f['width'] * f['height'])
    os.makedirs(a.out, exist_ok=True)
    for x in os.listdir(a.out):
        if x.startswith('f') and x.endswith('.jpg'): os.unlink(os.path.join(a.out, x))
    tmp = tempfile.mktemp(suffix='.mp4'); curl(f['link'], tmp, timeout=600)
    vf = f"setpts=PTS/{a.speed},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={a.fps}"
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-ss', str(a.start), '-t', str(a.dur * a.speed), '-i', tmp,
                    '-vf', vf, '-q:v', '3', os.path.join(a.out, 'f%04d.jpg')], check=True)
    os.unlink(tmp)
    n = len([x for x in os.listdir(a.out) if x.startswith('f') and x.endswith('.jpg')])
    info = dict(id=a.id, source=f"{f['width']}x{f['height']}", size=f'{W}x{H}', fps=a.fps, frames=n, start=a.start, dur=a.dur, speed=a.speed, pexels_url=v.get('url'))
    json.dump(info, open(os.path.join(a.out, 'info.json'), 'w'), indent=1)
    print(json.dumps(info))

p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
sp = p.add_subparsers(dest='cmd', required=True)
for name in ('photos', 'videos'):
    s = sp.add_parser(name); s.add_argument('query'); s.add_argument('--out', required=True)
    s.add_argument('--orientation', choices=['portrait', 'landscape', 'square']); s.add_argument('--n', type=int, default=15)
    s.add_argument('--page', type=int, default=1)
    if name == 'photos': s.add_argument('--color')
s = sp.add_parser('photo-get'); s.add_argument('id'); s.add_argument('--out', required=True); s.add_argument('--max', type=int, default=2560)
s = sp.add_parser('video-get'); s.add_argument('id'); s.add_argument('--out', required=True); s.add_argument('--size', default='1080x1920')
s.add_argument('--start', type=float, default=0); s.add_argument('--dur', type=float, default=4); s.add_argument('--fps', type=int, default=30)
s.add_argument('--speed', type=float, default=1.0, help='<1 = slow motion (0.5 = half speed)')
a = p.parse_args()
{'photos': photos, 'photo-get': photo_get, 'videos': videos, 'video-get': video_get}[a.cmd](a)

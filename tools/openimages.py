#!/usr/bin/env python3
"""Royalty-free photos from Google Open Images (Flickr photos under CC BY 2.0: commercial use OK,
credit the author — the tool records credits automatically). ~166k human-labelled photos, ≤1024 px.

  python3 tools/openimages.py labels "fruit"                      → label names containing "fruit"
  python3 tools/openimages.py search "Peach" --out pieces/<id>/assets/cands [--any "Apricot|Nectarine"] [--not "Person"]
         [--title market] [--orientation portrait|landscape|square] [--n 20] [--seed 1]
      → numbered contact.jpg to look at + results.json. Labels are exact Open Images names (see `labels`).
        Several --all labels are ANDed: --all "Fruit,Market"; --any is an OR list; --not excludes.
  python3 tools/openimages.py get <ImageID> --out pieces/<id>/assets/<name>.jpg [--upscale 2]
      → the photo (rotation fixed), optionally upscaled (Lanczos + unsharp mask), credit appended to
        <assets dir>/CREDITS.json (author, licence, source URL).

Sources are max 1024 px on the long side: use them at ≤1.3× native size when possible (frames, grids,
split screens, backgrounds under blur/grain/duotone). Full-bleed at 1080×1920 needs --upscale 2 and a
treatment (grain, grade, slight softness is fine behind sharp type).
Index is built once into /root/klipt-state/oi (metadata from storage.googleapis.com/openimages).
"""
import argparse, csv, json, os, pickle, random, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

D = '/root/klipt-state/oi'
META = {'validation-images-with-rotation.csv': '2018_04/validation/validation-images-with-rotation.csv',
        'test-images-with-rotation.csv': '2018_04/test/test-images-with-rotation.csv',
        'oidv7-val-annotations-human-imagelabels.csv': 'v7/oidv7-val-annotations-human-imagelabels.csv',
        'oidv7-test-annotations-human-imagelabels.csv': 'v7/oidv7-test-annotations-human-imagelabels.csv',
        'oidv7-class-descriptions.csv': 'v7/oidv7-class-descriptions.csv'}

def fetch(url, out, timeout=600):
    r = subprocess.run(['curl', '-sfL', '-m', str(timeout), '-o', out, url])
    if r.returncode: sys.exit(f'download failed: {url.split("/")[2]} (curl {r.returncode})')

def index():
    p = os.path.join(D, 'index.pkl')
    if os.path.exists(p): return pickle.load(open(p, 'rb'))
    os.makedirs(D, exist_ok=True)
    for f, rel in META.items():
        if not os.path.exists(os.path.join(D, f)):
            print(f'downloading {f}…', file=sys.stderr); fetch(f'https://storage.googleapis.com/openimages/{rel}', os.path.join(D, f))
    names = {r[0]: r[1] for r in csv.reader(open(os.path.join(D, 'oidv7-class-descriptions.csv'), encoding='utf-8')) if len(r) >= 2}
    imgs = {}
    for f in ('validation-images-with-rotation.csv', 'test-images-with-rotation.csv'):
        for r in csv.DictReader(open(os.path.join(D, f), encoding='utf-8')):
            if 'creativecommons.org/licenses/by/2.0' not in r['License']: continue
            imgs[r['ImageID']] = dict(subset=r['Subset'], author=r['Author'], page=r['OriginalLandingURL'], license=r['License'],
                                      title=r['Title'], bytes=int(r['OriginalSize'] or 0), rot=r['Rotation'], labels=set())
    for f in ('oidv7-val-annotations-human-imagelabels.csv', 'oidv7-test-annotations-human-imagelabels.csv'):
        for r in csv.DictReader(open(os.path.join(D, f), encoding='utf-8')):
            if r['Confidence'] == '1' and r['ImageID'] in imgs: imgs[r['ImageID']]['labels'].add(names.get(r['LabelName'], r['LabelName']).lower())
    idx = dict(images=imgs, labels=sorted({l for v in imgs.values() for l in v['labels']}))
    pickle.dump(idx, open(p, 'wb')); return idx

def url(i, subset): return f'https://open-images-dataset.s3.amazonaws.com/{subset}/{i}.jpg'

def load_rotated(path, rot):
    from PIL import Image
    im = Image.open(path).convert('RGB')
    if rot and rot not in ('0', '0.0'): im = im.rotate(-float(rot), expand=True)
    return im

def cmd_labels(a):
    q = a.query.lower()
    for l in index()['labels']:
        if q in l: print(l)

def cmd_search(a):
    idx = index(); imgs = idx['images']
    split = lambda s: [x.strip().lower() for x in s.replace('|', ',').split(',') if x.strip()] if s else []
    need, anyof, excl = split(a.all), split(a.any), split(a.exclude)
    hits = [(i, m) for i, m in imgs.items()
            if all(l in m['labels'] for l in need) and (not anyof or any(l in m['labels'] for l in anyof))
            and not any(l in m['labels'] for l in excl) and (not a.title or a.title.lower() in m['title'].lower())]
    if not hits: sys.exit('no match — check label names with: python3 tools/openimages.py labels "<word>"')
    rnd = random.Random(a.seed)
    hits.sort(key=lambda x: -x[1]['bytes'])                     # bigger originals ≈ better cameras/photographers
    pool = hits[:max(a.n * 6, 60)]; rnd.shuffle(pool)
    os.makedirs(a.out, exist_ok=True)
    def dl(x):
        i, m = x; p = os.path.join(a.out, f'{i}.jpg')
        if not os.path.exists(p): subprocess.run(['curl', '-sf', '-m', '60', '-o', p, url(i, m['subset'])])
        return x if os.path.exists(p) else None
    got = [x for x in ThreadPoolExecutor(8).map(dl, pool[:a.n * 3]) if x]
    keep = []
    for i, m in got:
        im = load_rotated(os.path.join(a.out, f'{i}.jpg'), m['rot']); r = im.width / im.height
        ok = {'portrait': r < 0.9, 'landscape': r > 1.1, 'square': 0.85 <= r <= 1.15, None: True}[a.orientation]
        if ok and len(keep) < a.n: keep.append((i, m, im.size))
        else: os.unlink(os.path.join(a.out, f'{i}.jpg'))
    from PIL import Image, ImageDraw, ImageFont
    W, cols = 300, 5; rows = (len(keep) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * W, rows * (W + 34)), (18, 18, 20)); d = ImageDraw.Draw(sheet)
    try: font = ImageFont.load_default(size=21)
    except TypeError: font = ImageFont.load_default()
    res = []
    for k, (i, m, size) in enumerate(keep):
        im = load_rotated(os.path.join(a.out, f'{i}.jpg'), m['rot']); im.thumbnail((W - 8, W - 8))
        x, y = (k % cols) * W, (k // cols) * (W + 34)
        sheet.paste(im, (x + (W - im.width) // 2, y + (W - im.height) // 2))
        d.text((x + 6, y + W + 4), f'#{k+1}  {size[0]}x{size[1]}', fill=(230, 230, 230), font=font)
        res.append(dict(n=k + 1, id=i, size=f'{size[0]}x{size[1]}', title=m['title'], labels=sorted(m['labels'])[:12]))
    sheet.save(os.path.join(a.out, 'contact.jpg'), quality=85)
    json.dump(res, open(os.path.join(a.out, 'results.json'), 'w'), indent=1, ensure_ascii=False)
    print(json.dumps(dict(matches=len(hits), shown=len(res), contact_sheet=os.path.join(a.out, 'contact.jpg'))))
    for r in res: print(f"#{r['n']:>2} {r['id']} {r['size']} — {r['title'][:50]} | {', '.join(r['labels'][:8])}")

def cmd_get(a):
    from PIL import Image, ImageFilter
    idx = index(); m = idx['images'].get(a.id)
    if not m: sys.exit('unknown ImageID')
    tmp = a.out + '.src.jpg'; fetch(url(a.id, m['subset']), tmp, 120)
    im = load_rotated(tmp, m['rot']); os.unlink(tmp)
    if a.upscale > 1:
        im = im.resize((round(im.width * a.upscale), round(im.height * a.upscale)), Image.LANCZOS)
        im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    im.save(a.out, quality=93)
    cp = os.path.join(os.path.dirname(os.path.abspath(a.out)), 'CREDITS.json')
    credits = json.load(open(cp)) if os.path.exists(cp) else []
    credits = [c for c in credits if c.get('file') != os.path.basename(a.out)] + [dict(
        file=os.path.basename(a.out), source='Open Images (Flickr)', image_id=a.id, title=m['title'], author=m['author'],
        license='CC BY 2.0', license_url=m['license'], page=m['page'])]
    json.dump(credits, open(cp, 'w'), indent=1, ensure_ascii=False)
    print(json.dumps(dict(out=a.out, size=f'{im.width}x{im.height}', author=m['author'], license='CC BY 2.0')))

p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
sp = p.add_subparsers(dest='cmd', required=True)
s = sp.add_parser('labels'); s.add_argument('query')
s = sp.add_parser('search'); s.add_argument('all', nargs='?', default=''); s.add_argument('--any'); s.add_argument('--not', dest='exclude')
s.add_argument('--title'); s.add_argument('--orientation', choices=['portrait', 'landscape', 'square']); s.add_argument('--n', type=int, default=20)
s.add_argument('--seed', type=int, default=1); s.add_argument('--out', required=True)
s = sp.add_parser('get'); s.add_argument('id'); s.add_argument('--out', required=True); s.add_argument('--upscale', type=float, default=1)
a = p.parse_args()
{'labels': cmd_labels, 'search': cmd_search, 'get': cmd_get}[a.cmd](a)

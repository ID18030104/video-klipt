#!/usr/bin/env python3
"""Higgsfield Marketing Studio image generation (text → image) with cost-conscious defaults.

  python3 tools/higgsfield_image.py "<prompt>" --out bench/higgsfield/<name>.png [--resolution 1k] [--quality low|medium|high] [--aspect 3:4]

Credentials: $HF_KEY (KEY_ID:KEY_SECRET) or /root/klipt-state/higgsfield.key — never stored in the repo.
Network: api.higgsfield.ai and the host serving the result images must be allowed.
Writes the image plus <out>.json (prompt, parameters, request id, timings) for the cost/quality comparison.
"""
import argparse, json, os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hf_ledger

API = 'https://api.higgsfield.ai/marketing-studio/image'

def key():
    k = os.environ.get('HF_KEY')
    if not k and os.path.exists('/root/klipt-state/higgsfield.key'): k = open('/root/klipt-state/higgsfield.key').read().strip()
    if not k: sys.exit('No Higgsfield key (set HF_KEY).')
    return k

def call(method, url, body=None):
    cmd = ['curl', '-s', '-m', '60', '-X', method, url, '-H', f'Authorization: Key {key()}', '-H', 'Content-Type: application/json', '-w', '\n%{http_code}']
    if body is not None: cmd += ['--data', json.dumps(body)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit(f'network error reaching {url.split("/")[2]} (curl {r.returncode}) — is the host allowed?')
    text, code = r.stdout.rsplit('\n', 1)
    try: data = json.loads(text)
    except json.JSONDecodeError: data = {'raw': text[:500]}
    if not code.startswith('2'): sys.exit(f'HTTP {code}: {json.dumps(data)[:500]}')
    return data

a = argparse.ArgumentParser()
a.add_argument('prompt'); a.add_argument('--out', required=True)
a.add_argument('--resolution', default='1k', choices=['1k', '2k', '4k'])
a.add_argument('--quality', default='medium', choices=['low', 'medium', 'high'])
a.add_argument('--aspect', default='3:4', choices=['auto', '1:1', '3:2', '2:3', '4:3', '3:4', '16:9', '9:16', '21:9'])
a.add_argument('--image-url', action='append', default=[], help='reference image (brand logo, product…); repeatable, max 16')
a = a.parse_args()
body = dict(prompt=a.prompt, quality=a.quality, resolution=a.resolution, aspect_ratio=a.aspect, moderation='auto', enhance_prompt=False)
if a.image_url: body['image_urls'] = a.image_url
# Budget guard: price the request first, reserve it in the shared ledger (file-locked), refund on failure.
est = call('POST', 'https://api.higgsfield.ai/estimate/marketing-studio/image', body)
usd = float(est.get('usd', 0))
hf_ledger.reserve(usd, a.out)
print(f'estimated cost ${usd:.3f}', file=sys.stderr)
t0 = time.time()
try:
    job = call('POST', API, body)
except SystemExit: hf_ledger.refund(usd, a.out); raise   # rejected before any work: not billed
rid, status_url = job.get('request_id'), job.get('status_url')
while job.get('status') in ('queued', 'in_progress', None):
    time.sleep(3)
    job = call('GET', status_url or f'https://api.higgsfield.ai/requests/{rid}/status')
if job.get('status') != 'completed': hf_ledger.refund(usd, a.out); sys.exit(f'generation {job.get("status")}: {job.get("error", "")}')
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
img_url = job['images'][0]['url']
r = subprocess.run(['curl', '-sfL', '-m', '120', '-o', a.out, img_url])
if r.returncode: sys.exit(f'could not download the image from {img_url.split("/")[2]} — allow that host too')
meta = dict(body, request_id=rid, seconds=round(time.time() - t0, 1), image_host=img_url.split('/')[2], cost_usd=usd)
json.dump(meta, open(a.out + '.json', 'w'), indent=1, ensure_ascii=False)
print(json.dumps(meta, ensure_ascii=False))

#!/usr/bin/env python3
"""Higgsfield Marketing Studio image generation (text → image) with cost-conscious defaults.

  python3 tools/higgsfield_image.py "<prompt>" --out bench/higgsfield/<name>.png [--resolution 1k] [--quality low|medium|high] [--aspect 3:4]

Credentials: $HF_KEY (KEY_ID:KEY_SECRET) or /root/klipt-state/higgsfield.key — never stored in the repo.
Network: api.higgsfield.ai and the host serving the result images must be allowed.
Writes the image plus <out>.json (prompt, parameters, request id, timings) for the cost/quality comparison.
"""
import argparse, json, os, subprocess, sys, time

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
# Budget guard: price the request first and refuse to overspend the ledger (/root/klipt-state/hf_budget.json).
LEDGER = '/root/klipt-state/hf_budget.json'
est = call('POST', 'https://api.higgsfield.ai/estimate/marketing-studio/image', body)
usd = float(est.get('usd', 0))
ledger = json.load(open(LEDGER)) if os.path.exists(LEDGER) else None
if ledger is not None and usd > ledger['remaining_usd'] + 1e-9:
    sys.exit(f'BUDGET GUARD: this image costs ${usd:.3f} but only ${ledger["remaining_usd"]:.3f} remains. Not generated.')
print(f'estimated cost ${usd:.3f}', file=sys.stderr)
t0 = time.time()
job = call('POST', API, body)
rid, status_url = job.get('request_id'), job.get('status_url')
while job.get('status') in ('queued', 'in_progress', None):
    time.sleep(3)
    job = call('GET', status_url or f'https://api.higgsfield.ai/requests/{rid}/status')
if job.get('status') != 'completed': sys.exit(f'generation {job.get("status")}: {job.get("error", "")}')
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
img_url = job['images'][0]['url']
r = subprocess.run(['curl', '-sfL', '-m', '120', '-o', a.out, img_url])
if r.returncode: sys.exit(f'could not download the image from {img_url.split("/")[2]} — allow that host too')
meta = dict(body, request_id=rid, seconds=round(time.time() - t0, 1), image_host=img_url.split('/')[2], cost_usd=usd)
if ledger is not None:
    ledger['remaining_usd'] = round(ledger['remaining_usd'] - usd, 4); ledger.setdefault('log', []).append(dict(out=a.out, usd=usd))
    json.dump(ledger, open(LEDGER, 'w'), indent=1)
json.dump(meta, open(a.out + '.json', 'w'), indent=1, ensure_ascii=False)
print(json.dumps(meta, ensure_ascii=False))

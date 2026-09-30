#!/usr/bin/env python3
"""Higgsfield video generation (text → video or image → video) with a shared budget guard.

  python3 tools/higgsfield_video.py <endpoint> --out pieces/<id>/assets/clip.mp4 --json '{"prompt": "...", "duration": 15, "aspect_ratio": "9:16"}'
  python3 tools/higgsfield_video.py <endpoint> --estimate --json '{...}'      → price only (free)

Endpoints tried and priced for 15 s, 9:16 (see docs/KLIPT_PRODUCTION.md for the table):
  kling-video/v3.0/std/text-to-video   {"sound":"off","multi_shots":true,"multi_prompt":[{"prompt":..,"duration":5},…]}
  kling-video/v3.0-turbo/image-to-video {"image_url":..,"resolution":"720p"}
  wan/v2.7/text-to-video · wan/v2.7/image-to-video {"resolution":"720p"}
  pixverse/v6/text-to-video {"resolution":"720p","generate_audio":false}
  minimax/hailuo-2.3/standard/text-to-video|image-to-video {"duration":6|10}   (768p, cheapest)
  minimax/h3/text-to-video {"resolution":"2K"} · alibaba/happy-horse/text-to-video {"resolution":"720p"}
Image inputs must be public URLs: upload local files with tools/higgsfield_upload.py first.
Credentials: $HF_KEY or /root/klipt-state/higgsfield.key — never in the repo.
"""
import argparse, json, os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hf_ledger

def key():
    k = os.environ.get('HF_KEY')
    if not k and os.path.exists('/root/klipt-state/higgsfield.key'): k = open('/root/klipt-state/higgsfield.key').read().strip()
    if not k: sys.exit('No Higgsfield key (set HF_KEY).')
    return k

def call(method, url, body=None):
    cmd = ['curl', '-s', '-m', '60', '-X', method, url, '-H', f'Authorization: Key {key()}', '-H', 'Content-Type: application/json', '-w', '\n%{http_code}']
    if body is not None: cmd += ['--data', json.dumps(body)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit(f'network error reaching {url.split("/")[2]} (curl {r.returncode})')
    text, code = r.stdout.rsplit('\n', 1)
    try: data = json.loads(text)
    except json.JSONDecodeError: data = {'raw': text[:500]}
    if not code.startswith('2'): sys.exit(f'HTTP {code}: {json.dumps(data)[:500]}')
    return data

a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
a.add_argument('endpoint'); a.add_argument('--json', required=True); a.add_argument('--out'); a.add_argument('--estimate', action='store_true')
a = a.parse_args()
body = json.loads(a.json)
est = call('POST', f'https://api.higgsfield.ai/estimate/{a.endpoint}', body)
if 'usd' not in est: sys.exit(f'no fixed estimate for this endpoint (token-metered?): {json.dumps(est)[:400]}')
usd = float(est['usd'])
if a.estimate: print(json.dumps(dict(endpoint=a.endpoint, usd=usd))); sys.exit()
if not a.out: sys.exit('--out is required')
hf_ledger.reserve(usd, a.out)
print(f'estimated cost ${usd:.3f}', file=sys.stderr)
t0 = time.time()
try:
    job = call('POST', f'https://api.higgsfield.ai/{a.endpoint}', body)
except SystemExit: hf_ledger.refund(usd, a.out); raise
rid, status_url = job.get('request_id'), job.get('status_url')
while job.get('status') in ('queued', 'in_progress', None):
    time.sleep(5)
    job = call('GET', status_url or f'https://api.higgsfield.ai/requests/{rid}/status')
if job.get('status') != 'completed': hf_ledger.refund(usd, a.out); sys.exit(f'generation {job.get("status")}: {json.dumps(job)[:400]}')
url = (job.get('video') or {}).get('url') or (job.get('videos') or [{}])[0].get('url')
if not url: sys.exit(f'no video url in response: {json.dumps(job)[:400]}')
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
r = subprocess.run(['curl', '-sfL', '-m', '300', '-o', a.out, url])
if r.returncode: sys.exit(f'could not download the video from {url.split("/")[2]} — allow that host too')
meta = dict(endpoint=a.endpoint, request=body, request_id=rid, seconds=round(time.time() - t0, 1), cost_usd=usd, video_host=url.split('/')[2])
json.dump(meta, open(a.out + '.json', 'w'), indent=1, ensure_ascii=False)
print(json.dumps(meta, ensure_ascii=False))

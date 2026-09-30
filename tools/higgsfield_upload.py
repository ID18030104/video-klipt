#!/usr/bin/env python3
"""Upload a local file (logo, plate, product photo) to Higgsfield and print its public URL, for use as
`image_urls` (Marketing Studio references) or `image_url` (image → video start frame). Free.

  python3 tools/higgsfield_upload.py brand/klipt/logo-dark.png
"""
import json, mimetypes, os, subprocess, sys

path = sys.argv[1]
k = os.environ.get('HF_KEY') or open('/root/klipt-state/higgsfield.key').read().strip()
ct = mimetypes.guess_type(path)[0] or 'application/octet-stream'
r = subprocess.run(['curl', '-s', '-m', '60', '-X', 'POST', 'https://api.higgsfield.ai/files/generate-upload-url',
                    '-H', f'Authorization: Key {k}', '-H', 'Content-Type: application/json', '--data', json.dumps(dict(content_type=ct))],
                   capture_output=True, text=True)
up = json.loads(r.stdout)
if 'upload_url' not in up: sys.exit(f'upload url refused: {r.stdout[:300]}')
cmd = ['curl', '-sf', '-m', '300', '-X', 'PUT', up['upload_url'], '--data-binary', '@' + path]
for h, v in up.get('upload_headers', {'Content-Type': ct}).items(): cmd += ['-H', f'{h}: {v}']
if subprocess.run(cmd).returncode: sys.exit('upload failed')
print(up['public_url'])

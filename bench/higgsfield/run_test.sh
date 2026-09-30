#!/usr/bin/env bash
# Cheap-image test: the same Klipt prompts at 1k in low / medium quality (≈ budget $0.34).
# Run from the repo root once api.higgsfield.ai (and the image host) are reachable.
set -e
cd "$(dirname "$0")/../.."
python3 - <<'PY'
import json, subprocess
for p in json.load(open('bench/higgsfield/prompts.json')):
    for q in ('low', 'medium'):
        out = f"bench/higgsfield/{p['name']}-1k-{q}.png"
        subprocess.run(['python3', 'tools/higgsfield_image.py', p['prompt'], '--out', out, '--resolution', '1k', '--quality', q, '--aspect', p['aspect']], check=False)
PY

#!/bin/bash
# Animate one plate with Hailuo 2.3 image-to-video (6 s, 768p). Usage: run_hailuo.sh <n> "<motion prompt>"
cd /home/user/video-klipt
u=$(python3 tools/higgsfield_upload.py bench/video/hailuo-plate$1.png) || exit 1
echo "$u" > bench/video/hailuo-plate$1.url
python3 tools/higgsfield_video.py minimax/hailuo-2.3/standard/image-to-video --out bench/video/hailuo-shot$1.mp4 \
  --json "$(python3 -c 'import json,sys;print(json.dumps(dict(prompt=sys.argv[1],image_url=sys.argv[2],duration=6)))' "$2" "$u")"

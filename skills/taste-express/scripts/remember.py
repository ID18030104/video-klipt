"""Record what a finished piece used, so later draws and choices avoid repeating it.

Usage:
  python remember.py --id <draw id> --brand NAME --concept "one line" --fonts "A, B" \
      --palette "#hex #hex #hex" --layout "one line" --device "one line" [--files "a.png b.png"]
"""
import argparse
import json
import sys
import time
from pathlib import Path

HISTORY = Path(__file__).resolve().parent.parent / "memory" / "history.jsonl"


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows consoles default to cp1252
    ap = argparse.ArgumentParser()
    for name in ("id", "brand", "concept", "fonts", "palette", "layout", "device"):
        ap.add_argument(f"--{name}", required=True)
    ap.add_argument("--files", default="")
    args = ap.parse_args()
    record = {"type": "piece", "time": time.strftime("%Y-%m-%d %H:%M:%S"), **vars(args)}
    HISTORY.parent.mkdir(exist_ok=True)
    with HISTORY.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"remembered: [{args.brand}] {args.concept}")


if __name__ == "__main__":
    main()

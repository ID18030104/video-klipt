"""Draw creative provocations for one piece, avoiding what recent pieces already used.

Usage:
  python draw.py "<one-line brief>" [--brand NAME] [--social]

Prints 3 creative operators, 4 foreign domains, 1 constraint (and 1 format mechanic with --social),
then what the last pieces already did (concepts, fonts, palettes, layouts) so the new one goes elsewhere.
The draw is recorded in memory/history.jsonl; pass its id to remember.py when the piece is done.
"""
import argparse
import hashlib
import json
import sys
import random
import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CREATIVE = ROOT / "creative"
HISTORY = ROOT / "memory" / "history.jsonl"
EXCLUDE_LAST_DRAWS = 12   # drawn items of the last N draws are not drawn again
SHOW_LAST_PIECES = 8      # finished pieces listed as "already done"
OPERATOR_LINE = re.compile(r"^- \*\*(?P<name>[^*]+)\*\*: (?P<text>.+)$")


def load_lines(name: str) -> list[str]:
    return [l.strip() for l in (CREATIVE / name).read_text(encoding="utf-8").splitlines() if l.strip()]


def load_operators() -> dict[str, str]:
    ops = {}
    for line in (CREATIVE / "operators.md").read_text(encoding="utf-8").splitlines():
        m = OPERATOR_LINE.match(line.strip())
        if m:
            ops[m["name"]] = m["text"]
    return ops


def load_history() -> list[dict]:
    if not HISTORY.exists():
        return []
    rows = []
    for line in HISTORY.read_text(encoding="utf-8").splitlines():
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def pick(rng: random.Random, pool: list[str], used: set[str], k: int) -> list[str]:
    fresh = [x for x in pool if x not in used]
    source = fresh if len(fresh) >= k else pool
    return rng.sample(source, k)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows consoles default to cp1252
    ap = argparse.ArgumentParser()
    ap.add_argument("brief")
    ap.add_argument("--brand", default="")
    ap.add_argument("--social", action="store_true")
    args = ap.parse_args()

    history = load_history()
    draws = [h for h in history if h.get("type") == "draw"][-EXCLUDE_LAST_DRAWS:]
    used = {key: {v for d in draws for v in (d.get(key) or [])} for key in ("operators", "domains")}
    used["constraint"] = {d.get("constraint") for d in draws}
    used["mechanic"] = {d.get("mechanic") for d in draws}

    seed = time.time_ns() ^ int(hashlib.sha1(args.brief.encode("utf-8")).hexdigest()[:12], 16)
    rng = random.Random(seed)
    operators = load_operators()
    chosen_ops = pick(rng, sorted(operators), used["operators"], 3)
    domains = pick(rng, load_lines("domains.txt"), used["domains"], 4)
    constraint = pick(rng, load_lines("constraints.txt"), used["constraint"], 1)[0]
    mechanic = pick(rng, load_lines("mechanics.txt"), used["mechanic"], 1)[0] if args.social else None

    draw_id = f"{time.strftime('%Y%m%d-%H%M%S')}-{rng.randrange(16 ** 4):04x}"
    record = {"type": "draw", "id": draw_id, "time": time.strftime("%Y-%m-%d %H:%M:%S"), "brand": args.brand,
              "brief": args.brief, "operators": chosen_ops, "domains": domains, "constraint": constraint, "mechanic": mechanic}
    HISTORY.parent.mkdir(exist_ok=True)
    with HISTORY.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"DRAW {draw_id}")
    print("\nOperators (apply them to the fragments you mined):")
    for name in chosen_ops:
        print(f"  - {name}: {operators[name]}")
    print("\nForeign domains (collide the brand's truth with them):")
    for d in domains:
        print(f"  - {d}")
    print(f"\nConstraint (optional, use it if it sharpens the idea): {constraint}")
    if mechanic:
        print(f"Format mechanic (optional): {mechanic}")

    pieces = [h for h in history if h.get("type") == "piece"][-SHOW_LAST_PIECES:]
    if pieces:
        print("\nAlready done recently (go somewhere else; brand constants excepted):")
        for p in pieces:
            print(f"  - [{p.get('brand', '')}] {p.get('concept', '')} | fonts: {p.get('fonts', '')} | palette: {p.get('palette', '')}"
                  f" | layout: {p.get('layout', '')} | device: {p.get('device', '')}")
    else:
        print("\nNo previous pieces recorded yet.")


if __name__ == "__main__":
    main()

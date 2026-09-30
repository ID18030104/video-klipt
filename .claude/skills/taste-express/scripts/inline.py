"""Inline local kit.css / kit.js (or any local stylesheet/script) into an HTML file -> self-contained deliverable.

Usage: python inline.py page.html [more.html ...]      (rewrites each file in place)
Remote URLs (Google Fonts, CDN) are left untouched.
"""
import re
import sys
from pathlib import Path

LINK = re.compile(r'<link\s+[^>]*rel=["\']stylesheet["\'][^>]*href=["\'](?P<href>[^"\':]+)["\'][^>]*>', re.I)
SCRIPT = re.compile(r'<script\s+[^>]*src=["\'](?P<src>[^"\':]+)["\'][^>]*>\s*</script>', re.I)


def inline(path: Path) -> int:
    html = path.read_text(encoding="utf-8")
    count = 0

    def css(m: re.Match) -> str:
        nonlocal count
        target = (path.parent / m["href"]).resolve()
        if not target.is_file():
            return m.group(0)
        count += 1
        return f"<style>/* {m['href']} */\n{target.read_text(encoding='utf-8')}</style>"

    def js(m: re.Match) -> str:
        nonlocal count
        target = (path.parent / m["src"]).resolve()
        if not target.is_file():
            return m.group(0)
        count += 1
        return f"<script>/* {m['src']} */\n{target.read_text(encoding='utf-8')}</script>"

    html = SCRIPT.sub(js, LINK.sub(css, html))
    path.write_text(html, encoding="utf-8")
    return count


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for arg in sys.argv[1:]:
        p = Path(arg)
        if not p.is_file():
            sys.exit(f"not found: {p}")
        print(f"{p.name}: {inline(p)} file(s) inlined")


if __name__ == "__main__":
    main()

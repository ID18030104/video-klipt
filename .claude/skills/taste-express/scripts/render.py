"""Render HTML pieces to PNG fast: warm Chromium kept alive between calls, all pieces rendered in parallel.

Usage:
  python render.py <file.html:WxH[@scale]> [more specs...] [--preview] [--settle MS]
  python render.py --stop          # shut the warm browser down now (it also stops by itself after 10 min idle)

  python render.py landing.html:1440x900 post.html:1080x1350 app.html:390x844@3 --preview
  python render.py carousel.html:6480x1350/6 --preview      # one wide strip, sliced into 6 slides

Each spec writes <file>.png next to the HTML. A "/N" suffix slices the render into N equal
slides: <file>-01.png ... <file>-0N.png (the strip itself is kept as <file>.png).
--preview also writes <file>.preview.jpg (max 900 px wide, or 450 px per slide for a carousel):
read THAT to review, it costs a fraction of the tokens of the PNG.
The first call starts a background Chromium (~10 s); later calls reuse it (~2-4 s per batch).
"""
import asyncio
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

from playwright.async_api import async_playwright

SPEC = re.compile(r"^(?P<path>.+\.html?):(?P<w>\d+)x(?P<h>\d+)(?:@(?P<scale>[\d.]+))?(?:/(?P<slices>\d+))?$")
PORT = 9333
CDP_URL = f"http://127.0.0.1:{PORT}"
STATE = Path(tempfile.gettempdir()) / "taste-express-render"
STAMP, STOP = STATE / "last-use", STATE / "stop"
IDLE_SECONDS = 600
PREVIEW_MAX_W = 900
PREVIEW_SLIDE_W = 450
DEFAULT_SETTLE_MS = 1200


def cdp_alive() -> bool:
    try:
        with urllib.request.urlopen(f"{CDP_URL}/json/version", timeout=1):
            return True
    except OSError:
        return False


def spawn_daemon() -> None:
    STATE.mkdir(exist_ok=True)
    STOP.unlink(missing_ok=True)
    flags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
    subprocess.Popen([sys.executable, __file__, "--daemon"], creationflags=flags, start_new_session=os.name != "nt",
                     stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True)
    deadline = time.time() + 40
    while time.time() < deadline:
        if cdp_alive():
            return
        time.sleep(0.3)
    raise RuntimeError("warm browser did not start")


async def run_daemon() -> None:
    """Background process: owns a Chromium with a CDP port, exits after IDLE_SECONDS without renders."""
    async with async_playwright() as p:
        exe = p.chromium.executable_path
    STATE.mkdir(exist_ok=True)
    STAMP.touch()
    proc = subprocess.Popen([exe, "--headless=new", f"--remote-debugging-port={PORT}", f"--user-data-dir={STATE / 'profile'}",
                             "--no-first-run", "--no-default-browser-check", "--hide-scrollbars", "--mute-audio"],
                            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        while proc.poll() is None:
            await asyncio.sleep(10)
            if STOP.exists() or time.time() - STAMP.stat().st_mtime > IDLE_SECONDS:
                break
    finally:
        proc.terminate()
        STOP.unlink(missing_ok=True)


def parse_args(argv: list[str]) -> tuple[list[dict], bool, int]:
    specs, preview, settle = [], False, DEFAULT_SETTLE_MS
    it = iter(argv)
    for arg in it:
        if arg == "--preview":
            preview = True
        elif arg == "--settle":
            settle = int(next(it))
        else:
            m = SPEC.match(arg)
            if not m:
                sys.exit(f"bad spec: {arg!r} (expected file.html:WxH[@scale][/slides])")
            path = Path(m["path"]).resolve()
            if not path.is_file():
                sys.exit(f"not found: {path}")
            specs.append({"path": path, "w": int(m["w"]), "h": int(m["h"]), "scale": float(m["scale"] or 1),
                          "slices": int(m["slices"] or 1)})
    if not specs:
        sys.exit(__doc__)
    return specs, preview, settle


def write_preview(png: Path, slices: int = 1) -> Path:
    from PIL import Image

    out = png.with_suffix(".preview.jpg")
    max_w = PREVIEW_SLIDE_W * slices if slices > 1 else PREVIEW_MAX_W
    with Image.open(png) as im:
        im = im.convert("RGB")
        if im.width > max_w:
            im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
        im.save(out, "JPEG", quality=82)
    return out


def write_slices(png: Path, slices: int) -> list[Path]:
    """Cut a carousel strip into equal slides: <stem>-01.png ..."""
    from PIL import Image

    outs = []
    with Image.open(png) as im:
        step = im.width // slices
        for k in range(slices):
            out = png.with_name(f"{png.stem}-{k + 1:02d}.png")
            im.crop((k * step, 0, (k + 1) * step, im.height)).save(out)
            outs.append(out)
    return outs


async def render_one(browser, spec: dict, preview: bool, settle: int) -> str:
    context = await browser.new_context(viewport={"width": spec["w"], "height": spec["h"]}, device_scale_factor=spec["scale"])
    page = await context.new_page()
    errors: list[str] = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    try:
        await page.goto(spec["path"].as_uri(), wait_until="networkidle", timeout=60000)
        await page.evaluate("document.fonts.ready")
        await page.wait_for_timeout(settle)
        png = spec["path"].with_suffix(".png")
        await page.screenshot(path=str(png), full_page=False)
    finally:
        await context.close()
    line = f"ok {png.name} {int(spec['w'] * spec['scale'])}x{int(spec['h'] * spec['scale'])}"
    if spec["slices"] > 1:
        cuts = write_slices(png, spec["slices"])
        line += f" -> {len(cuts)} slides {cuts[0].name}..{cuts[-1].name}"
    if preview:
        line += f" -> {write_preview(png, spec['slices']).name}"
    return line + "".join(f"\n   JS ERROR in {spec['path'].name}: {e}" for e in errors)


async def render(specs: list[dict], preview: bool, settle: int) -> None:
    t0 = time.time()
    if not cdp_alive():
        spawn_daemon()
    STAMP.touch()
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        lines = await asyncio.gather(*(render_one(browser, s, preview, settle) for s in specs))
    print("\n".join(lines))
    print(f"rendered {len(specs)} piece(s) in {time.time() - t0:.1f}s")


def main() -> None:
    args = sys.argv[1:]
    if args == ["--daemon"]:
        asyncio.run(run_daemon())
    elif args == ["--stop"]:
        STATE.mkdir(exist_ok=True)
        STOP.touch()
        print("warm browser will stop within 10 s")
    else:
        asyncio.run(render(*parse_args(args)))


if __name__ == "__main__":
    main()

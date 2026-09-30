# Klipt render contract (technical)

Every piece lives in its own folder `pieces/<PIECE_ID>/` and is authored as **one HTML page** (`index.html`, plus optional local CSS/JS/SVG files in the same folder). A deterministic renderer (Chromium + ffmpeg) turns it into an MP4 or PNG slides.

## Hard rules
- **Offline.** No `http(s)://` URLs — the renderer has no internet. Anything remote fails silently and ruins the render.
- Reference shared assets with relative paths from the piece folder: `../../node_modules/...` and `../../lib/...`.
- **Deterministic.** The frame at time `t` must depend only on `t`. No `Date.now()`, no un-seeded `Math.random()`, no `requestAnimationFrame` loops, no `setTimeout`/`setInterval` driving animation, no `<video>`/`<audio>`. Use `KK.rng(seed)` from `lib/klipt-kit.js` for randomness (generate random values once at load, not per frame).
- Page body must be exactly the canvas size (`margin:0; overflow:hidden`).
- Do not read or copy other folders in `pieces/` — each piece is an independent creation.
- Do not run `git` commands.
- **Never kill processes you did not start** (`pkill -f render.mjs`, `killall node`, `killall chrome`…): other designers render in parallel on this machine and you would destroy their work. To stop your own render, kill its PID only. A render that prints "waiting for a free render slot…" is queued, not stuck.

## Video pieces
Define, before or at load:
```js
window.KLIPT = {
  width: 1080, height: 1920, fps: 30, duration: 20, // seconds, 10–30
  ready: somePromise,        // optional: resolved when async assets (textures, 3D) are ready
  render(t) { /* draw the exact state at t seconds */ },
};
```
- **GSAP**: build one `gsap.timeline({paused:true})`, then `render: t => { tl.seek(t, false); }` (do NOT return the timeline).
- **CSS `@keyframes` / Web Animations**: automatically paused and scrubbed to `t` by the renderer — they just work.
- **Canvas / three.js**: redraw everything from `t` inside `render(t)`; create the WebGL renderer with `preserveDrawingBuffer: true`. WebGL runs in software (SwiftShader): keep geometry/shaders reasonable, no heavy post-processing.

## Still pieces (posts, carousels, stories)
- Each image is a `<section class="slide">` sized exactly `width × height`, stacked vertically in the page.
- `window.KLIPT = { width: 1080, height: 1350 };` (no duration/render needed). Static CSS only (or scripts that run once at load).

## Formats
| Use | Size |
|---|---|
| Reel / TikTok / Story (9:16) | 1080 × 1920 |
| Feed portrait / carousel (4:5) | 1080 × 1350 |
| Square post (1:1) | 1080 × 1080 |
| Landscape / web hero (16:9) | 1920 × 1080 |

## Commands (run from repo root)
```bash
node tools/render.mjs frame  pieces/<id> 3.2 /tmp/<id>-3.2.png   # one frame at t=3.2s — fast check (then view the PNG)
node tools/render.mjs video  pieces/<id> --preview                 # 10 fps draft → preview.mp4 + sheet.jpg (12-frame contact sheet)
node tools/render.mjs video  pieces/<id>                           # FINAL 30 fps → video.mp4 + poster.jpg + sheet.jpg
node tools/render.mjs stills pieces/<id>                           # slides/slide-01.png … + sheet.jpg
node tools/render.mjs qa     pieces/<id>                           # qa.jpg (labelled keyframes) + automatic defect report
```
Set `KLIPT.poster = <seconds>` to choose the video's thumbnail frame (default 62 % of the duration — often mid-transition).
The renderer prints page errors (JS errors, failed file loads) and exits with code 3 if any — fix them. `sheet.jpg` and single frames are images you can open to check your work visually. A 20 s final render takes ~1–2 min.

## Available offline assets
- **Animation / graphics**: `gsap` (`../../node_modules/gsap/dist/gsap.min.js`, all plugins incl. SplitText, DrawSVGPlugin, MorphSVGPlugin, MotionPathPlugin, ScrambleTextPlugin, TextPlugin, CustomEase, Physics2DPlugin), `three` (use an importmap: `{"imports":{"three":"../../node_modules/three/build/three.module.js","three/addons/":"../../node_modules/three/examples/jsm/"}}` — RoomEnvironment, RoundedBoxGeometry, TextGeometry+fonts, etc.), `d3` (`../../node_modules/d3/dist/d3.min.js`), `simplex-noise` (ESM, `../../node_modules/simplex-noise/dist/esm/simplex-noise.js`), `lib/klipt-kit.js` (seeded RNG, easings, `prog`, `lerp`).
- **Icons**: 2,100+ Lucide SVGs in `../../node_modules/lucide-static/icons/<name>.svg` (inline them or use as `<img>`).
- **Fonts** (`<link rel="stylesheet" href="../../node_modules/@fontsource/<name>/index.css">` for weight 400; other weights: `/700.css`, `/800.css`, `/400-italic.css`… — check the folder): abril-fatface, anton, archivo-black, baloo-2, barlow-condensed, bebas-neue, big-shoulders-display, bodoni-moda, bricolage-grotesque, caveat, chivo, cormorant-garamond, dela-gothic-one, dm-serif-display, eb-garamond, familjen-grotesk, figtree, fraunces, gloock, ibm-plex-mono, ibm-plex-sans, instrument-serif, inter, jetbrains-mono, kalam, libre-baskerville, lobster, major-mono-display, manrope, montserrat, nunito, oswald, pacifico, permanent-marker, playfair-display, poppins, press-start-2p, righteous, rubik-mono-one, shrikhand, sora, space-grotesk, space-mono, syne, unbounded, work-sans, young-serif, zilla-slab, outfit.
- **Real photos & footage (Pexels, free licence)** — `python3 tools/pexels.py -h`: search photos/videos (a numbered contact sheet to look at), download 4K originals (`photo-get`, keep them in `pieces/<id>/assets/`), or cut a video clip into a frame sequence (`video-get`, into `pieces/<id>/footage/<name>/`) played with `KK.footage()`. Search and download at build time only; the page must reference the local files.
- **Any Google Font**: `python3 tools/gfont.py "<Family>" "<axes>" pieces/<id>/fonts` downloads it locally (e.g. `"Inter Tight" "wght@400;800"`).

## Required deliverables in `pieces/<id>/`
1. `index.html` (+ local files) 2. the final render (`video.mp4` + `poster.jpg` + `sheet.jpg`, or `slides/*.png` + `sheet.jpg`) 3. `meta.json`:
```json
{ "id": "...", "brand": "...", "sector": "...", "kind": "video|carousel|post|story",
  "format": "1080x1920", "duration": 20, "slides": null,
  "title": "short title of the piece", "concept": "1–2 sentences on the idea and art direction",
  "techniques": ["gsap", "svg-illustration", "three.js", "..."], "fonts": ["..."], "palette": ["#hex", "..."],
  "copy_language": "fr" }
```
Delete `preview.mp4` and any scratch frames when you are done.

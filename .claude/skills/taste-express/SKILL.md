---
name: taste-express
description: Original visual design, delivered fast — Instagram/LinkedIn posts and carousels, stories, landing pages, app screens. A built-in creative cell (mine the brief, random provocations, 8 concepts, scoring, language derived from the concept, three-voice critique, memory of past pieces) makes every piece original in its own way and different from the previous ones; a ready kit (carousel strips auto-sliced, material devices, procedural imagery, charts, iOS parts, warm one-call render) keeps it fast. Merges design-taste-frontend, gpt-taste, apple-design and ui-ux-pro-max.
---

# Taste Express

Every piece original in its own way, delivered fast.
1. **Create** with the creative cell (§1): the look is born from a concept, never from a house style.
2. **Execute** with the kit (§2 onwards): one render call, one fix pass.

What each source skill brings: design-taste-frontend (reading the brief, refusing defaults), gpt-taste (bold composition, variety by random draw), apple-design (craft, materials, familiarity for app UI), ui-ux-pro-max (professional app rules, final checks).
Skill folder (below: `SKILL_DIR`): `~/.claude/skills/taste-express/`.

## 0. Speed contract

Budget: **one post ≤ 6 min, a 6–8 slide carousel ≤ 10 min**, of which ~3 min for the creative cell.
- The cell is written as short lines in `design-card.md`: no essays, no searching.
- Compose from the kit: never hand-write noise, textures, hand-drawn marks, status bars or chart SVG.
- **One render call for all pieces** (`scripts/render.py`: warm Chromium, parallel pages, carousels sliced automatically).
- Review the `.preview.jpg`, never the full PNG. One fix pass with targeted edits.
- Several independent pieces (a series of posts): one sub-agent per piece if available, each running its own cell and draw.

## 1. Create: the creative cell (mandatory, before any code)

Read `SKILL_DIR/creative/CELL.md` and run its 9 steps. In short:
1. **Mine the brief**: 10–15 concrete fragments plus one truth sentence.
2. **Name your autopilot**: what you would do without thinking, plus what recent pieces did. That is the zone to leave.
3. **Draw provocations**: `python SKILL_DIR/scripts/draw.py "<brief>" --brand <name> [--social]` gives operators, foreign domains, a constraint and a format mechanic, avoiding recent ones.
4. **Diverge**: 8 genuinely different concepts, at least 5 built from the draw.
5. **Converge**: score Truth, Surprise, Stop, Clarity, Feasible, Fresh; pick one.
6. **Derive the language from the concept**: composition, type, colour, material, each justified by the concept, and checked against the history.
7. **Commit** to one bold move and push it.
8. **Critique** the first render with three voices: art director, stranger in the feed, AI detector.
9. **Remember**: `python SKILL_DIR/scripts/remember.py …` so the next piece goes elsewhere.

There are no house styles, no recommended or forbidden fonts, colours or components. Anything is allowed when the concept calls for it; nothing is allowed by default.

## 2. Execute

**Step 1 — Design card (`design-card.md`)**: fragments and truth, autopilot, draw id and draw, 8 scored concepts, the choice, the derived language (with reasons), the bold move, the tokens (hex colours, Google Fonts).

**Step 2 — Set up.** Copy `SKILL_DIR/kit/kit.css` and `kit.js` next to the outputs. Head:
```html
<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=<the fonts the concept chose>&display=swap" rel="stylesheet">
<link rel="stylesheet" href="kit.css">
<style>:root{ /* tokens derived in the cell */ } /* page CSS */</style>
</head><body> … <script src="kit.js"></script></body></html>
```
The kit's default tokens are neutral placeholders: always set your own. Icons, if the concept needs them: Phosphor (`https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.1/src/regular/style.css`) or drawn in the concept's own style.

**Step 3 — Build.** Posts `<main class="artboard post">` (1080×1350; `.square`, `.story`), any size `style="--w:…;--h:…"`, app screens `<main class="artboard ios">`, carousels `<main class="carousel" style="--n:6">` (§4).

**Step 4 — Render everything in one call.**
```bash
python SKILL_DIR/scripts/render.py post.html:1080x1350 strip.html:6480x1350/6 app.html:390x844@3 --preview
```
Read the `*.preview.jpg`. Fix JS errors first. The warm browser stops after 10 min idle (`--stop` to stop it now).

**Step 5 — Critique, one fix pass, remember, ship.** Three-voice critique (cell step 8), targeted edits, re-render only what changed, then `remember.py`. Single-file deliverable: `python SKILL_DIR/scripts/inline.py *.html`.

## 3. Craft floors (quality, whatever the concept)

These are about quality, not style.
- **Type craft**: tracking adapted to size (tight large, open small), leading adapted to size, a clear hierarchy (size + weight + colour together), aligned figures where numbers line up, no clipped descenders.
- **French**: non-breaking thin spaces before `€ % ? ! : ;` and inside thousands (`1 095 €`); typographic apostrophes (’); « guillemets ».
- **Legibility**: body ≥ 4.5:1 contrast, large text ≥ 3:1. Social at 1080 wide: body ≥ 30px, titles ≥ 64px; the post or carousel cover must read at 450px (feed size).
- **Imagery**: assets the user gave first; a generation tool only if available and paid use was allowed; otherwise the kit and drawing in the concept's own style. No div-built fake screenshots. Never imitate a real organisation's documents, logos or branding.
- **Copy**: the user's facts only. Never invent claims, figures or testimonials. Your own strings: no em-dash, no filler verbs, no cute AI wordplay.
- **App UI** (ui-ux-pro-max, apple-design): the concept carries the brand, familiarity carries the use. Status bar, 16px gutters, 44pt touch targets, answer first, tab bar ≤ 5 with the active item marked, content clear of fixed bars.
- **Motion** (only when the piece moves): every animation has a reason, entries settle ≤ 1.2 s, reduced motion honoured. See `references/motion.md`.

## 4. Social: posts and carousels

**Formats.** Post 1080×1350 (`.post`), square 1080×1080 (`.post.square`), story 1080×1920 (`.post.story`: keep the top 250px and bottom 340px free of text). Carousel: 5–8 slides of 1080×1350.

**A carousel is ONE strip, ONE render:**
```html
<main class="carousel" style="--n:6">
  <div class="pano"> …anything that runs under every slide… </div>
  <section class="slide"> … </section>  ×6
</main>
```
`render.py strip.html:6480x1350/6 --preview` writes `strip-01.png … strip-06.png` and a preview of the whole strip at feed size.

**Narrative.** The cover works alone in the profile grid (hook ≤ 8 words); one idea per slide; ≤ 40 words per slide; the last slide asks for one action. How the slides vary and connect (a panorama, a sequence, a reveal, a game, a zoom…) is decided by the concept, not by a template. At least one thing should make the viewer want the next slide.

## 5. Kit reference (tools, not a style)

| Need | Use |
|---|---|
| Tokens | `:root{--bg --surface --surface-2 --ink --ink-2 --muted --line --accent --on-accent --ok --warn --bad --font-display --font-body --font-mono --r-card --r-tile}` |
| Canvases | `.artboard` + `--w/--h`, `.post` (`.square` `.story`), `.ios`, `.carousel` + `--n`, `.pano`, `.slide`, `.layer` |
| Materials and marks | `.paper` (+`--paper`), `.halftone` (+`--dot`), `.riso` (`--ink-a --ink-b --mis-x --mis-y`), `.edge-zigzag-top/-bottom` (`--tooth`), `.edge-perforated-x`, `.rule-dotted .rule-dashed`, `.rough` (hand wobble), `.ink` (worn print), `.stamp` (`--tilt`), `.grain`, `<span data-annotate='{"type":"circle|underline|strike|box","color":"#…"}'>`, `<svg data-guilloche='{"color":"#…","rings":3}'>` |
| Procedural imagery | `<canvas class="layer" data-field='{"preset":"sea|lagoon|mist|aurora|ink|stone|dune","seed":4,"stops":[[0,"#…"],[1,"#…"]]}'>` (options: scale, warp, stretch, angle, ridge, glint, contrast, vignette) |
| Charts | `data-bars` / `data-area`: labels, values, highlight, decimal ",", unit, digits, thousands, `scale` (2.5–3 at 1080 wide) |
| Social type sizes | `.s-hook .s-title .s-body .s-label .s-figure` (sizes only; set your own fonts and styles) |
| UI parts | `.glass .glass-dark .card .tile .btn .btn-primary .chip .live .stat .progress[data-progress]` · iOS `data-kit="status"`, `.tabbar`, `.ios-row`, `.home-indicator` |
| Motion | `.fx-in` + `--i` |

Canvas, chart and annotation targets need their final CSS size before the kit runs.

## 6. Pre-flight (on the previews, before the fix pass)

1. `design-card.md` holds the full cell: fragments, truth, autopilot, draw, 8 scored concepts, choice, derived language, bold move.
2. The piece is far from the autopilot and from recent pieces (different concept, typefaces, palette and layout; brand constants excepted).
3. Every visual decision traces back to the concept; the bold move is visible.
4. Three-voice critique done; the top issue of each voice is fixed.
5. Reads at feed size: hook, three levels, word limits, body ≥ 30px at 1080.
6. Craft floors: contrast, French typography, the user's facts only, nothing clipped or overlapping, no JS errors.
7. `remember.py` run.

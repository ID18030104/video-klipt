# p273 — Greenloop · 2025 impact post (LinkedIn, 1080 × 1350, single still)

> Copy language: **English (UK spelling — "tonnes", "colour")**. The template asks for "French copy"; the brief sets `lang: en`, so every string below is final English copy. Use it exactly as written.

---

## 1. Audience insight & the one message

**Who scrolls past this:** CSR/ESG managers, facilities and procurement leads, hotel/hospital/logistics operations directors, 30–55, on LinkedIn between meetings. They buy uniforms, linen and workwear by the thousand and quietly know where the old ones end up: in a skip. They need proof they can **quote in their own CSR report**, not a sustainability mood board.

**Insight:** "128 tonnes" is impressive but abstract; nobody can picture a tonne of fabric. A T-shirt everyone can picture. The post has to turn the weight into things you can count, and make the counting look like hard data rather than decoration.

**The one message:** *In 2025, Greenloop put 128 tonnes of corporate textiles back into the loop. That's 640,000 T-shirts.*

Register: **credible, calm, a little proud.** Think data poster, not greenwashing. No leaves, no globes, no hands holding a sprout.

---

## 2. Concept — "Counted, not claimed"

A **pictogram data poster**. 128 small T-shirt pictograms in a strict 16 × 8 grid: **one T-shirt = one tonne = 5,000 T-shirts**. The whole grid is enclosed by a **single stitched thread** (a dashed "running-stitch" line) that forms a rounded closed loop with a direction arrow. It reads as *Greenloop*: nothing leaves the loop.

Why it fits:
- It proves instead of saying: you can literally count the 128 tonnes.
- It carries the name. The stitched loop is the brand mark scaled up to the size of the post, and it is textile-native: a seam, not a generic recycling arrow.
- It suits LinkedIn: one focal number, legible as a thumbnail, sober enough for a CSR director to reshare.

Maths check (for the legend): 128,000 kg ÷ 640,000 = 0.2 kg per T-shirt, so 1 tonne = 5,000 T-shirts. ✔

---

## 3. Art direction

### Palette
| Role | Name | Hex | Use |
|---|---|---|---|
| Dominant background | Undyed cotton | `#F3EFE6` | Page background |
| Primary ink | Loop forest | `#0F3B2E` | Headline, T-shirts, thread, logo |
| Text ink | Deep ink | `#12211B` | Sub-headline, footer text |
| T-shirt tone 2 | Forest mid | `#1F5645` | Grid variation |
| T-shirt tone 3 | Forest soft | `#2F6E59` | Grid variation |
| Accent (rare) | Fresh-fibre lime | `#D4F06A` | ONE highlighted T-shirt, legend pill, marker bar behind "640,000" |
| Hairlines | Kraft | `#D8D0BF` | Footer rule, weave texture |

Contrast: `#0F3B2E` on `#F3EFE6` ≈ 11:1. Lime is **never** used for text on cream; only as a fill behind forest text (`#0F3B2E` on `#D4F06A` ≈ 9:1).

### Typography (max 2 families)
- **Bricolage Grotesque**: 800, 600, 500, 300 (`@fontsource/bricolage-grotesque/800.css`, `600.css`, `500.css`, `300.css`). Display and headlines. Its slightly irregular, "hand-cut" grotesque feel suits a fabric brand.
- **IBM Plex Mono**: 400, 500 (`@fontsource/ibm-plex-mono/400.css`, `500.css`). Data labels, eyebrow, legend, URL. This is the "report" voice.
- Enable `font-variant-numeric: tabular-nums` on all numbers and `font-feature-settings: "ss01"` off (defaults).

| Element | Font | Size | Weight | Tracking | Line-height |
|---|---|---|---|---|---|
| Hero "128" | Bricolage | 184 px | 800 | −0.045em | 0.9 |
| Hero "tonnes" (same line) | Bricolage | 184 px | 300 | −0.04em | 0.9 |
| Sub-headline | Bricolage | 42 px | 500 | −0.01em | 1.2 |
| Equivalence number "640,000 T-shirts" | Bricolage | 96 px | 800 | −0.035em | 0.95 |
| Eyebrow above equivalence | Plex Mono | 30 px | 500 | +0.06em, UPPERCASE | 1 |
| Header tag (top right) | Plex Mono | 30 px | 500 | +0.06em, UPPERCASE | 1 |
| Legend pill | Plex Mono | 30 px | 500 | 0 | 1 |
| Footer line | Bricolage | 34 px | 600 | −0.01em | 1.1 |
| Footer URL | Plex Mono | 30 px | 500 | 0 | 1 |
| Wordmark "greenloop" | Bricolage | 44 px | 700 | −0.03em | 1 |

(Bricolage 700 is allowed for the wordmark only: load `700.css` too.)

### Graphic language
- **T-shirt pictogram**: one custom filled SVG `<symbol id="tee">` with viewBox `0 0 44 40`. Flat silhouette: shoulders with short sleeves angled down about 25°, a straight body, a small scooped neckline cut out (a crescent, rendered as part of the path using `fill-rule="evenodd"` or just a notch). Corners rounded ~2px (use `stroke-linejoin: round` with a 2px stroke in the same colour). No outline, no detail. **Do not use Lucide `shirt.svg`**: it's a stroke icon and looks generic at this size.
- **Stitch thread**: `stroke: #0F3B2E; stroke-width: 4; stroke-dasharray: 14 9; stroke-linecap: round; fill: none`. It's the running-stitch motif, used for the grid loop and the logo ring only.
- **Direction arrow** on the loop: a small solid chevron (forest, 22 px wide, stroke 4, round caps) placed on the top edge of the loop, pointing right (clockwise flow).
- **Marker bar**: a lime rectangle behind the digits "640,000", height 38% of the font size, sitting on the baseline (bottom offset −4 px), extending 8 px left and right of the digits, and rotated −1°. It should look like a highlighter pen, not a UI chip.

### Textures (subtle, it has to feel like fabric/paper and not flat)
1. **Grain**: full-page SVG `feTurbulence` (`type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="273"`), desaturated, `mix-blend-mode: multiply`, opacity **0.06**.
2. **Canvas weave**: two overlaid `repeating-linear-gradient`s (0° and 90°), 1 px lines of `#D8D0BF` every 6 px, at opacity **0.18**. It's barely visible, like undyed cotton seen up close. Apply it to the page background only (not over text).
3. A very soft vignette: `radial-gradient(ellipse at 50% 45%, transparent 60%, rgba(15,59,46,0.05) 100%)`.

### Logo
**Symbol + wordmark**, built in SVG:
- Symbol: a 40 px circle drawn as **stitched thread** (stroke 4, dasharray `7 5`, forest), with a **gap at 1 o'clock** filled by a tiny solid chevron arrow (clockwise), and a 9 px **lime dot** (`#D4F06A`, 1.5 px forest stroke) sitting on the ring at 7 o'clock, like a bead of fibre riding the loop.
- Wordmark: `greenloop`, all lowercase, Bricolage 700, 44 px, forest, 14 px to the right of the symbol, vertically centred.
- Use this exact lock-up in the header. The big grid loop is its echo, so keep the same dash rhythm ratio (stitch longer than gap).

---

## 4. Final copy (exact strings: use verbatim, including curly apostrophes and non-breaking spaces)

| # | Location | String |
|---|---|---|
| C1 | Header left | logo lock-up: `greenloop` |
| C2 | Header right | `2025 IMPACT` |
| C3 | Hero | `128 tonnes` (with a non-breaking space: `128&nbsp;tonnes`) |
| C4 | Sub-headline, line 1 | `of corporate uniforms, linen and workwear` |
| C5 | Sub-headline, line 2 | `collected and recycled in 2025.` |
| C6 | Legend pill (on the loop) | `= 1 tonne ≈ 5,000 T-shirts` (preceded by the lime T-shirt glyph) |
| C7 | Eyebrow | `THAT’S THE WEIGHT OF` |
| C8 | Equivalence | `640,000 T-shirts` (non-breaking space between the number and `T-shirts`) |
| C9 | Footer left | `Put your old workwear back in the loop.` |
| C10 | Footer right | `greenloop.eco →` |

Hard line breaks: C4/C5 break exactly as shown. C3 and C8 must stay on one line each.
Proofread notes: "T-shirts" has a capital T and a hyphen. "tonnes" is UK spelling (metric). Use `≈` (U+2248), not `~`. Use `’` (U+2019), not `'`. Number grouping uses commas (640,000 / 5,000).

**Suggested LinkedIn caption** (not rendered, for the client):
> 128 tonnes. That’s how much corporate textile (uniforms, bed linen, workwear) our clients sent back into the loop instead of the skip in 2025. Laid out as T-shirts, it comes to 640,000. Thank you to every hotel, hospital, fleet and kitchen that trusted us with their end-of-life textiles. Want your 2026 number in your CSR report? greenloop.eco

---

## 5. Layout (single slide: exact geometry, 1080 × 1350, origin top-left)

Side margins: **80 px** (content column x 80 → 1000, 920 px wide).

```
y   64 ┌ Header ───────────────────────────────────────────────┐
       │ [stitch ring] greenloop                     2025 IMPACT│   (row height 48, centred on y 88)
y  160 │ 128 tonnes                                             │   hero, baseline ≈ y 318
y  344 │ of corporate uniforms, linen and workwear              │
       │ collected and recycled in 2025.                        │   sub ends ≈ y 446
y  500 │ ╭─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ▶ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─╮   │   stitched loop top edge
       │ │  16 × 8 grid of T-shirts (128)                    │   │
       │ │                                                   │   │
y 1030 │ ╰─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ [▣ = 1 tonne ≈ 5,000 T-shirts]╯   │   pill sits ON the bottom edge, right-aligned
y 1086 │ THAT’S THE WEIGHT OF                                   │
y 1124 │ 640,000 T-shirts                                       │   (lime marker behind 640,000)
y 1240 │ ────────────────────────────────────────────────────── │   1 px rule #D8D0BF
y 1268 │ Put your old workwear back in the loop.  greenloop.eco →│
y 1300 └────────────────────────────────────────────────────────┘
```

### Details
- **Header** (centre line y 88): logo lock-up left at x 80. `2025 IMPACT` right-aligned to x 1000, forest, mono 30/500, preceded by a 10 px solid forest dot with a 12 px gap.
- **Hero** C3: left-aligned at x 72 (optical compensation of −8 px for the "1"), top of text box y 160. "128" weight 800 and "tonnes" weight 300, same size, both forest. If the measured width exceeds 920 px, reduce the font-size in 4 px steps until it fits (target ≈ 184 px).
- **Sub** C4/C5: x 80, top y 344, deep ink `#12211B`, 42/500.
- **Stitched loop**: SVG rounded rect x 64 → 1016, y 500 → 1030, rx 44, stitch style above. Leave a **gap on the top edge from x 520 to x 560** for the chevron arrow (pointing right, centred at x 540, y 500). On the bottom edge, the stroke is hidden behind the legend pill (the pill has the background colour plus a lime fill, so it "interrupts" the seam).
- **T-shirt grid**: 16 columns × 8 rows inside x 104 → 976 and y 540 → 990.
  - Column pitch = 872 / 16 = **54.5 px**; row pitch = 450 / 8 = **56.25 px**.
  - Each tee is 44 × 40 px, centred in its cell.
  - Fill order is left→right, top→bottom (index 0 top-left, 127 bottom-right).
  - Colour: seeded with `KK.rng(273)` at load. Each tee randomly picks `#0F3B2E` (60%), `#1F5645` (25%) or `#2F6E59` (15%). It should read as a fibre mix and not as a checkerboard.
  - **Tee #127 (bottom-right)** is the highlighted one: fill `#D4F06A` with a 2 px `#0F3B2E` outline. A 2 px forest leader line drops straight down from it to the legend pill.
- **Legend pill** C6: height 56, radius 28, fill `#D4F06A`, 2 px forest border, padding 0 24 px. Right edge at x 1000, vertically centred on y 1030 (the loop's bottom edge). Contents: a 28 × 26 tee glyph (forest), 12 px gap, then the text in forest mono 30/500.
- **Eyebrow** C7: x 80, top y 1086, forest, mono 30/500 uppercase +0.06em.
- **Equivalence** C8: x 76, top y 1124, Bricolage 96/800 forest, with the lime marker bar behind "640,000" only.
- **Footer**: 1 px rule `#D8D0BF` from x 80 to 1000 at y 1240. C9 left at x 80 (Bricolage 34/600, deep ink), C10 right-aligned at x 1000 (mono 30/500, forest), both vertically centred on y 1284. The `→` is part of the string.

Hierarchy check: the eye goes **128 tonnes → grid → 640,000 T-shirts → logo/URL**. As a thumbnail you should still be able to read "128 tonnes" and see a block of T-shirts inside a loop.

---

## 6. Motion notes
Still post, no motion. Do not add CSS animations. The only "movement" is implied: the chevron on the loop and on the logo ring, both clockwise. Keep them consistent.

---

## 7. Technical approach
- One `index.html` with a single `<section class="slide">` of 1080 × 1350 and `window.KLIPT = { width: 1080, height: 1350 };`. Body `margin:0; overflow:hidden; background:#F3EFE6`.
- Fonts via relative `<link>` to `../../node_modules/@fontsource/bricolage-grotesque/{300,500,600,700,800}.css` and `../../node_modules/@fontsource/ibm-plex-mono/{400,500}.css`. Wait for `document.fonts.ready` before measuring the hero width (fit loop).
- Build the whole grid + loop + arrows as **one inline SVG** absolutely positioned over the page (viewBox `0 0 1080 1350`). Generate 128 `<use href="#tee">` elements with a small inline script at load. Seeded colours come from `../../lib/klipt-kit.js` `KK.rng(273)`; do not use `Math.random`.
- Text is HTML (absolutely positioned divs) for crisp font rendering. The marker bar is a `::before` on a `<span class="hl">640,000</span>` with `z-index:-1` inside an isolated stacking context.
- Grain: inline SVG filter on a full-size `<rect>` with the opacity and blend mode given above. Weave: CSS gradients on `.slide` background.
- No external URLs, no photos. Render with `node tools/render.mjs stills pieces/p273`.
- `meta.json`: kind `post`, format `1080x1350`, duration null, slides 1, copy_language `en`, fonts `["Bricolage Grotesque","IBM Plex Mono"]`, palette `["#F3EFE6","#0F3B2E","#12211B","#D4F06A","#1F5645"]`, techniques `["svg-illustration","pictogram-dataviz","svg-grain","css-texture"]`, title "128 tonnes, counted".

### Review checklist for the builder
- [ ] You can count exactly 128 tees (16 × 8), with exactly one lime tee at bottom-right.
- [ ] Hero fits within 920 px on one line; nothing overlaps the loop.
- [ ] The pill truly interrupts the stitch (no dashes visible through it).
- [ ] Curly apostrophe in "THAT’S", `≈` in the legend, non-breaking spaces kept.
- [ ] Texture is visible at 100% zoom and invisible as noise at thumbnail size.

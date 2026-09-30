# p226 — Verne Woodworks — “Before the wood, the drawing.”

**Format** 1920 × 1080 · 30 fps · **21.0 s** · video (website hero + LinkedIn, sound-off)
**Copy language: English (US spelling, US units — feet/inches).** The generic template mentions French copy; the brief sets `"lang": "en"`, so ALL on-screen copy below is English and final. Do not translate.

---

## 1. Audience insight & the one message

**Who watches:** Brooklyn/NYC homeowners aged 35–60, often in brownstones and pre-war apartments with odd room sizes (bay windows, radiators, 11-foot ceilings, crooked walls). Also designers and architects on LinkedIn who refer clients. They have bought “solid wood” furniture that wobbled after five years; they suspect bespoke is slow and vague.

**Insight:** For these people the drawing *is* the proof. An architect-grade shop drawing, dimensioned to their own room, says “these people are precise” louder than any adjective. The drawing is also the part of a bespoke commission you never see — showing it is the differentiator.

**The one message:** *Designed for your room. Built to last 100 years.*
Everything in the film serves one of those two halves: the first half is precision (the drawing), the second is permanence (the wood, the years).

**Register:** artisanal-expert. Quiet confidence, precise, warm. No gimmicks, no fast cuts. LinkedIn-credible.

---

## 2. Concept

**“Before the wood, the drawing.”** One continuous sheet. We watch a Verne shop drawing being made: the client’s dining room is drafted in plan on a blueprint sheet, a walnut table is fitted into it with real clearances, the plan folds into a front elevation with a joinery detail — then a hand-plane pass sweeps across the sheet and the drawing *becomes* the table: blueprint turns to warm paper, chalk lines become ink, and the elevation fills with real walnut grain. A carpenter’s rule then runs from 2026 to 2126. Finally the little title block that sat in the corner of the drawing the whole time grows into the end card — the brand signs the drawing.

Why it fits: it is exactly how a two-person bespoke studio works (measure → draw → build), it turns the brief’s angle into a story rather than a decoration, and every number on screen is mathematically consistent, which is the kind of detail this audience notices.

---

## 3. Art direction

### Palette
| Role | Name | Hex |
|---|---|---|
| Dominant, act 1 | Prussian blueprint | `#1B3553` |
| Blueprint shadow/vignette | Deep diazo | `#12263D` |
| Line color on blueprint | Chalk | `#EDE6D6` |
| Dominant, act 2 | Drafting paper | `#F1EADC` |
| Line/text on paper | Ink | `#221C17` |
| Wood — walnut dark / mid / light | Walnut | `#3A2418` / `#5A3825` / `#7A5236` |
| Wood — oak (shaving wipe, oak accents) | Oak | `#C79A62` |
| Rare accent (max 3 uses: the “100”, the key dimension highlight, CTA underline) | Red pencil | `#C24A2C` |

Contrast: Chalk on Prussian ≈ 10:1; Ink on paper ≈ 15:1. Red pencil is never used for body text.

### Typography (2 families + no third)
- **Fraunces** (`@fontsource/fraunces/400.css`, `400-italic.css`, `600.css`) — headlines & wordmark. Set `font-variation-settings` not needed; use static weights.
- **IBM Plex Mono** (`@fontsource/ibm-plex-mono/400.css`, `500.css`) — all dimensions, annotations, labels, title block, URL.

Scale (1920 × 1080):
| Use | Font | Size / line-height / tracking |
|---|---|---|
| Headline (H1) | Fraunces 400, one word in 400-italic | 96 px / 1.02 / −0.01em |
| Headline payoff “Built to last 100 years.” | Fraunces 400 (“100” in 600, red pencil) | 112 px / 1.0 / −0.015em |
| Subline | Fraunces 400 | 38 px / 1.25 |
| Annotation labels (sheet) | Plex Mono 500, UPPERCASE | 22 px / tracking 0.08em |
| Dimension numbers | Plex Mono 500 | 26 px (key dims 30 px) |
| Kicker above headlines | Plex Mono 500, UPPERCASE | 22 px / tracking 0.14em |
| Wordmark | Fraunces 600, UPPERCASE | 64 px (end card), 24 px (corner block) / tracking 0.12em |
| URL (end card) | Plex Mono 500 | 40 px |

Minimum on-screen text size is 22 px (mono caps). Prime marks: use real ′ (U+2032) and ″ (U+2033), never ' and ".

### Graphic language
- **Drafting conventions, done right:** 1-px fine lines (1.25 px for object lines, 0.75 px for hidden/center lines, 2 px for walls with a 45° hatch fill at 10 px spacing). Dimension lines with small 45° tick marks (architectural “slash” terminators, 12 px long), extension lines with 6 px gap from the object. Dashed center lines (dash 18/4/3/4). Door swing as a quarter arc. Window as a triple thin line in the wall.
- **Grid:** blueprint sheet has a 24 px minor grid (Chalk at 5 % opacity) and a 120 px major grid (Chalk at 9 %). Paper sheet has the same grid in Ink at 4 % / 7 %.
- **Sheet border:** 1.5 px frame inset 40 px from the canvas edges, with zone markers along the top and left edges (Plex Mono 500, 18 px, 60 % opacity: “1 2 3 4 5 6” centered in six equal zones across the top margin, “A B C” centered in three equal zones down the left margin — decorative, the only text allowed under 22 px). Stays on screen through the whole film (color follows the sheet: Chalk → Ink).
- **Title block** (bottom-right, always present until it becomes the end card): rectangle x 1476–1840, y 924–1040 (364 × 116), 1.5 px border, split by a vertical rule at x 1580. Left cell: the logo mark (64 px). Right cell, left-aligned at x 1600, three lines: `VERNE WOODWORKS` (Fraunces 600, 24 px, tracking 0.12em, baseline y 960) / `DWG VW-0226 · DINING TABLE` (Plex Mono 500, 18 px, baseline y 992) / `SCALE 1:24 · SHEET 01/01` (Plex Mono 500, 18 px, baseline y 1020). Decorative small print like the zone markers; nothing essential is carried here.

### Logo (build in SVG)
**Mark:** a square 64 × 64 with 1.5 px stroke; inside, a single filled **dovetail** tail (trapezoid, wide side on top: top edge 36 px, bottom edge 24 px, height 30 px, top edge at y 12, horizontally centered) — it reads as a stout “V” and as a joint at once. A 1 px horizontal line crosses the full square at y 44 (the joint line). Fill: walnut `#5A3825` on paper, Chalk on blueprint; stroke follows the line color. No extra text in the mark.
**Wordmark:** `VERNE WOODWORKS` in Fraunces 600 caps, tracking 0.12em. Lockup: mark left, wordmark right, 24 px gap, baselines aligned to the mark’s bottom.

### Textures
- Blueprint: SVG `feTurbulence` (baseFrequency 0.9, numOctaves 2, seed 7) grain at 6 % over everything + a low-frequency mottling layer (baseFrequency 0.004, seed 3) at 5 % to imitate diazo paper + radial vignette to `#12263D` at the corners (35 %).
- Paper: same fine grain at 5 %, a very soft warm vignette (`#E4D8C2` corners, 30 %).
- Wood: generated procedurally (see §7) — flat-sawn cathedral grain for the top, straight grain for legs and apron, fine pore specks, then a soft top-light gradient and a 1 px highlight on the top edge.
- Drawn lines get a very slight chalk irregularity on blueprint: `feDisplacementMap` scale 0.8 on the line layer (optional; skip if it costs render time).

---

## 4. Final copy (exact strings — use verbatim)

**On-screen headlines & sublines**
1. Kicker (0.2 s): `SHOP DRAWING — DINING ROOM, PARK SLOPE`
2. H1 (hook): `Before the wood,` / `the *drawing.*` (two lines; “drawing.” in italic)
3. Kicker (beat 2): `01 — MEASURED IN YOUR HOME`
4. H1: `Designed for` / `*your* room.` (“your” italic)
5. Kicker (beat 3): `02 — BUILT IN BROOKLYN`
6. H1: `Solid walnut.` / `Solid *oak.*` (“oak.” italic)
7. Subline: `No veneer. Joined by hand, one piece at a time.`
8. Kicker (beat 4): `03 — MADE TO BE HANDED DOWN`
9. H1: `Built to last` / `100 years.` (“100” Fraunces 600, red pencil `#C24A2C`)

**Drawing annotations (mono, uppercase except units)**
- Room plan dims: `15′-2″` (room length, top), `12′-6″` (room depth, left)
- Room labels: `WINDOW`, `DOOR`, `RADIATOR`
- Table dims: `96″` (length), `42″` (width)
- Clearances: `43″` (each end), `54″` (each side) — with label `CLEARANCE` once, next to the first `54″`
- Plan label under table: `DINING TABLE — SEATS 8`
- Elevation dims: `96″` (overall), `30″` (height), `1¾″` (top thickness)
- Elevation label: `FRONT ELEVATION`
- Detail bubble: `A` in a 44 px circle; detail caption: `DETAIL A — DRAWBORED MORTISE & TENON`
- Material callouts (appear on the finished table, beat 3): `TOP: BLACK WALNUT, 8/4` · `BASE: WHITE OAK` · `FINISH: HAND-RUBBED OIL`
- Year ruler labels (beat 4): `2026`, `2051`, `2076`, `2101`, `2126`

Math check (keep it consistent): room 182″ × 150″; table 96″ × 42″ centered → ends (182 − 96)/2 = 43″, sides (150 − 42)/2 = 54″.

**End card**
- Wordmark: `VERNE WOODWORKS`
- Descriptor: `Bespoke furniture · Brooklyn, NY`
- CTA: `Request a quote`
- URL: `vernewoodworks.com`
- Title-block cells (small mono, 20 px): `DRAWN BY: VERNE WOODWORKS` · `FOR: YOUR ROOM` · `SHEET 01/01`

Typography: curly apostrophes if any appear (none currently), real primes ′ ″, middot `·` with spaces, em dash `—` with spaces in kickers, `&` in the detail caption.

---

## 5. Layout grid

- Canvas 1920 × 1080, sheet frame inset 40 px.
- **Text column (left):** x 120 → 820. Kicker baseline y 300; H1 first line top at y 330; subline 40 px below H1. Headlines are always left-aligned, never centered (until the end card).
- **Drawing field (right):** x 900 → 1800, y 120 → 900. The title block occupies bottom-right (see §3).
- Plan view at scale **4 px per inch**: room 728 × 600 px, placed with top-left at (1000, 200) → room spans x 1000–1728, y 200–800. Table rectangle 384 × 168 centered at (1364, 500).
  - Window: on the top wall, 72″ wide (288 px) centered at x 1364. Door: on the right wall near the bottom, 36″ (144 px) opening y 640–784, quarter-circle swing into the room. Radiator: a 1-px rectangle 160 × 24 against the left wall at y 420–580 → rotated: 24 wide × 160 tall, at x 1004–1028.
  - Chairs: 8 chairs as rounded rects 72 × 64 px (18″ × 16″), dashed (hidden line style), 3 per long side + 1 per end, 12 px off the table.
- Elevation (beat 2B onward) at scale **8 px per inch**: table 768 × 240 px, floor line at y 780, table top from y 540 to y 554 (1¾″ = 14 px), apron 4″ (32 px, y 554–586) inset 3″ from each end, legs 3½″ (28 px) wide from y 554 to the floor y 780, outer faces inset 3″ (24 px) from each end of the top. Horizontal center x 1364, table spans x 980–1748. Note: 540→780 is exactly 30″ at 8 px/in.

---

## 6. Storyboard (21.0 s)

All times in seconds. “Camera” = a transform on the whole drawing group `#sheet` (not the text column, not the frame/title block).

### Beat 0 — Hook: the room is drawn (0.00 – 3.20)
- **0.00:** Blueprint sheet already on screen (Prussian + grid + frame + title block fully visible, NOT animated in — so frame 0 is a composed image). The first line is already mid-draw at frame 0: the top wall of the room is ~20 % drawn.
- **0.00–1.40:** Walls draw clockwise with DrawSVG (top wall → right → bottom → left), `power2.inOut`, total 1.4 s; wall hatch fills fade in behind each wall 0.2 s after its line completes. Window and door cut-outs draw at 1.0–1.6 s; door swing arc draws 1.4–1.9 s.
- **0.20–0.70:** Kicker `SHOP DRAWING — DINING ROOM, PARK SLOPE` types in via ScrambleText (chars “▮/0123456789”), 0.5 s.
- **0.30–1.00:** H1 “Before the wood, / the drawing.” — each line slides up 100 % from a clipping mask, `expo.out`, 0.7 s, stagger 0.12 s.
- **1.20–2.20:** Room dimension `15′-2″` above the room: extension lines grow (0.25 s), the dimension line draws from center outward (0.4 s), ticks pop (scale 0→1, `back.out(3)`), number scrambles in from `00′-0″` to `15′-2″` (0.5 s). `12′-6″` on the left side follows 0.25 s later (text rotated −90°).
- **1.80–2.60:** Room labels `WINDOW`, `DOOR`, `RADIATOR` fade/slide 8 px, stagger 0.1; radiator rectangle draws.
- **2.20–3.00:** Table outline draws inside the room (rect path, 0.6 s), chairs appear as dashed outlines, stagger 0.05 s; label `DINING TABLE — SEATS 8` under the table.
- Alive: whole `#sheet` slowly scales 1.00 → 1.02 over 0–3.2 s (linear drift).

### Transition 1 (3.20 – 3.70): push-in
- H1 + kicker exit: lines slide up out of their masks, `power2.in`, 0.35 s, stagger 0.05.
- Camera pushes in toward the table: `#sheet` scale 1.02 → 1.55, transform-origin at the table center (1364, 500), and translate so that the table center lands at (1364, 470). `power3.inOut`, 3.2 → 4.2 s. Room walls stay visible at the edges (cropped by the frame — the frame and title block do NOT scale).

### Beat 1 — Designed for your room (3.60 – 6.60)
- **3.60–4.30:** Kicker `01 — MEASURED IN YOUR HOME` + H1 “Designed for / your room.” mask-up as before.
- **4.00–5.40:** Clearance dimensions draw one by one, stagger 0.3 s: left end `43″`, right end `43″`, top side `54″` with `CLEARANCE` label, bottom side `54″`. Each: arrow/dimension line from table edge to wall (0.35 s, `power2.out`), then the number fades up 6 px.
- **4.80–5.60:** Table own dims `96″` (above the table) and `42″` (right of table) draw. The `96″` dimension line and number are highlighted in **red pencil** `#C24A2C` (the only red on the blueprint) — it is “the” number that fits the room.
- **5.60–6.60:** hold. Alive: a small crosshair cursor (two 1 px lines 40 px long + 10 px circle, Chalk) glides from the table corner to the `54″` label and “taps” (circle scale 1 → 1.4 → 1, opacity 1 → 0).

### Transition 2 (6.60 – 7.40): plan folds into elevation (match cut on the table top)
- H1 + kicker exit up (0.35 s).
- Everything in plan except the table rectangle fades out and drifts 20 px outward (0.4 s).
- Camera eases back to scale 1.00 (0.8 s, `power3.inOut`).
- The table rectangle (plan, 384 × 168 at 4 px/in) morphs into the elevation top slab (768 × 14 at 8 px/in, y 540–554): animate width, height and y (or MorphSVG between the two rect paths) 6.8 → 7.4 s, `power3.inOut`. It reads as the table “turning to face us”.
- 7.10–7.60: floor line draws across (x 940–1788, y 780), 0.5 s. Legs and apron draw down from the top slab (DrawSVG, 0.45 s, stagger 0.06).

### Beat 1B — Elevation & joinery (7.40 – 8.40)
- 7.40–7.90: elevation dims: `96″` overall above the top (y 500), `30″` height on the right of the table (x 1780, vertical), `1¾″` small dim at the top-left edge with a leader. Label `FRONT ELEVATION` under the floor line (centered x 1364, y 820).
- 7.70–8.30: Detail bubble: a 150 px-diameter dashed circle around the front-left leg/apron joint (center 1018, 570); a leader line to a detail circle (radius 110, 1.25 px stroke) centered at (1110, 330) in the upper-left of the drawing field, showing an enlarged mortise & tenon: tenon rectangle entering the leg, hidden-line mortise, a small circle for the drawbore peg. Bubble `A` + caption `DETAIL A — DRAWBORED MORTISE & TENON` in mono 22 px under the circle.
- No headline in this 1 s window — the drawing is the hero. (Detail holds through 9.2 s so the caption gets ≥ 1.5 s.)

### Transition 3 (8.40 – 9.30): the plane pass — blueprint becomes wood
- A **shaving wipe** crosses the canvas left → right, 8.40 → 9.30, `power2.inOut`:
  - Leading edge: a vertical band 90 px wide of Oak `#C79A62` with procedural straight grain, its right edge curling (an SVG path with a soft convex bulge and a 12 px lighter highlight `#DDB783`), slightly tilted 4°.
  - Behind the band: the sheet background is Paper `#F1EADC` (with paper grid); all lines are Ink; frame, zone markers and title block switch to Ink; logo mark fill switches to walnut.
  - Implementation: two full copies of the drawing (blueprint styling / paper styling) with the paper copy revealed by an animated `clip-path: inset(0 X 0 0)` synced to the band’s x.
- On the paper side, the table elevation is **filled with wood**: top slab and apron in walnut grain, legs in white oak grain (lighter: `#C79A62`→`#A97C48` ramp). Ink outlines remain on top at 60 % opacity, then fade to 25 % by 10.0 s — the drawing stays as a ghost of the object.
- Detail A circle and caption fade out on the paper side (they are not copied onto the paper version).
- Soft contact shadow under the table (ellipse, Ink 18 % blur 18 px) fades in 9.2–9.8 s.

### Beat 2 — Solid walnut. Solid oak. (9.00 – 12.60)
- 9.00–9.70: Kicker `02 — BUILT IN BROOKLYN` + H1 “Solid walnut. / Solid oak.” mask-up (Ink on paper).
- 9.60–10.10: Subline `No veneer. Joined by hand, one piece at a time.` fades up 10 px, 0.5 s.
- 10.00–11.00: Material callouts appear, leader lines drawing from the object (mono 22 px, Ink, stagger 0.25 s):
  The elevation dims `96″`, `30″`, `1¾″` and `FRONT ELEVATION` fade out 9.6–9.9 s to make room. Leaders are 1 px Ink, a 5 px dot on the object end, an elbow, then the label.
  - `TOP: BLACK WALNUT, 8/4` → dot on the top slab at (1560, 547), leader up to an elbow at (1560, 470), label left-aligned from x 1575, baseline y 478.
  - `FINISH: HAND-RUBBED OIL` → dot on the top slab at (1180, 547), leader up to (1180, 420), label left-aligned from x 1195, baseline y 428.
  - `BASE: WHITE OAK` → dot on the left leg at (1006, 700), leader straight down to (1006, 850), label left-aligned from x 1021, baseline y 858.
- Alive: a slow light sweep across the wood (a linear-gradient highlight band, white at 10 %, moving left → right over 9.5–12.5 s) — reads as oil sheen.

### Transition 4 (12.60 – 13.10): pull back + ruler
- H1, subline, kicker exit up (0.35 s). Material callouts fade (0.3 s).
- Table group scales 1.00 → 0.86 and moves up 30 px (`power3.inOut`, 0.5 s) to make room for the ruler.
- A **carpenter’s rule** slides in from the right along y 900–960 (height 60 px, x 120 → 1440, so it stops left of the title block): body Oak `#C79A62` with fine grain, Ink tick marks (every 8 px minor 12 px tall, every 40 px mid 20 px, every 200 px major 32 px) and brass end cap (`#B08A4E`, 16 px). `expo.out`, 0.5 s.

### Beat 3 — Built to last 100 years. (13.00 – 16.40)
- 13.00–13.70: Kicker `03 — MADE TO BE HANDED DOWN` + H1 “Built to last / 100 years.” mask-up; “100” is Fraunces 600 in red pencil.
- 13.20–15.60: The rule scrolls horizontally (its tick pattern translates left, `power2.inOut`) while year labels pass a fixed red-pencil index mark (a 2 px vertical red line, 76 px tall, at x 1000): `2026` at start, then `2051`, `2076`, `2101`, and it lands on `2126` exactly at the index at 15.60. Year labels: mono 26 px Ink, sitting on the rule above its major ticks.
- Simultaneously 13.20–15.60 (subtle, not gimmicky): the walnut grain deepens with patina — overlay a warm multiply layer `#7A4A26` from 0 % → 14 % opacity; the oak legs go slightly amber. The object ages; it doesn’t wear out.
- 15.60–16.40: hold. Index mark on `2126` ticks once (scale Y 1 → 1.15 → 1, 0.3 s).

### Transition 5 (16.40 – 17.20): the title block becomes the end card
- Headline, kicker, rule, table fade out and move up 12 px (0.35 s, `power2.in`), 16.40–16.75.
- The corner **title block** (x 1476–1840, y 924–1040) scales/morphs into the end-card block: final rect x 360–1560, y 250–830 (1200 × 580), `power3.inOut`, 16.50 → 17.20. Animate the rectangle geometry (x, y, width, height) — not a CSS scale on the text — so the 1.5 px stroke stays crisp. Its internal vertical divider (x 1580) animates to x 760 and becomes the first cell rule; the y 710 rule and the x 1160 rule draw in 17.10–17.40.
- Sheet frame and grid stay (paper version).

### Beat 4 — End card (17.20 – 21.00) — calm, held ≥ 3.5 s
End-card block (1200 × 580, 1.5 px Ink border), internal structure:
- **Top zone** (y 250–710):
  - Logo mark 120 × 120, top-left at (440, 350).
  - Wordmark `VERNE WOODWORKS` Fraunces 600, 64 px, tracking 0.12em, x 600, baseline y 420.
  - Descriptor `Bespoke furniture · Brooklyn, NY` Fraunces 400, 38 px, x 600, baseline y 480.
  - 1 px Ink rule at y 530, x 600 → 1480.
  - `Request a quote` Fraunces 400-italic, 56 px, x 600, baseline y 620.
  - `vernewoodworks.com` Plex Mono 500, 40 px, right-aligned to x 1480, baseline y 620, with a **red pencil underline** (2.5 px, `#C24A2C`, a hand-drawn path with 1–2 px wobble, y ≈ 636) drawn left → right.
- **Cell row** (y 710–830, separated from the top zone by a 1.5 px rule at y 710): three cells split by 1.5 px vertical rules at x 760 and x 1160; labels Plex Mono 500, 20 px, tracking 0.08em, left-aligned 24 px inside each cell, vertically centered (baseline ≈ y 777): `DRAWN BY: VERNE WOODWORKS` · `FOR: YOUR ROOM` · `SHEET 01/01`.
- Timing: 17.20–17.80 logo mark draws (square stroke DrawSVG 0.4 s, dovetail fills 17.50); wordmark letters rise from mask, stagger 0.025 s, 17.35–17.95; descriptor 17.70; rule draws 17.90–18.30; CTA + URL mask-up 18.10–18.60; red underline draws 18.60–19.10; bottom cells fade 18.30–18.70.
- 19.10–21.00: hold. Alive: the whole sheet drifts scale 1.00 → 1.015 (linear), grain static.
- Last frame is calm and complete (works as poster and as a loop point for the website hero).

---

## 7. Motion notes

- Personality: **draftsman’s hand** — lines are drawn, never faded; text slides from masks; nothing bounces except dimension ticks (tiny `back.out(3)`).
- Eases: entrances `expo.out` / `power3.out`; exits `power2.in`; camera moves `power3.inOut`; line drawing `power2.inOut` (feels like a pen accelerating and settling). Continuous drifts linear.
- Rhythm: build (0–3) → precise (3–8) → the one fast moment: the plane wipe (0.9 s) → slow (9–16) → calm end card (17–21).
- Staggers 0.05–0.12 s. Never more than 3 things starting at the same instant.
- Reading holds satisfied: H1 hook 2.6 s, “Designed for your room.” 2.7 s, “Solid walnut. Solid oak.” + subline 3.0 s, “Built to last 100 years.” 2.7 s, end card: CTA readable from 18.6 s, held 2.4 s after the last element lands, and the wordmark 3 s+.
- Nothing flashes, no camera shake, no 3D spin.

---

## 8. Technical approach hints

- **Stack:** one `index.html`, inline SVG for the whole drawing (viewBox 0 0 1920 1080), GSAP (`gsap.min.js`, `DrawSVGPlugin`, `MorphSVGPlugin`, `ScrambleTextPlugin`, `SplitText` optional) with a single `gsap.timeline({paused:true})`; `render: t => { tl.seek(t, false); }`. Duration 21.
- **Two sheet layers:** `#blue` (blueprint styles) and `#paper` (paper styles) share the same drawing markup — easiest is to build the drawing in JS once and clone it, then set `--line` color per layer via CSS custom properties (`stroke: var(--line)`). The paper layer is revealed with `clip-path: inset(0 calc(100% - Xpx) 0 0)` animated from X = 0 to 1920 between 8.40 and 9.30; the oak shaving band’s `x` is tied to the same X (use one tween on a proxy object with `onUpdate`, which is deterministic under `seek`).
- **Wood textures:** generate once at load on offscreen canvases with `simplex-noise` seeded through `KK.rng(226)`:
  - Walnut top (768 × 14 at 2× = 1536 × 28 → too thin to show cathedrals; render a 1536 × 512 texture and use the region; the apron (768 × 32) and top both sample it). Grain function: `v = sin((y*0.12 + noise2D(x*0.0015, y*0.02)*6 + noise2D(x*0.01, y*0.1)*0.6) * π)`; map `v` through a 3-stop ramp `#3A2418 → #5A3825 → #7A5236`; add pores: 0.6 % of pixels darkened by 25 %, elongated 1 × 4 px along grain.
  - Oak legs: straight vertical grain with occasional ray-fleck (short lighter flecks 2 × 8 px at 8 % opacity).
  - Export via `canvas.toDataURL()` and use as SVG `<pattern>`/`<image>` clipped to the table parts. Resolve `KLIPT.ready` after textures and `document.fonts.ready`.
- **Primes and fractions:** `15′-2″`, `1¾″` — ensure IBM Plex Mono renders ′ ″ ¾ (it does); if a glyph falls back, use Fraunces for that glyph only.
- **Grain/vignette** as a static top SVG overlay with `feTurbulence` (render it once; static is fine and keeps render fast).
- **Title block → end card:** keep the block as an SVG `<rect>` + divider `<line>`s whose attributes GSAP animates (`attr:{x,y,width,height}`), with the small title-block text fading out 16.40–16.60 and end-card text living in its own group.
- Keep all text as live SVG `<text>` or HTML over the SVG — either is fine; HTML for the left column headlines (easy masks with `overflow:hidden` wrappers), SVG for annotations.
- No three.js needed. Target < 1.5 s per preview frame.

## 9. meta.json hints
- title: “Before the wood, the drawing”
- techniques: `["gsap", "svg-illustration", "drawsvg", "morphsvg", "canvas-procedural-texture", "clip-path-wipe", "kinetic-type"]`
- fonts: `["Fraunces", "IBM Plex Mono"]`
- palette: `["#1B3553", "#EDE6D6", "#F1EADC", "#221C17", "#5A3825", "#C79A62", "#C24A2C"]`
- copy_language: `"en"`

# p232 · DataPulse · "The curve flips"
Video · 1920×1080 (16:9) · **24.0 s** · 30 fps · LinkedIn feed + landing page hero · sound-off, so every idea is carried by on-screen text.

> Language note: the orchestrator template asks for "French copy", but the brief (`lang: "en"`) and the task both say **English**. All copy below is final **US English**. Do not translate it.

---

## 1. Audience insight and the one message

**Who scrolls past this:** product managers, customer success leaders and SaaS CEOs on LinkedIn, between meetings. They have all lived the same moment: a "healthy" account sends a cancellation email, and the post-mortem shows the warning signs were in the data for weeks. What they fear is not churn itself. It is **finding out too late to do anything about it.**

**Insight:** every churn chart is read backwards. You only see the drop once it has happened.
**The one message:** *DataPulse shows you the drop 30 days before it happens, early enough to turn it around.*
Proof: **+21% net revenue retention on average.** CTA: **Book a demo at datapulse.io.**

Register: B2B SaaS, expert and trustworthy, with a little quiet drama. It should feel like a real product screen telling a real story, not a motion-graphics template.

---

## 2. Concept: "Rewind 30 days"

One believable account-health chart tells a four-act story in a single continuous shot:
1. **The line draws itself** and slides downhill: a customer is quietly leaving.
2. It **crashes into "Canceled"**, where most teams find out.
3. The playhead **rewinds 30 days** and DataPulse drops a flag at the exact moment the risk started.
4. The team steps in, and **the curve flips upward** into a renewal. Then we zoom out: it isn't one account, it's the whole portfolio, and the result is +21% NRR.

Why it fits: DataPulse is an analytics product, so the product *is* the story. The "rewind" shows "30 days before" as a visible gesture instead of a claim. The same chart and the same account run through the whole film, so the viewer never has to re-orient.

---

## 3. Art direction

### Palette (strict, 7 tokens)
| Token | Hex | Use |
|---|---|---|
| `--ink` | `#0A0E14` | Page background (dominant) |
| `--panel` | `#121821` | Dashboard panel, cards |
| `--line` | `#1F2733` | Panel borders, dividers, chart grid (grid at 70% opacity) |
| `--text` | `#EEF2F6` | Primary text, the healthy/neutral chart line |
| `--muted` | `#7D8898` | Secondary text, axis labels, ghost elements |
| `--ember` | `#FF5B3A` | Risk / churn ONLY (line below threshold, cancel marker, −MRR) |
| `--pulse` | `#5CF2A8` | Brand + DataPulse flag + recovery line + "+21%" (the accent, used sparingly) |

Mint and ember never share an element: ember means "problem", mint means "DataPulse / solved". No gradients except the ambient glow described below. No purple, no blue gradient.

### Typography (2 families)
- **Manrope** (`@fontsource/manrope` 500, 700, 800) for headlines and UI text.
- **JetBrains Mono** (`@fontsource/jetbrains-mono` 400, 500, 700) for every number, date, axis label and metric.

Scale (1920-wide canvas):
| Role | Font | Size / line-height / tracking |
|---|---|---|
| Headline (left column) | Manrope 800 | 76 px / 1.02 / −0.025em, `--text` |
| Headline accent line | Manrope 800 | 76 px, `--pulse` or `--ember` as specified |
| Sub-line | Manrope 500 | 34 px / 1.25, `--muted` |
| Eyebrow | JetBrains Mono 500 | 20 px, uppercase, +0.12em tracking, `--muted` |
| Big proof number | Manrope 800 | 300 px / 0.9 / −0.04em, `--pulse`, `font-variant-numeric: tabular-nums` |
| UI title (panel) | Manrope 700 | 26 px |
| UI body / card text | Manrope 500 | 22 px |
| Data labels, chips, axis | JetBrains Mono 400/500 | 20–24 px (axis 20, chips 22, key values 26–32) |
| End-card headline | Manrope 800 | 88 px / 1.02 / −0.03em |

### Layout grid (constant through beats A–D)
- Outer margin 120 px left/right, 96 px top/bottom.
- **Copy column:** x 120 → 600 (width 480), headlines top-aligned at y 300, with 20 px between the two H1 sentences. Eyebrow at y 250.
- **Dashboard panel:** x 680 → 1800 (1120 × 800), y 140 → 940, radius 20, fill `--panel`, 1 px border `--line`, shadow `0 40px 120px rgba(0,0,0,.55)`.
  - Top bar (height 64, bottom border `--line`): DataPulse symbol (28 px) + "DataPulse" Manrope 700 22 px; breadcrumb in `--muted` 20 px: `Accounts / Halcyon Freight`; right-aligned date-range chip mono 20 px: `Jul 14 – Oct 12, 2026`.
  - Account header row (y +96 inside panel, padding 40): name `Halcyon Freight` Manrope 700 34 px; beside it mono chips `$4,200 MRR` and `Plan · Growth` (chip: 1 px `--line` border, radius 8, padding 6×12, `--muted` text).
  - Tabs under it: `Health` (active, `--text`, 2 px mint underline) · `Usage` · `Revenue` (`--muted`), Manrope 600 22 px.
  - **Chart area:** inner box x 760 → 1740, y 400 → 860 (980 × 460). Chart title above it, left: `Account health score` Manrope 700 26 px; right: legend dot + `Health (0–100)` mono 20 px `--muted`.

### Chart spec (so both devs draw the same curve)
- X: day index 0 → 90 (day 0 = **Jul 14, 2026**; day 50 = **Sep 2**; day 80 = **Oct 2**; day 90 = **Oct 12**). Linear scale to the 980 px width.
- Y: 0 → 100 linear, gridlines at 0/25/50/75/100 (1 px `--line`), labels mono 20 px `--muted` on the left outside the box.
- X ticks (mono 20 px `--muted`): `Aug 1` (day 18), `Sep 1` (day 49), `Oct 1` (day 79).
- **Risk threshold:** horizontal dashed line at y = 65 (dash 6/8, `--muted` at 60%), right-end label mono 20 px `Risk threshold · 65`.
- Curve: `d3.line().curve(d3.curveMonotoneX)`, stroke width 4, round caps.
  - **Churn path** (days 0 → 80): `[0,81] [7,83] [14,80] [21,82] [28,79] [35,74] [42,69] [50,64] [57,55] [64,44] [71,33] [80,18]`, then a flat stub `[80,18] → [90,18]` drawn later in `--muted` dashed.
  - **Recovery path** (days 50 → 90): `[50,64] [54,60] [60,66] [66,74] [73,82] [80,88] [90,90]`.
- Color rule: draw the churn path twice, clipped by a rect at y(65). Above the threshold stroke = `--text`, below it stroke = `--ember`. The line turns red as it crosses the threshold.
- Area fill under the drawn line: vertical gradient of the stroke color from 14% to 0% opacity (matching clip).
- **Playhead:** 1 px vertical line `--text` at 35% opacity following the leading tip, with a 12 px dot at the tip (fill = current stroke color, 6 px outer glow of the same color at 40%). Above the chart at the playhead x: a mono 22 px date chip (`--panel` fill, `--line` border) showing the current date (`Jul 14` … `Oct 2`), computed from day index.

### Graphic language and texture
- Real product UI: hairline borders, 8/12/20 px radii, tabular mono numbers, believable names and dates. No glassmorphism, no emoji, no stock "dashboard noise" (no fake pie charts).
- **Grain:** full-frame SVG `feTurbulence` (baseFrequency 0.8, numOctaves 2, seeded) at 5% opacity, `mix-blend-mode: overlay`, static.
- **Ambient glow:** one soft radial light behind the panel (ellipse 1200×800 at 70%/45%, `#5CF2A8` at 5%), which shifts to `#FF5B3A` at 6% during beat B and back to mint from beat C on. This is the only colored gradient.
- Icons: Lucide, stroke 2, inlined: `triangle-alert`, `log-in`, `user`, `activity`, `calendar-check`, `mouse-pointer-2` (cursor, filled `--text`, 1.5 px `--ink` outline).

### Logo: DataPulse
- **Symbol:** 48×48 rounded square (rx 12) filled `--pulse`; inside, a heartbeat that ends by turning up, stroked `--ink`, width 4, round joins/caps: polyline `8,28 17,28 21,18 27,34 31,24 40,14` (flat, spike, dip, then a rising tail, which mirrors the story). Small 5 px dot at `40,14`, filled `--ink`.
- **Wordmark:** "DataPulse" Manrope 800, −0.02em, `--text`, set to the right of the symbol with a gap of 0.35× symbol height; cap height ≈ 0.5× symbol.
- Used in the panel top bar from frame 0 (brand present throughout), and large on the end card (symbol 96 px, wordmark 64 px).

---

## 4. Final copy (exact strings, US English)

Curly apostrophes (’) are required. Use a real minus sign (−, U+2212) in `−$4,200`. En dash (–) in date ranges. Numbers are tabular.

**Beat A: hook**
- Eyebrow: `ACCOUNT HEALTH · LIVE`
- H1 line 1: `This customer is about to leave.`
- H1 line 2 (`--muted`, Manrope 800 76 px): `They haven’t told you yet.`

**Beat B: too late**
- Eyebrow: `ACCOUNT HEALTH · OCT 2`
- H1: `Most teams find out here.`
- Sub (34 px `--ember`, Manrope 700): `On cancellation day.`
- Chart marker label (mono 22 px `--ember`): `Oct 2 · Canceled`
- Chip next to marker (ember 12% bg, ember text, mono 24 px 700): `−$4,200 MRR`

**Beat C: rewind**
- Eyebrow: `REWIND · 30 DAYS`
- H1 line 1: `DataPulse sees it here.`
- H1 line 2 (`--pulse`): `30 days earlier.`
- Flag pin label (mono 20 px `--pulse`): `Sep 2 · Flagged`
- **Alert card** (anchored to the flag, 440 px wide, `--panel`, 1 px mint 40% border, radius 12, padding 24):
  - Header row: icon `triangle-alert` (ember, 22 px) + `At risk · churn likely within 30 days` (Manrope 700 22 px `--text`)
  - Signal 1: icon `log-in` + `Logins` ........ `−38% in 14 days` (label Manrope 500 20 px `--muted`, value mono 500 22 px `--text`, right-aligned)
  - Signal 2: icon `user` + `Admin seat` ........ `removed`
  - Signal 3: icon `activity` + `Data exports` ........ `3× normal`
  - Button (full width, height 48, radius 10, fill `--pulse`, text `--ink` Manrope 700 22 px): `Start save play`

**Beat D: the flip**
- Eyebrow: `SAVE PLAY · ACTIVE`
- H1 line 1: `Your team steps in.`
- H1 line 2 (`--pulse`): `The curve flips.`
- Confirmation card (replaces the alert card content): icon `calendar-check` (mint) + `Check-in booked` (Manrope 700 22 px); line 2 Manrope 500 20 px `--muted`: `Maya Chen, Customer Success`; line 3 mono 22 px `--text`: `Fri, Sep 4 · 10:00 AM`
- End-of-recovery label (mono 22 px `--pulse`): `Oct 2 · Renewed · +2 seats`

**Beat E: proof**
- Eyebrow: `ALL ACCOUNTS · PORTFOLIO VIEW`
- Big number: `+21%`
- Label under the number (Manrope 700 40 px `--text`, 2 lines): `net revenue retention,` / `on average.`
- Footnote (mono 20 px `--muted`): `Average across DataPulse customers.`
- Portfolio panel title (Manrope 700 26 px): `Accounts at risk · last 90 days`. Right chip mono 20 px: `7 flagged · 7 saved`
- 12 account tiles (name Manrope 600 20 px, MRR mono 18 px `--muted`), row by row:
  1. `Halcyon Freight` · `$4,200`
  2. `Brightloop` · `$2,850`
  3. `Norda Health` · `$6,100`
  4. `Kestrel Pay` · `$3,400`
  5. `Oakline HR` · `$1,950`
  6. `Fieldnote` · `$2,300`
  7. `Tandem Labs` · `$5,750`
  8. `Vireo Cloud` · `$3,900`
  9. `Summit Ledger` · `$2,600`
  10. `Quarry AI` · `$7,200`
  11. `Palette Studio` · `$1,400`
  12. `Monarch Ops` · `$4,650`
  - Flagged and saved (flip to mint): Halcyon Freight, Brightloop, Kestrel Pay, Fieldnote, Vireo Cloud, Quarry AI, Monarch Ops (7). The others stay neutral `--text` and steady.
  - Tag on each flipped tile (mono 16 px, mint 14% bg, mint text, radius 6): `Saved`

**End card**
- Logo (large).
- Headline: `See churn coming` / `30 days before it happens.` (line 2 `30 days` in `--pulse`, rest `--text`)
- CTA button (pill, height 72, padding 0 36, fill `--pulse`, text `--ink` Manrope 700 28 px): `Book a demo  →` (arrow = Lucide `arrow-right`, 26 px)
- URL (mono 500 28 px `--text`, next to the button, 32 px gap): `datapulse.io`

Proofreading checklist: "haven’t" uses a curly apostrophe. The status label uses the US spelling `Canceled`. Use no other text anywhere.

---

## 5. Storyboard (24.0 s)

Easing defaults: entrances `expo.out` 0.7 s, exits `power2.in` 0.35 s, moves `power3.inOut`. Headline lines enter by **mask-rise**: each line sits in an `overflow:hidden` wrapper and translates from `y:110%` to `0`, 0.7 s `expo.out`, lines staggered 0.08 s. Headline exits: lines translate to `y:−110%`, 0.35 s `power2.in`, stagger 0.04. Eyebrows use ScrambleText (chars `0123456789ABCDEF·`, 0.5 s).

### Beat A: Hook (0.00 – 4.20)
- **Frame 0 is not empty:** the panel is already fully visible (no intro), with grid, axes and the first 3 px of the line. The line starts drawing at t = 0.
- 0.00–4.20: the churn path draws from day 0 to day **50** (`power1.inOut`), playhead and date chip following (`Jul 14` → `Sep 2`). At about 3.6 s the tip reaches the threshold at day 50 without crossing yet.
- 0.10: eyebrow scrambles in.
- 0.15: H1 line 1 mask-rises. 1.30: line 2 (`--muted`) mask-rises.
- Keep alive: panel scale drifts 1.00 → 1.015 (linear) across beats A–D. Transform-origin is the panel center.

### Beat B: Too late (4.20 – 8.20)
- 4.20: headline A exits. 4.40: new eyebrow + `Most teams find out here.` mask-rise.
- 4.20–6.00: line continues day 50 → 80 (`power2.in`, so it accelerates into the crash). Below 65 the stroke is ember (clip rule). The ambient glow cross-fades to ember over 1.2 s.
- 6.00: impact at `[80,18]`. Ember dot scales 0 → 1 (`back.out(3)`, 0.35 s) plus two ring pulses (radius 12 → 56, opacity .6 → 0, 0.8 s, 0.25 s apart). Panel does a **2 px vertical nudge** (y 0 → 2 → 0, 0.18 s). Marker label `Oct 2 · Canceled` and chip `−$4,200 MRR` pop in above the dot (y +12 → 0, 0.45 s `expo.out`, 0.08 s stagger).
- 6.20: flat dashed stub day 80 → 90 draws in `--muted` (0.6 s).
- 6.30: sub `On cancellation day.` mask-rises.
- 6.60–8.20: hold. The ember dot breathes (scale 1 → 1.15 → 1, 1.2 s sine).

### Beat C: Rewind (8.20 – 12.40), signature moment
- 8.20: headline B exits. Cancel marker, chip and stub fade to 0 (0.3 s).
- 8.30–9.20: **REWIND.** Playhead scrubs back from day 80 to day 50 (0.9 s `expo.inOut`). The drawn segment 50 → 80 does not vanish: it turns into a **ghost**, 2 px dashed (6/8) ember at 30% opacity. The date chip's text is driven per frame (`Oct 2` … `Sep 2`) so it visibly counts backward. Add horizontal "rewind" streaks during the scrub: 3 thin `--muted` lines (1 px, 120–260 px long) trailing right of the playhead at 25% opacity. Ambient glow cross-fades back to mint.
- 8.40: eyebrow `REWIND · 30 DAYS` scrambles in.
- 9.20: **flag drops** at `[50,64]`: mint vertical pin (2 px, 90 px tall) grows upward from the point (0.35 s `expo.out`), topped by a 14 px mint dot + ring pulse; label `Sep 2 · Flagged` appears at the pin top.
- 9.25: H1 `DataPulse sees it here.` mask-rises; 9.60: `30 days earlier.` (mint) mask-rises.
- 9.60: a 1 px mint bracket with end ticks spans from the flag x to the ghost cancel x at y = chart top − 24, labelled mono 20 px centered `30 days`. It draws left→right (0.6 s, DrawSVG).
- 9.90: alert card enters from the pin: anchored so its left edge sits 28 px right of the pin, top at pin top. It animates from scale 0.96 / opacity 0 / y +16 (0.6 s `expo.out`). Rows stagger 0.1 s (header, 3 signals, button). The card sits over the upper-right of the chart and must not cover the flag or the ghost line's end.
- 10.9–12.4: hold (≈ 7 words + card). The button has a subtle mint glow pulse (box-shadow 0 → 16 px at 35%, 1.2 s sine).

### Beat D: The flip (12.40 – 16.60)
- 12.40: headline C exits; 12.55: eyebrow `SAVE PLAY · ACTIVE`; 12.60: `Your team steps in.` mask-rises.
- 12.40–12.95: cursor enters from bottom-right of the panel and glides to the button (`power3.inOut`). 12.95: click: cursor scale 1 → 0.85 → 1 (0.18 s), button darkens 10% and a ripple circle expands from the click point.
- 13.15: card contents cross-swap (old rows slide up −12 px and fade 0.25 s; new rows rise +12 px 0.4 s `expo.out`, stagger 0.08) into the **confirmation card** (`Check-in booked` / `Maya Chen, Customer Success` / `Fri, Sep 4 · 10:00 AM`). Card border turns solid mint 60%. Cursor fades out 0.3 s.
- 13.70–15.90: **recovery path draws** days 50 → 90 in mint (2.2 s `power2.inOut`), with a mint area fill under it and the playhead/date chip following it again (`Sep 2` → `Oct 12`). It dips to 60 first (believable), then climbs above the threshold. The ember ghost stays visible underneath: the "fork" between two futures is the image of the film.
- 14.20: `The curve flips.` (mint) mask-rises.
- 15.20 (tip at day 80): mint dot + label `Oct 2 · Renewed · +2 seats` pops in (same animation as the cancel marker) directly above the recovery point, mirroring the ember one.
- 15.90–16.60: short hold.

### Beat E: Proof (16.60 – 20.60)
- 16.60–17.40: **zoom-out transition.** The whole panel scales 1.015 → 0.34 (`power3.inOut`) and moves to become **tile 1** (top-left) of a 4×3 grid inside a new, same-sized portfolio panel. The other 11 tiles fade/scale in around it (0.5 s, stagger 0.03 from tile 1 outward). Implementation: a FLIP-style tween of the panel to tile-1's rect, then cross-fade to the real tile-1 at 17.40 (the mini version shows the same chart simplified: ember ghost + mint recovery, no UI chrome).
- Headline D exits at 16.60. The left column switches to the proof layout.
- Portfolio panel: same rect as before (x 680–1800, y 140–940). Title row at top (`Accounts at risk · last 90 days` + chip `7 flagged · 7 saved`). Grid: 4 cols × 3 rows, gap 20, tiles ≈ 250 × 200, each with name, MRR, and a 90-day sparkline (2 px). Sparklines are generated from the seeded RNG (`KK.rng(232)`), neutral ones wobble between 70 and 90. Flagged ones start as a downward ember curve.
- 17.60–18.60: the 6 other flagged tiles **flip** in stagger (0.12 s, in reading order): their ember downturn redraws as a mint upturn from the flag point (0.5 s each). A `Saved` tag pops in at the top-right of each tile. The chip counter `7 flagged · 7 saved` has its "saved" digit count 1 → 7 in step.
- 17.40: eyebrow `ALL ACCOUNTS · PORTFOLIO VIEW` scrambles in. Big number block at x 120, y 330:
  - 17.50–18.90: `+21%` counts +0% → +21% (integer steps, `power2.out`), 300 px mint, with a mask-rise entrance.
  - 18.40: label `net revenue retention,` / `on average.` mask-rises (40 px, `--text`).
  - 18.80: footnote fades in (y +8 → 0).
- 18.90–20.60: hold; the portfolio panel keeps drifting (scale 1 → 1.012).

### End card (20.60 – 24.00)
- 20.60–21.10: **pulse-line wipe.** A 4 px mint heartbeat line (the logo's polyline shape stretched across the full width at y 540, amplitude 140 px) draws left→right across the frame (0.5 s `power2.inOut`). Behind its leading edge, an `--ink` panel wipes over everything (clip-path inset from the right). The line then collapses to the right into the logo symbol's position.
- 21.00: logo symbol scales 0.6 → 1 (`back.out(1.6)`, 0.5 s) at center-top (symbol 96 px; the lockup is centered at y 330). Wordmark `DataPulse` (64 px) mask-rises at 21.10.
- 21.25: headline (88 px, centered, 2 lines, lockup-to-headline gap 64 px) mask-rises, line stagger 0.08.
- 21.60: CTA row (centered, y ≈ 800): `Book a demo →` pill + `datapulse.io`, rise +16 → 0, 0.5 s `expo.out`. The arrow nudges right 6 px and back once at 22.4 (0.5 s).
- 21.9–24.00: **hold still** (≥ 2.1 s fully legible, 2.7 s from the headline). Keep alive only with a very faint mint ambient glow behind the logo breathing (5% → 7%), plus grain. No exit animation. The last frame is the full end card.

---

## 6. Motion notes
- Personality: **precise, analytic, one dramatic gesture** (the rewind). Snappy UI (`expo.out`), smooth data (`power1/2.inOut`), one impact (the cancel crash). Nothing bounces except the two marker dots and the logo (`back.out`).
- Rhythm: A steady, B accelerating into impact, C fast rewind then calm, D build, E quick zoom and counter, End calm. Fast–fast–slow.
- The chart line is the protagonist and the continuous thread: it is always moving or glowing, and never re-enters from scratch.
- Color storytelling is literal: neutral → ember (danger) → mint (DataPulse). Ember never appears after beat C except as the ghost line.
- Minimum holds are respected: every headline stays fully visible for ≥ 0.4 s/word + 0.8 s.
- Mark the ember/mint fork (ghost red line + mint recovery) as the **poster frame** candidate: t ≈ 16.2 s.

## 7. Technical approach hints
- Single `index.html`; GSAP (+ ScrambleTextPlugin, DrawSVGPlugin, CustomEase) and d3 (scales, `line`, `curveMonotoneX`, `area`) from `../../node_modules/`; `lib/klipt-kit.js` for `KK.rng`. One `gsap.timeline({paused:true})`; `KLIPT = {width:1920, height:1080, fps:30, duration:24, render: t => { tl.seek(t,false); }}`.
- Chart in one inline `<svg>` at 1:1 pixel coordinates. Build paths with d3 at load. **Progressive draw:** animate a proxy object `{day}` on the timeline, and in `onUpdate` set each path's `stroke-dasharray/offset` from a precomputed lookup `lengthAtDay[]` (sample `getPointAtLength` once at load into a 0.25-day table). Use the same table to position the playhead, tip dot and date chip, so everything stays locked together and deterministic.
- Threshold coloring: two copies of the churn path, each with a `clipPath` rect (above/below `y(65)`). The area fill uses the same clips.
- Date chip text: compute from the day index (`d3.timeDay.offset(Jul 14 2026, round(day))`, formatted `%b %-d`) inside `onUpdate`. No wall-clock time anywhere.
- Rewind ghost: at 8.30 swap the solid 50→80 segment for a separate pre-built dashed path (days 50→80). Only animate the playhead proxy backward.
- Zoom-out: tween the panel's `transform` (scale + translate) to tile 1's rect, then set `autoAlpha` swaps. Avoid `filter: blur` on large layers (software render).
- Grain: one static SVG `feTurbulence` layer. Glow: a CSS radial-gradient div with animated opacity (two stacked divs, mint and ember, cross-faded) rather than animated gradient colors.
- Fonts: load `manrope/500.css, 700.css, 800.css` and `jetbrains-mono/400.css, 500.css, 700.css`, and gate `KLIPT.ready` on `document.fonts.ready` so the first frame has final metrics. Use `font-variant-numeric: tabular-nums` on all counters so they don't jitter.
- Check frames at t = 0.5, 3.0, 6.3, 9.0, 11.0, 13.5, 16.2, 18.5, 23.0 for overlap of alert card vs. flag/ghost, clipped headlines (each H1 sentence wraps naturally to ≤ 2 lines in the 480 px column. Each wrapped visual line gets its own mask wrapper, so use SplitText `type:"lines"` and animate the lines. If any sentence needs 3 lines, reduce all headlines to 70 px, not just one), and end-card legibility.
- meta.json: title "The curve flips", techniques `["gsap","d3","svg-dataviz","ui-mockup","scrambletext","drawsvg"]`, fonts `["Manrope","JetBrains Mono"]`, palette = the 7 hex above, `copy_language: "en"`.

# k108 — Ledgerly · « Relances intelligentes »
Video · 1080 × 1350 (4:5) · 23.0 s · 30 fps · LinkedIn feed (sound-off) · Copy: French

---

## 1. Audience insight & the one message

**Who scrolls past this:** a PME boss (45–60), a DAF or a head of accounting, on LinkedIn between two meetings, sound off. They know *exactly* how many invoices are late this month. They hate chasing payments for two reasons that pull against each other: relancer trop tôt, on froisse un bon client ; relancer trop tard, la trésorerie trinque. So they postpone, and the DSO drifts.

**Insight:** the problem isn't *whether* to chase, it's **when and how** — and that differs for every client. Humans don't have time to know each client's rhythm; Ledgerly's AI does.

**The one message:** *Ledgerly relance chaque client au bon moment, avec le bon ton — et vous êtes payé 11 jours plus tôt.*

Register: B2B SaaS, trustworthy and expert, with one sharp editorial idea. Calm authority, not hype. Numbers are the heroes.

---

## 2. Concept — « Le bon moment. »

**The idea:** a ledger page becomes a timeline. We see three real-looking clients, each with its own payment rhythm drawn as dots on a 30-day ruled line. A thin green **playhead** (the AI) scans each line and **drops a reminder marker exactly where that client is most likely to pay**, each tagged with a tone (Cordial · Direct · Ferme). Then we zoom into one of those reminders to read the personalised e-mail, and finish on the proof (−38 %, 11 jours) and the offer.

**Why it fits Ledgerly:** the brand name is literally "ledger". The whole piece is built on accounting-paper rules (fine horizontal lines, a red margin line, tabular figures) — the visual world of the target — then brought to life by precise, software-like motion. It shows the feature working (not a metaphor that needs decoding), which is what a DAF trusts. The recurring "playhead + marker" is the brand's visual signature of *timing*.

---

## 3. Art direction

### Palette (strict)
| Role | Hex | Use |
|---|---|---|
| Paper (dominant bg) | `#F4F1EA` | background of every scene except the proof scene |
| Ink (secondary) | `#11221E` | all text, logo tile, proof-scene background |
| Ledger green (accent) | `#16A36B` | playhead, reminder markers, "paid" states, CTA button, positive numbers |
| Overdue coral (alert, rare) | `#E4533A` | only: "En retard" tags, the red margin line, late dots. Never on large areas |
| Rule grey | `#CFC9BC` | ledger rules, dividers, inactive dots |
| Muted text | `#5E6B66` | secondary labels (≥ 4.5:1 on paper: OK) |
| Card white | `#FFFFFF` | UI cards (e-mail, client rows) |

Contrast checks: Ink on Paper ≈ 15:1; Paper on Ink ≈ 15:1; Green `#16A36B` is used on Ink or as fill with white text at ≥ 34 px bold (OK for large text); on Paper, green is only used for shapes/numbers ≥ 60 px.

### Type (2 families + mono)
- **Manrope** (weights 500, 700, 800) — all headlines and UI text.
  `<link>` `../../node_modules/@fontsource/manrope/500.css`, `/700.css`, `/800.css`
- **JetBrains Mono** (400, 500, 700) — dates, amounts, invoice numbers, timecode-like labels, numbers of the proof. `font-variant-numeric: tabular-nums`.
  `../../node_modules/@fontsource/jetbrains-mono/400.css`, `/500.css`, `/700.css`

Scale (1080 wide):
- H1 hook / proof headline: Manrope 800, **96 px**, line-height 1.02, letter-spacing −0.035em
- H2 scene headline: Manrope 800, **64 px**, lh 1.08, ls −0.03em
- Giant number: JetBrains Mono 700, **300 px**, ls −0.06em
- UI body / labels: Manrope 600–700, **32–36 px**
- Micro-labels (kicker, tags): JetBrains Mono 500, **28 px**, uppercase, ls +0.08em (only for 1–3-word tags, never sentences)
- End-card URL: JetBrains Mono 500, 40 px

### Graphic language
- **Ledger page:** background paper with horizontal rules every **54 px** (1 px, `#CFC9BC` at 55 % opacity) across the full width, and one vertical **red margin line** (2 px, `#E4533A` at 60 %) at x = 120 px. This page is present in scenes 1, 2, 3, 5 (it's the world). Rules scroll very slowly upward (drift, 8 px/s) to keep holds alive.
- **Client rows:** white cards, radius 20 px, 1 px border `#E3DED3`, soft shadow `0 18px 40px -22px rgba(17,34,30,.28)`.
- **Timeline:** a 1 px ink line with tick marks every "day" (30 ticks), only `J+0` and `J+30` labels shown, JetBrains Mono 500 28 px muted.
- **Payment dots:** 14 px circles. Past payments = ink at 35 % opacity; late = coral outline.
- **Playhead:** 3 px vertical line in Ledger green with a 14 px green dot on top, plus a faint green glow (box-shadow 0 0 24px rgba(22,163,107,.45)).
- **Reminder marker:** a green pill (height 52 px, radius 26) containing a lucide `send` icon (white, 24 px) + mono label (e.g. `MAR. 9 H 40`) — white text 28 px 700. Below/next to it a **tone chip**: outlined pill, 2 px ink border, Manrope 700 28 px (`Cordial`, `Direct`, `Ferme`).
- Icons: Lucide only, 2 px stroke: `send`, `clock-3`, `sparkles` (used once, tiny, next to "IA"), `check`, `arrow-right`, `mail`, `message-square`.
- No gradients except the green glow; no glassmorphism; no emoji.

### Texture
- SVG `feTurbulence` grain overlay (baseFrequency 0.9, numOctaves 2, stitchTiles) as a full-frame fixed layer, **opacity 0.06** on paper scenes, `mix-blend-mode: multiply`; on the ink scene use opacity 0.08 with `mix-blend-mode: screen`.
- Very soft vignette on paper: radial-gradient(transparent 60 %, rgba(17,34,30,.06)).

### Logo — "ledgerly"
- **Symbol:** a 64 × 64 ink tile (`#11221E`), radius 16. Inside: two horizontal paper-colored bars (4 px tall, rounded): top bar 32 px wide at y = 24, bottom bar 20 px wide at y = 38, both left-aligned at x = 14; at the right end of the bottom bar, a **10 px green dot** (`#16A36B`) at x = 42, y = 40 center. Reading: ledger lines + "the right moment".
- **Wordmark:** "ledgerly" in Manrope 800, lowercase, ls −0.04em, ink, set 16 px right of the tile, cap-height aligned so the x-height centers on the tile.
- Sizes: header lock-up 40 px tile / 40 px wordmark; end card 96 px tile / 88 px wordmark.
- The same green dot is the "playhead dot" in the timeline — brand consistency: the logo's dot *is* the reminder.

### Persistent header (scenes 1–4)
Top-left at (72, 64): small logo lock-up (tile 40 px + "ledgerly" 36 px). Top-right at right: 72, y 72: mono 28 px `#5E6B66` text `RELANCES INTELLIGENTES` preceded by a 10 px green dot. On the proof scene (ink bg) the header stays but recolors to paper (tile becomes paper with ink bars). Hidden on end card (the big logo replaces it).

---

## 4. Final French copy (exact strings)

Use U+202F (narrow no-break space) before `: ; ! ?`, inside « », before `%`, before `€`, and as thousands separator; `’` apostrophes; real minus sign `−` (U+2212) for −38 %.

**Header (scenes 1–4)**
- `ledgerly`
- `RELANCES INTELLIGENTES`

**Scene 1 — Hook**
- Line A: `Relancer trop tôt, ça froisse.`
- Line B: `Trop tard, ça coûte.`
- Invoice card (3 cards stacked, fanned):
  - `F-2026-0412` · `Boulangerie Marceau` · `1 280,00 €` · tag `EN RETARD · 18 J`
  - `F-2026-0398` · `Atelier Brunet SARL` · `4 950,00 €` · tag `EN RETARD · 31 J`
  - `F-2026-0377` · `Groupe Lemaire` · `12 400,00 €` · tag `EN RETARD · 47 J`

**Scene 2 — Every client has its rhythm**
- H2: `Chaque client paie à son rythme.`
- Rows (name — sub-label):
  - `Boulangerie Marceau` — `paie souvent le 5 du mois`
  - `Atelier Brunet SARL` — `répond mieux par SMS`
  - `Groupe Lemaire` — `circuit de validation : 3 personnes`
- Timeline labels: `J+0` · `J+30`

**Scene 3 — The feature**
- Kicker (mono): `NOUVEAU`
- H2: `Relances intelligentes`
- Sub (Manrope 600, 36 px, muted): `L’IA choisit le bon moment et le bon ton.`
- Markers:
  - Row 1: `MAR. 9 H 40` + chip `Cordial`
  - Row 2: `JEU. 14 H 15` + chip `Direct` + small icon `message-square` + mono `SMS`
  - Row 3: `LUN. 8 H 30` + chip `Ferme`

**Scene 4 — The e-mail (zoom on row 1)**
- E-mail header lines:
  - `À : Julie Marceau`
  - `Objet : Facture F-2026-0412 — petit rappel`
- Body (3 lines, typed):
  - `Bonjour Julie,`
  - `Petit rappel amical : la facture F-2026-0412 (1 280,00 €) était due le 12 septembre.`
  - `Vous pouvez la régler en un clic ici. Belle journée !`
- Button in e-mail: `Payer la facture`
- Status toast (after send): `Envoyé · mardi 9 h 40` → then `Payée · mardi 11 h 02` (with `check` icon, green)

**Scene 5 — Proof (ink background)**
- Kicker: `EN MOYENNE, CHEZ NOS CLIENTS`
- Number 1: `−38 %` + label `de retards de paiement`
- Number 2: `11 jours` + label `gagnés sur le DSO`
- DSO bar labels: `DSO avant` `52 j` · `avec Ledgerly` `41 j`

**Scene 6 — End card**
- Logo lock-up (big)
- Line: `Soyez payé au bon moment.`
- Sub: `Connecté à votre logiciel de compta. E-mail et SMS.`
- CTA button: `Essai gratuit 14 jours`
- URL: `ledgerly.io`

Proofread notes: « froisse » (not « vexe »), « ça coûte » lowercase after comma; « Relances intelligentes » capital R only; « DSO » in caps; « 9 h 40 » with spaces (French hour style); « 1 280,00 € » with U+202F thousands and before €.

---

## 5. Storyboard (23.0 s)

Canvas 1080 × 1350. Side margin 72 px. Content column 72 → 1008 (936 px). All times in seconds.

### Scene 1 — Hook · 0.00 → 3.60
**Layout:** ledger page bg. Header visible from frame 0. Headline block top-left at y = 200: Line A (96 px, ink, 2 lines max → it wraps as "Relancer trop tôt, / ça froisse.") and Line B below with 24 px gap, Line B in **coral** for "ça coûte." only (`Trop tard,` in ink). Lower half (y 700–1250): three invoice cards (white, 720 × 190 px, radius 20) fanned: centered at x = 540, rotations −6°, +3°, −1.5°, stacked with 70 px vertical offset; each card: invoice number (mono 28 px muted) top-left, client name (Manrope 700 36 px) below, amount (mono 700 44 px) bottom-right, coral tag top-right (coral fill at 12 % opacity, coral text, JetBrains Mono 500 28 px, radius 10, padding 6 14).
**Motion:**
- 0.00: cards already in frame at 60 % of their final position (y + 120 px, opacity 1) — motion from frame 0: they rise and settle over 0.00–0.90 (`expo.out`, stagger 0.08).
- 0.10–0.70: Line A words slide up from masks (stagger 0.06, `power3.out`, from yPercent 110).
- 0.90–1.30: coral tags stamp on each card: scale 1.4 → 1, opacity 0 → 1, `back.out(2)`, stagger 0.1; tiny 3 px card shake at impact.
- 1.30–1.80: Line B words slide up (same style).
- 1.80–3.20: hold; the late-days number in each tag ticks up by +1 (18→19, 31→32, 47→48) at 2.6 s — a subtle "time is passing" beat. Rules drift.
- **Transition 3.20–3.60:** the three cards fly into a vertical list and flatten (rotation → 0, width 720 → 936, height 190 → 220), morphing into the three client rows of Scene 2 (FLIP-style; keep same stacking order). Headline lines exit up through masks (`power2.in`, 0.3 s).

### Scene 2 — Rhythm · 3.60 → 7.60
**Layout:** H2 `Chaque client paie à son rythme.` at y = 190, 64 px, max width 900 (2 lines). Three client rows, cards 936 × 230 px at y = 430, 690, 950 (gap 30). Inside each row: top-left client name (Manrope 700 36 px ink), under it sub-label (Manrope 500 30 px muted); bottom zone (y offset 130–200): the 30-day timeline across the card width (inner padding 36 px), with 30 ticks (1 px × 10 px, rule grey), `J+0` left and `J+30` right labels (mono 28 px muted) below the line.
**Payment dots** (historical, deterministic positions, day index 0–29):
- Row 1 (Marceau): dots at days 3, 4, 5, 5, 6 (clustered early) — ink 35 %.
- Row 2 (Brunet): dots at days 10, 14, 15, 16, 22 — ink 35 %, one at 22 coral outline.
- Row 3 (Lemaire): dots at days 19, 21, 24, 26, 27 — ink 35 %, the 26 and 27 coral outline.
(Overlapping dots at same day stack vertically by 16 px.)
**Motion:**
- 3.60–4.20: H2 words mask-in (stagger 0.05).
- 3.80–4.60: timelines draw left→right (scaleX 0 → 1, `power3.out`), ticks stagger in.
- 4.40–5.60: dots pop in per row (scale 0 → 1, `back.out(1.8)`, stagger 0.05 within row, 0.15 between rows), sub-labels fade/slide in (y 12 → 0) at 4.6 / 4.75 / 4.9.
- 5.60–7.20: hold with life: each row's dot cluster gets a soft ink-10 % bracket/highlight band behind it (a rounded rect behind the dots' span) that grows in at 5.8 (0.4 s) — shows the "rhythm zone".
- **Transition 7.20–7.60:** H2 slides out up (mask). Rows stay in place (continuity) — the scene 3 headline replaces it.

### Scene 3 — Feature reveal · 7.60 → 12.60
**Layout:** rows keep positions. Header area y 150–380: kicker `NOUVEAU` (mono 28 px, green, with `sparkles` icon 24 px left of it) at y = 160; H2 `Relances intelligentes` 64 px ink at y = 205; sub `L’IA choisit le bon moment et le bon ton.` 36 px muted at y = 290.
**Motion:**
- 7.60–8.20: kicker + H2 + sub mask-in (stagger 0.1).
- 8.30–11.40: **the playhead pass.** For each row in sequence (row 1: 8.3–9.2, row 2: 9.2–10.1, row 3: 10.1–11.0), a green playhead (3 px × card height minus 40, green dot on top) enters at J+0 and sweeps right (`power2.inOut`, 0.55 s) to the chosen day:
  - Row 1 → day 5 (in its cluster)
  - Row 2 → day 15
  - Row 3 → day 24
  On arrival: playhead stops, a short ring pulse (green, 0 → 40 px radius, opacity .5 → 0, 0.4 s), and the **reminder marker pill** pops from the playhead dot (scale 0.6 → 1, `back.out(2)`, 0.3 s), placed above the timeline, anchored left edge at playhead x (clamped inside card right edge − 24 px). The **tone chip** appears next to the pill 0.1 s later, sliding from x − 16 px. Row 2 additionally shows `message-square` icon + `SMS` next to the chip. The playhead then fades to 40 % and stays as a thin green line.
  To make room, the sub-label of each row fades to 0 just before its marker appears (markers sit in the sub-label line, right side of the card, y offset ≈ 70 px).
- 11.00–12.20: hold. All three markers visible; the three green lines give a staggered "diagonal" of right moments — the signature image. Micro-life: marker pills breathe (scale 1 → 1.02, sine, 1.6 s period).
- **Transition 12.20–12.60: zoom-through.** Camera (a wrapper transform) zooms into row 1's marker pill (scale 1 → 3.2, origin on the pill, `power3.in`); at 12.45 the pill's green fills the frame as a green circle wipe that expands to full frame; at 12.60 it reveals Scene 4 (the circle wipe reveals the paper e-mail scene beneath). (Implement: a green circle div at pill center, scale from 0 to cover 1800 px diameter 12.30–12.55, then the scene 4 layer is revealed by a second paper circle expanding from the same center 12.50–12.80 — a two-tone iris.)

### Scene 4 — The e-mail · 12.60 → 16.60
**Layout:** ledger paper bg. Top at y = 170: small row recap — green pill `MAR. 9 H 40` + chip `Cordial` + mono muted `Boulangerie Marceau` (so the viewer keeps context). E-mail card: white, x 72 → 1008, y 280 → 1040, radius 24, shadow as rows. Inside (padding 48 px):
- Top bar (no fake window dots): lucide `mail` icon 28 px + `Nouveau message` Manrope 700 30 px muted. 1 px rule.
- `À : Julie Marceau` (Manrope 600 32 px; "À :" muted), rule; `Objet : Facture F-2026-0412 — petit rappel`, rule.
- Body at 34 px Manrope 500 ink, lh 1.4, max width 840: 3 paragraphs (see copy). The amount `1 280,00 €` and `F-2026-0412` rendered in JetBrains Mono 500 (inline).
- Button: green fill, white Manrope 700 32 px `Payer la facture`, height 76, radius 38, padding 0 40, at bottom-left of the card.
- Below the card at y = 1090: status toast (ink bg, paper text, radius 999, height 72, Manrope 700 32 px, icon left).
**Motion:**
- 12.60–13.00: card rises (y + 40 → 0, `expo.out`), header lines type-in quickly (TextPlugin, 0.25 s each).
- 13.00–14.90: body text types in (TextPlugin or char reveal) — "Bonjour Julie," 0.3 s; paragraph 2 1.0 s; paragraph 3 0.6 s. A green caret blinks via deterministic `Math.floor(t*2)%2`.
- 14.90–15.20: button pops in (scale 0.9 → 1, `back.out`).
- 15.30: toast slides up from y + 40: `send` icon + `Envoyé · mardi 9 h 40`.
- 15.90: toast morphs: background ink → green (0.3 s), icon `send` → `check`, text crossfades (mask up) to `Payée · mardi 11 h 02`.
- **Transition 16.30–16.60:** ink panel wipes up from the bottom (full-frame ink rectangle, yPercent 100 → 0, `power4.inOut`, 0.35 s) covering the e-mail scene. Header recolors to paper as the panel passes.

### Scene 5 — Proof · 16.60 → 20.00 (ink background `#11221E`)
**Layout:** grain (screen). Faint ledger rules continue but in paper at 6 % opacity. Kicker `EN MOYENNE, CHEZ NOS CLIENTS` mono 28 px, paper at 70 %, at y = 190.
- Block 1 at y = 250: `−38 %` JetBrains Mono 700 **260 px** in **green**, label `de retards de paiement` Manrope 700 44 px paper, directly under (y ≈ 540).
- Divider 1 px paper 15 % at y = 640.
- Block 2 at y = 690: `11 jours` Manrope 800 **160 px**, paper; the "11" is mono 700 in green, " jours" in Manrope 800 paper. Label `gagnés sur le DSO` Manrope 700 44 px paper 80 %.
- DSO bars at y 1020–1180: two horizontal bars, height 52, radius 26, left x = 72.
  - Bar A: label left above `DSO avant` (mono 28 px paper 60 %), bar width 936 × (52/52) = 936 px, fill paper 18 %, value `52 j` at bar right inside (mono 700 32 px paper).
  - Bar B: label `avec Ledgerly`, width 936 × 41/52 = **738 px**, fill green, value `41 j` inside right (mono 700 32 px, ink).
  - The 198 px gap at the end of bar B is marked with a dashed paper outline and a small label `−11 j` in green mono 28 px above it.
**Motion:**
- 16.70: kicker types in (ScrambleText, chars "0123456789", 0.4 s).
- 16.80–17.60: `−38 %` counts from `0 %` to `−38 %` (integer steps, `power2.out`) while sliding up from mask; label mask-in at 17.2.
- 17.70–18.50: `11` counts 0 → 11; label in at 18.1.
- 18.40–19.30: Bar A grows 0 → 936 (0.5 s, `power3.out`), Bar B grows 0 → 936 then **shrinks back to 738** (0.35 s grow + 0.4 s settle, `power3.inOut`) — visualises days removed; dashed gap + `−11 j` fade in at 19.2.
- 19.30–19.70: hold.
- **Transition 19.70–20.00:** everything on the ink panel slides up 60 px and fades; the ink panel itself splits along the horizontal center into two halves that slide off top and bottom (`power4.inOut`), revealing the paper end card beneath.

### Scene 6 — End card · 20.00 → 23.00 (hold ≥ 2.5 s)
**Layout (centered column, paper bg + rules + red margin line):**
- Big logo lock-up centered horizontally at y = 380 (tile 96 px + wordmark 88 px).
- `Soyez payé au bon moment.` Manrope 800 72 px ink, centered, y = 560, max width 900 (can wrap to 2 lines: "Soyez payé / au bon moment.").
- Sub `Connecté à votre logiciel de compta. E-mail et SMS.` Manrope 600 34 px muted, centered, y ≈ 760, max width 820 (2 lines allowed).
- CTA button: green fill, height 100, radius 50, padding 0 56, Manrope 800 40 px white `Essai gratuit 14 jours` + lucide `arrow-right` 36 px white, centered, y = 900.
- URL `ledgerly.io` JetBrains Mono 500 40 px ink, centered, y = 1050.
- Bottom ornament y = 1180: a thin 30-tick timeline (like scene 2) across 600 px centered, with a single green dot/playhead at day 5 — echo of the idea.
**Motion:**
- 20.00–20.50: logo: tile scales 0.8 → 1 (`back.out(1.6)`), inside bars draw left→right (scaleX), green dot pops last (20.45); wordmark letters rise from mask (stagger 0.025).
- 20.40–20.90: headline words mask-in (stagger 0.05). Sub fades/slides at 20.8.
- 21.00: CTA button scales 0.92 → 1 + opacity; arrow nudges right 8 px and back (21.4–21.8, `sine.inOut`), once.
- 21.10: URL types in (TextPlugin 0.3 s). Timeline ornament draws 21.0–21.5; green playhead slides to day 5 at 21.5–21.9.
- 21.90–23.00: calm hold; only rules drift and the ornament's green dot has a soft pulse ring every 1.0 s (deterministic from t). No other motion.

---

## 6. Motion notes (global)
- Personality: **precise, confident, software-like.** Entrances `power3.out` / `expo.out` (0.4–0.6 s), exits `power2.in` (0.25–0.35 s), moves `power3.inOut`. Pops only on markers/tags (`back.out(1.8–2)`).
- All headline text enters by **line/word masks** (overflow-hidden wrapper, yPercent 110 → 0). Never a plain fade on headlines.
- Rhythm: fast (hook) – steady (rhythm) – **deliberate** (playhead passes, one per row) – quick (typing) – punchy (numbers) – calm (end card).
- Continuity devices: invoice cards → client rows (FLIP); marker pill → green iris → e-mail; ink panel wipe up → split open to end card; the green dot (logo = playhead = end ornament).
- Keep alive: rules drift 8 px/s upward throughout (except end card slows to 4 px/s); grain static (it's a texture, not noise flicker — no per-frame reseed).
- Reading-time check: Line A+B (8 words) visible 0.7→3.2 = 2.5 s+; H2 scene 2 (6 words) 4.0 s; scene 3 headline+sub (10 words) ~4.6 s; e-mail is a visual (not fully read — OK); proof blocks ≥ 2 s each; end card 3 s.
- LinkedIn feed, sound off: no reliance on audio; 4:5 so full canvas is visible — keep 60 px safety from all edges anyway (72 px used).

## 7. Technical approach hints
- Single `index.html`, DOM + SVG, **GSAP** one master `gsap.timeline({paused:true})`; `window.KLIPT = { width:1080, height:1350, fps:30, duration:23, ready: document.fonts.ready, render: t => { tl.seek(t,false); } }`.
- Plugins: TextPlugin (typing), ScrambleTextPlugin (kicker), CustomEase optional. Load from `../../node_modules/gsap/dist/`.
- Counters: tween a proxy object `{v:0}` with `onUpdate` writing `Math.round(v)` into the DOM (works with seek). Use `−` (U+2212) prefix and U+202F before `%`.
- Ledger rules: one absolutely positioned div with `repeating-linear-gradient(to bottom, transparent 0 53px, rgba(207,201,188,.55) 53px 54px)`; drift via a GSAP tween on `backgroundPositionY` across the whole duration (linear allowed for continuous drift).
- Grain: inline SVG `<filter><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>` on a full-frame rect; static.
- FLIP invoice → rows: pre-compute both layouts as absolute positions; tween x/y/width/height/rotation of the same card elements; cross-fade inner contents (invoice content out, row content in) at the midpoint.
- Playhead positions: `x = cardInnerLeft + (day/29) * timelineWidth`.
- Caret blink: in `render(t)` after `tl.seek`, set caret opacity from `Math.floor(t*2.5)%2` (deterministic).
- Iris transitions: use `clip-path: circle(r at x y)` on the incoming scene layer, tweened.
- Lucide icons inlined as SVG (`send`, `check`, `sparkles`, `mail`, `message-square`, `arrow-right`) with `stroke="currentColor"` stroke-width 2.
- Check with `node tools/render.mjs frame` at t = 0.5, 2.8, 5.8, 11.5, 14.5, 16.2, 19.4, 22.0.
- meta.json: kind `video`, format `1080x1350`, duration 23, techniques `["gsap","svg","ui-mockup","data-viz","kinetic-type","text-plugin"]`, fonts `["Manrope","JetBrains Mono"]`, palette `["#F4F1EA","#11221E","#16A36B","#E4533A","#CFC9BC"]`, copy_language `fr`.

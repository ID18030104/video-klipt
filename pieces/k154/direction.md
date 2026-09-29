# k154 — Garnier & Fils · « 5 signes que votre chauffe-eau va lâcher »

Carousel · 7 slides · 1080 × 1350 · Facebook + Instagram · French copy

---

## 1. Audience insight & the one message

**Who scrolls past this:** a homeowner in the Nantes area, 35–70, scrolling Facebook in the evening. Their water heater lives in a garage, cellar or cupboard: they haven't looked at it in years. They fear two things: a cold shower on a Sunday in January, and getting ripped off by a plumber found in a panic.

**Insight:** people don't call a plumber *before* a breakdown because they don't know what to look for. Give them a checklist they can do in 5 minutes and they will trust the family firm that gave it to them for free.

**The one message:** *Your water heater warns you before it gives up. Learn the signs, and call Garnier & Fils before the cold shower.*

**Register:** a local, expert, reassuring craftsman. Sturdy and precise, like a good technical manual or the plate on a boiler. Warm, not folksy. No gimmicks.

---

## 2. Concept — « La fiche technique du chauffe-eau »

The carousel is built like a **plumber's technical sheet**: clean cut-away illustrations of a water heater (cumulus), labelled parts, a hard-working copper pipe, and an "urgency gauge" for each sign. Each slide looks at one part of the same appliance (résistance, anode, calcaire, groupe de sécurité, plaque signalétique, consommation). The homeowner learns to "read" their own water heater.

**Visual continuity:** a **copper pipe** runs across every slide at exactly the same height (centre y = 1172 px). It comes out of the water heater on slide 1, crosses slides 2–6 edge to edge (so the swipe feels like one continuous installation), and on slide 7 it plugs into the phone-number block. The idea is that everything leads to the call.

Why it fits: plumbing is precise work. A technical-sheet look says *expertise* and the copper/navy palette says *artisan since 1987*. The generous white space and large type suit a 35–70 audience reading on a phone.

---

## 3. Art direction

### Palette (strict)
| Role | Name | Hex | Use |
|---|---|---|---|
| Dominant dark | Bleu atelier | `#14304A` | Backgrounds of slides 1 and 7, the "Quoi faire" boxes, illustration strokes |
| Dominant light | Papier | `#F4EEE3` | Backgrounds of slides 2–6, cream text on navy |
| Accent | Cuivre | `#C8662F` | Pipe, big numerals, highlighted parts, price. **Display sizes only (≥ 60 px or graphics)**: its contrast is 3.5:1 on navy and about 3.4:1 on cream |
| Accent text | Cuivre foncé | `#A24E1F` | Copper-coloured text on cream at small sizes (contrast about 4.9:1) |
| Accent text on navy | Cuivre clair | `#E89A66` | Copper-coloured text on navy at small sizes (contrast about 6:1) |
| Ink | Encre | `#0F1F30` | Body text and titles on cream |
| Water | Eau froide | `#5E8FB8` | **Only** for water, drops and the cold-water pipe |
| Lime | Calcaire | `#E3DCCB` | Scale/sediment layers, the metal plate background (slide 5 uses `#DCD6CC` for the plate) |
| Paper white | Blanc cuve | `#FFFBF4` | Water-heater body fill on cream slides |

### Typography (2 families)
- **Archivo Black 400** (`@fontsource/archivo-black/400.css`): all titles, numerals, price and phone number. Tight leading (1.0–1.05). Letter-spacing −0.01em on sizes ≥ 96 px.
- **Figtree** (`@fontsource/figtree/500.css`, `600.css`, `700.css`, `800.css`, `700-italic.css`): body, labels, kickers.

Scale (px, 1080-wide canvas):
| Role | Font | Size / line-height |
|---|---|---|
| Hook "5 signes" | Archivo Black | 150 / 1.0 |
| Sign numeral | Archivo Black | 260 / 0.85 |
| Price "49 €" | Archivo Black | 240 / 0.9 |
| Slide 7 title | Archivo Black | 96 / 1.0 |
| Slide 1 subtitle | Archivo Black | 72 / 1.04 |
| Sign titles (slides 2–6) | Archivo Black | 60 / 1.06 |
| Phone number | Archivo Black | 76 / 1.0 |
| Chart values | Archivo Black | 44 |
| Italic tagline | Figtree 700 italic | 52 |
| "Quoi faire" body / checklist | Figtree 600 | 34 / 1.3 |
| Explanations | Figtree 500 | 32 / 1.35 |
| Labels, kickers, header, footer, tags | Figtree 700–800 | 30, caps labels letter-spacing 0.12–0.14em |
| Logo sub-line only | Figtree 700 | 18, letter-spacing 0.18em (this is the logo lockup, not reading text) |

No reading text under 30 px. The only exceptions are the logo sub-line and the stamp line (28 px).

### Graphic language
- **Technical illustration:** SVG, flat fills, **6 px navy strokes** (`#14304A`, round joins/caps), with a hard offset shadow of 8 px 8 px 0 `rgba(15,31,48,0.12)` (on navy slides use `rgba(0,0,0,0.25)`). No gradients except on the copper pipe.
- **Callout tags:** rounded rectangles (radius 10, padding 8 × 16), navy fill, cream text in Figtree 700 30 px, with a 3 px navy leader line ending in a 14 px copper dot on the part.
- **Urgency gauge** (slides 2–6): 3 segments, each 44 × 14 px, radius 7, gap 6 px. Lit segments are `#C8662F`, unlit ones are `rgba(15,31,48,0.15)`. It is followed by a label in Figtree 700 30 px `#A24E1F`.
- **Icons:** Lucide inline SVG (`wrench`, `check`, `arrow-right`, `phone`, `triangle-alert`), stroke-width 2.5, in the listed colours.
- **Copper pipe (continuity element):** a horizontal bar 30 px tall, centred at y = 1172, full slide width on slides 2–6. Fill is a vertical linear gradient: `#E08A52` 0 %, `#C8662F` 45 %, `#8E4418` 100 %. A 3 px highlight line `rgba(242,183,140,0.6)` sits 7 px below the top edge. Each slide has **one fitting (raccord)**: a rounded rectangle 46 × 54, radius 6, fill `#A24E1F`, 2 px `#8E4418` border, with two 2 px lighter rings (`#C8662F`) 12 px from each side, vertically centred on the pipe. Fitting x-centre per slide: S2 = 300, S3 = 780, S4 = 520, S5 = 220, S6 = 860. The pipe must touch x = 0 and x = 1080 exactly, so the swipe joins seamlessly.

### Textures
- **Cream slides:** paper grain made with SVG `feTurbulence` (type fractalNoise, baseFrequency 0.9, numOctaves 2, seed 7), desaturated, `mix-blend-mode: multiply`, opacity 0.06, full-slide overlay above the background and below the content.
- **Navy slides:** a blueprint grid (1 px lines `rgba(244,238,227,0.05)` every 54 px, via two `repeating-linear-gradient`s), plus the same grain at opacity 0.05 in `soft-light`, plus a soft vignette `radial-gradient(ellipse at 30% 20%, rgba(255,255,255,0.05), transparent 60%)`.

### Logo — "Goutte-flamme" lockup
- **Symbol:** a water-drop outline (navy on cream, cream on navy), 64 px tall, 6 px stroke. Inside it, in its lower two-thirds, sits a small solid copper `#C8662F` flame (3-point flame path). This mixes plumbing (drop) and heating (flame).
- **Wordmark**, to the right of the symbol (gap 16 px):
  - Line 1: `GARNIER & FILS` in Archivo Black 34 px, with the `&` in copper (`#C8662F` on navy, `#A24E1F` on cream).
  - Line 2: `PLOMBERIE · CHAUFFAGE` in Figtree 700 18 px, letter-spacing 0.18em (`#E89A66` on navy, `#A24E1F` on cream).
- **Compact version** (header of slides 2–6): the symbol at 52 px plus line 1 only at 28 px.
- Build it once as an SVG `<symbol>` (drop + flame) and reuse it everywhere.

---

## 4. Shared grid (all slides)

- Canvas 1080 × 1350. Side margins 72 px, so the content box runs from x 72 to x 1008.
- **Header** (y 56–112): logo lockup at left (x 72). At right (aligned to x 1008), the pagination `0N / 07` in Figtree 700 30 px: `0N` at full opacity, ` / 07` at 45 % opacity.
- **Hairline** at y 136 (slides 2–6 only): 2 px, ink at 15 % opacity, from x 72 to x 1008.
- **Pipe** centred at y 1172 (see above).
- **Footer** (y 1236–1290, slides 1–6):
  - Left: `garnier-plomberie.fr` in Figtree 700 30 px, at 70 % opacity. On slide 1 the left footer reads `Dépannage 7j/7 · Nantes` instead.
  - Right: a copper circle 56 px (`#C8662F`) with a cream `arrow-right` icon (28 px). On slide 1 it is preceded by the text `Faites glisser`, Figtree 700 30 px, cream, with a 16 px gap before the circle.
- **Sign-slide columns (2–6):**
  - Left column x 72–600 holds the numeral, title and explanation.
  - Right column x 620–1008 holds the illustration or data, from y 170 to y 820.
  - The **"Quoi faire" box** spans full width: x 72–1008, y 846–1124, navy `#14304A`, radius 20, padding 44. Inside, first a row with the `wrench` icon (40 px, `#E89A66`), a 14 px gap, then `QUOI FAIRE` in Figtree 800 30 px, letter-spacing 0.14em, `#E89A66`. Then, 18 px below, the body text in Figtree 600 34 px, line-height 1.3, cream `#F4EEE3`, max 3 lines.

### Sign-slide left column, element by element (identical on 2–6)
1. **Numeral** (`1`…`5`): Archivo Black 260 px, `#C8662F`, line-height 0.85, top at y 170, x 72.
2. **Meta block**, to the right of the numeral with its left edge at x 270:
   - At y 196: `SIGNE N°X SUR 5` in Figtree 800 30 px, letter-spacing 0.12em, ink at 60 %.
   - At y 250: the urgency gauge, then its label 16 px to the right.
3. **Title**: Archivo Black 60 px, ink, line-height 1.06. Top at y 430, width 528. Use the **line breaks exactly as given below**. If any line overflows 528 px, reduce all five titles to 56 px together.
4. **Explanation**: Figtree 500 32 px, line-height 1.35, ink at 85 %. It starts 30 px under the title, width 528, max 4 lines. It must end above y 820.

---

## 5. Final French copy + slide-by-slide layout

The strings below are final. Apply French typography exactly as follows:
- Use a narrow no-break space U+202F before `? ! : ;` and inside « ».
- Use a no-break space U+00A0 in `49 €`, `2 400 W`, `55–60 °C`, `10 %`, `02 40 12 34 56` and `N°1`, and between a number and its unit (`10 ans`, `1 mm`, `200 L`).
- Use the typographic apostrophe `’` and the ellipsis `…`.
- `/` marks a forced line break.

### Slide 1 — Hook (navy background)
- **Background:** navy, with the blueprint grid, grain and vignette.
- **Header:** the full logo lockup (cream/copper), and `01 / 07` in cream.
- **Kicker pill**, top-left at (72, 196): 2 px `#E89A66` outline, radius 999, padding 12 × 24. Text in Figtree 800 30 px, letter-spacing 0.12em, cream: **`CONSEILS DE PLOMBIER`**.
- **Line A**, y 270, Archivo Black 150 px, cream, with the `5` in `#C8662F`: **`5 signes`**
- **Line B**, y 450, Archivo Black 72 px, cream, width ≤ 560: **`que votre / chauffe-eau / va lâcher`**
- **Tagline**, 24 px below line B, Figtree 700 italic 52 px, `#E89A66`: **`(et quoi faire)`**
- **Promise**, y about 850, Figtree 500 34 px, cream at 80 %, width 560, 2 lines: **`Les conseils de nos techniciens, / depuis 1987.`**
- **Illustration:** the full water heater (see "Heater component"), box x 700–980, y 470–1060.
  - Cream body `#F4EEE3`, navy strokes, dark shadow.
  - A copper `triangle-alert` badge (64 px, copper fill with navy "!") pinned at the heater's upper-right shoulder, rotated 8°.
  - One water drop (`#5E8FB8`, 22 px) hangs under the groupe de sécurité.
  - The **hot outlet (copper) pipe** goes down from the heater bottom, curves with a 40 px-radius elbow at y 1172, and runs right to x 1080. This is where the continuous pipe starts.
  - The cold pipe (`#5E8FB8` fill, navy stroke, 26 px wide) goes straight down off the bottom of the slide.
- **Footer:** at left, `Dépannage 7j/7 · Nantes`, cream at 70 %. At right, `Faites glisser` plus the copper arrow circle.

### Slide 2 — Sign 1 (cream background)
- **Numeral** `1`. **Meta:** `SIGNE N°1 SUR 5`. **Gauge:** 2 of 3 segments lit, label **`À traiter vite`**.
- **Title:** **`L’eau sort / tiède ou / rouillée`**
- **Explanation:** **`Tartre sur la résistance ou cuve qui rouille de l’intérieur : votre ballon s’épuise.`**
- **Right column:** the heater component, 260 × 620 inside x 700–960, y 180–800. The cut-away window shows **rust-tinted water** (`#C8662F` at 28 % over `#FFFBF4`).
  - Inside the window, highlighted in copper (stroke `#C8662F`, 6 px, plus an 18 px copper glow `drop-shadow(0 0 10px rgba(200,102,47,0.45))`):
    - the **résistance** (a zigzag coil near the bottom);
    - the **anode** (a vertical rod rising from the base, two-thirds of the height).
  - Callout tag `Anode` (leader to the anode tip) at about (620, 330).
  - Callout tag `Résistance` (leader to the coil) at about (620, 640).
  - Tags may overlap the heater's left edge by up to 20 px, never the left column.
- **Quoi faire:** **`Ouvrez un robinet d’eau froide : si elle est claire, le souci vient du ballon. Faites contrôler l’anode et détartrer la résistance.`**
- **Pipe fitting** at x 300.

### Slide 3 — Sign 2 (cream background)
- **Numeral** `2`. **Meta:** `SIGNE N°2 SUR 5`. **Gauge:** 1 of 3 lit, label **`À surveiller`**.
- **Title:** **`Il claque, / siffle ou / gronde`**
- **Explanation:** **`Le calcaire tassé au fond piège de l’eau qui bout par à-coups. L’appareil force et s’use.`**
- **Right column:** the same heater at the same position.
  - The window holds clear water (`#5E8FB8` at 14 %).
  - At the bottom of the window is a **sediment layer** 60 px tall: fill `#E3DCCB`, with navy 2 px outline and about 40 small navy dots (r 3–5, seeded RNG, seed 23).
  - Five bubbles (navy stroke circles r 6–12) rise above the sediment.
  - On each side of the heater at bottom height, **3 concentric sound arcs** in copper, 6 px, round caps (radii 40, 70, 100, each spanning 70°). They point outwards, the left set mirroring the right set.
  - Callout tag `Calcaire` pointing into the sediment, at about (620, 720).
- **Quoi faire:** **`Faites détartrer le ballon tous les 2 à 3 ans. Si le bruit continue après, c’est la résistance qu’il faut changer.`**
- **Pipe fitting** at x 780.

### Slide 4 — Sign 3 (cream background): the focal point is the groupe de sécurité
- **Numeral** `3`. **Meta:** `SIGNE N°3 SUR 5`. **Gauge:** 3 of 3 lit, label **`Agir vite`**.
- **Title:** **`Ça fuit sous / le groupe / de sécurité`**
- **Explanation:** **`Quelques gouttes pendant la chauffe, c’est normal. Un filet continu, non : pression trop forte ou groupe usé.`**
- **Right column:** a close-up detail illustration, **not** the full heater.
  - The heater's bottom dome is cropped at the top (y 170–300, full column width, white body, navy stroke).
  - A **cold pipe** (blue fill, navy stroke, 30 px wide) comes down from its centre into a **large groupe de sécurité** (about 200 × 220 px, centred at x 814, y 470). The groupe has:
    - a copper T-body;
    - a round **molette** on the right side (copper disc 70 px with 8 notches, navy stroke);
    - a short drain nozzle below.
  - **Three water drops** (`#5E8FB8`, 26 / 22 / 18 px) fall in a vertical line into a **funnel + siphon** (navy outline, white fill) at y 660–800.
  - Callout tags: `Molette` (leader to the disc) at about (640, 380), and `Évacuation` (leader to the drops) at about (640, 640).
- **Quoi faire:** **`Manœuvrez la molette du groupe une fois par mois. Si ça coule sans arrêt : coupez l’eau froide et appelez-nous.`**
- **Pipe fitting** at x 520.

### Slide 5 — Sign 4 (cream background): data variant 1, the plate and the timeline
- **Numeral** `4`. **Meta:** `SIGNE N°4 SUR 5`. **Gauge:** 2 of 3 lit, label **`À anticiper`**.
- **Title:** **`Il a passé / ses 10 ans`**
- **Explanation:** **`Un chauffe-eau électrique dure en moyenne 10 à 15 ans. Passé 10 ans, chaque hiver est un pari.`**
- **Right column, top — a riveted metal nameplate:** x 620–1008, y 180–540. Fill `#DCD6CC`, 4 px navy border, radius 12, same hard shadow. There are 4 rivets (12 px circles, navy stroke) in the corners, and a subtle brushed look (a repeating-linear-gradient at 90° with lines of `rgba(255,255,255,0.18)` 1 px every 4 px). Padding 32. Content:
  - `CHAUFFE-EAU` in Archivo Black 34 px, navy.
  - A 2 px navy hairline.
  - `200 L · 2 400 W` in Figtree 700 30 px, ink.
  - `Fab. 03/2013` in Figtree 800 34 px, ink, surrounded by a **copper highlight**: a 4 px `#C8662F` rounded-rect outline, radius 8, padding 6 × 12, rotated −2°.
- **Right column, bottom — a timeline:** y 600–800.
  - Label `Âge du ballon` in Figtree 800 30 px, letter-spacing 0.1em, ink at 60 %.
  - The bar is 368 × 22 px, radius 11, at y 680, and represents 0 to 15 years.
    - From 0 to 10 years (the first 245 px), fill navy at 20 %.
    - From 10 to 15 years, fill `#C8662F` with 45° hatching (`rgba(255,255,255,0.25)` every 10 px).
  - Tick labels under the bar (Figtree 700 30 px): `0`, `5`, `10`, `15 ans`.
  - A **marker** at 13 years (x = 620 + 368 × 13/15 ≈ 939): a navy downward triangle above the bar, with the tag `13 ans` (navy pill, cream Figtree 700 30 px) above it.
- **Quoi faire:** **`Lisez la date sur la plaque signalétique, sur le côté du ballon. Plus de 10 ans ? Faites-le vérifier avant la panne.`**
- **Pipe fitting** at x 220.

### Slide 6 — Sign 5 (cream background): data variant 2, the bar chart
- **Numeral** `5`. **Meta:** `SIGNE N°5 SUR 5`. **Gauge:** 1 of 3 lit, label **`À surveiller`**.
- **Title:** **`La facture / d’électricité / grimpe`**
- **Explanation:** **`Le tartre isole la résistance : elle chauffe plus longtemps pour la même eau chaude.`**
- **Right column — the chart**, at x 620–1008:
  - **Caption** at y 180: `CONSOMMATION DU BALLON`, Figtree 800 30 px, letter-spacing 0.1em, ink at 60 %. It wraps to 2 lines if needed.
  - **Baseline** at y 740, a 3 px navy line.
  - **Bars:** 3 bars, each 92 px wide with 48 px gaps, starting at x 640 and starting at zero:
    | Bar | Height | Fill | Value above (Archivo Black 44 px) |
    |---|---|---|---|
    | 1 | 380 px | navy | `+0 %`, navy |
    | 2 | 418 px | `#C8662F` | `+10 %`, `#A24E1F` |
    | 3 | 456 px | `#C8662F` | `+20 %`, `#A24E1F` |
  - Each bar has a **scale cap** drawn inside its bottom: 0, 14 and 28 px tall, fill `#E3DCCB` with navy dot texture.
  - **Under the baseline:** `0 mm`, `1 mm`, `2 mm` in Figtree 700 30 px, and then a line below them: `de tartre`, Figtree 500 30 px, ink at 70 %, centred under the chart.
- **Key fact strip:** a copper-outlined pill (3 px `#C8662F`, radius 999) placed at the bottom of the left column, just under the explanation. Text in Figtree 700 30 px, `#A24E1F`: **`1 mm de tartre ≈ +10 % de consommation`**. If it doesn't fit in 528 px, put it inside the right column above the bars instead, and shorten the caption to 1 line.
- **Quoi faire:** **`Réglez le thermostat sur 55–60 °C, pas plus. Et si la facture monte sans raison, faites détartrer le ballon.`**
- **Pipe fitting** at x 860.

### Slide 7 — Offer & CTA (navy background)
- **Background:** navy, with grid, grain and vignette. **Header:** the full logo, and `07 / 07`. **No footer.**
- **Kicker pill** at y 180, same style as slide 1: **`UN DOUTE ? ON VÉRIFIE.`**
- **Title** at y 260, Archivo Black 96 px, cream: **`Diagnostic / chauffe-eau`**
- **Price** at y 480, x 72, Archivo Black 240 px, `#C8662F`: **`49 €`**
- **Stamp:** a circle 270 px in diameter, centre (870, 600), rotated −10°. It has a double ring (4 px `#E89A66` outer, 2 px inner, 10 px apart) and a transparent fill. Centred text:
  - **`OFFERT`** in Archivo Black 46 px, cream;
  - below it, **`si / remplacement`** in Figtree 700 28 px, `#E89A66`, on 2 lines.
- **Checklist** at y 760–960: 3 rows, Figtree 600 34 px, cream, row pitch 64 px. Each row starts with a `check` icon (36 px, `#E89A66`, stroke 3) followed by a 18 px gap.
  1. **`Contrôle de l’anode et de la résistance`**
  2. **`Test du groupe de sécurité et de la pression`**
  3. **`Devis clair, sans engagement`**
- **Trust line** at y 1000, Figtree 700 30 px, `#E89A66`: **`Depuis 1987 · 3 générations · 9 techniciens · 7j/7`**
- **CTA block:** x 72–1008, y 1064–1280, fill `#F4EEE3`, radius 24, padding 36 × 48. It holds, stacked left-aligned:
  - a row with the `phone` icon (32 px, `#A24E1F`) and **`APPELEZ-NOUS`** in Figtree 800 30 px, letter-spacing 0.12em, `#A24E1F`;
  - **`02 40 12 34 56`** in Archivo Black 76 px, navy;
  - **`garnier-plomberie.fr`** in Figtree 700 34 px, ink at 75 %.
- **Pipe:** it enters from x 0 at y 1172 (the block's vertical centre) and ends at x 72 in a fitting nut (hex nut shape, 40 × 60, `#A24E1F`) butting against the block's left edge. The whole installation ends at the phone number.

---

## 6. Heater component (reusable SVG, viewBox 0 0 300 640)

- **Wall brackets:** two navy tabs 30 × 16 at (70, 20) and (200, 20).
- **Body:** rounded capsule x 30–270, y 40–560, with rx = 120 and ry = 70 (hemispherical ends). Fill `#FFFBF4` (cream slides) or `#F4EEE3` (navy slide 1). Stroke navy 6.
- **Label band:** a horizontal band y 150–170 at navy 10 % (the brand strip). On slide 1 only, it carries a small symbol (drop + flame, 26 px).
- **Cut-away window:** x 70–230, y 200–470, radius 20, with a navy stroke 4. On slide 1 it is not shown; the body is plain.
- **Control cover:** rect x 100–200, y 480–540, radius 10, navy 15 %, with a 22 px thermostat knob (copper) and a small navy "voyant" dot.
- **Outlets:**
  - **Cold** at x 110: blue fill, 26 px wide.
  - **Hot** at x 190: copper-gradient fill, 26 px wide.
  - Both descend from y 560. The cold pipe has a small groupe de sécurité (a copper square 36 px plus a disc) at y 600.
- **Shadow:** the hard offset shadow as defined above, applied through a filter or a duplicated shape.

---

## 7. Motion notes

This is a static carousel, so there is no animation. All scripts run once at load (seeded RNG for the sediment dots, seed 23). Visual "motion" is suggested only by:
- the continuous pipe across the swipe;
- falling drops and sound arcs drawn in staggered sizes;
- the arrow circle in each footer.

---

## 8. Technical approach hints

- **Page structure:** one `index.html`, with `window.KLIPT = { width: 1080, height: 1350 }`. There are 7 `<section class="slide">` elements, each `position: relative; width: 1080px; height: 1350px; overflow: hidden`. Inside a slide, everything is absolutely positioned using the coordinates above.
- **Fonts:** `../../node_modules/@fontsource/archivo-black/400.css` and figtree `500.css`, `600.css`, `700.css`, `800.css`, `700-italic.css`. If the renderer honours `KLIPT.ready`, expose `ready: document.fonts.ready`.
- **Shared SVG defs:** one hidden `<svg>` holding:
  - `<symbol id="logo-mark">` (drop + flame);
  - `<symbol id="heater-body">`;
  - `<filter id="grain">`;
  - `<linearGradient id="copper">`.
  Use them via `<use>`. The variant internals (rust water, sediment, highlighted anode) are drawn per slide on top of the body.
- **Pipe:** a CSS component, `.pipe { position:absolute; left:0; right:0; top:1157px; height:30px; background:linear-gradient(#E08A52, #C8662F 45%, #8E4418) }`, plus a `::after` for the highlight and one `.fitting` element per slide. On slide 1 the pipe starts at the heater elbow (use SVG for the elbow). On slide 7 it runs from x 0 to x 72.
- **Icons:** inline the Lucide SVG markup (read the files from `../../node_modules/lucide-static/icons/`: `wrench.svg`, `check.svg`, `arrow-right.svg`, `phone.svg`, `triangle-alert.svg`), and set `stroke="currentColor"`.
- **Text:**
  - Put the typographic spaces directly in the HTML as `&#8239;` (U+202F) or `&nbsp;`.
  - Use explicit `<br>` for the given line breaks.
  - Set `hyphens: none`.
  - Check that no title line exceeds 528 px (Archivo Black is wide). If one does, drop all sign titles to 56 px.
- **QA after `node tools/render.mjs stills pieces/k154`:**
  - Open `sheet.jpg` and check that the pipe lines up at the slide edges.
  - Check that no "Quoi faire" text exceeds 3 lines and that the explanations end above y 820.
  - Check the contrast of copper text: `#C8662F` is for large display only.
  - Proofread every accent: `À`, `Â`, `É`, `œ` in « Manœuvrez ».
- **meta.json:**
  - kind `carousel`, format `1080x1350`, slides 7;
  - techniques `["svg-illustration","technical-cutaway","data-viz","css-textures","continuous-element-across-slides"]`;
  - fonts `["Archivo Black","Figtree"]`;
  - palette `["#14304A","#F4EEE3","#C8662F","#0F1F30","#5E8FB8"]`.

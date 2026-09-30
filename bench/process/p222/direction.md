# p222 — Boucherie Dufour · « Le guide des morceaux pour réussir votre barbecue »

Carousel · 6 slides · 1080 × 1350 · copy in French · static (stills render).

---

## 1. Audience insight & the one message

**Who swipes:** people aged 30 to 60 from the villages west of Lyon who host the family barbecue on a Saturday. They buy a côte de bœuf twice a year, pay 45 € for it, and are scared of ruining it. They know the names of the cuts but not the cooking times. They go to the supermarket out of habit, and to the butcher "when it matters".

**Insight:** *"The expensive meat is not the risky part. The cooking is."* People don't need more beautiful meat pictures, they need the **butcher's cheat sheet**: how thick it is, how many minutes, which heat, and the one trick that makes the difference. A butcher who gives that away earns trust, gets the carousel saved, and gets the order.

**The one message:** *At Dufour you get the right cut **and** the right way to cook it. Order the day before.*

Register: **artisanal, expert, warm, straightforward.** It sounds like the butcher talking across the counter. No gastronomic pretension, no puns.

---

## 2. Concept: « La fiche du boucher »

The carousel is the **butcher's cheat sheet on kraft paper**: the one he'd write for you with a pencil tucked behind his ear, stamped with the shop's stamp and tied with **red-and-white butcher's twine**.

- **Butcher's paper** (cream kraft background, grain, fibres) = the shop's wrapping, the physical object people take home.
- **Red-and-white butcher's twine** runs along the bottom of **every** slide at the same height. It enters on the left and leaves on the right, so it is continuous from one slide to the next. A **price tag** hangs on it and moves one notch to the right on each slide: that's the progress indicator (01/06 → 06/06).
- **Each cut is drawn as a flat SVG illustration** (chunky shapes, marbling, grill marks), plus a **cooking sheet** built from reusable "instruments": a heat gauge (flames), a big chrono number, and a core thermometer.
- **A red ink stamp** (the Dufour logo, round) guarantees origin: *Charolaise, maturée sur place*.

Why it fits: it's the shop's own material (paper, twine, stamp, chalk slate), turned into a practical guide. It couldn't be a chain supermarket: the voice is first person plural ("nos astuces", "on vous le réserve"), and there are local details (Charolaise, the cellar, sausages made every Thursday).

---

## 3. Art direction

### Palette (5 colours, strict)
| Role | Name | Hex | Use |
|---|---|---|---|
| Dominant background | Papier boucher | `#EFE6D6` | background of slides 1, 2, 3, 5 |
| Text / dark background | Charbon | `#1E1A18` | all text on paper; background of slide 4 |
| Brand accent | Rouge Dufour | `#A3202A` | titles in emphasis, meat, stamp, twine, background of slide 6 |
| Heat accent (rare) | Braise | `#E8792B` | flames ONLY + thermometer mercury + 1 word on slide 4. Never text on paper (contrast too low) |
| Secondary neutral | Kraft | `#C9B79A` | rules, dotted lines, cards' shadow, bones' shading, fat lines on the cow |
| (light tint, derived) | Crème os / gras | `#F7F1E6` | bones, fat marbling, white strands of the twine, text on red/charcoal |

Contrasts checked: Charbon on Papier ≈ 14:1; Rouge on Papier ≈ 6.4:1; Crème on Rouge ≈ 7:1; Crème on Charbon ≈ 15:1; Braise on Charbon ≈ 6:1.

### Typography (2 families only)
- **Fraunces** (display, soft old-style serif with a butcher's-shop-sign feel). Weights 900, 700, 600-italic. Load `index.css` + `/900.css` + `/700.css` + `/600-italic.css`.
- **Barlow Condensed** (labels, data, body: the "etched label"). Weights 500, 600, 700. Load `/500.css` `/600.css` `/700.css`.

Scale (px, 1080 wide):
| Level | Font | Size / line-height | Tracking |
|---|---|---|---|
| H0 hook title | Fraunces 900 | 118 / 1.0 | -0.02em |
| Big number | Fraunces 900 | 250 / 0.9 | -0.03em, tabular |
| H1 cut name | Fraunces 900 | 104 / 1.0 | -0.02em |
| H1 italic tagline | Fraunces 600 italic | 44 / 1.15 | 0 |
| H2 section | Fraunces 700 | 52 / 1.1 | -0.01em |
| Kicker / labels | Barlow Condensed 700 UPPERCASE | 28 / 1 | +0.14em |
| Body | Barlow Condensed 500 | 36 / 1.25 | +0.01em |
| Data values | Barlow Condensed 700 | 40 / 1.1 | 0 |
| Header / footer | Barlow Condensed 600 UPPERCASE | 26 / 1 | +0.16em |

No body text under 30 px. Emphasised words in titles: Fraunces **600 italic** in Rouge Dufour.

### Grid & recurring system (identical on all 6 slides)
- Margins: **72 px** left/right, content width 936 px.
- **Header** (baseline y = 104): on the left, the mini-stamp logo (Ø 64 px, top 60, left 72) + "BOUCHERIE DUFOUR" (header style) at x = 150. On the right, right-aligned to x = 1008: "LE GUIDE BARBECUE". A 2 px Kraft rule at y = 140, from x = 72 to 1008.
- **Footer / twine**: the twine is a horizontal line from x = 0 to x = 1080, centred at **y = 1262**, 10 px thick (see graphic language). It has a gentle sag (a quadratic curve that dips 14 px in the middle of each slide; the ends at x = 0 and x = 1080 are exactly at y = 1262 so they join between slides).
- **Price tag / progress**: a cream luggage tag (`#F7F1E6`, 1 px Kraft stroke, 120 × 64 px, left end trimmed to a point, a punched hole Ø 10 px ringed in Kraft), hanging under the twine by a 26 px thin charcoal thread. Text "0X / 06" Barlow Condensed 700 28 px Charbon. **Tag centre x per slide: 01 → 150, 02 → 306, 03 → 462, 04 → 618, 05 → 774, 06 → 930.** Tag top at y = 1284.
- A cooking card (when there is one) never goes below y = 1215.

### Graphic language
- **Cut illustrations**: flat SVG, generous shapes, no outline except where specified. Meat `#A3202A`, a darker shade `#7E1820` for the thickness/side, marbling = fine irregular cream `#F7F1E6` streaks (6–10 organic paths at 40–70 % opacity), fat cap `#F7F1E6` with a Kraft `#C9B79A` inner edge, bone `#F7F1E6` shaded with Kraft. **Grill marks**: 4 parallel diagonal bars (−35°), Charbon at 85 % opacity, 14 px wide, 60 px apart, clipped to the meat shape, slightly irregular ends (round linecap).
- **Heat gauge** (`.feu`): 3 Lucide `flame` icons, 46 px, spaced 10 px; active flames filled Braise `#E8792B` with a 2.5 px Charbon stroke, inactive flames 2.5 px Kraft stroke only. Label on the right in Barlow Condensed 700 UPPERCASE 28 px: "FEU VIF", "FEU MOYEN", etc.
- **Thermometer** (côte de bœuf only): vertical, 36 × 300 px, rounded, Crème fill with a 3 px Charbon outline, bulb Ø 64, Braise mercury up to the 52 °C mark, graduations every 10 °C (40/50/60) in Barlow 600 26 px.
- **Stamp**: circles and text in Rouge Dufour, rotated −8° to −12°, with an "ink" texture (mask via `feTurbulence` + `feColorMatrix` threshold so ~12 % of the ink is missing, with irregular edges).
- **Dotted lines** (cut lines on the animal, knife line): Charbon or Kraft, stroke 3 px, dasharray `2 10`, round linecap.
- **"Astuce du boucher" block**: 6 px Rouge vertical rule on the left + label "L’ASTUCE DU BOUCHER" in Rouge (kicker style) + text in Fraunces 600 italic 38/1.2 in Charbon. It's the recurring signature element of slides 2 → 5.

### Textures
- **Paper grain** over everything: a full-slide SVG layer, `feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="7"` desaturated, `mix-blend-mode: multiply`, opacity **0.07**.
- **Kraft fibres**: a second layer, `feTurbulence baseFrequency="0.012 0.35"` (stretched horizontally), opacity 0.05. That's what makes it read as paper, not a flat colour.
- **Vignette**: radial-gradient, transparent from the centre to 70 %, then `rgba(30,26,24,.10)` in the corners.
- Slide 4 (charcoal): same grain at opacity 0.10 in `screen` mode, plus 2 soft Braise radial glows at 10 % (a hint of embers, bottom left and top right).
- Slide 6 (red): grain at 0.10 multiply.

### Logo (to build in SVG, reused everywhere)
**Round "Dufour" stamp**, Ø 300 in the master version:
- Outer ring 6 px + inner ring 2 px, 14 px apart, Rouge Dufour.
- Text on a circular path between the rings, Barlow Condensed 700 UPPERCASE 30 px, tracking 0.22em: `BOUCHERIE · CHARCUTERIE · ARTISAN DEPUIS 1978 ·`
- At the centre, a **frontal Charolaise head**, stylised: a head shaped like a rounded trapezoid (wider at the top), two short horns curving upwards and outwards, two horizontal ears, a wide muzzle suggested by a flattened oval, two dots for nostrils. Drawn as a single Rouge filled shape with cream counter-shapes (muzzle, eyes = 2 small cream ellipses).
- Under the head: "DUFOUR" Fraunces 900 44 px, Rouge.
- Mini version in the header: Ø 64, rings + head only (no text).
- The stamp always carries the "ink" texture.

---

## 4. Final French copy (exact strings)

Typography: `⍽` = **narrow non-breaking space U+202F** (before `: ; ! ?` and inside « »; none inside `2′30″`-type values). `·` = U+00B7 middle dot. Number + unit separated by a **non-breaking space U+00A0** (noted `~` below): `1,2~kg`, `52~°C`, `10~min`. Apostrophes are always `’` (U+2019). Dashes: en dash `–` for ranges. In the HTML, write `&#8239;` for U+202F and `&nbsp;` for U+00A0.

### Slide 1 — Hook
- Kicker: `BOUCHERIE DUFOUR · LE GUIDE`
- Title (H0, 3 forced lines):
  `Le guide des morceaux`
  `pour *réussir*` ← *réussir* in Fraunces 600 italic Rouge
  `votre barbecue`
- Subtitle (body 36): `5 morceaux, leurs cuissons et nos astuces de boucher.`
- Numbered legend next to the illustration (Barlow 700 30 px, a Rouge circled number Ø 44 followed by the name):
  `1 Côte de bœuf` · `2 Entrecôte` · `3 Onglet` · `4 Poitrine de porc` · `5 Merguez maison`
- Stamp badge (arc text around a Ø 220 circle): `CHAROLAISE · MATURÉE SUR PLACE ·`
- Swipe cue (Barlow 700 UPPERCASE 28, Rouge): `Faites glisser` + a Lucide `arrow-right` 32 px

### Slide 2 — Côte de bœuf
- Kicker: `MORCEAU 01`
- H1: `Côte de bœuf`
- Tagline (italic): `La reine du feu, à partager.`
- Data line (3 values separated by Kraft `·`): `1,2~kg` `·` `4~cm d’épaisseur` `·` `3 à 4~personnes`
- Heat gauge: 3 active flames → `FEU VIF, PUIS INDIRECT`
- Steps (numbered 1-2-3, label in Barlow 700 UPPERCASE 28 Rouge + body 36):
  1. `SAISIR` — `3~min par face sur les braises vives.`
  2. `FINIR` — `12~min à côté des braises, couvercle fermé.`
  3. `REPOSER` — `10~min sous une feuille d’alu.`
- Thermometer: label `À CŒUR` above, big value `52~°C`, under it `= saignant`
- Astuce du boucher: `Sortez-la du frigo 1~h avant. Sel juste avant la grille, poivre après.`
- Origin mention (Barlow 600 26 UPPERCASE, Charbon at 70 % opacity): `MATURÉE 4 SEMAINES DANS NOTRE CAVE`

### Slide 3 — Entrecôte
- Kicker: `MORCEAU 02`
- H1: `Entrecôte`
- Tagline: `Persillée, tendre, vite cuite.`
- Big number: `2′30″` (prime U+2032, double prime U+2033)
- Under the big number (H2 52): `par face, pour une cuisson saignante.`
- Second line (body 36): `À point : 3′30″ par face.`
- Data line: `350~g` `·` `2,5~cm` `·` `1~personne`
- Heat gauge: 3 active flames → `FEU VIF`
- Rule (body 36, with a Lucide `check` icon in Rouge): `Retournez-la une seule fois, à la pince. Jamais à la fourchette.`
- Astuce du boucher: `Entaillez le gras du bord tous les 3~cm : elle ne se recroquevillera pas sur la grille.` (with `⍽:`)

### Slide 4 — Onglet (charcoal background)
- Kicker (Braise): `MORCEAU 03`
- H1 (Crème): `Onglet`
- Tagline (italic, Braise): `Le morceau du boucher.`
- Big text (Fraunces 900 96 / 1.0, Crème, 2 lines): `Un seul` / `par bête.`
- Body (Crème 36): `Longtemps, on le gardait pour nous. Maintenant, on vous le réserve.`
- Heat gauge (inactive flames stroked in `#5A504A`): 3 active flames → `FEU TRÈS VIF`
- Cooking (H2 52 Crème): `2~min par face, pas plus.`
- Body (Crème 36, 80 % opacity): `Bleu ou saignant, sinon il durcit.`
- Knife diagram caption (Barlow 700 UPPERCASE 28, Braise): `TRANCHEZ EN BIAIS, CONTRE LE FIL`
- Data line: `180 à 200~g par personne`
- Astuce du boucher (label in Braise, rule in Braise, text in Crème): `Des échalotes crues ciselées, de la fleur de sel. C’est tout.`

### Slide 5 — Porc & maison (split slide)
Top half:
- Kicker: `MORCEAU 04`
- H1 (Fraunces 900 **84**): `Poitrine de porc`
- Heat gauge: 2 active flames → `FEU MOYEN`
- Body: `Tranches de 1~cm, 4 à 5~min par face, jusqu’à ce qu’elle croustille.`
- Astuce (compact version, same style, text 34): `Le gras coule et ça flambe ? Décalez-la hors des braises 30~secondes.` (with `⍽?`)

Bottom half:
- Kicker: `MORCEAU 05`
- H1 (Fraunces 900 84): `Merguez *maison*` ← *maison* in 600 italic Rouge
- Sub (Barlow 600 30, Charbon 75 %): `Bœuf et agneau, nos épices, embossées chaque jeudi.`
- Heat gauge: 2 active flames → `FEU MOYEN`
- Body: `8 à 10~min, en les tournant souvent.`
- Astuce (compact): `Ne les piquez jamais : tout le jus reste dedans.` (with `⍽:`)

### Slide 6 — CTA (Rouge Dufour background)
- Kicker (Crème 80 %): `POUR SAMEDI ?`  → exact string `POUR SAMEDI&#8239;?`
- Title (Fraunces 900 104 / 1.0, Crème, 2 lines): `On vous prépare` / `tout ça.`
- Body (Barlow 500 38, Crème): `Commandez la veille, c’est prêt, ficelé et emballé à votre arrivée.`
- Label above the phone (Barlow 700 UPPERCASE 28, Crème 80 %): `COMMANDE LA VEILLE AU`
- Phone (Fraunces 900 112, Crème, tabular): `04 78 00 00 12` (the spaces are U+00A0 so it never breaks)
- Recap card (Papier background, 5 lines, Barlow 600 32 Charbon + a heat gauge reduced to 30 px icons, right-aligned):
  - `Côte de bœuf` — 3 flames
  - `Entrecôte` — 3 flames
  - `Onglet` — 3 flames
  - `Poitrine de porc` — 2 flames
  - `Merguez maison` — 2 flames
- Card title (Fraunces 700 40 Rouge): `Le récap’`
- Sign-off (Barlow 600 28 Crème): `Boucherie Dufour · Artisan boucher-charcutier`
- Hours (Barlow 500 28 Crème 80 %): `Du mardi au samedi · 7~h~30 – 12~h~30 et 15~h~30 – 19~h`
- Save prompt (Barlow 700 UPPERCASE 26, Crème, Lucide `bookmark` icon 30 px): `ENREGISTREZ CE GUIDE POUR LE PROCHAIN BARBECUE`
- Handle: `@boucheriedufour`

Proofread: côte (circumflex), bœuf (œ ligature), épaisseur, cœur, Persillée, recroquevillera, échalotes, ciselées, Décalez-la, embossées, récap’. No "n’hésitez pas". Every `:` `?` has a U+202F before it.

---

## 5. Slide-by-slide layouts

Coordinates are in px, origin top left of each 1080 × 1350 slide. Header and twine/tag as in section 3 on **every** slide (on slide 4, the header text and rule turn Crème at 60 %, the mini logo turns Crème; on slide 6, everything Crème; the twine keeps its colours everywhere, with Crème strands turning `#F7F1E6` and red strands turning Charbon on slide 6 so they stay visible on red).

### Slide 1 — Hook: « la planche de découpe »
- Background: Papier + grain + fibres + vignette.
- Kicker at x 72, y 196 (Rouge, kicker style).
- H0 title: top y 236, left 72, 3 lines, max width 936 (line-height 118 → bottom ≈ 590).
- Subtitle at y 620, width 760, Charbon 85 %.
- **Illustration "Charolaise + cochon"**, zone x 72–1008, y 700–1150:
  - **Charolaise** in profile facing left, silhouette 620 × 380 at x 72, y 730: filled Crème `#F7F1E6`, 4 px Charbon outline (a heavy, muscular beef body, short horns, long straight back, 4 legs). Internal cut boundaries in Charbon dotted lines. Three highlighted cuts, filled Rouge at 90 %, each with a circled number (Rouge circle Ø 44, Crème number Barlow 700 26): **1 côte** (front of the back, over the ribs), **2 entrecôte** (just behind it, same band), **3 onglet** (small zone under the belly, in the middle of the flank).
  - **Pig** in profile, smaller (300 × 190), at x 700, y 900, same style; **4 poitrine** highlighted in Rouge (lower belly).
  - **Merguez**: a chain of 4 sausages linked by small twisted knots, drawn in `#7E1820` with a 6 px Crème highlight on top, forming a loose arc under the pig, x 700–1000, y 1110–1160, with the circled number **5**.
- Numbered legend: not a separate list; the circled numbers sit on the illustration, and next to each number a Barlow 700 30 px label on a Papier pill (padding 6 × 12) with a 2 px Charbon leader line (short, ≤ 60 px) going outwards.
- **Stamp badge** "CHAROLAISE · MATURÉE SUR PLACE": Ø 220, centre (900, 330), rotated −12°, Rouge with ink texture, the Charolaise head in the middle. It overlaps the end of the title slightly without touching the letters (the title lines end before x 820 except "Le guide des morceaux", check the overlap; if it touches, move the stamp to centre (910, 610)).
- Swipe cue: bottom right, right-aligned to 1008, baseline y 1215.
- Twine + tag "01 / 06" at x 150.

### Slide 2 — Côte de bœuf: « la fiche complète »
- Kicker y 196, H1 at y 232 (1 line), tagline y 352 (italic 44, Charbon), data line y 426 (Barlow 700 40; values Charbon, separators Kraft).
- **Illustration**: a côte de bœuf seen from above, 520 × 440, top-right zone, centre (770, 330), rotated −8°, **overlapping the header rule** a little (top edge at y ≈ 120: that's intentional, it "sits" on the sheet). Shape: a thick rounded wedge of meat in Rouge with a Crème fat cap along the curved outer edge (18 px), a **long rib bone** coming out at the top-left (Crème, 60 × 200, rounded end, Kraft shading on one side), marbling (8 streaks), 4 grill marks. Drop shadow: `drop-shadow(0 18px 24px rgba(30,26,24,.22))`.
  → The title zone then runs x 72–560 for the tagline and data line (wrap if needed; the data line may run under the meat; if it collides, stack it into 2 lines).
- **Heat gauge** at x 72, y 520.
- **Steps + thermometer block**, y 600–960:
  - Left (x 72–760): 3 steps stacked, 100 px apart, each: a Rouge circle Ø 56 with a Crème number (Fraunces 900 32), label to the right (x 150) and body underneath. A Kraft dotted vertical line connects the 3 circles.
  - Right (x 830–1008): thermometer, top y 600; "À CŒUR" above it (kicker style), the value `52 °C` in Fraunces 900 72 Rouge **under** the thermometer, centred on x 900, y 930, and "= saignant" Barlow 500 30 under it.
- **Astuce du boucher**: x 72–1008, y 1010–1150 (Rouge rule 6 px on the left, content at x 100).
- Origin mention: y 1185, x 72.
- Twine + tag "02 / 06" at x 306.

### Slide 3 — Entrecôte: « le chiffre »
- Kicker y 196, H1 y 232, tagline y 352.
- **Big number** `2′30″`: Fraunces 900 250 Rouge, left 60 (optical alignment), baseline y 640.
- Under it, the H2 "par face, pour une cuisson saignante." at y 668, width 620; then "À point : 3′30″ par face." at y 800.
- **Illustration** of the entrecôte: an oblong steak in a slight "kidney" shape, 420 × 300, centre (800, 560), rotated +10°, meat Rouge, a Crème fat edge along the top (22 px) **with 3 small notches cut into it** (echoing the tip), a "noix" of fat in the centre (the eye of the entrecôte, a Crème blob of 50 × 36 with soft edges), heavy marbling, 4 grill marks, same drop shadow.
- Heat gauge x 72, y 880. Data line y 960.
- Rule with the check icon: y 1020, width 936.
- Astuce: y 1090–1215 (tighter: text 36).
- Twine + tag "03 / 06" at x 462.

### Slide 4 — Onglet: « le secret » (charcoal)
- Background Charbon + grain + 2 Braise glows. Header in Crème.
- Kicker (Braise) y 196, H1 (Crème) y 232, tagline (Braise italic) y 352.
- **Big text** "Un seul / par bête." Fraunces 900 96 Crème, x 72, y 440–640 (width ≤ 540).
- Body "Longtemps, on le gardait…" y 670, width 700.
- **Knife diagram** (the visual of the slide), zone x 72–1008, y 780–1000: the onglet drawn as a long, fibrous lozenge (720 × 170), meat Rouge, with **~22 fine parallel curved fibre lines** in `#7E1820` running along the length. A **Braise dotted knife line** (stroke 4, dasharray 2 10) crosses the fibres at −60° three times (three slices). A Lucide `slice` icon (Crème, 56 px) at the start of the first knife line. The caption "TRANCHEZ EN BIAIS, CONTRE LE FIL" under it at y 1010, centred on the diagram.
- Heat gauge + cooking line on the same row: gauge at x 72, y 1060; H2 "2 min par face, pas plus." at x 72, y 1110; body "Bleu ou saignant, sinon il durcit." y 1170 (Crème 80 %). The data line "180 à 200 g par personne" right-aligned at 1008, y 1060.
- **Astuce du boucher** on this slide: on the right, x 640–1008, y 420–650, next to "Un seul par bête", with a Braise rule (text 34 px to fit).
- Twine + tag "04 / 06" at x 618 (the twine reads well on charcoal: Crème strands dominate).

### Slide 5 — Poitrine & merguez: « le duo »
- Split in two horizontal halves divided by a **Kraft dotted rule** at y 700 (x 72–1008).
- **Top half** (y 170–680):
  - Illustration left: 2 slices of pork belly, laid side by side, each 170 × 330, rotated −6° and +4°, centred at (220, 450); alternate layers of Rouge-pink (use `#C4474F`, a slightly lighter shade for pork) and Crème fat (5 stripes), a golden rind edge at the top (`#B8742E`), grill marks.
  - Text right, x 420–1008: kicker y 196, H1 "Poitrine de porc" (84, 2 lines "Poitrine / de porc") y 226–400, heat gauge y 420, body y 490 (width 588), compact astuce y 590–680.
- **Bottom half** (y 720–1215), **mirrored**: text left, illustration right.
  - Text x 72–640: kicker y 740, H1 "Merguez maison" (84, 2 lines) y 770–940, sub y 955, heat gauge y 1010, body y 1075, compact astuce y 1130–1215.
  - Illustration right, centred at (860, 960): a **coil of merguez** in a spiral (3 turns, Ø 300), `#7E1820` with a 6 px Crème highlight along the top edge, held by two crossed wooden skewers (Kraft, 8 px), grill marks.
- Twine + tag "05 / 06" at x 774.

### Slide 6 — CTA: « le bon de commande » (Rouge)
- Background Rouge Dufour + grain. Header in Crème. **Big stamp logo** in Crème (Ø 300, ink texture) at centre (860, 330), rotated −10°.
- Kicker y 196 (x 72), title "On vous prépare / tout ça." y 232–440, body y 470 (width 700).
- Label y 610, **phone** y 650–770 (Fraunces 900 112 Crème). A 3 px Crème rule under it, from x 72 to the end of the phone.
- **Recap card** "Le récap’": Papier rectangle x 72–1008, y 820–1130, 4° corner radius, `box-shadow: 0 16px 30px rgba(30,26,24,.25)`, paper grain on it, rotated −1.5° (a slip of paper placed on the counter). Inside: title y +28, then 5 rows of 44 px separated by 1 px Kraft rules, name on the left (x +40), mini heat gauge on the right (right-aligned at −40).
- Sign-off y 1160, hours y 1198 (both x 72), save prompt + icon right-aligned to 1008 at y 1160, handle right-aligned y 1198 (Barlow 600 28 Crème).
- Twine + tag "06 / 06" at x 930: here the twine **ends in a knot** (a small figure-eight loop at x ≈ 1000) instead of going off-slide: the parcel is tied.

---

## 6. Motion notes
None: a static carousel. The only sense of "movement" comes from:
- the twine continuing from one slide to the next and the tag moving right (progress);
- the slight rotations of the illustrations, stamps and recap card (−12° to +10°), which avoid a stiff grid;
- the illustrations overlapping the header rule (slide 2) or the edges, for a "laid on the counter" feel.
No CSS animation, no JS-driven animation.

---

## 7. Technical approach hints
- `pieces/p222/index.html`, 6 `<section class="slide">` at 1080 × 1350, stacked. `window.KLIPT = { width: 1080, height: 1350 };`. Body `margin:0; overflow:hidden`.
- Fonts: `<link>` to `../../node_modules/@fontsource/fraunces/{index,700,900,600-italic}.css` and `../../node_modules/@fontsource/barlow-condensed/{500,600,700}.css`. Use `font-variant-numeric: tabular-nums` on the phone and the big numbers; `font-variation-settings` is not needed.
- **A hidden `<svg>` with `<defs>` at the top of the body**: `<symbol id="logo-head">` (Charolaise head), `<symbol id="flame">` (Lucide `flame` path inlined), `<filter id="grain">`, `<filter id="fibres">`, `<filter id="ink">` (turbulence + displacement 2 px + alpha threshold for the stamp), `<pattern>` or 2 stacked strokes for the twine. Reuse via `<use href="#…">`.
- **Twine**: an absolutely positioned SVG per slide (1080 × 60 at y 1232) with the same path `M0 30 Q540 44 1080 30`; stroke 1 = Crème 10 px; stroke 2 = Rouge 10 px `stroke-dasharray="9 9"`; stroke 3 = a thin 1 px Charbon at 25 % offset 4 px under (shadow). Identical on every slide so the join between slides is perfect (except slide 6, which ends in a knot).
- **Grain**: one absolutely positioned div per slide `::after` with an inline SVG data-URI of the turbulence filter (encoded, no external URL) or an inline `<svg>` with `<rect filter="url(#grain)">`. Seeds fixed → deterministic.
- Cut illustrations: hand-written paths (cubic Bézier), grill marks via `<clipPath>` = meat shape. Marbling: 6–10 short curved paths, stroke Crème 3–7 px, opacity 0.4–0.7, fixed coordinates (or generated once with `KK.rng(222)` at load, never `Math.random()`).
- Circular text of the stamp: `<textPath>` on a circle path; check that the text fills the circle exactly (adjust `textLength`).
- Icons: Lucide `flame`, `arrow-right`, `check`, `slice`, `bookmark`: read the SVG from `../../node_modules/lucide-static/icons/` and inline it (stroke-width 2.5).
- French typography: write U+202F and U+00A0 as entities (`&#8239;`, `&nbsp;`), check with a search in the rendered text that no ` :`/` ?` with an ordinary space remains.
- Check with `node tools/render.mjs stills pieces/p222`: no text under 30 px (except the tag number 28 and the header 26, which are labels), no collision between the illustration and the text on slides 2 and 3, twine perfectly aligned between adjacent slides in `sheet.jpg`.
- `meta.json`: kind `carousel`, format `1080x1350`, slides 6, fonts `["Fraunces","Barlow Condensed"]`, palette `["#EFE6D6","#1E1A18","#A3202A","#E8792B","#C9B79A"]`, techniques `["svg-illustration","svg-filters","css-layout","textPath"]`.

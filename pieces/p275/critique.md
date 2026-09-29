# Critique — p275 · Atelier Mèche · Post 1080×1080 « Balayages −20 % en novembre »

## Verdict : 6.5 / 10

It works as a real salon post. The palette (crème / brun / terracotta / miel) fits the sector, Gloock gives an editorial serif feel, the arch with its gradient strands has personality, and "−20 %" reads in under a second. The focal zone is poorly built, though. The minus sign breaks away from the number, "20" collides with the arch, the "%" drowns in the hair, and the illustration looks more like a curtain or wood slats than a balayage. The copy stays generic: no dates, and "sur…" is repeated. Fix these and the piece can reach 8.

## Fixes, by priority

1. **"−20 %" is broken apart and collides with the arch (top issue).**
   - The minus sign (U+2212 in Gloock) renders as a thin 100 px rule at x≈35–130, set far from the "2". It reads as an em dash ("— 20"), not as "moins 20".
   - The "0" ends at x≈500 and touches the arch outline, which is offset (`translate(-16 16)`) to x≈504. The "%" (150 px) sits across the outline and on the honey hair: terracotta #B4533A on miel #D8A25E is about 2:1 contrast.
   - Fix: bring the whole group back into the left column. `.big{left:64px; top:585px; font-size:250px; letter-spacing:-.03em}`. Replace `−` with a hyphen `-` in Figtree 700 (or draw an 80×18 px terracotta bar placed at mid-height of the digits, 12 px from the "2"). Set `.big span{font-size:120px; margin-left:6px}` so "%" ends at x ≤ 470. Keep at least 30 px of cream between the text and the arch outline.

2. **The headline also touches the arch.** "Le balayage" at 84 px runs to x≈500, overflowing its declared width of 440 px, and nearly touches the outline at x≈504. Set `h1{font-size:76px; width:420px}` or move the arch right (`ax=560, aw=440`). The goal is ≥ 32 px of air between the text column and the arch.

3. **The illustration does not read as a "balayage".** Seventy nearly vertical, parallel strands with a single top-to-bottom gradient give an **ombré** or a curtain / wood-slat look. A balayage means **light strands painted from mid-length**, with some dark ones kept.
   - Give the strands more curve and a bit of fall: `w=(r()-.5)*160`, and a stronger control point `x0+w*2.2` at `ay+ah*.35`.
   - Alternate two gradients: dark strands (#2A1A13 → #5A3220) and lightened strands (#5A3220 at 30 % → #EBC98A at 70 %). Roughly 1 lightened strand for every 3.
   - Replace the 9 identical sheen strokes with 5–6 wider ribbons (`stroke-width` 10–16, #F6DDA6, opacity .6), painted from `ay+ah*.3` down. That creates the "hand-painted" effect.

4. **Missing or vague offer details.** "Novembre" alone does not state the validity period. Change the kicker to `DU 1ᴱᴿ AU 30 NOVEMBRE` (or `Tout novembre`). In `.cond`, fix the repeated "sur… / sur…" and the lowercase start. Replace it with `<b>Sur tous les balayages.</b><br>Uniquement sur rendez-vous.`. "couleurs naturelles" is already in the seal, so drop it from here, or keep it once as brand proof: `Couleurs naturelles, sans ammoniaque.`.

5. **Generic headline.** "Le balayage qui vous ressemble." could come from any salon. Tie it to the specialty: `Un balayage qui a l’air naturel.` or `La lumière, sans l’effet mèches.`. Keep 3 lines maximum at 76 px and use `’` (curly apostrophe).

6. **Seal: text too small and redundant.** The ring text is 15 px (≈5 px on a phone thumbnail), so it can't be read, and "NANCY" is already under the logo. Set `font-size` to 18, `textLength` to the real circumference (2π·58 ≈ 364) so the start and end don't collide, and change the text to `COULEURS NATURELLES · SUR RDV · `. The centre "RDV" becomes redundant, so replace it with "−20 %" in Gloock 40 px, or with the brand pictogram. Or remove the seal altogether if item 1 already makes the offer strong enough.

7. **CTA / footer.** "Réservez au 03 83 27 41 60" is good. Add a second, more Instagram-native action on the right: `Réservation en DM · @ateliermeche`. Numbers: use narrow non-breaking spaces (U+202F) in the phone number so it never splits across lines.

8. **Palette: dead code / unused colour.** Sage #7F8C6C is declared in the direction but only used by a rect at `opacity:.0`. Either remove it from the palette, or use it sparingly: a 3 px sage line under the kicker, or the offset arch outline in sage instead of brown. That lightens the heavy frame, which currently competes with the headline.

## What already works (keep)
- Logo mark (drop of hair in a brown circle) plus the Gloock wordmark: clean and reusable.
- Paper grain at a fair level, dark footer as a solid base, good hierarchy: kicker → headline → number → conditions → contact.
- Correct French typography overall ("−20 %" spacing, accents).

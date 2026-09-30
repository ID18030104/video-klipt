# Critique — p236 · Shala Yoga Annecy · « Réveil en douceur » (carrousel 6 × 1080×1350)

## Verdict : 7 / 10

A calm, coherent system that fits the brand: dawn arch + lake band, Fraunces/Figtree, restrained palette, grain, consistent header/footer and progress dots. Each slide gives posture + cue + breath + duration, which is exactly what the brief asks for. What keeps it out of the library as-is: two of the five pose illustrations don't read as the named posture (and these drawings *are* the content), the wave band has a visible rendering notch on every posture slide, the cover's swipe arrow is buried under the pill, and the CTA slide is a squeezed footer rather than a real close. Copy is clean (correct ’, accents, "7h15", "·"), no typos found.

## Fixes, by priority

1. **Redraw the Chat-vache figure (slide 02) so it reads as a person on all fours.** Right now the head (`head(120,205)`) floats ~40 px left of the body with no neck, and the body reads as a table or an "M". Connect the head to the spine with a neck: move the head to `cx=165, cy=230` and add `<path d="M190 222 L160 236">` in the same `${S}` stroke. Drop the `)` "sound waves" at `M600 190…/M616 172…`, since they mean nothing here. Keep the dashed arc (cow/cat), but make it apricot `#E8825A`, 8 px wide, so it looks like a breath/motion cue and not like a broken line.

2. **Redraw the Torsion assise figure (slide 05).** The vertical spine + horizontal shoulder bar + orange arm makes a cross/anchor on a boat, not a seated twist. Rotate the shoulder line about 20° (`M250 200 L355 170`), plant one hand behind on the mat (`M250 200 Q215 300 235 380`), bring the other arm across onto the opposite knee, and show one bent knee raised above the legs (a peak at about `300,330`). Remove the orange diagonal. It currently looks like a sash.

3. **Fix the notch in the wave band (slides 02–06, x ≈ 998–1010, y ≈ 590–612).** The waves SVG is 940 wide, but its wave pattern (16 × 58 = 928 px) stops short, so the teal water shows up as a square step at the right edge. Extend the path to 986 px (`…58 0 58 0` → add one more `t58 0`), or use `viewBox="0 0 928 40"` with `preserveAspectRatio="none"` and `width="100%"`.

4. **Cover (slide 01): un-bury the swipe cue.** The `.foot` arrow (right: 70px, bottom: 44px) sits under the `.pill` (top: 1235px), so only a stray tip sticks out at about (995, 1297). Remove the empty `.foot` from the cover and put the arrow inside the pill: « Glissez pour la routine → », with `display:flex; gap:12px`. Also stop the front mountain (`#2F5D62` at `opacity .55`) from muddying the sun into olive at (700–950, 970–1100). Draw the sun *behind* both ridges with no transparency on the ridge (use a solid `#284C50` for the back ridge) so the sun reads clean yellow and rises from behind the mountains.

5. **Give the CTA a real close (slide 06).** The band (170 px, no verb) reads like a footer, and slide 06 is cramped: the h2 bottom (≈ 890) sits 16 px from `.desc` (906). Options, best first:
   - Keep 6 slides but raise the CTA band to 230 px with an action line: small caps « COURS DU MATIN · BORD DU LAC », title « Rejoignez-nous à 7h15 », and the button « Réserver → shala-annecy.fr ». Reduce the posture block on this slide (h2 84px, `.desc` top 890, chips top 990, chip min-height 100) so it fits with ≥ 28 px between blocks.
   - Add a concrete hook to the button line, e.g. « 1er cours offert » or « Tous les jours sauf dimanche ». "Tous les jours, 7h15" is fine if it's true. Check it with the studio, because the brief says only "cours du matin 7h15".

6. **Make the "sun rises" continuity visible.** The sun's `top` only moves from 300 to 212 px across the 5 slides (−22 px per slide), so it barely changes. Use `top: ${330 - i*55}px` (330 → 110), so on slide 06 the full disc clears the water, and warm the arch gradient slightly per slide, e.g. interpolate the top stop from `#F8D9A6` to `#FBE7C4`. That turns the concept in meta.json into something the viewer actually sees.

7. **Tighten the breath copy on slide 03.** « Longues, par le nez. » has no noun and reads as a fragment. Use « Inspirez et expirez par le nez, lentement. » to match the imperative pattern of the other slides. Optionally make slide 06 « 6 longues expirations par la bouche. » so it is concrete.

8. **Small-type legibility.** Chip labels (`.chip span`, 22 px at opacity .75) and the logo subline « YOGA ANNECY » (20 px at opacity .7) are under the 30 px floor and fade at phone size. Raise `.chip span` to 24 px at opacity .9 and `.logo small` to 22 px at opacity .85. Also vertically center the Durée chip text with the two-line Respiration chip. It already is, but give both chips a fixed `min-height:128px` so the pair looks equal on slides 03 and 06, where the Respiration text is one line.

## What works (keep)
- The palette and type pairing are warm, premium and unmistakably "morning yoga by the lake". The italic « en douceur » in sun yellow is a strong hook.
- The system is consistent: `0X/06` counter, "POSTURE N SUR 5" kicker, the arch, two chips, and progress dots.
- Real information density: position, breath and duration on every posture slide. The five durations add up to about 5 min, consistent with the cover promise « 5 minutes, un tapis ».

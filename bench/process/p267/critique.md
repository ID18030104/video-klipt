# Critique p267 : Auto-École Feu Vert (vidéo 9:16, 22 s)

**Verdict : 7/10.** The idea is right for the brief and for this brand. It is a top-down illustrated road, the traffic light goes from red to green on "coup ?", then the car drives under road gantries that carry the proof, and it parks at the agency. The palette is disciplined and the gantry signs read at thumbnail size. The French typography is clean: non-breaking spaces in "87 %", "1 290 €" and "coup ?", and the maths checks out (4 × 322,50 € = 1 290 €).

It is not ready for the library. One sign has a collision between two elements, the end card is not held long enough, the end card has a visible seam, and the parking payoff is cluttered. None of these is a structural problem. Each is a quick fix.

Frames checked: sheet, poster, t = 0.5 / 5.2 / 9.2 / 16.8 / 18.3 / 21.5 s.

## Fixes, by priority

1. **The "A" badge covers "ans" on the conduite accompagnée sign (t ≈ 8–11 s).**
   `#abadge` (right:64px, top:34px, 180×180) lands on top of the final "s" of "dès 15 ans", which is 176 px wide. The main claim of that beat reads "dès 15 an". Pick one of these:
   - move the badge to `top:-40px; right:40px; width:150px; height:150px; font-size:124px` so it hangs off the top-right corner of the sign like a sticker;
   - or reduce "dès 15 ans" to `font-size:150px`, which keeps the text under about 690 px and stops it before x = 756.

2. **The end card is held for only about 1.4 s.**
   `#e5` finishes entering at 20.6 s and the video stops at 22 s. The skill asks for at least 2.5 s. Pick one of these:
   - set `duration:23.5` in `window.KLIPT` and stretch the `#end` scale tween to `duration:4.3`;
   - or bring the end card sequence forward by 0.8 s: `#sw` at 17.55 / 18.05, `#e1`–`#e5` at 18.35 → 19.1.

   Either way the CTA block should be fully readable from about 19.8 s to the end.

3. **A vertical line runs through the middle of the end card.**
   The first overlay in `#end` (`repeating-linear-gradient(90deg, transparent 0 538px, rgba(255,255,255,.07) 538px 542px)`) draws a 4 px line at x = 540. It cuts through "AUTO-ÉCOLE · TOULOUSE", the tagline, the CTA, the phone number and the chips (see the 21.5 s frame), and it looks like a render seam. Pick one of these:
   - delete the overlay;
   - or turn it into a real road marking: a centred dashed lane line at x = 1000, `opacity:.12`, so it sits outside the text column.

4. **The parking payoff is cluttered and weak (16.6–18.3 s).**
   - **The yellow sign stays in frame.** The half-visible "1 290 €" sign is still in the bottom 380 px unsafe zone (y ≈ 1640–1920) while the car parks. Stop the scroll so it has left the frame: extend the cruise, for example `if(t<17.2)` with a braking window of 1.2 s. You could also fade `#g3` to `opacity:0` from 16.4 s.
   - **The agency rooftop text is cut off.** The agency block (`left:850px; width:260px`) spills 30 px past the right edge, and the pink building above covers the "RT" of the "FEU VERT" rooftop text. Use `left:846px; width:230px`, and exclude buildings on the right side for `d0 + h > 4780 && d0 < 6150` instead of `< 6000`.
   - **The confetti is too thin.** It is 44 small pieces with no focal point. Raise it to 80 pieces, and add a small green "Garé·e ✓" or "Permis en poche" pill (48 px, Figtree 800) that pops above the parked car at 17.9 s. The story needs a punchline before the wipe.

5. **An empty green panel sits at the top of the hook frame (0–2.5 s).**
   The back of gantry g1 (y ≈ 0–145) shows a blank green rectangle above the brand pill, and the blank rectangle reads as a mistake. Pick one of these:
   - start g1 further up, for example `TP[0] = 7.3`;
   - or show nothing on that part of the road until 2.5 s: `gsap.set('#g1', {autoAlpha:0})`, then an `autoAlpha:1` tween at 2.6 s.

6. **The 87 % sign shows "0 %" as a static number before the count starts.**
   The sign enters the top of the frame around 3.8 s, but the counter only starts at 4.6 s (`TP[0]-2.3`), so "0 %" is readable for about 0.8 s (sheet frame 3). A viewer sees "0 % de réussite". Pick one of these:
   - start the count when the sign enters: `KK.prog(t, TP[0]-3.1, 1.3)`;
   - or render "—" until the count begins.

7. **"plus." sits alone on the second line of the conduite accompagnée sign.**
   "Tes parents à côté, la confiance en plus." breaks with "plus." by itself. Pick one of these:
   - use a `&nbsp;` between "en" and "plus", and set `font-size:50px`;
   - or rewrite the line to "Tes parents à côté, zéro stress." so it fits on one line at 54 px.

8. **Small polish points:**
   - The rooftop "A" sticker on the car gets scrambled when the car rotates to park (18.3 s). Give the `<text>` the attribute `text-rendering="geometricPrecision"`, or use a path glyph.
   - On the end card, the lower 30 % of the frame (y 1580–1920) is empty navy. Move `#e1`–`#e5` down by about 80 px, or put a small top-down car on a dashed lane at y ≈ 1700 so the illustrated world carries into the end card.

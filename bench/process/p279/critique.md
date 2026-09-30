# p279 — Nomad Cycles, "Who gets to school first?" (1080×1920, 24 s)

## Verdict: 7.5 / 10

This is a strong idea and it's well built. The map race is exactly what the brief's angle asked for. The palette (cream, ink, bike-lane green, Nomad orange) feels like it belongs to this brand. The dual timer cards make the claim easy to follow, and the copy reads as native English ("Arrived. Coffee time.", "Parked. Late."). The numbers are consistent: bike 19:04, car 32:08, a 13:04 gap, and the clock runs 8:00 to 8:33.

It is held back by these problems:
- The payoff line is on screen too briefly.
- Labels cover the hero vehicle and the route.
- The car's arrival can't be seen.
- One pill is out of the safe zone.
- The product/price beat goes by too fast to read.

I found no typos. US spelling and "$" placement are correct throughout.

## Fixes, in priority order

1. **The payoff "13 min faster." is on screen too briefly.** It pops in at 14.75 s, starts fading at 16.05 s, and the orange wipe covers it from 15.9 s. That leaves about 1.1 s at full opacity for the single most important line.
   - Move `#sticker2` in to **14.6 s** and its exit to **16.9 s**.
   - Shift the wipe/product/end-card block by **+0.8 s**: wipe at 16.7, `#prod` at 16.9, `#end` at 21.15. The duration stays 24 s, because fix 5 recovers the time.
   - Make it the loudest sticker: font-size **112px**, and add a second line "Every school day." at 40px mono.

2. **The car's arrival can't be seen.** `#carV` ends at (902,620), directly under `#bikeV`. In the 15.2–16 s frames there is no car on the map at all, just a grey line ending at the bike, so the "Circling for parking" moment is lost.
   - At TB (10.4 s), move the bike to a parked spot: `translate(960,700)`, then tween it there over 0.4 s.
   - Or end the car path at `L902,660` and draw the car with a lower z-order, offset 70px.

3. **The "Green lane. No queue." pill (5.1–8.6 s) covers the green bike marker.** At 7.5 s the bike sits at about (610,800) and the pill (left 214, top 800) hides half of the hero.
   - Move it to **left:96px; top:700px**, above the route and clear of the bike's path.
   - Or attach it to the bike: set x/y in `renderMap` to bike.x−200, bike.y−110.

4. **"Parking hunt" breaks the side safe zone and sits on the car route.** Its box is at left 790 and ends at about x=1062, where the limit is ≤1010. It also sits on top of the vertical car line at x=780.
   - Use **left:560px; top:660px**, to the left of the x=780 line, or right-align it at `right:70px; top:720px`.
   - Its 1.45 s hold (14.55→16.0) is fine once fix 1 lands.

5. **The product beat is too dense for its 4.2 s.**
   - The chips are each visible only about 1.0–1.6 s (ch3 enters at 17.8 s and leaves at 18.85 s).
   - The price box is visible 19.0→20.35 s, which is 1.35 s for "$4,290 or $99/month lease". It needs at least 2.8 s.
   - Keep the chips and the price on screen together:
     - chips at top 1180/1280/1380 → **1140/1230/1320** at 46px,
     - `#priceBox` at **top:1450**,
     - no chip exit.
   - Stagger the entrances: chips from 17.4 s, price at 18.4 s. Hold everything until the wipe.
   - Also cut the eyebrow "NOMAD CARGO" or replace it with the model name ("NOMAD HAULER · E-CARGO"). "Nomad Cargo" reads like a placeholder.

6. **"Bridge backup" covers the start of the jam** (left 64, top 1112). At 6.3–13.4 s it sits over the home→bridge road and the first jam cars, which are the thing it labels.
   - Move it below the queue to **left:230px; top:1236px**, which is under the lower lane of jam cars (y≈1222) and above the cards (1322).
   - Also: the Home marker and pill are covered by the "Bike's already there." sticker (10.65–13.0 s) and read as "Hor". Lift `#sticker` to **top:760px**.

7. **The bottom 360 px (y 1560–1920) is dead cream for 16 s**, and the cards reach y 1558, just inside the 380 px bottom UI zone (limit 1540).
   - Raise the cards to **top:1296px**. Keep the empty band as the platform-UI zone.
   - Continue the map fade lower: `#fadeBot` top **1360px**, so the map doesn't end in a flat block right under the cards.

8. **The hook frame is static apart from the headline.** At 0.5 s we see only the title, one orange home pin and empty white roads.
   - Draw the two ghost routes from **0.0 s**, not 0.4/0.6.
   - Pop the School pin at **0.5 s**, not 1.2, so the "race" (two routes, two endpoints) reads within the first second.
   - Optional: slide "Two kids. Zero traffic." up to "Two kids. One bag of groceries. Zero jams." "Zero traffic" is a slight overclaim, since the bike still shares streets.

## Keep as-is
- The timers running at the same speed, and the red and green status lines.
- The 3.65 s end-card hold and its hierarchy (logo → "Free test ride in store." → URL pill → address/hours/price).
- The grain texture, the line-drawn cargo bike with the two kids and the groceries, and the orange wipe transition.

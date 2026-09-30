# Critique p289 — Garage Moreau, pneus hiver (1080×1920, 15 s)

**Verdict : 6/10.** The direction works for a local garage: asphalt and safety-yellow, Anton, a tyre rolling through snow, a big phone number. But the hook contradicts itself and says something wrong ("1 JOURS avant le 1er novembre"). The legal claim is inaccurate. The logo disappears on the yellow scene. The offer's hierarchy is backwards. None of this can go out as is.

## Fixes, highest impact first

1. **The countdown says something false and has a grammar error (0–3.3 s).** The number drops from 10 to 1 in 3 s (one step every 0.3 s) while the label "jours avant le 1er novembre" stays fixed. It lands on **"1 JOURS"**, which is wrong in French and wrong as a fact (the post goes out around J-10). At t = 2.9 s the frame reads "1 / JOURS AVANT LE 1ER NOVEMBRE".
   → Fix in `render()`: count **31 → 10** from 0 to 1.6 s (step 0.08 s, easing out), then **lock on "10"** from 1.6 s to 3.35 s with a single 1 → 1.04 pulse. If the number must be allowed to reach 1, switch the label to the singular: `n===1 ? 'jour' : 'jours'`. Another option is to show "J-10" in the chip in place of "Compte à rebours", which is redundant.

2. **The legal claim is inaccurate.** "Pneus hiver obligatoires" is wrong: the Loi Montagne requires *either* winter tyres *or* snow chains/socks, and only in the listed communes (Puy-de-Dôme included). The brief itself says "équipement obligatoire".
   → Replace the `#h2` lines with: "En montagne," / "dès le 1er novembre," / "**équipement hiver**" / "obligatoire." Add underneath, at 38 px Barlow 500, `color: var(--ice)`, top 820 px: "Pneus hiver ou chaînes · communes classées zone montagne".

3. **"1ER" is shown in capitals in every title.** `text-transform: uppercase` on `.a` and on `#s1lbl` turns the superscript into "ER" (visible in scene 1, in the `#h2` headline and in "1ER NOV." in `#bar`). French typography needs a lowercase superscript ("1er").
   → Add `sup{text-transform:none;font-size:.45em;vertical-align:.8em}` and remove the inline `style` attributes on the `<sup>` tags so they stay consistent.

4. **The logo vanishes on the yellow scene (8.55–12.3 s).** The yellow shield sits on a yellow background, so only a stray "GM" is left floating at 236 px. That is the scene where brand presence matters most.
   → In `render()`, when `t>8.3&&t<12.3`: shield `path` → `fill:#10161d`, `text` → `fill:#ffc21a` (give them ids `#lgShield` and `#lgTxt`). Colour the wordmark the same way (already `#10161d`).

5. **The offer's hierarchy is backwards (scene 3).** The condition "4 PNEUS ACHETÉS," is the biggest text at 190 px, and the benefit "montage + équilibrage" is at 82 px. The only thing anyone remembers is "offerts". The "OFFERTS" stamp at left 560 / top 790 also sits 20 px from the "ACHETÉS," comma, and the two crowd each other.
   → Reorder: `#s3t` = "Montage +" / "équilibrage" at **150 px** (line-height 150, top 430). Stamp "OFFERTS" at **left 70, top 760**, rotate −5°, 440×170. Then "pour 4 pneus achetés" at **64 px** Anton, top 980. Move `#rows` down to top 1120 (it still ends before 1540, the bottom safe zone).

6. **The end card is too short, and the offer and hook are missing from it.** The last line ("Offre du 1er…") appears at 13.6 s, leaving 1.4 s to read 8 words (the target is ≥ 4 s). The "er" superscript is 24 px (44 × 0.55), under the 30 px minimum. There is an empty gap from 760 to 1000 px. The line "Offre du 1er novembre au 31 mars" also mixes up the obligation period with the offer period.
   → Take the duration to **16 s** (the brief allows 14–16). Move the sweep to 12.05 s and the end card to 12.3–16 s. Put a reminder chip at top 850: "Montage + équilibrage offerts" (40 px, red background `#e2402a`, cream text). Replace the last line with "Clermont-Ferrand · toutes marques" (the "Toutes marques" under the logo then goes). Show the full CTA by 13.4 s at the latest.

7. **Snow on the yellow scene.** The flakes turn `#ffffff` between 8.55 and 12.65 s, so white dots at 55–90 % alpha pepper the yellow and read as dirt on the text ("4 PNEUS", "gratuit").
   → On scene 3, drop to `globalAlpha = .18 + f.z/40` and draw only 1 flake in 3 (`i%3===0`). Alternatively, use `#fff8e0` at low opacity.

8. **Scene 2: the tyre rolls in the empty lower half and the track reads as a pavement.** The ice strip at 1240–1370 px floats over the dark background, and the space from 1560 to 1920 px is empty (acceptable for the safe zone, but the scene feels unbalanced). The tyre's sidewall snowflake (the 3PMSF symbol) is barely visible at 7 px wide.
   → Extend `#ground` to height 680 (down to the bottom of the frame) with a gradient `#eef6fa → #9fb8c6`, and put `#bar` on it with dark text. Or: stroke-width 10 on the snowflake, plus a "3PMSF"-style mountain pictogram.

## What works (keep)
Solid palette and type that fit a local garage register. Sweep transitions in yellow, ice and ink. The tyre illustration with its rotation matched to travel. The yellow phone number block at 110 px is very readable. Grain is present, and the logo stays visible from 0.2 s.

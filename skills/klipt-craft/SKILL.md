---
name: klipt-craft
description: Art direction and production craft for Klipt social content (short videos 10–30 s, carousels, posts, stories) built as code. Use before designing any Klipt piece, together with docs/RENDER_CONTRACT.md.
---

# Klipt craft — making social content a client would pay for

Klipt makes social content for every kind of business: SaaS, SMEs, local shops, restaurants, hairdressers, craftsmen, luxury brands. The bar: **a piece a real brand would post today without edits.** Not a demo of animation tricks, not a template with the name swapped in.

Work in this order: **understand → direct → write → build → review → polish.** Most weak pieces skip "direct" and "review".

## 1. Understand the brand (2 minutes, in your head)
Answer before touching code:
- **Who scrolls past this?** (age, context, what they care about — a 55-year-old homeowner ≠ a 28-year-old product manager ≠ a 19-year-old sneakerhead)
- **The one thing** the viewer must remember. One. Not three.
- **Register**: premium / friendly / expert / playful / raw / institutional / artisanal / techy. The register drives every visual decision.
- **Platform**: Reels/TikTok (fast hook, bold type, vertical), LinkedIn (clarity, credibility, less noise), Instagram feed (aesthetic consistency), Stories (ephemeral, direct, CTA).

## 2. Direct — pick an art direction that could only belong to this brand
Write down (in a comment at the top of `index.html`) a 5-line direction: **concept, palette (3–5 hex), type pairing, graphic language, motion personality.**

Registers → starting points (then push past the cliché):
| Register | Palette | Type | Graphic language | Motion |
|---|---|---|---|---|
| B2B SaaS, trustworthy | 1 deep neutral + 1 saturated accent, lots of white/near-black | Inter/Manrope/Figtree/Sora; mono for numbers | Real-looking UI mock-ups, data, cursor, clean grid | Precise, snappy (`power3/expo.out`), UI micro-interactions |
| SaaS, bold/challenger | Loud duotone, neon on black | Unbounded, Syne, Space Grotesk | Oversized type, geometric blocks | Fast cuts, kinetic type |
| Local craftsman / SME | Warm, sturdy (navy, ochre, brick, cream) | Archivo Black / Oswald / Zilla Slab + readable sans | Pictograms, tools illustrated, badges, "since 1987" | Solid, readable, no gimmicks; generous hold times |
| Hairdresser / barber / beauty | Brand-dependent: barber = black/cream/brass; salon = blush/terracotta/sage | Serif display (DM Serif, Gloock, Instrument Serif) or retro script (Lobster/Pacifico) sparingly | Scissors/comb line art, arches, textures, before/after | Elegant reveals, masks, sweeps |
| Restaurant / food | Appetite colors (tomato, saffron, olive, cream); avoid blue | Fraunces, Young Serif, Shrikhand, Caveat for handwritten | Menu layouts, illustrated ingredients, stamps, paper texture | Warm, bouncy but not childish |
| Luxury / premium | Restraint: ivory, black, one metal (gold/bronze), or deep jewel tone | Bodoni Moda, Cormorant, Playfair (thin/italic), wide letter-spacing caps | Negative space, fine rules, 3D product with soft light | Slow, confident; long holds, subtle parallax |
| Youth / streetwear / events | High contrast, acid/neon, stickers | Anton, Bebas, Dela Gothic, Rubik Mono, Permanent Marker | Collage, tape, halftone, distortion, marquee | Aggressive: smash cuts, shakes, strobe (tasteful) |
| Health / care / public | Calm (teal, soft green, sky), high legibility | Nunito, Figtree, Work Sans | Friendly icons, rounded shapes, reassurance cues | Gentle, clear, never frantic |

Rules:
- **Max 2 typefaces** (+ a mono for data if needed). Establish a clear scale (e.g., 180 / 96 / 48 / 32 px on a 1080-wide canvas). **Never body text under 30 px** on 1080 wide (it's read on a phone).
- **Palette discipline**: one dominant, one secondary, one accent used rarely. Check contrast (text ≥ 4.5:1).
- **Give it texture** so it doesn't look like a flat template: SVG `feTurbulence` grain at 4–8 % opacity, subtle gradient mesh, paper, halftone, noise, soft shadows, light leaks — chosen to fit the register.
- **Invent a brand mark**: a simple logo (wordmark + symbol built in SVG) and reuse it consistently.

## 3. Write the copy (French unless told otherwise; English when the brief says so)
- **Hook in the first 1.0 s** (video) / first slide (carousel): a question, a bold claim, a number, a tension. Not the brand name.
- Short lines. Spoken French, concrete, specific numbers ("-37 % de temps de relance", "Ouvert dès 7h"), no corporate filler ("solutions innovantes", "n'hésitez pas").
- **French typography**: non-breaking space before `! ? : ;` and inside « guillemets » (use `&nbsp;` or U+202F), `’` not `'`, accents on capitals (É, À), "1 500 €" with a space. Proofread every string — a typo kills the piece.
- **English copy** (when the brief asks for it): native, idiomatic marketing English — not translated French. Pick US or UK spelling to match the market and stay consistent (color/colour, center/centre); curly quotes “ ” and apostrophes ’; sentence case for most headlines; currency before the number ($48, £15.50, €42); en dash for ranges (9am–7pm).
- End with a **clear CTA** + brand (handle, URL, address, phone — invented but plausible, e.g. `ledgerly.io`, `06 12 34 56 78`).

## 4. Build — video
**Structure a 15–25 s video like a story:**
1. **Hook** (0–1.5 s): motion from frame 0 — never start on an empty or static screen.
2. **Development** (3–4 beats of 3–5 s): one idea per beat, each with its own composition.
3. **Payoff / proof** (number, result, product, testimonial).
4. **End card** (2.5–3.5 s): logo, CTA, contact — held still long enough to read.

**Reading time**: hold any text ≥ 0.4 s per word + 0.8 s. If the viewer can't read it, it doesn't exist.

**Motion principles**
- Everything eases (`power3.out`/`expo.out` for entrances, `power2.in` for exits, `inOut` for moves). No linear motion except continuous drifts.
- **Stagger** related elements (0.04–0.12 s). Animate words/lines with masks (text sliding up from behind a clipping container) rather than plain fades.
- **Transitions carry energy between beats**: wipes, mask reveals, zoom-throughs, shape morphs, match cuts, a color block sweeping across. Avoid "fade to black, fade in" repeated.
- **Keep something alive** during holds: slow drift, parallax, grain, a subtle scale (1 → 1.04).
- Vary rhythm: fast–fast–slow. The end card is calm.
- **Safe zones for 9:16**: keep key text out of the top 220 px and bottom 380 px (platform UI), and 70 px from the sides.

**Format ideas beyond "motion design"** (choose what serves the brand):
- Product UI demo: a believable app screen (real-looking data, names, dates in French), animated cursor, clicks, zoom on the key feature.
- Chat/SMS/DM story: a conversation that tells the benefit.
- 3D product hero (three.js, `RoomEnvironment` + PBR materials, soft rim light, slow orbit).
- Illustrated scene (SVG) drawn line by line (`DrawSVGPlugin`), isometric shop front, map/route animation.
- Data story: one striking number counting up, a chart that builds itself.
- Before/after split with a sweeping divider; listicle "3 raisons de…"; countdown/event teaser; testimonial with quote typography; recruitment ad; menu of the day; kinetic manifesto; retro/pixel ad; paper cut-out collage.

## 5. Build — carousels & posts
- **Carousel (5–8 slides, 1080×1350)**: slide 1 = hook (big promise, max 8 words) + swipe cue; middle slides = one idea each, same grid and header/footer system, numbered ("02/07"); last slide = recap or CTA + brand. **Consistency across slides + variety inside the grid** (alternate a big-number slide, an illustration slide, a checklist…).
- Build **visual continuity** across the swipe: an element that crosses from one slide to the next, a continuous line, a progress indicator.
- **Single post**: one idea, one focal point, readable in 1 second at thumbnail size. Test: would it stop the scroll?
- Real information density: carousels should teach or prove something concrete (tips, numbers, steps, prices, schedules).

## 6. Review — look at your own frames like a demanding art director
After a preview render, **open `sheet.jpg`** (and 2–4 single frames at key moments). Check honestly:
- [ ] Does frame 0.5 s already hook? Is any frame empty/boring?
- [ ] Any text clipped, overlapping, overflowing, too small, or low-contrast?
- [ ] Is every string correct French, typo-free, with proper typography?
- [ ] Does it look like *this brand* or like a generic template? Would you swap it with another brand's piece without noticing? If yes, push the art direction.
- [ ] Hierarchy: in each frame, is there one obvious focal point?
- [ ] Is there texture/depth, or is it flat shapes on a flat background?
- [ ] End card: logo, CTA, readable, held ≥ 2.5 s?
Fix, re-render, re-check. Two review rounds usually separate "OK" from "wow". Stop when the checklist passes — don't gold-plate.

## 7. Anti-patterns (instant "template" smell)
- Centered white text on a purple-blue gradient. Glassmorphism cards for everything. Emoji as graphics.
- Lorem ipsum, "Votre texte ici", placeholder names ("John Doe", "Company"), fake-looking round numbers everywhere.
- Every element fading in the same way at the same speed.
- Dozens of tiny elements; text walls; 4+ fonts; rainbow palettes.
- Inconsistent logo, or no brand presence until the last frame.

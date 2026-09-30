# Prompting Kling 3.0 for Klipt clips

Kling 3.0 std (`kling-video/v3.0/std/text-to-video`) is Klipt's default footage model: 15 s in up to 6 custom shots, 720×1280 at 24 fps, $0.69 silent or $1.04 with native sound (June 2026 prices, estimate endpoint). The clip is **raw footage** for the code layer: the model supplies light, material, motion and sound; Claude supplies every word, number, logo and UI. Prompt it like a director's shot list, not like a poster.

## Request shape
```json
{"prompt": "<STYLE BIBLE, 300–700 chars>", "duration": 15, "aspect_ratio": "9:16", "sound": "on",
 "cfg_scale": 0.6, "multi_shots": true,
 "multi_prompt": [{"prompt": "<SHOT 1, ≤ 512 chars>", "duration": 3}, {"prompt": "<SHOT 2>", "duration": 4}, …]}
```
- `multi_prompt` durations are what get generated and billed (they must add up to the total); 3–6 shots of 2–5 s. Put cuts where the edit needs them (the code layer wipes or matches on them), e.g. 3 + 3 + 4 + 5.
- `cfg_scale` 0.6–0.7 = follows the shot list more literally (0.5 default is looser and more "creative").
- `sound: "on"` (+50 %) gives synchronised ambience and effects — worth it for craft, food, places, nature, machines. Leave it off when the piece will be carried by music and graphics only.

## The style bible (top-level `prompt`)
One paragraph that every shot inherits, so the cut-together clip looks like one film:
- **Medium & look**: "shot on 35 mm film / ARRI Alexa, anamorphic, fine grain, soft halation", or "clean 3D render, Octane, studio lighting", or "macro product cinematography".
- **Palette & grade**: name 2–4 colours and the contrast ("deep ink-blue shadows, warm tungsten highlights, one acid-lime accent light").
- **World & casting**: place, era, the people's age range, wardrobe and attitude ("real small-business owners in their 30s–50s, work clothes, candid, not models, no suits").
- **Camera grammar**: default lens and movement ("50 mm, slow dolly and gentle handheld, shallow depth of field").
- **Sound** (when on): the sonic world ("natural room tone and foley only, no music, no speech").
- **Hard constraints**: "No text, no letters, no numbers, no logos, no signage, no watermarks, no brand names, no readable screens."

## Each shot (`multi_prompt[i].prompt`)
Write in this order, ≤ 512 characters, one idea per shot:
1. **Shot size + angle**: extreme close-up / close-up / medium / wide / top-down / low angle.
2. **Subject + ONE simple physical action** with a clear start and end: "pulls a tray of croissants from the oven", "spins the chair to face the camera", "a drop of espresso falls into the cup".
3. **Camera move**, one only: slow push-in, dolly left, orbit 30°, crane up, whip pan (to cut on), locked-off.
4. **Light**: source and direction ("low morning sun from the left, dust in the beam", "neon rim light, magenta and cyan").
5. **Composition for the layer**: where the empty space is ("subject in the lower half, clean dark upper third for a title").
6. **Sound** (if on): 2–3 concrete sounds ("crackling fire, metal peel scraping brick").

## What Kling does well — lean on it
Macro textures (flour, steam, liquids, fabric, hair), light changes and flares, slow elegant camera moves, small natural human gestures (smile, turn, hand-over), crowds and cities at a distance, food and drink, nature, abstract 3D (glass, chrome, liquid metal, particles, iridescent forms), phones held in hand **with the screen facing away or glowing blank**.

## What it does badly — avoid or hide
- **Any readable text**: signage, shop windows, screens, packaging, jerseys → ask for "blank", "out of focus", "facing away"; Claude adds real text/UI on top.
- **Precise tool use** (knife scoring, typing specific keys, writing) → show the result or the gesture from a forgiving angle ("hands lift the scored loaf").
- **Fast complex motion, many people interacting, hands in close-up doing fine work, mirrors, animals doing tricks.**
- **Stock clichés** (people in suits pointing at laptops, handshakes, thumbs-up) → cast specifically and give them a real task.
- **Morphing between shots**: each shot is independent; for continuity repeat the key descriptors (same person: "the same woman, short black hair, rust-coloured sweater").

## Designing for the code layer
- Plan the edit first (storyboard in plan.md), then write the shots so each leaves room for its super (empty third, dark area, sky, wall).
- Make cuts useful: end a shot on a whip pan or a dark frame to hide a wipe; match colour or shape across a cut for a match cut in code.
- The first 0.5 s of shot 1 is the thumbnail: strong subject, high contrast, already moving.
- Leave the last 2–3 s simple (slow move, clean background) so the end card and logo sit on it, or blur it in code.
- For a "mix" look, alternate real-world shots with abstract 3D shots in the same palette — the style bible keeps them coherent.

## Sound in the final piece
Kling's audio is the **ambience layer**. In the piece, mix it with `KLIPT.audio` (see the contract):
`{src: 'assets/clip.mp4', gain: -8}` under a music bed (`tools/sfx.py bed`, −6 to −10 dB) and transition effects (`whoosh`, `impact`, `tick`, `shimmer`) placed exactly on the code layer's cuts, wipes and logo reveal. Cut picture on the bed's beats (beat = 60 / bpm).

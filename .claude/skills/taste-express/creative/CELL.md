# The creative cell

Originality is not a style. It is **a true, specific observation about the brief, seen through an unexpected lens, executed with total commitment.** No typeface, colour, layout or effect is good or bad in itself; what kills a design is the default (what you would do on autopilot) and repetition (what was already done). This cell exists to leave both behind, differently every time.

Time box: about 3 minutes, written as short lines in `design-card.md`. Never skip a step; never pad one.

## 1. Mine the brief (raw material)
List 10–15 concrete fragments, the more specific the better:
objects · gestures · places · numbers · words and idioms (in the audience's language) · sensations (sound, texture, temperature, smell) · daily rituals · the enemy or tension · what the audience jokes about · what they would never say.
Then one **truth** sentence: what is really, specifically true about this product or offer (a mechanism, a moment, an object, a number), never an adjective.

## 2. Name your autopilot
Write, in two lines, what you would design for this brief if you did not think: composition, colours, type, components, imagery. Add what the last pieces in the history did (step 3 prints them). Together they are the **zone to leave**. Describing it is enough; there is no list of forbidden things.

## 3. Draw provocations
```bash
python SKILL_DIR/scripts/draw.py "<one-line brief>" --brand <name> [--social]
```
You get 3 creative operators (`operators.md`), 4 foreign domains, one optional constraint and, for social, one optional format mechanic, all avoiding what recent pieces used, plus a reminder of those recent pieces. Keep the draw id. The draw is a random provocation (the "random entry" technique): it forces your associations away from their usual paths. Use it seriously, even when a domain looks absurd at first: the absurd ones produce the most original bridges.

## 4. Diverge: 8 concepts
Write 8 genuinely different concepts, one line each: **name — what the viewer sees — why it is true**.
- At least 5 must be built from the draw: a fragment × an operator × a domain (or the constraint, or the mechanic).
- Up to 3 may come from your own intuition, but none may sit in the zone to leave.
- Eight variations of one idea count as one. Change the idea, not the colour.

## 5. Converge: score and choose
Score each concept 1–5 on:
- **Truth**: says something true and specific about this product.
- **Surprise**: someone who has seen a thousand AI-made posts would not expect it.
- **Stop**: stops a thumb in half a second.
- **Clarity**: the message lands in three seconds.
- **Feasible**: buildable well in HTML/CSS with the kit, within the time budget.
- **Fresh**: far from the history and from the zone to leave.

Pick the highest total; if tied, the higher Surprise wins. A concept scoring 1 on Truth or Clarity is out, whatever its total. Write one line on why it won.

## 6. Derive the language from the concept
Every visual decision is answered by the concept, never by habit. For each, write the reason in a few words:
- **Composition**: where does this concept put the eye first, second, third? What would its world do with the frame?
- **Type**: what voice does the concept speak with (who wrote it, printed it, carved it, typed it, shouted it)? Choose the typeface from that voice, from any family on Google Fonts.
- **Colour**: what colours does the concept's world really contain? Name them from the real referent, then give each one a job.
- **Material and detail**: what surface, texture, marks and small details make it believable?
- **Brand constants**: only the brand name, handle, logo and anything the user fixed stay constant across pieces. Everything else is free to move.

Freshness check: no typeface and no palette identical to a recent piece in the history (brand constants excepted). If your derivation lands on the same choices as last time, go back to the concept and ask again.

## 7. Commit to one bold move
Name the one move a cautious designer would soften (scale, crop, placement, material, colour, rule-breaking, humour) and push it further than feels comfortable. Keep everything else in service of it.

## 8. Critique after the first render (three voices)
Look at the preview and answer in one line each:
- **Art director**: is it committed, crafted, specific? What is weak or generic?
- **Stranger in the feed**: do I stop? Do I understand in three seconds? What do I remember?
- **AI detector**: would I guess an AI made this? What gave it away?
Fix the top issue of each voice in the one fix pass.

## 9. Remember
```bash
python SKILL_DIR/scripts/remember.py --id <draw id> --brand <name> --concept "…" --fonts "…" --palette "#… #…" --layout "…" --device "…" --files "…"
```
This is what keeps the next piece from resembling this one.

## Series and carousels
- A series (several posts) runs one draw per post. Different posts of the same brand share only the brand constants.
- A carousel is one piece: one draw, one concept; the concept decides how the slides vary and connect.

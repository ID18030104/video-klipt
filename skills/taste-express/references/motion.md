# Motion (read only when a piece really moves: multi-section pages, interactive prototypes)

## Springs (Apple, via Motion One on plain HTML)
```html
<script type="module">
import { animate, spring } from "https://cdn.jsdelivr.net/npm/motion@11/+esm";
// Default UI: critically damped, no overshoot
animate(".sheet", { y: 0 }, { type: spring, bounce: 0, duration: 0.4 });
// After a flick only: a little bounce
animate(".card", { x: 0 }, { type: spring, bounce: 0.2, duration: 0.4 });
</script>
```
| Interaction | bounce | duration (≈ response) |
|---|---|---|
| move / reposition | 0 | 0.4 |
| sheet / drawer | 0.2 | 0.3 |
| rotation | 0.2 | 0.4 |

Rules: start from the current on-screen value; hand the release velocity to the spring; enter and exit on the same path; anchor popovers to their trigger (`transform-origin`); feedback on pointer-down; animate only `transform` and `opacity`.

## Scroll storytelling (GSAP, only for real multi-section pages)
```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js"></script>
<script>
gsap.registerPlugin(ScrollTrigger);
if (!matchMedia("(prefers-reduced-motion: reduce)").matches) {
  // Sticky stack: each card pins at the top, shrinks as the next arrives
  const cards = gsap.utils.toArray(".stack-card");
  cards.forEach((card, i) => {
    if (i === cards.length - 1) return;
    ScrollTrigger.create({ trigger: card, start: "top top", endTrigger: cards.at(-1), end: "top top", pin: true, pinSpacing: false });
    gsap.to(card, { scale: 0.92, opacity: 0.55, ease: "none", scrollTrigger: { trigger: cards[i + 1], start: "top bottom", end: "top top", scrub: true } });
  });
  // Horizontal pan: pin the wrapper, scrub the track
  const track = document.querySelector(".pan-track");
  if (track) gsap.to(track, { x: () => -(track.scrollWidth - innerWidth), ease: "none",
    scrollTrigger: { trigger: ".pan", start: "top top", end: () => "+=" + (track.scrollWidth - innerWidth), pin: true, scrub: 1, invalidateOnRefresh: true } });
  // Reveal: images grow in, words scrub from 0.15 to 1
  gsap.utils.toArray(".reveal-img").forEach((el) => gsap.from(el, { scale: 0.85, opacity: 0.4, scrollTrigger: { trigger: el, start: "top 85%", end: "top 40%", scrub: true } }));
}
</script>
```
Always `start: "top top"` for pins. Never `window.addEventListener("scroll")`. One marquee per page at most.

## Static renders
Screenshots capture the state at ~1.2 s: entry animations must be finished by then, and nothing important may depend on scroll.

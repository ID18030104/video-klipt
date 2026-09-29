// Tiny deterministic helpers for Klipt compositions. Load with:
//   <script src="../../lib/klipt-kit.js"></script>   → window.KK
(function () {
  function rng(seed) { // mulberry32 — seeded, reproducible randomness
    let a = seed >>> 0;
    return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  }
  const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const lerp = (a, b, t) => a + (b - a) * t;
  // progress of t inside [start, start+dur], clamped 0..1
  const prog = (t, start, dur) => clamp((t - start) / dur);
  const ease = {
    linear: x => x,
    inCubic: x => x * x * x, outCubic: x => 1 - Math.pow(1 - x, 3),
    inOutCubic: x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2,
    outExpo: x => x === 1 ? 1 : 1 - Math.pow(2, -10 * x),
    inOutExpo: x => x === 0 ? 0 : x === 1 ? 1 : x < .5 ? Math.pow(2, 20 * x - 10) / 2 : (2 - Math.pow(2, -20 * x + 10)) / 2,
    outBack: (x, s = 1.70158) => 1 + (s + 1) * Math.pow(x - 1, 3) + s * Math.pow(x - 1, 2),
    outElastic: x => x === 0 ? 0 : x === 1 ? 1 : Math.pow(2, -10 * x) * Math.sin((x * 10 - .75) * (2 * Math.PI / 3)) + 1,
  };
  window.KK = { rng, clamp, lerp, prog, ease };
})();

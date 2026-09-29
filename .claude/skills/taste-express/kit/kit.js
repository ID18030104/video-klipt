/* taste-express kit — procedural imagery, charts, iOS status bar.
   Declarative: add attributes, the kit fills them on load. window.Kit exposes the same functions.

   <canvas class="layer" data-field='{"preset":"sea","seed":4}'></canvas>
   <div data-bars='{"labels":["06 h","09 h"],"values":[0.5,0.6],"highlight":1,"decimal":","}'></div>
   <div data-area='{...same keys...}'></div>
   <div class="ios-status" data-kit="status" data-time="9:41"></div>
   <div class="progress" data-progress="2/6"></div>
   <span data-annotate='{"type":"circle","color":"#ff2a6d"}'>0,60</span>   (circle | underline | strike | box)
   <svg style="width:600px;height:600px" data-guilloche='{"color":"#1f6f4a","rings":3}'></svg>
*/
(function () {
  "use strict";

  // ---------- noise ----------
  function mulberry32(a) {
    return function () {
      a |= 0; a = (a + 0x6d2b79f5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function makeNoise(seed) {
    const rnd = mulberry32(seed);
    const perm = new Uint8Array(512);
    const grid = new Float32Array(256);
    const p = Array.from({ length: 256 }, (_, i) => i);
    for (let i = 255; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [p[i], p[j]] = [p[j], p[i]]; }
    for (let i = 0; i < 512; i++) perm[i] = p[i & 255];
    for (let i = 0; i < 256; i++) grid[i] = rnd();
    return function (x, y) {
      const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi;
      const u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf);
      const X = xi & 255, Y = yi & 255;
      const a = grid[perm[perm[X] + Y]], b = grid[perm[perm[X + 1] + Y]];
      const c = grid[perm[perm[X] + Y + 1]], d = grid[perm[perm[X + 1] + Y + 1]];
      return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v;
    };
  }

  function fbm(noise, x, y, octaves) {
    let sum = 0, amp = 0.5, freq = 1, norm = 0;
    for (let o = 0; o < octaves; o++) {
      sum += amp * noise(x * freq, y * freq); norm += amp; amp *= 0.5; freq *= 2.03;
    }
    return sum / norm;
  }

  function hexToRgb(hex) {
    const h = hex.replace("#", "");
    const n = parseInt(h.length === 3 ? h.split("").map((c) => c + c).join("") : h, 16);
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  }

  function gradientLut(stops) {
    const lut = new Uint8ClampedArray(256 * 3);
    const s = stops.map(([pos, hex]) => [pos, hexToRgb(hex)]).sort((a, b) => a[0] - b[0]);
    for (let i = 0; i < 256; i++) {
      const t = i / 255;
      let k = 0;
      while (k < s.length - 2 && t > s[k + 1][0]) k++;
      const [p0, c0] = s[k], [p1, c1] = s[Math.min(k + 1, s.length - 1)];
      const f = p1 === p0 ? 0 : Math.min(1, Math.max(0, (t - p0) / (p1 - p0)));
      for (let ch = 0; ch < 3; ch++) lut[i * 3 + ch] = c0[ch] + (c1[ch] - c0[ch]) * f;
    }
    return lut;
  }

  // Presets: stops go dark -> light. Tune per brand by passing your own stops.
  const PRESETS = {
    sea:    { stops: [[0, "#052330"], [0.4, "#0b4152"], [0.68, "#156a78"], [0.86, "#3a97a0"], [1, "#a6dcd6"]], scale: 5.5, warp: 0.35, stretch: 4.5, angle: -12, ridge: 0.55, glint: 0.4, contrast: 1.1 },
    lagoon: { stops: [[0, "#0b4a57"], [0.4, "#138c90"], [0.72, "#46c4b7"], [1, "#d3f3e8"]], scale: 3.2, warp: 0.7, stretch: 2.2, angle: 20, ridge: 0.3, glint: 0.3, contrast: 1.1 },
    mist:   { stops: [[0, "#a9b9c4"], [0.5, "#cdd9e0"], [1, "#f1f5f7"]], scale: 1.8, warp: 1.4, stretch: 1.4, angle: 0, glint: 0, contrast: 1.0 },
    aurora: { stops: [[0, "#06121a"], [0.45, "#0e3a3a"], [0.72, "#2c7c69"], [1, "#b4e2c4"]], scale: 1.6, warp: 1.6, stretch: 2.8, angle: -30, glint: 0, contrast: 1.3 },
    ink:    { stops: [[0, "#04080b"], [0.55, "#0d1a23"], [1, "#22404f"]], scale: 2.2, warp: 1.2, stretch: 1.2, angle: 0, glint: 0.15, contrast: 1.2 },
    stone:  { stops: [[0, "#686f75"], [0.5, "#9aa1a6"], [1, "#dde1e3"]], scale: 4.0, warp: 0.6, stretch: 1, angle: 0, glint: 0, contrast: 1.1 },
    dune:   { stops: [[0, "#9c7f58"], [0.5, "#c9ad80"], [1, "#efe1c6"]], scale: 2.4, warp: 0.8, stretch: 3.2, angle: 8, glint: 0.1, contrast: 1.2 },
  };

  /** Paint an organic noise field (aerial water, mist, stone...) on a canvas sized by CSS. */
  function field(target, options) {
    const canvas = typeof target === "string" ? document.querySelector(target) : target;
    if (!canvas) return;
    const o = Object.assign({ seed: 7, res: 0.5, vignette: 0.22, octaves: 5, ridge: 0 }, PRESETS[(options && options.preset) || "sea"], options || {});
    const dpr = window.devicePixelRatio || 1;
    const cssW = canvas.clientWidth || canvas.width, cssH = canvas.clientHeight || canvas.height;
    canvas.width = Math.round(cssW * dpr); canvas.height = Math.round(cssH * dpr);
    const w = Math.max(2, Math.round(canvas.width * o.res)), h = Math.max(2, Math.round(canvas.height * o.res));
    const off = document.createElement("canvas"); off.width = w; off.height = h;
    const octx = off.getContext("2d"), img = octx.createImageData(w, h), data = img.data;
    const n1 = makeNoise(o.seed), n2 = makeNoise(o.seed + 101), n3 = makeNoise(o.seed + 202);
    const lut = gradientLut(o.stops);
    const rad = (o.angle * Math.PI) / 180, ca = Math.cos(rad), sa = Math.sin(rad);
    const aspect = w / h, thr = 1 - o.glint * 0.16;
    for (let y = 0; y < h; y++) {
      for (let x = 0; x < w; x++) {
        let u = (x / w) * aspect, v = y / h;
        const ru = (u * ca - v * sa) * o.scale, rv = (u * sa + v * ca) * o.scale * o.stretch;
        const qx = fbm(n2, ru + 1.7, rv + 9.2, 4), qy = fbm(n2, ru + 8.3, rv + 2.8, 4);
        let val = fbm(n1, ru + o.warp * (qx - 0.5) * 2, rv + o.warp * (qy - 0.5) * 2, o.octaves);
        if (o.ridge) { const cr = 1 - Math.abs(fbm(n3, ru * 2.2 + 3.1, rv * 2.2 + 7.7, 3) * 2 - 1); val = val * (1 - o.ridge * 0.5) + cr * cr * o.ridge * 0.5; }
        val = Math.min(1, Math.max(0, 0.5 + (val - 0.5) * o.contrast * 1.6));
        const dx = x / w - 0.5, dy = y / h - 0.5;
        const vig = 1 - o.vignette * Math.min(1, (dx * dx + dy * dy) * 2.2);
        const li = Math.round(val * 255) * 3, i = (y * w + x) * 4;
        let r = lut[li] * vig, g = lut[li + 1] * vig, b = lut[li + 2] * vig;
        if (o.glint > 0) {
          const s = n3(ru * 17 + 50, rv * 17 + 50);
          if (s > thr && val > 0.45) { const k = ((s - thr) / (1 - thr)) * 0.85 * val; r += (255 - r) * k; g += (255 - g) * k; b += (255 - b) * k; }
        }
        data[i] = r; data[i + 1] = g; data[i + 2] = b; data[i + 3] = 255;
      }
    }
    octx.putImageData(img, 0, 0);
    const ctx = canvas.getContext("2d");
    ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = "high";
    ctx.drawImage(off, 0, 0, canvas.width, canvas.height);
  }

  // ---------- charts ----------
  const fmt = (v, o) => {
    let [int, dec] = (o.digits === undefined ? v.toFixed(1) : v.toFixed(o.digits)).split(".");
    const sep = o.thousands !== undefined ? o.thousands : o.decimal === "," ? " " : "";
    if (sep) int = int.replace(/\B(?=(\d{3})+(?!\d))/g, sep);
    return int + (dec ? (o.decimal === "," ? "," : ".") + dec : "") + (o.unit || "");
  };

  /** Rounded bar chart with value labels; `highlight` = index drawn in the accent. */
  function bars(target, options) {
    const el = typeof target === "string" ? document.querySelector(target) : target;
    const o = Object.assign({ height: 132, gap: 10, highlight: -1, color: "var(--accent)", rest: "color-mix(in srgb, var(--ink) 14%, transparent)", labelColor: "var(--muted)" }, options);
    const k = o.scale || 1, W = el.clientWidth || 320, H = o.height, n = o.values.length;
    const top = 22 * k, bottom = 22 * k, max = o.max || Math.max(...o.values) * 1.08;
    const bw = (W - o.gap * (n - 1)) / n;
    let svg = `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="${o.aria || "chart"}" style="display:block;font-family:inherit">`;
    o.values.forEach((v, i) => {
      const bh = Math.max(4, ((H - top - bottom) * v) / max), x = i * (bw + o.gap), y = H - bottom - bh, on = i === o.highlight;
      svg += `<rect x="${x}" y="${y}" width="${bw}" height="${bh}" rx="${Math.min(10 * k, bw / 2.4)}" style="fill:${on ? o.color : o.rest}"/>`;
      svg += `<text x="${x + bw / 2}" y="${y - 7 * k}" text-anchor="middle" style="font-size:${12 * k}px;font-weight:${on ? 700 : 600};fill:${on ? "var(--ink)" : "var(--ink-2)"};font-variant-numeric:tabular-nums">${fmt(v, o)}</text>`;
      svg += `<text x="${x + bw / 2}" y="${H - 5 * k}" text-anchor="middle" style="font-size:${11 * k}px;font-weight:${on ? 700 : 500};fill:${on ? "var(--ink)" : o.labelColor}">${o.labels[i]}</text>`;
    });
    el.innerHTML = svg + "</svg>";
  }

  /** Smooth area/line chart with dots, labels and an optional "now" marker. */
  function area(target, options) {
    const el = typeof target === "string" ? document.querySelector(target) : target;
    const o = Object.assign({ height: 140, highlight: -1, color: "var(--accent)", nowLabel: "", labelColor: "var(--muted)" }, options);
    const k = o.scale || 1, W = el.clientWidth || 320, H = o.height, n = o.values.length, pad = 14 * k, top = 26 * k, bottom = 24 * k;
    const min = o.min !== undefined ? o.min : 0, max = o.max || Math.max(...o.values) * 1.12;
    const X = (i) => pad + ((W - pad * 2) * i) / (n - 1);
    const Y = (v) => top + (H - top - bottom) * (1 - (v - min) / (max - min));
    const pts = o.values.map((v, i) => [X(i), Y(v)]);
    let d = `M${pts[0][0]},${pts[0][1]}`;
    for (let i = 0; i < n - 1; i++) {
      const p0 = pts[Math.max(0, i - 1)], p1 = pts[i], p2 = pts[i + 1], p3 = pts[Math.min(n - 1, i + 2)];
      d += ` C${p1[0] + (p2[0] - p0[0]) / 6},${p1[1] + (p2[1] - p0[1]) / 6} ${p2[0] - (p3[0] - p1[0]) / 6},${p2[1] - (p3[1] - p1[1]) / 6} ${p2[0]},${p2[1]}`;
    }
    const id = "g" + Math.random().toString(36).slice(2, 7);
    let svg = `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="${o.aria || "chart"}" style="display:block;font-family:inherit">`;
    svg += `<defs><linearGradient id="${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" style="stop-color:${o.color};stop-opacity:.28"/><stop offset="1" style="stop-color:${o.color};stop-opacity:0"/></linearGradient></defs>`;
    svg += `<path d="${d} L${pts[n - 1][0]},${H - bottom} L${pts[0][0]},${H - bottom} Z" fill="url(#${id})"/>`;
    svg += `<path d="${d}" fill="none" style="stroke:${o.color}" stroke-width="${2.4 * k}" stroke-linecap="round"/>`;
    if (o.highlight >= 0) {
      const [hx, hy] = pts[o.highlight];
      svg += `<line x1="${hx}" x2="${hx}" y1="${hy + 7 * k}" y2="${H - bottom}" style="stroke:var(--ink)" stroke-width="1" stroke-dasharray="2 3" opacity=".45"/>`;
      if (o.nowLabel) svg += `<rect x="${hx - 22 * k}" y="${H - bottom - 20 * k}" width="${44 * k}" height="${17 * k}" rx="${8.5 * k}" style="fill:var(--ink)"/><text x="${hx}" y="${H - bottom - 8 * k}" text-anchor="middle" style="font-size:${10 * k}px;font-weight:700;fill:var(--bg)">${o.nowLabel}</text>`;
    }
    pts.forEach(([x, y], i) => {
      const on = i === o.highlight;
      svg += `<circle cx="${x}" cy="${y}" r="${(on ? 5 : 3) * k}" style="fill:${on ? o.color : "var(--surface)"};stroke:${o.color}" stroke-width="${2 * k}"/>`;
      svg += `<text x="${x}" y="${y - 10 * k}" text-anchor="middle" style="font-size:${11.5 * k}px;font-weight:${on ? 700 : 600};fill:var(--ink-2);font-variant-numeric:tabular-nums">${fmt(o.values[i], o)}</text>`;
      svg += `<text x="${x}" y="${H - 5 * k}" text-anchor="middle" style="font-size:${11 * k}px;font-weight:${on ? 700 : 500};fill:${on ? "var(--ink)" : o.labelColor}">${o.labels[i]}</text>`;
    });
    el.innerHTML = svg + "</svg>";
  }

  // ---------- iOS status bar ----------
  const GLYPHS =
    '<svg width="18" height="12" viewBox="0 0 18 12" fill="currentColor" aria-hidden="true"><rect x="0" y="7.5" width="3.2" height="4.5" rx="1"/><rect x="4.8" y="5.2" width="3.2" height="6.8" rx="1"/><rect x="9.6" y="2.8" width="3.2" height="9.2" rx="1"/><rect x="14.4" y="0" width="3.2" height="12" rx="1"/></svg>' +
    '<svg width="16" height="12" viewBox="0 0 16 12" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" aria-hidden="true"><path d="M1.6 4.4a9 9 0 0 1 12.8 0"/><path d="M4.3 7.2a5.2 5.2 0 0 1 7.4 0"/><circle cx="8" cy="10.2" r="1.35" fill="currentColor" stroke="none"/></svg>' +
    '<svg width="27" height="13" viewBox="0 0 27 13" aria-hidden="true"><rect x=".5" y=".5" width="23" height="12" rx="3.6" fill="none" stroke="currentColor" opacity=".4"/><rect x="2.4" y="2.4" width="19.2" height="8.2" rx="2.1" fill="currentColor"/><path d="M25 4.4v4.2c.8-.3 1.4-1.1 1.4-2.1s-.6-1.8-1.4-2.1z" fill="currentColor" opacity=".45"/></svg>';

  function statusBar(target) {
    const el = typeof target === "string" ? document.querySelector(target) : target;
    el.innerHTML = `<span>${el.dataset.time || "9:41"}</span><span class="glyphs">${GLYPHS}</span>`;
  }


  // ---------- material devices ----------
  const FILTERS = '<svg id="kit-filters" width="0" height="0" style="position:absolute" aria-hidden="true">' +
    '<filter id="kit-rough"><feTurbulence type="fractalNoise" baseFrequency=".03" numOctaves="2" seed="4"/><feDisplacementMap in="SourceGraphic" scale="7"/></filter>' +
    '<filter id="kit-ink" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency=".75" numOctaves="3" seed="9" result="n"/>' +
    '<feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -3.2 2.05" result="m"/>' +
    '<feComposite in="SourceGraphic" in2="m" operator="in" result="c"/><feTurbulence type="fractalNoise" baseFrequency=".04" numOctaves="2" seed="2" result="w"/>' +
    '<feDisplacementMap in="c" in2="w" scale="2.5"/></filter></svg>';

  function injectFilters() {
    if (document.getElementById("kit-filters")) return;
    const holder = document.createElement("div");
    holder.innerHTML = FILTERS;
    document.body.prepend(holder.firstChild);
  }

  /** Hand-drawn annotation around/under an inline element: circle | underline | strike | box. */
  function annotate(el, options) {
    const o = Object.assign({ type: "circle", color: "var(--accent)", width: 5, pad: 14, seed: 3, loops: 1.15 }, options);
    const rnd = mulberry32(o.seed);
    const w = el.offsetWidth + o.pad * 2, h = el.offsetHeight + o.pad * 2;
    let d = "";
    if (o.type === "circle") {
      const cx = w / 2, cy = h / 2, steps = 64, turns = o.loops * Math.PI * 2, start = rnd() * Math.PI * 2;
      for (let i = 0; i <= steps; i++) {
        const t = start + (turns * i) / steps, j = 1 + (rnd() - 0.5) * 0.06 + (i / steps) * 0.05;
        d += `${i ? "L" : "M"}${(cx + Math.cos(t) * (w / 2) * j).toFixed(1)},${(cy + Math.sin(t) * (h / 2) * j).toFixed(1)}`;
      }
    } else if (o.type === "box") {
      d = `M4,6 L${w - 3},3 L${w - 5},${h - 4} L6,${h - 2} Z`;
    } else {
      const y = o.type === "strike" ? h / 2 : h - o.pad * 0.6;
      d = `M2,${y + 3} C${w * 0.3},${y - 4} ${w * 0.6},${y + 5} ${w - 2},${y - 2}`;
      if (o.type === "underline") d += ` M${w * 0.1},${y + 10} C${w * 0.4},${y + 5} ${w * 0.7},${y + 12} ${w * 0.92},${y + 6}`;
    }
    if (getComputedStyle(el).position === "static") el.style.position = "relative";
    if (getComputedStyle(el).display === "inline") el.style.display = "inline-block";
    el.insertAdjacentHTML("beforeend", `<svg aria-hidden="true" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" style="position:absolute;left:${-o.pad}px;top:${-o.pad}px;overflow:visible;pointer-events:none"><path d="${d}" fill="none" style="stroke:${o.color}" stroke-width="${o.width}" stroke-linecap="round" stroke-linejoin="round" filter="url(#kit-rough)"/></svg>`);
  }

  /** Guilloche rosette (banknote / security print) drawn into an <svg> sized by CSS. */
  function guilloche(svg, options) {
    const o = Object.assign({ color: "currentColor", rings: 3, R: 0.36, r: 0.047, d: 0.09, stroke: 0.7, opacity: 0.8 }, options);
    const W = svg.clientWidth || 600, H = svg.clientHeight || 600, s = Math.min(W, H), cx = W / 2, cy = H / 2;
    svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
    let out = "";
    for (let k = 0; k < o.rings; k++) {
      const R = s * (o.R - k * 0.07), r = s * o.r * (1 + k * 0.35), dd = s * o.d * (1 - k * 0.18);
      const turns = Math.round((R + r) / r), steps = 2400;
      let d = "";
      for (let i = 0; i <= steps; i++) {
        const t = (i / steps) * Math.PI * 2 * turns;
        const x = cx + (R + r) * Math.cos(t) - dd * Math.cos(((R + r) / r) * t);
        const y = cy + (R + r) * Math.sin(t) - dd * Math.sin(((R + r) / r) * t);
        d += `${i ? "L" : "M"}${x.toFixed(1)},${y.toFixed(1)}`;
      }
      out += `<path d="${d}" fill="none" style="stroke:${o.color}" stroke-width="${o.stroke}" opacity="${o.opacity}"/>`;
    }
    svg.innerHTML = out;
  }

  // ---------- auto-init ----------
  function parse(el, attr) {
    try { return JSON.parse(el.getAttribute(attr) || "{}"); } catch (e) { console.error("kit: bad JSON in", attr, e); return {}; }
  }

  /** Carousel progress: data-progress="i/n" -> n segments, the first i lit. */
  function progress(el) {
    const [i, n] = (el.dataset.progress || "1/5").split("/").map(Number);
    el.innerHTML = Array.from({ length: n }, (_, k) => `<i class="${k < i ? "on" : ""}"></i>`).join("");
  }

  function init() {
    injectFilters();
    document.querySelectorAll("svg[data-guilloche]").forEach((el) => guilloche(el, parse(el, "data-guilloche")));
    document.querySelectorAll("[data-annotate]").forEach((el) => annotate(el, parse(el, "data-annotate")));
    document.querySelectorAll('[data-kit="status"]').forEach(statusBar);
    document.querySelectorAll("[data-progress]").forEach(progress);
    document.querySelectorAll("canvas[data-field]").forEach((c) => field(c, parse(c, "data-field")));
    document.querySelectorAll("[data-bars]").forEach((el) => bars(el, parse(el, "data-bars")));
    document.querySelectorAll("[data-area]").forEach((el) => area(el, parse(el, "data-area")));
  }

  window.Kit = { field, bars, area, statusBar, progress, annotate, guilloche, presets: PRESETS, init };
  const start = () => (document.fonts ? document.fonts.ready.then(init) : init());
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
})();

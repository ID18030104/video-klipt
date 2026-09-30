#!/usr/bin/env node
// Deterministic HTML → MP4 / PNG renderer for Klipt example pieces.
// Usage:
//   node tools/render.mjs video  <piece-dir> [--fps 30] [--preview]   → video.mp4 + poster.jpg + sheet.jpg
//   node tools/render.mjs stills <piece-dir>                          → slides/slide-01.png … + sheet.jpg
//   node tools/render.mjs frame  <piece-dir> <t-seconds> [out.png] [--w 540] → single frame (quick check)
//   node tools/render.mjs qa     <piece-dir>                          → qa.jpg keyframe grid + automatic defect report
// Contract: see docs/RENDER_CONTRACT.md
import { chromium } from 'playwright-core';
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const FFMPEG = process.env.KLIPT_FFMPEG || 'ffmpeg';

const [mode, dirArg, ...rest] = process.argv.slice(2);
if (!mode || !dirArg) { console.error('usage: render.mjs video|stills|frame <piece-dir> ...'); process.exit(2); }
const dir = path.resolve(dirArg);
const entry = path.join(dir, 'index.html');
if (!fs.existsSync(entry)) { console.error(`missing ${entry}`); process.exit(2); }
const opt = (k, d) => { const i = rest.indexOf(k); return i >= 0 ? rest[i + 1] : d; };
const flag = k => rest.includes(k);

function ff(args, input) {
  return new Promise((res, rej) => {
    const p = spawn(FFMPEG, ['-hide_banner', '-loglevel', 'error', '-y', ...args], { stdio: [input ? 'pipe' : 'ignore', 'inherit', 'inherit'] });
    p.on('close', c => c === 0 ? res() : rej(new Error(`ffmpeg exited ${c}`)));
    if (input) input(p.stdin);
  });
}

async function open() {
  const browser = await chromium.launch({
    executablePath: CHROME,
    args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist',
           '--allow-file-access-from-files', '--disable-web-security', '--font-render-hinting=none', '--force-color-profile=srgb'],
  });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('requestfailed', r => errors.push(`request failed: ${r.url()}`));
  await page.goto(pathToFileURL(entry).href, { waitUntil: 'load' });
  await page.waitForFunction(() => window.KLIPT, null, { timeout: 15000 }).catch(() => {
    throw new Error('window.KLIPT not defined — see docs/RENDER_CONTRACT.md');
  });
  const meta = await page.evaluate(async () => {
    const K = window.KLIPT;
    if (K.ready) await K.ready;
    await document.fonts.ready;
    // Freeze every CSS/WAAPI animation so the renderer owns the clock.
    for (const a of document.getAnimations()) a.pause();
    return { width: K.width || 1080, height: K.height || 1920, fps: K.fps || 30, duration: K.duration || 0, poster: K.poster, slides: document.querySelectorAll('.slide').length };
  });
  await page.setViewportSize({ width: meta.width, height: meta.height });
  return { browser, page, meta, errors };
}

async function seek(page, t) {
  await page.evaluate(async t => {
    const K = window.KLIPT;
    for (const a of document.getAnimations()) { a.pause(); a.currentTime = t * 1000; }
    // Only await real Promises: GSAP timelines are thenables that never resolve while paused.
    if (K.render) { const r = K.render(t); if (r instanceof Promise) await r; }
    await new Promise(r => requestAnimationFrame(() => r()));
  }, t);
}

async function sheet(pattern, start, n, cols, out) {
  // Grid of thumbnails for quick visual review (images must be a numbered sequence).
  const rows = Math.ceil(n / cols);
  await ff(['-framerate', '1', '-start_number', String(start), '-i', pattern, '-frames:v', String(n),
    '-vf', `scale=360:-2,pad=iw+8:ih+8:4:4:color=0x222222,tile=${cols}x${rows}:color=0x111111`, '-frames:v', '1', '-q:v', '3', out]);
}

// Machine-wide render slots: parallel agents share 4 CPUs, and too many concurrent
// Chromium captures crash ("browser closed"). Full renders queue for a free slot.
const SLOTS = +(process.env.KLIPT_RENDER_SLOTS || 2);
function alive(pid) { try { process.kill(pid, 0); return true; } catch { return false; } }
async function acquireSlot() {
  if (mode === 'frame' || mode === 'qa') return null;
  const waitStart = Date.now(); let told = false;
  for (;;) {
    for (let i = 0; i < SLOTS; i++) {
      const f = `/tmp/klipt-render-slot-${i}.lock`;
      try { fs.writeFileSync(f, String(process.pid), { flag: 'wx' }); return f; }
      catch { const pid = +fs.readFileSync(f, 'utf8'); if (!alive(pid)) fs.rmSync(f, { force: true }); }
    }
    if (!told && Date.now() - waitStart > 3000) { console.log('waiting for a free render slot…'); told = true; }
    await new Promise(r => setTimeout(r, 1000));
  }
}
const slot = await acquireSlot();
const releaseSlot = () => { if (slot) fs.rmSync(slot, { force: true }); };
process.on('exit', releaseSlot);
for (const sig of ['SIGINT', 'SIGTERM']) process.on(sig, () => { releaseSlot(); process.exit(130); });

const t0 = Date.now();
const { browser, page, meta, errors } = await open();
try {
  if (mode === 'frame') {
    const t = parseFloat(rest[0] || '0');
    await seek(page, t);
    const out = rest[1] && !rest[1].startsWith('--') ? rest[1] : path.join(dir, `frame-${t}.png`);
    await page.screenshot({ path: out });
    // --w <px>: downscale the saved frame (cheaper to look at than a full 1080p frame).
    const w = opt('--w', null);
    if (w) { const tmpOut = out + '.full.png'; fs.renameSync(out, tmpOut); await ff(['-i', tmpOut, '-vf', `scale=${w}:-2`, out]); fs.rmSync(tmpOut); }
    console.log(out);
  } else if (mode === 'video') {
    if (!meta.duration) throw new Error('KLIPT.duration must be set for video pieces');
    const fps = +opt('--fps', flag('--preview') ? 10 : meta.fps);
    const frames = Math.round(meta.duration * fps);
    const out = path.join(dir, flag('--preview') ? 'preview.mp4' : 'video.mp4');
    const shots = [];
    const tmp = fs.mkdtempSync('/tmp/klipt-');
    const sheetTimes = Array.from({ length: 12 }, (_, i) => (i + 0.5) * meta.duration / 12);
    let enc;
    const done = ff(['-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
      '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], s => { enc = s; });
    for (let f = 0; f < frames; f++) {
      const t = f / fps;
      await seek(page, t);
      const buf = await page.screenshot({ type: 'jpeg', quality: 94 });
      if (!enc.write(buf)) await new Promise(r => enc.once('drain', r));
      if (f % Math.max(1, Math.round(fps * 5)) === 0) process.stdout.write(`frame ${f}/${frames}\n`);
    }
    enc.end(); await done;
    for (const [i, t] of sheetTimes.entries()) { await seek(page, t); const p = path.join(tmp, `s${String(i).padStart(2, '0')}.jpg`); await page.screenshot({ path: p, type: 'jpeg', quality: 90 }); shots.push(p); }
    const posterT = meta.poster != null ? meta.poster : meta.duration * 0.62; await seek(page, posterT);
    await page.screenshot({ path: path.join(dir, 'poster.jpg'), type: 'jpeg', quality: 90 });
    await sheet(path.join(tmp, 's%02d.jpg'), 0, shots.length, 6, path.join(dir, 'sheet.jpg'));
    const size = fs.statSync(out).size;
    console.log(JSON.stringify({ out, frames, fps, duration: meta.duration, width: meta.width, height: meta.height, mb: +(size / 1e6).toFixed(2), renderSeconds: (Date.now() - t0) / 1000 }));
  } else if (mode === 'qa') {
    // Keyframes a viewer (or a judge) actually sees: first frame, hook, every 1.5 s, end, poster — or every slide.
    const tmp = fs.mkdtempSync('/tmp/klipt-qa-');
    const shots = [];
    const audit = () => page.evaluate(() => {
      const W = innerWidth, H = innerHeight, issues = [];
      const shown = el => { for (let e = el; e && e !== document.documentElement; e = e.parentElement) { const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity < 0.35) return false; } return true; };
      const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT), seen = new Set();
      while (w.nextNode()) {
        const n = w.currentNode, txt = n.textContent.replace(/\s+/g, ' ').trim(); if (txt.length < 2) continue;
        const el = n.parentElement; if (!el || seen.has(el) || el.closest('script,style,svg defs')) continue; seen.add(el);
        if (!shown(el)) continue;
        const rg = document.createRange(); rg.selectNodeContents(n); const r = rg.getBoundingClientRect();
        if (r.width < 2 || r.height < 2 || r.right < 0 || r.left > W || r.bottom < 0 || r.top > H) continue;
        const t = txt.slice(0, 48), fsz = parseFloat(getComputedStyle(el).fontSize);
        if (r.left < -2 || r.right > W + 2 || r.top < -2 || r.bottom > H + 2) issues.push({ type: 'text cut by the frame edge', text: t });
        for (let e = el.parentElement; e && e !== document.body; e = e.parentElement) {
          const cs = getComputedStyle(e);
          if (cs.overflow !== 'visible' || cs.clipPath !== 'none') {
            const a = e.getBoundingClientRect();
            const inter = Math.max(0, Math.min(r.right, a.right) - Math.max(r.left, a.left)) * Math.max(0, Math.min(r.bottom, a.bottom) - Math.max(r.top, a.top));
            const f = inter / (r.width * r.height);
            if (f > 0.03 && f < 0.92) issues.push({ type: 'text partially masked (mid-reveal?)', text: t, visible: Math.round(f * 100) + '%' });
            if (f > 0.03) break;
          }
        }
        if (fsz < 26 && Math.max(W, H) >= 1080) issues.push({ type: 'small text', text: t, px: Math.round(fsz) });
        if (H / W > 1.7 && (r.top < 200 || r.bottom > H - 340)) issues.push({ type: 'text in 9:16 unsafe zone (platform UI)', text: t });
      }
      const fams = new Set();
      document.querySelectorAll('body *').forEach(e => { const cs = getComputedStyle(e), f = cs.fontFamily.split(',')[0].trim().replace(/["']/g, ''); if (f && e.childNodes.length) fams.add(JSON.stringify([f, cs.fontStyle, cs.fontWeight])); });
      const generic = ['serif', 'sans-serif', 'monospace', 'system-ui', 'inherit', 'cursive', 'fantasy', 'ui-monospace', '-apple-system'];
      const missing = [...new Set([...fams].map(x => JSON.parse(x)).filter(([f, st, wt]) => !generic.includes(f) && !document.fonts.check(`${st} ${wt} 16px "${f}"`)).map(([f, st, wt]) => `${f} ${wt}${st === 'italic' ? ' italic' : ''}`))];
      return { issues, missing };
    });
    const report = [];
    if (meta.slides && !meta.duration) {
      const slides = await page.$$('.slide');
      for (const [i, el] of slides.entries()) {
        await el.evaluate(e => e.scrollIntoView({ block: 'start' }));
        const p = path.join(tmp, `k${String(i).padStart(2, '0')}.jpg`); await page.screenshot({ path: p, type: 'jpeg', quality: 85 });
        shots.push({ p, label: `slide ${i + 1}` }); report.push({ at: `slide ${i + 1}`, ...(await audit()) });
      }
    } else {
      const d = meta.duration, ts = [0, 0.4, 1.0];
      for (let t = 2.5; t < d - 1; t += 1.5) ts.push(+t.toFixed(2));
      ts.push(+(d - 0.05).toFixed(2));
      const posterT = meta.poster != null ? meta.poster : d * 0.62;
      for (const [i, t] of ts.entries()) {
        await seek(page, t);
        const p = path.join(tmp, `k${String(i).padStart(2, '0')}.jpg`); await page.screenshot({ path: p, type: 'jpeg', quality: 85 });
        shots.push({ p, label: `t=${t}s` }); report.push({ at: `t=${t}s`, ...(await audit()) });
      }
      await seek(page, posterT); const pp = path.join(tmp, 'poster.jpg'); await page.screenshot({ path: pp, type: 'jpeg', quality: 85 });
      shots.push({ p: pp, label: `poster t=${posterT}s` }); report.push({ at: `poster t=${posterT}s`, ...(await audit()) });
    }
    // Pixel checks + labelled grid (Python/PIL).
    const py = `
import json,sys
from PIL import Image,ImageDraw,ImageFont,ImageStat
shots=json.loads(sys.argv[1]); out=sys.argv[2]; res=[]
tiles=[]
for s in shots:
  im=Image.open(s['p']).convert('RGB'); g=im.convert('L').resize((160,int(160*im.height/im.width)))
  sd=ImageStat.Stat(g).stddev[0]
  q=im.resize((96,int(96*im.height/im.width))).quantize(8); h=sorted(q.histogram(),reverse=True); dom=h[0]/sum(h)
  res.append(dict(at=s['label'],contrast=round(sd,1),dominant_color_share=round(dom,2)))
  t=im.copy(); t.thumbnail((300,540)); tiles.append((s['label'],t))
cols=6; tw=max(t.width for _,t in tiles); th=max(t.height for _,t in tiles)+30; rows=(len(tiles)+cols-1)//cols
sheet=Image.new('RGB',(cols*(tw+8),rows*th),(20,20,22)); d=ImageDraw.Draw(sheet)
try: f=ImageFont.load_default(size=20)
except TypeError: f=ImageFont.load_default()
for i,(l,t) in enumerate(tiles):
  x=(i%cols)*(tw+8); y=(i//cols)*th; sheet.paste(t,(x,y)); d.text((x+4,y+t.height+4),l,fill=(230,230,230),font=f)
sheet.save(out,quality=85); print(json.dumps(res))`;
    const out = path.join(dir, 'qa.jpg');
    const { execFileSync } = await import('node:child_process');
    const pix = JSON.parse(execFileSync('python3', ['-c', py, JSON.stringify(shots), out]).toString());
    // Group identical findings across keyframes so the report stays short.
    const groups = new Map(), add = (k, at) => { if (!groups.has(k)) groups.set(k, []); if (!groups.get(k).includes(at)) groups.get(k).push(at); };
    for (const [i, r] of report.entries()) {
      const px = pix[i];
      if (px.contrast < 14 || px.dominant_color_share > 0.9) add(`NEAR-EMPTY FRAME (contrast ${px.contrast}, ${Math.round(px.dominant_color_share * 100)}% one colour)`, r.at);
      for (const is of r.issues) add(`${is.type}: "${is.text}"${is.px ? ` (${is.px}px)` : ''}${is.visible ? ` (${is.visible} visible)` : ''}`, r.at);
      for (const m of r.missing) add(`font face not loaded (fallback likely): ${m}`, r.at);
    }
    console.log(`QA ${path.basename(dir)} → ${out} (open it and look)`);
    for (const [k, ats] of groups) console.log(`- ${k}  @ ${ats.length > 4 ? ats.slice(0, 4).join(', ') + ` +${ats.length - 4} more` : ats.join(', ')}`);
    console.log(groups.size ? `${groups.size} finding(s). Heuristics: fix real problems; a deliberate effect (e.g. giant background type bleeding off-frame) may be kept.` : 'No automatic finding — still open qa.jpg and judge it.');
    fs.rmSync(tmp, { recursive: true, force: true });
  } else if (mode === 'stills') {
    const slides = await page.$$('.slide');
    if (!slides.length) throw new Error('stills mode needs one or more .slide elements');
    const outDir = path.join(dir, 'slides'); fs.mkdirSync(outDir, { recursive: true });
    for (const f of fs.readdirSync(outDir)) fs.unlinkSync(path.join(outDir, f));
    // One slide-sized viewport, scrolled to each slide: a viewport as tall as the whole
    // stack (7 × 1350 px…) makes Chromium's capture fail intermittently.
    await seek(page, 0);
    const files = [];
    for (const [i, el] of slides.entries()) {
      const p = path.join(outDir, `slide-${String(i + 1).padStart(2, '0')}.png`);
      const box = await el.evaluate(e => { e.scrollIntoView({ block: 'start' }); const r = e.getBoundingClientRect(); return { x: r.left, y: r.top, width: r.width, height: r.height }; });
      await page.screenshot({ path: p, clip: { x: Math.max(0, box.x), y: Math.max(0, box.y), width: meta.width, height: meta.height } });
      files.push(p);
    }
    await sheet(path.join(outDir, 'slide-%02d.png'), 1, files.length, Math.min(files.length, 5), path.join(dir, 'sheet.jpg'));
    console.log(JSON.stringify({ slides: files.length, width: meta.width, height: meta.height, renderSeconds: (Date.now() - t0) / 1000 }));
  } else throw new Error(`unknown mode ${mode}`);
  if (errors.length) { console.error('PAGE ERRORS:\n' + [...new Set(errors)].join('\n')); process.exitCode = 3; }
} finally { await browser.close(); }

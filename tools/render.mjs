#!/usr/bin/env node
// Deterministic HTML → MP4 / PNG renderer for Klipt example pieces.
// Usage:
//   node tools/render.mjs video  <piece-dir> [--fps 30] [--preview]   → video.mp4 + poster.jpg + sheet.jpg
//   node tools/render.mjs stills <piece-dir>                          → slides/slide-01.png … + sheet.jpg
//   node tools/render.mjs frame  <piece-dir> <t-seconds> [out.png]    → single frame (quick check)
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
    return { width: K.width || 1080, height: K.height || 1920, fps: K.fps || 30, duration: K.duration || 0, slides: document.querySelectorAll('.slide').length };
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

const t0 = Date.now();
const { browser, page, meta, errors } = await open();
try {
  if (mode === 'frame') {
    const t = parseFloat(rest[0] || '0');
    await seek(page, t);
    const out = rest[1] || path.join(dir, `frame-${t}.png`);
    await page.screenshot({ path: out });
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
    const posterT = meta.duration * 0.62; await seek(page, posterT);
    await page.screenshot({ path: path.join(dir, 'poster.jpg'), type: 'jpeg', quality: 90 });
    await sheet(path.join(tmp, 's%02d.jpg'), 0, shots.length, 6, path.join(dir, 'sheet.jpg'));
    const size = fs.statSync(out).size;
    console.log(JSON.stringify({ out, frames, fps, duration: meta.duration, width: meta.width, height: meta.height, mb: +(size / 1e6).toFixed(2), renderSeconds: (Date.now() - t0) / 1000 }));
  } else if (mode === 'stills') {
    const slides = await page.$$('.slide');
    if (!slides.length) throw new Error('stills mode needs one or more .slide elements');
    const outDir = path.join(dir, 'slides'); fs.mkdirSync(outDir, { recursive: true });
    for (const f of fs.readdirSync(outDir)) fs.unlinkSync(path.join(outDir, f));
    await page.setViewportSize({ width: meta.width, height: meta.height * slides.length });
    await seek(page, 0);
    const files = [];
    for (const [i, el] of slides.entries()) {
      const p = path.join(outDir, `slide-${String(i + 1).padStart(2, '0')}.png`);
      await el.screenshot({ path: p }); files.push(p);
    }
    await sheet(path.join(outDir, 'slide-%02d.png'), 1, files.length, Math.min(files.length, 5), path.join(dir, 'sheet.jpg'));
    console.log(JSON.stringify({ slides: files.length, width: meta.width, height: meta.height, renderSeconds: (Date.now() - t0) / 1000 }));
  } else throw new Error(`unknown mode ${mode}`);
  if (errors.length) { console.error('PAGE ERRORS:\n' + [...new Set(errors)].join('\n')); process.exitCode = 3; }
} finally { await browser.close(); }

#!/usr/bin/env python3
"""Synthesised sound design for Klipt pieces (deterministic, royalty-free, offline): transition effects and a
music bed, written as 48 kHz stereo WAV. Mix them with KLIPT.audio (see docs/RENDER_CONTRACT.md).

  python3 tools/sfx.py whoosh  pieces/<id>/audio/whoosh.wav [--dur 0.6]      air sweep for wipes / whip pans
  python3 tools/sfx.py riser   pieces/<id>/audio/riser.wav  [--dur 2.0]      tension build into a reveal
  python3 tools/sfx.py impact  pieces/<id>/audio/impact.wav                  sub hit + air for a logo / title slam
  python3 tools/sfx.py tick    pieces/<id>/audio/tick.wav                    UI click / counter tick
  python3 tools/sfx.py pop     pieces/<id>/audio/pop.wav                     bubbly pop for stickers, cards
  python3 tools/sfx.py shimmer pieces/<id>/audio/shimmer.wav [--dur 1.5]     bright chime for a logo or end card
  python3 tools/sfx.py glitch  pieces/<id>/audio/glitch.wav  [--dur 0.3]     digital stutter (tech / gaming)
  python3 tools/sfx.py bed     pieces/<id>/audio/bed.wav --dur 15 --bpm 112 [--mood bright|warm|dark|tech] [--drop 11.2]
       → music bed: pad chords + pluck arpeggio + kick/hat groove (+ optional stop at --drop s, then a big return)
Beat length = 60/bpm s: place cuts and SFX on beats (e.g. 112 bpm → a beat every 0.536 s) so picture and sound lock.
--seed changes the random texture; --gain scales the output (dB).
"""
import argparse, wave
import numpy as np
from scipy.signal import butter, sosfilt

SR = 48000

def env(n, a, r, shape=3.0):
    t = np.linspace(0, 1, n)
    e = np.minimum(1, t * n / max(1, a * SR)) * (1 - t) ** shape if r is None else np.minimum(1, t * n / max(1, a * SR))
    return e

def adsr(n, a, d, s, r):
    e = np.ones(n) * s
    A, D, R = int(a * SR), int(d * SR), int(r * SR)
    e[:A] = np.linspace(0, 1, A) if A else e[:A]
    e[A:A + D] = np.linspace(1, s, len(e[A:A + D]))
    if R: e[-R:] *= np.linspace(1, 0, len(e[-R:]))
    return e

def bp(x, lo, hi, order=2): return sosfilt(butter(order, [lo, hi], 'bandpass', fs=SR, output='sos'), x)
def lp(x, f, order=2): return sosfilt(butter(order, f, 'lowpass', fs=SR, output='sos'), x)
def hp(x, f, order=2): return sosfilt(butter(order, f, 'highpass', fs=SR, output='sos'), x)

def sweep_noise(rng, dur, f0, f1, width=0.6, chunks=48):
    """Noise through a band-pass whose centre moves from f0 to f1 (log), block-wise with crossfades."""
    n = int(dur * SR); x = rng.standard_normal(n); out = np.zeros(n)
    edges = np.linspace(0, n, chunks + 1).astype(int)
    for i in range(chunks):
        c = f0 * (f1 / f0) ** (i / (chunks - 1))
        a, b = edges[i], edges[i + 1]; pad = min(a, 2048)
        seg = bp(x[a - pad:b], max(30, c * (1 - width / 2)), min(SR / 2 - 100, c * (1 + width / 2)))[pad:]
        out[a:b] = seg
    return out

def stereo(x, width=0.0, rng=None):
    if not width: return np.stack([x, x], 1)
    d = int(0.012 * SR); r = np.concatenate([np.zeros(d), x[:-d]])
    return np.stack([x, (1 - width) * x + width * r], 1)

def norm(x, peak=0.9):
    m = np.max(np.abs(x)) or 1; return x / m * peak

def whoosh(a, rng):
    n = int(a.dur * SR); t = np.linspace(0, 1, n)
    x = sweep_noise(rng, a.dur, 300, 4200) * np.sin(np.pi * t) ** 1.6
    x += 0.5 * sweep_noise(rng, a.dur, 120, 900) * np.sin(np.pi * t) ** 2
    return stereo(norm(x, 0.8), 0.6)

def riser(a, rng):
    n = int(a.dur * SR); t = np.linspace(0, 1, n)
    x = sweep_noise(rng, a.dur, 200, 7000, 0.4) * t ** 2.2
    f = 110 * 2 ** (3 * t ** 1.5); ph = 2 * np.pi * np.cumsum(f) / SR
    x += 0.35 * np.sin(ph) * t ** 2 + 0.2 * np.sin(2 * ph) * t ** 3
    return stereo(norm(x, 0.8), 0.5)

def impact(a, rng):
    n = int(1.6 * SR); t = np.arange(n) / SR
    f = 38 + 90 * np.exp(-t * 18); sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.2)
    air = hp(rng.standard_normal(n), 2500) * np.exp(-t * 14) * 0.35
    body = lp(rng.standard_normal(n), 400) * np.exp(-t * 9) * 0.6
    return stereo(norm(np.tanh(1.6 * (sub + body + air)), 0.95), 0.3)

def tick(a, rng):
    n = int(0.06 * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 180) + 0.4 * hp(rng.standard_normal(n), 5000) * np.exp(-t * 400)
    return stereo(norm(x, 0.7))

def pop(a, rng):
    n = int(0.18 * SR); t = np.arange(n) / SR
    f = 380 + 900 * np.exp(-t * 40); x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 28)
    return stereo(norm(x, 0.75))

def shimmer(a, rng):
    n = int(a.dur * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for k, f in enumerate([1318.5, 1760.0, 2217.5, 2637.0, 3520.0]):
        d = int(k * 0.045 * SR); tt = t[:n - d]
        x[d:] += np.sin(2 * np.pi * f * tt) * np.exp(-tt * 2.6) * (0.9 ** k)
    x += 0.15 * hp(rng.standard_normal(n), 6000) * np.exp(-t * 6)
    return stereo(norm(x, 0.6), 0.7)

def glitch(a, rng):
    n = int(a.dur * SR); x = np.zeros(n); pos = 0
    while pos < n:
        L = int(rng.uniform(0.01, 0.05) * SR); f = rng.choice([220, 440, 880, 1760, 3520])
        seg = np.sign(np.sin(2 * np.pi * f * np.arange(L) / SR)) * rng.uniform(0.3, 1)
        x[pos:pos + L] = seg[:len(x[pos:pos + L])]; pos += L + int(rng.uniform(0, 0.02) * SR)
    return stereo(norm(lp(x, 6000), 0.55), 0.4)

MOODS = {  # chord roots (MIDI) and chord shapes per bar
    'bright': dict(prog=[(60, 'maj7'), (67, 'maj'), (69, 'm7'), (65, 'maj7')], cut=3200),
    'warm':   dict(prog=[(57, 'm7'), (65, 'maj7'), (60, 'maj'), (67, 'maj')], cut=2200),
    'dark':   dict(prog=[(57, 'm'), (53, 'maj'), (60, 'maj'), (55, 'maj')], cut=1600),
    'tech':   dict(prog=[(62, 'm7'), (58, 'maj7'), (65, 'maj'), (60, 'sus2')], cut=2800),
}
SHAPES = dict(maj=[0, 4, 7], m=[0, 3, 7], maj7=[0, 4, 7, 11], m7=[0, 3, 7, 10], sus2=[0, 2, 7])
hz = lambda m: 440 * 2 ** ((m - 69) / 12)

def saw(f, n, rng, detune=0.004):
    t = np.arange(n) / SR; x = np.zeros(n)
    for d in (-detune, 0, detune):
        ph = (f * (1 + d) * t + rng.uniform()) % 1; x += 2 * ph - 1
    return x / 3

def bed(a, rng):
    n = int(a.dur * SR); out = np.zeros((n, 2)); beat = 60 / a.bpm; bar = 4 * beat
    mood = MOODS[a.mood]; drop = a.drop
    def add(sig, start, pan=0.0, g=1.0):
        s = int(start * SR); e = min(n, s + len(sig))
        if e <= s: return
        seg = sig[:e - s] * g; out[s:e, 0] += seg * (1 - max(0, pan)); out[s:e, 1] += seg * (1 + min(0, pan))
    silent = lambda t: drop is not None and drop <= t < drop + beat * 2
    b = 0; t = 0.0
    while t < a.dur:
        root, shape = mood['prog'][b % len(mood['prog'])]
        L = int(bar * SR)
        pad = sum(saw(hz(root + iv), L, rng) for iv in SHAPES[shape]) / len(SHAPES[shape])
        pad = lp(pad, mood['cut']) * adsr(L, 0.25, 0.4, 0.7, 0.3)
        add(pad * 0.28, t, 0.0)
        add(lp(saw(hz(root - 24), L, rng, 0.002), 180) * adsr(L, 0.01, 0.2, 0.8, 0.05) * 0.45, t)   # bass
        notes = [root + 12 + SHAPES[shape][k % len(SHAPES[shape])] + (12 if k % 8 >= 4 else 0) for k in range(8)]
        for k, m in enumerate(notes):                                                            # pluck arp, 8ths
            tt = t + k * beat / 2
            if tt >= a.dur or silent(tt): continue
            Ln = int(beat * 0.9 * SR); tn = np.arange(Ln) / SR
            pl = (np.sin(2 * np.pi * hz(m) * tn) + 0.3 * np.sin(4 * np.pi * hz(m) * tn)) * np.exp(-tn * 9)
            add(pl * 0.16, tt, 0.35 if k % 2 else -0.35)
        for k in range(4):                                                                       # drums
            tt = t + k * beat
            if tt >= a.dur or silent(tt): continue
            Lk = int(0.35 * SR); tk = np.arange(Lk) / SR
            kick = np.sin(2 * np.pi * np.cumsum(45 + 110 * np.exp(-tk * 30)) / SR) * np.exp(-tk * 9)
            add(np.tanh(1.5 * kick) * 0.7, tt)
            Lh = int(0.05 * SR); th = np.arange(Lh) / SR
            hat = hp(rng.standard_normal(Lh), 7000) * np.exp(-th * 90)
            add(hat * 0.18, tt + beat / 2, 0.2)
            if k in (1, 3):
                Ls = int(0.2 * SR); ts = np.arange(Ls) / SR
                clap = bp(rng.standard_normal(Ls), 900, 4000) * np.exp(-ts * 22)
                add(clap * 0.25, tt, -0.1)
        b += 1; t += bar
    out = np.tanh(out * 1.2)
    fo = int(min(1.2, a.dur * 0.1) * SR); out[-fo:] *= np.linspace(1, 0, fo)[:, None]
    return norm(out, 0.85)

def write(path, x, gain_db):
    import os
    x = np.clip(x * 10 ** (gain_db / 20), -1, 1)
    os.makedirs(os.path.dirname(os.path.abspath(path)) or '.', exist_ok=True)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype('<i2').tobytes())

p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
p.add_argument('kind', choices=['whoosh', 'riser', 'impact', 'tick', 'pop', 'shimmer', 'glitch', 'bed']); p.add_argument('out')
p.add_argument('--dur', type=float); p.add_argument('--bpm', type=float, default=112); p.add_argument('--mood', default='bright', choices=list(MOODS))
p.add_argument('--drop', type=float); p.add_argument('--seed', type=int, default=1); p.add_argument('--gain', type=float, default=0)
a = p.parse_args()
a.dur = a.dur or dict(whoosh=0.6, riser=2.0, shimmer=1.5, glitch=0.3, bed=15).get(a.kind, 1)
x = globals()[a.kind](a, np.random.default_rng(a.seed))
write(a.out, x, a.gain)
print(f'{a.out}  {len(x) / SR:.2f}s' + (f'  beat={60 / a.bpm:.3f}s' if a.kind == 'bed' else ''))

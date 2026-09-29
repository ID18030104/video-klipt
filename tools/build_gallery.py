#!/usr/bin/env python3
"""Build gallery/ (data.json + light assets) from pieces/, bench/ and the cost/judgment results.
Usage: python3 tools/build_gallery.py <assignments.json> <costs.json>"""
import json, os, sys, subprocess, glob, shutil
assign = json.load(open(sys.argv[1]))          # {id: {config, set, brief_id?}}
costs = json.load(open(sys.argv[2]))
J = json.load(open('bench/results/judgments.json')) if os.path.exists('bench/results/judgments.json') else {'scores': [], 'ranks': []}
CONFIGS = {
 'A': dict(name='Sonnet seul', models=['Sonnet 5.5'], skill='aucun', pipeline='1 agent'),
 'B': dict(name='Sonnet + klipt-craft', models=['Sonnet 5.5'], skill='klipt-craft', pipeline='1 agent'),
 'C': dict(name='Opus seul', models=['Opus 5.5'], skill='aucun', pipeline='1 agent'),
 'D': dict(name='Opus + klipt-craft', models=['Opus 5.5'], skill='klipt-craft', pipeline='1 agent'),
 'E': dict(name='Opus DA → Sonnet', models=['Opus 5.5', 'Sonnet 5.5'], skill='klipt-craft', pipeline='directeur artistique → exécutant'),
 'F': dict(name='Sonnet → critique Opus → Sonnet', models=['Sonnet 5.5', 'Opus 5.5'], skill='klipt-craft', pipeline='exécutant → critique → correction'),
 'G': dict(name='Opus + taste-express', models=['Opus 5.5'], skill='taste-express', pipeline='1 agent'),
 'H': dict(name='Sonnet + taste-express', models=['Sonnet 5.5'], skill='taste-express', pipeline='1 agent'),
}
FF = 'ffmpeg'
out = 'gallery'; os.makedirs(f'{out}/a', exist_ok=True)
def run(*a): subprocess.run([FF, '-hide_banner', '-loglevel', 'error', '-y', *a], check=True)
per = {}
for r in costs:
    p = per.setdefault(r['piece'], dict(cost=0, seconds=0, out=0, inp=0, cache_read=0, cache_write=0, stages=[], done=True))
    p['done'] &= r['done']
    for k in ('cost', 'seconds', 'out', 'inp', 'cache_read', 'cache_write'): p[k] += r[k]
    p['stages'].append(dict(stage=r['stage'], model=r['model'], cost=round(r['cost'], 3), seconds=r['seconds'], out=r['out']))
rankpos = {}
for r in J['ranks']:
    for i, pid in enumerate(r['ranking']): rankpos[pid] = (i + 1, len(r['ranking']))
items = []
for pid, a in assign.items():
    d = f'pieces/{pid}'
    if not os.path.exists(f'{d}/meta.json') or not per.get(pid, {}).get('done'): continue  # skip pieces still in production
    meta = json.load(open(f'{d}/meta.json'))
    brief = json.load(open(f'bench/briefs/{pid}.json')) if os.path.exists(f'bench/briefs/{pid}.json') else {}
    ad = f'{out}/a/{pid}'; os.makedirs(ad, exist_ok=True)
    it = dict(id=pid, set=a['set'], brief_id=a.get('brief_id'), config=a['config'], brand=brief.get('brand', meta.get('brand')),
              sector=brief.get('sector', meta.get('sector')), kind=brief.get('kind', meta.get('kind')), format=brief.get('format', meta.get('format')),
              lang=brief.get('lang', 'fr'), title=meta.get('title'), concept=meta.get('concept'), techniques=meta.get('techniques', []),
              fonts=meta.get('fonts', []), palette=meta.get('palette', []), duration=meta.get('duration'), brief=brief.get('brief'))
    w, h = map(int, (it['format'] or '1080x1920').split('x'))
    if os.path.exists(f'{d}/video.mp4'):
        if not os.path.exists(f'{ad}/v.mp4'):
            run('-i', f'{d}/video.mp4', '-vf', 'scale=540:-2', '-c:v', 'libx264', '-crf', '27', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-an', f'{ad}/v.mp4')
            run('-i', f'{d}/poster.jpg', '-vf', 'scale=540:-2', '-q:v', '4', f'{ad}/t.jpg')
        it['video'] = f'a/{pid}/v.mp4'; it['thumb'] = f'a/{pid}/t.jpg'
    slides = sorted(glob.glob(f'{d}/slides/*.png'))
    if slides:
        it['slides'] = []
        for i, s in enumerate(slides):
            o = f'{ad}/s{i+1:02d}.jpg'
            if not os.path.exists(o): run('-i', s, '-vf', 'scale=720:-2', '-q:v', '4', o)
            it['slides'].append(f'a/{pid}/s{i+1:02d}.jpg')
        it['thumb'] = it['slides'][0]
    if os.path.exists(f'{d}/sheet.jpg'):
        if not os.path.exists(f'{ad}/sheet.jpg'): run('-i', f'{d}/sheet.jpg', '-vf', 'scale=1400:-2', '-q:v', '5', f'{ad}/sheet.jpg')
        it['sheet'] = f'a/{pid}/sheet.jpg'
    c = per.get(pid)
    if c: it['metrics'] = dict(cost=round(c['cost'], 2), minutes=round(c['seconds'] / 60, 1), out=c['out'], inp=c['inp'] + c['cache_read'] + c['cache_write'], stages=c['stages'])
    js = [s for s in J['scores'] if s['id'] == pid]
    if js:
        keys = ['brand_fit', 'art_direction', 'typography', 'composition', 'copy_quality', 'storytelling', 'technical_polish', 'originality', 'overall']
        it['judges'] = [{k: s.get(k) for k in keys + ['judge', 'client_ready', 'verdict', 'defects']} for s in js]
        it['score'] = round(sum(s['overall'] for s in js) / len(js), 2)
    if pid in rankpos: it['rank'] = rankpos[pid]
    items.append(it)
ranks = [dict(brief_id=assign[r['ranking'][0]].get('brief_id'), ranking=r['ranking'], rationale=r['rationale']) for r in J['ranks']]
json.dump(dict(configs=CONFIGS, items=items, ranks=ranks), open(f'{out}/data.json', 'w'), ensure_ascii=False)
print(len(items), 'items;', sum(1 for i in items if 'judges' in i), 'judged')

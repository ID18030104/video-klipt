#!/usr/bin/env python3
"""Final comparison of configurations: quality (blind judges), API cost, time, tokens.
Usage: python3 tools/analyze.py <assignments.json> <costs.json> <main-transcript.jsonl>
Writes bench/results/summary.json. Prints a markdown summary."""
import json, sys, statistics as st
from collections import defaultdict
sys.path.insert(0, 'tools')
from metrics import agent_metrics
A = json.load(open(sys.argv[1])); C = json.load(open(sys.argv[2])); main = agent_metrics(sys.argv[3])
J = json.load(open('bench/results/judgments.json'))
BR = {p: json.load(open(f'bench/briefs/{p}.json')) for p in A}
# pieces whose final agent reused files from an attempt cut short by the container restart:
# their cost/time is understated, so they are excluded from cost & time averages (kept for quality).
REUSED = {'p279', 'p213', 'p289', 'p245', 'p286', 'p275', 'p258', 'p283', 'p267', 'p273'}
NAMES = {'A': 'Sonnet seul', 'B': 'Sonnet + klipt-craft', 'C': 'Opus seul', 'D': 'Opus + klipt-craft', 'E': 'Opus DA → Sonnet',
         'F': 'Sonnet → critique Opus → Sonnet', 'G': 'Opus + taste-express', 'H': 'Sonnet + taste-express'}
mean = lambda xs: round(st.mean(xs), 2) if xs else None
piece = defaultdict(lambda: dict(cost=0, seconds=0, out=0, inp=0, cr=0, cw=0))
lost = judge_cost = 0
for r in C:
    if r['label'].startswith(('judge', 'rank')): judge_cost += r['cost']; continue
    if not r['done']: lost += r['cost']; continue
    p = piece[r['piece']]
    p['cost'] += r['cost']; p['seconds'] += r['seconds']; p['out'] += r['out']; p['inp'] += r['inp']; p['cr'] += r['cache_read']; p['cw'] += r['cache_write']
sc = defaultdict(list)
for s in J['scores']: sc[s['id']].append(s)
rank = {pid: i + 1 for r in J['ranks'] for i, pid in enumerate(r['ranking'])}
rows = {}
for c in NAMES:
    ids = [p for p in A if A[p]['config'] == c]
    costed = [p for p in ids if p not in REUSED and p in piece]
    son = [s['overall'] for p in ids for s in sc[p] if s['judge'] == 'sonnet']
    son_v = [s['overall'] for p in ids if BR[p]['kind'] == 'video' for s in sc[p] if s['judge'] == 'sonnet']
    son_s = [s['overall'] for p in ids if BR[p]['kind'] != 'video' for s in sc[p] if s['judge'] == 'sonnet']
    ready = [s['client_ready'] for p in ids for s in sc[p] if s['judge'] == 'sonnet']
    bench = [p for p in ids if A[p]['set'] == 'bench']
    crit = defaultdict(list)
    for p in ids:
        for s in sc[p]:
            if s['judge'] == 'sonnet':
                for k in ('brand_fit', 'art_direction', 'typography', 'composition', 'copy_quality', 'storytelling', 'technical_polish', 'originality'): crit[k].append(s[k])
    rows[c] = dict(config=c, name=NAMES[c], pieces=len(ids), videos=sum(BR[p]['kind'] == 'video' for p in ids),
        score_sonnet_all=mean(son), score_video=mean(son_v), score_stills=mean(son_s),
        client_ready_pct=round(100 * sum(ready) / len(ready)) if ready else None,
        bench_score_opus=mean([s['overall'] for p in bench for s in sc[p] if s['judge'] == 'opus']),
        bench_score_both=mean([s['overall'] for p in bench for s in sc[p]]), bench_rank=mean([rank[p] for p in bench if p in rank]),
        cost_per_piece=mean([piece[p]['cost'] for p in costed]), cost_video=mean([piece[p]['cost'] for p in costed if BR[p]['kind'] == 'video']),
        cost_stills=mean([piece[p]['cost'] for p in costed if BR[p]['kind'] != 'video']),
        minutes_per_piece=mean([piece[p]['seconds'] / 60 for p in costed]),
        out_tokens_per_piece=round(mean([piece[p]['out'] for p in costed]) or 0),
        in_tokens_per_piece=round(mean([piece[p]['inp'] + piece[p]['cr'] + piece[p]['cw'] for p in costed]) or 0),
        cost_total=round(sum(piece[p]['cost'] for p in ids if p in piece), 2),
        criteria={k: mean(v) for k, v in crit.items()})
    r = rows[c]; r['score_per_dollar'] = round(r['score_sonnet_all'] / r['cost_per_piece'], 1) if r['cost_per_piece'] else None
prod_cost = sum(v['cost'] for v in piece.values())
tot = dict(pieces=len(A), production_cost=round(prod_cost, 2), judging_cost=round(judge_cost, 2), lost_to_restart=round(lost, 2),
           orchestration_cost=round(main['cost'], 2), total=round(prod_cost + judge_cost + lost + main['cost'], 2),
           orchestration_out_tokens=main['out'], orchestration_cache_read=main['cr'])
# judge agreement on bench pieces
pairs = [(min(v, key=lambda s: s['judge'])['overall'], max(v, key=lambda s: s['judge'])['overall']) for v in sc.values() if len(v) == 2]
tot['judge_pairs'] = len(pairs); tot['judge_mean_abs_diff'] = mean([abs(a - b) for a, b in pairs])
by_model = {}
for label, cfgs in {'Sonnet 5.5 seul (A,B,H)': 'ABH', 'Opus 5.5 seul (C,D,G)': 'CDG', 'Mixte Opus+Sonnet (E,F)': 'EF'}.items():
    ids = [p for p in A if A[p]['config'] in cfgs]
    by_model[label] = dict(score=mean([s['overall'] for p in ids for s in sc[p] if s['judge'] == 'sonnet']),
                           cost=mean([piece[p]['cost'] for p in ids if p not in REUSED and p in piece]),
                           minutes=mean([piece[p]['seconds'] / 60 for p in ids if p not in REUSED and p in piece]))
by_skill = {}
for label, cfgs in {'aucun skill (A,C)': 'AC', 'klipt-craft (B,D)': 'BD', 'taste-express (G,H)': 'GH'}.items():
    ids = [p for p in A if A[p]['config'] in cfgs]
    by_skill[label] = dict(score=mean([s['overall'] for p in ids for s in sc[p] if s['judge'] == 'sonnet']),
                           cost=mean([piece[p]['cost'] for p in ids if p not in REUSED and p in piece]))
top = sorted([dict(id=p, brand=BR[p]['brand'], kind=BR[p]['kind'], config=A[p]['config'], score=mean([s['overall'] for s in sc[p]])) for p in A if sc[p]],
             key=lambda x: -x['score'])[:12]
out = dict(configs=rows, totals=tot, by_model=by_model, by_skill=by_skill, top=top, reused_excluded_from_cost=sorted(REUSED))
json.dump(out, open('bench/results/summary.json', 'w'), ensure_ascii=False, indent=1)
f = lambda x, d=2: '—' if x is None else f'{x:.{d}f}'.replace('.', ',')
print('| Config | Pièces | Note (juge Sonnet, 74 pièces) | Vidéo | Stills | Publiable | Banc: note 2 juges | Banc: rang | $/pièce | $/vidéo | min/pièce | tokens sortie | note/$ |')
print('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for c, r in rows.items():
    print(f"| {c} — {r['name']} | {r['pieces']} | {f(r['score_sonnet_all'])} | {f(r['score_video'])} | {f(r['score_stills'])} | {r['client_ready_pct']} % | {f(r['bench_score_both'])} | {f(r['bench_rank'],1)} | {f(r['cost_per_piece'])} | {f(r['cost_video'])} | {f(r['minutes_per_piece'],0)} | {r['out_tokens_per_piece']:,} | {f(r['score_per_dollar'],1)} |")
print(json.dumps(dict(totals=tot, by_model=by_model, by_skill=by_skill), ensure_ascii=False, indent=1))

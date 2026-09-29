#!/usr/bin/env python3
"""Join workflow journals (agentId → label "piece·config·stage") with transcript metrics.
Usage: python3 tools/bench_costs.py <workflows-dir> [--json out.json]"""
import json, sys, os, glob
sys.path.insert(0, os.path.dirname(__file__))
from metrics import agent_metrics
root = sys.argv[1]
rows = []
for j in glob.glob(os.path.join(root, '*', 'journal.jsonl')):
    wf = os.path.dirname(j)
    done = set()
    labels = {}
    for l in open(j):
        d = json.loads(l)
        if d['type'] == 'started': labels[d['agentId']] = d['label']
        if d['type'] == 'result': done.add(d['agentId'])
    for aid, label in labels.items():
        f = os.path.join(wf, f'agent-{aid}.jsonl')
        if not os.path.exists(f): continue
        m = agent_metrics(f)
        parts = label.split('·')
        rows.append(dict(workflow=os.path.basename(wf), agent=aid, label=label, piece=parts[-3] if len(parts) >= 3 else '',
                         config=parts[-2] if len(parts) >= 3 else '', stage=parts[-1], done=aid in done,
                         model=','.join(m['models']), seconds=m['seconds'], calls=m['calls'], out=m['out'], thinking=m['thinking'],
                         inp=m['inp'], cache_read=m['cr'], cache_write=m['cw5'] + m['cw1h'], cost=round(m['cost'], 4)))
if '--json' in sys.argv:
    json.dump(rows, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
pieces = {}
for r in rows:
    p = pieces.setdefault(r['piece'], dict(config=r['config'], cost=0, seconds=0, out=0, done=True, stages=0))
    p['cost'] += r['cost']; p['seconds'] += r['seconds']; p['out'] += r['out']; p['done'] &= r['done']; p['stages'] += 1
for k, p in sorted(pieces.items(), key=lambda x: (x[1]['config'], x[0])):
    print(f"{k:6} {p['config']:2} {'done' if p['done'] else 'RUN ':4} ${p['cost']:6.2f} {p['seconds']/60:5.1f} min out={p['out']}")
print('TOTAL $%.2f' % sum(r['cost'] for r in rows))

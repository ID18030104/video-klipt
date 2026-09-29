#!/usr/bin/env python3
"""Collect judge scores / rankings from workflow journals into bench/results/judgments.json."""
import json, glob, os, sys
root = sys.argv[1]
scores, ranks = [], []
for j in glob.glob(os.path.join(root, '*', 'journal.jsonl')):
    labels = {}
    for l in open(j):
        d = json.loads(l)
        if d['type'] == 'started': labels[d['agentId']] = d['label']
        if d['type'] == 'result' and d.get('result'):
            lab = labels.get(d['agentId'], '')
            if lab.startswith('judge·'):
                _, judge, pid = lab.split('·'); r = dict(d['result']); r.update(id=pid, judge=judge); scores.append(r)
            elif lab.startswith('rank·'):
                ranks.append(d['result'])
os.makedirs('bench/results', exist_ok=True)
json.dump({'scores': scores, 'ranks': ranks}, open('bench/results/judgments.json', 'w'), ensure_ascii=False, indent=1)
print(len(scores), 'scores,', len(ranks), 'rankings')

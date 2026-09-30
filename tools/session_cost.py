#!/usr/bin/env python3
"""API-equivalent cost of the main (orchestrating) session between two times, from its transcript.
Main-loop messages carry exact final usage. Usage: python3 tools/session_cost.py <transcript.jsonl> <since ISO> [<until ISO>]"""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from metrics import price_for
f, since = sys.argv[1], sys.argv[2]; until = sys.argv[3] if len(sys.argv) > 3 else '9999'
seen, tot = {}, dict(inp=0, out=0, cr=0, cw5=0, cw1h=0, cost=0.0, calls=0)
for line in open(f):
    try: d = json.loads(line)
    except json.JSONDecodeError: continue
    ts = d.get('timestamp', '')
    if d.get('type') != 'assistant' or not (since <= ts[:19] <= until): continue
    m = d.get('message', {}); u = m.get('usage'); mid = m.get('id')
    if not u or not mid: continue
    seen[mid] = (m.get('model'), u)          # last line of a message holds its final usage
for model, u in seen.values():
    _, p = price_for(model)
    if not p: continue
    cc = u.get('cache_creation') or {}
    cw1h = cc.get('ephemeral_1h_input_tokens', 0); cw5 = cc.get('ephemeral_5m_input_tokens', u.get('cache_creation_input_tokens', 0) - cw1h)
    r = dict(inp=u.get('input_tokens', 0), out=u.get('output_tokens', 0), cr=u.get('cache_read_input_tokens', 0), cw5=cw5, cw1h=cw1h)
    for k in r: tot[k] += r[k]
    tot['cost'] += sum(r[k] * p[k] for k in r) / 1e6; tot['calls'] += 1
tot['cost'] = round(tot['cost'], 4)
print(json.dumps(tot))

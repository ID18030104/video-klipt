#!/usr/bin/env python3
"""Token / time / API-cost accounting from Claude Code transcripts (.jsonl).

Usage: python3 tools/metrics.py <file-or-dir> [...] [--json]
Each .jsonl = one agent. Usage is deduplicated per API message id (a response is
split over several transcript lines that repeat the same usage block).
Prices: Anthropic first-party list prices, USD per million tokens.

Output tokens: sub-agent transcripts only store the usage snapshot taken when the
response *starts* (input and cache figures are exact, output_tokens is a stub), and
thinking text is omitted (only its encrypted signature is kept). For those messages
output tokens are ESTIMATED with a linear model fitted on this session's main-loop
messages, where exact final usage is recorded (see FIT below; ~±15 % per agent).
"""
import json, sys, os, glob
from datetime import datetime

PRICES = {  # input, output, cache write 5m, cache write 1h, cache read
    'claude-opus-5-5':   dict(inp=4.0, out=20.0, cw5=5.0,  cw1h=8.0, cr=0.20),
    'claude-sonnet-5-5': dict(inp=2.0, out=10.0, cw5=2.5,  cw1h=4.0, cr=0.20),
    'claude-haiku-4-5':  dict(inp=1.0, out=5.0,  cw5=1.25, cw1h=2.0, cr=0.10),
}

# Fitted on main-loop messages (exact usage): thinking ≈ a·len(signature)+b ; visible ≈ c·chars + d·tool_calls
FIT = dict(a=0.2865, b=-226.7, c=0.4572, d=59.4)

def estimate_out(content):
    sig = vis = tools = 0
    for c in content or []:
        if c.get('type') == 'thinking': sig += len(c.get('signature', ''))
        elif c.get('type') == 'text': vis += len(c.get('text', ''))
        elif c.get('type') == 'tool_use': vis += len(json.dumps(c.get('input'), ensure_ascii=False)); tools += 1
    th = max(0.0, FIT['a'] * sig + FIT['b']) if sig else 0.0
    return int(th + FIT['c'] * vis + FIT['d'] * tools), int(th)

def price_for(model):
    for k, v in PRICES.items():
        if model and model.startswith(k):
            return k, v
    return model, None

def ts(s):
    return datetime.fromisoformat(s.replace('Z', '+00:00'))

def agent_metrics(path):
    seen, first_user, times = {}, None, []
    for line in open(path, encoding='utf-8'):
        try: d = json.loads(line)
        except Exception: continue
        if d.get('timestamp'): times.append(ts(d['timestamp']))
        m = d.get('message') or {}
        if first_user is None and d.get('type') == 'user':
            c = m.get('content')
            first_user = c if isinstance(c, str) else ' '.join(x.get('text', '') for x in (c or []) if isinstance(x, dict))
        u = m.get('usage')
        if d.get('type') == 'assistant' and u:
            key = m.get('id') or d.get('requestId') or d.get('uuid')
            prev = seen.get(key)
            content = (prev[2] if prev else []) + (m.get('content') or [])
            seen[key] = (m.get('model'), u, content, bool(d.get('isSidechain')))
    tot = dict(inp=0, out=0, cw5=0, cw1h=0, cr=0, thinking=0, calls=0, cost=0.0)
    models = {}
    est = False
    for model, u, content, side in seen.values():
        if model == '<synthetic>': continue
        th_est = None
        if side:  # usage snapshot from stream start: estimate output from content
            u = dict(u); u['output_tokens'], th_est = estimate_out(content); est = True
        cc = u.get('cache_creation') or {}
        cw1h = cc.get('ephemeral_1h_input_tokens', 0)
        cw5 = cc.get('ephemeral_5m_input_tokens', u.get('cache_creation_input_tokens', 0) - cw1h)
        row = dict(inp=u.get('input_tokens', 0), out=u.get('output_tokens', 0), cw5=cw5, cw1h=cw1h,
                   cr=u.get('cache_read_input_tokens', 0))
        name, p = price_for(model)
        cost = sum(row[k] * p[k] for k in row) / 1e6 if p else 0.0
        for k in row: tot[k] += row[k]
        tot['thinking'] += th_est if th_est is not None else (u.get('output_tokens_details') or {}).get('thinking_tokens', 0)
        tot['calls'] += 1; tot['cost'] += cost
        models[name] = models.get(name, 0) + 1
    dur = (max(times) - min(times)).total_seconds() if times else 0
    return dict(file=path, out_estimated=est, models=models, seconds=round(dur), prompt_head=(first_user or '')[:300], **tot)

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    files = []
    for a in args:
        files += sorted(glob.glob(os.path.join(a, '**', '*.jsonl'), recursive=True)) if os.path.isdir(a) else [a]
    rows = [agent_metrics(f) for f in files]
    if '--json' in sys.argv:
        print(json.dumps(rows, indent=1)); return
    T = dict(cost=0, inp=0, out=0, cr=0, cw=0)
    for r in rows:
        cw = r['cw5'] + r['cw1h']
        print(f"{os.path.basename(r['file'])[:40]:40} {','.join(r['models']):28} {r['seconds']:6}s calls={r['calls']:4} "
              f"out={r['out']:8} cr={r['cr']:10} cw={cw:8} ${r['cost']:.3f}")
        T['cost'] += r['cost']; T['inp'] += r['inp']; T['out'] += r['out']; T['cr'] += r['cr']; T['cw'] += cw
    print(f"TOTAL {len(rows)} agents  out={T['out']} cache_read={T['cr']} cache_write={T['cw']} input={T['inp']}  ${T['cost']:.2f}")

if __name__ == '__main__':
    main()

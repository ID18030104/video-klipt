"""Shared Higgsfield budget ledger (/root/klipt-state/hf_budget.json), safe for parallel agents.

reserve(usd, label) takes the money *before* the request under an exclusive file lock and refuses to
overspend; refund(usd, label) gives it back if the request fails (Higgsfield does not bill failures).
"""
import fcntl, json, os, sys
from contextlib import contextmanager

LEDGER = '/root/klipt-state/hf_budget.json'

@contextmanager
def _locked():
    fd = os.open(LEDGER + '.lock', os.O_CREAT | os.O_RDWR)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        data = json.load(open(LEDGER)) if os.path.exists(LEDGER) else None
        yield data
        if data is not None:
            tmp = LEDGER + '.tmp'; json.dump(data, open(tmp, 'w'), indent=1); os.replace(tmp, LEDGER)
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN); os.close(fd)

def reserve(usd, label):
    with _locked() as d:
        if d is None: return
        if usd > d['remaining_usd'] + 1e-9:
            sys.exit(f'BUDGET GUARD: this request costs ${usd:.3f} but only ${d["remaining_usd"]:.3f} remains. Not generated.')
        d['remaining_usd'] = round(d['remaining_usd'] - usd, 4); d.setdefault('log', []).append(dict(out=label, usd=usd))

def refund(usd, label):
    with _locked() as d:
        if d is None: return
        d['remaining_usd'] = round(d['remaining_usd'] + usd, 4); d.setdefault('log', []).append(dict(out=label, usd=-usd, refund=True))

# review_workbench — the peer-review surface (one object, full context)

One object's full review context on ONE screen: its state + downstream impact + the decision surface.
This is the vision's "show me exactly what changes if I reject this" (globalplan Phase 11).

## Run
```bash
cd /root/patalacheckpoints
PYTHONPATH=pipeline python3 pipeline/products/review_workbench/test.py   # 6/6 proof
PYTHONPATH=pipeline python3 pipeline/products/review_workbench/engine.py demo
```

## Engine API
```python
from products.review_workbench.engine import open_workbench, decide
wb = open_workbench(ref, ident)   # state + downstream + decision surface
dec = decide(ref, ident, "ACCEPT", "sound", sign=True)   # through the review gate
```

## Why it matters
Composes context_bundle + impact + scholar_review into the actual reviewing surface. A scholar sees
what changes before committing. The decision goes through the gate (authorized scholar only).

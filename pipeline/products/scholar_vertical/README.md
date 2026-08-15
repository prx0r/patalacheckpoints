# scholar_vertical — the Scholar Attestation Vertical (the anti-theatre proof)

The FRONTIER-MAP's Layer-08 gap, operationalized: "a real scholar adjudicates one gold argument at the
right epistemic level, and the correction PROPAGATES through the graph."

Walks ONE real IPVV object end-to-end: pick → review (decision) → attest (Ed25519) → propagate (impact)
→ profile records → publish. This is the proof the whole scholar product works on real data.

## Run
```bash
cd /root/patalacheckpoints
PYTHONPATH=pipeline python3 pipeline/products/scholar_vertical/test.py   # 5/5 proof
PYTHONPATH=pipeline python3 pipeline/products/scholar_vertical/engine.py ACCEPT
```

## Engine API
```python
from products.scholar_vertical.engine import run_vertical
r = run_vertical(decision="ACCEPT")   # -> {target, workbench, decision, propagation, profile, published}
```

## Why it matters
The operational proof of human authority: a review + attestation on a real object, and the system knows
what downstream changes. The correction is recorded and published — not just engineered.

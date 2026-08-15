# claim — Claim (#4)

A **standalone** engine: real IPVV C1 passage → a Proposition with an HONEST epistemic envelope. The
proposition floor beneath Argument.

## What it enforces (the anti-theatre core)
- **Three epistemic statuses kept visibly distinct** (never inflated):
  `SOURCE-SAYS` (→ SCHOLARLY_CORROBORATED) · `SCHOLAR-RECONSTRUCTS` (→ PRELIMINARY) ·
  `PĀṬALA-INFERS` (→ **MACHINE_PROPOSED**, the honest default).
- **Honest scope/modality** — never over-generalize a passage-local claim.
- **Deterministic gate** flags genuine inflation (a NECESSITY claim without body necessity language).

## Run
```bash
cd /root/patalacheckpoints
PYTHONPATH=pipeline python3 pipeline/products/claim/test.py      # 7/7 proof
PYTHONPATH=pipeline python3 pipeline/products/claim/engine.py    # all 49 claims
```

## Engine API
```python
from products.claim.engine import claims, gate_scope, make_claim
from products._shared import ipvv
cs = claims()                              # 49 real claims (PĀṬALA-INFERS)
g = [gate_scope(c) for c in cs]            # apply the honesty gate
src = make_claim(ipvv.passages()[0], "SOURCE-SAYS")   # raise ceiling with a real source
```

## Honest limits
- Thesis extraction is the first substantive C1 sentence (real text, but a real extractor is future).
- The ceiling is honest but the *authority* is machine-proposed — only a scholar/review event raises it.

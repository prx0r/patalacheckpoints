# crux — Crux (#6)

A **standalone** engine that computes the minimal divergence between two real IPVV arguments — the
smallest load-bearing disagreement a targeted research task should attack.

## Run
```bash
cd /root/patalacheckpoints
PYTHONPATH=pipeline python3 pipeline/products/crux/test.py    # 4/4 proof
PYTHONPATH=pipeline python3 pipeline/products/crux/engine.py ARG:...A ARG:...B
PYTHONPATH=pipeline python3 pipeline/products/crux/engine.py            # list argument ids
```

## Engine API
```python
from products.crux.engine import crux_between
cx = crux_between("ARG:pt:passage:ipvv:chunkA-svatyandya.md",
                  "ARG:pt:passage:ipvv:chunkB-eligibility-gita.md")
```

## Honest limits
- Divergence = symmetric difference of premise/thesis sets; no semantic embedding. Fine for crux
  surfacing; a semantic-difference pass is a later improvement.

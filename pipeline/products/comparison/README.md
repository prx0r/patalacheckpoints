# comparison — Comparison (#13)

A **standalone** structured-comparison engine: two real IPVV arguments → AGREEMENT or REAL CRUX, with
the shared + divergent premises.

## Run
```bash
cd /root/patalacheckpoints
PYTHONPATH=pipeline python3 pipeline/products/comparison/test.py   # 3/3 proof
PYTHONPATH=pipeline python3 pipeline/products/comparison/engine.py ARG:...A ARG:...B
```

## Engine API
```python
from products.comparison.engine import compare_between
cmp = compare_between("ARG:pt:passage:ipvv:chunkA-svatyandya.md",
                      "ARG:pt:passage:ipvv:chunkB-eligibility-gita.md")
```

## Honest limits
- Classification is structural (divergence present/absent); a semantic/scope-difference pass
  (APPARENT DISAGREEMENT, TERMINOLOGICAL DIFFERENCE, SCOPE DIFFERENCE) is a later refinement.

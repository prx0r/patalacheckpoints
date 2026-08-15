# argument — Argument (#5)

A **standalone** argument-derivation engine: real IPVV C1 passage → thesis + premises + inference +
defeaters (AIF-style). Derived from the REAL C1 body, never hand-fed.

## Run
```bash
cd /root/patalacheckpoints
PYTHONPATH=pipeline python3 pipeline/products/argument/test.py        # 6/6 proof
PYTHONPATH=pipeline python3 pipeline/products/argument/engine.py      # all
PYTHONPATH=pipeline python3 pipeline/products/argument/engine.py "ARG:pt:passage:ipvv:chunkD-memory-pramana.md"
```

## Engine API
```python
from products.argument.engine import arguments
args = arguments()   # all 49
args = arguments("ARG:pt:passage:ipvv:chunkD-memory-pramana.md")
```

## Honest limits
- Structure is derived (abduction); formal validity/soundness checking (ASPIC+/AIF) is not wired.
- Premises come from the C1's first sentences — a real premise-extractor is a later improvement.

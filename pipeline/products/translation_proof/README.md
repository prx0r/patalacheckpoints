# translation_proof — Translation Proof (#2, the moat)

A **standalone** non-aggregate audit vector + publication gate over REAL IPVV passages.

## Why it's the moat
No single "quality = 94%" score. Ten independent dimensions; the publication gate **BLOCKs** on any
failing dimension. A scholar sees exactly *which* dimension fails, never a mushy average.

## Run
```bash
cd /root/patalacheckpoints
PYTHONPATH=pipeline python3 pipeline/products/translation_proof/test.py        # 6/6 proof
PYTHONPATH=pipeline python3 pipeline/products/translation_proof/engine.py      # all passages
PYTHONPATH=pipeline python3 pipeline/products/translation_proof/engine.py "pt:passage:ipvv:chunkD-memory-pramana.md"
```

## Engine API
```python
from products.translation_proof.engine import translation_proofs
proofs = translation_proofs()               # all
proofs = translation_proofs("pt:passage:ipvv:chunkD-memory-pramana.md")
```

## Honest limits
- Audit dims are derived from the L200 proof + structural coverage; live external auditors
  (xCOMET/MQM/Vidyut) are not wired yet.
- SOURCE_COVERAGE is currently low on full passages (a whole passage source vs its L2 summary) — the
  gate honestly BLOCKs; a real token-aligned coverage is a later improvement.

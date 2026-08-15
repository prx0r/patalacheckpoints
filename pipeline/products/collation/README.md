# collation — witness → variant apparatus (critical edition)

A **standalone** engine that turns N witness transcriptions of a Sanskrit passage into a **variant
apparatus** — which siglum reads what at each locus. Steals Saktumiva's critical-edition process
(`chchch/upama`): compare witnesses by segment, surface variants per siglum.

## Run
```bash
cd /root/patalacheckpoints
PYTHONPATH=pipeline python3 pipeline/products/collation/test.py   # 7/7 proof
PYTHONPATH=pipeline python3 pipeline/products/collation/engine.py demo
```

## Engine API
```python
from products.collation.engine import collate
r = collate({"W1": "kālī tu bhairavārūḍhā ...", "W2": "kālīṃ tu ..."}, base_siglum="W1")
# -> {base, witnesses[], variant_loci, apparatus: [{locus, base, variants: [{siglum, reading}]}]}
```

## Why it matters
Completes the manuscript→critical-text path: after OCR (kraken) produces witness transcriptions
(`manuscript_ingest` routes + scores them), **collation** turns multiple witnesses into the variant
apparatus a critical edition needs. The witness→variant→editorial-decision chain from vision-14.

## Honest limits
- The alignment is lightweight (token-position matching, not full LCS) — good enough to surface
  variants deterministically.
- It's MACHINE_PROPOSED: it surfaces variants; an editor/scholar decides the reading.

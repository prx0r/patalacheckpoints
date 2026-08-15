# tension_finder — the vision's /find-interesting-tension

The headline research function from vision-07: instead of finding "the answer," surface WHERE
interpretations diverge — the places papers come from. Embeds the LOGICVID curiosity markers
(distinction-forensics, live-issue isolation, doctrinal shift, contradiction, crux) on real IPVV.

## Kinds detected (67 tensions, 5 kinds)
CONTRADICTION · CRUX · DISTINCTION · DOCTRINAL_SHIFT · LIVE_ISSUE

## Run
```bash
cd /root/patalacheckpoints
PYTHONPATH=pipeline python3 pipeline/products/tension_finder/test.py          # 6/6 proof
PYTHONPATH=pipeline python3 pipeline/products/tension_finder/engine.py 0 20   # all, top 20
```

## Engine API
```python
from products.tension_finder.engine import find_tensions
r = find_tensions(kinds=["CRUX"], min_score=0.5, limit=10)
```

## Why it matters
"AI as a generator of research questions, not answers." Each tension is typed + scored + carries the
quote/why. Surfaces where intelligent interpretations diverge — MACHINE_PROPOSED, never a verdict.

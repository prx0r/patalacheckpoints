# timeline — Timeline

The diachronic Śiva source-tree: schools/traditions laid across time (genealogy + prehistory +
philosophical interlocutors). Consumes the REAL curated `data/atlas/historyTimeline.json`
(schema `patala:history-timeline:v1`). CPU-only, deterministic.

## What it provides
- `schools()` — all schools/traditions with period + era
- `school(id)` — one school's full record + influences
- `lineage(id)` — the ancestor chain (parent links)
- `era_breakdown()` — schools grouped by epistemic era (textual/comparative/archaeological)
- `timeline()` — the full chronological map (schools + chains + hop roadmap)

## Run
```bash
cd /root/patalacheckpoints
python3 pipeline/products/timeline/test.py          # 5/5 proof
python3 pipeline/products/timeline/engine.py eras
python3 pipeline/products/timeline/engine.py lineage trika
```

## Engine API
```python
from products.timeline.engine import schools, school, lineage, era_breakdown, timeline
tl = timeline()                       # 23 schools + chains + hop roadmap
chain = lineage("trika")              # 11 ancestors, proto_indoeuropean -> trika
eras = era_breakdown()                # {textual, comparative, archaeological}
```

## Real result (trika lineage)
`proto_indoeuropean <- proto_indo_iranian <- vedic_rudra <- sakta_svetasvatara <- epic_siva <-
pasupata <- mantramarga <- bhairava <- vidyapitha <- kaula <- trika` — the full 11-ancestor genealogy.

## Honest limits
- The data is the curated Śaiva-before-Abhinava genealogy (vision-11); 23 schools currently.
- Reconstruction (proto-* schools) is marked `comparative` era — never presented as textual fact.

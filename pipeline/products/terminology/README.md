# terminology — Terminology / Lemma-through-time

The diachronic sense-trajectory product: how a technical lemma's meaning shifts across traditions and
periods. Consumes the REAL curated `data/corpus/trajectories.json` (converted from `trajectories.ts`) +
`data/terms.json` (accepted senses). CPU-only, deterministic.

## What it provides
- `lemma_history(lemma)` — the diachronic nodes (period/tradition/sense/claim/evidence)
- `sense_trajectory(lemma)` — the chronological sense-shift
- `evidence_for(lemma, node_id)` — the passage/resource evidence supporting a sense

The data is curated interpretation ("Sense"/"Synthesis" authority), so every node is a **reviewable
assertion** (status: proposed/reviewed/accepted/disputed) — never mechanically-derived noise.

## Run
```bash
cd /root/patalacheckpoints
python3 pipeline/products/terminology/test.py          # 6/6 proof
python3 pipeline/products/terminology/engine.py kula trajectory
python3 pipeline/products/terminology/engine.py kula evidence
```

## Engine API
```python
from products.terminology.engine import lemma_history, sense_trajectory, evidence_for, lemmas
ls = lemmas()                         # ['kula','krama','khecarī','śakti','vimarśa','visarga']
tr = sense_trajectory("kula")         # chronological sense-shift
ev = evidence_for("kula", "kula.kubjika.mantra-body")  # passage + locator
```

## Real result (kula)
`lineage` (early Yoginī, secure) → `body/power` (developed Kaula, probable) → `body/power` (Kubjikā,
reviewed) → `body/power` (Abhinavagupta/Trika, secure). The clearest documented semantic shift in the
ecosystem.

## Honest limits
- 6 lemmas / 14 nodes (the current curated set) — more lemmas = more coverage.
- Data is curated, not corpus-derived; a corpus-occurrence cross-check is future work.

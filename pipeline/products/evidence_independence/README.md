# evidence_independence — the evidence-independence product (Claim/evidence upgrade)

A **standalone** engine that upgrades the corroboration model with REAL independence classification,
closing the "3 papers say X may be 1 origin" gap (SOURCE_ECHO). Built on the REAL corroboration
registry + the finished OpenCitations adapter (live Crossref SAME_AUTHOR).

## What it does
For each corroborated proposition, it:
1. Loads the real `data/corpus/registries/corroboration-registry.jsonl` + assertion registry.
2. **Deduplicates** — the registry records the SAME source multiple times (the real data has Sanderson
   5×). Counting them as 5 corroborations overstates independence.
3. Classifies each unique source's independence via OpenCitations + Crossref:
   `INDEPENDENT_AUTHOR / DERIVED_CITATION / SAME_AUTHOR` + detects `SOURCE_ECHO`.

## Real finding (anti-theatre)
The current registry has **6 recorded corroborations collapsing to 2 unique sources (1 duplicate)** —
the corroboration count was overstating evidence by ~3×. This is the honest signal the independence
model surfaces before any review gate.

## Run
```bash
cd /root/patalacheckpoints
python3 pipeline/products/evidence_independence/test.py          # 5/5 proof (offline, deterministic)
python3 pipeline/products/evidence_independence/engine.py live   # live OpenCitations+Crossref
python3 pipeline/products/evidence_independence/engine.py offline
```

## Engine API
```python
from products.evidence_independence.engine import independence_report, corroborated_propositions
r = independence_report(live=True)   # or live=False for deterministic offline
```

## Honest limits
- Live classification needs network (OpenCitations/Crossref). Unreachable -> `UNAVAILABLE`/`OPEN`, never
  fabricated.
- The output is MACHINE_PROPOSED evidence — it feeds the review gate, never claims truth itself.
- The dedup is by source_id; a semantic (same-work-different-EDITION) dedup is future work.

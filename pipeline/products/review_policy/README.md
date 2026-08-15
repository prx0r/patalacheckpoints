# review_policy — what each review decision grants (authority semantics)

The authority semantics behind peer review: what ACCEPT/REVISE/REJECT/ABSTAIN by each actor kind does to
an object's epistemic ceiling. Aligned to the canonical G3 6-decision vocabulary
(`source-evidence/schema/contracts_human_authority.py`).

## The invariant
`authority(projection) ≤ authority(parent)` — a review never raises an object above its evidence.
A machine may propose; only a human/adjudicator reaches the top rungs.

## Run
```bash
cd /root/patalacheckpoints
PYTHONPATH=pipeline python3 pipeline/products/review_policy/test.py   # 7/7 proof
PYTHONPATH=pipeline python3 pipeline/products/review_policy/engine.py summary
```

## Engine API
```python
from products.review_policy.engine import grants, g3_decision
grants("DISPUTE", "scholar")   # -> SUPERSEDED (maps G3 -> core REVISE)
g3_decision("ACCEPT_WITH_QUALIFICATION")  # -> maps to ACCEPT, canonical
```

## Decisions (G3 canonical)
ACCEPT · ACCEPT_WITH_QUALIFICATION · DISPUTE · PROPOSE_ALTERNATIVE · ABSTAIN · OUT_OF_SCOPE

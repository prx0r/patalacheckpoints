# passage_workbench — Passage Workbench (disagreement recording)

The vision's philology primitive (vision-15 / vision-14): a Sanskritist disagrees with a reading /
sandhi / translation and RECORDS it as a structured proposal that enters the durable review gate.
"AI proposes, scholar adjudicates" — but here the SCHOLAR proposes a correction to a passage, and it
must survive the same review gate.

## What it provides
- `disagree(passage_ref, claim, kind, rationale, evidence)` → a PROPOSED review
- `approve(proposal_id, drop_missing)` → durable APPROVED (dead-ref-checked)
- `reject(proposal_id)` → durable REJECTED
- `list_disagreements()` → open/approved/rejected

**Closed disagreement kinds:** sandhi_resolution, reading_variant, translation_fidelity, morphology,
scope, attribution, edition_choice.

## Run
```bash
cd /root/patalacheckpoints
python3 pipeline/products/passage_workbench/test.py    # 5/5 proof
python3 pipeline/products/passage_workbench/engine.py disagree chunkD "the sandhi should resolve to ātmā here" sandhi_resolution
```

## Engine API
```python
from products.passage_workbench.engine import PassageWorkbench
wb = PassageWorkbench()
prop = wb.disagree("chunkD", "sandhi → ātmā", kind="sandhi_resolution", rationale="preferred reading")
wb.approve(prop["proposal_id"])    # succeeds (the passage resolves, not a dead ref)
```

## Honest limits
- The gate resolves cited refs against REAL passages (a ghost citation blocks approval).
- Production signed-auth for the scholar's identity is the attestation product (next).

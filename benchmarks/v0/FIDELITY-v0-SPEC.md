# PATALA-FIDELITY v0 — SPEC (prepared, NOT yet built)

*2026-08-12. The PĀṬALA-FIDELITY benchmark family: **the verifier's sensitivity to known, deliberately
injected corruption** (Category A — construction-verifiable). This is the prepared spec only. It is
**NOT executed** until the P0 worktree reconciliation is complete (DEVPLAN.md §4 item 2; NEXT-STEPS.md P2).
No fixtures are generated from this spec yet.*

---

## 1. Why this family exists (and what it does NOT claim)

FIDELITY measures whether the verifier detects error types we deliberately inject into a **known-good,
structurally verified object**. It is falsifiable **by construction** — no semantic oracle is needed.

- **It establishes:** `Sensitivity(V, E) = P( V(x ⊕ e) = FAIL | e )` for a verifier `V` and injected
  error `e` on a known-good object `x`.
- **It does NOT establish:** that `V` detects all naturally occurring errors.

```
SYNTHETIC_SENSITIVITY  ≠  REAL_WORLD_RECALL
```

The latter requires human gold (P1). Keep them separate in every report.

---

## 2. The fixture envelope (one fixture = one injected corruption)

```json
{
  "fixture_id": "FID-SOURCE-001",
  "task_family": "PATALA-FIDELITY",
  "task": "verifier_sensitivity",
  "corruption_type": "DROP_SPAN",
  "injected_at": "benchmarks/v0/vertical/vertical-v2o-g-tc2.json",
  "expected_failure": true,
  "detector": "verify_l0 P0",
  "split_class": "EVALUATION_ONLY",
  "allowed_training_use": false,
  "input": { "known_good": "<hash or path of the pristine object>", "corruption": { ... } },
  "expected": { "verifier_must_fail": true }
}
```

---

## 3. The families + corruption taxonomy

### FID-SOURCE — source integrity (expected: P0 MUST FAIL)
```
DROP_SPAN · DUPLICATE_SPAN · SHIFT_SPAN_START · SHIFT_SPAN_END · REORDER_TOKEN · INSERT_UNKNOWN_REGION
```

### FID-L0 — L0 analysis (expected: the relevant proof dimension must disagree / flag)
```
FLIP_LEMMA · CHANGE_CASE · CHANGE_NUMBER · CHANGE_GENDER · REPLACE_SURFACE
```

### FID-ALIGNMENT — alignment (expected: the alignment verifier detects corruption)
```
SHIFT_ANCHOR · REMOVE_ANCHOR · LINK_WRONG_TOKEN · SWAP_TWO_ANCHORS
```

### FID-PROVENANCE — dependency / provenance (expected: vertical integrity fails)
```
DELETE_GROUNDING_EDGE · POINT_TO_NONEXISTENT_REF · USE_STALE_PROOF · CHANGE_SOURCE_HASH
```

### FID-DEPENDENCY — argument/inference integrity (prepared for later, needs reviewed gold)
```
DELETE_INFERENCE · SWAP_PREMISE_IDS · ORPHAN_CONCLUSION · BREAK_REFERENTIAL_GROUNDING
```

---

## 4. The run report (every run records)

```
corruption_type · injected_at · expected_failure · observed_failure · detector · pass/fail
```

Aggregated per family:

```
Sensitivity(V, FID-SOURCE) = detected / injected
```

And a per-detector table so a weak detector is surfaced, never hidden in an aggregate.

---

## 5. The falsification test (what would convince us this does NOT work)

> If the verifier **fails to flag** a corruption that a human can plainly see changed the object (e.g.
> a dropped span, a flipped lemma, a removed anchor), then the verifier is not doing its claimed job.
> Conversely, if the verifier flags a corruption that did **not** alter meaning (a false positive on an
> actually-identical object), that is also a failure — a fidelity fixture has no false positives by
> construction, so any is a verifier bug.

---

## 6. Guardrails

1. **Additive only:** FIDELITY adds fixtures; it never mutates existing gold (`PAT-STRUCT-*`, the
   vertical object, the theme map). Run against a **copy** of the known-good object.
2. Route through `benchmarks/v0/runs/` as an immutable `BenchmarkRun`.
3. Report `SYNTHETIC_SENSITIVITY` and `REAL_WORLD_RECALL` separately, always.
4. `FID-DEPENDENCY` requires independently reviewed argument gold before it can assert expected outcomes
   that are semantically meaningful — defer it to P1/P5.
5. No neural / ML machinery in v0 — this is deterministic mutation + deterministic verifier only.

---

## 7. Status

- **Prepared:** this spec + the corruption taxonomy.
- **Not built:** no `fid_*.py`, no fixtures, no runs.
- **Build gate:** P0 worktree reconciliation complete → then implement as `experiments/build_fidelity_suite.py`
  producing `FID-SOURCE/L0/ALIGNMENT/PROVENANCE` fixtures + a `FIDELITY-v0` run.

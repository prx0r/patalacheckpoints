# PATALA-FIDELITY v0 — SPEC (prepared, NOT yet built)

*2026-08-12. The PĀṬALA-FIDELITY benchmark family: **the verifier's sensitivity to known, deliberately
injected corruption** (Category A — construction-verifiable). This is the prepared spec only. It is
**NOT executed** until the STEP-0 worktree reconciliation is complete (DEVPLAN.md §4 item 0; NEXT-STEPS.md STEP 0).
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
  "fixture_id": "FID-ALIGNMENT-003",
  "family": "FID-ALIGNMENT",
  "task_family": "PATALA-FIDELITY",
  "task": "verifier_sensitivity",
  "corruption": "REMOVE_ANCHOR",
  "base_object": "benchmarks/v0/vertical/vertical-v2o-g-tc2.json",
  "mutation": { "...": "exactly the fields changed (one corruption at a time)" },
  "expected_detector": "alignment verifier",
  "expected_outcome": "FAIL",
  "split_class": "EVALUATION_ONLY",
  "allowed_training_use": false,
  "input": {
    "known_good": "<sha of the pristine object>",
    "clean_control_sha": "<sha of the object through the harness, unchanged>",
    "corrupted_sha": "<sha after mutation>"
  },
  "expected": { "verifier_must_fail": true }
}
```

### The acceptance contract (narrow, mandatory)

```text
INPUT        known-good frozen vertical object
MUTATIONS    deterministic, one corruption at a time
EXPECTED     a named verifier / invariant must fail
OUTPUT       an immutable BenchmarkRun
NO           semantic model judging · human-authored expected answers ·
             changes to the original gold object
```

---

## 3. The families + corruption taxonomy

v0 must ship at least these 15 classes:

### FID-SOURCE — source integrity (expected: P0 MUST FAIL)
```
DROP_SPAN · SHIFT_SPAN_START · CHANGE_SOURCE_HASH
```

### FID-L0 — L0 analysis (expected: the relevant proof dimension must disagree / flag)
```
FLIP_LEMMA · CHANGE_MORPH_FEATURE · REPLACE_SURFACE
```

### FID-ALIGNMENT — alignment (expected: the alignment verifier detects corruption)
```
REMOVE_ANCHOR · SHIFT_ANCHOR · LINK_WRONG_TOKEN
```

### FID-PROVENANCE — dependency / provenance (expected: vertical integrity fails)
```
BROKEN_REF · STALE_PROOF · MISSING_PROVENANCE
```

### FID-DEPENDENCY — argument/inference integrity (prepared for later, needs reviewed gold)
```
DELETE_GROUNDING_EDGE · RETARGET_GROUNDING_EDGE · DANGLING_DEPENDENCY
```

---

## 4. The run report (every run records)

Per fixture:
```
fixture · family · corruption · expected · observed · detector ·
detected (true/false) · false_positive (true/false) · git_sha · verifier_version
```

Every run also includes the **clean control** and **mutation isolation** checks:
```
clean_control_detected (must be false — unchanged object must PASS)
mutation_isolation_ok  (must be true  — exactly the intended fields changed)
```

Aggregates per family + per detector:
```
Sensitivity(V, FID-SOURCE) = detected injected errors / injected errors
FalsePositiveRate(V)        = clean objects flagged FAIL / clean objects  (must be 0)
```

A verifier that screams `FAIL` at everything will show high synthetic sensitivity but a non-zero
clean false-positive rate — the contract below kills it.

### The empirical contract (stronger than raw sensitivity)

```text
CORRUPTED object → expected FAILURE   (sensitivity)
CLEAN object     → expected PASS      (clean-control false-positive rate = 0)
```

### Mutation isolation (the "exactly one field" check)

Each fixture changes exactly one thing. Before/after hashes are recorded and the harness asserts no
unrelated canonical field changed:

```text
mutation_distance = exactly the intended fields
```

Otherwise a mutation meant to test alignment might also break source integrity, and you would not know
which detector actually fired.

---

## 5. The falsification test (what would convince us this does NOT work)

> If the verifier **fails to flag** a corruption that a human can plainly see changed the object (e.g.
> a dropped span, a flipped lemma, a removed anchor), then the verifier is not doing its claimed job.
> Conversely, if the verifier flags the **clean control** (an actually-identical object) as `FAIL`, that
> is a false positive — a verifier that cannot pass a clean object is not measuring corruption at all.
> And if a mutation changes more than its intended field (`mutation_isolation_ok = false`), the fixture
> is invalid because it cannot attribute the failure to a specific detector.

---

## 6. Guardrails

1. **Additive only:** FIDELITY adds fixtures; it never mutates existing gold (`PAT-STRUCT-*`, the
   vertical object, the theme map). Run against a **copy** of the known-good object.
2. Route through `benchmarks/v0/runs/` as an immutable `BenchmarkRun`.
3. Report `SYNTHETIC_SENSITIVITY` and `REAL_WORLD_RECALL` separately, always.
4. `FID-DEPENDENCY` requires independently reviewed argument gold before it can assert expected outcomes
   that are semantically meaningful — defer it to P1/P5.
5. No neural / ML machinery in v0 — this is deterministic mutation + deterministic verifier only.
6. **Clean control is mandatory:** every run passes the unchanged object through the harness and requires
   `clean_control_detected = false` (else false-positive rate non-zero and the verifier is not measuring
   corruption).
7. **Mutation isolation is mandatory:** before/after hashes per fixture; assert `mutation_isolation_ok`
   (exactly the intended fields changed) so failures are attributable to a single detector.

---

## 7. Status

- **Prepared:** this spec + the corruption taxonomy.
- **Not built:** no `fid_*.py`, no fixtures, no runs.
- **Build gate:** STEP-0 worktree reconciliation complete → then implement as `experiments/build_fidelity_suite.py`
  producing `FID-SOURCE/L0/ALIGNMENT/PROVENANCE` fixtures + a `FIDELITY-v0` run.

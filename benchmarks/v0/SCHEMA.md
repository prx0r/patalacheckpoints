# PATALA BENCHMARK v0 — SCHEMA

*2026-08-12. The fixture schema. Every fixture carries provenance and an explicit adjudication
boundary. A fixture is not "gold" just because it exists — it must pass the CANDIDATE → … →
BENCHMARK_ACCEPTED gate and carry an honest review_state.*

---

## 1. The common fixture envelope (every fixture)

```json
{
  "fixture_id": "PAT-STRUCT-001",
  "task_family": "PATALA-STRUCTURE",
  "task": "proposition_extraction",
  "source_ids": ["pt:passage:ipvv:chunkV2-O-saptamo-vimarsa.md", "C1:V2O-orderless-support"],
  "gold_version": "1",
  "authoring_method": "HAND_ADJUDICATED | MACHINE_PROPOSED | DERIVED_FROM_PRODUCT",
  "review_state": "CANDIDATE | SINGLE_EDITOR_GOLD | DOUBLE_REVIEWED_GOLD | ADJUDICATED_GOLD",
  "created_from": ["C1:V2O-orderless-support", "passage:pt:...:V2-O"],
  "allowed_training_use": false,
  "split_class": "EVALUATION_ONLY | S0 | S1 | S2 | S3 | S4",
  "input": { ... task-specific ... },
  "expected": { ... task-specific gold ... }
}
```

**Key field:** `allowed_training_use: false` → the fixture is EVALUATION_ONLY; no model may be
selected/optimized against it. ARG-GOLD-001 is EVALUATION_ONLY (one gold argument ≠ a train/test split).

---

## 2. Task-specific shapes

### PATALA-RETRIEVAL
```json
{
  "task": "passage_retrieval",
  "input": { "query": "why must manifestation be self-apprehending?" },
  "expected": { "relevant": ["pt:passage:ipvv:chunkV2-O-..."], "hard_negatives": [...] },
  "split_class": "S1"
}
```

### PATALA-EVIDENCE
```json
{
  "task": "claim_to_support",
  "input": { "claim": "the support of ordered presentation is itself orderless" },
  "expected": { "supporting": ["pt:passage:ipvv:chunkV2-O-..."], "counterevidence": [] }
}
```

### PATALA-STRUCTURE (the argument gold)
```json
{
  "task": "argument_extraction",
  "input": { "source": "the C1/L2 of V2-O" },
  "expected": {
    "nodes": [
      {"proposition": "...", "kind": "TEXTUAL_CLAIM", "explicitness": "EXPLICIT",
       "source_support": {"passage_ids": [...]}}
    ],
    "inferences": [{"premise_ids": [...], "conclusion_id": "...", "scheme": "TRANSCENDENTAL"}],
    "boundary": {"text": "...", "not_claiming": [...]}
  }
}
```

### PATALA-FIDELITY
```json
{
  "task": "l2_to_c1",
  "input": { "l2": "...", "c1_candidate": "..." },
  "expected": { "preserves": true, "corruption": null }
}
```

---

## 3. The acceptance gate (fixture → gold)

```
CANDIDATE
  → schema validation (conforms to this SCHEMA.md)
  → source resolution (all source_ids resolve)
  → leakage inspection (source not already used to generate it)
  → human check (a reviewer signs review_state)
  → BENCHMARK_ACCEPTED
```

**Anti-circularity rule:** if a fixture was produced by the clustering/argument system, it cannot be
presented as independent gold for evaluating that same system. Mark `authoring_method: DERIVED_FROM_PRODUCT`
and exclude from that method's evaluation.

---

## 4. The metric semantics contract (see METRICS.md)

Never collapse to one score. Report per-metric (proposition recovery F1, role macro-F1, explicitness
macro-F1, grounding exact-source precision, relation F1, inference-scheme macro-F1, scope-fidelity error
rate, boundary-preservation error rate). One dashboard OK; no `argument_quality = 0.83`.

# PATALA BENCHMARK v0 — METRICS

*2026-08-12. Freeze metric semantics. No magical aggregate score. The lesson from the fake B-STRUCT
result: metric design IS part of the scientific claim.*

---

## 1. Per-task metrics (report SEPARATELY, never one score)

### PATALA-RETRIEVAL
```
passage / term-sense / related / crux retrieval:
  Recall@k, MRR@k, nDCG@k   (with bootstrap CI + paired delta vs baseline)
```

### PATALA-EVIDENCE
```
claim → support:   support precision, Recall@k
claim → counterevidence:  counter-evidence Recall@k
quote verification:   AUTHENTIC precision (quote really occurs), RESOLVES precision
```

### PATALA-STRUCTURE (argument extraction — the key one)
```
PROPOSITION RECOVERY   precision / recall / F1      (did it recover the propositions?)
ROLE CLASSIFICATION    macro-F1                      (premise/conclusion/objection/qualification)
EXPLICITNESS           macro-F1                      (explicit/reconstructed/implicit)
GROUNDING              exact resolved-source precision (does the proposition resolve to the cited source?)
RELATION RECOVERY      support/attack/qualify F1
INFERENCE SCHEME       macro-F1                      (DEDUCTIVE/REDUCTIO/TRANSCENDENTAL/...)
SCOPE FIDELITY         error rate                    (did the proposition become stronger than the source?)
BOUNDARY PRESERVATION  error rate                    (was the honest limit erased?)
```

### PATALA-FIDELITY
```
l2→c1, c1→theme, theme→guide:
  semantic-preservation (polarity/scope/attribution/boundary) error rate
  corruption-detection: does the detector catch each injected corruption type?
```

---

## 2. The 4-layer epistemic declaration

Every test/run must declare WHICH layer it establishes:
```
SCHEMA TEST     object conforms
RESOLUTION TEST cited objects exist
GROUNDING TEST  source support present
DERIVATION TEST claim follows from lower layer
EDITORIAL       human judgment
FORMAL          formal consequence given encoding
```
**Never report these together as "N tests = scholarship verified."**

---

## 3. Baseline discipline

- Every INFER result must beat a baseline (BM25 for retrieval; majority-class for role; etc.) on the
  FROZEN suite, split S2 where possible.
- If an earlier result doesn't reproduce against the frozen suite, retire it. No sentimentality.

---

## 4. Run immutability

Every run is one directory:
```
runs/2026-08-12T.../
  benchmark_version.json
  split_manifest.json
  config.json
  predictions.jsonl
  metrics.json
  error_analysis.md
  git_commit.txt
```
Then "X beat Y" is answerable exactly (version, split, metrics, commit, config).

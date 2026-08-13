# MIGRATION PLAN — NO ID BREAKAGE

## Phase M0 — Freeze meanings before moving files

Deliver:
- glossary of existing state values by file/module;
- canonical `ObjectRef`;
- target authority axes;
- canonical ReviewEvent v2;
- adapter test harness.

No bulk data rewrite.

Exit:
- every existing object type has an owner or explicit “legacy/generic only” classification.

## Phase M1 — Canonical reference/version seam

Add shared:
- ObjectRef;
- ObjectVersionRef;
- content hash;
- resolver interface.

Adapters wrap old string IDs.

Exit:
- Agent1 review fixture can run against ObjectRef adapter with unchanged semantic outcome.

## Phase M2 — Authority envelope

Add `AuthorityEnvelopeV2`.
Read projection:
```text
legacy object → legacy adapter → V2 read model
```

New writes use V2.
Old objects remain byte-identical.

Exit:
- no product/API needs to infer authority from legacy enum directly.

## Phase M3 — Review engine hardening

Move schema ownership to shared kernel.
Keep reducer implementation in pipeline.

Lock down:
- append boundary;
- actor/scope;
- version binding;
- idempotency;
- concurrency;
- persistence;
- reducer lineage.

Exit:
- current review vertical passes plus production-hardening suite.

## Phase M4 — RAW-L0 hardening

- add nullable lemma;
- add AnalysisWitness;
- distinguish orthographic tokenization from segmentation;
- introduce passage completeness;
- stop `committed > 0` whole-work promotion;
- split structural validation from workflow state.

Migration:
- old records with `lemma_iast == surface_iast` are **not automatically declared wrong**;
- mark provenance/analysis certainty `LEGACY_AMBIGUOUS` unless analyzer lineage proves lemma;
- rerun analyzer only as needed.

## Phase M5 — Benchmark adapter

- keep existing `benchmarks/v0`;
- create canonical fixture schema adapter;
- add Inspect task/run adapter;
- preserve evaluation review ladder;
- one-way production→candidate exporter.

Exit:
- no benchmark run changes production DB.

## Phase M6 — Translation Audit v0

Implement deterministic findings only.
All findings exact-ref and lineage-bearing.

Exit:
- scholar can inspect source→finding→review→impact;
- reviewed finding can become benchmark candidate.

## Phase M7 — model-proposed Audit

Add interpretive detectors one-by-one.
Each has:
- abstention;
- evidence;
- failure taxonomy;
- explicit MODEL_PROPOSED class;
- benchmark task.

## Phase M8 — calibration

Only promote detector to CALIBRATED after independent reviewed fixture threshold and declared metrics.

## Phase M9 — Pāṭala Review

Start with native Pāṭala arguments.
Then Pāṭala-generated essays.
Then external source-resolvable thesis sections.
Arbitrary humanities PDF ingestion is a later problem.

## Phase M10 — Workbench

Build around repeated typed scholar actions observed in real Audit/Review use.

Do not start with:
- generic dashboard;
- social layer;
- gamification;
- rich text editor clone;
- journal CMS clone.

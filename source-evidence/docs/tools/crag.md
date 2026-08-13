# CRAG mock-API pattern — reproducible benchmark environment

**What Pāṭala borrows:** Meta's CRAG pattern of **mock APIs** so retrieval/knowledge access is evaluated in a
reproducible controlled environment rather than against a changing live web. Pāṭala's benchmarks use a frozen
corpus snapshot instead of unrestricted live access.

**License:** CRAG is open (mock-API pattern; the idea is what we borrow).

## Usage (no live API)
Provide each benchmark agent the **same frozen corpus snapshot** through mock endpoints:
```
TantraFact benchmark container
├── mock_source_api
├── mock_bibliography_api
├── resolve_span()
└── search_sources()
```
Each model gets exactly the same corpus; no retrieval drift, no contamination from current product state,
reproducible papers, and safe external release without exposing restricted PDFs.

## Etiquette
Freeze the snapshot + commit hash; record the corpus version in the Inspect task config / RO-Crate so a
benchmark's numbers are reproducible.

## How Pāṭala consumes it
Combine with **Inspect AI** + **RO-Crate**: `TantraFact data → frozen RO-Crate → mock Pāṭala Source API → Inspect
task → custom scorers + scanners → EvalLog`.

**Priority: when TantraFact v0 begins.**

# LAYER 01 — INGESTION

*Part of the `globalglobal.md` spine. Turns external sources into canonical objects.*

## 1. What it is
The intake engine: converts external sources (PANDiT, GRETIL, SARIT, Muktabodha, papers, Wikidata,
VIAF, C-SALT, NGMCP, IIIF) into canonical, provenance-carrying Pāṭala objects.

## 2. Purpose
Make ANY source flow into the same epistemic machine without changing the pipeline. A new source = a
new adapter subclass; nothing else changes. Enforces the license firewall and the "external IDs are
crosswalks, never canonical identity" rule.

## 3. External tools used
Borrowed adapters (see `docs/process/external-tools.md`):
`PanditBulkAdapter` · `GretilAdapter` · `SaritAdapter` · `WikidataAdapter` · `ViafAdapter` ·
`CSaltAdapter` · `NgmcpAdapter` · `IiifAdapter`. Underlying substrate: R2 (immutable bytes),
entity reconciliation, text fingerprints.

**Manuscript/OCR substrate (from the `patalagithubs` review — §J):** for manuscript → machine-readable
ingest, **don't build OCR**: use **Kraken** (historical/non-Latin OCR → ALTO/PageXML/hOCR) + **eScriptorium**
(the research UI around Kraken; Pāṭala is the importer/exporter) + the **pe-ocr-sanskrit** post-OCR
correction benchmark (`OCRProofBenchmark`). Every OCR model tests before entering the factory.

## 4. Data
- **Bronze:** R2 snapshots (`source/ingestion/<SOURCE>/snapshots/<id>/` + manifest) — immutable raw bytes.
- **Silver:** `ExternalRecord[]` (raw, source-bound).
- **Gold:** canonical objects → Postgres + `atlas-bibliography.json`.
- **Scholar queue:** POSSIBLE/CONFLICT/UNRESOLVED records awaiting human adjudication.

## 5. Processes
```
source → Connector(discover/fetch/parse/normalize) → ExternalRecord[] → reconcile()
  → EXACT/PROBABLE (gold) vs POSSIBLE/CONFLICT/UNRESOLVED (scholar queue)
  → persist → Postgres + bibliography + registry
```
The **license firewall**: PANDiT is CC BY-NC-SA → discovery/index/provenance, not unrestricted commercial.

## 6. Implementations
- `ingestion/asserter.py` — `SourceAsserter` (the intake engine).
- `ingestion/persistence.py` — `AtlasWriter` (idempotent Postgres writes).
- `ingestion/r2.py` — `SnapshotStore` (immutable Bronze snapshots).
- `ingestion/adapters/*.py` — the 8 source connectors.
- `source-evidence/schema/external_record.py` — the contract (`ExternalRecord`, `ReconciliationAdapter`).
- `source-evidence/evals/patala/tasks/entity_reconciliation.py` — `reconcile()`.
- Tests: `ingestion/test_asserter.py`, `ingestion/test_smoke.py`.

## 7. Docs
- `docs/process/01-ingestion.md` — the detailed layer guide.
- `docs/global/ingestion-refinery.md` — the ingestion/refinery architecture.
- `docs/global/globalpartnerships.md` — the integration/identity strategy.
- `docs/process/external-tools.md` — the adapter/tool status.

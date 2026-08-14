# 01 — INGESTION (intake → reconcile → persist)

*Part of `docs/process/README.md`. This is the permanent intake layer. **Goal:** turn any external
source (PANDiT, GRETIL, SARIT, Gyan Bharatam, ...) into canonical Pāṭala objects without changing the
pipeline — by composing the existing primitives, not redefining them.*

## 1. What this layer IS

The single reusable intake engine. A new source = a new `ReconciliationAdapter` subclass fed into the
`SourceAsserter`. Nothing else changes.

```
SourceSnapshot (R2 Bronze)  →  ExternalRecord[] (Silver)  →  reconcile()
   →  EXACT/PROBABLE (gold)          vs   POSSIBLE/CONFLICT/UNRESOLVED (scholar queue)
   →  persist gold → Postgres + bibliography + registry
```

## 2. The files (reusable, tested)

| File | What it is | Key entry points |
|---|---|---|
| `ingestion/asserter.py` | the intake engine | `SourceAsserter(adapter, dry_run=True).run()` → `AsserterResult` |
| `ingestion/persistence.py` | Postgres writer | `AtlasWriter` — `ensure_work`, `ensure_external_identifier`, `add_authority_evidence` |
| `ingestion/r2.py` | R2 snapshot store | `SnapshotStore` — `put_snapshot`, `manifest`, `list_snapshots` |
| `ingestion/bibliography.py` | thin-bib reads | `existing_works()`, `canonical_entities()` |
| `ingestion/adapters/pandit.py` | PANDiT connector | `PanditAdapter` (CSV-based, CC BY-NC-SA firewall) |
| `ingestion/adapters/gretil.py` | GRETIL connector | `GretilAdapter` (IAST HTML + TEI) |
| `ingestion/connector.py` | thin runner | `run_ingestion(adapter, against=...)` |

## 3. The reusable contract it builds on (do NOT redefine)

- `source-evidence/schema/external_record.py` — `ExternalRecord` + `ReconciliationAdapter` + maturity ladder (`DISCOVERED→…→ADJUDICATED`).
- `source-evidence/evals/patala/tasks/entity_reconciliation.py` — `reconcile()` returns `EXACT/PROBABLE/POSSIBLE/CONFLICT/UNRESOLVED`.
- `python/patala_core/atlas/adapter.py` — the canonical crosswalk + compiled read-model.

## 4. How to use it (process)

### Bronze snapshot → R2 (the FIRST step of any ingestion)
```bash
# stage a source on disk, then put it on R2 as an immutable snapshot
python3 -m ingestion.r2 --source GRETIL --snapshot-id gretil-tei-2026-08-14 \
    --file /path/to/gretil-tei.tar.gz --license per-file
```
From code:
```python
from ingestion.r2 import SnapshotStore
store = SnapshotStore(r2_bucket="patala")
m = store.put_snapshot("GRETIL", "gretil-tei-2026-08-14",
                       {"gretil-tei.tar.gz": data}, license="per-file")
```
Layout: `source/ingestion/<SOURCE>/snapshots/<id>/` + `manifest.json`. **Never mutate a snapshot** — a new upstream state is a NEW snapshot_id; both survive.

### Run the asserter (reconcile against the bibliography)
```python
from ingestion.asserter import SourceAsserter
from ingestion.adapters.pandit import PanditAdapter

adapter = PanditAdapter(csv_path="/mnt/HC_Volume_106427611/patala-ingest/staging/pandit-export.csv")
result = SourceAsserter(adapter, dry_run=True).run()   # compute only, no writes

result.gold          # EXACT/PROBABLE → these become canonical
result.scholar_queue # POSSIBLE/CONFLICT/UNRESOLVED → human adjudication (data capital)
result.matches       # every CandidateMatch with per-axis evidence
```
Set `dry_run=False` to persist gold to Postgres + bibliography (+ `commit_registry=True` to write SOURCE objects).

## 5. The non-negotiable rules

1. **External IDs → `external_identifier` rows, NEVER canonical identity.** PANDiT `:91821` stays a crosswalk; your identity is `PATA-W-…`.
2. **Imported relationships → `authority_evidence` (per-dimension), NEVER canonical fields.** A later dispute adds an assertion, never corrupts the graph.
3. **Raw is preserved forever.** `ExternalRecord` is immutable; reconciliation produces NEW objects.
4. **POSSIBLE/CONFLICT/UNRESOLVED → human queue, NEVER auto-merged.** FALSE_MERGE_RATE = 0 is the goal (confirmed by the existing eval).
5. **Rights firewall** (e.g. PANDiT CC BY-NC-SA): partner / respect license, never relicense.

## 6. Honest caveat about reconciliation

The thin bibliography (`atlas-bibliography.json`) carries only `id/title/translation_status/verified` —
**no author or date**. So reconciliation against it is deliberately conservative (mostly POSSIBLE). To
get EXACT/PROBABLE at scale, feed the asserter a canonical set enriched from the rich bibliography
(`data/evaluation/atlas-backfill-candidates.json` / `audited.ts`) which has `author` + `date`/`tradition`.

## 7. Tests

```bash
python3 ingestion/test_smoke.py    # adapter contract + run_ingestion
python3 ingestion/test_asserter.py # SourceAsserter end-to-end (dry-run, no writes)
```
Both PASS. Existing reconciliation eval (FALSE_MERGE_RATE = 0) still passes — no regression.

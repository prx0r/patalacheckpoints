# ingestion/ — the Pāṭala ingestion/refinery layer

The reusable intake engine. Turns any external source (PANDiT, GRETIL, SARIT, Gyan Bharatam, ...)
into canonical Pāṭala objects. **A new source = a new `ReconciliationAdapter` subclass fed into the
`SourceAsserter`; nothing else changes.**

Full guide: `docs/process/01-ingestion.md`.

## Files

| File | Purpose |
|---|---|
| `asserter.py` | the intake engine — `SourceAsserter(adapter, dry_run=True).run()` → `AsserterResult` |
| `persistence.py` | Postgres writer — `AtlasWriter` (idempotent, reuses crosswalk + deterministic UUID) |
| `r2.py` | R2 snapshot store — `SnapshotStore` (immutable Bronze snapshots + manifests) |
| `bibliography.py` | thin-bibliography reads/merge |
| `connector.py` | thin runner over the existing `ReconciliationAdapter` contract |
| `adapters/pandit.py` | PANDiT connector (CSV-based, CC BY-NC-SA firewall) |
| `adapters/gretil.py` | GRETIL connector (IAST HTML + TEI) |
| `test_smoke.py`, `test_asserter.py` | tests (both PASS) |

## Quickstart

```python
from ingestion.asserter import SourceAsserter
from ingestion.adapters.pandit import PanditAdapter

adapter = PanditAdapter(csv_path="/path/to/pandit-export.csv")
result = SourceAsserter(adapter, dry_run=True).run()   # compute only, no writes

result.gold          # EXACT/PROBABLE → canonical
result.scholar_queue # POSSIBLE/CONFLICT/UNRESOLVED → human adjudication
```

## Bronze snapshot → R2

```bash
python3 -m ingestion.r2 --source GRETIL --snapshot-id gretil-tei-2026-08-14 \
    --file /path/to/gretil-tei.tar.gz --license per-file
```

## Non-negotiable rules

1. External IDs → `external_identifier` rows, never canonical identity.
2. Imported relationships → `authority_evidence` (per-dimension), never canonical fields.
3. Raw preserved forever; reconciliation produces NEW objects.
4. POSSIBLE/CONFLICT/UNRESOLVED → human queue, never auto-merged (FALSE_MERGE_RATE = 0).
5. Rights firewall (e.g. PANDiT CC BY-NC-SA).

## Builds on (do NOT redefine)

- `source-evidence/schema/external_record.py` — `ExternalRecord`, `ReconciliationAdapter`
- `source-evidence/evals/patala/tasks/entity_reconciliation.py` — `reconcile()`
- `python/patala_core/atlas/adapter.py` — crosswalk + read-model

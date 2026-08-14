"""ingestion/ — the Pāṭala ingestion/refinery system (docs/global/ingestion-refinery.md).

ALIGNED WITH EXISTING INFRA (do not duplicate): this layer is a thin adapter/orchestration layer on
top of the already-built P2 reconciliation framework, NOT a parallel contract.

  Reconciliation contract   -> source-evidence/schema/external_record.py
                               (ExternalRecord, ReconciliationAdapter, MATURITY ladder)
  Entity resolver           -> source-evidence/evals/patala/tasks/entity_reconciliation.py
                               (EXACT/PROBABLE/POSSIBLE/CONFLICT/UNRESOLVED)
  Text fingerprints         -> source-evidence/schema/text_fingerprint.py
  Production adapters       -> source-evidence/production/adapters/
                               (Crossref/OpenAlex, OpenCitations, identity crosswalks, GROBID)
  Bibliography (thin)       -> data/corpus/atlas-bibliography.json
  Bibliography (rich)       -> data/atlas/bibliographySeed.ts + data/evaluation/atlas-backfill-candidates.json
  Canonical Postgres        -> python/patala_core/atlas/ (work/edition/witness/... schema, migration 0001)

THE ACTUAL GAP this fills: no concrete PANDiT or GRETIL ReconciliationAdapter exists (only the
abstract contract + one-off acquire scripts). This package implements them and wires intake into the
existing bibliography / Atlas, so external records become versioned Assertions — never canonical ids.

Pipeline (Bronze -> Silver -> Gold -> Reviewed):
  SOURCE -> Connector(discover/fetch/parse/normalize) -> ExternalRecord[] -> resolver
  -> EXACT/PROBABLE/POSSIBLE/CONFLICT/UNRESOLVED -> scholar queue -> Atlas Gold graph.
"""
from .asserter import AsserterResult, SourceAsserter  # noqa: F401
from .connector import IngestionResult, run_ingestion  # noqa: F401
from .persistence import AtlasWriter, deterministic_uuid  # noqa: F401
from . import bibliography  # noqa: F401

__all__ = [
    "AsserterResult", "AtlasWriter", "IngestionResult", "SourceAsserter",
    "bibliography", "deterministic_uuid", "run_ingestion",
]

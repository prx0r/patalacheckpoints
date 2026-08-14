"""ingestion/connector.py — a thin runner over the existing P2 ReconciliationAdapter contract.

ALIGNED, NOT DUPLICATED: the adapter contract already exists at
`source-evidence/schema/external_record.py` (ReconciliationAdapter). This module only provides an
orchestration convenience (Bronze->Silver->Gold run + resolver + scholar queue) that drives any
ReconciliationAdapter subclass — it does NOT redefine the contract.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_ROOT / "source-evidence"))
sys.path.insert(0, str(_ROOT / "source-evidence" / "schema"))
sys.path.insert(0, str(_ROOT / "source-evidence" / "evals" / "patala" / "tasks"))

from external_record import ExternalRecord, ReconciliationAdapter  # noqa: E402
from entity_reconciliation import reconcile, STATUS  # noqa: E402


@dataclass
class IngestionResult:
    """The complete output of one connector run."""

    source: str
    snapshots: List[dict] = field(default_factory=list)
    records: List[ExternalRecord] = field(default_factory=list)
    matches: List[dict] = field(default_factory=list)   # CandidateMatch results
    gold_candidates: List[dict] = field(default_factory=list)  # records that reached EXACT/PROBABLE
    scholar_queue: List[dict] = field(default_factory=list)    # POSSIBLE/CONFLICT/UNRESOLVED -> human
    errors: List[str] = field(default_factory=list)


def run_ingestion(adapter: ReconciliationAdapter,
                  params: dict | None = None,
                  against: list[dict] | None = None,
                  dry_run: bool = False) -> IngestionResult:
    """Drive one adapter through the full Bronze->Silver->Gold->Reviewed flow.

    against: optional list of canonical entities {rid,title,author,shelfmark,incipit} to reconcile
             the incoming records against. If None, reconciliation is skipped (raw import only).
    """
    out = IngestionResult(source=adapter.source)

    try:
        snap = adapter.snapshot()
        out.snapshots.append(snap)
    except Exception as e:  # noqa: BLE001
        out.errors.append(f"snapshot: {e}")
        snap = {}

    # Silver: fetch + normalize the raw records into ExternalRecords
    try:
        raws = adapter.fetch(params or {})
        records = adapter.emit_external_records(raws)
        out.records = records
    except Exception as e:  # noqa: BLE001
        out.errors.append(f"fetch/emit: {e}")
        return out

    # Gold: reconcile against canonical entities (if provided)
    if against:
        for rec in out.records:
            incoming = {"rid": rec.external_id, "title": rec.title_raw,
                        "author": rec.author_raw, "shelfmark": rec.shelfmark_raw}
            for cand in against:
                match = reconcile(incoming, cand)
                out.matches.append(match)
                if match["status"] in ("EXACT", "PROBABLE"):
                    out.gold_candidates.append({**match, "record": rec.emit()})
                else:
                    out.scholar_queue.append({**match, "record": rec.emit()})
    else:
        # no canonical set yet -> everything is a POSSIBLE new entity for the scholar queue
        for rec in out.records:
            out.scholar_queue.append({
                "subject": rec.external_id, "candidate": None, "type": "NEW_ENTITY",
                "status": "POSSIBLE", "reasons": ["no canonical set — needs scholar classification"],
                "record": rec.emit(),
            })

    return out

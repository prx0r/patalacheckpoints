"""ingestion/asserter.py — the reusable SourceAsserter (the permanent intake engine).

The single reusable entry point for turning ANY external source (PANDiT, GRETIL, SARIT, Gyan Bharatam,
...) into canonical Pāṭala objects. It composes the EXISTING primitives rather than redefining them:

    ReconciliationAdapter  (source-evidence/schema/external_record.py)   — the per-source connector
    reconcile()            (source-evidence/evals/.../entity_reconciliation.py) — identity resolution
    AtlasWriter            (ingestion/persistence.py)                    — Postgres writes
    object_registry        (pipeline/object_registry.py)                 — SOURCE registry + event ledger
    bibliography           (ingestion/bibliography.py)                   — thin bibliography merge

A new source = a new ReconciliationAdapter subclass fed into SourceAsserter. Nothing else changes.
This is the "one connector interface" abstraction realized on top of the permanent infra.

Pipeline (Bronze -> Silver -> Gold -> Reviewed):
    SourceSnapshot (R2 Bronze) -> ExternalRecord[] (Silver)
    -> reconcile against bibliography -> EXACT/PROBABLE (gold) vs POSSIBLE/CONFLICT/UNRESOLVED (queue)
    -> persist gold to Postgres (work/external_identifier/authority_evidence) + registry + bibliography
    -> scholar queue (human adjudication -> data capital)

Design laws (from ingestion-refinery.md):
    external IDs -> external_identifier rows, NEVER canonical identity
    relationships -> authority_evidence (per-dimension), NEVER canonical fields
    raw preserved forever; reconciliation produces new objects
    POSSIBLE/CONFLICT/UNRESOLVED -> human queue, NEVER auto-merged
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

_ROOT = Path(__file__).resolve().parent.parent
for _p in (_ROOT, _ROOT / "source-evidence" / "schema",
           _ROOT / "source-evidence" / "evals" / "patala" / "tasks",
           _ROOT / "pipeline"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from external_record import ExternalRecord, ReconciliationAdapter  # noqa: E402
from entity_reconciliation import reconcile, STATUS  # noqa: E402

from .persistence import AtlasWriter  # noqa: E402
from . import bibliography as B  # noqa: E402


@dataclass
class AsserterResult:
    """The full outcome of one SourceAsserter.run() pass."""

    source: str
    records: List[ExternalRecord] = field(default_factory=list)
    matches: List[dict] = field(default_factory=list)
    gold: List[dict] = field(default_factory=list)          # EXACT/PROBABLE -> persisted
    scholar_queue: List[dict] = field(default_factory=list)  # POSSIBLE/CONFLICT/UNRESOLVED -> human
    persisted: dict = field(default_factory=dict)            # counts from the writers
    errors: List[str] = field(default_factory=list)


class SourceAsserter:
    """Reusable intake engine. Construct once per source; call run() repeatedly (idempotent)."""

    def __init__(self, adapter: ReconciliationAdapter,
                 canonical: Optional[list[dict]] = None,
                 dry_run: bool = True,
                 commit_registry: bool = False,
                 registry_created_by: str = "ingestion"):
        """adapter: the per-source ReconciliationAdapter.
        canonical: optional canonical entity set (else bibliography.existing_works() is used).
        dry_run:   if True, compute only — no writes to Postgres/registry/bibliography.
        commit_registry: also commit SOURCE objects to object_registry (default off).
        """
        self.adapter = adapter
        self.canonical = canonical
        self.dry_run = dry_run
        self.commit_registry = commit_registry
        self.registry_created_by = registry_created_by

    def _canonical(self) -> list[dict]:
        if self.canonical is not None:
            return self.canonical
        return B.canonical_entities()

    def run(self) -> AsserterResult:
        out = AsserterResult(source=self.adapter.source)
        try:
            snap = self.adapter.snapshot()
        except Exception as e:  # noqa: BLE001
            out.errors.append(f"snapshot: {e}")
            snap = {}

        # Silver: fetch -> ExternalRecords
        try:
            raws = self.adapter.fetch({})
            out.records = self.adapter.emit_external_records(raws)
        except Exception as e:  # noqa: BLE001
            out.errors.append(f"fetch/emit: {e}")
            return out

        # Gold: reconcile against canonical entities
        canonical = self._canonical()
        for rec in out.records:
            incoming = {"rid": rec.external_id, "title": rec.title_raw,
                        "author": rec.author_raw, "shelfmark": rec.shelfmark_raw}
            if not incoming["title"]:
                out.scholar_queue.append({"subject": rec.external_id, "status": "UNRESOLVED",
                                          "reasons": ["no title to reconcile"], "record": rec.emit()})
                continue
            for cand in canonical:
                m = reconcile(incoming, cand)
                out.matches.append(m)
                if m["status"] in ("EXACT", "PROBABLE"):
                    out.gold.append({**m, "record": rec.emit()})
                else:
                    out.scholar_queue.append({**m, "record": rec.emit()})

        # Persist gold + bibliography + registry (skipped when dry_run or no gold)
        if not self.dry_run:
            self._persist(out)
        return out

    def _persist(self, out: AsserterResult) -> dict:
        # 1. Postgres (work/external_identifier/authority_evidence) for gold candidates
        with AtlasWriter(dry_run=False) as w:
            for g in out.gold:
                rec = g["record"]
                wid = w.ensure_work(rec.external_id, rec.title_raw, source=self.adapter.source)
                # external id -> external_identifier row (NEVER canonical identity)
                w.ensure_external_identifier("work", wid, "PANDIT" if self.adapter.source == "PANDIT"
                                             else self.adapter.source, rec.external_id)
                # per-dimension authority evidence
                w.add_authority_evidence(wid, "WORK_IDENTITY", self.adapter.source,
                                         g.get("type", "WORK_IDENTITY"),
                                         {"status": g["status"], "evidence": g.get("evidence", {}),
                                          "reasons": g.get("reasons", []),
                                          "resolution_status": g.get("resolution_status",
                                                                     "MACHINE_PROPOSED")})
            # record the intake snapshot as an assertion too
            w.add_authority_evidence(str(uuid_of(self.adapter.source)), "RIGHTS", self.adapter.source,
                                     "SOURCE_INTRODUCED",
                                     {"license": self.adapter.license,
                                      "snapshot_id": self.adapter.snapshot()})
            out.persisted["postgres"] = {"gold": len(out.gold)}

        # 2. Bibliography merge (new works -> thin json) — reuse the thin-merge logic
        data = B.load_thin()
        records = data.setdefault("records", {})
        added = updated = 0
        for g in out.gold:
            rec = g["record"]
            title = (rec.title_raw or "").strip()
            if not title:
                continue
            key = rec.external_id or title.lower().replace(" ", "_")
            if key in records:
                updated += 1
                records[key].setdefault("title", title)
                records[key].setdefault("translation_status", "pending")
                records[key].setdefault("verified", "false")
            else:
                records[key] = {"id": key, "title": title,
                                "translation_status": "pending", "verified": "false"}
                added += 1
        from .bibliography import THIN
        THIN.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        out.persisted["bibliography"] = {"added": added, "updated": updated}

        # 3. Registry (SOURCE objects -> object_registry + event ledger) — optional
        if self.commit_registry:
            import object_registry as R
            import hashlib as _hl
            entries = []
            for g in out.gold:
                rec = g["record"]
                entries.append({
                    "object_id": rec.external_id,
                    "input_hash": _hl.sha256(rec.emit().encode() if isinstance(rec.emit(), str)
                                             else json.dumps(rec.emit(), sort_keys=True).encode()).hexdigest(),
                    "payload": {"title": rec.title_raw, "source": self.adapter.source,
                                "status": g["status"], "provenance": rec.emit()},
                })
            committed = R.commit_batch("SOURCE", entries, self.registry_created_by, status="GENERATED")
            out.persisted["registry"] = {"committed": len(committed)}
        return out.persisted


def uuid_of(s: str) -> str:
    """Small helper to derive a stable uuid for snapshot-level assertion subject."""
    from .persistence import deterministic_uuid
    return deterministic_uuid(f"snapshot:{s}")

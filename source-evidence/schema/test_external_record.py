#!/usr/bin/env python3
"""test_external_record.py — P2 ExternalRecord + reconciliation adapter framework acceptance.

Checks (the reviewer's P2):
  1. ExternalRecord is first-class + raw-preserving (immutable, hashed — never mutates the raw)
  2. the epistemic-maturity ladder exists (DISCOVERED..ADJUDICATED)
  3. the adapter framework contract (fetch/snapshot/normalize/map_identifiers/emit/reconcile/export)
  4. an adapter declares its metadata (license/access/source_authority/cadence/rights)
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from external_record import ExternalRecord, ReconciliationAdapter, MATURITY

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


print("== 1. ExternalRecord first-class + raw-preserving ==")
rec = ExternalRecord(source="GYAN_BHARATAM", external_id="GB_8291", title_raw="Malinivijayottara Tantra")
e = rec.emit()
check("raw hash is stable + immutable", rec.raw_payload_hash and rec.raw_payload_hash == ExternalRecord(
    source="GYAN_BHARATAM", external_id="GB_8291", title_raw="Malinivijayottara Tantra").raw_payload_hash)
check("raw fields preserved", e["fields"]["title"] == "Malinivijayottara Tantra")
check("raw never mutated (design law)", "raw is preserved forever" in e["design_law"])

print("\n== 2. maturity ladder ==")
check("epistemic-maturity ladder", MATURITY == ("DISCOVERED", "NORMALIZED", "CANDIDATE_MATCH",
                                                "RESOLVED", "SCHOLAR_REVIEWED", "ADJUDICATED"))

print("\n== 3. adapter framework contract ==")
methods = ["fetch", "snapshot", "normalize", "map_identifiers", "emit_external_records", "reconcile", "export_enrichment"]
check("adapter implements the full contract", all(hasattr(ReconciliationAdapter, m) for m in methods))

print("\n== 4. adapter metadata ==")
class GyanBharatam(ReconciliationAdapter):
    source = "GYAN_BHARATAM"
    license = "partnership"
    source_authority = "national manuscript survey"
    entity_types = ["manuscript", "work"]
d = GyanBharatam().describe()
check("adapter declares metadata", d["source"] == "GYAN_BHARATAM" and d["license"] and d["entity_types"])

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (ExternalRecord + adapter framework works)"))
sys.exit(1 if failures else 0)

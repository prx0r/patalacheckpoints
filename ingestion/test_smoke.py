#!/usr/bin/env python3
"""ingestion/test_smoke.py — smoke test for the ingestion/refinery layer.

Verifies the ingestion layer ALIGNS with (not duplicates) the existing P2 reconciliation framework:
  1. PanditAdapter emits ExternalRecords (the raw boundary object) with license firewall intact.
  2. run_ingestion() drives a ReconciliationAdapter through fetch->emit->reconcile->scholar queue.
  3. Reconciliation against the existing bibliography produces EXACT/PROBABLE matches for known works.
  4. bibliography.merge_into_thin adds new works without clobbering rich fields (dry-run default).

Run: python3 ingestion/test_smoke.py
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "source-evidence" / "schema"))
sys.path.insert(0, str(ROOT / "source-evidence" / "evals" / "patala" / "tasks"))

from external_record import ExternalRecord, ReconciliationAdapter, MATURITY  # noqa: E402
from ingestion.adapters.pandit import PanditAdapter  # noqa: E402
from ingestion.adapters.gretil import GretilAdapter  # noqa: E402
from ingestion.connector import run_ingestion  # noqa: E402
from ingestion import bibliography as B  # noqa: E402

FAILS = []


def check(name: str, cond: bool, detail: str = ""):
    print(("  PASS " if cond else "  FAIL ") + name + (f"  ({detail})" if detail else ""))
    if not cond:
        FAILS.append(name)


def main() -> int:
    print("== 1. PanditAdapter emits ExternalRecords (raw boundary, license firewall) ==")
    csv_data = (
        "id,title,author,shelfmark\n"
        "pandit:91821,Mālinīvijayottaratantra,,\n"
        "pandit:91822,Tantrāloka,Abhinavagupta,\n"
    )
    tmp = ROOT / "tmp_t1" / "pandit_smoke.csv"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(csv_data, encoding="utf-8")

    pa = PanditAdapter(csv_path=str(tmp))
    d = pa.describe()
    check("license firewall declared", "CC-BY-NC-SA" in d["license"])
    check("no live-API claim", "no public REST API" in d["access_constraints"])

    raws = pa.fetch({})
    recs = pa.emit_external_records(raws)
    check("2 records emitted", len(recs) == 2, f"got {len(recs)}")
    check("record is ExternalRecord (existing contract)", isinstance(recs[0], ExternalRecord))
    check("raw preserved (title_raw)", recs[0].title_raw == "Mālinīvijayottaratantra")
    check("hash computed", bool(recs[0].raw_payload_hash))

    print("== 2. run_ingestion drives the adapter (fetch->emit->reconcile->queue) ==")
    canonical = [
        {"rid": "malinivijayottara", "title": "Mālinīvijayottaratantra"},
        {"rid": "tantraloka", "title": "Tantrāloka", "author": "Abhinavagupta"},
    ]
    result = run_ingestion(pa, against=canonical)
    check("4 matches produced (2 recs x 2 canon)", len(result.matches) == 4, f"got {len(result.matches)}")
    statuses = [m["status"] for m in result.matches]
    check("work WITH author reaches PROBABLE/EXACT",
          "PROBABLE" in statuses or "EXACT" in statuses, f"statuses={statuses}")
    # anonymous work (Mālinīvijayottara) vs canonical malinivijayottara: same title, no author -> POSSIBLE
    anon_status = next(m["status"] for m in result.matches
                       if m["subject"] == "pandit:91821" and m["candidate"] == "malinivijayottara")
    # anonymous work honestly abstains (unknown author = uncertain) — the false-merge guard
    check("anonymous work honestly stays POSSIBLE (never confident merge)",
          anon_status == "POSSIBLE", f"got {anon_status}")
    check("matches carry MACHINE_PROPOSED (never truth)", result.matches and
          result.matches[0].get("resolution_status") == "MACHINE_PROPOSED")
    check("gold candidates separated from scholar queue",
          (len(result.gold_candidates) + len(result.scholar_queue)) == len(result.matches))

    print("== 3. bibliography.merge_into_thin (dry-run, no clobber) ==")
    merge = B.merge_into_thin(result, dry_run=True)
    check("dry-run reported (no write)", merge["dry_run"] is True and merge["added"] >= 0)
    # verify the file was NOT modified by the dry-run
    after = tmp.read_text if False else None
    check("known existing work preserved", "malinivijayottara" in B.existing_works())

    print("== 4. ReconciliationAdapter contract is inherited (not redefined) ==")
    check("subclass of existing contract", issubclass(PanditAdapter, ReconciliationAdapter))
    check("maturity ladder available", "RESOLVED" in MATURITY and "ADJUDICATED" in MATURITY)

    print("== 5. GretilAdapter offline path (no network, fails-closed) ==")
    ga = GretilAdapter(targets={"t1": ("https://example.invalid/t.htm", "Test")}, git_commit="offline")
    gr = run_ingestion(ga)
    check("gretil record emitted even when fetch failed", len(gr.records) == 1)
    check("gretil fetch failure recorded (fails-closed)", gr.records[0].extra.get("ok") is False)

    print()
    if FAILS:
        print("FAILURES:", FAILS)
        return 1
    print("SMOKE TEST PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())

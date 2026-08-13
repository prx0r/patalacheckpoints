#!/usr/bin/env python3
"""test_entity_reconciliation.py — P3 entity reconciliation engine acceptance.

Checks (the reviewer's P3):
  1. typed CandidateMatch statuses (EXACT/PROBABLE/POSSIBLE/CONFLICT/UNRESOLVED)
  2. same-title-different-author = CONFLICT (the false-merge trap, never silently merged)
  3. duplicate record (title+shelfmark) = EXACT
  4. compatible author + title = PROBABLE
  5. per-axis evidence is reported (title/author/shelfmark)
  6. resolution_status = MACHINE_PROPOSED (never scholarly truth)
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from entity_reconciliation import reconcile, STATUS

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


print("== 1. typed statuses ==")
r = reconcile({"rid": "A", "title": "X"}, {"rid": "B", "title": "Y"})
check("returns a status from the ladder", r["status"] in STATUS, r["status"])

print("\n== 2. same-title-different-author = CONFLICT ==")
rc = reconcile({"rid": "GB_010", "title": "Tantrāloka", "author": "Abhinavagupta"},
               {"rid": "GB_011", "title": "Tantrāloka", "author": "an anonymous different text"})
check("CONFLICT on same-title-diff-author", rc["status"] == "CONFLICT", rc["status"])

print("\n== 3. duplicate record = EXACT ==")
rd = reconcile({"rid": "GB_020", "title": "Svacchandatantra", "shelfmark": "NMS 45/86"},
               {"rid": "GB_021", "title": "Svacchanda Tantra", "shelfmark": "NMS 45/86"})
check("EXACT on duplicate title+shelfmark", rd["status"] == "EXACT", rd["status"])

print("\n== 4. compatible author + title = PROBABLE ==")
rp = reconcile({"rid": "A", "title": "Tantrasāra", "author": "Abhinavagupta"},
               {"rid": "B", "title": "Tantrasara", "author": "Abhinavagupta"})
check("PROBABLE on matching author+title", rp["status"] == "PROBABLE", rp["status"])

print("\n== 5. per-axis evidence ==")
check("evidence has title/author/shelfmark",
      set(r["evidence"].keys()) >= {"title_similarity", "author_similarity", "shelfmark_match"})

print("\n== 6. MACHINE_PROPOSED, not scholarly truth ==")
check("resolution_status = MACHINE_PROPOSED", r["resolution_status"] == "MACHINE_PROPOSED")

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (entity reconciliation engine works)"))
sys.exit(1 if failures else 0)

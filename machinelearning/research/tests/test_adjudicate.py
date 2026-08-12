#!/usr/bin/env python3
"""tests/test_adjudicate.py — validate the human-review → accepted loop.

The gold chain becomes scholarship when a human signs it. This tests:
  - all-accepted → EDITORIALLY_ACCEPTED (the promotion)
  - a rejection → MODIFIED (not falsely accepted)
  - missing decision → error
  - the signed record carries the reviewer + decisions (auditable)

Run: cd research && . .venv/bin/activate && python tests/test_adjudicate.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patala_ml.adjudicate import load_adjudication, Adjudication

PASS = 0
FAIL = 0


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        print(f"  ✓ {name}")
        PASS += 1
    else:
        print(f"  ✗ {name} {detail}")
        FAIL += 1


def main():
    # a minimal adjudication record (same shape as the real CL-3 package)
    record = {
        "adjudication_id": "adj:test",
        "decisions_required": [
            {"id": "D-THEME-ACCEPT", "default": "ACCEPT"},
            {"id": "D-ARG-ACCEPT", "default": "ACCEPT"},
            {"id": "D-LEXICAL-OPEN", "default": "APPROVE_AS_OPEN"},
        ],
        "proposed_theme": {"label": "Test Theme"},
        "proposed_argument": {"argument_id": "pt:argument:test"},
        "status": "AWAITING_REVIEW",
    }
    adj = Adjudication("adj:test", record)

    # 1. accept-all → EDITORIALLY_ACCEPTED
    print("== all-accepted promotes ==")
    r = adj.sign("editor-1", {"D-THEME-ACCEPT": "ACCEPT", "D-ARG-ACCEPT": "ACCEPT",
                              "D-LEXICAL-OPEN": "APPROVE_AS_OPEN"})
    check("sign returns ok", r["ok"], r)
    check("status → EDITORIALLY_ACCEPTED", r["status"] == "EDITORIALLY_ACCEPTED", r["status"])
    check("record carries reviewer", adj.record["reviewed_by"] == "editor-1")
    check("record carries decisions", adj.record["decisions"]["D-THEME-ACCEPT"] == "ACCEPT")
    check("accepted_theme set", adj.record.get("accepted_theme") == "Test Theme")

    # 2. a rejection → MODIFIED (not falsely accepted)
    print("\n== rejection stays modified ==")
    adj2 = Adjudication("adj:test2", dict(record))
    r2 = adj2.sign("editor-2", {"D-THEME-ACCEPT": "REJECT", "D-ARG-ACCEPT": "ACCEPT",
                                "D-LEXICAL-OPEN": "APPROVE_AS_OPEN"})
    check("rejection → MODIFIED", r2["status"] == "MODIFIED", r2["status"])
    check("not accepted", adj2.all_accepted is False)

    # 3. missing decision → error
    print("\n== missing decision errors ==")
    adj3 = Adjudication("adj:test3", dict(record))
    r3 = adj3.sign("editor-3", {"D-THEME-ACCEPT": "ACCEPT"})
    check("missing decision → ok False", r3["ok"] is False, r3)

    print(f"\n=== RESULT: {PASS} pass / {FAIL} fail ===")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()

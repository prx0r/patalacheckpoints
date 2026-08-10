#!/usr/bin/env python3
"""Dump the gold exemplars (and audit them) — no model calls.

Usage:
    python3 -m pipeline.exemplars           # print both exemplars as JSON
    python3 -m pipeline.exemplars --audit   # audit them + print the report
    python3 -m pipeline.exemplars --out-dir ./pipeline/exemplars_out
"""
from __future__ import annotations
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from exemplars import all_exemplars  # noqa: E402
from audit import audit_record, audit_ok, report  # noqa: E402


def main() -> None:
    out_dir = None
    args = sys.argv[1:]
    if "--audit" in args:
        audit = True
    else:
        audit = False
    for i, a in enumerate(args):
        if a == "--out-dir" and i + 1 < len(args):
            out_dir = args[i + 1]

    for ex in all_exemplars():
        pid = ex["passage_id"].replace(":", "_").replace(".", "_")
        findings = audit_record(ex)
        status = "PASS" if audit_ok(findings) else "FAIL"
        print(f"{ex['passage_id']}  [{status}]  stages={list(ex['stages'].keys())}")
        if audit:
            print(report(findings))
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
            p = os.path.join(out_dir, pid + ".json")
            with open(p, "w", encoding="utf-8") as f:
                json.dump(ex, f, ensure_ascii=False, indent=2)
            print(f"  wrote {p}")

    if not audit and not out_dir:
        # print one full exemplar as the reference shape
        print("\n--- reference shape (kramasadbhava.1.8) ---")
        print(json.dumps(all_exemplars()[0], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

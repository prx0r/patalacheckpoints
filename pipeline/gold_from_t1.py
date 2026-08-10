#!/usr/bin/env python3
"""Generate gold passage records from on-disk T1 files (no model calls).

For each (T1 file, verse) it builds a schema-valid record with T1 populated from
the real house material. These are the gold exemplars models imitate; the review
stages (R1/T2/R2/T3/T3.1/C1) are left for the model to fill, guided by the
gold exemplars in exemplars.py.

Usage:
    python3 pipeline/gold_from_t1.py <t1file> <work_id> <verse1> [verse2 ...]
    python3 pipeline/gold_from_t1.py --all-kramasadbhava
"""
from __future__ import annotations
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from from_t1 import parse_t1_verse, record_from_t1  # noqa: E402
from audit import audit_record, audit_ok  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gold_records")


def emit(rec: dict) -> str:
    os.makedirs(OUT, exist_ok=True)
    name = rec["passage_id"].replace(":", "_").replace(".", "_")
    path = os.path.join(OUT, name + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=2)
    return path


def main() -> None:
    args = sys.argv[1:]
    if args and args[0] == "--all-kramasadbhava":
        t1 = "/root/projects/sanskritree/translations/01_t1_working/kramasadbhava_patala1_pass1.md"
        verses = [v["id"] for v in parse_t1_verse(open(t1, encoding="utf-8").read())]
        paths = []
        for vid in verses:
            r = record_from_t1(t1, "kramasadbhava", vid, "Dyczkowski ed., Muktabodha (NGMPP A 209/23)")
            ok = audit_ok(audit_record(r))
            paths.append((emit(r), ok))
        print(f"wrote {len(paths)} gold records to {OUT}:")
        for p, ok in paths:
            print(f"  [{'PASS' if ok else 'FAIL'}] {p}")
        return

    if len(args) < 3:
        print(__doc__)
        sys.exit(1)
    t1, work = args[0], args[1]
    for vid in args[2:]:
        r = record_from_t1(t1, work, vid)
        print(f"  {emit(r)}  ({r['passage_id']})")


if __name__ == "__main__":
    main()

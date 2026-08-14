#!/usr/bin/env python3
"""docs/check_docs_audit.py — validate docs/DOCS-AUDIT.json + check archive files are flagged.

The anti-theatre / anti-redundancy check for the loose docs in docs/:
  1. every file in the audit exists on disk
  2. no duplicate file paths
  3. every ARCHIVE file should carry a visible "ARCHIVED/SUPERSEDED" marker so agents don't follow it
  4. every loose .md in docs/ (top-level) is accounted for in the audit

Run: python3 docs/check_docs_audit.py
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIT = ROOT / "docs/DOCS-AUDIT.json"
DOCS = ROOT / "docs"


def main() -> int:
    errors = []
    try:
        d = json.loads(AUDIT.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"FAIL: audit not valid JSON — {e}")
        return 1

    files = d.get("files", [])
    print(f"audit valid JSON: {len(files)} files classified")

    # 1. files exist on disk
    missing = [f["file"] for f in files if not (DOCS / f["file"]).exists()]
    if missing:
        errors.append(f"MISSING on disk: {missing}")

    # 2. no duplicate file paths
    dup = [f["file"] for f, c in Counter(x["file"] for x in files).items() if c > 1]
    if dup:
        errors.append(f"DUPLICATE file paths: {dup}")

    # 3. ARCHIVE files should carry a marker so agents don't follow them
    unmarked = []
    for f in files:
        if f["status"] == "ARCHIVE":
            txt = (DOCS / f["file"]).read_text(encoding="utf-8", errors="ignore")[:500]
            if not re.search(r"(?i)archiv|supersed|historical|old ", txt):
                unmarked.append(f["file"])
    if unmarked:
        errors.append(f"ARCHIVE files lacking an ARCHIVED/SUPERSEDED marker: {unmarked}")

    # 4. every top-level .md in docs/ is accounted for
    loose = sorted(p.name for p in DOCS.glob("*.md") if p.is_file())
    audited = {f["file"] for f in files}
    unaccounted = [x for x in loose if x not in audited and x not in ("DOCS-AUDIT.json",)]
    if unaccounted:
        errors.append(f"LOOSE .md NOT in audit: {unaccounted}")

    from collections import Counter as _C
    print("status distribution:", dict(_C(f["status"] for f in files)))
    print("all files exist ✓" if not missing else "files: ✗")
    print("file paths unique ✓" if not dup else "paths: ✗")
    print("archive files marked ✓" if not unmarked else f"archive markers: {unmarked}")
    print("all loose docs accounted ✓" if not unaccounted else f"unaccounted: {unaccounted}")

    if errors:
        print("\nFAILURES:")
        for e in errors:
            print(" -", e)
        return 1
    print("\nDOCS AUDIT VALID — every loose doc is classified; archive docs are marked; nothing is unaccounted.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

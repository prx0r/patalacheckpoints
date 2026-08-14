#!/usr/bin/env python3
"""docs/vision/check_manifest.py — validate VISION-MANIFEST.json (the anti-redundancy check).

Every vision doc must have EXACTLY ONE distinct role. This validator fails if:
  1. the manifest is not valid JSON
  2. any two docs claim the same role (the "no 3 files saying the same thing" rule)
  3. any file path referenced in the manifest doesn't exist on disk

Run: python3 docs/vision/check_manifest.py
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
MANIFEST = ROOT / "docs/vision/VISION-MANIFEST.json"
VISION = ROOT / "docs/vision"


def main() -> int:
    errors = []
    try:
        d = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"FAIL: manifest is not valid JSON — {e}")
        return 1

    docs = d.get("docs", [])
    print(f"manifest valid JSON: {len(docs)} docs")

    # 1. duplicate roles (the anti-redundancy rule)
    roles = [x.get("role", "").strip().lower() for x in docs]
    dup = [r for r, n in Counter(roles).items() if n > 1]
    if dup:
        errors.append(f"DUPLICATE ROLES (no two docs may share a role): {dup}")

    # 2. duplicate names (accurate-distinct-name rule)
    names = [x.get("name", "").strip() for x in docs]
    dup_name = [n for n, c in Counter(names).items() if c > 1]
    if dup_name:
        errors.append(f"DUPLICATE NAMES: {dup_name}")

    # 3. referenced files exist on disk
    missing = []
    for x in docs:
        p = VISION / x["file"]
        if not p.exists():
            missing.append(x["file"])
    if missing:
        errors.append(f"MISSING FILES (referenced but not on disk): {missing}")

    # 4. unique file paths
    files = [x["file"] for x in docs]
    dup_file = [f for f, c in Counter(files).items() if c > 1]
    if dup_file:
        errors.append(f"DUPLICATE FILE PATHS: {dup_file}")

    print("validated: roles unique ✓" if not dup else "roles: ✗")
    print("validated: names unique ✓" if not dup_name else "names: ✗")
    print("validated: files exist ✓" if not missing else "files: ✗")
    print("validated: file paths unique ✓" if not dup_file else "files: ✗")

    if errors:
        print("\nFAILURES:")
        for e in errors:
            print(" -", e)
        return 1
    print("\nMANIFEST VALID — every vision doc has one distinct role, one distinct name, one real file.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

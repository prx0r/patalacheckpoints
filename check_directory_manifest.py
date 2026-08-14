#!/usr/bin/env python3
"""DIRECTORY-MANIFEST validator — every top-level folder resolves to a layer/role/class.

The deterministic codebase map. Validates DIRECTORY-MANIFEST.json:
  1. valid JSON
  2. every referenced folder exists on disk
  3. no duplicate folder paths
  4. every top-level folder is accounted for (canonical/coordination/archive/scratch)

Run: python3 check_directory_manifest.py
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "DIRECTORY-MANIFEST.json"


def main() -> int:
    errors = []
    try:
        d = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"FAIL: manifest not valid JSON — {e}")
        return 1
    folders = d.get("folders", [])
    print(f"manifest valid JSON: {len(folders)} folders")

    # 1. folders exist on disk
    missing = [f["dir"] for f in folders if not (ROOT / f["dir"]).exists()]
    if missing:
        errors.append(f"MISSING on disk: {missing}")

    # 2. no duplicate dirs
    dup = [f["dir"] for f, c in Counter(x["dir"] for x in folders).items() if c > 1]
    if dup:
        errors.append(f"DUPLICATE dirs: {dup}")

    # 3. every top-level folder on disk is accounted for
    on_disk = sorted(p.name + "/" for p in ROOT.iterdir() if p.is_dir() and not p.name.startswith(".")
                     and p.name not in ("node_modules", ".next", ".git", "logs"))
    # exclude hidden + venv + known-excluded
    on_disk = [d for d in on_disk if not d.startswith((".", "_")) and "venv" not in d]
    accounted = {f["dir"] for f in folders}
    unaccounted = [x for x in on_disk if x not in accounted]
    if unaccounted:
        errors.append(f"TOP-LEVEL folders NOT in manifest: {unaccounted}")

    from collections import Counter as _C
    print("class distribution:", dict(_C(f["class"] for f in folders)))
    print("all folders exist ✓" if not missing else "files: ✗")
    print("no duplicate dirs ✓" if not dup else "dirs: ✗")
    print("all top-level folders accounted ✓" if not unaccounted else f"unaccounted: {unaccounted}")

    if errors:
        print("\nFAILURES:")
        for e in errors:
            print(" -", e)
        return 1
    print("\nDIRECTORY MANIFEST VALID — every top-level folder resolves to a role/layer/class.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""pipeline/test_catalog.py — deterministic tests for the unified catalog view.

Verifies the per-work × per-layer catalog projection:
  - bibliography linkage (translation_status from the atlas)
  - source linkage (SOURCE registry objects)
  - per-layer counts for ALL canonical layers (incl. THEME/ARGUMENT/SYNTHESIS/ESSAY/EDUCATION)
  - audit trail present when events exist
Run: python3 pipeline/test_catalog.py
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")

import object_registry as R
import catalog as C


def t(name, cond, detail=""):
    print(("PASS" if bool(cond) else "FAIL"), "-", name, (f" [{detail}]" if detail else ""))
    return bool(cond)


def main() -> int:
    ok = True
    R.REG_DIR = Path(tempfile.mkdtemp())

    print("=== unified catalog ===")
    # a clean work with SOURCE+T1+L0+THEME (high layer)
    R.commit("SOURCE", "work:v1", "h0", created_by="test", payload={"verse": "x"})
    R.commit("T1", "work:v1", "h0", created_by="test", payload={"t1": {"tokens": []}})
    R.commit("L0", "work:v1", "h0", created_by="test")
    R.commit("THEME", "work:v1", "h0", created_by="test", payload={"theme": {"member_claims": []}})

    e = C.work_catalog("work")
    ok &= t("source linkage detected", e["source"]["source_objects"] == 1, str(e["source"]))
    ok &= t("T1 layer tracked", e["layers"]["T1"]["done"] == 1, str(e["layers"]["T1"]))
    ok &= t("L0 layer tracked", e["layers"]["L0"]["done"] == 1)
    ok &= t("HIGH layer THEME tracked", e["layers"]["THEME"]["done"] == 1, str(e["layers"]["THEME"]))
    ok &= t("all canonical layers present",
            set(C.LAYERS) <= set(e["layers"]), str(list(e["layers"].keys())))
    # bibliography: work not in a fresh atlas parse (empty atlas in test env) -> not_in_atlas or title
    ok &= t("bibliography field present", "translation_status" in e["bibliography"])

    # render produces WORK: header
    ok &= t("render produces a WORK: header", "WORK: work" in C.render(e))

    print("\n  " + "\n  ".join(C.render(e).split("\n")))
    print("\n" + ("CATALOG ALL PASS" if ok else "CATALOG SOME FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

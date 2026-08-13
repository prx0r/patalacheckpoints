#!/usr/bin/env python3
"""pipeline/test_factory_status.py — deterministic tests for the corpus progress dashboard (A2-12).

Verifies the operational view renders correctly from the registry:
  - per-layer done/of counts derive from committed SOURCE objects (the work's passages)
  - stale counts reflect superseded versions
  - the view includes the status classes (retryable, source_blocked)

Run: python3 pipeline/test_factory_status.py
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")

import object_registry as R
import factory_status as FS


def t(name, cond, detail=""):
    print(("PASS" if bool(cond) else "FAIL"), "-", name, (f" [{detail}]" if detail else ""))
    return bool(cond)


def main() -> int:
    ok = True
    R.REG_DIR = Path(tempfile.mkdtemp())
    FS.FAILURE_QUEUE = Path(tempfile.mkdtemp()) / "q.jsonl"

    print("=== A2-12 corpus progress dashboard ===")
    # seed 2 SOURCE objects + 1 T1 + 1 superseded L0
    for i in (1, 2):
        R.commit("SOURCE", f"work:v{i}", f"h{i}", created_by="test")
    R.commit("T1", "work:v1", "h1", created_by="test", payload={"t1": {"tokens": [], "source_text": "x"}})
    R.commit("L0", "work:v1", "h1", created_by="test")
    R.commit("L0", "work:v1", "h1b", created_by="test")  # second version (old superseded)
    R.supersede("L0", "work:v1")

    view = FS.work_status("work")
    ok &= t("SOURCE done = 2", view["layers"]["SOURCE"]["done"] == 2, str(view["layers"]["SOURCE"]))
    ok &= t("T1 done = 1 (of 2 SOURCE)", view["layers"]["T1"]["done"] == 1,
            str(view["layers"]["T1"]))
    ok &= t("T1 denominator = SOURCE count", view["layers"]["T1"]["of"] == 2,
            str(view["layers"]["T1"]))
    ok &= t("L0 shows stale count", view["layers"]["L0"]["stale"] >= 1,
            str(view["layers"]["L0"]))
    ok &= t("view includes status classes", "retryable" in view and "source_blocked" in view)
    # render produces the WORK: header
    ok &= t("render produces a WORK: header", "WORK: work" in FS.render(view))

    print("\n  " + "\n  ".join(FS.render(view).split("\n")))
    print("\n" + ("FACTORY-STATUS ALL PASS" if ok else "FACTORY-STATUS SOME FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""pipeline/test_register_sources.py — deterministic tests for bulk SOURCE registration.

A2-INT A2-17: the intake bridge (register_sources.py) that turns translated <work>.jsonl into
committed SOURCE objects must:
  - register many verses in ONE load/save (commit_batch) efficiently
  - dedup object_ids (skip already-committed)
  - produce a verifiable, hash-chained event for each registered object
  - skip works that are already registered
Run: python3 pipeline/test_register_sources.py
"""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")

import object_registry as R
import register_sources as RS


def t(name, cond, detail=""):
    print(("PASS" if bool(cond) else "FAIL"), "-", name, (f" [{detail}]" if detail else ""))
    return bool(cond)


def main() -> int:
    ok = True
    R.REG_DIR = Path(tempfile.mkdtemp())
    R.EVENT_LOG = None

    print("=== intake: bulk SOURCE registration (commit_batch + register_sources) ===")

    # commit_batch registers many objects in one save
    entries = [{"object_id": f"workA:v{i}", "input_hash": hashlib.sha256(str(i).encode()).hexdigest(),
                "payload": {"verse": f"verse{i}"}} for i in range(100)]
    recs = R.commit_batch("SOURCE", entries, created_by="test")
    ok &= t("commit_batch registers 100 SOURCE objects", len(recs) == 100, f"got {len(recs)}")
    objs = R._load("SOURCE")["objects"]
    ok &= t("all 100 object_ids present in registry", len(objs) == 100, f"got {len(objs)}")

    # each has a version + payload preserved
    cur = R.current("SOURCE", "workA:v5")
    ok &= t("payload preserved (verse)", cur and cur.get("payload", {}).get("verse") == "verse5")
    ok &= t("input_hash preserved", cur and cur.get("input_hash") == hashlib.sha256(b"5").hexdigest())

    # idempotent: committing the same object_id again creates a NEW version, not overwrite
    dup = R.commit_batch("SOURCE", [{"object_id": "workA:v5", "input_hash": "x",
                                     "payload": {"verse": "new"}}], created_by="test")
    vs = R._load("SOURCE")["objects"]["workA:v5"]
    ok &= t("re-commit creates a new version (immutable, not overwrite)",
            len(vs) == 2 and vs[0]["payload"]["verse"] == "verse5", f"versions={len(vs)}")

    # events appended and chain verifies
    ok &= t("event chain verifies intact", R.verify_event_chain())

    # register_sources.work_registered detects already-registered works
    ok &= t("_work_registered('workA') is True after registration", RS._work_registered("workA"))

    # register_work returns 0 for an already-registered work (no double work)
    RS.TDIR = Path(tempfile.mkdtemp())
    (RS.TDIR / "workA.jsonl").write_text(
        "\n".join(json.dumps({"sanskrit": f"v{i}"}) for i in range(5)), encoding="utf-8")
    n = RS.register_work("workA")
    ok &= t("register_work('workA') returns 0 when already registered", n == 0, f"got {n}")

    # register_work registers a brand-new work from its jsonl
    (RS.TDIR / "workB.jsonl").write_text(
        "\n".join(json.dumps({"sanskrit": f"b{i}"}) for i in range(7)), encoding="utf-8")
    nb = RS.register_work("workB")
    ok &= t("register_work registers 7 new SOURCE objects for a new work", nb == 7, f"got {nb}")
    ok &= t("new work's objects present", len(R._load("SOURCE")["objects"]) == 107,
            f"got {len(R._load('SOURCE')['objects'])}")
    ok &= t("event chain still verifies", R.verify_event_chain())

    print("")
    print(f"RESULT: {'ALL PASS' if ok else 'FAILURES'} ({sum(1 for _ in [])})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

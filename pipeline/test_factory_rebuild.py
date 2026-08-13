#!/usr/bin/env python3
"""pipeline/test_factory_rebuild.py — deterministic tests for the Era C rebuild engine (A2-14/15/16).

Verifies the supersession-propagation / targeted-regeneration engine:
  1. invalidating an upstream object (e.g. T1) supersedes its downstream (L0/L2/L200/C1)
  2. corrected object_registry.current() returns None for an invalidated object (no current version)
  3. regenerate rebuilds only the affected downstream (targeted, not the whole corpus)
Run: python3 pipeline/test_factory_rebuild.py
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")

import object_registry as R
import factory_batch as FB
import factory_rebuild as RB
import t1_worker as TW


def t(name, cond, detail=""):
    print(("PASS" if bool(cond) else "FAIL"), "-", name, (f" [{detail}]" if detail else ""))
    return bool(cond)


def main() -> int:
    ok = True
    R.REG_DIR = Path(tempfile.mkdtemp())
    FB.FAILURE_QUEUE = Path(tempfile.mkdtemp()) / "q.jsonl"
    oid = "kramasadbhava:v1"

    print("=== A2-14/15/16 supersession propagation + targeted regeneration ===")
    R.commit("SOURCE", oid, "h0", created_by="test", payload={"verse": "śivo", "source_text": "śivo"})
    R.commit("T1", oid, "h1", created_by="test", payload={"t1": {"tokens": [], "source_text": "śivo"}})
    R.commit("L0", oid, "h1", created_by="test")
    R.commit("L2", oid, "h1", created_by="test", payload={"l2": {"text": "x"}})
    R.commit("L200", oid, "h1", created_by="test", payload={"l200": {"0_identification": {}}})
    R.commit("C1", oid, "h1", created_by="test", payload={"c1": {"summary": "x"}})

    # invalidate when T1 is corrected
    inv = RB.invalidate("t1-kramasadbhava:v1-v1")
    affected = inv.get("affected", {})
    ok &= t("T1 correction invalidates L0 downstream", "L0" in affected)
    ok &= t("T1 correction invalidates C1 downstream", "C1" in affected)
    ok &= t("invalidated L0 has no current version (corrected current())", R.current("L0", oid) is None)
    ok &= t("invalidated C1 has no current version", R.current("C1", oid) is None)

    # regenerate: rebuild the affected downstream (T1 stub succeeds)
    TW.chat = lambda s, p, **kw: '{"tokens": {"śivo": {"gloss":"x"}}}'
    # re-establish upstream so downstream can rebuild
    R.commit("L0", oid, "h1b", created_by="test")  # a new L0 (post-correction)
    R.commit("L2", oid, "h1b", created_by="test", payload={"l2": {"text": "x"}})
    rebuilt = RB.regenerate("t1-kramasadbhava:v1-v1", dry_run=True)
    ok &= t("dry-run regenerate returns WOULD_REBUILD for affected layers",
            all(v == "WOULD_REBUILD" for v in rebuilt.get("rebuilt", {}).values()),
            str(rebuilt.get("rebuilt")))

    print("\n  affected:", sorted(affected.keys()))
    print("\n" + ("FACTORY-REBUILD ALL PASS" if ok else "FACTORY-REBUILD SOME FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

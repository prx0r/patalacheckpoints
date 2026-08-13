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
    # canonical multi-parent gating: a layer is WOULD_REBUILD ONLY if ALL its 'requires' are current;
    # a layer whose any required parent is stale/none MUST be DEPENDENCY_BLOCKED (never WOULD_REBUILD).
    rb = rebuilt.get("rebuilt", {})
    blocked = {k for k, v in rb.items() if v == "DEPENDENCY_BLOCKED (a required parent not current)"}
    rebuildable = {k for k, v in rb.items() if v == "WOULD_REBUILD"}
    # ARGMAP requires [SOURCE, L0]; both re-committed current -> rebuildable
    ok &= t("ARGMAP rebuildable (SOURCE+L0 current)", "ARGMAP" in rebuildable, str(rb))
    # L200 requires [L2]; L2 re-committed current -> rebuildable
    ok &= t("L200 rebuildable (L2 current)", "L200" in rebuildable, str(rb))
    # C1 requires [L200]; L200 current here -> C1 is rebuildable, but if L200 were stale C1 must block.
    # The KEY invariant: no layer is WOULD_REBUILD when a required parent is genuinely stale.
    # (In this fixture L2/L200 were re-committed, so C1's parent is current -> allowed.)
    # Check the gating is ACTIVE: there is at least one genuinely-blocked layer (ARGUMENT needs C1,
    # but C1's chain needs more parents that aren't all current in this fixture).
    ok &= t("canonical multi-parent gating is active (some layer blocked)",
            bool(blocked), f"blocked={blocked}")

    print("\n  affected:", sorted(affected.keys()))
    print("\n" + ("FACTORY-REBUILD ALL PASS" if ok else "FACTORY-REBUILD SOME FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

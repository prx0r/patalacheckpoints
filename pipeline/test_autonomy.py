#!/usr/bin/env python3
"""pipeline/test_autonomy.py — tests for the generic autonomy controller + object registry.

Covers: per-layer registry (commit/current/idempotency/supersession/three-state), the controller's
eligibility DAG, cascading supersession, and the tick run report. Fail fast: exits 1 on any failure.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import object_registry as R
import autonomy as A


def t(name, cond):
    print(("PASS" if cond else "FAIL"), "-", name)
    return cond


def main() -> int:
    ok = True
    oid = "TEST:OBJ"
    ih = "hash-v1"

    # isolate registries to a temp dir so we never touch real data
    tmp = tempfile.mkdtemp()
    R.REG_DIR = __import__("pathlib").Path(tmp)

    # registry: commit + current
    c = R.commit("L0", oid, ih, created_by="test")
    ok &= t("registry: commit returns a version", c["version"].startswith("l0-"))
    ok &= t("registry: current exists", R.current("L0", oid) is not None)
    ok &= t("registry: is_committed (idempotency by input hash)", R.is_committed("L0", oid, ih))
    ok &= t("registry: different input not committed", not R.is_committed("L0", oid, "other"))

    # three-state ladder
    R.set_status("L0", oid, c["version"], R.ENGINEERING_VALIDATED, "test")
    ok &= t("registry: three-state ladder (ENGINEERING_VALIDATED)",
            R.current("L0", oid)["status"] == R.ENGINEERING_VALIDATED)

    # eligibility DAG
    ok &= t("eligibility: L1 eligible after L0 committed", A.eligible_for("L1", oid, ih) == "")
    ok &= t("eligibility: L2 blocked until L1", A.eligible_for("L2", oid, ih) == "prereq_L1_missing")
    R.commit("L1", oid, ih, created_by="test")
    # canonical stack: L2 depends on L1 AND the argument map (the lateral guide)
    ok &= t("eligibility: L2 blocked until ARGMAP", A.eligible_for("L2", oid, ih) == "prereq_ARGMAP_missing")
    R.commit("ARGMAP", oid, ih, created_by="test")
    ok &= t("eligibility: L2 eligible after L1 + ARGMAP committed", A.eligible_for("L2", oid, ih) == "")
    ok &= t("eligibility: L0 idempotent (already committed)", A.eligible_for("L0", oid, ih) != "")

    # controller find_eligible + tick (while L1 is valid)
    elig = A.find_eligible("L2", [{"object_id": oid, "input_hash": ih}])
    ok &= t("controller: find_eligible returns the object", any(e["object_id"] == oid for e in elig))
    rep = A.tick(layers=["L2"], dry_run=True,
                 inputs={"L2": [{"object_id": oid, "input_hash": ih}]})
    ok &= t("controller: tick emits a run report", "run_id" in rep and "layers" in rep)
    rep2 = A.tick(layers=["L2"], dry_run=False,
                  inputs={"L2": [{"object_id": oid, "input_hash": ih}]})
    ok &= t("controller: tick commits an eligible object", rep2["committed"] == 1)
    ok &= t("controller: committed object now not eligible", A.eligible_for("L2", oid, ih) != "")

    # supersession / cascading stale (after L2 is committed)
    R.supersede("L1", oid)
    ok &= t("supersession: L1 current marked stale", R.current("L1", oid)["superseded"] is True)
    ok &= t("supersession: L1 no longer idempotent-committed (superseded)",
            not R.is_committed("L1", oid, ih))
    ok &= t("supersession: L2 now blocked because its prereq L1 is stale",
            A.eligible_for("L2", oid, ih) != "")

    print("\n" + ("ALL PASS" if ok else "SOME FAILED"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

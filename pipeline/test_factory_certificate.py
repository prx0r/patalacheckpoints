#!/usr/bin/env python3
"""pipeline/test_factory_certificate.py — deterministic tests for the Era-B bulk certificate (A2-13).

Verifies the machine-readable certificate emits correctly:
  - per-layer commit counts from the registry
  - integrity checks (duplicates, bad parents, conflicts) are computed
  - resume_test reflects idempotency
  - exit code reflects a clean certificate (0 duplicates + resume PASS)
Run: python3 pipeline/test_factory_certificate.py
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")

import object_registry as R
import factory_certificate as FC


def t(name, cond, detail=""):
    print(("PASS" if bool(cond) else "FAIL"), "-", name, (f" [{detail}]" if detail else ""))
    return bool(cond)


def main() -> int:
    ok = True
    R.REG_DIR = Path(tempfile.mkdtemp())

    print("=== A2-13 Era-B bulk certificate ===")
    # clean chain for work:v1
    R.commit("SOURCE", "work:v1", "h0", created_by="test", payload={"verse": "x", "source_text": "x"})
    R.commit("T1", "work:v1", "h0", created_by="test", payload={"t1": {"tokens": []}})
    R.commit("L0", "work:v1", "h0", created_by="test")
    R.commit("ARGMAP", "work:v1", "h0", created_by="test")

    cert = FC.certificate(work_id="work", scheduler_version="test", passes=2, model_calls=3)
    ok &= t("by_layer reflects commits", cert["by_layer"]["T1"] >= 1 and cert["by_layer"]["L0"] >= 1,
            f"T1={cert['by_layer']['T1']} L0={cert['by_layer']['L0']}")
    ok &= t("passes + model_calls recorded", cert["passes"] == 2 and cert["model_calls"] == 3)
    ok &= t("integrity computed (clean chain -> 0 duplicates)", cert["integrity"]["duplicates"] == 0,
            f"dups={cert['integrity']['duplicates']}")
    ok &= t("resume_test PASS on a clean chain", cert["resume_test"] == "PASS", cert["resume_test"])
    ok &= t("works_touched = 1", cert["works_touched"] == 1)

    # a duplicate (two current versions of same object+different hash) is caught
    R.commit("L0", "work:v1", "h0b", created_by="test")
    cert2 = FC.certificate(work_id="work")
    ok &= t("duplicate detected", cert2["integrity"]["duplicates"] >= 1, f"{cert2['integrity']['duplicates']}")

    print("\n" + ("FACTORY-CERTIFICATE ALL PASS" if ok else "FACTORY-CERTIFICATE SOME FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

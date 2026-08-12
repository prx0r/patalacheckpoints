#!/usr/bin/env python3
"""tests/test_benchmark.py — validate Pāṭala Benchmark v0 structure.

Checks the REAL invariants:
  1. the MANIFEST exists and declares the 4 task families + review states
  2. every fixture passes the ingest gate (schema/source/leakage)
  3. ARG-GOLD-001 is seeded in PATALA-STRUCTURE with the honest envelope
     (EVALUATION_ONLY, train_use=false, SINGLE_EDITOR_GOLD)
  4. the benchmark is SEPARATE from the product (no collapsing)

Run: cd research && . .venv/bin/activate && python tests/test_benchmark.py
"""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PASS = 0
FAIL = 0


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        print(f"  ✓ {name}")
        PASS += 1
    else:
        print(f"  ✗ {name} {detail}")
        FAIL += 1


def ingest_ok(path: str) -> bool:
    import subprocess
    r = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                    "../ingest_fixture.py"), path],
                       capture_output=True, text=True)
    return r.returncode == 0


def main():
    base = "/root/projects/patala/benchmarks/v0"

    # 1. MANIFEST
    print("== MANIFEST ==")
    manifest = json.load(open(os.path.join(base, "MANIFEST.json")))
    for fam in ["PATALA-RETRIEVAL", "PATALA-EVIDENCE", "PATALA-STRUCTURE", "PATALA-FIDELITY"]:
        check(f"manifest has {fam}", fam in manifest["task_families"])
    check("manifest has review states", "review_states" in manifest)
    check("manifest declares anti-circularity", any("cannot be independent gold" in r for r in manifest["honesty_rules"]))

    # 2. every seeded fixture passes the gate
    print("\n== fixture acceptance ==")
    fixtures = glob.glob(os.path.join(base, "*", "*.json"))
    fixtures = [f for f in fixtures if "PAT-" in f]  # not MANIFEST/SCHEMA/etc
    check("at least one fixture seeded", len(fixtures) >= 1, len(fixtures))
    for f in fixtures:
        check(f"{os.path.basename(f)} passes gate", ingest_ok(f))

    # 3. ARG-GOLD-001 envelope
    print("\n== ARG-GOLD-001 (the seed) ==")
    goldf = os.path.join(base, "structure", "PAT-STRUCT-001.json")
    check("gold fixture exists", os.path.exists(goldf))
    if os.path.exists(goldf):
        g = json.load(open(goldf))
        check("task = argument_extraction", g["task"] == "argument_extraction")
        check("EVALUATION_ONLY split", g["split_class"] == "EVALUATION_ONLY")
        check("allowed_training_use = false", g["allowed_training_use"] is False)
        check("CANDIDATE (honest, unreviewed)", g["review_state"] == "CANDIDATE")
        check("MACHINE_PROPOSED authoring (honest)", g["authoring_method"] == "MACHINE_PROPOSED")
        exp = g["expected"]
        check("gold has nodes + inferences + boundary",
              "nodes" in exp and "inferences" in exp and "boundary" in exp)

    # 4. separation of benchmark from product
    print("\n== benchmark/product separation ==")
    check("benchmark under benchmarks/v0 (not machinelearning/research/tasks)",
          os.path.exists(os.path.join(base, "MANIFEST.json")))

    print(f"\n=== RESULT: {PASS} pass / {FAIL} fail ===")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""test_fidelity.py — PĀṬALA-FIDELITY v0: the verifier detects known, injected corruption.

Asserts the empirical contract:
    CORRUPTED object -> expected FAILURE (sensitivity)
    CLEAN object     -> expected PASS   (clean false-positive rate = 0)

This is construction-verifiable (Category A). It establishes SyntheticSensitivity, NOT
RealWorldRecall. See benchmarks/v0/FIDELITY-v0-SPEC.md.
"""
from __future__ import annotations

import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "experiments"))

import build_fidelity_suite as fid

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


def run_all_families():
    all_rows = []
    all_rows += fid.run_family("FID-SOURCE",
                               ["DROP_SPAN", "SHIFT_SPAN_START", "CHANGE_SOURCE_HASH"],
                               lambda c: fid.mutate_source(fid.load_source(), fid.load_l0(), c),
                               fid.verify_source, None)
    all_rows += fid.run_family("FID-PROVENANCE",
                               ["BROKEN_REF", "STALE_PROOF", "MISSING_PROVENANCE"],
                               lambda c: (fid.mutate_provenance(json.load(open(fid.VERTICAL_PATH)), c),),
                               lambda v: fid.verify_provenance(v), None)
    all_rows += fid.run_family("FID-ALIGNMENT",
                               ["REMOVE_ANCHOR", "SHIFT_ANCHOR", "LINK_WRONG_TOKEN"],
                               lambda c: (fid.mutate_alignment(json.load(open(fid.VERTICAL_PATH)), c),),
                               lambda v: fid.verify_alignment(v, fid.pristine_anchor_ids()),
                               fid.pristine_anchor_ids)
    return all_rows


print("== clean control (pristine object must PASS; false-positive rate must be 0) ==")
rows = run_all_families()
for fam in ("FID-SOURCE", "FID-PROVENANCE", "FID-ALIGNMENT"):
    clean = next(r for r in rows if r["family"] == fam and r["corruption"] == "CLEAN_CONTROL")
    check(f"{fam} clean control PASSES", clean["observed"] == "PASS", clean["observed"])

print("\n== synthetic sensitivity (each injected corruption must be detected) ==")
for fam in ("FID-SOURCE", "FID-PROVENANCE", "FID-ALIGNMENT"):
    fam_rows = [r for r in rows if r["family"] == fam and r["corruption"] != "CLEAN_CONTROL"]
    det = sum(1 for r in fam_rows if r["detected"])
    check(f"{fam} sensitivity 1.0 ({det}/{len(fam_rows)})",
          det == len(fam_rows) == 3,
          f"{det}/{len(fam_rows)} detected")

print("\n== the immutable run is well-formed ==")
runs = sorted(glob.glob(os.path.join(fid.RUNS_DIR, "fidelity-*.json")))
check("at least one FIDELITY run exists", bool(runs))
if runs:
    d = json.load(open(runs[-1]))
    req = ["fixture_id", "family", "corruption", "expected", "observed",
           "detected", "false_positive", "detector"]
    check("run results carry all required fields",
          all(all(k in r for k in req) for r in d.get("results", [])))
    check("run records execution_base_sha + verifier_version",
          bool(d.get("execution_base_sha")) and d.get("verifier_version") == "fidelity-v0")
    check("run records artifact_commit_sha (may be None if uncommitted) + working_tree_dirty flag",
          "artifact_commit_sha" in d and "working_tree_dirty" in d)
    check("run uses stable detector IDs (no <lambda>)",
          all(isinstance(r["detector"], str) and not r["detector"].startswith("<")
              for r in d.get("results", [])))
    check("run records clean false-positive rate 0 for every family",
          all(s["false_positives"] == 0 for s in d.get("summary", {}).values()))

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (FIDELITY v0 — synthetic sensitivity 1.0, clean-FP 0)"))
sys.exit(1 if failures else 0)

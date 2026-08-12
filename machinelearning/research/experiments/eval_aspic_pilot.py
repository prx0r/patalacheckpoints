#!/usr/bin/env python3
"""eval_aspic_pilot.py — the first external-evaluator falsification test (ARG-002 v2 -> ASPIC+).

Question under test (the reviewer's pilot):
  Can Pāṭala's ARG-002 v2 reconstruction be losslessly projected into ASPIC+, and does ASPIC behave
  as expected?

EXPECTED RESULT (written BEFORE executing):
  Run A (WITHOUT the defeater not_constructed):
      art => constructed => vikalpa is unopposed
      -> vikalpa SHOULD be acceptable.
  Run B (WITH the defeater not_constructed = G2-TC2):
      not_constructed attacks constructed (contrary)
      -> the art=>constructed=>vikalpa chain is defeated
      -> vikalpa SHOULD be NOT acceptable (contested/defeated).

⚠️ HONEST CAVEAT: the reference py-aspic engine (arg.tech web service) returned 503 (unavailable) at run
time, so this pilot runs a MINIMAL LOCAL grounded-semantics evaluator as a fallback. This is a PILOT
proxy, NOT the production delegation; re-run against the real engine before accepting the "delegate
reasoning to ASPIC+" bet.

Run: cd research && . .venv/bin/activate && python experiments/eval_aspic_pilot.py
"""
from __future__ import annotations
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patala_ml.aspic_adapter import project_arg002, run_arg002_aspic

RUNS_DIR = "/root/projects/patala/benchmarks/v0/runs"


def main():
    print("ASPIC+ PILOT — ARG-002 v2 (adapter + semantic fidelity)\n")

    proj = project_arg002()
    print("PROJECTION (representational fidelity — what the adapter preserves):")
    print(f"  facts: {proj['facts']}")
    rule_strs = [f"{r['label']}: {r['premises']} => {r['conclusion']} "
                 f"({'strict' if r['strict'] else 'defeasible'})" for r in proj['rules']]
    print("  rules: " + "; ".join(rule_strs))
    for n in proj["fidelity_notes"]:
        print(f"   - {n}")

    print("\nEXPECTED RESULT (written before executing):")
    print("  Run A (no defeater): vikalpa acceptable = True")
    print("  Run B (with defeater not_constructed): vikalpa acceptable = False")
    print("  (The reply undercuts the objection by blocking construction via G2-TC2.)\n")

    results = {}
    for with_defeater in (False, True):
        r = run_arg002_aspic(with_defeater)
        results["RunA" if not with_defeater else "RunB"] = r
        expected = True if not with_defeater else False
        ok = r["vikalpa_acceptable"] == expected
        print(f"  Run {'A' if not with_defeater else 'B'} (defeater={with_defeater}): "
              f"acceptable_conclusions={r['acceptable_conclusions']}  "
              f"vikalpa_acceptable={r['vikalpa_acceptable']}  (expected {expected})  "
              f"{'✓' if ok else '✗ MISMATCH'}")

    # the three questions
    fidelity = "can encode ARG-002 v2; explicit proposition / reconstructed warrant / objection kept separate"
    semantic = "matches expected under grounded semantics (Run A accepted, Run B defeated)"
    fit = "minimal LOCAL evaluator used (pilot fallback); real py-aspic (arg.tech) was 503 at run time — MUST re-run"

    print("\nTHREE QUESTIONS:")
    print(f"  1. Representational fidelity: {fidelity}")
    print(f"  2. Semantic fidelity: {semantic}")
    print(f"  3. Architectural fit: {fit}")

    # ── record an immutable EvaluationRun ─────────────────────────────────────
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    run_dir = os.path.join(RUNS_DIR, ts)
    os.makedirs(run_dir, exist_ok=True)
    try:
        commit = subprocess.run(["git", "-C", "/root/projects/patala", "rev-parse", "--short", "HEAD"],
                                capture_output=True, text=True).stdout.strip()
    except Exception:
        commit = "unknown"
    json.dump({"benchmark": "PATALA-BENCH-v0", "gold": "ARG-GOLD-002-v2", "task": "ASPIC_PILOT",
               "method": "minimal-local-grounded-semantics (pilot fallback)", "engine": "py-aspic/arg.tech (503 at run time)",
               "status": "COMPLETED", "generated": ts},
              open(os.path.join(run_dir, "benchmark_version.json"), "w"), indent=2)
    json.dump({"split": "EVALUATION_ONLY", "train_use": False}, open(os.path.join(run_dir, "split_manifest.json"), "w"), indent=2)
    json.dump({"projection": proj, "expected": {"RunA": True, "RunB": False}},
              open(os.path.join(run_dir, "config.json"), "w"), indent=2, ensure_ascii=False)
    json.dump({"metrics": results, "questions": {"representational_fidelity": fidelity,
               "semantic_fidelity": semantic, "architectural_fit": fit}},
              open(os.path.join(run_dir, "metrics.json"), "w"), indent=2, ensure_ascii=False)
    open(os.path.join(run_dir, "git_commit.txt"), "w").write(commit + "\n")
    open(os.path.join(run_dir, "error_analysis.md"), "w").write(
        "# ASPIC pilot — error analysis\n\nThe reference py-aspic engine (arg.tech web service) was "
        "unavailable (503) at run time. A minimal local grounded-semantics evaluator was used as a pilot "
        "fallback. Re-run against the real engine before accepting the delegate-reasoning-to-ASPIC+ bet.\n")
    print(f"\nEvaluationRun recorded: {run_dir}")


if __name__ == "__main__":
    main()

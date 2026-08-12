#!/usr/bin/env python3
"""eval_extraction.py — run the primitive extractor BLIND against the 5 ARG-GOLD fixtures + record a run.

Build 4 of the CP4 plan (NEXT-STEPS): measure whether automatic proposition extraction is worth
building, using the frozen Argument Gold as ground truth. The extractor reads ONLY the C1 body
(blind — it never sees the fixture's `expected`). It is a deliberately-generic BASELINE, not a
capability; nothing here promotes extraction (CLAIMS P-003 stays NOT_ESTABLISHED).

Metrics (per PATALA-STRUCTURE / METRICS.md): proposition P/R/F1, role macro-F1, explicitness macro-F1,
grounding precision, inference recovery, inference-scheme macro-F1, scope-fidelity error, abstention.
Results are written as an immutable BenchmarkRun under benchmarks/v0/runs/<ts>/.

Run: cd research && . .venv/bin/activate && python experiments/eval_extraction.py
"""
from __future__ import annotations

import json
import os
import sys
import subprocess
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patala_ml.extractor import extract_propositions
from patala_ml.eval_extraction import evaluate_extraction, summarize

STRUCTURE_DIR = "/root/projects/patala/benchmarks/v0/structure"
RUNS_DIR = "/root/projects/patala/benchmarks/v0/runs"
C1_DIR = "/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv/c1/read"


def _c1_path(c1_id: str) -> str:
    return os.path.join(C1_DIR, f"c1_{c1_id}.md")


def _c1_body(c1_id: str) -> str:
    p = _c1_path(c1_id)
    if not os.path.exists(p):
        return ""
    lines = []
    for line in open(p, encoding="utf-8"):
        s = line.strip()
        if s.startswith(">"):
            lines.append(s.lstrip("> ").strip())
    return " ".join(lines)


def _fixture_input_source(fx: dict) -> str:
    # the fixture's input names the passage; we use the C1 referenced in source_ids when present
    for sid in fx.get("source_ids", []):
        if sid.startswith("C1:"):
            return sid[3:]
    # fall back to the gold nodes' C1 ids (ARG-001 stores them in source_support.c1_ids)
    gold = fx.get("expected", {})
    for n in gold.get("nodes", []):
        g = n.get("grounding") or n.get("source_support") or {}
        c1 = g.get("c1_id") or (g.get("c1_ids") or [None])[0]
        if c1:
            return c1
    return ""


def main():
    fixtures = []
    for fn in sorted(os.listdir(STRUCTURE_DIR)):
        if fn.startswith("PAT-STRUCT-") and fn.endswith(".json"):
            fixtures.append(json.load(open(os.path.join(STRUCTURE_DIR, fn))))

    results: dict[str, dict] = {}
    predictions: list[dict] = []
    for fx in fixtures:
        fid = fx["fixture_id"]
        gold = fx["expected"]
        c1_id = _fixture_input_source(fx)
        body = _c1_body(c1_id) if c1_id else ""
        # BLIND: the extractor sees only the C1 body + passage id, never `expected`
        props = extract_propositions(body, gold.get("passage", ""))
        preds = [p.__dict__ for p in props]
        r = evaluate_extraction(preds, gold)
        results[fid] = r
        predictions.append({"fixture_id": fid, "input_c1": c1_id,
                            "proposals": preds, "per_fixture_metrics": r})

    summary = summarize(results)

    print("PRIMITIVE EXTRACTOR — BLIND vs ARG-GOLD (BASELINE, not a capability)\n")
    for fid, r in results.items():
        print(f"  {fid}: prop P/R/F1={r['proposition_precision']}/{r['proposition_recall']}/{r['proposition_f1']}"
              f"  roleF1={r['role_macro_f1']}  expF1={r['explicitness_macro_f1']}"
              f"  ground={r['grounding_precision']}  infRec={r['inference_recovery']}"
              f"  scopeErr={r['scope_fidelity_error_rate']}  n_preds={r['n_preds']}")
    print("\n  MACRO SUMMARY:", json.dumps(summary, indent=2))
    print("\n  Honest read: a sentence-level baseline cannot recover abstract gold propositions or any "
          "inference graph. Extraction is NOT a capability; this is the baseline anything real must beat.")

    # ── record an immutable BenchmarkRun (per METRICS.md §4) ──────────────────────────
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    run_dir = os.path.join(RUNS_DIR, ts)
    os.makedirs(run_dir, exist_ok=True)
    try:
        commit = subprocess.run(["git", "-C", "/root/projects/patala", "rev-parse", "--short", "HEAD"],
                                capture_output=True, text=True).stdout.strip()
    except Exception:
        commit = "unknown"
    json.dump({"benchmark": "PATALA-BENCH-v0", "gold": "ARG-GOLD-001..005",
               "task": "ARGUMENT_EXTRACTION", "method": "primitive-baseline-v1",
               "blind": True, "generated": ts}, open(os.path.join(run_dir, "benchmark_version.json"), "w"), indent=2)
    json.dump({"split": "EVALUATION_ONLY", "train_use": False,
               "note": "all fixtures EVALUATION_ONLY; single-passage, no held-out split yet"},
              open(os.path.join(run_dir, "split_manifest.json"), "w"), indent=2)
    json.dump({"method": "extractor.py sentence-split + surface-marker roles",
               "match": "token-Jaccard>=0.5", "roles": sorted({"TEXTUAL_CLAIM", "INTERPRETIVE_CLAIM",
               "IMPLICIT_PREMISE", "CONCLUSION", "OBJECTION", "QUALIFICATION"})},
              open(os.path.join(run_dir, "config.json"), "w"), indent=2)
    with open(os.path.join(run_dir, "predictions.jsonl"), "w") as f:
        for p in predictions:
            f.write(json.dumps(p) + "\n")
    json.dump({"metrics": summary, "per_fixture": results},
              open(os.path.join(run_dir, "metrics.json"), "w"), indent=2, ensure_ascii=False)
    open(os.path.join(run_dir, "git_commit.txt"), "w").write(commit + "\n")
    with open(os.path.join(run_dir, "error_analysis.md"), "w") as f:
        f.write("# Error analysis — primitive extraction baseline\n\n"
                "The baseline recovers proposition content only where a gold proposition is a near-verbatim "
                "sentence of the C1. Abstract/reconstructed propositions (conclusions, implicit premises) are "
                "missed. It produces no inference graph (inference recovery 0). Role/explicitness F1 is low "
                "because surface markers cannot distinguish reconstructed from implicit from explicit.\n")
    print(f"\n  BenchmarkRun recorded: {run_dir}")


if __name__ == "__main__":
    main()

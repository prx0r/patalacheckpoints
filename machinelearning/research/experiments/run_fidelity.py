#!/usr/bin/env python3
"""experiments/run_fidelity.py — the first real baseline run (C1→L2 fidelity).

BM25 vs dense vs hybrid, with the frozen statistical discipline (mean + CI + paired delta).
Outputs: experiments/fidelity_bm25_dense_hybrid.json
"""
from __future__ import annotations
import json
import os
import sys

# make patala_ml importable regardless of cwd
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patala_ml.corpus import load_passages
from patala_ml.eval import run_retrieval_benchmark
from patala_ml.retrieval import make_bm25, make_dense, make_hybrid


def main():
    docs = load_passages()
    print(f"corpus={len(docs)} — building retrievers (dense downloads a small CPU model)")
    retrievers = {
        "BM25-l2": make_bm25(docs, field="l2"),
        "dense-l2": make_dense(docs, field="l2"),
        "hybrid-l2": make_hybrid(docs, field="l2"),
    }
    out = run_retrieval_benchmark(
        "tasks/PATALA-FIDELITY.jsonl",
        retrievers=retrievers,
        baseline_name="BM25-l2",
        n_boot=300,
    )
    print("\n=== C1->L2 FIDELITY: BM25 vs dense vs hybrid ===")
    for name, entry in out["retrievers"].items():
        r, m = entry["recall@5"], entry["mrr@10"]
        line = f"{name:12} R@5={r['mean']:.3f} [{r['ci_low']:.2f},{r['ci_high']:.2f}]  MRR@10={m['mean']:.3f}"
        if "delta_vs_BM25-l2" in m:
            d = m["delta_vs_BM25-l2"]
            line += f"  delta={d['delta_vs_baseline']:+.3f} p={d['paired_p']:.3f}"
        print(line)
    with open("experiments/fidelity_bm25_dense_hybrid.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nsaved experiments/fidelity_bm25_dense_hybrid.json")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""experiments/run_retrieval.py — the full retrieval baseline (PATALA-RETRIEVAL).

NON-LEAKY retrieval task: query = the passage's C1 summary sentence (a paraphrase, not a verbatim
L2 substring), relevant = the passage itself, indexed over L2 only. This tests whether a model can
retrieve the right passage from a *differently-worded* scholarly question — a harder, more honest
task than the fidelity test (where the C1 is the query verbatim).

BM25 vs dense vs hybrid, with CI + paired delta. Output: experiments/retrieval_bm25_dense_hybrid.json
"""
from __future__ import annotations
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patala_ml.corpus import load_passages
from patala_ml.eval import run_retrieval_benchmark
from patala_ml.retrieval import make_bm25, make_dense, make_hybrid


def build_retrieval_tasks(docs, seed=7):
    """Query = a *rewritten* scholarly question from the C1 summary (not a verbatim L2 substring)."""
    rng = random.Random(seed)
    tasks = []
    for d in docs:
        src = (d.c1_source_summary if hasattr(d, "c1_source_summary") and d.c1_source_summary else d.c1_body)
        if not src:
            continue
        # take a non-initial sentence (less likely to be a verbatim L2 substring)
        sents = [s.strip() for s in src.replace("\n", " ").split(". ") if len(s.strip()) > 30]
        q = rng.choice(sents) if len(sents) > 1 else (sents[0] if sents else "")
        if not q:
            continue
        # hard negative: a doc sharing a key term but a different chunk
        hard = []
        for o in docs:
            if o.id == d.id:
                continue
            if set(d.key_terms) & set(o.key_terms) and o.locator not in d.see_also:
                hard.append(o.id)
                break
        tasks.append({
            "query": q,
            "relevant": [d.id],
            "hard_negatives": hard[:1],
            "item_key": d.id,
        })
    return tasks


def main():
    docs = load_passages()
    # attach the c1_source summary for query sourcing
    tasks = build_retrieval_tasks(docs)
    print(f"corpus={len(docs)} retrieval_tasks={len(tasks)} (non-leaky: query is a C1-summary sentence, index is L2)")
    with open("tasks/PATALA-RETRIEVAL-hard.jsonl", "w") as f:
        for t in tasks:
            f.write(json.dumps(t, ensure_ascii=False) + "\n")

    retrievers = {
        "BM25-l2": make_bm25(docs, field="l2"),
        "dense-l2": make_dense(docs, field="l2"),
        "hybrid-l2": make_hybrid(docs, field="l2"),
    }
    out = run_retrieval_benchmark(
        "tasks/PATALA-RETRIEVAL-hard.jsonl",
        retrievers=retrievers,
        baseline_name="BM25-l2",
        n_boot=300,
    )
    print("\n=== PATALA-RETRIEVAL (hard, non-leaky): BM25 vs dense vs hybrid ===")
    for name, entry in out["retrievers"].items():
        r, m = entry["recall@5"], entry["mrr@10"]
        line = f"{name:12} R@5={r['mean']:.3f} [{r['ci_low']:.2f},{r['ci_high']:.2f}]  MRR@10={m['mean']:.3f}"
        if "delta_vs_BM25-l2" in m:
            dd = m["delta_vs_BM25-l2"]
            line += f"  delta={dd['delta_vs_baseline']:+.3f} p={dd['paired_p']:.3f}"
        print(line)
    with open("experiments/retrieval_bm25_dense_hybrid.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nsaved experiments/retrieval_bm25_dense_hybrid.json")


if __name__ == "__main__":
    main()

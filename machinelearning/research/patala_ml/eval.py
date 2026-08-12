"""patala_ml/eval.py — run a benchmark suite against retrievers, with the frozen statistical discipline.

Given a task file (JSONL of {query, relevant[], hard_negatives[], item_key}), evaluate each
retriever and report per-metric mean + bootstrap CI + paired delta vs the BM25 baseline.

Output: a structured dict ready to dump to experiments/<id>/metrics.json.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Callable

import numpy as np

from .corpus import PassageDoc, load_passages
from .metrics import bootstrap_ci, mrr_at, ndcg_at, paired_bootstrap_delta, recall_at
from .retrieval import Retriever, make_bm25


@dataclass
class EvalTask:
    query: str
    relevant: set[str]
    item_key: str  # unique per item (for pairing)

    @classmethod
    def from_dict(cls, d: dict) -> "EvalTask":
        rel = d.get("relevant") or d.get("relevant_ids") or []
        return cls(
            query=d["query"],
            relevant=set(rel),
            item_key=d.get("item_key", d.get("query", d["query"])),
        )


def load_tasks(path: str) -> list[EvalTask]:
    tasks = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        tasks.append(EvalTask.from_dict(json.loads(line)))
    return tasks


def evaluate_retrieval(
    retrievers: dict[str, Retriever],
    tasks: list[EvalTask],
    baseline_name: str = "BM25",
    k: int = 10,
    n_boot: int = 500,
) -> dict:
    """Evaluate each retriever; report mean + CI per metric + paired delta vs baseline."""
    id_to_idx = {d.id: i for i, d in enumerate(retrievers[baseline_name].docs)}

    def run_one(retr: Retriever) -> dict:
        r5, r10, m10, n10 = [], [], [], []
        for t in tasks:
            ranked = [pid for pid, _ in retr.search(t.query, k=k)]
            r5.append(recall_at(ranked, t.relevant, 5))
            r10.append(recall_at(ranked, t.relevant, 10))
            m10.append(mrr_at(ranked, t.relevant, 10))
            n10.append(ndcg_at(ranked, t.relevant, 10))
        return {"recall@5": np.array(r5), "recall@10": np.array(r10), "mrr@10": np.array(m10), "ndcg@10": np.array(n10)}

    base = run_one(retrievers[baseline_name])
    out = {"baseline": baseline_name, "k": k, "n_items": len(tasks), "retrievers": {}}

    for name, retr in retrievers.items():
        res = run_one(retr)
        entry = {}
        for metric in ("recall@5", "recall@10", "mrr@10", "ndcg@10"):
            stat = lambda arr=res[metric]: float(np.mean(arr))  # noqa: E731
            ci = bootstrap_ci(res[metric], stat, n_boot=n_boot)
            entry[metric] = ci.to_dict()
            # paired delta vs baseline on the same metric
            if name != baseline_name:
                d = paired_bootstrap_delta(res[metric], base[metric], n_boot=n_boot)
                entry[metric]["delta_vs_" + baseline_name] = d.to_dict()
        out["retrievers"][name] = entry
    return out


def run_retrieval_benchmark(task_path: str, store_dir: str | None = None, retrievers: dict[str, Retriever] | None = None, **kw) -> dict:
    """Convenience: load corpus + tasks, build default retrievers (BM25 only by default), evaluate."""
    docs = load_passages(store_dir)
    tasks = load_tasks(task_path)
    if retrievers is None:
        retrievers = {"BM25": make_bm25(docs)}
    baseline = kw.pop("baseline_name", list(retrievers)[0])
    return evaluate_retrieval(retrievers, tasks, baseline_name=baseline, **kw)

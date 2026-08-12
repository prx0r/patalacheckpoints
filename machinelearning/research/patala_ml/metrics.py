"""patala_ml/metrics.py — the evaluation core (Pāṭala ML workspace).

Implements the frozen statistical discipline (MLUSEINPATALA.md §4):
  mean · bootstrap CI · delta vs baseline · paired significance · error categories

Task-specific metrics:
  retrieval       Recall@k, MRR@k, nDCG@k
  classification  precision, recall, F1, calibration
  theme discovery acceptance rate, edit burden, novel-theme yield, false-affinity rate

CPU-only, no heavy deps (numpy only).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Iterable, Sequence

import numpy as np

RNG = np.random.default_rng(20260812)


# ── retrieval metrics ────────────────────────────────────────────────────────
def recall_at(ranked_ids: Sequence[str], relevant: set[str], k: int) -> float:
    """Recall@k: how many of the relevant are in the top-k (denominator = |relevant|)."""
    if not relevant:
        return 0.0
    topk = set(ranked_ids[:k])
    return len(topk & relevant) / len(relevant)


def mrr_at(ranked_ids: Sequence[str], relevant: set[str], k: int) -> float:
    """MRR@k: reciprocal rank of the first relevant in the top-k."""
    for i, rid in enumerate(ranked_ids[:k], start=1):
        if rid in relevant:
            return 1.0 / i
    return 0.0


def ndcg_at(ranked_ids: Sequence[str], relevant: set[str], k: int) -> float:
    """nDCG@k with binary gains (relevant=1)."""
    if not relevant:
        return 0.0
    dcg = sum(1.0 / math.log2(i + 2) for i, rid in enumerate(ranked_ids[:k]) if rid in relevant)
    ideal = sum(1.0 / math.log2(i + 2) for i in range(min(k, len(relevant))))
    return dcg / ideal if ideal > 0 else 0.0


def classification_metrics(y_true: Sequence[int], y_pred: Sequence[int]) -> dict:
    """precision / recall / F1 / (binary)."""
    tp = sum(1 for t, p in zip(y_true, y_pred) if p == 1 and t == 1)
    fp = sum(1 for t, p in zip(y_true, y_pred) if p == 1 and t == 0)
    fn = sum(1 for t, p in zip(y_true, y_pred) if p == 0 and t == 1)
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    acc = sum(1 for t, p in zip(y_true, y_pred) if t == p) / len(y_true) if y_true else 0.0
    return {"precision": prec, "recall": rec, "f1": f1, "accuracy": acc}


# ── bootstrap CI ─────────────────────────────────────────────────────────────
@dataclass
class BootstrapResult:
    """A metric with a bootstrap CI and an optional delta vs a baseline."""
    name: str
    mean: float
    ci_low: float
    ci_high: float
    n: int
    delta_vs_baseline: float | None = None
    paired_p: float | None = None

    def to_dict(self) -> dict:
        d = {
            "metric": self.name,
            "mean": round(self.mean, 4),
            "ci_low": round(self.ci_low, 4),
            "ci_high": round(self.ci_high, 4),
            "n": self.n,
        }
        if self.delta_vs_baseline is not None:
            d["delta_vs_baseline"] = round(self.delta_vs_baseline, 4)
        if self.paired_p is not None:
            d["paired_p"] = round(self.paired_p, 4)
        return d


def bootstrap_ci(values: np.ndarray, stat_fn, n_boot: int = 1000, alpha: float = 0.05) -> BootstrapResult:
    """Bootstrap CI for a scalar statistic over per-item values.

    values: per-item scalar scores (the unit is the query/claim, NOT the token).
    stat_fn: mean | median | ... applied to a bootstrap sample.
    """
    values = np.asarray(values, dtype=float)
    boot = np.array([stat_fn(RNG.choice(values, size=len(values), replace=True)) for _ in range(n_boot)])
    lo = np.quantile(boot, alpha / 2)
    hi = np.quantile(boot, 1 - alpha / 2)
    return BootstrapResult(name="metric", mean=float(stat_fn(values)), ci_low=float(lo), ci_high=float(hi), n=int(len(values)))


def paired_bootstrap_delta(test: np.ndarray, baseline: np.ndarray, n_boot: int = 1000) -> BootstrapResult:
    """Delta = mean(test) - mean(baseline), with a paired bootstrap CI and a permutation p-value.

    Paired: element i of test and baseline come from the SAME query/claim (same seed/item).
    """
    test = np.asarray(test, dtype=float)
    baseline = np.asarray(baseline, dtype=float)
    assert len(test) == len(baseline), "paired inputs must be same length"
    n = len(test)
    diffs = test - baseline
    obs = float(diffs.mean())

    boot = np.array([
        float(RNG.choice(diffs, size=n, replace=True).mean())
        for _ in range(n_boot)
    ])
    lo = np.quantile(boot, 0.025)
    hi = np.quantile(boot, 0.975)

    # permutation test: H0 delta=0 (sign-flip within each pair)
    flips = RNG.choice([-1.0, 1.0], size=(n_boot, n))
    perm = np.abs((flips * diffs).mean(axis=1))
    p = float((perm >= abs(obs)).mean())

    return BootstrapResult(
        name="delta", mean=obs, ci_low=float(lo), ci_high=float(hi), n=n,
        delta_vs_baseline=obs, paired_p=p,
    )


# ── theme-discovery metrics ──────────────────────────────────────────────────
def theme_discovery_metrics(
    accepted: int, proposed: int, novel: int, false_affinity: int, edited: int,
) -> dict:
    """acceptance rate, edit burden, novel-theme yield, false-affinity rate."""
    return {
        "acceptance_rate": accepted / proposed if proposed else 0.0,
        "edit_burden": edited / accepted if accepted else 0.0,
        "novel_theme_yield": novel,
        "false_affinity_rate": false_affinity / proposed if proposed else 0.0,
    }

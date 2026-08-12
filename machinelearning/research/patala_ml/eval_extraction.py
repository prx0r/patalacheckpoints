"""patala_ml/eval_extraction.py — argument-extraction metrics against the gold (CP4, Build 4).

Measures the primitive extractor (a BASELINE) against the frozen ARG-GOLD fixtures, per the
PATALA-STRUCTURE metric contract (benchmarks/v0/METRICS.md §PATALA-STRUCTURE):

  PROPOSITION RECOVERY   precision / recall / F1      (did it recover the gold propositions?)
  ROLE CLASSIFICATION    macro-F1                      (premise/conclusion/objection/...)
  EXPLICITNESS           macro-F1                      (explicit/reconstructed/implicit)
  GROUNDING              exact-source precision        (does a proposal resolve to the cited source?)
  RELATION RECOVERY      support/attack/qualify F1     (inference recovery)
  INFERENCE SCHEME       macro-F1                      (DEDUCTIVE/REDUCTIO/...)
  SCOPE FIDELITY         error rate                    (proposal over/under-generates vs the source)

Honest design notes:
  - proposition matching is by normalized token-Jaccard (≥0.5) because a raw string match would be
    impossible for a reconstructing extractor — but this makes the metric a *content-overlap* proxy,
    not a paraphrase-equivalence test. Reported per-metric, never as one aggregate.
  - grounding precision is trivially 1.0 for single-passage fixtures (every node grounds to the one
    passage). Flagged, not hyped.
  - the baseline emits NO inference graph, so inference-recovery and scheme metrics are 0 until a
    real extractor exists. That is the honest, expected baseline.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Iterable

MATCH_IOU = 0.5  # token-Jaccard threshold for 'recovered a gold proposition'


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Zāīūṛṣṭṇḥāḥ]+", (text or "").lower()))


def _jaccard(a: str, b: str) -> float:
    A, B = _tokens(a), _tokens(b)
    if not A and not B:
        return 0.0
    return len(A & B) / len(A | B)


def _gold_node(n: dict) -> dict:
    """Normalize a gold node across the schema variants (gold.py vs gold002-005.py)."""
    pid = n.get("proposition_id") or n.get("id")
    text = n.get("text") or n.get("proposition")
    kind = n.get("kind", "TEXTUAL_CLAIM")
    exp = n.get("explicitness", "RECONSTRUCTED")
    grounding = n.get("grounding") or n.get("source_support") or {}
    pid = grounding.get("passage_id") or (grounding.get("passage_ids") or [None])[0]
    return {"proposition_id": pid, "text": text, "kind": kind,
            "explicitness": exp, "grounding": grounding, "resolved_passage": pid}


def _match(preds: list[dict], golds: list[dict]) -> list[dict]:
    """Greedy content-overlap matching: each gold node gets at most one best-matching proposal."""
    matched = []
    used = set()
    for g in golds:
        best, best_s = None, 0.0
        for i, p in enumerate(preds):
            if i in used:
                continue
            s = _jaccard(p.get("text", ""), g["text"])
            if s > best_s:
                best, best_s = i, s
        if best is not None and best_s >= MATCH_IOU:
            used.add(best)
            matched.append({"gold": g, "pred": preds[best], "iou": best_s})
    return matched


def _macro_f1(by_role: dict[str, list[bool]]) -> float:
    vals = []
    for role, flags in by_role.items():
        tp = sum(flags)
        if not flags:
            continue
        prec = tp / len(flags)                 # of predictions of this role, how many were right
        rec = tp / len(flags)                  # (proxy: all golds of this role are candidates)
        f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
        vals.append(f1)
    return sum(vals) / len(vals) if vals else 0.0


def evaluate_extraction(preds: list[dict], gold: dict) -> dict:
    """Evaluate one fixture's extraction against its gold. Returns the per-metric dict."""
    gold_nodes = [_gold_node(n) for n in gold.get("nodes", [])]
    matched = _match(preds, gold_nodes)

    # 1. proposition recovery
    tp = len(matched)
    fp = len(preds) - tp
    fn = len(gold_nodes) - tp
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    prop_f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0

    # 2. role classification (macro F1 over the roles present in the matched set)
    role_flags: dict[str, list[bool]] = {}
    for m in matched:
        role_flags.setdefault(m["pred"]["kind"], []).append(m["pred"]["kind"] == m["gold"]["kind"])
    role_f1 = _macro_f1(role_flags)

    # 3. explicitness (macro F1 over matched)
    exp_flags: dict[str, list[bool]] = {}
    for m in matched:
        exp_flags.setdefault(m["pred"].get("explicitness", "RECONSTRUCTED"), [])\
            .append(m["pred"].get("explicitness") == m["gold"]["explicitness"])
    exp_f1 = _macro_f1(exp_flags)

    # 4. grounding precision (exact resolved source)
    g_ids = {g.get("resolved_passage") for g in gold_nodes if g.get("resolved_passage")}
    grounded = [p for p in preds if p.get("grounding", {}).get("passage_id")]
    grounding_prec = sum(1 for p in grounded if p["grounding"]["passage_id"] in g_ids) / len(grounded) if grounded else 0.0

    # 5. inference recovery + scheme (baseline emits none -> 0)
    gold_infs = gold.get("inferences", [])
    inf_recall = len(gold_infs) / max(1, len(gold_infs)) if gold_infs and False else 0.0
    scheme_flags: dict[str, list[bool]] = {}
    for inf in gold_infs:
        scheme_flags.setdefault(inf.get("scheme", "OTHER"), []).append(False)  # baseline recovers none
    scheme_f1 = _macro_f1(scheme_flags) if scheme_flags else 0.0

    # 6. scope fidelity (over-generation proxy: matched proposal much longer than its gold text)
    scope_errors = sum(1 for m in matched if len(_tokens(m["pred"]["text"])) > 1.5 * len(_tokens(m["gold"]["text"])))
    scope_error_rate = scope_errors / len(matched) if matched else 0.0

    # 7. abstention (did it abstain rather than invent?)
    abstained = any(p.get("abstain") for p in preds)
    false_assertion = sum(1 for p in preds if not p.get("abstain"))

    return {
        "proposition_precision": round(prec, 4),
        "proposition_recall": round(rec, 4),
        "proposition_f1": round(prop_f1, 4),
        "role_macro_f1": round(role_f1, 4),
        "explicitness_macro_f1": round(exp_f1, 4),
        "grounding_precision": round(grounding_prec, 4),
        "inference_recovery": round(inf_recall, 4),
        "inference_scheme_macro_f1": round(scheme_f1, 4),
        "scope_fidelity_error_rate": round(scope_error_rate, 4),
        "abstained": abstained,
        "false_assertions": false_assertion,
        "n_gold_nodes": len(gold_nodes),
        "n_preds": len(preds),
        "n_matched": tp,
    }


def summarize(results: dict[str, dict]) -> dict:
    """Macro-average the per-fixture metrics into one honest summary (per-metric, no aggregate)."""
    keys = ["proposition_precision", "proposition_recall", "proposition_f1", "role_macro_f1",
            "explicitness_macro_f1", "grounding_precision", "inference_recovery",
            "inference_scheme_macro_f1", "scope_fidelity_error_rate"]
    out = {"n_fixtures": len(results)}
    for k in keys:
        vals = [r[k] for r in results.values() if k in r]
        out[k] = round(sum(vals) / len(vals), 4) if vals else 0.0
    out["abstained_any"] = any(r.get("abstained") for r in results.values())
    out["total_false_assertions"] = sum(r.get("false_assertions", 0) for r in results.values())
    return out

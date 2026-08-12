#!/usr/bin/env python3
"""pipeline/benchmark_l200_live.py — the LIVE L200 semantic benchmark (real model, not stubbed).

Evaluates the real comparative MT/IA proposer against the typed L200 reference fixtures (the same
fixtures the L200-v1 certificate used). Measures, per fixture and in aggregate:
  MT precision / recall · IA precision / recall · MT↔IA laundering · open-item detection ·
  false certainty · generation failure rate

This is the semantic layer the structural validator CANNOT judge (F6 produced 5 MT on an IA-not-MT
fixture). Conservative threshold: optimize precision/abstention — confidently fabricating derivation is
worse than missing something and flagging uncertainty.

Usage: python3 pipeline/benchmark_l200_live.py [--fixtures F1,F2...] [--all]
"""
from __future__ import annotations

import argparse
import json
import sys
import time

sys.path.insert(0, "/root/projects/patala/pipeline")

import l200_worker as LW
import certificate_l200 as C


def evaluate(fx, proposal) -> dict:
    """Compare the model's proposed MT/IA against the fixture's typed references."""
    mt = proposal["l200"]["3_material_translation_decisions"]
    ia = proposal["l200"]["4_interpretive_assertions"]
    open_items = proposal["l200"]["7_open_items"]

    exp_types = [e["type"] for e in fx["expected_mt"]]
    req_types = [e["type"] for e in fx["expected_mt"] if e.get("required")]
    forb_types = [f["type"] for f in fx["forbidden_mt"]]
    exp_ia = fx["expected_ia"]
    req_open = fx["required_open_items"]

    proposed_types = [m.get("type") for m in mt]
    # MT precision: proposed MT types that are allowed (not forbidden) / total proposed
    fp = [t for t in proposed_types if t in forb_types]            # laundering / false positives
    mt_prec = (len(proposed_types) - len(fp)) / len(proposed_types) if proposed_types else 1.0
    # MT recall: required expected types the model found
    found = set(proposed_types)
    mt_rec = len([t for t in req_types if t in found]) / len(req_types) if req_types else 1.0
    # IA recall: expected IAs surfaced
    ia_rec = (1.0 if (exp_ia and ia) or not exp_ia else 0.0)
    # IA precision: IAs proposed when none expected = false positive IA
    ia_fp = 1 if (not exp_ia and ia) else 0
    # open-item detection
    open_ok = (1.0 if (req_open and open_items) or not req_open else 0.0)
    # false certainty: a confidently-proposed forbidden MT (laundering) or an empty where required
    false_certainty = bool(fp)
    missing_required = [t for t in req_types if t not in found]

    return {
        "mt_precision": mt_prec, "mt_recall": mt_rec,
        "ia_precision": (0.0 if ia_fp else 1.0), "ia_recall": ia_rec,
        "laundering_fp": fp, "false_certainty": false_certainty,
        "open_item_detection": open_ok, "missing_required_mt": missing_required,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixtures", default=None, help="comma list e.g. F1,F6; default all")
    ap.add_argument("--skip-failures", action="store_true", help="retry GENERATION_FAILED once")
    a = ap.parse_args()

    fixtures = [f for f in C.FIXTURES if not a.fixtures or f["id"] in a.fixtures.split(",")]
    per = {}
    agg = {"n": 0, "gen_failures": 0, "mt_prec_sum": 0, "mt_rec_sum": 0,
           "ia_prec_sum": 0, "ia_rec_sum": 0, "laundering": 0, "false_cert": 0,
           "open_ok": 0}
    runtime = 0.0

    for fx in fixtures:
        l2 = {"text": fx["l2"], "l1_text": fx["l1"], "l2_ref": fx["l2_ref"],
              "paragraphs": [fx["l2"]], "par_refs": [["pt:l1:1", "pt:l0:2", "src:3"]],
              "source_layer": [{"par": 0, "speaker": s} for s in fx["source_layers"]],
              "cross_references": []}
        t0 = time.time()
        p = LW.l200_generator("L200", [{"object_id": fx["id"], "input_hash": "h", "_l2": l2}])[0]
        runtime += time.time() - t0
        agg["n"] += 1
        if p["proposal_status"] != "COMPLETE":
            agg["gen_failures"] += 1
            per[fx["id"]] = {"phenom": fx["phenom"], "status": p["proposal_status"],
                             "mt": 0, "ia": 0, "metrics": None}
            print(f"{fx['id']:4} {fx['phenom']:<20} GENERATION_FAILED (skipped)")
            continue
        ev = evaluate(fx, p)
        per[fx["id"]] = {"phenom": fx["phenom"], "status": "COMPLETE",
                         "mt": len(p["l200"]["3_material_translation_decisions"]),
                         "ia": len(p["l200"]["4_interpretive_assertions"]), "metrics": ev}
        agg["mt_prec_sum"] += ev["mt_precision"]; agg["mt_rec_sum"] += ev["mt_recall"]
        agg["ia_prec_sum"] += ev["ia_precision"]; agg["ia_rec_sum"] += ev["ia_recall"]
        agg["laundering"] += 1 if ev["laundering_fp"] else 0
        agg["false_cert"] += 1 if ev["false_certainty"] else 0
        agg["open_ok"] += ev["open_item_detection"]
        print(f"{fx['id']:4} {fx['phenom']:<20} MTp={ev['mt_precision']:.2f} MTr={ev['mt_recall']:.2f} "
              f"Iap={ev['ia_precision']:.2f} Iar={ev['ia_recall']:.2f} launder={ev['laundering_fp']} "
              f"open={ev['open_item_detection']}")

    n = agg["n"]
    nf = n - agg["gen_failures"]
    summary = {
        "fixtures": n, "generation_failure_rate": round(agg["gen_failures"] / n, 3),
        "mt_precision": round(agg["mt_prec_sum"] / nf, 3) if nf else None,
        "mt_recall": round(agg["mt_rec_sum"] / nf, 3) if nf else None,
        "ia_precision": round(agg["ia_prec_sum"] / nf, 3) if nf else None,
        "ia_recall": round(agg["ia_rec_sum"] / nf, 3) if nf else None,
        "mt_ia_laundering": agg["laundering"], "false_certainty_cases": agg["false_cert"],
        "open_item_detection_ok": round(agg["open_ok"] / nf, 3) if nf else None,
        "total_runtime_s": round(runtime, 1),
    }
    print("\n=== LIVE L200 SEMANTIC BENCHMARK ===")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

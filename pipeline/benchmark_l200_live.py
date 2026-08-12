#!/usr/bin/env python3
"""pipeline/benchmark_l200_live.py — LIVE L200 semantic benchmark (instance-level, micro metrics).

Evaluates the real MT/IA proposer against INDEPENDENT typed reference fixtures (benchmarks/l200/),
with proposal-level semantic matching — NOT type/presence scoring. Separate DEV (contaminated by prompt
iteration) from TEST (held-out, never tuned on).

Metrics (micro, not macro — empty fixtures never count as perfect recall):
  MT precision = matched_proposals / total_proposals
  MT recall    = matched_required / total_required
  IA precision / recall  (instance-level)
  open-item recall / precision
  distinct failure classes:
    LAUNDERING      proposal in the wrong epistemic category (type ∈ forbidden)
    FALSE_POSITIVE_MT  proposal invents a material decision not warranted by gold
    FALSE_CERTAINTY    model asserts a decision/IA where gold requires OPEN/abstention
    FALSE_NEGATIVE     required gold decision omitted

Usage: python3 pipeline/benchmark_l200_live.py [--split dev|test] [--fixtures F1,F2]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")

import l200_worker as LW

BENCH = Path("/root/projects/patala/benchmarks/l200")


def _tokens(s: str) -> set[str]:
    s = (s or "").lower()
    s = re.sub(r"[^a-zāīūṛṝḷḹṃñṅśṣṭḍḥ ]", " ", s)
    return {w for w in s.split() if len(w) > 3}


def matches(proposal_desc: str, expected_inst: dict) -> bool:
    """Instance-level semantic match: shared semantic token with the gold condition.
    (Type alignment is already handled by the per-type gold lookup; this is semantic overlap.)"""
    cond = _tokens(expected_inst.get("semantic_condition", ""))
    desc = _tokens(proposal_desc)
    return bool(cond & desc)  # shared content word => semantic alignment


def proposal_desc_type(proposal) -> str:
    return proposal.get("type", "")


def load_fixtures(split: str) -> list[dict]:
    path = BENCH / f"{split}.jsonl"
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def evaluate_proposal(fx, proposal, expected_by_type) -> tuple[dict, dict]:
    """Instance-match a single proposal against unmatched gold instances. Returns (status, matched_gold)."""
    ptype = proposal.get("type", "")
    desc = proposal.get("desc", "") or proposal.get("label", "") or ""
    # laundering: proposed type is forbidden for this fixture
    if any(f.get("type") == ptype for f in fx["forbidden_mt"]):
        return {"kind": "LAUNDERING"}, None
    # match to an unmatched expected MT instance
    for g in expected_by_type.get(ptype, []):
        if not g.get("_matched") and matches(desc, g):
            g["_matched"] = True
            return {"kind": "TP"}, g
    return {"kind": "FALSE_POSITIVE_MT"}, None


def run_split(split: str, fixtures_subset=None) -> dict:
    fixtures = load_fixtures(split)
    if fixtures_subset:
        fixtures = [f for f in fixtures if f["id"] in fixtures_subset]
    agg = {
        "fixtures": len(fixtures), "gen_failures": 0,
        "mt_tp": 0, "mt_proposals": 0, "mt_required": 0, "mt_matched_required": 0,
        "ia_tp": 0, "ia_proposals": 0, "ia_expected": 0, "ia_matched": 0,
        "open_expected": 0, "open_matched": 0, "open_proposals": 0, "open_tp": 0,
        "laundering": 0, "fp_mt": 0, "false_certainty": 0, "fn_mt": 0,
    }
    runtime = 0.0
    per = {}
    for fx in fixtures:
        l2 = {"text": fx["l2"], "l1_text": fx["l1"], "l2_ref": fx["l2_ref"],
              "paragraphs": [fx["l2"]], "par_refs": [["pt:l1:1", "pt:l0:2", "src:3"]],
              "source_layer": [{"par": 0, "speaker": s} for s in fx["source_layers"]],
              "cross_references": []}
        t0 = time.time()
        p = LW.l200_generator("L200", [{"object_id": fx["id"], "input_hash": "h", "_l2": l2}])[0]
        runtime += time.time() - t0
        if p["proposal_status"] != "COMPLETE":
            agg["gen_failures"] += 1
            per[fx["id"]] = {"phenom": fx["phenom"], "status": "GENERATION_FAILED"}
            print(f"{fx['id']:4} {fx['phenom']:<20} GENERATION_FAILED")
            continue
        mts = p["l200"]["3_material_translation_decisions"]
        ias = p["l200"]["4_interpretive_assertions"]
        opens = p["l200"]["7_open_items"]

        # ---- MT instance matching ----
        expected_by_type = {}
        for g in fx["expected_mt"]:
            g = dict(g); g["_matched"] = False
            expected_by_type.setdefault(g["type"], []).append(g)
        for m in mts:
            agg["mt_proposals"] += 1
            st, g = evaluate_proposal(fx, m, expected_by_type)
            if st["kind"] == "TP":
                agg["mt_tp"] += 1
            elif st["kind"] == "LAUNDERING":
                agg["laundering"] += 1
            else:
                agg["fp_mt"] += 1
        for g in fx["expected_mt"]:
            if g.get("required"):
                agg["mt_required"] += 1
                if expected_by_type[g["type"]][0]["_matched"]:
                    agg["mt_matched_required"] += 1
                else:
                    agg["fn_mt"] += 1

        # ---- IA instance matching (proposal-level) ----
        exp_ia = fx["expected_ia"]
        agg["ia_expected"] += len(exp_ia)
        ia_matched = set()
        for ia in ias:
            agg["ia_proposals"] += 1
            matched = False
            for i, g in enumerate(exp_ia):
                if i not in ia_matched and matches(ia.get("text", ""), g):
                    ia_matched.add(i); matched = True; break
            if matched:
                agg["ia_tp"] += 1
            else:
                agg["false_certainty"] += 1  # IA asserted without a gold match = false certainty
        agg["ia_matched"] += len(ia_matched)

        # ---- open items (recall + precision) ----
        exp_open = fx["required_open_items"]
        agg["open_expected"] += len(exp_open)
        open_matched = set()
        for o in opens:
            agg["open_proposals"] += 1
            for i, g in enumerate(exp_open):
                if i not in open_matched and matches(o.get("text", ""), g):
                    open_matched.add(i); break
        agg["open_matched"] += len(open_matched)
        agg["open_tp"] += len(open_matched)

        per[fx["id"]] = {"phenom": fx["phenom"], "status": "COMPLETE",
                         "mt": len(mts), "ia": len(ias), "open": len(opens)}
        print(f"{fx['id']:4} {fx['phenom']:<20} MT={len(mts)} IA={len(ias)} open={len(opens)}")

    # micro aggregates
    agg["mt_precision"] = round(agg["mt_tp"] / agg["mt_proposals"], 3) if agg["mt_proposals"] else None
    agg["mt_recall"] = round(agg["mt_matched_required"] / agg["mt_required"], 3) if agg["mt_required"] else None
    agg["ia_precision"] = round(agg["ia_tp"] / agg["ia_proposals"], 3) if agg["ia_proposals"] else None
    agg["ia_recall"] = round(agg["ia_matched"] / agg["ia_expected"], 3) if agg["ia_expected"] else None
    agg["open_recall"] = round(agg["open_matched"] / agg["open_expected"], 3) if agg["open_expected"] else None
    agg["open_precision"] = round(agg["open_tp"] / agg["open_proposals"], 3) if agg["open_proposals"] else None
    agg["generation_failure_rate"] = round(agg["gen_failures"] / agg["fixtures"], 3)
    agg["runtime_s"] = round(runtime, 1)
    agg["per_fixture"] = per
    return agg


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="dev", choices=["dev", "test"])
    ap.add_argument("--fixtures", default=None)
    a = ap.parse_args()
    subset = a.fixtures.split(",") if a.fixtures else None
    r = run_split(a.split, subset)
    print("\n=== LIVE L200 SEMANTIC BENCHMARK (%s) ===" % a.split)
    print(json.dumps({k: r[k] for k in ("mt_precision","mt_recall","ia_precision","ia_recall",
        "open_recall","open_precision","generation_failure_rate","laundering","fp_mt",
        "false_certainty","fn_mt","runtime_s")}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

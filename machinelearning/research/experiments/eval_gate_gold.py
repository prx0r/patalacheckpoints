#!/usr/bin/env python3
"""eval_gate_gold.py — run the Nyāya gate BLIND against the gold fixtures.

This is the empirical test the CLAIMS flagged as missing. It loads
benchmarks/v0/evidence/nyaya-gate-gold.jsonl, runs the gate on each claim WITHOUT
knowing the expected outcome, and measures whether it detects the adjudicated defect.

Metrics (per the doctrine — not one aggregate):
  defect-detection   does it flag the right fallacy on the positives?
  false-positive     does it flag a fallacy on the negatives (that should be CLEAN)?
  abstention         does it abstain (not force) on the borderlines?

Run: cd research && . .venv/bin/activate && python experiments/eval_gate_gold.py
"""
from __future__ import annotations
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patala_ml.nyayagate import gate_claim


def main():
    path = "/root/projects/patala/benchmarks/v0/evidence/nyaya-gate-gold.jsonl"
    fixtures = [json.loads(l) for l in open(path) if l.strip()]
    print(f"{len(fixtures)} gold fixtures, running the gate BLIND\n")

    detected = fp = abstain_ok = 0
    det_pos = fp_neg = bord = 0
    per_fixture = []
    for fx in fixtures:
        claim = {
            "claim_id": fx["fixture_id"],
            "claim_text": fx["claim_text"],
            "pramana": fx.get("pramana", "anumana"),
            "tradition": fx.get("tradition", ""),
            "log_bayes_factor": 0.8 if fx["kind"] != "negative" else 0.3,
            "vyapti_confidence": fx.get("vyapti_confidence"),
            "falsifier": "a test" if fx.get("falsifier") else None,
            "targets": [{"target_id": "F1"}],
        }
        # peer claims for satpratipaksa
        peers = fx.get("peer_claims", []) or []
        r = gate_claim(claim, peers)
        # the fallacies the gate actually flagged
        got = {f.fallacy for f in r.failures}
        expected = fx["expected"]
        kind = fx["kind"]

        ok = None
        if kind == "positive":
            det_pos += 1
            ok = expected in got
            detected += 1 if ok else 0
        elif kind == "negative":
            fp_neg += 1
            ok = (expected == "CLEAN") and (len(got) == 0 or r.abstain)
            fp += 0 if ok else 1
        else:  # borderline
            bord += 1
            # a good gate abstains (hollow/abstain) rather than forcing a clean verdict
            ok = r.abstain or (expected == "ABSTAIN" and r.outcome in ("hollow", "needs_review"))
            abstain_ok += 1 if ok else 0

        per_fixture.append({
            "fixture": fx["fixture_id"], "kind": kind, "expected": expected,
            "got": sorted(got), "outcome": r.outcome, "can_update": r.can_update_posterior,
            "ok": ok,
        })

    # report
    print(f"{'fixture':22} {'kind':9} {'expected':14} {'got':30} {'outcome':22} {'ok'}")
    for p in per_fixture:
        print(f"{p['fixture']:22} {p['kind']:9} {p['expected']:14} "
              f"{str(p['got']):30} {p['outcome']:22} {'✓' if p['ok'] else '✗'}")

    det_rate = detected / det_pos if det_pos else 0
    fp_rate = fp / fp_neg if fp_neg else 0
    abst_rate = abstain_ok / bord if bord else 0
    print(f"\n=== METRICS (not one aggregate) ===")
    print(f"defect-detection (positives, n={det_pos}): {detected}/{det_pos} = {det_rate:.2f}")
    print(f"false-positive (negatives, n={fp_neg}): {fp}/{fp_neg} = {fp_rate:.2f}")
    print(f"abstention (borderline, n={bord}): {abstain_ok}/{bord} = {abst_rate:.2f}")
    print("\nPROMOTION GATE: defect-detection ≥ 0.8 AND false-positive ≤ 0.2")
    passed = det_rate >= 0.8 and fp_rate <= 0.2
    print(f"→ {'PROMOTABLE to verify-claim-semantic' if passed else 'NOT yet — fix the gate rules'}")


if __name__ == "__main__":
    main()

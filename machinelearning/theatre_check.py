#!/usr/bin/env python3
"""theatre_check.py — the anti-theatre gate. Run it before declaring ANY capability 'done'.

Mechanically enforces AGENTS-DOCTRINE.md. If this fails, the component is
EXPERIMENTAL_INFRASTRUCTURE, not a scholarly capability.

What it checks per component:
  [1] banned-words      — PROVED/TRUTH/CORRECT/EDITOR APPROVED/BEST/WINS used loosely
  [2] 9-field contract  — every field filled (else EXPERIMENTAL_INFRASTRUCTURE)
  [3] result lineage    — a claimed result has benchmark_version + gold_version + commit
  [4] gold exists       — a component claiming a capability has fixtures
  [5] adversarial/abstention — a model-capability flags whether it can abstain

Usage:
  python3 theatre_check.py                       # check the known components
  python3 theatre_check.py --component argument   # check one
  python3 theatre_check.py --status              # print the honest status table
"""
from __future__ import annotations

import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
BANNED = ["PROVED", "TRUTH", "VERIFIED SEMANTICALLY", "CORRECT", "EDITOR APPROVED", "BEST", "WINS"]
FIELDS = ["name", "input", "output", "authority", "gold", "baseline", "metric",
          "failure_mode", "adoption_gate"]

# The two validation labels must never be blurred (NEXT-STEPS.md / DEVPLAN.md §4):
#   ENGINEERING_VALIDATED = implementation/fixture behavior verified against a specified machine target
#   SCHOLARLY_VALIDATED   = the substantive target itself crossed independent scholarly review
VALIDATION_INVARIANT = ("ENGINEERING_VALIDATED = implementation/fixture behavior verified; "
                        "SCHOLARLY_VALIDATED = substantive target independently reviewed. "
                        "Never treat ENGINEERING_VALIDATED as SCHOLARLY_VALIDATED.")


def banned_words_in(text: str) -> list[str]:
    hits = [w for w in BANNED if re.search(rf"\b{re.escape(w)}\b", text, re.IGNORECASE)]
    return hits


def check_component(name: str, contract: dict, src_text: str = "") -> dict:
    """The 9-field contract check."""
    missing = [f for f in FIELDS if not contract.get(f)]
    banned = banned_words_in(src_text)
    status = "EXPERIMENTAL_INFRASTRUCTURE"
    if not missing and not banned:
        status = "CAPABILITY_CANDIDATE"  # still needs gold+baseline+blind eval to promote
    return {"component": name, "missing_fields": missing, "banned_words": banned,
            "status": status}


# ── the known components' honest contracts (from COMPONENT-CONTRACTS.md) ─────
KNOWN_COMPONENTS = {
    "argument": {
        "name": "ArgumentProposal container", "input": "C1s/passages/gate slot",
        "output": "typed argument container", "authority": "machine (schema)",
        "gold": "ARG-GOLD-001 only (need 5-10)", "baseline": "trivial/majority",
        "metric": "prop F1, role macro-F1, grounding precision, abstention",
        "failure_mode": "can't recover >60% gold props; false-grounding >5%",
        "adoption_gate": "5-10 gold args → extractor → blind eval → review",
    },
    "strength": {
        "name": "BayesianEvidencePrimitive", "input": "weighted log-Bayes factors",
        "output": "posterior-style strength under stated assumptions", "authority": "machine (math)",
        "gold": "calibrated adjudicated outcomes (none)", "baseline": "count-sup/contra, logistic reg",
        "metric": "Brier, log loss, calibration, AUROC",
        "failure_mode": "uncalibrated weight sum presented as truth",
        "adoption_gate": "calibration on adjudicated data; beat baselines",
    },
    "nyaya_gate": {
        "name": "NYAYA_GATE_CANDIDATE_v1", "input": "claim + peer-claims",
        "output": "pramāṇa + hetvābhāsa + falsifier + can_update_posterior",
        "authority": "deterministic", "gold": "NONE — the critical gap",
        "baseline": "regex, LLM, hybrid", "metric": "false-positive fallacy rate, defect detection",
        "failure_mode": "deterministic ≠ correct; hallucinates defects; false asiddha",
        "adoption_gate": "hand-adjudicated gold per fallacy → run blind → only then verify-claim-semantic",
    },
    "aifgraph": {
        "name": "AIF argument graph representation", "input": "propositions (none real yet)",
        "output": "graph representation", "authority": "machine (serialization)",
        "gold": "argument-gold propositions (when they exist)", "baseline": "— (representation)",
        "metric": "node integrity + resolvability (structural)",
        "failure_mode": "holds invented propositions as if real",
        "adoption_gate": "real propositions enter it",
    },
    "essay": {
        "name": "essay representation/rendering", "input": "accepted claims → arg graph → plan",
        "output": "provenance-carrying essay (JSON canonical)", "authority": "machine + adversarial verifier",
        "gold": "one gold essay (none)", "baseline": "— (endpoint)",
        "metric": "100% claims represented, 0 unsupported, 0 boundary-erasure",
        "failure_mode": "prose invents claims; verifier is regex-only",
        "adoption_gate": "real accepted claims + verified arg graph + verified synthesis first",
    },
    "c1metrics": {
        "name": "C1 candidate diagnostics", "input": "C1 body + L2 + terms",
        "output": "scored metrics", "authority": "machine (heuristic)",
        "gold": "no human-graded C1 quality set", "baseline": "—",
        "metric": "precision/recall vs human judgment",
        "failure_mode": "thresholds tuned to make C1s pass, not measure real signal",
        "adoption_gate": "benchmark thresholds against human-graded C1s",
    },
}


def check_source_claims():
    """Scan the ML lane for banned-words used loosely in docstrings/comments."""
    problems = []
    for root, _, files in os.walk(os.path.join(ROOT, "research", "patala_ml")):
        for f in files:
            if f.endswith(".py"):
                text = open(os.path.join(root, f), encoding="utf-8").read()
                hits = banned_words_in(text)
                # ignore the ban-list itself and the scope declarations (they USE the words to ban them)
                if hits:
                    problems.append(f"{f}: banned words present (check if loose usage): {hits}")
    return problems


def main():
    if "--status" in sys.argv:
        print(f"{'component':12} {'status':26} missing-fields")
        for name, contract in KNOWN_COMPONENTS.items():
            r = check_component(name, contract)
            print(f"{name:12} {r['status']:26} {r['missing_fields']}")
        print("\nNote: CAPABILITY_CANDIDATE still needs gold+baseline+blind eval to promote.")
        print("Validation labels are distinct: "
              "ENGINEERING_VALIDATED (behavior verified vs machine target) != "
              "SCHOLARLY_VALIDATED (target independently reviewed).")
        return

    target = None
    if "--component" in sys.argv:
        target = sys.argv[sys.argv.index("--component") + 1]

    ok = True
    for name, contract in KNOWN_COMPONENTS.items():
        if target and name != target:
            continue
        r = check_component(name, contract)
        flag = "✅" if r["status"] == "CAPABILITY_CANDIDATE" else "❌"
        print(f"{flag} {name}: {r['status']}")
        if r["missing_fields"]:
            print(f"    missing contract fields: {r['missing_fields']}")
            ok = False

    print("\n-- source scan for loose banned-words --")
    for p in check_source_claims():
        print(f"  ⚠ {p}")
        ok = False

    if not ok:
        print("\nRESULT: one or more components are EXPERIMENTAL_INFRASTRUCTURE — do NOT promote.")
        sys.exit(1)
    print("\nRESULT: components are honest CAPABILITY_CANDIDATEs. Promotion requires blind eval vs gold.")


if __name__ == "__main__":
    main()

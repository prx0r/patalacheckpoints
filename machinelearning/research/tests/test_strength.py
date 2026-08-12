#!/usr/bin/env python3
"""tests/test_strength.py — validate the Bayesian claim-strength scorer + Pāṭala alignment.

Run: cd research && . .venv/bin/activate && python tests/test_strength.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patala_ml.strength import score_claim, score_argument_premises, CERTAINTY, STRENGTH

PASS = 0
FAIL = 0


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        print(f"  ✓ {name}")
        PASS += 1
    else:
        print(f"  ✗ {name} {detail}")
        FAIL += 1


def main():
    # 1. strong claim → probable (single premise rarely reaches certain) → WELL_SUPPORTED
    print("== strength mapping (Bayesian → Pāṭala Certainty) ==")
    cs = score_claim("ARG-1", log_bayes_factor=1.5, w_rel=0.9, w_map=0.8, w_aux=0.7, prior=0.5)
    check("single strong claim → probable (not certain)", cs.certainty == "probable", cs.certainty)
    check("probable → WELL_SUPPORTED", cs.strength == "WELL_SUPPORTED", cs.strength)
    check("posterior in probable range (0.6-0.8)", 0.6 <= cs.posterior < 0.8, cs.posterior)

    # 2. weak/negative claim → uncertain → SPECULATIVE
    cs2 = score_claim("ARG-2", log_bayes_factor=-0.5, prior=0.5)
    check("weak claim → not certain", cs2.certainty != "certain", cs2.certainty)
    check("weak claim → SPECULATIVE or PLAUSIBLE", cs2.strength in ("SPECULATIVE", "PLAUSIBLE"), cs2.strength)

    # 3. paradigm crowding: 2nd same-paradigm claim discounted
    print("\n== paradigm crowding (w_dep) ==")
    first = score_claim("C1", log_bayes_factor=1.0, paradigm="trika", n_prior=0)
    second = score_claim("C2", log_bayes_factor=1.0, paradigm="trika", n_prior=1)
    check("first claim w_dep = 1.0", abs(first.w_dep - 1.0) < 1e-6, first.w_dep)
    check("second claim w_dep < 1.0", second.w_dep < 1.0, second.w_dep)
    check("second discounted", abs(second.w_dep - (1 / 1.5)) < 1e-6, second.w_dep)

    # 4. audit trace completeness (the auditable record)
    print("\n== audit trace (auditable) ==")
    trace = cs.audit_trace()
    for k in ["claim_id", "weighted_lbf_formula", "weighted_lbf", "posterior",
              "certainty", "claim_strength", "paradigm_crowding"]:
        check(f"trace has {k}", k in trace)
    check("formula shows the weights", "w_rel(0.9)" in trace["weighted_lbf_formula"])

    # 5. argument premise aggregation
    print("\n== argument premise aggregation ==")
    agg = score_argument_premises("ARG-X", [
        {"premise_id": "P1", "log_bayes_factor": 1.0, "w_rel": 0.9, "paradigm": "trika"},
        {"premise_id": "P2", "log_bayes_factor": 0.8, "w_rel": 0.8, "paradigm": "trika"},
    ], paradigm_crowding={"trika": 0})
    check("aggregate exists", "aggregate" in agg)
    check("premises scored", len(agg["premises"]) == 2)
    a = agg["aggregate"]
    check("aggregate posterior in range", 0 < a["posterior"] < 1, a["posterior"])
    # 2nd premise discounted by crowding
    check("2nd premise w_dep < 1st", agg["premises"][1]["paradigm_crowding"] != agg["premises"][0]["paradigm_crowding"])

    # 5b. strong multi-premise argument reaches certain (the mapping's point)
    print("\n== aggregate reaches certain ==")
    strong = score_argument_premises("ARG-Y", [
        {"premise_id": "P1", "log_bayes_factor": 1.5, "w_rel": 0.9, "w_map": 0.8, "w_aux": 0.7, "paradigm": "trika"},
        {"premise_id": "P2", "log_bayes_factor": 1.2, "w_rel": 0.9, "w_map": 0.8, "w_aux": 0.7, "paradigm": "trika"},
        {"premise_id": "P3", "log_bayes_factor": 1.0, "w_rel": 0.9, "w_map": 0.8, "w_aux": 0.7, "paradigm": "trika"},
    ], paradigm_crowding={"trika": 0})
    sa = strong["aggregate"]
    check("3 strong premises → certain", sa["certainty"] == "certain", sa["certainty"])
    check("certain → WELL_SUPPORTED", sa["claim_strength"] == "WELL_SUPPORTED", sa["claim_strength"])

    # 6. formula correctness (hand-computed)
    print("\n== formula correctness ==")
    # weighted = 0.9*0.8*1.0*0.7*1.5 = 0.756 ; prior 0.5 -> lo=0 -> posterior=sigmoid(0.756)
    import math
    exp_post = 1 / (1 + math.exp(-0.756))
    check("weighted_lbf correct", abs(cs.weighted_lbf - 0.756) < 1e-6, cs.weighted_lbf)
    check("posterior correct", abs(cs.posterior - exp_post) < 1e-6, cs.posterior)

    print(f"\n=== RESULT: {PASS} pass / {FAIL} fail ===")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()

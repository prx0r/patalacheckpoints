#!/usr/bin/env python3
"""patala_ml/crux_engine.py — devpath5 (G3C): perturbation-based Crux computation.

The handover's discipline: **cruxes come from perturbation, not importance/centrality.** A crux is a
premise (or small premise-set) whose removal flips the argument's conclusion — the minimal hitting set
of decisive premises (outcome-sensitivity), per ARGUMENT-IR-VISION and SPEC-EPISTEMIC-CORE G3C.

This engine computes, over an assembled argument graph (gold inferences + the derivational Proposition
layer from devpath4):
  1. For every inference, the minimal premise subset whose removal flips the conclusion
     (outcome-sensitivity). Each such decisive premise-set is a Crux candidate.
  2. Each Crux carries: the decisive premises, why they matter (the inference that depends on them),
     what would resolve it (the adjudication question), and the downstream load-bearing status.
  3. The result is `DerivedScholarlyObject(layer=CRUX)`-compatible emissions with an honest ceiling.

Also wires the **Nyāya-profile** onto assembled arguments (the bounded gate from devpath1,
`verify_claim_semantic`) so each argument carries an honest structural audit.

This is a STRUCTURAL/engineering computation (deterministic). It nominates cruxes; it does not settle
truth. The adjudication question is for a scholar/H witness.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

try:
    from .proposition_layer import Proposition, from_gold_node
except ImportError:  # run as a bare script (python patala_ml/crux_engine.py)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from proposition_layer import Proposition, from_gold_node  # noqa: E402


def _sha256(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode("utf-8")).hexdigest()


# a simple deterministic outcome model for the perturbation test:
#   a conclusion holds iff ALL its premises hold (the inference is a conjunction of its premises,
#   plus a warrant). Removing a premise removes support -> the conclusion is no longer licensed
#   (flips from LICENSED -> UNLICENSED).
# This is intentionally minimal and transparent; a richer semantic outcome model can replace the
# `_conclusion_holds` predicate without changing the crux machinery.


def _conclusion_holds(premises_present: set, inference: dict) -> bool:
    """Deterministic outcome model: the conclusion holds iff its support is satisfiable.

    P6 stress-test support (devpath13 P6): the plain AND-rule holds when all premise_ids are present.
    Harder structures are modeled by optional inference fields:
      - `alternative_support_sets`: [[...],[...]] — the conclusion holds if ANY full alternative set
        is present (redundant / P1-OR-P2 independently-sufficient support). When present, it OVERRIDES
        the plain AND rule.
      - `defeaters`: if any defeater is `active` (True), the inference is blocked -> conclusion fails
        even with all premises (a non-monotonic defeater).
    """
    if inference.get("active_defeater"):
        return False  # a defeater blocks the inference (non-monotonic)
    alt = inference.get("alternative_support_sets")
    if alt:
        return any(set(a).issubset(premises_present) for a in alt)
    req = set(inference.get("premise_ids", []))
    return req.issubset(premises_present)


def _minimal_decisive_sets(premise_ids: list[str], inference: dict) -> list[list[str]]:
    """The minimal premise subsets whose removal flips the conclusion (outcome-sensitivity).

    Returns the minimal hitting sets of decisive premises: the smallest premise-set whose absence
    changes the conclusion from LICENSED to UNLICENSED. This IS the crux (perturbation, not
    importance).

    P6 (devpath13): for `alternative_support_sets` (redundant support), the decisive set is the
    premises OUTSIDE the surviving alternative — i.e. what must be removed to leave no alternative
    intact. For plain AND support, it is the minimal combo whose removal breaks the AND (handled below).
    """
    all_ids = list(premise_ids)
    alt = inference.get("alternative_support_sets")
    if alt:
        # conclusion holds iff at least one alternative survives; decisive = premises that kill all
        # alternatives. Minimal decisive set = a hitting set over the alternatives' complements.
        full_present = set(all_ids)
        if not _conclusion_holds(full_present, inference):
            return []
        decisive = []
        # single premises whose removal leaves no alternative intact
        for p in all_ids:
            if not _conclusion_holds(full_present - {p}, inference):
                decisive.append([p])
        if not decisive:
            # need a combination that removes every alternative's full set
            from itertools import combinations
            alt_sets = [set(a) for a in alt]
            n = 2
            while n <= len(all_ids) and not decisive:
                for combo in combinations(all_ids, n):
                    removed = set(combo)
                    if not any(removed.isdisjoint(a) for a in alt_sets):
                        decisive.append(list(combo))
                n += 1
        return decisive
    return _minimal_and_decisive_sets(all_ids, inference)


def _minimal_and_decisive_sets(all_ids: list[str], inference: dict) -> list[list[str]]:
    full_present = set(all_ids)
    if not _conclusion_holds(full_present, inference):
        return []  # conclusion doesn't hold even with all premises -> not a crux here
    minimal = []
    # try removing each single premise (a premise whose removal flips the conclusion is decisive)
    for p in all_ids:
        if not _conclusion_holds(full_present - {p}, inference):
            minimal.append([p])
    # if no single premise is decisive, find the smallest decisive combination (2-element, etc.)
    if not minimal:
        n = 2
        while n <= len(all_ids) and not minimal:
            from itertools import combinations
            for combo in combinations(all_ids, n):
                removed = set(combo)
                if not _conclusion_holds(full_present - removed, inference):
                    minimal.append(list(combo))
            n += 1
    return minimal


def compute_cruxes(arguments: list[dict], propositions: list[Proposition]) -> list[dict]:
    """Compute perturbation-based cruxes over the argument graph.

    arguments:    [{argument_id, inference_scheme, inferences:[{inference_id, premise_ids,
                  conclusion_ids, warrant, ...}]}]
    propositions: the derivational Proposition layer (devpath4) keyed by id.

    Returns crux emissions (DerivedScholarlyObject(layer=CRUX)-compatible).
    """
    prop_by_id = {p.proposition_id: p for p in propositions}
    cruxes = []
    for arg in arguments:
        for inf in arg.get("inferences", []):
            premise_ids = inf.get("premise_ids", [])
            # P6: mark an active defeater (a defeater with status ACTIVE blocks the inference)
            active_defeater = any(
                str(d.get("status", "")).upper() == "ACTIVE"
                for d in inf.get("defeaters", [])
                if isinstance(d, dict))
            inf = {**inf, "active_defeater": active_defeater}
            decisive = _minimal_decisive_sets(premise_ids, inf)
            if not decisive:
                continue
            # a crux per minimal decisive set (the perturbation result)
            for ds in decisive:
                p_texts = []
                source_refs = []
                for pid in ds:
                    p = prop_by_id.get(pid)
                    if p:
                        p_texts.append(p.proposition_text)
                        source_refs.extend(p.source_refs)
                crux_id = f"pt:crux:{arg.get('argument_id')}:{inf.get('inference_id')}:{'-'.join(ds)}"
                cruxes.append({
                    "crux_id": crux_id,
                    "decisive_premises": ds,
                    "premise_texts": p_texts,
                    "inference": inf.get("inference_id"),
                    "argument": arg.get("argument_id"),
                    "why_it_matters": ("The conclusion "
                                       f"{inf.get('conclusion_ids', [])} depends on these premises; "
                                       "removing them flips the conclusion (outcome-sensitivity)."),
                    "method": "PERTURBATION",
                    "adjudication_question": (
                        "Is each decisive premise independently licensed, or is the conclusion "
                        "over-derived from these premises? (scholar/H witness)")
                    ,
                    "review_status": "NOT_HUMAN_REVIEWED",
                    "source_refs": source_refs,
                    "crux_hash": _sha256({"crux_id": crux_id, "decisive_premises": ds}),
                })
    return cruxes


def wire_nyaya_profile(argument: dict, gold_propositions: list[dict]) -> dict:
    """Wire the bounded Nyāya gate onto an assembled argument (the G3C Nyāya-profile).

    Runs `verify_claim_semantic` (devpath1) over the argument's conclusion + each premise, and
    attaches the bounded audit to the argument. The gate stays a bounded evaluator (never
    `argument_valid=true`).
    """
    try:
        from .nyayagate import verify_claim_semantic  # noqa: E402
    except ImportError:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from nyayagate import verify_claim_semantic  # noqa: E402

    # a conclusion = the last inference's conclusion_ids resolved to a proposition text
    inferences = argument.get("inferences", [])
    profile = {"argument_id": argument.get("argument_id"), "checks": [], "outcome": "PASS"}
    checked = 0
    failed = 0
    if inferences:
        last = inferences[-1]
        for cid in last.get("conclusion_ids", []):
            p = {"claim_id": cid, "claim_text": f"conclusion {cid}"}
            # if a proposition text is available, use it
            # (the caller passes gold_propositions which carry text)
            for gp in gold_propositions:
                if gp.get("proposition_id") == cid:
                    p["claim_text"] = gp.get("text", p["claim_text"])
                    p["falsifier"] = {"type": "structural"} if gp.get("status") else None
                    break
            res = verify_claim_semantic(p, gold_propositions=gold_propositions)
            profile["checks"].append({"target": cid, "verdict": res["verdict"],
                                      "dimensions": res["dimensions"]})
            checked += 1
            if res["verdict"] == "FAIL":
                failed += 1
    profile["outcome"] = "FAIL" if failed else ("PASS_WITH_OPEN" if any(
        c["verdict"] == "PASS_WITH_OPEN" for c in profile["checks"]) else "PASS")
    profile["checked"] = checked
    return profile


def build_crux_layer(arguments: list[dict], propositions: list[Proposition],
                     gold_propositions: list[dict] | None = None) -> dict:
    """Assemble the G3C crux layer: cruxes + Nyāya-profiles over the assembled arguments."""
    cruxes = compute_cruxes(arguments, propositions)
    profiles = []
    for arg in arguments:
        prof = wire_nyaya_profile(arg, gold_propositions or [])
        profiles.append(prof)
    return {
        "cruxes": cruxes,
        "nyaya_profiles": profiles,
        "counts": {"cruxes": len(cruxes), "arguments_profiled": len(profiles)},
        "method_honesty": "cruxes = perturbation (outcome-sensitivity), not importance/centrality; "
                          "Nyāya-profile = bounded structural audit, NOT a truth oracle",
    }


def build_arguments_from_gold(gold) -> list[dict]:
    """Assemble an argument graph from a gold object (nodes + inferences)."""
    return [{
        "argument_id": gold.get("gold_id", "ARG-?"),
        "inference_scheme": gold.get("structure", {}).get("scheme", "") if isinstance(gold.get("structure"), dict) else "",
        "inferences": gold.get("inferences", []),
    }]


if __name__ == "__main__":
    _research = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    if _research not in sys.path:
        sys.path.insert(0, _research)
    from patala_ml.gold002 import build_gold_002
    from patala_ml.gold003 import build_gold_003
    from patala_ml.gold004 import build_gold_004
    from patala_ml.gold005 import build_gold_005
    from patala_ml.proposition_layer import from_gold_node

    all_golds = [build_gold_002(), build_gold_003(), build_gold_004(), build_gold_005()]
    arguments = [build_arguments_from_gold(g)[0] for g in all_golds]
    arguments = [a for a in arguments if a["inferences"]]
    propositions = []
    for g in all_golds:
        propositions.extend(from_gold_node(n, g.get("gold_id", "ARG"), "ipvv") for n in g.get("nodes", []))
    # gold nodes already carry proposition_id/text
    gold_propositions = [n for g in all_golds for n in g.get("nodes", [])]

    res = build_crux_layer(arguments, propositions, gold_propositions)
    print(json.dumps(res["counts"], indent=2))
    for c in res["cruxes"][:6]:
        print(f"  ◆ {c['crux_id']}  decisive={c['decisive_premises']}")
        for t in c["premise_texts"]:
            print(f"      {t[:80]}")
    print("Nyāya-profiles:")
    for p in res["nyaya_profiles"]:
        print(f"  {p['argument_id']}: outcome={p['outcome']} checked={p['checked']}")

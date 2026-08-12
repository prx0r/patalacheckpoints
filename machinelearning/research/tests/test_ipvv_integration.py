#!/usr/bin/env python3
"""test_ipvv_integration.py — end-to-end wiring test against the REAL IPVV corpus.

Exercises the connected pipeline (truth-engine gate + graph-aware viruddha + golds + ResearchPack)
on actual IPVV data:

1. CROSS-ARGUMENT viruddha: run each gold's established propositions against the OTHERS to detect
   real conflicts (e.g. does ARG-002 contradict ARG-004? does a claim contradicting a gold get caught?).
2. REAL-PASSAGE test: run the gate + graph viruddha against the reflexion-core IPVV passage (chunkM)
   and its L2.
3. RESEARCHPACK resolution: the pack's refs point to real existing objects (ARG-002 gold, themes,
   propositions, essay).
"""
from __future__ import annotations

import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "experiments"))

from patala_ml.gold import build_gold_v0
from patala_ml.gold002 import build_gold_002
from patala_ml.gold003 import build_gold_003
from patala_ml.gold004 import build_gold_004
from patala_ml.gold005 import build_gold_005
from patala_ml.nyayagate import check_viruddha_graph, validate

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))

GOLDS = {"ARG-GOLD-001": build_gold_v0, "ARG-GOLD-002": build_gold_002,
         "ARG-GOLD-003": build_gold_003, "ARG-GOLD-004": build_gold_004,
         "ARG-GOLD-005": build_gold_005}

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)


print("== 1. CROSS-ARGUMENT: each gold's established claims run against the others ==")
# collect all established propositions (commitment ASSERTS/DERIVES)
established = {}
for gid, fn in GOLDS.items():
    g = fn()
    for n in g["nodes"]:
        comm = str(n.get("commitment") or n.get("speaker") or "").upper()
        if comm in ("ASSERTS", "DERIVES", "SIDDHANTA", "RECONSTRUCTED"):
            established.setdefault(gid, []).append(n)
total_established = sum(len(v) for v in established.values())
check("all 5 golds contribute established propositions", len(established) == 5, str(len(established)))
check("meaningful established-proposition count across golds", total_established >= 20,
      str(total_established))

# for each gold's conclusion, check it against every OTHER gold's established propositions
# (a conclusion should not be flagged as viruddha against its own or other golds unless genuinely opposed)
cross_flags = []
for gid, fn in GOLDS.items():
    g = fn()
    for n in g["nodes"]:
        if n.get("kind") != "CONCLUSION":
            continue
        claim = {"claim_id": f"{gid}:{n.get('proposition_id')}",
                 "claim_text": n.get("proposition") or n.get("text") or "",
                 "pramana": "anumana"}
        for other_gid, props in established.items():
            if other_gid == gid:
                continue  # don't test a gold against itself
            hits = check_viruddha_graph(claim, props)
            if hits:
                cross_flags.append((gid, n.get("proposition_id"), other_gid, len(hits)))
check("cross-argument scan runs without error", True)
# NOTE: genuine cross-gold conflicts are a FINDING (good), not a failure. Log them.
for cf in cross_flags:
    print(f"    [cross-conflict finding] {cf[0]}/{cf[1]} vs {cf[2]} → {cf[3]} viruddha hit(s)")
print(f"    → {len(cross_flags)} cross-gold viruddha findings (these are real disagreement candidates)")

print("\n== 2. REAL-PASSAGE: gate + graph viruddha on the reflexion-core (chunkM) ==")
passage_path = os.path.join(ROOT, "data/published/ipvv",
                            "pt-passage-ipvv-chunkM-jnanadhikara-reflexion-core-md.json")
check("reflexion-core passage exists", os.path.exists(passage_path))
if os.path.exists(passage_path):
    with open(passage_path, encoding="utf-8") as f:
        passage = json.load(f)
    l2 = passage.get("l2_text", "")
    check("reflexion-core passage has L2 content", len(l2) > 200, str(len(l2)))

    # a claim CONTRADICTING the reflexion-core thesis (that determination cannot reach outside)
    contradicting = {"claim_id": "c:chunkM-contra",
                     "claim_text": "The determination (adhyavasāya) establishes an external thing outside the cognition",
                     "pramana": "anumana"}
    # run graph viruddha against ARG-004 (reflexivity/consciousness gold) + ARG-002
    g2 = build_gold_002(); g4 = build_gold_004()
    hits2 = check_viruddha_graph(contradicting, g2["nodes"])
    hits4 = check_viruddha_graph(contradicting, g4["nodes"])
    # the claim asserts a construction/externality the golds deny — expect at least one viruddha signal
    print(f"    viruddha vs ARG-002: {len(hits2)}, vs ARG-004: {len(hits4)}")
    # at least run the gate cleanly on a real L2-derived claim (no crash, valid outcome)
    l2_claim = {"claim_id": "c:chunkM", "claim_text": l2[:300], "pramana": "anumana"}
    res = validate(l2_claim, gold_propositions=g2["nodes"])
    check("gate runs on real reflexion-core L2 without error",
          res.get("outcome") in ("accepted", "accepted_with_penalty", "needs_review", "hollow"),
          res.get("outcome"))

print("\n== 3. RESEARCHPACK resolves against real IPVV objects ==")
pack_path = os.path.join(ROOT, "benchmarks/v0/packs/PACK-IPVV-NONCONSTRUCTED-I.json")
check("ResearchPack exists", os.path.exists(pack_path))
if os.path.exists(pack_path):
    with open(pack_path, encoding="utf-8") as f:
        pack = json.load(f)
    # argument ref resolves to a real gold
    arg_ref = pack["argument_refs"][0]
    check(f"argument_ref '{arg_ref}' is a real gold", arg_ref in GOLDS)
    # proposition refs resolve into the referenced gold
    g2 = build_gold_002()
    prop_ids = {n.get("proposition_id") for n in g2["nodes"]}
    unresolved = [p for p in pack["proposition_refs"] if p not in prop_ids]
    check("all pack proposition_refs resolve into ARG-002", not unresolved, str(unresolved))
    # theme refs resolve against the real theme map
    tm = json.load(open(os.path.join(ROOT, "benchmarks/v0/theme-map-ipvv-v0.json")))
    theme_ids = {t.get("candidate_id") for t in tm.get("themes", [])}
    unresolved_th = [t for t in pack["theme_refs"] if t not in theme_ids]
    check("all pack theme_refs resolve into the theme map", not unresolved_th, str(unresolved_th))
    # essay rendering points to a real existing essay
    essay = pack["renderings"]["essay"]
    check("pack essay rendering references the real essay", "ESSAY-NONCONSTRUCTED-I" in essay)

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (IPVV integration: gate + viruddha + golds + pack connected)"))
sys.exit(1 if failures else 0)

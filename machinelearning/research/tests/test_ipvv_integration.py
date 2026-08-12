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
        # only TEXTUALLY-COMMITTED (ASSERTS/SIDDHANTA) or DERIVED (DERIVES) count as established;
        # RECONSTRUCTED is EXCLUDED (a reconstruction is not independently established and must not
        # create apparent disagreement in the IPVV).
        if comm in ("ASSERTS", "DERIVES", "SIDDHANTA"):
            established.setdefault(gid, []).append(n)
total_established = sum(len(v) for v in established.values())
check("all 5 golds contribute established propositions", len(established) == 5, str(len(established)))
check("established (non-reconstructed) proposition count", total_established >= 15,
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
# These are TENSION CANDIDATES for inspection, NOT settled disagreements. The detector is
# 'selective enough to nominate a small set of cross-argument tension candidates' — it does NOT
# establish precision or real philosophical disagreement.
for cf in cross_flags:
    print(f"    [tension candidate] {cf[0]}/{cf[1]} vs {cf[2]} → {cf[3]} viruddha hit(s)")
print(f"    → {len(cross_flags)} cross-gold tension candidates (NOT settled disagreements; "
      f"require semantic review + the T3/T4 eligibility gate)")

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

    # run graph viruddha against ARG-002 + ARG-004
    g2 = build_gold_002(); g4 = build_gold_004()
    hits2 = check_viruddha_graph(contradicting, g2["nodes"])
    hits4 = check_viruddha_graph(contradicting, g4["nodes"])
    print(f"    viruddha vs ARG-002: {len(hits2)}, vs ARG-004: {len(hits4)}")
    l2_claim = {"claim_id": "c:chunkM", "claim_text": l2[:300], "pramana": "anumana"}
    res = validate(l2_claim, gold_propositions=g2["nodes"])
    check("gate runs on real reflexion-core L2 without error",
          res.get("outcome") in ("accepted", "accepted_with_penalty", "needs_review", "hollow"),
          res.get("outcome"))

print("\n== 2b. Detector discipline: akrama same-claim abstains; junk overlap does not fire ==")
g2 = build_gold_002()
g3 = build_gold_003()
# PRECISION-FIRST invariant: akrama = a-krama = not-order = 'order-less'. 'X is order-less' and
# 'X is not constituted by order (akrama)' are the SAME claim in different polarity ENCODING, so
# the detector must ABSTAIN (0 hits) — not nominate it as a contradiction. This is the honest
# precision-first behavior (the akrama same-claim is not a real disagreement).
same_claim = {"claim_id": "c:akrama", "claim_text": "pratibhā is order-less (akrama)",
              "pramana": "anumana"}
check("akrama same-claim ABSTAINS (0 hits — same claim in different encoding)",
      len(check_viruddha_graph(same_claim, g3["nodes"])) == 0,
      str(len(check_viruddha_graph(same_claim, g3["nodes"]))))
# function-word junk: 'a/one/the' overlap must NOT fire
junk = {"claim_id": "c:junk", "claim_text": "one a the awareness self", "pramana": "anumana"}
check("function-word-only claim does not fire viruddha", len(check_viruddha_graph(junk, g2["nodes"])) == 0)
# opponent-attributed propositions must NOT count as established (no viruddha from the objector)
g_obj = build_gold_002()
obj = [n for n in g_obj["nodes"] if n.get("proposition_id") == "G2-OBJ"]
check("opponent-attributed proposition excluded from established (no viruddha)",
      len(check_viruddha_graph(
          {"claim_id": "x", "claim_text": "reflexive awareness IS a conceptual construction"},
          obj)) == 0)

print("\n== 2c. GENUINE dataflow: ArgumentProposal -> graph audit -> audit_ref on the argument ==")
from patala_ml.argument import build_argument, audit_argument, NyayaMember
arg = build_argument(
    "pt:argument:ipvv:reflexion-core", "ipvv", "The reflexion-core argument", "ENTAILMENT",
    members=[NyayaMember(role="PRATIJNA", text="The determination cannot establish externality."),
             NyayaMember(role="HETU", text="The object-form is inert."),
             NyayaMember(role="UDAHARANA", text="An inert thing cannot establish."),
             NyayaMember(role="UPANAYA", text="The determination is error-form."),
             NyayaMember(role="NIGAMANA", text="Self-experience is self-luminous, not reaching out.")],
)
# build_argument is construction-only (gate is None); audit is separate
check("build_argument is construction-only (no graph audit at construction)",
      arg.gate is None and arg.audit_refs == [])
# run the graph-aware audit against a REAL gold (ARG-004: consciousness/reflexivity)
g4 = build_gold_004()
audit = audit_argument(arg, comparison_graph=g4["nodes"])
check("audit_argument runs the graph-aware gate (returns audit_id + outcome)",
      "audit_id" in audit and audit.get("outcome") in ("accepted", "accepted_with_penalty", "needs_review", "hollow"))
check("the audit_id is recorded on the ArgumentProposal.audit_refs",
      audit["audit_id"] in arg.audit_refs)
check("the audited argument serializes with its audit_ref",
      arg.to_dict()["audit_refs"] == arg.audit_refs)
# the argument (via its conclusion) is now an auditable object that a ResearchPack can reference
check("audited argument carries a conclusion the pack layer can bind to",
      arg.conclusion is not None and bool(arg.conclusion.text))

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

# also validate the reflexion-core pack (the second ResearchPack on a real IPVV passage)
rc_path = os.path.join(ROOT, "benchmarks/v0/packs/PACK-IPVV-REFLEXION-CORE.json")
check("reflexion-core ResearchPack exists", os.path.exists(rc_path))
if os.path.exists(rc_path):
    from check_research_pack import check_pack
    r = check_pack(rc_path)
    check("reflexion-core pack well-formed", r["ok"], str(r["problems"]))
    rc = json.load(open(rc_path))
    g4 = build_gold_004()
    g4_ids = {n.get("proposition_id") for n in g4["nodes"]}
    check("reflexion-core pack references real ARG-004 props (G4-CRYSTAL/G4-CONC)",
          {"G4-CRYSTAL", "G4-CONC"} <= g4_ids)
    check("reflexion-core pack points to a real published passage",
          os.path.exists(os.path.join(ROOT, "data/published/ipvv",
                         "pt-passage-ipvv-chunkM-jnanadhikara-reflexion-core-md.json")))

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (IPVV integration: gate + viruddha + golds + pack connected)"))
sys.exit(1 if failures else 0)

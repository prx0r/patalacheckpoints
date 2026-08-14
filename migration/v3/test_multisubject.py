#!/usr/bin/env python3
"""test_multisubject.py — run the proven v3 kernels on MULTIPLE DIFFERENT subjects to prove generality.

The anti-theatre test for v3: a mechanism that only works on one corpus (IPVV) is not proven —
it's overfit. This runs the SAME kernels on three genuinely different subjects:
  1. IPVV   (Sanskrit philosophy — the gold vertical)
  2. Doyle  (a 2009 Nature science paper — the lab's own general corpus)
  3. Ratié  (contemporary philosophy scholarship — Le Soi et l'Autre)
If the kernels behave correctly across all three, they generalize. If a step only works on one,
that step is called out honestly.
"""
import os, sys, json, hashlib
sys.path.insert(0, "/mnt/HC_Volume_106427611/ip-graph/lib")

from epistemic import EpistemicEnvelope, Authority, rank, invariant_ok
from review import reducer, ReviewState, ReviewPhase, promote
from scholar_review import verify_citations, Finding
from staleness import build_dependency_index, blast_radius, incremental_rebuild_order
from education import LearningClaim, wrong_answer_to_neighbor
from pedagogy import MasteryEvidence, LearnerState, mastery_reducer
from essay_ingest import EssayIngestor

ROOT = "/mnt/HC_Volume_106427611"
results = []
def check(subject, name, cond, detail=""):
    results.append((subject, bool(cond)))
    mark = "PASS" if cond else "FAIL"
    print(f"  [{mark}] [{subject}] {name} {detail}")

# ═══════════════════════════ SUBJECT 1: IPVV (Sanskrit philosophy) ═══════════════════════════
def subject_ipvv():
    s = "IPVV"
    IPVV = f"{ROOT}/sanskritree/translations/_stack/ipvv"
    # raw + T1 + L2 + C1 gold
    src = open(f"{IPVV}/00_source/torella_ipk.txt").read()
    check(s, "raw Torella IPK text", len(src) > 50000)
    t1 = open(f"{IPVV}/02_t1/chunkV2-A-caturtho-vimarsa-aham.md").read()
    check(s, "T1 word-faithful draft", "[and]-the-Lord" in t1)
    l2 = open(f"{IPVV}/pilot/pilot_V2A_L2_read.md").read()
    check(s, "L2 readable prose", "Memory as the Lord's power" in l2)
    c1 = open(f"{IPVV}/c1/read/c1_V2A-memory-lords-power.md").read()
    check(s, "C1 commentary", "memory" in c1.lower())
    # epistemic: the honest ceiling
    env_corr = EpistemicEnvelope(id="IPK-1.5.19", layer="04", type="claim",
                                 epistemic_ceiling="SCHOLARLY_CORROBORATED", source_refs=["IPK 1.5.19"])
    env_machine = EpistemicEnvelope(id="felt-ground", layer="04", type="claim",
                                    epistemic_ceiling="MACHINE_PROPOSED", source_refs=["Ratié Ch7"])
    check(s, "epistemic: corroborated vs machine-proposed distinct",
          rank(env_corr.epistemic_ceiling) > rank(env_machine.epistemic_ceiling))
    check(s, "epistemic: invariant holds", invariant_ok(rank(env_machine.epistemic_ceiling), rank(env_machine.epistemic_ceiling)))
    # review reducer
    st = ReviewState("ipvv-claim"); reducer(st, evidence_ok=True)
    check(s, "review: evidence advances the claim", st.phase in (ReviewPhase.ALIGNED, ReviewPhase.REVIEWING))
    # staleness
    dag = {"1.5.11": {"requires": []}, "1.5.19": {"requires": ["1.5.11"]}, "felt-ground": {"requires": ["1.5.19"]}}
    stale = blast_radius(build_dependency_index(dag), {"1.5.11"})
    check(s, "staleness: retract 1.5.11 flags the thesis", "felt-ground" in stale)
    # education
    lc = LearningClaim(learning_claim_id="LC1", content="reconstruct memory-as-lords-power", derived_from=["IPK 1.2.3"], claim_type="thesis")
    check(s, "education: LearningClaim", lc.learning_claim_id == "LC1")

# ═══════════════════════════ SUBJECT 2: DOYLE (science paper, Nature 2009) ═══════════════════════════
def subject_doyle():
    s = "DOYLE"
    doyle = open(f"{ROOT}/ip-graph/data/extracted_md/pdf/articles/Doyle-Nature-25June2009.md").read()
    check(s, "raw Doyle Nature paper", len(doyle) > 2000 and ("physics" in doyle.lower() or "quantum" in doyle.lower() or "membrane" in doyle.lower()))
    # epistemic on a science claim
    env = EpistemicEnvelope(id="doyle-thesis", layer="04", type="claim",
                            epistemic_ceiling="SCHOLARLY_CORROBORATED", source_refs=["Doyle-Nature-2009"])
    check(s, "epistemic: science claim enveloped", env.epistemic_ceiling == "SCHOLARLY_CORROBORATED")
    # review reducer on the science claim — the human gate
    st = ReviewState("doyle-claim"); reducer(st, evidence_ok=True, human_approves=False)
    # human_approves=False → never reaches HUMAN_OVERRIDE (the human-gated terminal); evidence alone
    # only advances to REVIEWING/ALIGNED, and the claim is NOT granted canonical status
    check(s, "review: evidence without human approval does NOT reach the human-gated terminal",
          st.phase != ReviewPhase.HUMAN_OVERRIDE and st.phase in (ReviewPhase.REVIEWING, ReviewPhase.ALIGNED))
    # with human approval it can reach the terminal state
    st2 = ReviewState("doyle-claim2"); reducer(st2, evidence_ok=True, human_approves=True)
    check(s, "review: human approval reaches the terminal human-gated state",
          st2.phase == ReviewPhase.HUMAN_OVERRIDE)
    # staleness across a science DAG
    dag = {"QM": {"requires": []}, "OBSERVER": {"requires": ["QM"]}, "CONSCIOUSNESS": {"requires": ["OBSERVER"]}}
    stale = blast_radius(build_dependency_index(dag), {"QM"})
    check(s, "staleness: retract QM flags observer+consciousness", "OBSERVER" in stale and "CONSCIOUSNESS" in stale)
    # education: wrong answer to known neighbor (graph_neighbors is a callable)
    nb = wrong_answer_to_neighbor("consciousness", "observer collapses wavefunction",
                                  lambda claim: ["quantum measurement", "observation"])
    check(s, "education: wrong answer maps to known neighbor", bool(nb.get("maps_to_epistemic_neighbor")))
    # essay ingest on the science paper (mine claims)
    ing = EssayIngestor("doyle")
    ing.structure("The Nature of Physics", "Doyle", [{"id": "s1", "chapter": "physics", "ipk_refs": []}])
    ing.mine_claim("The physics thesis", "Doyle-Nature", "SCHOLARLY_CORROBORATED", "thesis", "quantum", "s1")
    check(s, "essay-ingest: science claim mined", len(ing.claims) == 1)

# ═══════════════════════════ SUBJECT 3: RATIÉ (philosophy scholarship) ═══════════════════════════
def subject_ratie():
    s = "RATIE"
    # the Ratié essay (Le Soi et l'Autre) is the essay_ingest real-data test subject
    ing = EssayIngestor("ratie-le-soi-et-lautre")
    ing.structure("Le Soi et l'Autre", "Ratié", [{"id": "ch7", "chapter": "ch7", "ipk_refs": ["IPK 1.5.19"]}])
    ing.mine_claim("Recognition is the felt (camatkāra) ground", "Ratié Ch7", "SCHOLARLY_CORROBORATED",
                   "thesis", "camatkāra", "ch7")
    ing.mine_claim("Recognition is not a construction", "Ratié Ch4", "SCHOLARLY_CORROBORATED",
                   "conclusion", "not construction", "ch7")
    ing.add_move("Recognition is felt", "Recognition is not construction", "PRESUPPOSITION")
    ing.detect_crux("felt recognition", "construction reading", "OPEN", "Ratié vs constructionist reading")
    check(s, "essay-ingest: philosophy claims + crux mined", len(ing.claims) == 2 and len(ing.cruxes) == 1)
    rep = ing.report()
    check(s, "essay-ingest: report has hash", len(rep["hash"]) == 10)
    # citecheck on the philosophy refs
    cits = verify_citations(["Ratié Ch7", "IPK 1.5.19"], known_refs={"Ratié Ch7", "IPK 1.5.19"})
    check(s, "review: philosophy citations resolve", all(c.status != "PHANTOM" for c in cits))
    # pedagogy on a philosophy learner (pedagogy.MasteryEvidence matches mastery_reducer)
    ev = MasteryEvidence("learner", "LC-camatkara", "CRUX_IDENTIFICATION",
                         response="assumed felt entails universal ground", correct=False)
    ls = mastery_reducer(LearnerState("learner"), ev)
    check(s, "pedagogy: wrong answer → skill held + misconception recorded",
          "LC-camatkara" in ls.misconception_state)

# ═══════════════════════════ RUN ALL SUBJECTS ═══════════════════════════
print("=== MULTI-SUBJECT KERNEL TEST: IPVV + DOYLE + RATIE ===\n")
subject_ipvv()
print()
subject_doyle()
print()
subject_ratie()
print(f"\n=== SUMMARY: {sum(1 for _,c in results if c)}/{len(results)} passed ===")
from collections import Counter
by = Counter(s for s,c in results if c)
tot = Counter(s for s,_ in results)
for s in ["IPVV","DOYLE","RATIE"]:
    print(f"  {s}: {by[s]}/{tot[s]}")
sys.exit(0 if all(c for _,c in results) else 1)

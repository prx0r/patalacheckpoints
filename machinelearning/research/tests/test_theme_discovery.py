#!/usr/bin/env python3
"""test_theme_discovery.py — validation of the recall-first theme-discovery pipeline."""
from __future__ import annotations
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patala_ml.theme_discovery import (discover_themes, segment, extract_concepts,
                                       check_sense_stability, coverage_audit)

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)

DOC = """Passage one: vimarśa is the reflexive awareness, the self-grasping of the light.

Passage two: pramāṇa is the means of knowledge; anumāna is inference.

Passage three: the orderless support (āśraya) is not itself ordered.

Passage four: vimarśa, as reflexive awareness, is also the basis of recognition and memory.

Passage five: pramāṇa as a means of knowledge supports inference and perception.
"""

print("== structure + decomposition ==")
res = discover_themes(DOC)
check("returns ThemeDiscoveryResult keys",
      all(k in res for k in ["segments","extracted_concepts","candidate_objects",
                             "uncovered_segments","uncertain_assignments","coverage","provenance"]))
check("decomposed into separate tasks", res["provenance"]["decomposition"] ==
      ["segment","concept_extraction","relation_graph","grouping","kind_proposal",
       "sense_stability","coverage_audit"])
check("all candidates MACHINE_PROPOSED",
      all(c["status"] == "MACHINE_PROPOSED" and c["origin"] == "MACHINE" for c in res["candidate_objects"]))
check("candidates carry the full contract",
      all(all(k in c for k in ["candidate_id","label","suspected_kind","member_segments","key_lemmas",
                               "sense_stability","membership_rationale","nearest_competing_candidate",
                               "origin","status"]) for c in res["candidate_objects"]))

print("\n== recall-first: the three concepts surface ==")
labels = [c["label"] for c in res["candidate_objects"]]
for concept in ["vimarśa", "pramāṇa", "orderless"]:
    check(f"'{concept}' surfaces as a candidate", any(concept in l for l in labels), labels)

print("\n== overlap is allowed ==")
# passage four mentions vimarśa + recognition + memory -> should be in multiple candidates
multi = [c for c in res["candidate_objects"] if "vimarśa" in c["label"]][0]["member_segments"]
check("a multi-concept segment can be assigned to multiple candidates",
      res["coverage"]["n_multi_assigned"] >= 1, str(res["coverage"]["n_multi_assigned"]))

print("\n== coverage accounting ==")
segs = segment(DOC)
audit = coverage_audit(res["candidate_objects"], len(segs))
check("assigned + unassigned == total", audit["n_assigned"] + audit["n_unassigned"] == len(segs))
check("assigned_pct consistent", abs(audit["assigned_pct"] - audit["n_assigned"]/len(segs)) < 1e-9)

print("\n== sense-stability is coarse and MACHINE_PROPOSED ==")
svals = {c["sense_stability"] for c in res["candidate_objects"]}
check("uses only the coarse vocabulary", svals <= {"SAME_SENSE","NEAR_SAME","DIFFERENT_SENSE",
                                                   "AMBIGUOUS","NOT_ENOUGH_CONTEXT","NOT_YET_JUDGED"}, str(svals))

print(f"\n=== RESULT: {len(failures)} fail ===")
sys.exit(1 if failures else 0)

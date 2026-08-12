#!/usr/bin/env python3
"""test_vertical.py — RESOLUTION / INTEGRITY tests for the vertical object v0.

These prove IDs/links resolve and are TYPED. They do NOT prove scholarly validity (that a span entails
the proposition, that the reconstruction is defensible, etc.) — that is review, not resolution.
"""
from __future__ import annotations
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patala_ml.gold import build_gold_v0, V2O_PROOF_ID
from patala_ml.vertical import build_vertical, load_l0, resolve_exact_refs, extract_sanskrit, norm

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)

CHUNK = "chunkV2-O-saptamo-vimarsa"
GROUNDING_REFS = [f"{CHUNK}:L32:T114", f"{CHUNK}:L32:T115", f"{CHUNK}:L33:T116", f"{CHUNK}:L44:T181"]

print("== primitives ==")
check("norm strips diacritics", norm("pratibhā") == "pratibha")
check("extract_sanskrit handles trailing quote", extract_sanskrit('(pratibhā ...)"') == "pratibhā ...")

print("\n== exact ref resolution (GOLD grounding, no search) ==")
recs = load_l0(CHUNK)
found, missing = resolve_exact_refs(recs, GROUNDING_REFS)
check("all exact grounding refs resolve", not missing, str(missing))
check("exact refs return the requested records", len(found) == len(GROUNDING_REFS))
check("L32:T114 is pratibhā", any(r["id"].endswith("L32:T114") and r.get("lemma_iast") == "pratibhā" for r in found))
check("an unknown ref is reported unresolved",
      resolve_exact_refs(recs, [f"{CHUNK}:L999:T999"])[1] != [])

print("\n== the vertical object (typed edges + honest resolution) ==")
gold = build_gold_v0()
v = build_vertical(gold, "G-TC2", GROUNDING_REFS, "pilot_V2O_L2_read.md", V2O_PROOF_ID,
                   key_terms=["pratibhā", "rūṣitā", "akrama"],
                   c1_span="the flashing ... but itself not ordered.",
                   l2_span="The flashing itself is not ordered.",
                   authoritative_proof_version="P0 35/35 (frozen)")
check("proposition carried through", v["proposition"]["proposition_id"] == "G-TC2")
check("G-TC2 is a PREMISE of G-INF1", any(i["inference_id"] == "G-INF1" and i["proposition_role"] == "PREMISE"
                                          for i in v["inferences_using_proposition"]))
check("direct grounding = the exact refs only", len(v["direct_grounding"]) == len(GROUNDING_REFS))
check("candidate_context is separate (discovery, not evidence)", "candidate_context" in v
      and sum(len(a) for a in v["candidate_context"].values()) >= len(GROUNDING_REFS))
check("C1 edge is SPAN_LEVEL (exact span given)", v["c1"]["resolution"] == "SPAN_LEVEL")
check("L2 edge is SPAN_LEVEL (exact span given)", v["l2"]["resolution"] == "SPAN_LEVEL")
check("every link has a typed relation + resolution",
      all(l.get("relation") and l.get("resolution") for l in v["links"]))
check("grounding links are EXACT", any(l["relation"] == "TEXTUALLY_GROUNDED_BY" and l["resolution"] == "EXACT"
                                       for l in v["links"]))
# proof must be EXACT / REFERENCE_RESOLVED now that Agent 2 regenerated the authoritative proof
pp = v["philological_proof"]
check("proof resolution is EXACT (authoritative proof now on disk)", pp["resolution"] == "EXACT", pp["resolution"])
check("proof status labels the reference-resolved artifact", pp["status"] == "REFERENCE_RESOLVED", pp["status"])
check("proof carries the authoritative version ref", pp["authoritative_version"] == "P0 35/35 (frozen)")
# missing IR fields surfaced, NOT retrofitted
check("research_question surfaced as null (ARG-001 predates it)", v["research_question"] is None)
check("commitment surfaced as null (not retrofitted)", v["proposition"]["commitment"] is None)
# no UNRESOLVED arrows remain (all layers located)
check("no UNRESOLVED resolutions", "UNRESOLVED" not in v["unresolved_resolutions"], str(v["unresolved_resolutions"]))

print(f"\n=== RESULT: {len(failures)} fail ===")
sys.exit(1 if failures else 0)

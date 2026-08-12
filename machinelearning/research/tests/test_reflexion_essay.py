#!/usr/bin/env python3
"""test_reflexion_essay.py — Commit C: the essay + SentenceEvidenceAudit, with adversarial prose mutations.

Proves that readable prose can be generated from the epistemically constrained object WITHOUT claim inflation:
  - the happy-path audit is VALID (every synthesis sentence resolves through SYN-INF-001);
  - 5 adversarial mutations each FAIL for the right epistemic reason (metadata-driven, NOT forbidden-word regex):
      A. STRENGTH INFLATION   (suggests -> proves)
      B. AUTHORSHIP LAUNDERING (reconstruction -> "Abhinavagupta argues")
      C. BOUNDARY ERASURE      (drop the universal-Self / not-established boundary)
      D. RIVAL LAUNDERING      (unsourced opponent rendered as asserted)
      E. WARRANT ERASURE       (claim the thesis but bypass SYN-INF-001, citing sources directly)
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "experiments"))
from build_reflexion_essay import build_audit, sentences
from check_sentence_evidence_audit import check_audit, synthesis_authority

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)

authority = synthesis_authority()
audit = build_audit(authority)
r = check_audit(audit, authority)
check("happy-path essay audit is VALID", r["ok"], str(r["problems"]))

def find(sid):
    return next(s for s in audit["sentences"] if s["sid"] == sid)

print("\n== happy path: synthesis sentence resolves through the bridge ==")
s8 = find("S008")
check("thesis sentence S008 carries SYN-INF-001 in inference_refs (no bypass)", "SYN-INF-001" in s8["inference_refs"])
check("thesis sentence S008 is QUALIFIED (not DIRECT)", s8["render_mode"] == "QUALIFIED")
check("thesis sentence S008 is NOT attributed to Abhinavagupta", s8["speaker"] != "Abhinavagupta")

print("\n== A. STRENGTH INFLATION (suggests -> proves) ==")
bad = json.loads(json.dumps(audit))
find_b = next(s for s in bad["sentences"] if s["sid"] == "S008")
find_b["assertion_strength"] = "PROVEN"
ra = check_audit(bad, authority)
check("A fails (inflation on a reconstructed thesis)", not ra["ok"])
check("A fails for the inflation reason", any("inflation" in p for p in ra["problems"]), str(ra["problems"]))

print("\n== B. AUTHORSHIP LAUNDERING (reconstruction -> 'Abhinavagupta argues') ==")
bad = json.loads(json.dumps(audit))
find_b = next(s for s in bad["sentences"] if s["sid"] == "S008")
find_b["speaker"] = "Abhinavagupta"
rb = check_audit(bad, authority)
check("B fails (reconstruction mis-attributed to the author)", not rb["ok"])
check("B fails for the authorship-laundering reason", any("authorship" in p for p in rb["problems"]), str(rb["problems"]))

print("\n== C. BOUNDARY ERASURE (drop the not-established boundary) ==")
bad = json.loads(json.dumps(audit))
bad["sentences"] = [s for s in bad["sentences"] if s["sid"] != "S012"]  # drop the boundary sentence
rc = check_audit(bad, authority)
check("C fails (boundary erased)", not rc["ok"])
check("C fails for the boundary-erasure reason", any("boundary erasure" in p for p in rc["problems"]), str(rc["problems"]))

print("\n== D. RIVAL LAUNDERING (unsourced opponent rendered as asserted) ==")
bad = json.loads(json.dumps(audit))
find_b = next(s for s in bad["sentences"] if s["sid"] == "S013")
find_b["render_mode"] = "DIRECT"
find_b["assertion_strength"] = "PROVEN"
rd = check_audit(bad, authority)
check("D fails (unsourced rival asserted)", not rd["ok"])
check("D fails for the rival-laundering reason", any("rival" in p for p in rd["problems"]), str(rd["problems"]))

print("\n== E. WARRANT ERASURE (claim the thesis but bypass SYN-INF-001) ==")
bad = json.loads(json.dumps(audit))
find_b = next(s for s in bad["sentences"] if s["sid"] == "S008")
find_b["inference_refs"] = []          # drop the bridge
find_b["source_refs"] = ["pt:passage:ipvv:chunkV2-L-sastho-vimarsa-smrti-apohana.md"]  # cite source directly
re_ = check_audit(bad, authority)
check("E fails (thesis claimed without the bridge inference)", not re_["ok"])
check("E fails for the warrant-erasure / provenance-bypass reason",
      any("bypass" in p or "warrant" in p for p in re_["problems"]), str(re_["problems"]))

print("\n== non-load-bearing prose is exempt (C06): essay can still read naturally ==")
trans = {"sid": "S014", "role": "TRANSITION",
         "text": "The second argument approaches the problem from another direction."}
audit_ex = json.loads(json.dumps(audit))
audit_ex["sentences"].append(trans)
check("a TRANSITION sentence with no provenance chain is allowed", check_audit(audit_ex, authority)["ok"])

print("\n== C.1 — paraphrase-expansion guard (semantic-strength drift inside a single proposition) ==")
# every LOAD_BEARING claimed sentence carries a valid semantic_relation_to_claim
for s in audit["sentences"]:
    if s["role"] == "LOAD_BEARING" and s.get("claim_refs"):
        check(f"{s['sid']}: semantic_relation_to_claim present",
              s.get("semantic_relation_to_claim") in ("EXACT", "CONSERVATIVE_PARAPHRASE", "EXPANSIVE"))

# S007 is RECONSTRUCTED/QUALIFIED (G4-CONC is RECONSTRUCTED), not AUTHOR/TEXTUAL
s7 = next(s for s in audit["sentences"] if s["sid"] == "S007")
check("S007 is RECONSTRUCTED/QUALIFIED (G4-CONC reconstructed), not AUTHOR/TEXTUAL",
      s7["attribution"] == "SYNTHESIS" and s7["render_mode"] == "QUALIFIED"
      and s7["assertion_strength"] == "RECONSTRUCTED")
check("S007 no longer imports the 'rather than a thing' contrast (conservative narrowing)",
      "rather than a thing" not in s7["text"] and s7["semantic_relation_to_claim"] == "CONSERVATIVE_PARAPHRASE")

# REVISE-pass locks (6b19f2b review): S005 reconstruction, S009 no-strengthen, S010 no-unaudited-follows,
# S001 source closure, S006 no-reflect
s5 = next(s for s in audit["sentences"] if s["sid"] == "S005")
check("S005 is RECONSTRUCTED/SYNTHESIS (G2-CONC is RECONSTRUCTED_NECESSARY, not authorial)",
      s5["attribution"] == "SYNTHESIS" and s5["assertion_strength"] == "RECONSTRUCTED")
s9 = next(s for s in audit["sentences"] if s["sid"] == "S009")
check("S009 no longer strengthens G2-CONC to 'is not a construction' / no 'conclusion follows'",
      "not a construction" not in s9["text"] and "conclusion follows" not in s9["text"])
s10 = next(s for s in audit["sentences"] if s["sid"] == "S010")
check("S010 no longer manufactures an unaudited 'conclusion follows' / strength UNRESOLVED",
      "conclusion follows" not in s10["text"] and "not yet been audited" in s10["text"]
      and s10["assertion_strength"] == "UNRESOLVED")
s1 = next(s for s in audit["sentences"] if s["sid"] == "S001")
check("S001 source closure complete (V2-L + V2-H, matching the synthesis's two premises)",
      len(s1["source_refs"]) == 2 and any("chunkV2-H" in r for r in s1["source_refs"]))
s6 = next(s for s in audit["sentences"] if s["sid"] == "S006")
check("S006 no longer adds 'it would reflect' surface content",
      "would reflect" not in s6["text"])

# C.1-review fixes: S001 is EXPANSIVE but BACKED by the synthesis (SYN-CONC-001 + SYN-INF-001), so it passes
s1 = next(s for s in audit["sentences"] if s["sid"] == "S001")
check("S001 is EXPANSIVE with synthesis backing (SYN-CONC-001 + SYN-INF-001 refs) — not an unsupported expansion",
      s1["semantic_relation_to_claim"] == "EXPANSIVE"
      and "SYN-CONC-001" in s1["claim_refs"] and "SYN-INF-001" in s1["inference_refs"])
# S003/S004 now track their propositions exactly (EXACT), not importing neighbor-category wording
s3 = next(s for s in audit["sentences"] if s["sid"] == "S003")
s4 = next(s for s in audit["sentences"] if s["sid"] == "S004")
check("S003 is CONSERVATIVE_PARAPHRASE to G2-TC1 (payload exact, sentence adds framing)",
      s3["semantic_relation_to_claim"] == "CONSERVATIVE_PARAPHRASE" and "combines" in s3["text"])
check("S004 is CONSERVATIVE_PARAPHRASE to G2-TC2 (legitimate narrowing), no G2-TC1 leak",
      s4["semantic_relation_to_claim"] == "CONSERVATIVE_PARAPHRASE"
      and "assembled out of parts" not in s4["text"]
      and "not itself treated as one more constructed relation" in s4["text"])

# MUTATION: a faithful sentence acquires an unsupported clause -> EXPANSIVE with no extra refs -> FAIL
good = "The passage distinguishes the I-awareness from the operations of conceptual construction."
bad = "The passage therefore shows that the I-awareness is the universal precondition of every cognition."
bad_audit = json.loads(json.dumps(audit))
b = next(s for s in bad_audit["sentences"] if s["sid"] == "S004")
b["text"] = bad
b["semantic_relation_to_claim"] = "EXPANSIVE"     # added a stronger clause
b["claim_refs"] = ["ARG-GOLD-002:G2-TC2"]          # only the base claim, no extra refs
b["inference_refs"] = []
rf = check_audit(bad_audit, authority)
check("unsupported paraphrase expansion (EXPANSIVE, no extra refs) is REJECTED", not rf["ok"])
check("fails for the paraphrase-expansion reason", any("EXPANSIVE" in p or "expansion" in p for p in rf["problems"]),
      str(rf["problems"]))

print("\n" + ("RESULT: FAIL" if failures else "RESULT: PASS (prose preserves the epistemic graph; 5 mutations caught for the right reasons)"))
sys.exit(1 if failures else 0)

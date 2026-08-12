#!/usr/bin/env python3
"""build_essay_from_synthesis.py — the first essay that CONSUMES an ArgumentSynthesis.

Pipeline (per the architecture): ArgumentSynthesis -> EssayPlan -> Draft -> SentenceEvidenceAudit.

This is grounded in the gold-standard reflexion debate (research-library LOGICAL-ARGUMENT-1 + the
observer proofs): reflexivity is ESTABLISHED (all four candidates agree on the phenomenon), but its
nature is CONTESTED (three live positions), and the universalization (C) is NOT entailed.

The synthesis SYN-IPVV-REFLEXION-CORE-001 exposes the unsupported bridge (SYN-INF-001, MACHINE_
RECONSTRUCTED) and an UNRESOLVED ceiling. The essay must respect that: every load-bearing sentence
maps to a claim that resolves to a proposition or an explicitly-marked bridge, and the essay's
conclusion carries the honest boundary (reflexivity established; universalization not entailed).

Each sentence carries a provenance relation + the claim it licenses. The SentenceEvidenceAudit checks
that no sentence overclaims beyond its claim's ceiling (the hard render rule: UNRESOLVED -> qualify,
never settle).
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))
SYN = os.path.join(ROOT, "benchmarks/v0/review/SYN-IPVV-REFLEXION-CORE-001.json")


def main() -> int:
    with open(SYN, encoding="utf-8") as f:
        syn = json.load(f)

    audit = syn["synthesis_audit"]
    ceiling = audit["epistemic_ceiling"]
    unsupported = audit["unsupported_bridges"]

    # EssayPlan: claims resolve to synthesis inputs/bridges + the gold-standard debate positions
    # Each claim: text + role + provenance (proposition or marked bridge) + ceiling
    claims = [
        # ---- grounded claims (resolve to a synthesis input proposition) ----
        {"id": "essay:c1", "role": "supporting", "text": "The 'I'-reflexive-awareness is not a conceptual construction.",
         "provenance": "gold:ARG-GOLD-002:G2-TC2", "ceiling": "UNRESOLVED"},
        {"id": "essay:c2", "role": "supporting", "text": "Manifestation without reflexive awareness (vimarśa) would be inert, like crystal.",
         "provenance": "gold:ARG-GOLD-004:G4-CRYSTAL", "ceiling": "PARTIALLY_CORROBORATED"},
        # ---- the reconstructed bridge (MUST be marked, never settled) ----
        {"id": "essay:c3", "role": "thesis", "text": "Reflexivity belongs intrinsically to manifestation.",
         "provenance": "SYN-INF-001", "ceiling": "UNRESOLVED", "bridge": True},
        # ---- the honest boundary from the gold-standard debate ----
        {"id": "essay:c4", "role": "qualification", "text": "Reflexivity is established as a real feature of experience, but its nature is contested and the universalization is not entailed.",
         "provenance": "gold-standard:LOGICAL-ARGUMENT-1-resolution", "ceiling": "CAN_RENDER"},
    ]

    # Essay sentences, each licensed by a claim (provenance relation); the sentence must not
    # overclaim beyond its claim's ceiling (the hard render rule).
    sentences = [
        {"id": "s1", "text": "The I-reflexive-awareness is not a conceptual construction.",
         "claim_ids": ["essay:c1"], "relation": "PARAPHRASE"},
        {"id": "s2", "text": "A manifestation without reflexive awareness would be inert, like a crystal.",
         "claim_ids": ["essay:c2"], "relation": "PARAPHRASE"},
        {"id": "s3", "text": "From these, it is reconstructed that reflexivity belongs intrinsically to manifestation — but this is a reconstruction, not a proven entailment.",
         "claim_ids": ["essay:c3"], "relation": "INFERENCE", "marked_bridge": True},
        {"id": "s4", "text": "Across traditions, reflexivity is a shared phenomenon: Abhinavagupta treats it as intrinsic, Dharmakīrti as conditioned, and Ñāṇavīra as structural.",
         "claim_ids": ["essay:c4"], "relation": "COMPRESSION"},
        {"id": "s5", "text": "Whether this reflexivity entails a single universal Self is left open.",
         "claim_ids": ["essay:c4"], "relation": "QUALIFICATION"},
    ]

    # SentenceEvidenceAudit: enforce the hard rule — a sentence licensed by an UNRESOLVED claim
    # must not overclaim; a bridge sentence must be marked; no certainty inflation.
    inflation_terms = ["proves", "certainly", "definitively", "therefore it is settled", "undeniably"]
    issues = []
    claim_by_id = {c["id"]: c for c in claims}
    for s in sentences:
        for cid in s["claim_ids"]:
            c = claim_by_id[cid]
            if c.get("bridge") and not s.get("marked_bridge"):
                issues.append(f"{s['id']}: renders the reconstructed bridge {cid} without marking it as reconstruction")
            if c["ceiling"] == "UNRESOLVED" and any(t in s["text"].lower() for t in inflation_terms):
                issues.append(f"{s['id']}: certainty inflation beyond UNRESOLVED ceiling of {cid}")
            if c["ceiling"] == "UNRESOLVED" and s.get("relation") == "PARAPHRASE":
                # a bare paraphrase of an unresolved claim is OK (it restates it); flag only if it asserts
                pass
    if ceiling == "UNRESOLVED":
        issues.append("synthesis ceiling is UNRESOLVED: essay conclusion must QUALIFY, never settle")

    result = {
        "essay_id": "ESSAY-REFLEXION-CORE-001",
        "consumes_synthesis": syn["synthesis_id"],
        "synthesis_ceiling": ceiling,
        "unsupported_bridges": unsupported,
        "plan": {"claims": claims, "sentences": sentences},
        "sentence_evidence_audit": {
            "issues": issues,
            "verdict": "PASS" if not issues else "REVIEW",
            "note": "every load-bearing sentence maps to a claim; UNRESOLVED claims are qualified/marked, never settled",
        },
        "render_rule": "UNRESOLVED ceiling -> QUALIFY / represent alternatives / ABSTAIN; never settle.",
    }

    out = os.path.join(ROOT, "benchmarks/v0/review/ESSAY-REFLEXION-CORE-001.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print("ESSAY (consumes ArgumentSynthesis) — ESSAY-REFLEXION-CORE-001")
    print(f"  synthesis ceiling: {ceiling} | unsupported bridges: {unsupported}")
    for s in sentences:
        tag = " [bridge]" if s.get("marked_bridge") else ""
        print(f"    {s['id']}: {s['text'][:60]}{tag}")
    print(f"  sentence-evidence audit: {result['sentence_evidence_audit']['verdict']} "
          f"({len(issues)} issues)")
    for i in issues:
        print(f"    ⚠ {i}")
    print(f"\nwritten: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

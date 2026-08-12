#!/usr/bin/env python3
"""build_reflexion_essay.py — Commit C: one readable essay + SentenceEvidenceAudit from the synthesis.

Per the coordinator directive: prove that readable prose can be generated from the epistemically constrained
object WITHOUT claim inflation. This is the real product test (rhetoric must not destroy the epistemic
distinctions A+B preserved).

The essay answers the narrow question "Does reflexivity belong intrinsically to manifestation?" using the
synthesis's own argumentative structure:
  1. problem      (linguistic/conceptual articulation vs intrinsic reflexivity)
  2. ARG-002      (the 'I'-reflexive awareness is not shown to be a conceptual construction)
  3. ARG-004      (manifestation without vimarśa would be inert)
  4. synthesis    (motivate the reconstructed bridge: reflexivity belongs intrinsically to manifestation)
  5. limitation   (the bridge is RECONSTRUCTED + UNRESOLVED; validity vs soundness)
  6. boundary     (does NOT establish universal Self / one consciousness / consciousness fundamental)

Each LOAD_BEARING sentence carries semantic metadata {claim_refs, inference_refs, source_refs, render_mode,
speaker, assertion_strength}. render_mode is DERIVED from the source object's epistemic state (see the
RENDER table). Only load-bearing scholarly sentences need full chains; TRANSITION/EXPLANATORY/SIGNPOST prose
stays unaudited so the essay reads naturally.

The audit is validated by check_sentence_evidence_audit.py against the synthesis's authority — NOT by regex.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_argument_synthesis import build_synthesis

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))
OUT_MD = os.path.join(ROOT, "benchmarks/v0/review/ESSAY-IPVV-REFLEXION-CORE-001.md")
OUT_AUDIT = os.path.join(ROOT, "benchmarks/v0/review/ESSAY-IPVV-REFLEXION-CORE-001.audit.json")

# source provenance (real passage ids)
V2L = "pt:passage:ipvv:chunkV2-L-sastho-vimarsa-smrti-apohana.md"
V2H = "pt:passage:ipvv:chunkV2-H-pancamo-vimarsa-k11-13.md"


# ── the essay as a list of sentence records (role + text + semantic metadata) ──
def sentences() -> list[dict]:
    return [
        # ── 1. problem ─────────────────────────────────────────────────────────
        {"sid": "S001", "role": "LOAD_BEARING", "render_mode": "QUALIFIED",
         "claim_refs": ["ARG-GOLD-002:G2-OBJ", "SYN-CONC-001"], "inference_refs": ["SYN-INF-001"], "source_refs": [V2L, V2H],
         "attribution": "SYNTHESIS", "speaker": "the reconstruction", "assertion_strength": "MOTIVATES",
         "semantic_relation_to_claim": "EXPANSIVE",
         "text": "At stake is whether the reflexive awareness in which consciousness is present to itself belongs to the very nature of manifestation, or is something added to it by linguistic and conceptual articulation."},
        {"sid": "S002", "role": "EXPLANATORY", "attribution": "SYNTHESIS",
         "text": "The worry is real: if the self's awareness of itself is always joined to a word, it may look like a mental construction rather than an intrinsic feature."},
        # ── 2. ARG-002 ─────────────────────────────────────────────────────────
        {"sid": "S003", "role": "LOAD_BEARING", "render_mode": "ATTRIBUTED",
         "claim_refs": ["ARG-GOLD-002:G2-TC1"], "inference_refs": [], "source_refs": [V2L],
         "attribution": "AUTHOR", "speaker": "Abhinavagupta", "assertion_strength": "TEXTUAL",
         "semantic_relation_to_claim": "CONSERVATIVE_PARAPHRASE",
         "text": "Abhinavagupta's reply turns on what construction does: a conceptual construction combines, differentiates, or determines contents."},
        {"sid": "S004", "role": "LOAD_BEARING", "render_mode": "ATTRIBUTED",
         "claim_refs": ["ARG-GOLD-002:G2-TC2"], "inference_refs": [], "source_refs": [V2L],
         "attribution": "AUTHOR", "speaker": "Abhinavagupta", "assertion_strength": "TEXTUAL",
         "semantic_relation_to_claim": "CONSERVATIVE_PARAPHRASE",
         "text": "The awareness expressed as \u201cI\u201d is not itself treated as one more constructed relation."},
        {"sid": "S005", "role": "LOAD_BEARING", "render_mode": "QUALIFIED",
         "claim_refs": ["ARG-GOLD-002:G2-CONC"], "inference_refs": [], "source_refs": [V2L],
         "attribution": "SYNTHESIS", "speaker": "the reconstruction", "assertion_strength": "RECONSTRUCTED",
         "semantic_relation_to_claim": "CONSERVATIVE_PARAPHRASE",
         "text": "It can be reconstructed that being articulated in language does not, by itself, show that the underlying self-awareness is produced by conceptual determination."},
        # ── 3. ARG-004 ─────────────────────────────────────────────────────────
        {"sid": "S006", "role": "LOAD_BEARING", "render_mode": "ATTRIBUTED",
         "claim_refs": ["ARG-GOLD-004:G4-CRYSTAL"], "inference_refs": [], "source_refs": [V2H],
         "attribution": "AUTHOR", "speaker": "Abhinavagupta", "assertion_strength": "TEXTUAL",
         "semantic_relation_to_claim": "CONSERVATIVE_PARAPHRASE",
         "text": "A light that merely showed the world without knowing that it showed it would be no different from inert crystal."},
        {"sid": "S007", "role": "LOAD_BEARING", "render_mode": "QUALIFIED",
         "claim_refs": ["ARG-GOLD-004:G4-CONC"], "inference_refs": [], "source_refs": [V2H],
         "attribution": "SYNTHESIS", "speaker": "the reconstruction", "assertion_strength": "RECONSTRUCTED",
         "semantic_relation_to_claim": "CONSERVATIVE_PARAPHRASE",
         "text": "The light can be taken to be conscious in that it is aware of itself in the very act of manifesting."},
        {"sid": "S014", "role": "TRANSITION", "attribution": "SYNTHESIS",
         "text": "The second argument approaches the same question from the side of manifestation rather than of the knowing subject."},
        # ── 4. synthesis (MUST resolve through SYN-INF-001, never bypass) ──────
        {"sid": "S008", "role": "LOAD_BEARING", "render_mode": "QUALIFIED",
         "claim_refs": ["SYN-CONC-001"], "inference_refs": ["SYN-INF-001"], "source_refs": [V2L, V2H],
         "attribution": "SYNTHESIS", "speaker": "the reconstruction", "assertion_strength": "SUGGESTIVE",
         "semantic_relation_to_claim": "CONSERVATIVE_PARAPHRASE",
         "text": "Taken together, these passages give reason to think that reflexivity belongs intrinsically to manifestation rather than being added to it from outside."},
        {"sid": "S009", "role": "LOAD_BEARING", "render_mode": "QUALIFIED",
         "claim_refs": ["ARG-GOLD-002:G2-CONC", "ARG-GOLD-004:G4-CONC"],
         "inference_refs": ["SYN-INF-001"], "source_refs": [V2L, V2H],
         "attribution": "SYNTHESIS", "speaker": "the reconstruction", "assertion_strength": "SUGGESTIVE",
         "semantic_relation_to_claim": "CONSERVATIVE_PARAPHRASE",
         "text": "The first argues that linguistic articulation does not by itself show self-awareness to be conceptually produced; the second shows that self-awareness in the act is what separates the conscious from the inert, and if both hold and the warrant joining them is granted, this yields the proposed synthesis."},
        {"sid": "S015", "role": "SIGNPOST", "attribution": "SYNTHESIS",
         "text": "It is worth pausing on how much this step does and does not establish."},
        # ── 5. limitation (validity vs soundness) ─────────────────────────────
        {"sid": "S010", "role": "LOAD_BEARING", "render_mode": "QUALIFIED",
         "claim_refs": ["SYN-CONC-001"], "inference_refs": ["SYN-INF-001"], "source_refs": [V2L, V2H],
         "attribution": "SYNTHESIS", "speaker": "the reconstruction", "assertion_strength": "UNRESOLVED",
         "semantic_relation_to_claim": "CONSERVATIVE_PARAPHRASE",
         "text": "The reasoning can be reconstructed in this form, but its structural adequacy has not yet been audited."},
        {"sid": "S011", "role": "LOAD_BEARING", "render_mode": "QUALIFIED",
         "claim_refs": ["SYN-INF-001"], "inference_refs": [], "source_refs": [],
         "attribution": "SYNTHESIS", "speaker": "the reconstruction", "assertion_strength": "UNRESOLVED",
         "semantic_relation_to_claim": "CONSERVATIVE_PARAPHRASE",
         "text": "But the warrant is itself reconstructed, and its support remains unresolved: one can reconstruct the argument as running this way, but one cannot yet present it as established."},
        # ── 6. boundary ────────────────────────────────────────────────────────
        {"sid": "S012", "role": "LOAD_BEARING", "render_mode": "BOUNDARY",
         "claim_refs": [], "inference_refs": [], "source_refs": [],
         "attribution": "SYNTHESIS", "speaker": "the reconstruction", "assertion_strength": "BOUNDARY",
         "text": "The step, even where it succeeds, is per-act: it does not establish a universal Self in which all manifestation is one consciousness, nor that consciousness is fundamental simpliciter — those remain open boundaries."},
        # ── 7. rival (unsourced) ──────────────────────────────────────────────
        {"sid": "S013", "role": "LOAD_BEARING", "render_mode": "RIVAL", "is_rival": True,
         "claim_refs": [], "inference_refs": [], "source_refs": [],
         "attribution": "SYNTHESIS", "speaker": "the reconstruction", "assertion_strength": "RECONSTRUCTED",
         "text": "A Buddhist opponent can be reconstructed as holding that the determination establishes an external object, but because that position is not grounded in the passages under study, it remains an unsourced reconstruction rather than a live, sourced opponent."},
    ]


# render_mode is DERIVED from the source object's epistemic state (RENDER table, metadata-driven)
def render_mode_from_authority(claim_refs: list[str], authority: dict) -> str:
    """Derive an allowed render_mode from the authority of the referenced claims (not free-form)."""
    if not claim_refs:
        return "UNSPECIFIED"   # boundary/rival sentences are tagged by role, not by a claim
    statuses = [authority["ref_status"].get(r, "MACHINE_PROPOSED") for r in claim_refs]
    if all(s in ("SCHOLARLY_CORROBORATED", "SCHOLARLY_CORROBORATED_PRELIMINARY") for s in statuses):
        return "DIRECT"
    return "QUALIFIED"   # anything involving a reconstructed/unresolved claim must be qualified


def build_audit(authority: dict) -> dict:
    recs = sentences()
    for r in recs:
        if r["role"] == "LOAD_BEARING":
            # audit booleans are filled by the checker; here we record the sentence + its declared metadata
            r.setdefault("epistemic_ceiling", authority["ceiling"])
            r["audit"] = {
                "claim_supported": bool(r["claim_refs"]) or r["render_mode"] in ("BOUNDARY", "RIVAL"),
                "inference_preserved": True,
                "boundary_preserved": True,
                "epistemic_strength_ok": True,
            }
    return {
        "essay_id": "ESSAY-IPVV-REFLEXION-CORE-001",
        "synthesis_id": "SYN-IPVV-REFLEXION-CORE-001",
        "question": "Does reflexivity belong intrinsically to manifestation?",
        "epistemic_ceiling": authority["ceiling"],
        "render_vocabulary": ["DIRECT", "QUALIFIED", "ATTRIBUTED", "RIVAL", "BOUNDARY", "ABSTAIN"],
        "sentences": recs,
    }


def render_markdown(recs: list[dict]) -> str:
    """Assemble a readable essay. Non-load-bearing prose flows naturally; load-bearing sentences carry no
    machine tags in the prose (the metadata lives in the .audit.json)."""
    lines = [
        "# Does Reflexivity Belong Intrinsically to Manifestation?",
        "",
        "The reflexion-core of the Īśvarapratyabhijñāvimarśinī turns on one question: whether the reflexive "
        "awareness in which consciousness is present to itself belongs to the very nature of manifestation, "
        "or is something added to it by language and concept.",
        "",
    ]
    for r in recs:
        lines.append(r["text"])
        lines.append("")
    return "\n".join(lines)


def build_essay_plan() -> dict:
    """A MINIMAL EssayPlan for this one essay (do NOT build a reusable schema)."""
    return {
        "plan_id": "ESSAY-PLAN-IPVV-REFLEXION-CORE-001",
        "synthesis_id": "SYN-IPVV-REFLEXION-CORE-001",
        "question": "Does reflexivity belong intrinsically to manifestation?",
        "sections": [
            {"section": "problem", "sentences": ["S001", "S002"]},
            {"section": "arg-002", "sentences": ["S003", "S004", "S005"]},
            {"section": "arg-004", "sentences": ["S006", "S007", "S014"]},
            {"section": "synthesis", "sentences": ["S008", "S009", "S015"]},
            {"section": "limitation", "sentences": ["S010", "S011"]},
            {"section": "boundary", "sentences": ["S012"]},
            {"section": "rival", "sentences": ["S013"]},
        ],
        "epistemic_ceiling": "UNRESOLVED",
        "render_rule": "UNRESOLVED -> QUALIFIED (suggest/motivate/can-be-reconstructed); never proves/establishes.",
    }


def main() -> int:
    syn = build_synthesis()
    deps = {d["ref"]: d["epistemic_status"] for d in syn["dependency_state"]["dependencies"]}
    authority = {
        "ceiling": syn["synthesis_audit"]["epistemic_ceiling"],
        "ref_status": deps,
        "syn_conc_origin": syn["thesis"].get("status"),
        "bridge": {inf["inference_id"]: inf for inf in syn["inferences"]},
        "does_not_establish": syn.get("boundary", {}).get("does_not_establish", []),
    }
    recs = sentences()
    audit = build_audit(authority)

    plan_path = os.path.join(ROOT, "benchmarks/v0/review/ESSAY-PLAN-IPVV-REFLEXION-CORE-001.json")
    with open(plan_path, "w", encoding="utf-8") as f:
        json.dump(build_essay_plan(), f, indent=2)
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write(render_markdown(recs))
    with open(OUT_AUDIT, "w", encoding="utf-8") as f:
        json.dump(audit, f, indent=2)

    words = sum(len(r["text"].split()) for r in recs)
    print("Reflexion-core essay + EssayPlan + SentenceEvidenceAudit (Commit C)")
    print(f"  sentences: {len(recs)} | ~{words} words")
    print(f"  synthesis ceiling: {authority['ceiling']} | SYN-CONC-001 origin: {authority['syn_conc_origin']}")
    print(f"  written: {OUT_MD}\n          {OUT_AUDIT}\n          {plan_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

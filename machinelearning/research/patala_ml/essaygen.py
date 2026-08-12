"""patala_ml/essaygen.py — the CL-3 gold-chain essay generator.

The pipeline (from the review):
  ACCEPTED THEME → ACCEPTED ARGUMENT GRAPH → ESSAY PLAN → ATOMIC ESSAY CLAIMS
  → CLAIM VALIDATION → SENTENCE DRAFTING → SENTENCE→CLAIM ALIGNMENT
  → SEMANTIC VERIFICATION → BOUNDARY CHECK → PROVENANCE WALK → MARKDOWN RENDER

The hard invariant:
  A sentence cannot introduce a proposition that does not exist in its linked EssayClaim(s).
  TRANSITION is the only exception, and even those are non-substantive.

The generator WRITES prose (model-draftable) but the CLAIM GRAPH CONSTRAINS content and the
VERIFIER (essayverify.py, independent) decides what survives. This generator produces the
MODEL_PROPOSED sentences; the verifier promotes/ rejects.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .essay import Essay, plan_hash
from .essaysentence import EssaySentence


def freeze_claims(plan, argument) -> list[dict]:
    """Freeze the atomic EssayClaims from the plan + argument (BEFORE prose).

    Each claim: id, text, role (premise/conclusion/QUALIFICATION), argument_id, passage_ids,
    boundary (the local epistemic limit), provenance targets (resolved recursively).
    """
    claims = []
    # the premises become EVIDENCED claims (licensed by their passages)
    for i, m in enumerate(argument.members):
        if m.role == "NIGAMANA":
            continue
        passage_ids = [p for p in m.passage_ids if p]
        if not passage_ids and i < len(argument.premise_claims):
            passage_ids = [t["target_id"] for t in argument.premise_claims[i].argument_targets]
        claims.append({
            "id": f"EC-{len(claims)+1:03d}",
            "text": m.text,
            "role": "premise",
            "argument_id": argument.argument_id,
            "passage_ids": passage_ids,
            "boundary": "licensed by the cited passages; does not by itself exceed them",
            "type": "EVIDENCED",
        })
    # the conclusion (NIGAMANA) → the thesis claim, WITH the honest boundary
    conc_text = argument.conclusion.text if argument.conclusion else argument.title
    claims.append({
        "id": f"EC-{len(claims)+1:03d}",
        "text": conc_text,
        "role": "conclusion",
        "argument_id": argument.argument_id,
        "passage_ids": [p for p in (argument.conclusion.passage_ids if argument.conclusion else []) if p],
        "boundary": "This argument establishes a structural requirement; it does not by itself "
                    "establish the stronger identity of the support with a universal Self.",
        "type": "EVIDENCED",
    })
    # an explicit QUALIFICATION claim (the essay actively tells the reader the limit)
    claims.append({
        "id": f"EC-{len(claims)+1:03d}",
        "text": "The argument therefore establishes a structural requirement, not yet the full "
                "metaphysical identity claimed elsewhere in the work.",
        "role": "QUALIFICATION",
        "argument_id": argument.argument_id,
        "passage_ids": [],
        "boundary": "the honest limit, visible to the reader",
        "type": "SYNTHETIC",
    })
    return claims


def _claim_license(claim: dict) -> list[str]:
    """The passage_ids a claim licenses (its evidence)."""
    return claim.get("passage_ids", [])


def draft_sentences(claims: list[dict], argument) -> list[EssaySentence]:
    """Draft MODEL_PROPOSED sentences, each licensed by ≥1 claim.

    Each premise claim gets an EVIDENCED sentence (PARAPHRASE/COMPRESSION of its licensed
    content). The conclusion gets an INFERENCE sentence (licensed by the argument). The
    QUALIFICATION gets a QUALIFICATION sentence. Transitions are non-substantive.
    """
    sentences = []
    # EVIDENCED premise sentences (PARAPHRASE — same content, restated)
    for c in claims:
        if c["role"] != "premise":
            continue
        sentences.append(EssaySentence(
            id=f"S-{len(sentences)+1:03d}",
            text=c["text"],                    # restate the licensed claim (the content is frozen)
            claim_ids=[c["id"]],
            provenance_relation="PARAPHRASE",
            argument_ids=[c["argument_id"]],
            passage_ids=_claim_license(c),
        ))
    # the conclusion (INFERENCE — derived from the premises, licensed by the argument)
    concl = next(c for c in claims if c["role"] == "conclusion")
    sentences.append(EssaySentence(
        id=f"S-{len(sentences)+1:03d}",
        text=concl["text"],
        claim_ids=[concl["id"]],
        provenance_relation="INFERENCE",
        argument_ids=[concl["argument_id"]],
        passage_ids=_claim_license(concl),
    ))
    # the QUALIFICATION
    qual = next(c for c in claims if c["role"] == "QUALIFICATION")
    sentences.append(EssaySentence(
        id=f"S-{len(sentences)+1:03d}",
        text=qual["text"],
        claim_ids=[qual["id"]],
        provenance_relation="QUALIFICATION",
        argument_ids=[qual["argument_id"]],
        passage_ids=[],
    ))
    return sentences


def generate_essay(plan, argument, essay_id: str, title: str) -> Essay:
    """Generate the canonical Essay from a frozen EssayPlan + accepted argument."""
    claims = freeze_claims(plan, argument)
    plan_dict = {"plan_id": plan.plan_id, "thesis": plan.thesis,
                 "claims": [c["text"] for c in claims]}
    essay = Essay(
        essay_id=essay_id, plan_id=plan.plan_id, plan_hash=plan_hash(plan_dict),
        theme_id=plan.theme, title=title, claims=claims,
    )
    for s in draft_sentences(claims, argument):
        essay.add_sentence(s)
    return essay

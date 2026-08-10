"""Pāṭala passage-record schema.

The machine shape every pipeline stage writes into. Mirrors the house contract
(docs/TRANSLATION_SCHEMA.md) and maps 1:1 to the existing T1/T2/T3/C1 markdown.
Versioned 1.0.0.

Each stage (T1 → R1 → T2 → R2 → T3 → T3.1 → C1) appends its layer to this record.
The audit checker (audit.py) validates it at every level.
"""
from __future__ import annotations
from typing import Any, Optional

# The pipeline stages, in order. T3.1 is derived from T3 (in lock-step).
STAGES = ["T1", "R1", "T2", "R2", "T3", "T3.1", "C1"]

# The [G]/[P]/[A]/[R] justification codes (PASS_PROTOCOL.md §2)
JUSTIFICATION_CODES = ("G", "P", "A", "R")

# The R1 verdicts (R1_CONTENT_ENGINEERING.md)
R1_VERDICTS = ("RIGHT", "ERROR", "FORK", "OPEN")

# The typed ambiguity flags (TRANSLATION_SCHEMA.md) + the legacy house [X]
# (provisional / corrupt / unresolved — PASS_PROTOCOL.md status vocabulary).
FLAGS = ("TXT", "GRAM", "LEX", "DOCT", "WIT", "SUP", "X")

# The audit dimensions (per-dimension, not scalar confidence)
ASSESSMENT_DIMS = ("textual", "grammatical", "lexical", "interpretive")
ASSESSMENT_STATES = ("secure", "ambiguous", "uncertain", "moderate")

# Parallel kinds (TRANSLATION_SCHEMA.md)
PARALLEL_KINDS = (
    "exact_quote", "probable_quote", "adaptation", "formulaic_parallel",
    "lexical_parallel", "syntactic_parallel", "conceptual_parallel",
)


def new_passage(work_id: str, chapter: int, verse: int, sanskrit: str,
                edition: str, source_file: str, source_id: str = "",
                locator: str | None = None) -> dict[str, Any]:
    """A blank, schema-valid passage record.

    Separates the three dimensions the review flagged (scoped to versions):
      pipeline_stage    where in the flow (T1 → R1 → ... → C1) — null until a stage runs
      origin            who produced it (machine / human) — on each version
      editorial_status  proposed / reviewed / accepted — on each version, set only
                        by a scoped ReviewEvent
    """
    locator = locator or f"{chapter}.{verse}"
    src_id = source_id or edition
    return {
        "passage_id": f"tantra:text:{work_id}:{chapter}.{verse}",
        "work_id": work_id,
        "location": {"chapter": chapter, "verse": verse, "locator": locator},
        "source": {
            "source_id": src_id,
            "source_edition": edition,
            "source_file": source_file,
            "source_text": sanskrit,
        },
        # first-class source spans (the passage may appear differently across witnesses)
        "source_spans": [
            {"source_id": src_id, "locator": locator, "text": sanskrit,
             "relationship": "canonical"}
        ],
        "stages": {},          # stage -> CURRENT version's payload
        "versions": {},        # stage -> [all versions] (never overwrite)
        "audit": {},           # stage -> audit report
        "lineage": [],         # [{stage, version, created_by, derived_from, at}]
        "policy": {
            "translation_contract": "1.0.0",
            "style_guide": "1.0.0",
            "schema": "1.1.0",
        },
        "pipeline_stage": None,   # null until a stage has run (not "T1" before T1 exists)
        "origin": "machine",
        "editorial_status": "proposed",
        "review_events": [],   # scoped ReviewEvents (added by set_review)
    }


# ── the per-stage payload shapes ────────────────────────────────────────────

def stage_T1(close: str, reader_draft: str = "", flags: Optional[list] = None,
             notes: Optional[list] = None, lexical_decisions: Optional[list] = None,
             grammatical_notes: Optional[list] = None, parallels: Optional[list] = None,
             time_place_context: Optional[dict] = None) -> dict[str, Any]:
    """T1: one careful working translation + evidence + the required header."""
    return {
        "close_translation": close,
        "reader_draft": reader_draft,
        "flags": [f for f in (flags or []) if f in FLAGS],
        "notes": notes or [],
        "lexical_decisions": lexical_decisions or [],
        "grammatical_notes": grammatical_notes or [],
        "parallels": parallels or [],
        "time_place_context": time_place_context or {},
        "stage": "T1",
    }


R1_CRUX_TYPES = ("LEXICAL", "GRAMMATICAL", "TEXTUAL", "REFERENTIAL", "DOCTRINAL", "CONTEXTUAL")
R2_DECISIONS = ("CONSTRAINED", "PREFERRED", "OPEN", "RECONSTRUCTED")


def stage_R1(detail: str, anchor_quote: str = "",
             source: str = "", verdicts: Optional[list] = None,
             cruxes: Optional[list] = None) -> dict[str, Any]:
    """R1: the adversarial critique (machine pass, NOT human peer review). Maps the
    genuine cruxes (id/type/assumption/rivals/evidence-needed), gives verdicts
    (RIGHT/ERROR/FORK/OPEN), and leaves commentary stubs."""
    verdicts = verdicts or []
    for v in verdicts:
        if v.get("verdict") not in R1_VERDICTS:
            raise ValueError(f"R1 verdict must be one of {R1_VERDICTS}, got {v.get('verdict')!r}")
    for c in cruxes or []:
        if c.get("type") and c["type"] not in R1_CRUX_TYPES:
            raise ValueError(f"R1 crux type must be one of {R1_CRUX_TYPES}, got {c.get('type')!r}")
    return {"detail": detail, "anchor_quote": anchor_quote,
            "source": source, "verdicts": verdicts, "cruxes": cruxes or [],
            "stage": "R1"}


def stage_T2(close: str, strategy: str = "", rival_decisions: Optional[list] = None,
             constrained: Optional[list] = None) -> dict[str, Any]:
    """T2: the strongest materially-different defensible rival. SEES T1 + R1.
    Differs only where it changes syntax/referent/technical sense/doctrine/text/
    meaningful interpretation; marks source-constrained readings CONSTRAINED.
    `rival_decisions` = [{crux_id, adopted, differs_from_t1, reason, evidence}]
    `constrained` = [crux_id] that had no defensible alternative (kept T1)."""
    return {"close_translation": close, "strategy": strategy,
            "rival_decisions": rival_decisions or [], "constrained": constrained or [],
            "stage": "T2"}


def stage_R2(chosen: str, reasoning: str, rejected: Optional[list] = None,
             commentary: str = "", hard_core: str = "",
             divergence: str = "", readability: str = "",
             school_context: str = "", equal_alternates: Optional[list] = None,
             is_open: bool = False, decisions: Optional[list] = None) -> dict[str, Any]:
    """R2: the adjudication. Compares T1-vs-T2 BY DECISION, not just prose.
    hard_core = agreement + source-constrained. `decisions` is a list of
    {crux_id, preferred, status: CONSTRAINED|PREFERRED|OPEN|RECONSTRUCTED, reason, evidence}."""
    for d in decisions or []:
        if d.get("status") and d["status"] not in R2_DECISIONS:
            raise ValueError(f"R2 decision status must be one of {R2_DECISIONS}, got {d.get('status')!r}")
    return {"chosen": chosen, "reasoning": reasoning,
            "rejected": rejected or [], "commentary": commentary,
            "hard_core": hard_core, "divergence": divergence,
            "readability": readability, "school_context": school_context,
            "equal_alternates": equal_alternates or [], "is_open": is_open,
            "decisions": decisions or [], "stage": "R2"}


def stage_T3(resolved: str, open_flags: Optional[list] = None,
             editorial_notes: Optional[list] = None) -> dict[str, Any]:
    """T3: the final resolved text."""
    return {"resolved": resolved, "open_flags": open_flags or [],
            "editorial_notes": editorial_notes or [], "stage": "T3"}


def stage_T31(reading: str) -> dict[str, Any]:
    """T3.1: the natural-English reading layer, derived from T3 (in lock-step)."""
    return {"reading": reading, "stage": "T3.1"}


C1_EVIDENCE_STATES = ("C1_EVIDENCE_COMPLETE", "C1_EVIDENCE_PARTIAL")


def stage_C1(interpretation: str, challenges: Optional[list] = None,
             c1_id: str = "", derived_from_t3: str = "",
             evidence_state: str = "C1_EVIDENCE_PARTIAL",
             evidence: Optional[list] = None,
             open_questions: Optional[list] = None,
             proposals: Optional[list] = None,
             cruxes: Optional[list] = None) -> dict[str, Any]:
    """C1: the capstone scholarly commentary (per skills/write-commentary).

    - interpretation  the commentary prose
    - challenges      TranslationChallenges (C1 may challenge T3 but never mutate it)
    - evidence_state  C1_EVIDENCE_COMPLETE | C1_EVIDENCE_PARTIAL
    - evidence        [{id, what_it_supports}] — stable passage/resource ids
    - open_questions  explicit unresolved points
    - proposals       structured PROPOSALS (TermHistoryAssertion, ParallelAssertion,
                      TranslationChallenge, ...) — origin machine, status proposed
    """
    if evidence_state not in C1_EVIDENCE_STATES:
        raise ValueError(f"evidence_state must be one of {C1_EVIDENCE_STATES}, got {evidence_state!r}")
    return {"interpretation": interpretation,
            "challenges": challenges or [],
            "c1_id": c1_id,
            "derived_from_t3": derived_from_t3,
            "evidence_state": evidence_state,
            "evidence": evidence or [],
            "open_questions": open_questions or [],
            "proposals": proposals or [],
            "cruxes": cruxes or [],
            "stage": "C1"}


def set_stage(record: dict[str, Any], payload: dict[str, Any],
              created_by: str, derived_from: Optional[str] = None,
              supersedes: Optional[str] = None) -> dict[str, Any]:
    """Attach a stage payload WITHOUT overwriting prior versions. Every write is a
    new version; `stages` points at the current one and `versions` keeps history.

    stage      the floor (T1/R1/T2/R2/T3/T3.1/C1)
    version    an incrementing per-stage counter
    origin     machine/human — never changed by a machine stage alone
    pipeline_stage + editorial_status are updated here (editorial_status stays
    'proposed' until an actual ReviewEvent promotes it)."""
    stage = payload["stage"]
    versions = record["versions"].setdefault(stage, [])
    version = len(versions) + 1
    v_payload = dict(payload)
    v_payload["version"] = version
    v_payload["supersedes"] = supersedes
    versions.append(v_payload)
    record["stages"][stage] = v_payload  # current pointer
    record["lineage"].append({
        "stage": stage,
        "version": version,
        "created_by": created_by,
        "derived_from": derived_from,
        "supersedes": supersedes,
        "origin": payload.get("origin", "machine"),
    })
    record["pipeline_stage"] = stage
    # origin: a machine stage writes machine origin; do NOT promote editorial_status
    record["origin"] = payload.get("origin", record.get("origin", "machine"))
    return record


REVIEW_TYPES = ("TEXTUAL", "GRAMMATICAL", "LEXICAL", "TRANSLATIONAL",
                "HISTORICAL", "DOCTRINAL", "READABILITY", "MANUSCRIPT")


def set_review(record: dict[str, Any], review: dict[str, Any]) -> dict[str, Any]:
    """Record a SCOPED ReviewEvent on a specific target/version. Only this promotes
    a version's editorial_status to 'reviewed'. Machine stages NEVER set it.

    Required: target_stage, target_version, reviewer, review_type, scope, outcome, reason.
    An 'accept' → that target/version is reviewed (not the whole passage). 'accepted'
    is an editorial promotion issued separately (promote_version)."""
    n = len(record["review_events"]) + 1
    review.setdefault("id", f"review:{record.get('passage_id','?')}:{n}")
    review.setdefault("target_id", record.get("passage_id"))
    if not review.get("target_stage") or not review.get("target_version"):
        raise ValueError("a ReviewEvent must target a specific version (target_stage + target_version)")
    if review.get("review_type") not in REVIEW_TYPES:
        raise ValueError(f"review_type must be one of {REVIEW_TYPES}, got {review.get('review_type')!r}")
    record["review_events"].append(review)

    # mark the targeted version reviewed
    for v in record["versions"].get(review["target_stage"], []):
        if v.get("version") == review.get("target_version"):
            v["editorial_status"] = "reviewed"
    record["editorial_status"] = _aggregate_review_state(record)
    return record


def promote_version(record: dict[str, Any], stage: str, version: int,
                    reviewer: dict, reason: str = "") -> dict[str, Any]:
    """Editorial promotion: reviewed → accepted (a separate, explicit editor action)."""
    for v in record["versions"].get(stage, []):
        if v.get("version") == version:
            v["editorial_status"] = "accepted"
            v.setdefault("promoted_by", reviewer)
            v.setdefault("promotion_reason", reason)
    record["editorial_status"] = _aggregate_review_state(record)
    return record


def _aggregate_review_state(record) -> str:
    states = {v.get("editorial_status") for versions in record.get("versions", {}).values() for v in versions}
    if not states or states == {"proposed"}:
        return "proposed"
    if "accepted" in states:
        return "mixed" if len(states) > 1 else "accepted"
    if "reviewed" in states:
        return "mixed" if len(states) > 1 else "reviewed"
    return "proposed"


def get_stage(record: dict[str, Any], stage: str) -> Optional[dict[str, Any]]:
    return record["stages"].get(stage)

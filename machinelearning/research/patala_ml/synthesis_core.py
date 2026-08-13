#!/usr/bin/env python3
"""patala_ml/synthesis_core.py — devpath8: the ArgumentSynthesis core (G5B).

The convergence object (the globalplan Phase 8 + the directive). One structured debate object that
essays, education, review, and agent answers all consume.

    ResearchQuestion   what question does the debate answer?
    DebateFrame        the positions + their relationship (the frame)
    Position           a participant stance (ŚAIVA / BUDDHIST / ...)
    ArgumentSynthesis  the parent: question + frame + positions + arguments + relations +
                       cruxes + evidence + open disagreement

Design law (the directive §8, non-negotiable):
    The synthesis is NOT a final-truth object. It says "under DebateFrame DF4: Position A has X/Y,
    Position B has objection Z, decisive crux CRUX-12, evidence status ..., review state ..." — it
    NEVER says CONCLUSION = TRUE. It preserves: speaker identity, argument direction, scope,
    modality, unresolved disagreement, cruxes, counterevidence, source grounding, review status. It
    NEVER manufactures consensus.

The frozen relation vocabulary (my reaction note §4e — the directive uses "ATTACKS" but never defines
it; devpath8 freezes it):
    SUPPORTS · ATTACKS · UNDERPINS · UNDERMINES · REPLIES_TO · RESTRICTS · COMPLEMENTS

Builds on the devpath7 typed contract (BaseScholarlyObject + AuthorityVector) and the devpath4/5
layers (propositions, cruxes).
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from typing import Annotated, Literal, Union

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))

try:
    from pydantic import BaseModel, Field
    _HAS_PYDANTIC = True
except Exception:  # pragma: no cover
    _HAS_PYDANTIC = False

if _HAS_PYDANTIC:
    # the frozen relation vocabulary
    RELATION_VOCABULARY = ("SUPPORTS", "ATTACKS", "UNDERPINS", "UNDERMINES",
                           "REPLIES_TO", "RESTRICTS", "COMPLEMENTS")

    class ResearchQuestion(BaseModel):
        research_question_id: str
        question: str
        works: list[str] = Field(default_factory=list)

    class Position(BaseModel):
        position_id: str
        label: str
        stance: str = ""              # e.g. "ŚAIVA" / "BUDDHIST" / "synthetic"
        speaker_ref: str | None = None
        arguments: list[str] = Field(default_factory=list)   # argument refs held by this position

    class DebateFrame(BaseModel):
        debate_frame_id: str
        research_question_ref: str
        positions: list[Position] = Field(default_factory=list)

    class ArgumentRelation(BaseModel):
        from_ref: str
        to_ref: str
        relation: Literal["SUPPORTS", "ATTACKS", "UNDERPINS", "UNDERMINES",
                          "REPLIES_TO", "RESTRICTS", "COMPLEMENTS"] = "SUPPORTS"

    class ArgumentSynthesis(BaseModel):
        """The structured current-best-understanding of one debate. NOT a truth object."""
        synthesis_id: str
        research_question: ResearchQuestion
        debate_frame: DebateFrame
        arguments: list[str] = Field(default_factory=list)
        relations: list[ArgumentRelation] = Field(default_factory=list)
        cruxes: list[str] = Field(default_factory=list)
        propositions: list[str] = Field(default_factory=list)
        supported_conclusions: list[str] = Field(default_factory=list)
        counterevidence: list[str] = Field(default_factory=list)
        open_questions: list[str] = Field(default_factory=list)
        scope_boundaries: list[str] = Field(default_factory=list)
        unresolved_disagreement: list[str] = Field(default_factory=list)
        source_refs: list[str] = Field(default_factory=list)
        review_status: str = "NOT_REVIEWED"

        def is_truth_asserting(self) -> bool:
            """The honesty check: a synthesis must NEVER assert a single TRUE conclusion."""
            return bool(self.supported_conclusions) and not self.unresolved_disagreement

    # ── the builder ────────────────────────────────────────────────────────────
    def build_synthesis(*, synthesis_id: str, question: ResearchQuestion, frame: DebateFrame,
                        arguments: list[str], relations: list[ArgumentRelation],
                        cruxes: list[str], propositions: list[str],
                        supported_conclusions: list[str], counterevidence: list[str],
                        open_questions: list[str], scope_boundaries: list[str],
                        unresolved_disagreement: list[str], source_refs: list[str] | None = None
                        ) -> ArgumentSynthesis:
        """Assemble one ArgumentSynthesis. It preserves disagreement by construction."""
        return ArgumentSynthesis(
            synthesis_id=synthesis_id, research_question=question, debate_frame=frame,
            arguments=arguments, relations=relations, cruxes=cruxes,
            propositions=propositions, supported_conclusions=supported_conclusions,
            counterevidence=counterevidence, open_questions=open_questions,
            scope_boundaries=scope_boundaries, unresolved_disagreement=unresolved_disagreement,
            source_refs=source_refs or [],
        )
else:  # pragma: no cover
    RELATION_VOCABULARY = ()
    ArgumentSynthesis = None
    ResearchQuestion = None
    DebateFrame = None
    Position = None
    ArgumentRelation = None

    def build_synthesis(**kwargs):  # type: ignore
        return None


def _sha256(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode("utf-8")).hexdigest()


# ── assemble a real synthesis from the gold argument layers (devpath4/5) ──────
def build_synthesis_from_gold(gold: dict, *, synthesis_id: str, research_question: str,
                              works: list[str] | None = None) -> dict | None:
    """Build one ArgumentSynthesis from a gold object's nodes + inferences.

    Positions come from the commitment/speaker of the gold nodes (ŚAIVA asserted vs opponent).
    Cruxes come from the gold's inferences' premise sets (devpath5 perturbation). The synthesis
    preserves disagreement (opponent positions are NOT collapsed into consensus).
    """
    if not _HAS_PYDANTIC:
        return None
    nodes = gold.get("nodes", [])
    inferences = gold.get("inferences", [])

    # derive positions from the commitment vocabulary
    asserted = [n for n in nodes if str(n.get("commitment", "")).upper() in ("ASSERTS", "DERIVES", "SIDDHANTA")]
    opponent = [n for n in nodes if str(n.get("commitment", "")).upper() in ("ATTRIBUTES_TO_OPPONENT", "QUOTES")]
    reconstructed = [n for n in nodes if str(n.get("commitment", "")).upper() in ("RECONSTRUCTED", "EDITORIAL_RATIONAL_RECONSTRUCTION")]

    pos_saiva = Position(position_id="POS-SIDDHANTA", label="Siddhānta (asserted)",
                         stance="ŚAIVA", arguments=[g for g in []])
    positions = [pos_saiva]
    if opponent:
        positions.append(Position(position_id="POS-OPPONENT", label="Opponent",
                                  stance="OPPONENT"))
    if reconstructed:
        positions.append(Position(position_id="POS-RECONSTRUCTED", label="Reconstructed",
                                  stance="RECONSTRUCTED"))

    # arguments = the inferences (each is a local argument), cruxes = their decisive premise sets
    arguments = [inf.get("inference_id") for inf in inferences]
    cruxes = [f"pt:crux:{inf.get('inference_id')}" for inf in inferences]
    # relations: each inference grounds its conclusion (SUPPORTS)
    relations = []
    for inf in inferences:
        for cid in inf.get("conclusion_ids", []):
            relations.append(ArgumentRelation(from_ref=inf.get("inference_id"), to_ref=cid,
                                              relation="SUPPORTS"))
    # propositions = the nodes
    propositions = [n.get("proposition_id") for n in nodes]
    # source grounding
    source_refs = []
    for n in nodes:
        g = n.get("grounding", {}) or {}
        for k in ("passage_id", "c1_id", "span_id"):
            if g.get(k):
                source_refs.append(g[k])
    # disagreement: an opponent position exists => unresolved
    unresolved = ["opponent position present (disagreement preserved)"] if opponent else []

    q = ResearchQuestion(research_question_id=f"RQ-{gold.get('gold_id', 'ARG')}",
                         question=research_question, works=works or [])
    frame = DebateFrame(debate_frame_id=f"DF-{gold.get('gold_id', 'ARG')}",
                        research_question_ref=q.research_question_id, positions=positions)
    synth = build_synthesis(
        synthesis_id=synthesis_id, question=q, frame=frame, arguments=arguments,
        relations=relations, cruxes=cruxes, propositions=propositions,
        supported_conclusions=[], counterevidence=[],
        open_questions=[], scope_boundaries=[],
        unresolved_disagreement=unresolved, source_refs=source_refs,
    )
    return synth.model_dump()


if __name__ == "__main__":
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    from patala_ml.gold002 import build_gold_002

    g = build_gold_002()
    out = build_synthesis_from_gold(
        g, synthesis_id="SYNTH-IPVV-RECOGNITION",
        research_question="Is recognition fundamentally a recollection of an already-existing self?",
        works=["IPK", "IPVV"])
    print(json.dumps(out, indent=2, ensure_ascii=False)[:1500])

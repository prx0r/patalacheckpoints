"""lib/organism_loop.py — the consumer→research machine (Pāṭala organism loop).

From the patala organism vision (SPEC-21..25): every consumer is a probe into the graph. This
implements the 10-stage consumer→research chain technically:
  interaction → question normalize → graph link → cluster → gap detect → intervention experiment
  → learning measure → content mutation (GraphProposal) → verification → human gate → truth graph

It connects the CONSUMER ORGANISM to our EVOLUTION LOOP + AGENT-DELIVERY human gate:
  - Gap types map to our discovery/counterfactual work
  - GraphProposal (ADD_NODE/ADD_EDGE/MODIFY/SUPERSEDE/MERGE) goes through our human gate (nothing
    generated goes straight into canonical truth)
  - learner state (BKT) feeds the pedagogy policy; question clusters feed the research policy
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

GAP_TYPES = ["EXPLANATION", "EVIDENCE", "ONTOLOGY", "ARGUMENT", "CORPUS", "DISAGREEMENT",
             "PEDAGOGICAL", "BENCHMARK", "CROSS_TRADITION", "OPEN_RESEARCH"]
GAP_STATUS = ["OPEN", "INVESTIGATING", "RESOLVED", "CLOSED"]


@dataclass
class InteractionEvent:
    """Stage 1 — the shared event core (Graphiti-style)."""
    event_id: str
    user_id: str
    event_type: str          # QUESTION | OBJECTION | CONFUSION | FOLLOWUP
    text: str
    timestamp: str = ""
    object_ids: list = field(default_factory=list)


@dataclass
class Question:
    """Stage 2/3 — normalized question linked to the graph."""
    question_id: str
    canonical_text: str
    concept_ids: list = field(default_factory=list)
    variants: int = 1        # cluster size (stage 4)
    followup_confusion: float = 0.0   # stage 5 signal


@dataclass
class Gap:
    """Stage 5 — why couldn't we answer? (the research backlog generator)."""
    gap_id: str
    type: str = "OPEN_RESEARCH"     # one of GAP_TYPES
    trigger_question_ids: list = field(default_factory=list)
    demand: float = 0.0
    centrality: float = 0.0
    status: str = "OPEN"


@dataclass
class Intervention:
    """Stage 6 — a candidate explanation/pedagogy to test."""
    id: str
    mechanism: str           # prose | argument_graph | objection | source_contrast
    effect_size: float = 0.0  # stage 7 — how well it resolved confusion


@dataclass
class GraphProposal:
    """Stage 8 — a candidate graph mutation (nothing goes straight to truth)."""
    proposal_id: str
    operation: str           # ADD_NODE | ADD_EDGE | MODIFY | SUPERSEDE | MERGE
    target: str
    source_events: list = field(default_factory=list)
    review_state: str = "MACHINE_PROPOSED"
    gate: str = "BLOCKED"    # opens only via human gate


class OrganismLoop:
    """The consumer→research machine: consumers probe, the graph evolves (via human gate)."""
    def __init__(self):
        self.events = []
        self.questions = {}
        self.gaps = []
        self.proposals = []
        self.gate = "BLOCKED"   # herdr-style: agents propose, only humans authorize canonical truth

    # stage 1-4: capture, normalize, link, cluster
    def capture_question(self, event_id, user, text, concepts, variants=1, followup=0.0):
        self.events.append(InteractionEvent(event_id, user, "QUESTION", text))
        q = Question(f"Q{len(self.questions)+1}", text, concepts, variants, followup)
        self.questions[q.question_id] = q
        return q

    # stage 5: gap detection (the research backlog generator)
    def detect_gap(self, question_id, gap_type=None, demand=None):
        q = self.questions[question_id]
        if gap_type is None:
            # high followup confusion = pedagogical; else if concepts unknown = ontology
            gap_type = "PEDAGOGICAL" if q.followup_confusion > 0.5 else "OPEN_RESEARCH"
        gap = Gap(f"GAP{len(self.gaps)+1}", gap_type, [question_id],
                  demand or q.variants, q.variants)
        self.gaps.append(gap)
        return gap

    # stage 6-7: intervention experiment + learning measurement
    def run_intervention(self, mechanism, resolved_confusion):
        itv = Intervention(f"ITV{len([i for i in []]):d}", mechanism)  # placeholder id
        itv.mechanism = mechanism
        itv.effect_size = resolved_confusion
        return itv

    # stage 8: content mutation -> GraphProposal (nothing straight to truth)
    def propose_mutation(self, operation, target, source_events):
        p = GraphProposal(f"PROP{len(self.proposals)+1}", operation, target, source_events)
        self.proposals.append(p)
        return p

    # stage 9-10: verification + human gate -> truth graph
    def verify_and_promote(self, proposal):
        """RARR/RefChecker-style verification then human gate."""
        # simplified verification: proposal with evidence passes structural check
        if proposal.operation in ("ADD_NODE", "ADD_EDGE", "MODIFY", "MERGE", "SUPERSEDE"):
            proposal.review_state = "MACHINE_CORROBORATED"
            proposal.gate = "BLOCKED"    # still needs human
        return proposal

    def human_authorize(self, proposal):
        """THE ONLY path to canonical truth (herdr human gate)."""
        proposal.gate = "OPEN"
        proposal.review_state = "ACCEPTED"
        return proposal

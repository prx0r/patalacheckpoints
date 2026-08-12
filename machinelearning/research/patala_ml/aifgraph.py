"""patala_ml/aifgraph.py — the AIF-informed argument graph (propositions ≠ inference ≠ conflict).

From the external review (ML-ARGUMENT-REVIEW-CORRECTED.md §6): the mature Argument Interchange
Format separates THREE node types instead of flattening everything into premise[]→conclusion:

  INFORMATION NODE  a proposition / textual assertion (a claim, a premise)
  INFERENCE NODE    why proposition A supposedly licenses B (the scheme, the move)
  CONFLICT NODE     why proposition X challenges Y (objection / rebuttal)

Pāṭala alignment: each node resolves to passages; edges are typed. The graph sits BETWEEN Sanskrit
and Lean — philosophical/defeasible stays in the graph; strictly-formalizable subgraphs may route to
Lean later.

This is judged on STRUCTURAL SOUNDNESS + AUDITABLE GROUNDING, not invented numeric scores.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class InfoNode:
    """An information node: a proposition / assertion, resolvable to passages."""
    id: str
    text: str
    node_type: str = "INFORMATION"     # INFORMATION (a proposition)
    passage_ids: list[str] = field(default_factory=list)
    role: str = "claim"                # claim | premise | conclusion | objection | reply
    explicitness: str = "EXPLICIT"     # EXPLICIT | IMPLICIT (implicit → human review)

    def to_dict(self) -> dict:
        return {"id": self.id, "text": self.text, "node_type": self.node_type,
                "passage_ids": self.passage_ids, "role": self.role,
                "explicitness": self.explicitness}


@dataclass
class InferenceNode:
    """An inference node: WHY proposition A licenses B (the scheme / the move)."""
    id: str
    scheme: str            # TRANSCENDENTAL | REDUCTIO | ANALOGY | ENTAILMENT | PRESUPPOSITION
    premise_ids: list[str] = field(default_factory=list)
    conclusion_id: str = ""
    passage_ids: list[str] = field(default_factory=list)   # where the move is grounded

    def to_dict(self) -> dict:
        return {"id": self.id, "scheme": self.scheme, "premise_ids": self.premise_ids,
                "conclusion_id": self.conclusion_id, "passage_ids": self.passage_ids}


@dataclass
class ConflictNode:
    """A conflict node: WHY proposition X challenges Y (objection / rebuttal)."""
    id: str
    type: str                      # OBJECTION | REBUTTAL | QUALIFICATION
    source_id: str                 # the proposition being challenged
    target_id: str                 # the proposition challenged
    text: str = ""
    passage_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"id": self.id, "type": self.type, "source_id": self.source_id,
                "target_id": self.target_id, "text": self.text, "passage_ids": self.passage_ids}


@dataclass
class ArgumentGraph:
    """The AIF-informed argument graph for one argument."""
    argument_id: str
    work_id: str
    info_nodes: list[InfoNode] = field(default_factory=list)
    inference_nodes: list[InferenceNode] = field(default_factory=list)
    conflict_nodes: list[ConflictNode] = field(default_factory=list)

    def add_info(self, **kw) -> str:
        n = InfoNode(**kw)
        self.info_nodes.append(n)
        return n.id

    def add_inference(self, scheme: str, premise_ids: list[str], conclusion_id: str,
                      passage_ids: list[str] | None = None) -> str:
        nid = f"{self.argument_id}:inf:{len(self.inference_nodes) + 1}"
        self.inference_nodes.append(InferenceNode(
            id=nid, scheme=scheme, premise_ids=premise_ids, conclusion_id=conclusion_id,
            passage_ids=passage_ids or []))
        return nid

    def add_conflict(self, type_: str, source_id: str, target_id: str,
                     text: str = "", passage_ids: list[str] | None = None) -> str:
        nid = f"{self.argument_id}:con:{len(self.conflict_nodes) + 1}"
        self.conflict_nodes.append(ConflictNode(
            id=nid, type=type_, source_id=source_id, target_id=target_id,
            text=text, passage_ids=passage_ids or []))
        return nid

    # ── structural soundness checks (NOT invented metrics — real invariants) ──
    def check(self) -> dict:
        """Return a pass/fail report of REAL invariants:
           - every inference's premises + conclusion exist as info nodes
           - every conflict's source + target exist
           - every premise (info node role=premise) has a resolvable passage_id
           - no inference with an IMPLICIT premise that isn't flagged for review
        """
        info_by_id = {n.id: n for n in self.info_nodes}
        problems = []

        # 1. inference integrity
        for inf in self.inference_nodes:
            for pid in inf.premise_ids:
                if pid not in info_by_id:
                    problems.append(f"{inf.id}: premise {pid} missing")
            if inf.conclusion_id not in info_by_id:
                problems.append(f"{inf.id}: conclusion {inf.conclusion_id} missing")

        # 2. conflict integrity
        for con in self.conflict_nodes:
            if con.source_id not in info_by_id:
                problems.append(f"{con.id}: source {con.source_id} missing")
            if con.target_id not in info_by_id:
                problems.append(f"{con.id}: target {con.target_id} missing")

        # 3. resolvability (the auditable floor) — premises must resolve; conclusions are derived
        unresolved = [n.id for n in self.info_nodes if n.role == "premise"
                      and not n.passage_ids]
        if unresolved:
            problems.append(f"unresolved premise nodes (no passage): {unresolved}")

        # 4. implicit-premise review flag
        implicit = [n.id for n in self.info_nodes if n.explicitness == "IMPLICIT"
                    and n.role in ("premise", "conclusion")]
        # implicit premises are allowed but must be flagged for human review (not an error)

        return {
            "ok": len(problems) == 0,
            "problems": problems,
            "implicit_flagged_for_review": implicit,
            "n_info": len(self.info_nodes), "n_inference": len(self.inference_nodes),
            "n_conflict": len(self.conflict_nodes),
        }

    def to_dict(self) -> dict:
        return {
            "argument_id": self.argument_id, "work_id": self.work_id,
            "info_nodes": [n.to_dict() for n in self.info_nodes],
            "inference_nodes": [n.to_dict() for n in self.inference_nodes],
            "conflict_nodes": [n.to_dict() for n in self.conflict_nodes],
        }

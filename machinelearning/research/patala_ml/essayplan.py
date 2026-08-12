"""patala_ml/essayplan.py — the EssayPlan (the essay as a scholarly decision, not prose).

From the external review (ML-ARGUMENT-REVIEW-CORRECTED.md §7): a serious essay DECIDES which
problem matters, which claims are load-bearing, which evidence is omitted, which counterposition
deserves attention, and where the conclusion stops. So the essay plan is itself an auditable
object — thesis / claims / objections / evidence sets / inference deps — approved by a human
BEFORE prose is generated.

The essay is NOT "argument → essay.md". It is:
  THEME/QUESTION → EssayPlan → human approval → sentence generation → provenance → verification
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class EssayClaim:
    """A claim in the essay plan, each pointing to its evidence + argument root."""
    id: str
    text: str
    role: str = "claim"             # thesis | supporting | objection | conclusion
    argument_id: str = ""           # the pt:argument: it derives from
    passage_ids: list[str] = field(default_factory=list)
    provenance_level: str = "RESOLVES"   # RESOLVES | AUTHENTIC | RELEVANT | SUPPORTS
    status: str = "MACHINE_PROPOSED"

    def to_dict(self) -> dict:
        return {"id": self.id, "text": self.text, "role": self.role,
                "argument_id": self.argument_id, "passage_ids": self.passage_ids,
                "provenance_level": self.provenance_level, "status": self.status}


@dataclass
class EssayPlan:
    """The auditable essay plan — the scholarly DECISION, reviewed before prose."""
    plan_id: str
    work_id: str
    theme: str                     # the theme/question it addresses
    thesis: str
    claims: list[EssayClaim] = field(default_factory=list)
    objections: list[EssayClaim] = field(default_factory=list)   # the counterpositions
    evidence_sets: dict = field(default_factory=dict)            # {claim_id: [passage_ids]}
    status: str = "MACHINE_PROPOSED"

    def add_claim(self, text: str, argument_id: str, passage_ids: list[str],
                  role: str = "supporting") -> str:
        cid = f"{self.plan_id}:c{len(self.claims) + 1}"
        self.claims.append(EssayClaim(id=cid, text=text, role=role, argument_id=argument_id,
                                      passage_ids=passage_ids))
        self.evidence_sets[cid] = passage_ids
        return cid

    def add_objection(self, text: str, target_claim_id: str,
                      passage_ids: list[str]) -> str:
        oid = f"{self.plan_id}:obj{len(self.objections) + 1}"
        self.objections.append(EssayClaim(id=oid, text=text, role="objection",
                                          argument_id=target_claim_id, passage_ids=passage_ids))
        return oid

    def check(self) -> dict:
        """Structural soundness (REAL invariants, not fake scores):
           - thesis present
           - every claim + objection resolves (has passage_ids OR an argument_id)
           - the plan's claims trace to a source (no orphan claims)
        """
        problems = []
        if not self.thesis.strip():
            problems.append("no thesis")
        for c in self.claims:
            if not c.passage_ids and not c.argument_id:
                problems.append(f"{c.id} has no evidence or argument root")
        for o in self.objections:
            if not o.passage_ids and not o.argument_id:
                problems.append(f"{o.id} has no evidence or argument root")
        return {"ok": len(problems) == 0, "problems": problems,
                "n_claims": len(self.claims), "n_objections": len(self.objections)}

    def to_dict(self) -> dict:
        return {"plan_id": self.plan_id, "work_id": self.work_id, "theme": self.theme,
                "thesis": self.thesis, "claims": [c.to_dict() for c in self.claims],
                "objections": [c.to_dict() for c in self.objections],
                "evidence_sets": self.evidence_sets, "status": self.status}


def plan_from_argument(argument, theme_label: str, work_id: str) -> EssayPlan:
    """Derive an EssayPlan from an ArgumentProposal (thesis = the conclusion, claims = premises).

    This is the 'Argument → EssayPlan' step — the conclusion becomes the thesis, the premises
    become supporting claims, each tracing to its passages.
    """
    thesis = argument.conclusion.text if argument.conclusion else argument.title
    plan = EssayPlan(plan_id=f"{argument.argument_id}:plan", work_id=work_id, theme=theme_label,
                     thesis=thesis)
    for i, m in enumerate(argument.members):
        if m.role == "NIGAMANA":
            continue  # the conclusion is the thesis
        passage_ids = [p for p in m.passage_ids if p]
        # fall back to the premise claim's argument_targets if no passage_ids on the member
        if not passage_ids and i < len(argument.premise_claims):
            passage_ids = [t["target_id"] for t in argument.premise_claims[i].argument_targets]
        plan.add_claim(text=m.text, argument_id=argument.argument_id, passage_ids=passage_ids,
                       role="premise")
    return plan

"""patala_ml/argument.py — the Claim-v3-shaped ArgumentProposal (auditable, in-system).

Adopts the truth-engine's Claim v3 (truthadvanced.md): the mature claim schema that resolves
the runtime-vs-argument split:

  posterior_targets  → move the Bayesian numeric state (Certainty) — AFTER gate approval
  argument_targets   → create graph nodes/edges + state-of-play pressure (never touch the posterior)
  every posterior update must be backed by a gate result

Pāṭala alignment (ML-ALIGNMENT.md):
  - the claim mirrors TranslationDecision
  - weights → the truth-engine weighted_lbf (strength.py)
  - status → EpistemicState (machine_proposed → editorially_accepted)
  - every claim is resolvable (passage_id → /api/resolve → Sanskrit)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .strength import score_argument_premises
from .nyayagate import validate


@dataclass
class NyayaMember:
    """One member of the 5-member syllogism (Pratijñā/Hetu/Udāharaṇa/Upanaya/Nigamana)."""
    role: str            # PRATIJNA | HETU | UDAHARANA | UPANAYA | NIGAMANA
    text: str
    passage_ids: list[str] = field(default_factory=list)


@dataclass
class ClaimV3:
    """The Claim v3 record — a single atomic scholarly claim."""
    claim_id: str
    claim_text: str
    tradition_scope: str = ""
    pramana: str = "anumana"
    evidence_dimension: str = "phenomenological"
    argument_dimension: str = ""
    hetu: str = ""
    sadhya: str = ""
    vyapti_statement: str = ""
    falsifier: dict = field(default_factory=dict)
    # runtime targets (posterior) vs graph targets (argument)
    posterior_targets: list[dict] = field(default_factory=list)   # [{target_id, target_type}]
    argument_targets: list[dict] = field(default_factory=list)     # [{target_id, target_type: crux|candidate|bridge}]
    weights: dict = field(default_factory=lambda: {
        "log_bayes_factor": 0.0, "w_rel": 1.0, "w_map": 1.0, "w_aux": 1.0})
    gate: Optional[dict] = None          # the Nyāya gate result (must exist to update posterior)
    status: str = "machine_proposed"     # EpistemicState
    strength: Optional[dict] = None      # derived via strength.py

    def to_dict(self) -> dict:
        return {
            "claim_id": self.claim_id, "claim_text": self.claim_text,
            "tradition_scope": self.tradition_scope, "pramana": self.pramana,
            "evidence_dimension": self.evidence_dimension,
            "argument_dimension": self.argument_dimension,
            "hetu": self.hetu, "sadhya": self.sadhya, "vyapti_statement": self.vyapti_statement,
            "falsifier": self.falsifier,
            "posterior_targets": self.posterior_targets,
            "argument_targets": self.argument_targets,
            "weights": self.weights,
            "gate": self.gate,
            "status": self.status,
            "strength": self.strength,
        }


@dataclass
class ArgumentProposal:
    """The full auditable argument: the 5-member syllogism + its claims + derived strength.

    Mirrors TranslationDecision (ML-ALIGNMENT.md §4) + Claim v3 (truth-engine truthadvanced.md).
    The premise claims each carry their own ClaimV3; the aggregate strength is derived via the
    Bayesian scorer. Every posterior update must be backed by a gate result (the verify floor).
    """
    argument_id: str        # pt:argument:<work>:<slug>
    work_id: str
    title: str
    kind: str               # reductio | analogy | identity | entailment | decomposition
    inference_scheme: str   # TRANSCENDENTAL | REDUCTIO | ANALOGY | ENTAILMENT | PRESUPPOSITION
    members: list[NyayaMember] = field(default_factory=list)
    conclusion: Optional[NyayaMember] = None    # the NIGAMANA (the explicit conclusion)
    tension_id: str = ""                        # the PUSHING question it resolves
    premise_claims: list[ClaimV3] = field(default_factory=list)
    gate: Optional[dict] = None                 # the Nyāya gate result (must exist to update posterior)
    status: str = "machine_proposed"
    aggregate_strength: Optional[dict] = None
    audit_refs: list[str] = field(default_factory=list)   # ids of ContextualArgumentAudits run on this arg

    def to_dict(self) -> dict:
        return {
            "argument_id": self.argument_id, "work_id": self.work_id, "title": self.title,
            "kind": self.kind, "inference_scheme": self.inference_scheme,
            "members": [m.__dict__ for m in self.members],
            "conclusion": self.conclusion.__dict__ if self.conclusion else None,
            "tension_id": self.tension_id,
            "premise_claims": [c.to_dict() for c in self.premise_claims],
            "gate": self.gate,
            "status": self.status,
            "aggregate_strength": self.aggregate_strength,
            "audit_refs": self.audit_refs,
        }


def build_argument(
    argument_id: str,
    work_id: str,
    title: str,
    inference_scheme: str,
    members: list[NyayaMember],
    *,
    kind: str = "entailment",
    tension_id: str = "",
    premise_weights: list[dict] | None = None,
    paradigm_crowding: dict[str, int] | None = None,
    gate: Optional[dict] = None,
) -> ArgumentProposal:
    """Assemble an ArgumentProposal and derive its aggregate strength via the Bayesian scorer.

    CONSTRUCTION ONLY. This does NOT do graph-aware Nyāya audit — that is a separate operation
    (`audit_argument`). Construction and contextual validation are different concerns. If a gate
    result is supplied, it is attached as-is (e.g. a structural gate result); graph-aware viruddha
    is NOT run here (the argument does not know its comparison context).
    """
    # build ClaimV3 for each premise (with its weights) if weights given
    premise_claims = []
    wl = premise_weights or []
    for i, m in enumerate(members):
        w = wl[i] if i < len(wl) else {}
        premise_claims.append(ClaimV3(
            claim_id=f"{argument_id}:prem{i + 1}",
            claim_text=m.text,
            hetu=m.text, sadhya=title,
            argument_targets=[{"target_id": m.role.lower(), "target_type": "premise"}],
            weights={"log_bayes_factor": w.get("log_bayes_factor", 0.0),
                     "w_rel": w.get("w_rel", 1.0), "w_map": w.get("w_map", 1.0),
                     "w_aux": w.get("w_aux", 1.0)},
            tradition_scope=w.get("paradigm", ""),
        ))

    # derive aggregate strength
    agg = score_argument_premises(argument_id, premise_weights or [], paradigm_crowding=paradigm_crowding)

    # the conclusion = the NIGAMANA member (the explicit conclusion)
    conclusion = next((m for m in members if m.role == "NIGAMANA"), None)

    return ArgumentProposal(
        argument_id=argument_id, work_id=work_id, title=title,
        kind=kind, inference_scheme=inference_scheme, members=members,
        conclusion=conclusion, tension_id=tension_id,
        premise_claims=premise_claims, gate=gate, aggregate_strength=agg["aggregate"],
    )


def audit_argument(argument: ArgumentProposal, comparison_graph: list[dict],
                   audit_id: str | None = None) -> dict:
    """Run the GRAPH-AWARE Nyāya audit on an argument against a comparison graph.

    This is the ContextualArgumentAudit: it runs the structural gate on the argument's conclusion
    AND the graph-aware viruddha check against the comparison graph (other golds' established
    propositions). It returns a GateAudit and records its id on the argument's audit_refs.

    Construction (`build_argument`) and contextual validation (`audit_argument`) are separate —
    this is the seam the graph-aware gate actually lives on.
    """
    if argument.conclusion is None:
        raise ValueError("argument has no NIGAMANA conclusion to audit")
    if audit_id is None:
        audit_id = f"{argument.argument_id}:audit:{len(argument.audit_refs) + 1}"
    claim = {
        "claim_id": argument.argument_id,
        "claim_text": argument.conclusion.text,
        "pramana": "anumana",
        "falsifier": {"type": "structural"} if argument.aggregate_strength else None,
        "log_bayes_factor": float((argument.aggregate_strength or {}).get("log_bayes_factor", 0.0) or 0.0),
    }
    result = validate(claim, gold_propositions=comparison_graph)  # structural gate + graph viruddha
    result["audit_id"] = audit_id
    result["argument_id"] = argument.argument_id
    result["graph_viruddha"] = result.get("graph_viruddha", False)
    if audit_id not in argument.audit_refs:
        argument.audit_refs.append(audit_id)
    return result


def from_logical_argument_file(path: str, work_id: str, argument_id: str) -> ArgumentProposal:
    """Parse a LOGICAL-ARGUMENT-*.md file (the Nyāya 5-member shape) into an ArgumentProposal.

    Best-effort: extracts the PRATIJNĀ / HETU / UDAHARANA / UPANAYA / NIGAMANA members.
    """
    text = open(path, encoding="utf-8").read()
    import re
    # match the 5 Nyāya member labels, tolerating diacritic variants (Ñ/N, Ā/A)
    roles = {
        "PRATIJNĀ": r"PRATIJ[ÑN]Ā?\s*[—-]\s*(.+)",
        "HETU": r"HETU\s*[—-]\s*(.+)",
        "UDAHARANA": r"UDAHARANA\s*[—-]\s*(.+)",
        "UPANAYA": r"UPANAYA\s*[—-]\s*(.+)",
        "NIGAMANA": r"NIGAMANA\s*[—-]\s*(.+)",
    }
    members = []
    for role, pat in roles.items():
        m = re.search(pat, text)
        if m:
            members.append(NyayaMember(role=role, text=m.group(1).strip().split("**")[0].strip()))
    # heuristic inference scheme + kind
    scheme = "ENTAILMENT"
    kind = "entailment"
    tl = text.lower()
    if "debate" in tl or "dialectic" in tl:
        scheme = "REDUCTIO"; kind = "reductio"
    elif "transcendental" in tl or "argument for" in tl:
        scheme = "TRANSCENDENTAL"; kind = "entailment"
    title = re.search(r"^#\s+(.+)", text)
    return build_argument(argument_id, work_id, title.group(1).strip() if title else "untitled",
                          scheme, members, kind=kind)

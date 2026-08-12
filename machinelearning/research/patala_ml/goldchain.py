"""patala_ml/goldchain.py — the cross-layer gold-chain certificate.

The milestone: ONE end-to-end chain from Sanskrit to essay sentence, with every transformation
inspectable and every lower-layer proof status propagated upward — WITHOUT collapsing into a
single number.

Two kinds of proof (the review's frozen architecture):
  PHILOLOGICAL  does the English stay licensed by the Sanskrit?   (Agent L0 / philproof.py)
  DERIVATIONAL  does this higher claim derive from the lower scholarly objects?  (Agent ML)

The certificate is per-dimension:
  SOURCE_INTEGRITY  ← the philological proof's source_integrity
  MORPHOLOGY        ← philological
  LEXICAL_SENSE     ← philological (may be OPEN — propagated, not hidden)
  INTERPRETATION    ← derivational (C1 grounded in passage)
  INFERENCE         ← derivational (argument grounded in theme/passages)
  ESSAY_CLAIM       ← derivational (essay claim grounded in argument)

Each node exposes: depends_on[] · status · evidence · review_state
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ChainNode:
    """A node in the gold chain, with its dependency trace."""
    id: str
    layer: str               # SANSKRIT | L0 | L2 | L200 | C1 | THEME | ARGUMENT | AIF | ESSAYPLAN | ESSAYCLAIM | SENTENCE
    status: str              # PROVED | SUPPORTED | EDITOR_APPROVED | OPEN | machine
    evidence: str = ""
    depends_on: list[str] = field(default_factory=list)   # the lower node ids
    philological_proof: Optional[str] = None              # pp:ipvv:v2o:p4
    review_state: str = "machine"

    def to_dict(self) -> dict:
        return {"id": self.id, "layer": self.layer, "status": self.status,
                "evidence": self.evidence, "depends_on": self.depends_on,
                "philological_proof": self.philological_proof, "review_state": self.review_state}


@dataclass
class GoldChainCertificate:
    """The full auditable artifact: the chain + the propagated per-dimension certificate."""
    chain_id: str
    work_id: str
    theme_id: str
    nodes: list[ChainNode] = field(default_factory=list)
    philological: dict = field(default_factory=dict)   # the philproof checks

    def add_node(self, **kw) -> str:
        n = ChainNode(**kw)
        self.nodes.append(n)
        return n.id

    def certificate(self) -> dict:
        """The propagated, per-dimension certificate (NOT collapsed to one number)."""
        # find the philological statuses from the lowest node's philological_proof
        # (in production these come from the actual PhilologicalProof; here we read from the node)
        phil = self.philological
        cert = {
            "SOURCE_INTEGRITY": phil.get("source_integrity", "UNCHECKED"),
            "MORPHOLOGY": phil.get("morphology", "UNCHECKED"),
            "LEXICAL_SENSE": phil.get("lexical_sense", "UNCHECKED"),
        }
        # derivational: the max-of-severity status across the interpretation layers
        def worst(layers):
            order = {"FAILED": 5, "OPEN": 4, "machine": 3, "SUPPORTED": 2,
                     "EDITOR_APPROVED": 1, "PROVED": 0}
            cands = [n.status for n in self.nodes if n.layer in layers]
            return max(cands, key=lambda s: order.get(s, 3)) if cands else "UNCHECKED"
        cert["INTERPRETATION"] = worst(["C1", "THEME"])
        cert["INFERENCE"] = worst(["ARGUMENT", "AIF", "ESSAYPLAN"])
        cert["ESSAY_CLAIM"] = worst(["ESSAYCLAIM", "SENTENCE"])
        # proof_level reflects the PHILOLOGICAL proof level (from the L0 nodes) — P0..P3,
        # NOT derived from interpretation. If any L0 node is OPEN, cap at P1; else use the
        # deepest L0 proof_level present.
        l0_levels = [n.status for n in self.nodes if n.layer == "L0"]
        phil_open = any(n.status == "OPEN" or "OPEN" in n.status for n in self.nodes if n.layer == "L0")
        if l0_levels:
            deepest = max(l0_levels, key=lambda s: {"P0": 0, "P1": 1, "P2": 2, "P3": 3}.get(s, 0))
            cert["proof_level"] = "P1" if phil_open else deepest
        else:
            cert["proof_level"] = "P0"
        return cert

    def to_dict(self) -> dict:
        return {"chain_id": self.chain_id, "work_id": self.work_id, "theme_id": self.theme_id,
                "nodes": [n.to_dict() for n in self.nodes],
                "certificate": self.certificate()}

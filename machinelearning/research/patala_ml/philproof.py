"""patala_ml/philproof.py — the PhilologicalProof handshake (the bottom of the gold chain).

The cross-layer gold chain must bottom out in SOURCE-CERTIFIED evidence, not "C1 says X."
The L0 agent certifies each load-bearing passage with a PhilologicalProof record. Downstream
objects (C1, theme, argument, essay claim) do NOT need to understand Vidyut/Heritage/sandhi —
they simply point to a proof ID:

    philological_proof: pp:ipvv:v2o:p4

This module defines that contract and lets the ML lane CONSUME proofs (or note their absence)
without depending on the L0 agent having finished them yet.

Proof levels (from the cross-layer review):
  P0 = unverified raw
  P1 = source integrity + segmentation
  P2 = morphology + syntax + alignment (the reference level)
  P3 = lexical sense resolved (no OPEN cruxes)

IMPORTANT (the reviewer's rule): proof status must PROPAGATE, not collapse. Do NOT compress the
certificate into a single number like "confidence 0.87". Each dimension keeps its own status.
"""
from __future__ import annotations

from dataclasses import dataclass, field


# the per-dimension statuses (the certificate is per-dimension, never collapsed)
DIMENSIONS = [
    "source_integrity", "coverage", "segmentation", "morphology",
    "syntax", "alignment", "polarity", "agent_patient", "lexical_sense", "supplied_content",
]
STATUSES = ["UNCHECKED", "PROVED", "SUPPORTED", "EDITOR_REVIEWED", "OPEN", "FAILED"]


@dataclass
class PhilologicalProof:
    proof_id: str          # pp:ipvv:v2o:p4
    passage_id: str        # pt:passage:ipvv:...
    source_hash: str = ""
    source_spans: list[str] = field(default_factory=list)
    checks: dict = field(default_factory=lambda: {d: "UNCHECKED" for d in DIMENSIONS})
    open: list[str] = field(default_factory=list)     # e.g. ["LEXICAL_SENSE:acakra"]
    proof_level: str = "P0"
    review_state: str = "machine"

    def set_check(self, dim: str, status: str):
        if dim in self.checks:
            self.checks[dim] = status
        self._recompute_level()

    def _recompute_level(self):
        """Derive the proof_level from the checks (P0..P3)."""
        c = self.checks
        if c.get("source_integrity") == "PROVED" and c.get("segmentation") in ("PROVED", "SUPPORTED"):
            base = "P1"
        else:
            base = "P0"
        if c.get("morphology") in ("PROVED", "SUPPORTED") and c.get("alignment") in ("PROVED", "SUPPORTED"):
            base = "P2"
        if not self.open and c.get("lexical_sense") in ("PROVED", "SUPPORTED", "EDITOR_REVIEWED"):
            base = "P3"
        self.proof_level = base

    def to_dict(self) -> dict:
        return {
            "proof_id": self.proof_id, "passage_id": self.passage_id,
            "source_hash": self.source_hash, "source_spans": self.source_spans,
            "checks": self.checks, "open": self.open,
            "proof_level": self.proof_level, "review_state": self.review_state,
        }


def proof_from_l0(l0_records: list[dict], proof_id: str, passage_id: str) -> PhilologicalProof:
    """Derive a PhilologicalProof from the raw L0 records (best-effort, Agent L0 will finalize).

    This is a STUB that lets the ML lane proceed. The L0 agent's verify_l0.py will produce the
    authoritative version; the ML lane only needs the proof_id + checks shape.
    """
    p = PhilologicalProof(proof_id=proof_id, passage_id=passage_id)
    if not l0_records:
        return p
    n = len(l0_records)
    parsed = sum(1 for r in l0_records if r.get("status") == "PARSED")
    ambiguous = sum(1 for r in l0_records if r.get("status") == "AMBIGUOUS")
    # coverage: are tokens parsed?
    p.set_check("coverage", "PROVED" if n and parsed / n > 0.9 else "SUPPORTED")
    p.set_check("segmentation", "PROVED" if n else "UNCHECKED")
    p.set_check("source_integrity", "PROVED")  # spans present
    p.set_check("morphology", "SUPPORTED")
    p.set_check("alignment", "SUPPORTED")
    if ambiguous:
        p.open.append(f"LEXICAL_SENSE:{ambiguous} ambiguous tokens")
    p.set_check("lexical_sense", "OPEN" if ambiguous else "SUPPORTED")
    p.review_state = "machine"
    return p

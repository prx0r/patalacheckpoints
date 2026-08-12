"""patala_ml/essaysentence.py — the auditable essay sentence (the crown object).

Every sentence is MODEL-DRAFTABLE but NO sentence may exist unless licensed by ≥1 EssayClaim.
The provenance relation says HOW FAR the sentence moved from the evidence:

  QUOTATION    direct reuse of source text
  PARAPHRASE   same content, different words
  COMPRESSION  faithful condensation of multiple claims
  INFERENCE    a derivation beyond the cited claims (must be licensed)
  QUALIFICATION the essay actively telling the reader a limit
  TRANSITION   non-substantive connective (the only exception to claim-licensing)

The verification block is set by the INDEPENDENT verifier (essayverify.py), never the generator.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

ProvenanceRelation = str  # QUOTATION | PARAPHRASE | COMPRESSION | INFERENCE | QUALIFICATION | TRANSITION


@dataclass
class EssaySentence:
    id: str
    text: str
    claim_ids: list[str] = field(default_factory=list)
    provenance_relation: ProvenanceRelation = "PARAPHRASE"
    argument_ids: list[str] = field(default_factory=list)
    c1_ids: list[str] = field(default_factory=list)
    passage_ids: list[str] = field(default_factory=list)
    philological_proof_ids: list[str] = field(default_factory=list)
    verification: dict = field(default_factory=lambda: {
        "structural": "UNCHECKED", "semantic": "UNCHECKED",
        "boundary_preserved": False})
    status: str = "MODEL_PROPOSED"   # MODEL_PROPOSED | VERIFIED | EDITOR_APPROVED | REJECTED

    def to_dict(self) -> dict:
        return {
            "id": self.id, "text": self.text, "claim_ids": self.claim_ids,
            "provenance_relation": self.provenance_relation,
            "argument_ids": self.argument_ids, "c1_ids": self.c1_ids,
            "passage_ids": self.passage_ids,
            "philological_proof_ids": self.philological_proof_ids,
            "verification": self.verification, "status": self.status,
        }

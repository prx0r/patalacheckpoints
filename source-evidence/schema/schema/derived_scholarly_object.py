"""schema/derived_scholarly_object.py — the shared schema (the culmination).

Every layer (argument · proposition · essay · evidence · review · education) defines the SAME
five-field envelope. This is the unified base every concrete object extends:

    id · layer · derived_from · source_refs · epistemic_ceiling · review_state · authority

The design law (invariant, enforced by the 4-axis authority model):
    authority(projection) <= authority(parent)
A projection never exceeds the epistemic status of what it is derived from.

This is the technical proof that Pāṭala is ONE versioned epistemic graph, not several apps:
education, peer review, logical argument, essay, and scholar evidence are all projections of the
same envelopes, and a correction at the source drops the ceiling of every downstream object.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from typing import Any


def sha256(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode("utf-8")).hexdigest()


# ── the ONE epistemic-status ladder (merge of the 4 divergent doc ladders) ──
EPISTEMIC_RANK = {
    "MACHINE_PROPOSED": 0,               # any generative skill (max for machines)
    "ENGINEERING_VALIDATED": 1,          # deterministic verifier
    "SCHOLARLY_CORROBORATED_PRELIMINARY": 2,  # partial corroboration
    "SCHOLARLY_CORROBORATED": 3,         # scholar corpus (no live reviewer)
    "INDEPENDENT_REVIEWED": 4,           # a live independent reviewer
    "ADJUDICATED": 5,                    # human adjudication only
}

# the anti-theatre review ladder (education + essay both use it)
REVIEW_RANK = {
    "GENERATED": 0,
    "STRUCTURALLY_VALID": 1,
    "SUBJECT_REVIEWED": 2,
    "PEDAGOGICALLY_REVIEWED": 3,
    "PILOTED": 4,
    "MEASURED": 5,
    "VALIDATED": 6,
}


@dataclass
class Authority:
    """The 4-axis authority (never one scalar — PATALA-GLOBAL-ARCHITECTURE §9).

    R1 (G3): machine output may set generation/evidence; only an H witness may set review."""
    generation: str = "MACHINE_PROPOSED"      # deterministic/engineering
    evidence: str = "MACHINE_PROPOSED"        # scholar corpus corroboration
    review: str = "NOT_REVIEWED"              # only a human can raise this
    publication: str = "PRIVATE"


# rank of each authority axis (used to derive the ceiling)
_AXIS_RANK = {
    "generation": {"MACHINE_PROPOSED": 0, "ENGINEERING_VALIDATED": 1, "AUTONOMOUSLY_PROVEN": 2},
    "evidence": {"MACHINE_PROPOSED": 0, "MACHINE_CORROBORATED": 1,
                 "SCHOLARLY_CORROBORATED_PRELIMINARY": 2, "SCHOLARLY_CORROBORATED": 3,
                 "SCHOLARLY_CORROBORATED_MULTI_SOURCE": 4},
    "review": {"NOT_REVIEWED": 0, "INDEPENDENT_REVIEWED": 3, "ADJUDICATED": 4},
    "publication": {"PRIVATE": 0, "PUBLIC": 1},
}


@dataclass
class DerivedScholarlyObject:
    """The universal envelope every layer's object extends.

    R3 (G3): `authority` is the canonical vector; `epistemic_ceiling` is a DERIVED projection
    (`derive(authority, dependency ceilings)`) — it is NOT independently writable. This prevents
    drift between the two."""
    id: str                          # pt:<layer>:<work>:<slug>:<version>
    layer: str                       # ARGUMENT|PROPOSITION|ESSAY|EVIDENCE|REVIEW|EDUCATION|LEARNING
    derived_from: list[str] = field(default_factory=list)   # exact pt:* upstream refs
    source_refs: list[str] = field(default_factory=list)    # exact pt:passage / pt:span
    review_state: str = "GENERATED"
    authority: Authority = field(default_factory=Authority)
    witness_classes: dict[str, str] = field(default_factory=dict)  # {axis: "D"|"W"|"M"|"H"}
    content: dict[str, Any] = field(default_factory=dict)   # layer-specific content fields

    def _axis(self, name: str) -> int:
        return _AXIS_RANK.get(name, {}).get(getattr(self.authority, name, ""), -1)

    def derive_ceiling(self) -> str:
        """R3: epistemic_ceiling = derive(authority vector). The review axis dominates (a human
        review legitimately raises the ceiling; it is the sole upward path)."""
        # strongest achievable ceiling = max over axes, but review is the binding human axis
        gen = self._axis("generation")
        ev = self._axis("evidence")
        rev = self._axis("review")
        pub = self._axis("publication")
        # ceiling rank = the max authority actually held
        rank = max(gen, ev, rev, pub)
        for label, r in sorted(EPISTEMIC_RANK.items(), key=lambda kv: kv[1]):
            if r == rank:
                return label
        return "MACHINE_PROPOSED"

    @property
    def epistemic_ceiling(self) -> str:
        """Derived — do not write this directly (G3 R3)."""
        return self.derive_ceiling()

    def ceiling_rank(self) -> int:
        return EPISTEMIC_RANK.get(self.epistemic_ceiling, -1)

    def projection_ok(self, parent_ceiling: str) -> bool:
        """The design law: authority(projection) <= authority(parent)."""
        return self.ceiling_rank() <= EPISTEMIC_RANK.get(parent_ceiling, -1)

    def emit(self) -> dict[str, Any]:
        body = asdict(self)
        body["schema"] = "DERIVED-SCHOLARLY-OBJECT-v1"
        body["epistemic_ceiling"] = self.derive_ceiling()   # derived projection, explicit in emit
        body["hash"] = sha256({k: v for k, v in body.items() if k != "hash"})
        return body

    @classmethod
    def verify(cls, cert: dict[str, Any]) -> bool:
        expected = sha256({k: v for k, v in cert.items() if k != "hash"})
        return expected == cert.get("hash")

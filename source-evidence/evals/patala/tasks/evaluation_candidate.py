#!/usr/bin/env python3
"""evals/patala/tasks/evaluation_candidate.py — the cross-lane evaluation contract (shared).

The handover (devpath1, E2-01) requires the ARGMAP NAT harness to reuse the SAME cross-lane object as
T1: `EvaluationCandidate -> ARGMAP NAT -> EvaluationFinding`. This module defines that shared object
so T1 and ARGMAP evaluations speak one contract (SPEC-EPISTEMIC-CORE, SPEC-CLOSE-G2). Do NOT invent
an ARGMAP-specific handoff format.

An EvaluationCandidate is a FROZEN, exact-versioned scholarly object being evaluated, plus the
minimum provenance to attribute the evaluation. It is deliberately SUT-independent: any layer's output
(ARGMAP, T1, L0, ...) can be wrapped in one.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from typing import Any


def sha256(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode("utf-8")).hexdigest()


@dataclass
class EvaluationCandidate:
    """A frozen, exact-versioned object submitted for evaluation.

    candidate_id : unique (e.g. "cand-argmap-kramasadbhava:v1-v1")
    layer        : the producing layer (ARGMAP | T1 | L0 | ...)
    object_ref   : the passage/work object (e.g. "kramasadbhava:v1")
    version      : the EXACT version (e.g. "argmap-kramasadbhava:v1-v1")
    payload      : the frozen object body the solver consumes
    source_refs  : upstream provenance (T1/L0 refs the object derived from)
    producer     : {agent, commit, status} — how it was produced
    candidate_hash : SHA over the payload (exact-version binding)
    """
    candidate_id: str
    layer: str
    object_ref: str
    version: str
    payload: dict[str, Any] = field(default_factory=dict)
    source_refs: list[str] = field(default_factory=list)
    producer: dict[str, str] = field(default_factory=dict)
    status: str = "MACHINE_PROPOSED"

    def emit(self) -> dict[str, Any]:
        body = asdict(self)
        body["candidate_hash"] = sha256(self.payload)
        return body

    @classmethod
    def from_registry_row(cls, row: dict) -> "EvaluationCandidate":
        """Wrap a layer-registry row (see data/corpus/registries/<layer>-registry.jsonl)."""
        payload = row.get("payload", {})
        return cls(
            candidate_id=f"cand-{row.get('version', row.get('object_id'))}",
            layer=row.get("layer", ""),
            object_ref=row.get("object_id", ""),
            version=row.get("version", ""),
            payload=payload,
            source_refs=row.get("input_refs", []),
            producer={"agent": row.get("created_by", ""), "commit": "",
                      "status": row.get("status", "GENERATED")},
            status=row.get("status", "MACHINE_PROPOSED"),
        )

    @classmethod
    def from_dict(cls, d: dict) -> "EvaluationCandidate":
        return cls(**{k: v for k, v in d.items() if k != "candidate_hash"})

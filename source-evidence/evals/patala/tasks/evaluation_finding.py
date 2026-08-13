#!/usr/bin/env python3
"""evals/patala/tasks/evaluation_finding.py — the cross-lane EvaluationFinding contract (shared).

Mirrors the schema of the 6-finding bundle in data/evaluation/findings/EF-*.json
(schema_version "EvaluationFinding-v1") so the ARGMAP NAT harness emits findings in the SAME shape
the T1/L0 findings use — one contract, not a parallel format (handover devpath1 E2-01).

Lifecycle: OPEN -> IN_REVIEW -> RESOLVED | STILL_FAILING. An OPEN finding on an exact version is a
reviewable object (SPEC-REVIEW-ENGINE-WIRING); a review RETEST_PASS closes it.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from typing import Any

ALLOWED_STATUS = {"OPEN", "IN_REVIEW", "RESOLVED", "STILL_FAILING"}


def sha256(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode("utf-8")).hexdigest()


@dataclass
class EvaluationFinding:
    """An immutable, independently-frozen evaluation finding (exact-version bound)."""
    finding_id: str
    schema_version: str = "EvaluationFinding-v1"
    object_ref: str = ""                 # the passage/work (e.g. "kramasadbhava:v1")
    evaluated_version: str = ""          # EXACT version (e.g. "argmap-kramasadbhava:v1-v1")
    layer: str = ""                      # ARGMAP | T1 | L0 | ...
    contract: str = ""                   # e.g. "ARGMAP-NAT-v1"
    evaluation_run_ref: str = ""
    dimension: str = ""                  # NODE | ROLE | EDGE | SPEAKER | SCOPE | OPEN | INFERENCE
    result: str = "FAIL"                 # FAIL (a finding is a defect)
    failure_class: str = ""              # the mutation/defect family
    observed: str = ""                   # what was observed
    expected_constraint: str = ""        # the violated constraint
    evidence_refs: list[str] = field(default_factory=list)
    recommended_action: str = "REGENERATE_AFTER_WORKER_FIX"
    status: str = "OPEN"                 # OPEN | IN_REVIEW | RESOLVED | STILL_FAILING
    producer: dict = field(default_factory=dict)
    finding_hash: str = ""

    def emit(self) -> dict[str, Any]:
        body = asdict(self)
        body["finding_hash"] = sha256({k: v for k, v in body.items() if k != "finding_hash"})
        return body

    @classmethod
    def from_dict(cls, d: dict) -> "EvaluationFinding":
        f = cls(**{k: v for k, v in d.items() if k != "finding_hash"})
        f.finding_hash = d.get("finding_hash", "")
        return f

    def transition(self, to: str) -> "EvaluationFinding":
        if to not in ALLOWED_STATUS:
            raise ValueError(f"invalid status {to}")
        self.status = to
        return self

    def retest(self, passed: bool) -> "EvaluationFinding":
        """A retest closes the finding: PASS -> RESOLVED, FAIL -> STILL_FAILING."""
        return self.transition("RESOLVED" if passed else "STILL_FAILING")

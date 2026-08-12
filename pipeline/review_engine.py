#!/usr/bin/env python3
"""pipeline/review_engine.py — Phase 3: the executable-corrections vertical loop.

The moat: a scholar's judgment is an immutable, append-only ReviewEvent that a deterministic
reducer consumes to produce a NEW effective scholarly state, then a dependency traversal yields
an ImpactReport — WITHOUT rewriting any historical object or touching unrelated objects.

Core model (minimal, five concepts):
  ReviewEvent   append-only evidence about a judgment (never a destructive mutation)
  ObjectVersion immutable version of a scholarly object
  DependencyEdge typed relation (GROUNDS / USES_AS_PREMISE / USES_AS_WARRANT / ORGANIZES)
  DerivedState  the effective state, deterministically reduced from the review ledger
  ImpactReport  the product-facing output: exactly what a correction changes

The doctrine preserved:
  ACCEPT ≠ truth · REJECT ≠ delete · REVISE ≠ overwrite
  REVISE: P:v1 stays immutable, P:v2 is created, ReviewEvent links v1→v2
  REJECT: P:v1 stays historically resolvable, effective state = REJECTED
  ACCEPT: P:v1 gains accepted review state with reviewer + scope attached

Dependency semantics (typed, explicit — NOT generic "anything downstream is invalid"):
  GROUNDS          source span → philological proof → translation decision → proposition
  USES_AS_PREMISE  proposition → inference → argument
  USES_AS_WARRANT  rule/warrant → inference
  ORGANIZES        theme membership → theme materialization (argument unaffected unless explicitly dependent)

Usage:
  from review_engine import ReviewLedger, apply_review, impact_report
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone

# --------------------------------------------------------------------------- #
# constants
# --------------------------------------------------------------------------- #
DECISIONS = {"ACCEPT", "REVISE", "REJECT", "ABSTAIN"}
EDGE_TYPES = {"GROUNDS", "USES_AS_PREMISE", "USES_AS_WARRANT", "ORGANIZES"}
DERIVED = {
    "CANDIDATE": 0, "SINGLE_REVIEWED": 1, "DOUBLE_REVIEWED": 2,
    "ADJUDICATED": 3, "SPECIALIST_REVIEWED": 4, "REJECTED": -1,
}

# the dependency graph for ARG-002 (the one vertical loop we prove):
#   G2-TC1, G2-TC2 (propositions) USES_AS_PREMISE -> G2-INF1 -> G2-CONC
#   G2-INF1 USES_AS_WARRANT -> (the reconstructed warrant rule W-articulation)
#   G2-TC1/G2-TC2 GROUNDS -> source spans -> philological proof -> translation decisions
ARG002_DEPENDENCIES = [
    {"from": "G2-TC1", "to": "G2-INF1", "type": "USES_AS_PREMISE"},
    {"from": "G2-TC2", "to": "G2-INF1", "type": "USES_AS_PREMISE"},
    {"from": "G2-INF1", "to": "G2-CONC", "type": "GROUNDS"},
    {"from": "W-ARTICULATION", "to": "G2-INF1", "type": "USES_AS_WARRANT"},
    # grounding flows UP from source → proof → translation → proposition, so a proposition
    # revision NEVER stales its source; only a source/span/proof change does.
    {"from": "source:V2L", "to": "pp:ipvv:v2l:p0", "type": "GROUNDS"},
    {"from": "pp:ipvv:v2l:p0", "to": "TD:V2L", "type": "GROUNDS"},
    {"from": "TD:V2L", "to": "G2-TC1", "type": "GROUNDS"},
    {"from": "TD:V2L", "to": "G2-TC2", "type": "GROUNDS"},
    # an UNRELATED object that must stay untouched (the isolation test)
    {"from": "ARG-004-P", "to": "ARG-004", "type": "ORGANIZES"},
]


# --------------------------------------------------------------------------- #
# the five concepts
# --------------------------------------------------------------------------- #
@dataclass
class ReviewEvent:
    review_id: str
    target_ref: str          # e.g. "G2-TC2"
    target_version: str      # e.g. "v1"
    reviewer: str
    reviewer_kind: str       # "human" | "machine" | "scholar"
    scope: str               # e.g. "proposition" | "inference" | "argument"
    decision: str            # ACCEPT | REVISE | REJECT | ABSTAIN
    rationale: str
    evidence_refs: list[str] = field(default_factory=list)
    replacement_ref: str | None = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return {
            "review_id": self.review_id, "target_ref": self.target_ref,
            "target_version": self.target_version, "reviewer": self.reviewer,
            "reviewer_kind": self.reviewer_kind, "scope": self.scope,
            "decision": self.decision, "rationale": self.rationale,
            "evidence_refs": self.evidence_refs, "replacement_ref": self.replacement_ref,
            "created_at": self.created_at,
        }


@dataclass
class ObjectVersion:
    object_ref: str
    version: str             # "v1", "v2", ...
    content: str
    supersedes: str | None = None   # the version this replaces (v2 supersedes v1)
    superseded_by: str | None = None


@dataclass
class DependencyEdge:
    source: str
    target: str
    type: str                # GROUNDS | USES_AS_PREMISE | USES_AS_WARRANT | ORGANIZES

    @classmethod
    def from_dict(cls, d: dict) -> "DependencyEdge":
        return cls(source=d["from"], target=d["to"], type=d["type"])


@dataclass
class DerivedState:
    """The effective state of every object, deterministically reduced from the review ledger."""
    states: dict[str, str] = field(default_factory=dict)  # object_ref -> derived state

    def get(self, ref: str) -> str:
        return self.states.get(ref, "UNCHECKED")


class ReviewLedger:
    """The append-only review ledger + the deterministic reducer + the impact computation."""

    def __init__(self, dependencies: list[dict] | None = None):
        self.events: list[ReviewEvent] = []
        self.versions: dict[str, list[ObjectVersion]] = {}  # ref -> [ObjectVersion...]
        self.edges: list[DependencyEdge] = [
            DependencyEdge.from_dict(d) for d in (dependencies or ARG002_DEPENDENCIES)
        ]
        self._seq = 0

    # ── versioning ───────────────────────────────────────────────────────────
    def add_version(self, object_ref: str, content: str) -> str:
        """Register an object version (immutable). Returns its version tag (v1, v2, ...)."""
        vs = self.versions.setdefault(object_ref, [])
        tag = f"v{len(vs) + 1}"
        prev = vs[-1] if vs else None
        v = ObjectVersion(object_ref, tag, content)
        if prev:
            v.supersedes = prev.version
            prev.superseded_by = tag
        vs.append(v)
        return tag

    # ── review ───────────────────────────────────────────────────────────────
    def record_review(self, target_ref: str, target_version: str, decision: str,
                      reviewer: str, reviewer_kind: str, scope: str, rationale: str,
                      evidence_refs: list[str] | None = None,
                      replacement_ref: str | None = None) -> ReviewEvent:
        """Append an immutable ReviewEvent. Never mutates any object."""
        if decision not in DECISIONS:
            raise ValueError(f"invalid decision {decision}")
        self._seq += 1
        ev = ReviewEvent(
            review_id=f"REV-{self._seq:04d}", target_ref=target_ref,
            target_version=target_version, reviewer=reviewer, reviewer_kind=reviewer_kind,
            scope=scope, decision=decision, rationale=rationale,
            evidence_refs=evidence_refs or [], replacement_ref=replacement_ref,
        )
        self.events.append(ev)
        return ev

    # ── deterministic reducer ────────────────────────────────────────────────
    def reduce(self) -> DerivedState:
        """Compute the effective state of every object from the review ledger + dependency edges.

        Deterministic + idempotent: the same ledger always yields the same DerivedState.
        """
        ds = DerivedState()
        # start: every referenced object is CANDIDATE (a machine-proposed candidate)
        for e in self.edges:
            ds.states.setdefault(e.source, "CANDIDATE")
            ds.states.setdefault(e.target, "CANDIDATE")

        # apply reviews: a REJECT sets REJECTED; ACCEPT/REVISE advance the ladder for the
        # specific reviewed version. Reviews are append-only; the reducer folds them in order.
        for ev in self.events:
            if ev.decision == "REJECT":
                ds.states[ev.target_ref] = "REJECTED"
            elif ev.decision == "REVISE":
                # the reviewed version is superseded; the replacement becomes CANDIDATE
                ds.states[ev.target_ref] = "SUPERSEDED"
                if ev.replacement_ref:
                    ds.states.setdefault(ev.replacement_ref, "CANDIDATE")
            elif ev.decision == "ACCEPT":
                cur = ds.states.get(ev.target_ref, "CANDIDATE")
                ds.states[ev.target_ref] = self._advance_ladder(cur)

        # propagate typed dependency consequences (explicit, not generic)
        self._propagate(ds)
        return ds

    @staticmethod
    def _advance_ladder(cur: str) -> str:
        if cur in ("REJECTED", "SUPERSEDED"):
            return cur
        nxt = {"CANDIDATE": "SINGLE_REVIEWED", "SINGLE_REVIEWED": "DOUBLE_REVIEWED",
               "DOUBLE_REVIEWED": "ADJUDICATED", "ADJUDICATED": "SPECIALIST_REVIEWED"}
        return nxt.get(cur, cur)

    def _propagate(self, ds: DerivedState) -> None:
        """Apply the typed dependency semantics (explicit consequences, not generic invalidation)."""
        # USES_AS_PREMISE: a rejected/revised premise -> the inference + conclusion NEED_REVIEW
        for e in self.edges:
            if e.type != "USES_AS_PREMISE":
                continue
            if ds.get(e.source) in ("REJECTED", "SUPERSEDED", "NEED_REVIEW"):
                ds.states[e.target] = "NEED_REVIEW"
                # the inference's conclusion is affected (via a GROUNDS edge from the inference)
                for e2 in self.edges:
                    if e2.type == "GROUNDS" and e2.source == e.target:
                        ds.states[e2.target] = "NEED_REVIEW"
        # USES_AS_WARRANT: a rejected warrant -> the inference NEED_REVIEW
        for e in self.edges:
            if e.type == "USES_AS_WARRANT" and ds.get(e.source) in ("REJECTED", "SUPERSEDED"):
                ds.states[e.target] = "NEED_REVIEW"
        # GROUNDS: only a changed SOURCE/SPAN propagates staleness DOWNWARD (proof -> translation
        #   -> proposition). A REVISE of a proposition does NOT stale its source grounding — the
        #   source didn't change, the interpretation of it did. (This is the explicit semantic:
        #   interpretation flows up; source-grounding staleness flows down.)
        for e in self.edges:
            if e.type == "GROUNDS" and ds.get(e.source) in ("REJECTED", "SUPERSEDED", "STALE"):
                # only propagate if the CHANGED object is the source-side of the grounding
                # (i.e. we are a span/proof/translation being invalidated, not a proposition)
                if ds.get(e.source) in ("REJECTED", "SUPERSEDED"):
                    ds.states[e.target] = "STALE"

    # ── impact ───────────────────────────────────────────────────────────────
    def impact_report(self, reviewed_ref: str) -> dict:
        """The product-facing output: exactly what a correction changes.

        Uses the CURRENT reduced DerivedState (which already encodes typed propagation),
        so transitively-affected objects (e.g. a conclusion via an affected inference) are
        correctly reported — not just direct-edge neighbors.
        """
        ds = self.reduce()
        affected_states = {"NEED_REVIEW", "STALE", "SUPERSEDED", "REJECTED"}
        direct = []
        potential = []
        # direct: the reviewed object's immediate dependency neighbors (typed)
        for e in self.edges:
            if e.source == reviewed_ref:
                s = ds.get(e.target)
                entry = {"object": e.target, "type": e.type, "state": s}
                if s in affected_states:
                    direct.append(entry)
                else:
                    potential.append(entry)
            elif e.target == reviewed_ref:
                s = ds.get(e.source)
                entry = {"object": e.source, "type": e.type, "state": s}
                if s in affected_states:
                    direct.append(entry)
                else:
                    potential.append(entry)
        # transitively affected: any object whose derived state changed to an affected state
        # but is not the reviewed object itself and not already listed
        known = {d["object"] for d in direct} | {p["object"] for p in potential} | {reviewed_ref}
        for obj, state in ds.states.items():
            if obj == reviewed_ref or obj in known:
                continue
            if state in affected_states:
                direct.append({"object": obj, "type": "DERIVED", "state": state})
                known.add(obj)
        # unaffected = everything in the graph not affected
        unaffected = []
        for obj, state in ds.states.items():
            if obj not in known:
                unaffected.append({"object": obj, "state": state})

        def dedup(items):
            seen, out = set(), []
            for i in items:
                if i["object"] not in seen:
                    seen.add(i["object"]); out.append(i)
            return out
        return {
            "review": self.events[-1].review_id if self.events else None,
            "target": reviewed_ref,
            "directly_affected": dedup(direct),
            "potentially_affected": dedup(potential),
            "unaffected": dedup(unaffected),
            "historical_version_retained": True,
        }


# --------------------------------------------------------------------------- #
# CLI: the synthetic executable-corrections demonstration (ARG-002)
# --------------------------------------------------------------------------- #
def run_demo() -> dict:
    """The controlled REVISE of G2-TC2 v1 → v2, producing the vertical-loop proof."""
    ledger = ReviewLedger()
    # register the original proposition + a narrower revision
    v1 = ledger.add_version("G2-TC2",
        "The awareness expressed as 'I' (ahaṃ-pratyavamarśa) is not treated as one more relation constructed between independently given elements.")
    v2 = ledger.add_version("G2-TC2",
        "The awareness expressed as 'I' is not a conceptual construction of the elements it unifies (narrower formulation).")
    # the REVISE review linking v1 → v2
    ledger.record_review(
        target_ref="G2-TC2", target_version=v1, decision="REVISE",
        reviewer="synthetic-reviewer", reviewer_kind="machine", scope="proposition",
        rationale="narrow the formulation to exclude over-claiming construction (controlled demo)",
        replacement_ref="G2-TC2", evidence_refs=["source:V2L", "pp:ipvv:v2l:p0"],
    )
    ds = ledger.reduce()
    report = ledger.impact_report("G2-TC2")
    return {
        "versions": {r: [v.version for v in vs] for r, vs in ledger.versions.items()},
        "reviews": [ev.to_dict() for ev in ledger.events],
        "derived_state": ds.states,
        "impact": report,
    }


if __name__ == "__main__":
    import sys
    out = "/root/projects/patala/data/corpus/downloads/review-demo-arg002.json"
    res = run_demo()
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=2, ensure_ascii=False)
    print(json.dumps(res["impact"], indent=2, ensure_ascii=False))
    print(f"\nwrote {out}")

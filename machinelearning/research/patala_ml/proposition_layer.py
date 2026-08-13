#!/usr/bin/env python3
"""patala_ml/proposition_layer.py — devpath4 (G3B): the derivational Proposition layer.

The epistemic core's proposition floor. Every proposition is a first-class
`DerivedScholarlyObject(layer=PROPOSITION)` that remembers HOW it came into existence
(ARGUMENT-IR-VISION: derivational Proposition, commitment, explicitness), so a correction at any
upstream layer drops the ceiling of every downstream object.

Design (per ARGUMENT-IR-VISION §5 + SPEC-EPISTEMIC-CORE G3B):
  - Commitment (speaker/force) on every proposition: ASSERTS / DENIES / PRESUPPOSES /
    ASSUMES_FOR_ARGUMENT / ATTRIBUTES_TO_OPPONENT / QUOTES / RECONSTRUCTED / EDITORIAL_RATIONAL_RECONSTRUCTION
  - derivational fields: derived_from (SANSKRIT_EXPLICIT / SANSKRIT_SUPPORTED /
    INTERPRETIVE_RECONSTRUCTION / C1_INTERPRETIVE / IMPLICIT / EDITOR) + explicitness
    (EXPLICIT / RECONSTRUCTED / IMPLICIT)
  - every proposition is a DerivedScholarlyObject -> the authority(projection) <= authority(parent)
    invariant is enforced by construction (ceiling is derived, not writable).

Sources:
  - gold argument nodes (gold002 / gold003/004/005) already carry commitment/explicitness/derived_from
  - ARGMAP argument steps + decision_for_l2 (Agent 2's committed map) -> propositions
  - SourceAssertions (assertion-registry) -> propositions (SPAN_BOUND evidence)

The module is SUT-independent: it lifts whatever real, committed objects exist into the proposition
layer as `DerivedScholarlyObject`s, honoring the honest status ladder (MACHINE_PROPOSED ->
ENGINEERING_VALIDATED; never claims review).
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from dataclasses import dataclass, field

# import the shared envelope (repo root = patala_ml -> research -> machinelearning -> repo)
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
_SCHEMA_DIR = os.path.join(_REPO_ROOT, "source-evidence", "schema")
if _SCHEMA_DIR not in sys.path:
    sys.path.insert(0, _SCHEMA_DIR)
from derived_scholarly_object import DerivedScholarlyObject, Authority  # noqa: E402
try:  # the devpath7 typed contract (reconcile path) — optional, backward-compatible
    from typed_scholarly_object import PropositionObject, PropositionContent, AuthorityVector
    _HAS_TYPED = True
except Exception:  # pragma: no cover
    _HAS_TYPED = False

# the honest commitment vocabulary (ARGUMENT-IR-VISION §5)
COMMITMENTS = (
    "ASSERTS", "DENIES", "PRESUPPOSES", "ASSUMES_FOR_ARGUMENT", "ATTRIBUTES_TO_OPPONENT",
    "QUOTES", "RECONSTRUCTED", "EDITORIAL_RATIONAL_RECONSTRUCTION",
)

# derived_from provenance floor
DERIVED_FROM = (
    "SANSKRIT_EXPLICIT", "SANSKRIT_SUPPORTED", "INTERPRETIVE_RECONSTRUCTION",
    "C1_INTERPRETIVE", "IMPLICIT", "EDITOR", "L2", "C1",
)


def _sha256(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode("utf-8")).hexdigest()


@dataclass
class Proposition:
    """A derivational Proposition: a claim + how it came into existence + its provenance."""
    proposition_id: str
    proposition_text: str
    commitment: str = "ASSERTS"
    explicitness: str = "EXPLICIT"          # EXPLICIT | RECONSTRUCTED | IMPLICIT
    derived_from: str = "SANSKRIT_SUPPORTED"
    source_refs: list[str] = field(default_factory=list)
    grounding: dict = field(default_factory=dict)     # passage/c1/span/edition
    scholarly_corroboration: dict = field(default_factory=dict)
    status: str = "MACHINE_PROPOSED"
    layer: str = "PROPOSITION"

    def to_dso(self) -> DerivedScholarlyObject:
        """Project this proposition as a `DerivedScholarlyObject(layer=PROPOSITION)`."""
        # generation authority is ENGINEERING_VALIDATED only if the proposition is structurally
        # well-formed (has grounding); otherwise MACHINE_PROPOSED. Review axis stays NOT_REVIEWED
        # (only an H witness can raise it) — the honest ceiling is derived, not asserted.
        generation = "ENGINEERING_VALIDATED" if self.grounding else "MACHINE_PROPOSED"
        dso = DerivedScholarlyObject(
            id=f"pt:proposition:{self.proposition_id}:v1",
            layer="PROPOSITION",
            derived_from=self.source_refs,
            source_refs=self.source_refs,
            authority=Authority(generation=generation, evidence="MACHINE_PROPOSED"),
            witness_classes={"generation": "D", "evidence": "W", "review": "W"},
            content={
                "proposition_text": self.proposition_text,
                "commitment": self.commitment,
                "explicitness": self.explicitness,
                "derived_from": self.derived_from,
                "grounding": self.grounding,
                "scholarly_corroboration": self.scholarly_corroboration,
                "proposition_status": self.status,
            },
        )
        return dso

    def to_typed(self) -> "PropositionObject | None":
        """Reconcile to the devpath7 typed contract (Atlas PropositionContent).

        Maps this Proposition onto the typed PropositionObject with the Atlas field shape
        (formulation/subject/scope/modality/explicitness/speaker_ref/support_scope), with a vector
        authority (§28). Returns None if the typed module is unavailable.
        """
        if not _HAS_TYPED:
            return None
        generation = "ENGINEERING_VALIDATED" if self.grounding else "MACHINE_PROPOSED"
        return PropositionObject(
            id=f"pt:proposition:{self.proposition_id}:v1",
            object_id=self.proposition_id,
            layer="PROPOSITION",
            derived_from=self.source_refs,
            source_refs=self.source_refs,
            authority=AuthorityVector(generation=generation, evidence="MACHINE_PROPOSED"),
            content=PropositionContent(
                formulation=self.proposition_text,
                explicitness={"EXPLICIT": "EXPLICIT", "RECONSTRUCTED": "RECONSTRUCTED",
                              "IMPLICIT": "IMPLIED"}.get(self.explicitness, "EXPLICIT"),
                speaker_ref=self.grounding.get("attributed_to") if self.grounding else None,
                assumptions=[],
                derived_from=self.derived_from,
                scholarly_corroboration=self.scholarly_corroboration,
            ),
        )

    def emit(self) -> dict:
        dso = self.to_dso()
        body = dso.emit()
        body["proposition_id"] = self.proposition_id
        body["proposition_text"] = self.proposition_text
        body["commitment"] = self.commitment
        body["explicitness"] = self.explicitness
        body["derived_from"] = self.derived_from
        body["proposition_hash"] = _sha256({
            "text": self.proposition_text, "commitment": self.commitment,
            "derived_from": self.derived_from, "explicitness": self.explicitness,
        })
        return body


# ── lifters: real, committed objects -> propositions ──────────────────────────
def from_gold_node(node: dict, gold_id: str, work_id: str) -> Proposition:
    """Lift a gold argument node (gold002/003/004/005) into a derivational Proposition."""
    g = node.get("grounding", {}) or {}
    return Proposition(
        proposition_id=node.get("proposition_id", "PROP-?"),
        proposition_text=node.get("text", ""),
        commitment=node.get("commitment", "ASSERTS"),
        explicitness=node.get("explicitness", "EXPLICIT"),
        derived_from=node.get("derived_from", "SANSKRIT_SUPPORTED"),
        source_refs=[x for x in [g.get("passage_id"), g.get("c1_id"), g.get("span_id")] if x],
        grounding=g,
        scholarly_corroboration=node.get("scholarly_corroboration", {}),
        status=node.get("status", "MACHINE_PROPOSED"),
    )


def from_argmap(argument_map: dict, object_id: str) -> list[Proposition]:
    """Derive propositions from a committed ARGMAP (argument_steps + decision_for_l2).

    Each argument step becomes a proposition (EXPLICIT, SANSKRIT_SUPPORTED via the map's grounding
    in SOURCE/L0). The decision_for_l2 becomes a derived proposition (derived_from=C1/L2).
    """
    am = (argument_map or {}).get("argument_map", {}) if isinstance(argument_map, dict) and "argument_map" in argument_map else (argument_map or {})
    steps = am.get("argument_steps", []) or []
    props = []
    for i, s in enumerate(steps):
        props.append(Proposition(
            proposition_id=f"{object_id}:step{i + 1}",
            proposition_text=str(s),
            commitment="ASSERTS", explicitness="EXPLICIT",
            derived_from="SANSKRIT_SUPPORTED",
            source_refs=[object_id],
            grounding={"passage_id": object_id},
            status="MACHINE_PROPOSED",
        ))
    decision = am.get("decision_for_l2")
    if decision:
        props.append(Proposition(
            proposition_id=f"{object_id}:decision",
            proposition_text=str(decision),
            commitment="ASSUMES_FOR_ARGUMENT", explicitness="IMPLICIT",
            derived_from="C1_INTERPRETIVE",
            source_refs=[object_id],
            grounding={"passage_id": object_id},
            status="MACHINE_PROPOSED",
        ))
    return props


def from_source_assertion(assertion: dict) -> Proposition:
    """Lift a SourceAssertion (assertion-registry) into a Proposition (SPAN_BOUND evidence)."""
    return Proposition(
        proposition_id=assertion.get("source_assertion_id", "PROP-?"),
        proposition_text=assertion.get("proposition_text", ""),
        commitment=assertion.get("commitment", "ASSERTS"),
        explicitness="EXPLICIT",
        derived_from="SANSKRIT_SUPPORTED",
        source_refs=[assertion.get("span_ref")],
        grounding={"span_ref": assertion.get("span_ref"), "attributed_to": assertion.get("attributed_to")},
        status=assertion.get("generation_status", "MACHINE_PROPOSED"),
    )


def load_gold_propositions(gold_builder, gold_id: str, work_id: str) -> list[Proposition]:
    """Load every derivational Proposition from a gold builder (build_gold_002, etc.)."""
    g = gold_builder()
    return [from_gold_node(n, gold_id, work_id) for n in g.get("nodes", [])]


# ── the layer: emit a full proposition corpus as DerivedScholarlyObjects ──────
def build_proposition_layer(gold_builders=None, argmap=None, assertions=None) -> dict:
    """Assemble the proposition layer from all real committed sources.

    Returns {propositions: [...DerivedScholarlyObject.emit()...],
             counts: {gold, argmap, assertions}, ceiling_honesty: str}.
    """
    props: list[Proposition] = []
    gold_builders = gold_builders or []
    for builder, gid, wid in gold_builders:
        props.extend(load_gold_propositions(builder, gid, wid))
    if argmap:
        # a registry row is {layer, object_id, payload:{argument_map,...}}; pass the argument_map
        argmap_payload = argmap.get("payload", {}) if isinstance(argmap.get("payload"), dict) else argmap
        am_for_props = argmap_payload.get("argument_map", argmap_payload)
        props.extend(from_argmap(am_for_props, argmap.get("object_id", "argmap")))
    if assertions:
        props.extend(from_source_assertion(a) for a in assertions)

    emitted = []
    for p in props:
        d = p.emit()
        emitted.append(d)
    return {
        "propositions": emitted,
        "counts": {"gold": sum(len(load_gold_propositions(b[0], b[1], b[2])) for b in gold_builders),
                   "argmap": sum(1 for _ in from_argmap(
                       (argmap.get("payload", {}).get("argument_map")
                        if isinstance(argmap.get("payload"), dict) else argmap),
                       argmap.get("object_id", "argmap"))) if argmap else 0,
                   "assertions": len(assertions or [])},
        "ceiling_honesty": "every proposition is MACHINE_PROPOSED/ENGINEERING_VALIDATED; "
                           "review axis is NOT_REVIEWED (only an H witness raises it)",
    }


if __name__ == "__main__":
    import json
    sys.path.insert(0, _REPO_ROOT)
    sys.path.insert(0, os.path.join(_REPO_ROOT, "machinelearning", "research"))
    from patala_ml.gold002 import build_gold_002
    from patala_ml.gold003 import build_gold_003
    from patala_ml.gold004 import build_gold_004
    from patala_ml.gold005 import build_gold_005

    builders = [(build_gold_002, "ARG-002", "ipvv"),
                (build_gold_003, "ARG-003", "ipvv"),
                (build_gold_004, "ARG-004", "ipvv"),
                (build_gold_005, "ARG-005", "ipvv")]
    # load the committed ARGMAP + assertions if present
    argmap = None
    am_path = "data/corpus/registries/argmap-registry.jsonl"
    if os.path.exists(am_path):
        with open(am_path) as f:
            first = f.readline().strip()
            if first:
                argmap = json.loads(first)
    assertions = []
    as_path = "data/corpus/registries/assertion-registry.jsonl"
    if os.path.exists(as_path):
        with open(as_path) as f:
            for line in f:
                line = line.strip()
                if line:
                    assertions.append(json.loads(line))

    res = build_proposition_layer(builders, argmap, assertions)
    print(f"proposition layer: {len(res['propositions'])} propositions "
          f"({json.dumps(res['counts'])})")
    for p in res["propositions"][:3]:
        print(f"  {p['proposition_id']:20} {p['commitment']:36} {p['explicitness']:14} {p['epistemic_ceiling']}")

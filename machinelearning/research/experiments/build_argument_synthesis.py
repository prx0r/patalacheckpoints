#!/usr/bin/env python3
"""build_argument_synthesis.py — the CANONICAL ArgumentSynthesis (Pāṭala-native higher-order reasoning).

THIS IS A CANONICAL REBUILD, not a generalization of the earlier prototype. The prototype hardcoded a
PROP_EPISTEMIC_STATUS dict and invented audit IDs; that is NOT a real system. This version:

  * resolves each dependency's epistemic state FROM THE ACTUAL proposition objects (the gold dicts),
    via resolve_dependency(ref) -> {epistemic_status, provenance, structural_audit};
  * uses ONLY real, persisted audit refs — with no persisted ContextualArgumentAudit registry, every
    argument reports structural_audit.state="NOT_AUDITED" / outcome=null rather than inventing an ID;
  * gives the thesis a STABLE proposition id (SYN-CONC-001) equal to the conclusion of the bridge;
  * separates the bridge's ORIGIN (RECONSTRUCTED) from its EVIDENTIAL support_state (UNRESOLVED);
  * marks each dependency's ROLE (LOAD_BEARING_PREMISE / CONTEXT / ...) and computes the epistemic ceiling
    by WEAKEST-GOVERNS over the LOAD_BEARING dependencies only;
  * keeps themes as metadata, never inferential premises;
  * keeps the STRUCTURAL audit axis SEPARATE from the EPISTEMIC axis (two axes, not one scalar).

Audits are NEVER merged into stronger support. Dependency propagation (weakest-governs) is the core mechanism.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from patala_ml.gold002 import build_gold_002
from patala_ml.gold004 import build_gold_004

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))
PACK = os.path.join(ROOT, "benchmarks/v0/packs/PACK-IPVV-REFLEXION-CORE.json")
OUT = os.path.join(ROOT, "benchmarks/v0/review/SYN-IPVV-REFLEXION-CORE-001.json")

# ── epistemic ceiling rank (weakest-governs ordering) ─────────────────────────
CEILING_RANK = {
    "UNRESOLVED": 0,
    "MACHINE_PROPOSED": 1,
    "ENGINEERING_VALIDATED": 2,
    "SCHOLARLY_CORROBORATED_PRELIMINARY": 3,
    "SCHOLARLY_CORROBORATED": 4,
    "INDEPENDENT_REVIEWED": 5,
}

ROLE_LOAD_BEARING = {"LOAD_BEARING_PREMISE", "LOAD_BEARING_INFERENCE"}


# ── the real dependency resolver (no hardcoded status map) ────────────────────
def _gold_registry() -> dict:
    """gold_id -> {proposition_id: node} — the ACTUAL source of epistemic state."""
    golds = {"ARG-GOLD-002": build_gold_002(), "ARG-GOLD-004": build_gold_004()}
    return {gid: {n["proposition_id"]: n for n in g["nodes"]} for gid, g in golds.items()}


def _proposition_index(registry: dict) -> dict:
    """bare proposition_id -> {gold_id, node} (union across input arguments)."""
    index = {}
    for gid, nodes in registry.items():
        for pid, node in nodes.items():
            index[pid] = {"gold_id": gid, "node": node}
    return index


def resolve_dependency(ref: str, registry: dict, prop_index: dict,
                       audits: dict | None = None) -> dict:
    """Resolve a dependency reference to its ACTUAL object state.

    ref forms: "ARG-GOLD-002:G2-CONC" (qualified) or "G2-CONC" (bare, resolved via the index).
    Returns {ref, gold_id, proposition_id, epistemic_status, provenance, structural_audit}.

    epistemic_status comes from the proposition node (its `scholarly_corroboration.promotes_to` if a
    DOSSIER_CORROBORATED block exists, else its `status`). structural_audit comes ONLY from the real
    (persisted) audits registry; if none exist, state="NOT_AUDITED", outcome=null (never invented).
    """
    gold_id, _, pid = ref.partition(":")
    if gold_id not in registry or not pid:
        if ref not in prop_index:
            raise KeyError(f"unresolvable dependency ref: {ref!r}")
        entry = prop_index[ref]
        gold_id, pid = entry["gold_id"], ref
        node = entry["node"]
    else:
        node = registry[gold_id].get(pid)
        if node is None:
            raise KeyError(f"no proposition {pid!r} in {gold_id}")
    corrob = node.get("scholarly_corroboration") or {}
    promotes = corrob.get("promotes_to")
    epistemic_status = promotes if promotes and corrob.get("level") == "DOSSIER_CORROBORATED" \
        else node.get("status", "MACHINE_PROPOSED")
    audit_refs = list((audits or {}).get(gold_id, {}).get("audit_refs", []))
    audit_state = "AUDITED" if audit_refs else "NOT_AUDITED"
    return {
        "ref": f"{gold_id}:{pid}",
        "gold_id": gold_id,
        "proposition_id": pid,
        "epistemic_status": epistemic_status,
        "provenance": node.get("grounding", {}),
        "structural_audit": {
            "state": audit_state,        # NOT_AUDITED until a persisted registry exists
            "outcome": None,             # never a fabricated structural outcome
            "audit_refs": audit_refs,
        },
    }


def build_synthesis(audits: dict | None = None) -> dict:
    """Build the canonical SYN-IPVV-REFLEXION-CORE-001 from actual objects.

    `audits` is an OPTIONAL real-audit registry: {gold_id: {"audit_refs": [...]}}. With no persisted
    registry, every dependency reports structural_audit.state="NOT_AUDITED" — never an invented audit ID.
    """
    with open(PACK, encoding="utf-8") as f:
        pack = json.load(f)

    registry = _gold_registry()
    prop_index = _proposition_index(registry)

    input_args = [
        {"argument_ref": "ARG-GOLD-002",
         "proposition_refs": ["G2-TC2", "G2-CONC"],
         "structural_audit": {
             "state": "AUDITED" if (audits or {}).get("ARG-GOLD-002", {}).get("audit_refs") else "NOT_AUDITED",
             "outcome": None,
             "audit_refs": list((audits or {}).get("ARG-GOLD-002", {}).get("audit_refs", [])),
         }},
        {"argument_ref": "ARG-GOLD-004",
         "proposition_refs": ["G4-CRYSTAL", "G4-CONC"],
         "structural_audit": {
             "state": "AUDITED" if (audits or {}).get("ARG-GOLD-004", {}).get("audit_refs") else "NOT_AUDITED",
             "outcome": None,
             "audit_refs": list((audits or {}).get("ARG-GOLD-004", {}).get("audit_refs", [])),
         }},
    ]

    # ── the bridge inference (first-class, explicit, warrant-carrying) ─────────
    bridge = {
        "inference_id": "SYN-INF-001",
        "premises": ["G2-CONC", "G4-CONC"],
        "conclusion": "SYN-CONC-001",
        "warrant": ("If the 'I'-reflexive awareness is not a conceptual construction [G2-CONC], and "
                    "what makes the light conscious (rather than a thing) is its self-awareness in the "
                    "act of manifesting [G4-CONC], then reflexivity belongs intrinsically to "
                    "manifestation [SYN-CONC-001] — the reconstruction's bridge, not an entailed result."),
        # ORIGIN (how the object came to exist) and EVIDENTIAL state (how supported) are SEPARATE.
        "origin": "RECONSTRUCTED",
        "support_state": "UNRESOLVED",
        "assessment": {
            "inference_id": "SYN-INF-001",
            "origin": "RECONSTRUCTED",
            "support_state": "UNRESOLVED",
            "warrant": "the reconstructed bridge (articulation/construction ≠ intrinsic reflexivity)",
            "defeaters": [
                {"defeater_id": "SYN-DEF-UNIVERSAL",
                 "type": "SCOPE_PROBLEM",
                 "description": "per-act intrinsic reflexivity does not by itself entail one universal Self"},
            ],
            "crux_refs": ["CRUX-REFLEXION-INERT", "CRUX-SYNTHESIS-UNIVERSAL"],
        },
    }

    # ── resolve the LOAD-BEARING dependency states from actual objects ────────
    deps = []
    for ref in ["G2-CONC", "G4-CONC"]:
        d = resolve_dependency(ref, registry, prop_index, audits)
        d["role"] = "LOAD_BEARING_PREMISE"
        deps.append(d)
    deps.append({
        "ref": "SYN-INF-001", "gold_id": "SYNTHESIS", "proposition_id": "SYN-INF-001",
        "role": "LOAD_BEARING_INFERENCE",
        "epistemic_status": bridge["support_state"],
        "provenance": {},
        "structural_audit": {"state": "NOT_APPLICABLE", "outcome": None, "audit_refs": []},
    })

    # ── epistemic ceiling: WEAKEST-GOVERNS over LOAD-BEARING deps only ─────────
    lb = [d for d in deps if d["role"] in ROLE_LOAD_BEARING]
    ceiling = min((CEILING_RANK.get(d["epistemic_status"], 1) for d in lb),
                  default=CEILING_RANK["UNRESOLVED"])
    ceiling_status = next((s for s, r in sorted(CEILING_RANK.items(), key=lambda kv: kv[1])
                           if r == ceiling), "UNRESOLVED")

    unresolved = [d["ref"] for d in lb if d["epistemic_status"] in ("UNRESOLVED", "MACHINE_PROPOSED")]
    corroborated = [d["ref"] for d in lb
                    if d["epistemic_status"] in ("SCHOLARLY_CORROBORATED", "SCHOLARLY_CORROBORATED_PRELIMINARY")]
    # structural axis: INCOMPLETE until the arguments have real persisted contextual audits
    structural_audit_state = "COMPLETE" if all(
        a["structural_audit"]["state"] == "AUDITED" for a in input_args) else "INCOMPLETE"

    cruxes = [
        {"crux_id": "CRUX-REFLEXION-INERT",
         "affects": ["SYN-INF-001", "SYN-CONC-001"],
         "question": "Can an inert thing establish, or does establishment require the self-luminous non-inert?"},
        {"crux_id": "CRUX-SYNTHESIS-UNIVERSAL",
         "affects": ["SYN-CONC-001"],
         "question": "Does per-act intrinsic reflexivity commit to the universal Self, or only to per-act self-luminosity?"},
    ]

    synthesis = {
        "synthesis_id": "SYN-IPVV-REFLEXION-CORE-001",
        "object_kind": "ArgumentSynthesis",
        "research_question": pack.get("research_question", ""),
        "thesis": {
            "proposition_id": "SYN-CONC-001",  # stable id == conclusion of SYN-INF-001
            "text": ("Reflexivity (vimarśa) belongs intrinsically to manifestation: the 'I'-reflexive "
                     "awareness is not a conceptual construction, and what makes the light conscious is "
                     "its self-awareness in the act of manifesting."),
            "status": "MACHINE_RECONSTRUCTED",
        },
        "inputs": input_args,
        "inferences": [bridge],
        "theme_refs": pack.get("theme_refs", []),   # metadata ONLY — never inferential premises
        "dependency_state": {
            "dependencies": deps,
            "load_bearing": [d["ref"] for d in lb],
            "unresolved": unresolved,
            "corroborated": corroborated,
        },
        "cruxes": cruxes,
        "synthesis_audit": {
            # two SEPARATE axes: epistemic (what the evidence supports) vs structural (audit readiness)
            "epistemic_ceiling": ceiling_status,
            "structural_audit_state": structural_audit_state,
            "ceiling_basis": {
                "load_bearing": [d["ref"] for d in lb],
                "statuses": {d["ref"]: d["epistemic_status"] for d in lb},
                "rule": "WEAKEST_GOVERNS over LOAD_BEARING dependencies only (non-load-bearing never caps)",
                "result": ceiling_status,
            },
            # NOT_EVALUATED — no cross-inference contradiction / warrant-consistency / Nyāya check has run
            "internal_consistency": "NOT_EVALUATED",
            "audit_merge_note": "audits are NOT merged; accepted + accepted != strongly supported",
            "themes_not_premises": True,
        },
        "status": "MACHINE_PROPOSED",
        "boundary": {
            "currently_supports": [
                {"claim": "reflexivity belongs intrinsically to manifestation (per-act, reconstructed)",
                 "status": "UNRESOLVED_RECONSTRUCTION"},
            ],
            "does_not_establish": ["the universal Self (one Lord)", "all manifestation is one consciousness",
                                   "consciousness is fundamental simpliciter"],
        },
    }
    return synthesis


def main() -> int:
    syn = build_synthesis()
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(syn, f, indent=2)

    audit = syn["synthesis_audit"]
    print("SYN-IPVV-REFLEXION-CORE-001 (canonical ArgumentSynthesis)")
    print(f"  thesis: {syn['thesis']['proposition_id']} == conclusion of SYN-INF-001")
    print(f"  bridge: origin={syn['inferences'][0]['origin']} | support_state={syn['inferences'][0]['support_state']}")
    print(f"  epistemic_ceiling: {audit['epistemic_ceiling']} (weakest-governs over load-bearing only)")
    print(f"  structural_audit_state: {audit['structural_audit_state']} (separate axis)")
    print(f"  internal_consistency: {audit['internal_consistency']}")
    print(f"  boundary.currently_supports: {[c['claim'] for c in syn['boundary']['currently_supports']]}")
    print(f"  cruxes: {[c['crux_id'] for c in syn['cruxes']]}")
    print(f"\nwritten: {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

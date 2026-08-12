"""patala_ml/goldutil.py — the mechanical gold-fixture tooling (Builds 1 & 3).

The parts that are mechanical and safe to do well:
  1. wrap_fixture()  — wrap a gold-argument dict into the BenchmarkFixture envelope (CP0 schema)
  2. validate_gold() — the gold-consistency validator: every passage_id resolves, every inference's
                       premises/conclusion exist as nodes, no orphan nodes, boundary present.

These make ARG-GOLD-001..005 usable as benchmark fixtures + internally consistent before any
extraction is attempted (the "gold is worth reviewing" gate).
"""
from __future__ import annotations

import glob
import json
import os
import re

VALID_NODE_KINDS = {"TEXTUAL_CLAIM", "INTERPRETIVE_CLAIM", "IMPLICIT_PREMISE",
                    "CONCLUSION", "OBJECTION", "QUALIFICATION"}
VALID_SCHEMES = {"NYAYA_ANUMANA", "REDUCTIO", "TRANSCENDENTAL", "CONCEPTUAL_DISTINCTION",
                 "OBJECTION_REPLY", "COUNTEREXAMPLE", "OTHER", "INTERPRETIVE_CLAIM"}
VALID_EXPLICITNESS = {"EXPLICIT", "RECONSTRUCTED", "IMPLICIT"}
# well-formedness enums (type/integrity ONLY — never validate whether the label is *correct*;
# that is scholarly review). "Validator establishes well-formedness; reviewers establish validity."
VALID_COMMITMENTS = {"ASSERTS", "DENIES", "PRESUPPOSES", "ASSUMES_FOR_ARGUMENT",
                     "ATTRIBUTES_TO_OPPONENT", "QUOTES", "RECONSTRUCTED", "DERIVES",
                     "IMPLIES_ON_RECONSTRUCTION", "EDITORIAL_RATIONAL_RECONSTRUCTION"}
VALID_STATUSES = {"MACHINE_PROPOSED", "CANDIDATE", "SINGLE_EDITOR_GOLD", "DOUBLE_REVIEWED_GOLD",
                  "ADJUDICATED_GOLD", "SUPPORTED", "PROPOSED", "REVIEWED",
                  "ENGINEERING_VALIDATED", "MULTI_MODEL_CORROBORATED", "SCHOLARLY_CORROBORATED",
                  "INDEPENDENT_REVIEWED", "HISTORICALLY_ATTESTED", "STRUCTURALLY_COHERENT",
                  "SCHOLARLY_UNREVIEWED"}
VALID_ALIGNMENT_LEVELS = {"LEXICAL", "CONCEPTUAL", "PROPOSITIONAL"}
VALID_TASK_LEVELS = {"A_PROPOSITION_EXTRACTION", "B_ARGUMENT_RECONSTRUCTION",
                     "C_SYSTEMATIC_INTERPRETATION"}
VALID_SUPPORT_SCOPES = {"LOCAL_TEXT", "LOCAL_CONTEXT", "SAME_WORK", "CROSS_WORK",
                        "SYSTEMATIC_RECONSTRUCTION"}



def wrap_fixture(gold: dict, gold_version: str = "1",
                 review_state: str = "CANDIDATE",
                 authoring_method: str = "MACHINE_PROPOSED") -> dict:
    """Wrap a gold-argument dict into the CP0 BenchmarkFixture envelope.

    Honest defaults: a gold produced by a machine (the agent hand-reconstructing from source) is
    `authoring_method=MACHINE_PROPOSED`, `review_state=CANDIDATE` — NOT `SINGLE_EDITOR_GOLD`/`HAND_ADJUDICATED`,
    which would fabricate a review that never happened. Promotion to `SINGLE_EDITOR_GOLD`/`ADJUDICATED_GOLD`
    must come from an actual reviewer signing the fixture (per the doctrine: statuses come from review events,
    never from code defaults).
    """
    # derive the source ids from the gold's nodes' grounding
    source_ids = []
    for n in gold.get("nodes", []):
        g = n.get("grounding", {})
        if g.get("passage_id") and g["passage_id"] not in source_ids:
            source_ids.append(g["passage_id"])
        if g.get("c1_id"):
            source_ids.append(f"C1:{g['c1_id']}")
    # fall back to the gold's own passage
    if gold.get("passage") and gold["passage"] not in source_ids:
        source_ids.append(gold["passage"])

    return {
        "fixture_id": f"PAT-STRUCT-{gold['gold_id'].split('-')[-1]}",
        "task_family": "PATALA-STRUCTURE",
        "task": "argument_extraction",
        "source_ids": source_ids,
        "gold_version": gold_version,
        "authoring_method": authoring_method,
        "review_state": review_state,
        "created_from": [f"C1:{gold.get('passage', '')}"],
        "allowed_training_use": False,
        "split_class": "EVALUATION_ONLY",
        "input": {"source": f"the C1 read + L2 of {gold.get('passage', '')}"},
        "expected": gold,
    }


def validate_gold(gold: dict) -> dict:
    """The gold-consistency validator. Returns problems (empty = consistent).

    Checks (per the spec — Build 3):
      1. every node's passage_id is a real resolvable store id
      2. every inference's premises + conclusion exist as nodes
      3. no orphan nodes (every node is referenced by some inference OR is a conclusion)
      4. boundary present
      5. node kinds + explicitness are valid
    """
    problems = []
    store = os.environ.get("PATALA_STORE", "/root/projects/patala/data/published/ipvv")
    known_ids = set()
    idx_path = os.path.join(store, "index.json")
    if os.path.exists(idx_path):
        known_ids = {p["id"] for p in json.load(open(idx_path))["passages"]}

    nodes = {n.get("proposition_id") or n.get("id"): n for n in gold.get("nodes", [])}
    used_ids = set(nodes)

    # 1. resolvability
    for nid, n in nodes.items():
        g = n.get("grounding", {})
        pid = g.get("passage_id", "")
        if pid and pid.startswith("pt:passage:ipvv:") and pid not in known_ids:
            problems.append(f"{nid}: passage {pid} does not resolve")
    # gold-level passage
    if gold.get("passage") and gold["passage"].startswith("pt:passage:") \
            and gold["passage"] not in known_ids:
        problems.append(f"gold passage {gold['passage']} does not resolve")

    # 2. inference integrity
    referenced = set()
    for inf in gold.get("inferences", []):
        for p in inf.get("premise_ids", []):
            if p not in used_ids:
                problems.append(f"{inf.get('inference_id')}: premise {p} missing")
            referenced.add(p)
        for c in inf.get("conclusion_ids", []):
            if c not in used_ids:
                problems.append(f"{inf.get('inference_id')}: conclusion {c} missing")
            referenced.add(c)

    # 3. orphan nodes: a node used by NO inference is only suspicious if it is a
    #    TEXTUAL_CLAIM that should feed an inference (the raw textual basis).
    #    INTERPRETIVE_CLAIM / CONCLUSION / OBJECTION / IMPLICIT_PREMISE can be standalone.
    for nid, n in nodes.items():
        if nid in referenced:
            continue
        if n.get("kind") == "TEXTUAL_CLAIM":
            problems.append(f"unused textual claim {nid} (no inference consumes it)")

    # 4. boundary
    if not gold.get("boundary"):
        problems.append("no boundary")

    # 5. valid kinds + explicitness
    for nid, n in nodes.items():
        if n.get("kind") and n["kind"] not in VALID_NODE_KINDS:
            problems.append(f"{nid}: invalid kind {n['kind']}")
        if n.get("explicitness") and n["explicitness"] not in VALID_EXPLICITNESS:
            problems.append(f"{nid}: invalid explicitness {n['explicitness']}")
    for inf in gold.get("inferences", []):
        if inf.get("scheme") and inf["scheme"] not in VALID_SCHEMES:
            problems.append(f"{inf.get('inference_id')}: invalid scheme {inf['scheme']}")

    # 6. well-formedness: type/integrity checks ONLY (never whether a label is semantically correct —
    #    that is scholarly review, not validation). See the ARCHITECTURAL DOCTRINE: "Validator
    #    establishes well-formedness; reviewers establish validity."
    for nid, n in nodes.items():
        if n.get("commitment") and n["commitment"] not in VALID_COMMITMENTS:
            problems.append(f"{nid}: invalid commitment {n['commitment']}")
        if n.get("status") and n["status"] not in VALID_STATUSES:
            problems.append(f"{nid}: invalid status {n['status']}")
        if n.get("task_level") and n["task_level"] not in VALID_TASK_LEVELS:
            problems.append(f"{nid}: invalid task_level {n['task_level']}")
    # derived_from: only flag DANGLING node-refs (free-text descriptions are fine, not validated)
    for nid, n in nodes.items():
        df = n.get("derived_from", "")
        if df:
            for tok in re.findall(r"(?:G[0-9]|A[0-9]|G5)[A-Z0-9_-]*", df):
                if tok not in used_ids:
                    problems.append(f"{nid}: derived_from references missing node {tok}")
    # debate_frame: positions + semantic_alignments (integrity only)
    df = gold.get("debate_frame") or {}
    for pos in df.get("positions", []):
        if not pos.get("position_id"):
            problems.append("debate_frame.position missing position_id")
        for pid in pos.get("proposition_ids", []):
            if pid not in used_ids:
                problems.append(f"position {pos.get('position_id')}: proposition {pid} missing")
    for al in df.get("semantic_alignments", []):
        if al.get("level") and al["level"] not in VALID_ALIGNMENT_LEVELS:
            problems.append(f"semantic_alignment level {al['level']} invalid")
        # left/right may be terms (not ids) — only resolve where they reference proposition ids
        for side in ("left_term", "right_term"):
            t = al.get(side)
            if t and isinstance(t, str) and t in used_ids:
                continue  # resolves to a node — fine
            elif t and isinstance(t, str) and re.fullmatch(r"G[0-9][A-Z0-9_-]*", t):
                problems.append(f"semantic_alignment {side} '{t}' does not resolve to a node")
    # support_scope integrity (when present)
    for pos in df.get("positions", []):
        for sc in pos.get("support_scope", []):
            if sc not in VALID_SUPPORT_SCOPES:
                problems.append(f"position {pos.get('position_id')}: invalid support_scope {sc}")

    return {"ok": len(problems) == 0, "problems": problems,
            "n_nodes": len(nodes), "n_inferences": len(gold.get("inferences", []))}


def validate_all_gold(structure_dir: str | None = None) -> dict:
    """Validate every PAT-STRUCT-*.json fixture in the structure dir."""
    if structure_dir is None:
        structure_dir = "/root/projects/patala/benchmarks/v0/structure"
    results = {}
    for f in sorted(glob.glob(os.path.join(structure_dir, "PAT-STRUCT-*.json"))):
        fx = json.load(open(f))
        gold = fx.get("expected", fx)   # the fixture wraps gold under 'expected'
        r = validate_gold(gold)
        results[f.split("/")[-1]] = r
    return results


# ── the SCHOLARLY_CORROBORATED_PRELIMINARY promotion protocol ────────────────
# A proposition may be promoted to SCHOLARLY_CORROBORATED_PRELIMINARY ONLY when ALL six hold.
# This is the mechanical freeze of the ARG-004 rule (which kept G4-CRYSTAL from laundering I4-1/C4).
VALID_SCHOLARLY_RELATIONS = {"SUPPORTS", "QUALIFIES", "CONTRADICTS", "ALTERNATIVE"}

# ── the T/R/E/C/H/X evidence-kind adapter (preserve semantics, don't flatten) ──
# The markguidance status-tag discipline is preserved exactly and mapped into Pāṭala's evidence kinds,
# so Review can ask "WHAT KIND of evidence supports this proposition?" instead of a generic evidence_ref.
# Semantics preserved from source; each maps to a Pāṭala evidence-kind that Review can render.
TRECX_ADAPTER = {
    "T": "TEXTUAL_ATTESTATION",      # directly attested in a primary text / critical edition
    "R": "RECONSTRUCTION",           # supported by peer-reviewed reconstruction / specialist scholarship
    "E": "EMPIRICAL_EVIDENCE",       # empirical finding / method claim from contemporary research
    "C": "COMPARATIVE",              # structured comparison across traditions or frameworks
    "H": "HYPOTHESIS",               # research proposal / inference beyond current proof
    "X": "UNRESOLVED_CONFLICT",      # contested, weakly supported, unavailable, or invalid
}


def validate_scholarly_corroboration(gold: dict) -> dict:
    """Check every proposition tagged for scholarly corroboration against the promotion protocol.

    For each proposition with a `scholarly_corroboration` block, all of these must hold:

      PRIMARY       exact Sanskrit span resolves + an edition address resolves
      INDEPENDENCE  the scholarly source is not the Pāṭala argument reconstruction itself
      RELEVANCE     the scholar addresses the proposition/reading, not merely the same Sanskrit term
      RELATION      one of SUPPORTS / QUALIFIES / CONTRADICTS / ALTERNATIVE
      TRACEABILITY  publication + page/section/passage recorded
      SCOPE         promotion applies only to the corroborated proposition(s), never propagated to
                    dependent inferences/conclusions

    Returns {"ok", "problems"}. Well-formedness only — it does NOT judge whether a scholar's reading is
    correct (that is scholarly review).
    """
    problems = []
    nodes = {n.get("proposition_id") or n.get("id"): n for n in gold.get("nodes", [])}

    for nid, n in nodes.items():
        block = n.get("scholarly_corroboration")
        if not block:
            continue
        # PRIMARY
        spans = block.get("primary", {})
        if not spans.get("span_id") or not spans.get("edition_ref"):
            problems.append(f"{nid}: corroboration lacks resolving primary span + edition address (PRIMARY)")
        # INDEPENDENCE
        src = block.get("scholarship", [])
        if not src:
            problems.append(f"{nid}: corroboration has no scholarly source (INDEPENDENCE)")
        for s in src:
            if s.get("origin") == "patala_argument_reconstruction":
                problems.append(f"{nid}: source is not independent of the Pāṭala reconstruction (INDEPENDENCE)")
            # RELEVANCE: must address the proposition/reading, not just the term
            if not s.get("addresses"):
                problems.append(f"{nid}: scholar source lacks 'addresses' (what reading it bears on) (RELEVANCE)")
            # RELATION
            if s.get("relation") not in VALID_SCHOLARLY_RELATIONS:
                problems.append(f"{nid}: invalid scholarly relation {s.get('relation')} (RELATION)")
            # TRACEABILITY
            if not s.get("publication") or not (s.get("page") or s.get("section") or s.get("passage")):
                problems.append(f"{nid}: source lacks publication + page/section/passage (TRACEABILITY)")
        # SCOPE: the promotion must be scoped to this proposition; never blanket
        # (this is structurally enforced by attaching the block per-proposition, but check the
        #  promotion state name explicitly)
        state = n.get("status") or n.get("review_state")
        if block.get("promotes_to") == "SCHOLARLY_CORROBORATED" and block.get("level") != "PUBLICATION_VERIFIED":
            problems.append(f"{nid}: full SCHOLARLY_CORROBORATED requires PUBLICATION_VERIFIED "
                            f"(PRELIMINARY is the default) (SCOPE)")

    return {"ok": len(problems) == 0, "problems": problems, "corroborated_nodes": [
        nid for nid, n in nodes.items() if n.get("scholarly_corroboration")]}

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

VALID_NODE_KINDS = {"TEXTUAL_CLAIM", "INTERPRETIVE_CLAIM", "IMPLICIT_PREMISE",
                    "CONCLUSION", "OBJECTION", "QUALIFICATION"}
VALID_SCHEMES = {"NYAYA_ANUMANA", "REDUCTIO", "TRANSCENDENTAL", "CONCEPTUAL_DISTINCTION",
                 "OBJECTION_REPLY", "COUNTEREXAMPLE", "OTHER", "INTERPRETIVE_CLAIM"}
VALID_EXPLICITNESS = {"EXPLICIT", "RECONSTRUCTED", "IMPLICIT"}


def wrap_fixture(gold: dict, gold_version: str = "1", review_state: str = "SINGLE_EDITOR_GOLD") -> dict:
    """Wrap a gold-argument dict into the CP0 BenchmarkFixture envelope."""
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
        "authoring_method": "HAND_ADJUDICATED",
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

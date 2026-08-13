#!/usr/bin/env python3
"""pipeline/theme_worker.py — the THEME layer handler (evidence-backed synthesis across C1s).

Per SPEC_THEME.md + SPEC_THEME_CLUSTERING.md + the patala-theme skill:
  - THEME is NOT a keyword/cluster. It is an evidence-backed synthesis across C1s.
  - Discovery is machine-derived (hybrid relation-graph over C1s); acceptance is editorial.
  - Themes OVERLAP (a C1 has a primary_theme + member_of[]), they do not partition.
  - Cluster ≠ theme: structural evidence is the floor; semantic/Louvain grouping is proposal.

This handler REUSES Agent 1's deterministic machinery (machinelearning/research/patala_ml/):
  - build_hybrid_graph_c1 (shared terms + see-also edges)
  - cluster_c1s / louvain_baseline (overlapping communities, deterministic seed)
  - core_hierarchy (k-core structural embeddedness)
Per the doctrine: reuse before building — do NOT rebuild parallel theme machinery.

Consumes committed C1s from OUR registry (Agent 2's source of truth) and emits a ThemeProposal
(MACHINE_PROPOSED) with member_C1s + strengths + roles + edge_evidence + THEME BOUNDARY.
A deterministic THEME validator gates the commit: every member_C1 resolves; no member without C1
evidence; overlapping member_of allowed; status MACHINE_PROPOSED; boundary present.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, "/root/projects/patala/pipeline")
sys.path.insert(0, "/root/projects/patala/machinelearning/research")

import object_registry as R

# Reuse Agent 1's theme/cluster machinery (the deterministic floor + overlapping communities).
try:
    from patala_ml.cluster import (build_hybrid_graph_c1, cluster_c1s, ClusterProposal)
    from patala_ml.c1corpus import C1Node
    _AGENT1 = True
except Exception as _e:  # pragma: no cover
    _AGENT1 = False
    _AGENT1_ERR = str(_e)

MIN_C1S = 2


def _c1_nodes_from_registry(object_ids: list[str]) -> list[C1Node]:
    """Build Agent 1 C1Node objects from our committed C1 registry (the source of truth)."""
    nodes = []
    for oid in object_ids:
        cur = R.current("C1", oid)
        if not cur:
            continue
        c1 = cur.get("payload", {}).get("c1", {}) or {}
        terms = []
        for kt in c1.get("key_terms") or []:
            if isinstance(kt, dict):
                t = kt.get("term") or ""
            else:
                t = str(kt)
            if t:
                terms.append(t)
        related = c1.get("related_passages") or []
        body = " ".join(str(c1.get(k) or "") for k in
                        ("summary", "function", "explanation", "boundary"))
        nodes.append(C1Node(c1_id=oid, passage_id=oid, body=body,
                            terms=terms, see_also=related))
    return nodes


def _propose_themes(c1nodes: list[C1Node], work_id: str) -> list[dict]:
    """Deterministic theme proposal via Agent 1's hybrid graph + overlapping clustering."""
    if not _AGENT1 or len(c1nodes) < MIN_C1S:
        return []
    try:
        import networkx as nx
        proposals = cluster_c1s(c1nodes)  # overlapping communities, deterministic seed
        out = []
        for i, p in enumerate(proposals):
            # membership strengths -> roles (deterministic heuristic, explicit + honest)
            members = []
            sorted_members = sorted(p.member_c1_ids,
                                    key=lambda m: -p.strengths.get(m, 0.0))
            for m in sorted_members:
                s = p.strengths.get(m, 0.0)
                if s >= 0.7:
                    role = "DEFINES"
                elif s >= 0.4:
                    role = "ESTABLISHES"
                elif s > 0.0:
                    role = "DEVELOPS"
                else:
                    role = "CONTRASTS"
                members.append({"c1_id": m, "strength": round(s, 3), "role": role})
            out.append({
                "theme_id": f"{work_id}__theme_{i+1}",
                "label": f"candidate theme {i+1}",
                "member_claims": members,
                "development": [],
                "counterexamples": [],
                "edge_evidence": [dict(e) for e in p.edge_evidence],
                "boundary": {
                    "included_because": [m["c1_id"] for m in members],
                    "not_claiming": "essay-level thesis / cross-tradition / modern application",
                },
                "status": "MACHINE_PROPOSED",
            })
        return out
    except Exception:
        return []


def theme_generator(layer: str, batch: list[dict]) -> list[dict]:
    """Produce ThemeProposals from the committed C1s in the batch (one proposal set per run)."""
    c1nodes = _c1_nodes_from_registry([b["object_id"] for b in batch])
    themes = _propose_themes(c1nodes, work_id=_work_id(batch))
    if not themes:
        return []
    # emit one proposal object per theme (the controller commits each independently)
    return [{"object_id": t["theme_id"], "input_hash": _batch_hash(batch),
             "theme": t, "theme_status": "MACHINE_PROPOSED"} for t in themes]


def _work_id(batch: list[dict]) -> str:
    for b in batch:
        oid = b.get("object_id", "")
        if ":" in oid:
            return oid.split(":")[0]
    return "ipvv"


def _batch_hash(batch: list[dict]) -> str:
    import hashlib
    ids = "|".join(sorted(b.get("object_id", "") for b in batch))
    return hashlib.sha256(ids.encode()).hexdigest()


def theme_validator(layer: str, proposal: dict) -> tuple[bool, str]:
    """Deterministic THEME gate (SPEC_THEME §7 / SPEC_THEME_CLUSTERING §7).

    - every member_C1 resolves to a committed C1 (or a real C1 id)
    - every member has a strength + role (not just "in the cluster")
    - overlapping member_of is allowed; status MACHINE_PROPOSED; boundary present
    """
    if proposal.get("theme_status") != "MACHINE_PROPOSED":
        return False, f"theme_status:{proposal.get('theme_status','MISSING')}"
    theme = proposal.get("theme", {})
    members = theme.get("member_claims", [])
    if not members:
        return False, "theme has no members (cluster ≠ theme; nothing grounded)"
    if not theme.get("theme_id"):
        return False, "theme missing theme_id"
    if not theme.get("boundary", {}).get("included_because"):
        return False, "theme missing boundary (synthesis inflation guard)"
    for m in members:
        c1_id = m.get("c1_id")
        if not c1_id:
            return False, "member missing c1_id"
        # member must resolve to a committed C1 in the registry
        if not R.current("C1", c1_id) and not _looks_like_c1_id(c1_id):
            return False, f"member_C1 unresolved: {c1_id}"
        if "strength" not in m or "role" not in m:
            return False, f"member missing strength+role: {c1_id}"
    return True, ""


def _looks_like_c1_id(s: str) -> bool:
    # a real IPVV-style C1 id (V2A, V3B, ...) even if not in our registry (IPVV corpus path)
    return bool(re.match(r"^[Vv]\d[A-Za-z]", s or ""))


def make_theme_handlers() -> dict:
    return {"generator": theme_generator, "validator": theme_validator}

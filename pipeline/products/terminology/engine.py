"""products/terminology/engine.py — Terminology / Lemma-through-time.

The diachronic sense-trajectory product: how a technical lemma's meaning shifts across traditions and
periods. Consumes the REAL curated trajectories.json (converted from data/corpus/trajectories.ts) +
data/terms.json (accepted senses).

What it provides (deterministic, CPU-only):
  - lemma_history(lemma) -> the diachronic nodes (period/tradition/sense/claim/evidence)
  - sense_trajectory(lemma) -> ordered chronological sense-shift
  - evidence_for(lemma, node_id) -> the evidence links (passages/resources) supporting a sense

The data is curated interpretation ("Sense"/"Synthesis" authority), seeded from the reference map —
so every node is a reviewable ASSERTION (status: proposed/reviewed/accepted/disputed), never
mechanically-derived corpus noise.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
DATA = _ROOT / "data/corpus"


def _load() -> list[dict]:
    p = DATA / "trajectories.json"
    if not p.exists():
        return []
    return json.loads(p.read_text(encoding="utf-8"))


def _load_terms() -> dict:
    p = DATA / "terms.json"
    if not p.exists():
        return {}
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(d, dict) and "terms" in d:
            return {t.get("lemma"): t for t in d["terms"]}
        if isinstance(d, list):
            return {t.get("lemma"): t for t in d}
        return d
    except Exception:
        return {}


def lemmas() -> list[str]:
    return [t["lemma"] for t in _load()]


def lemma_history(lemma: str) -> dict:
    """The diachronic sense-history of one lemma (all nodes, ordered by earliest date)."""
    traj = next((t for t in _load() if t["lemma"] == lemma), None)
    if not traj:
        return {"lemma": lemma, "found": False, "nodes": []}
    nodes = traj.get("nodes", [])
    nodes_sorted = sorted(nodes, key=lambda n: (n.get("date_range") or {}).get("not_before", 0) or 0)
    return {"lemma": lemma, "title": traj.get("title"), "note": traj.get("note"),
            "found": True, "nodes": nodes_sorted}


def sense_trajectory(lemma: str) -> dict:
    """The chronological sense-shift: period_label -> sense_id/claim, in order."""
    h = lemma_history(lemma)
    if not h["found"]:
        return h
    return {
        "lemma": lemma,
        "trajectory": [{
            "period": n.get("period_label"),
            "sense_id": n.get("sense_id") or n.get("proposed_sense_id"),
            "status": n.get("status"),
            "certainty": n.get("certainty"),
            "tradition": n.get("tradition_label"),
            "claim": n.get("claim"),
            "translation_policy": (n.get("translation_policy") or {}).get("guidance"),
        } for n in h["nodes"]],
        "note": "chronological sense-shift of the lemma (curated interpretation)",
    }


def evidence_for(lemma: str, node_id: str | None = None) -> dict:
    """Evidence links supporting a lemma's sense node(s)."""
    h = lemma_history(lemma)
    if not h["found"]:
        return {"lemma": lemma, "found": False, "evidence": []}
    nodes = h["nodes"] if node_id is None else [n for n in h["nodes"] if n["id"] == node_id]
    return {
        "lemma": lemma, "node_id": node_id,
        "evidence": [{
            "node": n["id"], "period": n.get("period_label"),
            "target_id": e.get("target_id"), "type": e.get("type"),
            "role": e.get("role"), "locator": e.get("locator"),
        } for n in nodes for e in n.get("evidence_links", [])],
    }


def terminology_report() -> dict:
    """The full terminology product surface (all lemmas + their trajectories)."""
    terms = _load_terms()
    return {
        "lemmas": lemmas(),
        "n_terms": len(lemmas()),
        "n_accepted_senses": len(terms),
        "trajectories": {t["lemma"]: sense_trajectory(t["lemma"])["trajectory"] for t in _load()},
    }


if __name__ == "__main__":
    import sys as _s
    lemma = _s.argv[1] if len(_s.argv) > 1 else "kula"
    op = _s.argv[2] if len(_s.argv) > 2 else "history"
    if op == "history":
        print(json.dumps(lemma_history(lemma), indent=2, ensure_ascii=False))
    elif op == "trajectory":
        print(json.dumps(sense_trajectory(lemma), indent=2, ensure_ascii=False))
    elif op == "evidence":
        print(json.dumps(evidence_for(lemma), indent=2, ensure_ascii=False))
    elif op == "report":
        print(json.dumps(terminology_report(), indent=2, ensure_ascii=False))
    else:
        print(json.dumps({"error": f"unknown op {op}"}))

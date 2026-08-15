"""products/timeline/engine.py — Timeline.

The diachronic Śiva source-tree: schools/traditions laid across time (genealogy + prehistory +
philosophical interlocutors), each with period, epistemic era (textual/comparative/archaeological),
influences, anchors, bibliography ids, and hop. Consumes the REAL curated
`data/atlas/historyTimeline.json` (schema patala:history-timeline:v1).

What it provides (deterministic, CPU-only):
  - schools() — all schools/traditions with period + era
  - school(id) — one school's full record + its influences
  - lineage(id) — the ancestor chain (parent links)
  - era_breakdown() — schools grouped by epistemic era
  - timeline() — the full chronological map (schools + chains)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
DATA = _ROOT / "data/atlas"


def _load() -> dict:
    p = DATA / "historyTimeline.json"
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def schools() -> list[dict]:
    return _load().get("schools", [])


def school(school_id: str) -> dict | None:
    return next((s for s in schools() if s["id"] == school_id), None)


def lineage(school_id: str) -> list[dict]:
    """The ancestor chain (parent -> ... -> this school)."""
    chain = []
    cur = school(school_id)
    seen = set()
    while cur and cur["id"] not in seen:
        seen.add(cur["id"])
        chain.append(cur)
        parent = cur.get("parent")
        cur = school(parent) if parent else None
    chain.reverse()
    return chain


def era_breakdown() -> dict:
    eras = {}
    for s in schools():
        eras.setdefault(s.get("era"), []).append(s["id"])
    return {k: v for k, v in sorted(eras.items())}


def timeline() -> dict:
    d = _load()
    return {
        "schema": d.get("schema"), "date": d.get("date"), "note": d.get("note"),
        "n_schools": len(d.get("schools", [])),
        "schools": d.get("schools", []),
        "chains": d.get("chains", []),
        "era_labels": d.get("era_labels", {}),
        "hop_roadmap": d.get("hop_roadmap", []),
    }


def chronological() -> list[dict]:
    """Schools sorted by earliest period start."""
    return sorted(schools(), key=lambda s: (s.get("period") or [0, 0])[0])


if __name__ == "__main__":
    import sys as _s
    op = _s.argv[1] if len(_s.argv) > 1 else "timeline"
    if op == "schools":
        print(json.dumps({"schools": schools()}, indent=2, ensure_ascii=False))
    elif op == "school":
        print(json.dumps(school(_s.argv[2]), indent=2, ensure_ascii=False))
    elif op == "lineage":
        print(json.dumps(lineage(_s.argv[2]), indent=2, ensure_ascii=False))
    elif op == "eras":
        print(json.dumps(era_breakdown(), indent=2))
    elif op == "chronological":
        print(json.dumps([{"id": s["id"], "period": s.get("period"), "era": s.get("era")}
                          for s in chronological()], indent=2))
    else:
        print(json.dumps(timeline(), indent=2, ensure_ascii=False))

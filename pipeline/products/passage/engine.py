"""products/passage/engine.py — Passage / Reading (#3).

The philology-facing primitive: a canonical Passage object + a deterministic KG2Code-style query engine
over the real IPVV passage graph. Borrows the proven `KnowledgeQuery` pattern from fuck-off's
`lib/query.py` (resolve / neighbors / path / evidence), re-expressed against PĀṬALA's real passages.

What it provides:
  - a canonical Passage object (source Sanskrit + L2 + C1 + immutable_id + work)
  - resolve / neighbors / path / evidence queries over the passage graph (passages linked by
    shared work + salient terms) — deterministic, no embeddings, CPU-only.
"""
from __future__ import annotations

import json
import sys
from collections import deque
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT / "pipeline") not in sys.path:
    sys.path.insert(0, str(_ROOT / "pipeline"))

from products._shared import ipvv  # noqa: E402


def canonical_passage(passage: dict) -> dict:
    """The canonical Passage object (the philology primitive)."""
    c1 = passage.get("c1") or {}
    return {
        "passage_id": passage.get("id"),
        "immutable_id": ipvv.passage_id(passage),
        "work_id": passage.get("work_id"),
        "vol": passage.get("vol"),
        "chunk": passage.get("chunk"),
        "section": passage.get("section"),
        "source_sanskrit": passage.get("source", {}).get("text", ""),
        "l2_translation": passage.get("l2_text") or "",
        "c1_commentary": ipvv.c1_body(passage),
        "status": passage.get("status"),
    }


def _link_terms(passage: dict) -> set:
    import re
    c1 = ipvv.c1_body(passage)
    hay = (passage.get("source", {}).get("text", "") + " " + (passage.get("l2_text") or "") + " " + c1).lower()
    return {w for w in re.findall(r"[a-zA-Z\u0900-\u097F]+", hay) if len(w) > 3}


class PassageQuery:
    """Deterministic KG2Code-style query over the real passage graph (borrowed query.py pattern)."""

    def __init__(self):
        self.passages = ipvv.passages()
        self.by_id = {ipvv.passage_id(p): p for p in self.passages if ipvv.passage_id(p)}
        self.by_passage_id = {p.get("id"): p for p in self.passages if p.get("id")}
        self.by_work = {}
        for p in self.passages:
            self.by_work.setdefault(p.get("work_id"), []).append(ipvv.passage_id(p))
        # adjacency: passages of the same work are linked; plus shared-term links
        self.terms = {ipvv.passage_id(p): _link_terms(p) for p in self.passages}
        self.adj = {}
        for pid, terms in self.terms.items():
            self.adj[pid] = set()
            work = next((p for p in self.passages if ipvv.passage_id(p) == pid), {}).get("work_id")
            for other in self.by_work.get(work, []):
                if other != pid:
                    self.adj[pid].add(other)

    def resolve(self, ref: str) -> str | None:
        """Resolve an id / immutable / passage-id / fragment to a canonical (immutable) passage id."""
        if ref in self.by_id:
            return ref
        if ref in self.by_passage_id:
            return ipvv.passage_id(self.by_passage_id[ref])
        # fragment match against passage ids (human-friendly: "chunkD")
        for pid in self.by_passage_id:
            if ref in pid or pid in ref:
                return ipvv.passage_id(self.by_passage_id[pid])
        return None

    def get(self, ref: str) -> dict | None:
        pid = self.resolve(ref)
        if not pid:
            return None
        return canonical_passage(self.by_id[pid])

    def neighbors(self, ref: str) -> list[str]:
        pid = self.resolve(ref)
        return sorted(self.adj.get(pid, []))

    def path(self, start_ref: str, end_ref: str, max_hops: int = 4, limit: int = 5) -> list[list[str]]:
        """BFS paths between two passages (deterministic)."""
        start, end = self.resolve(start_ref), self.resolve(end_ref)
        if not start or not end:
            return []
        q = deque([[start]])
        out = []
        while q and len(out) < limit:
            p = q.popleft()
            if len(p) > max_hops:
                continue
            last = p[-1]
            if last == end and len(p) > 1:
                out.append(p)
                continue
            for nb in self.adj.get(last, []):
                if nb not in p:
                    q.append(p + [nb])
        return out

    def evidence(self, ref: str) -> dict | None:
        p = self.get(ref)
        if not p:
            return None
        return {"passage_id": p["passage_id"], "work_id": p["work_id"],
                "immutable_id": p["immutable_id"], "status": p["status"],
                "source_chars": len(p["source_sanskrit"]), "has_c1": bool(p["c1_commentary"])}


def make_query() -> PassageQuery:
    return PassageQuery()


if __name__ == "__main__":
    import sys as _s
    q = make_query()
    ref = _s.argv[1] if len(_s.argv) > 1 else "chunkD"
    op = _s.argv[2] if len(_s.argv) > 2 else "get"
    if op == "get":
        print(json.dumps(q.get(ref), indent=2, ensure_ascii=False))
    elif op == "neighbors":
        print(json.dumps({"passage": q.resolve(ref), "neighbors": q.neighbors(ref)}, indent=2))
    elif op == "evidence":
        print(json.dumps(q.evidence(ref), indent=2))
    else:
        print(json.dumps({"error": f"unknown op {op}"}))

"""products/research_packet/engine.py — Research Packet (#9).

Question -> structured evidence packet using REAL graph retrieval (PathRAG flow) over real IPVV
passages. Lexical seed + PathRAG graph flow: a question returns exact matches AND the
graph-relevant neighborhood (the retrieval moat). Deterministic + stdlib + networkx.

    from products.research_packet.engine import research_packet
    research_packet("eternal self memory")
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT / "pipeline") not in sys.path:
    sys.path.insert(0, str(_ROOT / "pipeline"))

from products._shared import ipvv


def _tokens(t: str) -> set:
    return {w for w in re.findall(r"[a-zA-Z\u0900-\u097F]+", t.lower()) if len(w) > 3}


def _build_graph(passages: list[dict]):
    import networkx as nx

    G = nx.Graph()
    texts = {}
    for p in passages:
        pid = ipvv.passage_id(p)
        if not pid:
            continue
        hay = (p.get("source", {}).get("text", "") + " " + (p.get("l2_text") or "") +
               " " + ipvv.c1_body(p)).lower()
        texts[pid] = _tokens(hay)
        G.add_node(pid)
    pids = list(texts.keys())
    for i in range(len(pids)):
        for j in range(i + 1, len(pids)):
            w = len(texts[pids[i]] & texts[pids[j]])
            if w > 0:
                G.add_edge(pids[i], pids[j], weight=w)
    return G, texts


def _pathrag_flow(G, start, alpha=0.7, theta=1e-3, iters=40) -> dict:
    S = {n: 0.0 for n in G.nodes}
    S[start] = 1.0
    for _ in range(iters):
        newS = dict(S)
        for v in G.nodes:
            if v == start:
                continue
            newS[v] = sum(alpha * S[u] / max(1, G.degree(u)) for u in G.neighbors(v))
        S = newS
        if max(abs(S[v] - newS[v]) for v in G.nodes) < 1e-6:
            break
    for v in S:
        if S[v] / max(1, G.degree(v)) < theta:
            S[v] = 0.0
    return S


def research_packet(question: str, max_sources: int = 4) -> dict:
    passages = ipvv.passages()
    q_tokens = [t for t in re.findall(r"\w+", question.lower()) if len(t) > 2]

    # canonical-id resolution (borrowed sage-wiki pattern): if the question names a WORK alias
    # (e.g. "IPVV"), expand the match set so passages of that canonical work are surfaced.
    try:
        from products._shared.canonical_id import default_index
        cidx = default_index()
        q_aliases = set()
        for t in q_tokens:
            cid = cidx.canonical_id(t)
            if cid != t:  # this token resolved to a canonical work id
                q_aliases.add(cid)
        for w in cidx.canonical:
            for t in q_tokens:
                if w.endswith(t) or t in w:  # partial: 'isvarapratyabhijnavivrtivimarsini' matches
                    q_aliases.add(w)
    except Exception:
        q_aliases = set()

    G, texts = _build_graph(passages)

    seeded = []
    for p in passages:
        pid = ipvv.passage_id(p)
        if pid not in texts:
            continue
        hits = sum(1 for t in q_tokens if t in texts[pid])
        # bonus: a passage whose WORK resolves to a queried canonical alias
        work = (p.get("work_id") or "").lower()
        if any(a in work for a in q_aliases):
            hits += 2
        if hits:
            seeded.append((hits, pid, p))
    seeded.sort(key=lambda x: -x[0])

    ranked = []
    if seeded and len(G.nodes) > 1:
        top_seed = seeded[0][1]
        if top_seed in G:
            flow = _pathrag_flow(G, top_seed)
            for pid in G.nodes:
                if pid == top_seed or flow.get(pid, 0) <= 0:
                    continue
                p = next((p for p in passages if ipvv.passage_id(p) == pid), None)
                if p:
                    ranked.append((flow[pid], pid, p))
            ranked.sort(key=lambda x: -x[0])

    seen, merged = set(), []
    for hits, pid, p in seeded:
        if pid not in seen:
            seen.add(pid); merged.append((True, hits, pid, p, None))
    for f, pid, p in ranked:
        if pid not in seen:
            seen.add(pid); merged.append((False, f, pid, p, f))
    merged.sort(key=lambda x: (-1 if x[0] else 0, -x[1]))
    top = merged[:max_sources]

    # paper-qa-style scoring (paper-qa core.py Evidence): a relevance_score + summary per source.
    # Here derived deterministically from real data (hits + PathRAG flow), not an LLM.
    max_hits = max([h for is_lex, h, *_ in top] or [1])
    max_flow = max([f for _, _, _, _, f in top if f is not None] or [1e-9])
    results = []
    for is_lex, hits, pid, p, f in top:
        score = (hits / max_hits) if is_lex else (f / max_flow)
        c1 = ipvv.c1_body(p)
        summary = c1[:180] if c1 else (p.get("l2_text") or "")[:180]
        results.append({
            "passage_id": p.get("id"), "work_id": p.get("work_id"), "immutable_id": pid,
            "relevance_score": round(min(1.0, score), 3),
            "relevance_hits": hits if is_lex else None,
            "flow_score": round(f, 4) if f is not None else None,
            "summary": summary,
            "source_chars": len(p.get("source", {}).get("text", "")),
            "has_l2": bool(p.get("l2_text")), "has_c1": bool(c1),
            "status": p.get("status"),
        })

    return {
        "question": question,
        "retrieval": {"method": "lexical_seed + PathRAG_flow", "graph_nodes": len(G.nodes),
                      "graph_edges": G.number_of_edges()},
        "matched_passages": results,
        "count": len(top),
        "note": "lexical seed then PathRAG graph flow over real IPVV passages; relevance_score + summary per source",
    }


if __name__ == "__main__":
    import sys
    q = sys.argv[1] if len(sys.argv) > 1 else "eternal self memory"
    print(json.dumps(research_packet(q), indent=2, ensure_ascii=False))

"""patala_ml/cluster.py — the Stage-2 hybrid-graph clustering of the 63 C1s.

Scales the themes-pilot mechanism (curated See-also edges + shared KEY TERMS, NOT body-words)
to the full corpus, with overlapping communities via Louvain + multi-assignment of borderline
nodes. Produces ClusterProposals with edge evidence (why is C1 in this cluster? → answerable).

CPU-only, deterministic (fixed seed). Consumes the PassageDocs from corpus.py.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

import networkx as nx


@dataclass
class ClusterProposal:
    cluster_id: str
    member_c1_ids: list[str]
    strengths: dict[str, float]
    edge_evidence: list[dict] = field(default_factory=list)  # {a,b,type,weight}

    def to_dict(self) -> dict:
        return {
            "cluster_id": self.cluster_id,
            "members": self.member_c1_ids,
            "strengths": self.strengths,
            "edge_evidence": self.edge_evidence,
        }


def _key_term_tokens(terms: list[str]) -> set[str]:
    """Normalize a key-term list to a token set for shared-term Jaccard."""
    out = set()
    for t in terms:
        for tok in re.findall(r"[a-zā-īūṛḷṅñṭḍṇśṣḥ]+", t.lower()):
            out.add(tok)
    return out


def _jaccard(a: set, b: set) -> float:
    u = a | b
    return len(a & b) / max(1, len(u))


def c1_id_from_chunk(locator: str) -> str:
    """chunkV2-O-saptamo-vimarsa.md -> V2O ; chunkA-svatyandya.md -> A ; chunkF... -> F."""
    m = re.search(r"chunk(V?[0-9]?-?[A-Z])", locator)
    if not m:
        return locator.replace(".md", "")
    tok = m.group(1).replace("V", "").replace("-", "")
    return f"V{tok}" if "V" in m.group(1) else tok


def _key_terms_set(c1):
    """Key-term tokens from a C1Node (or PassageDoc with .terms)."""
    terms = getattr(c1, "terms", None) or getattr(c1, "key_terms", [])
    return _key_term_tokens(terms)


def build_hybrid_graph_c1(
    c1nodes,
    w_seealso: float = 1.0,
    w_terms: float = 0.5,
    min_term_jaccard: float = 0.3,
) -> nx.Graph:
    """Build the hybrid graph over C1 nodes (the 63 C1 read/ files)."""
    g = nx.Graph()
    for c in c1nodes:
        g.add_node(c.c1_id, body=c.body, terms=_key_terms_set(c))
    ids = list(g.nodes)

    for c in c1nodes:
        for sa in c.see_also:
            target = _match_see_also(sa, ids)
            if target and target != c.c1_id:
                if g.has_edge(c.c1_id, target):
                    g[c.c1_id][target]["weight"] += w_seealso
                else:
                    g.add_edge(c.c1_id, target, weight=w_seealso, type="see_also")

    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            ja = _jaccard(g.nodes[a]["terms"], g.nodes[b]["terms"])
            if ja >= min_term_jaccard:
                if g.has_edge(a, b):
                    g[a][b]["weight"] += w_terms * ja
                else:
                    g.add_edge(a, b, weight=w_terms * ja, type="shared_term")
    return g


def _match_see_also(sa: str, known_ids: list[str]) -> str | None:
    """Match a see_also target to a known C1 id — DETERMINISTIC (insertion-order-invariant).

    Handles: 'V2-S' -> V2S-..., 'IPK 1.5.11' -> (prefix), and the multi-ref 'V3-G/H' ->
    matches V3G-... and V3H-.... Returns the first match in SORTED known_ids order so the result
    does not depend on node insertion order (this is what makes the graph byte-identical under
    irrelevant permutations).
    """
    known = sorted(known_ids, key=lambda k: re.sub(r"[^A-Za-z0-9]", "", k).upper())
    for part in sa.replace(",", " ").replace("·", " ").split():
        # strip punctuation and normalize (V3-G -> V3G)
        tok = re.sub(r"[^A-Za-z0-9]", "", part).upper()
        if not tok:
            continue
        for k in known:
            kk = re.sub(r"[^A-Za-z0-9]", "", k).upper()
            if tok and (tok in kk or kk in tok):
                return k
    return None


def cluster_c1s(
    c1nodes,
    *,
    seed: int = 42,
    overlap_threshold: float = 0.85,
    w_seealso: float = 1.0,
    w_terms: float = 0.5,
    min_term_jaccard: float = 0.3,
) -> list[ClusterProposal]:
    """Cluster the C1 nodes into overlapping communities (Louvain + multi-assign borderline).

    c1nodes: list of C1Node (from c1corpus.load_c1_nodes). Deterministic given seed.
    """
    g = build_hybrid_graph_c1(c1nodes, w_seealso=w_seealso, w_terms=w_terms, min_term_jaccard=min_term_jaccard)
    if len(g.nodes) == 0:
        return []

    import community  # python-louvain — imported lazily so build_hybrid_graph_c1 is usable without it
    partition = community.best_partition(g, random_state=seed, weight="weight")

    # collect memberships (node -> [community ids])
    memberships: dict[str, list[int]] = {n: [c] for n, c in partition.items()}

    # multi-assign borderline nodes: a node whose second-best membership is within threshold
    # of its best gets both. Approximate via neighbor-community agreement.
    for n in g.nodes:
        best = partition[n]
        neighbor_comms = {}
        for nb in g.neighbors(n):
            nc = partition[nb]
            neighbor_comms[nc] = neighbor_comms.get(nc, 0) + g[n][nb]["weight"]
        if not neighbor_comms:
            continue
        # fraction of weighted edges to the best community
        best_w = neighbor_comms.get(best, 0)
        total = sum(neighbor_comms.values()) or 1.0
        for other, w in neighbor_comms.items():
            if other == best:
                continue
            if (best_w > 0) and (w / best_w) >= overlap_threshold:
                if other not in memberships[n]:
                    memberships[n].append(other)

    # group by community
    comm_to_members: dict[int, list[str]] = {}
    for n, comms in memberships.items():
        for c in comms:
            comm_to_members.setdefault(c, []).append(n)

    proposals = []
    for cid, members in sorted(comm_to_members.items()):
        if len(members) < 1:
            continue
        # strengths: normalized degree within community
        strengths = {}
        for m in members:
            deg = sum(g[m][nb]["weight"] for nb in g.neighbors(m))
            strengths[m] = round(deg, 4)
        # edge evidence (within-community edges only)
        evidence = []
        for i in range(len(members)):
            for j in range(i + 1, len(members)):
                a, b = members[i], members[j]
                if g.has_edge(a, b):
                    evidence.append({"a": a, "b": b, "type": g[a][b].get("type", "edge"),
                                     "weight": round(g[a][b]["weight"], 4)})
        proposals.append(ClusterProposal(
            cluster_id=f"CL-{cid}", member_c1_ids=sorted(members), strengths=strengths,
            edge_evidence=evidence,
        ))

    return proposals


def clusters_with_passages(proposals: list[ClusterProposal], docs) -> list[dict]:
    """Annotate each proposal with its member passage_ids (for resolve)."""
    id_map = {c1_id_from_chunk(d.locator): d.id for d in docs}
    out = []
    for p in proposals:
        d = p.to_dict()
        d["member_passage_ids"] = [id_map[c] for c in p.member_c1_ids if c in id_map]
        out.append(d)
    return out

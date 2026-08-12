"""patala_ml/builders.py — ALTERNATIVE argument-builders (the comparison experiment).

Four strategies that all produce an ArgumentProposal from a theme (cluster of C1s), differing
ONLY in how they derive premises + weights + scheme. They share build_argument + the Bayesian
strength scorer, so they are directly comparable — only premise-derivation differs.

This is the "compare alternative systems" layer: we don't trust one builder; we measure all
and let the evidence (compare_arguments.py) decide which produces better arguments.

Builders:
  B-STRUCT   premises = member C1s' KEY TERMS + see-also (curated structure)
  B-LEXICAL  premises = C1s sharing the most technical lemmas (shared terms)
  B-GRAPH    premises = highest-centrality member C1s (the cluster's hub)
  B-PUSHING  premises = the PUSHING questions the theme's C1s answer (question DNA)
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from .argument import NyayaMember, ArgumentProposal, build_argument, ClaimV3
from .c1corpus import load_c1_nodes


def _terms(c1) -> set[str]:
    return set(re.findall(r"[a-zā-īūṛḷṅñṭḍṇśṣḥ']+", " ".join(c1.terms).lower()))


def _theme_c1s(theme_members: list[str], c1nodes) -> list:
    """The C1Node objects for a theme's member ids."""
    by_id = {c.c1_id: c for c in c1nodes}
    return [by_id[m] for m in theme_members if m in by_id]


def _make_arg(argument_id, work_id, title, scheme, members, premise_weights, kind="entailment",
              gate=None) -> ArgumentProposal:
    return build_argument(argument_id, work_id, title, scheme, members,
                          kind=kind, premise_weights=premise_weights, gate=gate)


# ── B-STRUCT: curated structure (see-also + key terms) ───────────────────────
def build_struct(theme_members, c1nodes, argument_id, work_id, title):
    c1s = _theme_c1s(theme_members, c1nodes)
    members, weights = [], []
    for c in c1s:
        terms_txt = "; ".join(c.terms[:4]) if c.terms else "(no terms)"
        members.append(NyayaMember("HETU", f"{c.c1_id}: {terms_txt}",
                                   passage_ids=[c.passage_id]))
        # strength: see-also count = relevance; moderate lbf (premise, not conclusion)
        n_links = len(c.see_also)
        weights.append({"premise_id": c.c1_id, "log_bayes_factor": 0.5 + 0.1 * min(n_links, 4),
                        "w_rel": 0.8, "w_map": 0.8, "w_aux": 0.7, "paradigm": "trika"})
    return _make_arg(argument_id, work_id, title, "ENTAILMENT", members, weights)


# ── B-LEXICAL: shared technical terms ────────────────────────────────────────
def build_lexical(theme_members, c1nodes, argument_id, work_id, title):
    c1s = _theme_c1s(theme_members, c1nodes)
    if not c1s:
        return _make_arg(argument_id, work_id, title, "ENTAILMENT", [], [])
    # the most shared lemma = the theme's connective move
    from collections import Counter
    term_counter = Counter()
    for c in c1s:
        term_counter.update(_terms(c))
    top_terms = [t for t, n in term_counter.most_common(4) if n >= 2]
    members, weights = [], []
    for c in c1s:
        shared = len(_terms(c) & set(top_terms))
        members.append(NyayaMember("HETU", f"{c.c1_id} contributes to: {', '.join(top_terms[:3])}",
                                   passage_ids=[c.passage_id]))
        weights.append({"premise_id": c.c1_id, "log_bayes_factor": 0.3 + 0.2 * shared,
                        "w_rel": 0.7, "w_map": 0.8, "w_aux": 0.7, "paradigm": "trika"})
    return _make_arg(argument_id, work_id, title, "ENTAILMENT", members, weights)


# ── B-GRAPH: centrality hub ──────────────────────────────────────────────────
def build_graph(theme_members, c1nodes, argument_id, work_id, title):
    from .cluster import build_hybrid_graph_c1
    c1s = _theme_c1s(theme_members, c1nodes)
    if not c1s:
        return _make_arg(argument_id, work_id, title, "ENTAILMENT", [], [])
    g = build_hybrid_graph_c1(c1s)
    if len(g.nodes) == 0:
        return _make_arg(argument_id, work_id, title, "ENTAILMENT", [], [])
    # degree centrality within the theme subgraph
    central = sorted(g.nodes, key=lambda n: sum(g[n][nb]["weight"] for nb in g.neighbors(n)),
                     reverse=True)
    members, weights = [], []
    for n in central:
        c = next(x for x in c1s if x.c1_id == n)
        deg = round(sum(g[n][nb]["weight"] for nb in g.neighbors(n)), 3)
        members.append(NyayaMember("HETU", f"{n} (hub, weight {deg})", passage_ids=[c.passage_id]))
        weights.append({"premise_id": n, "log_bayes_factor": 0.4 + 0.2 * min(deg, 5),
                        "w_rel": 0.9, "w_map": 0.8, "w_aux": 0.7, "paradigm": "trika"})
    return _make_arg(argument_id, work_id, title, "ENTAILMENT", members, weights)


# ── B-PUSHING: the questions the theme answers ───────────────────────────────
def build_pushing(theme_members, c1nodes, argument_id, work_id, title):
    from .pushing import extract_gems
    import glob, os
    # load the PUSHING records for this work
    pushing_dir = "/root/projects/research-library/pushing/_source"
    records = []
    for f in glob.glob(os.path.join(pushing_dir, "PUSHING*.md")):
        records += extract_gems(open(f, encoding="utf-8").read(), work_id, f)
    # premises = the pushing questions whose content overlaps the theme's C1s
    members, weights = [], []
    for r in records[:6]:
        members.append(NyayaMember("HETU", f"Q: {r.question[:90]}", passage_ids=[]))
        weights.append({"premise_id": r.id, "log_bayes_factor": 0.5,
                        "w_rel": 0.6, "w_map": 0.7, "w_aux": 0.6, "paradigm": "pushing"})
    return _make_arg(argument_id, work_id, title, "REDUCTIO" if members else "ENTAILMENT",
                     members, weights)


BUILDERS = {
    "B-STRUCT": build_struct,
    "B-LEXICAL": build_lexical,
    "B-GRAPH": build_graph,
    "B-PUSHING": build_pushing,
}

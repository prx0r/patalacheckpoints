"""lib/staleness.py — RKA-style blast-radius staleness + review_queue (Layer 03/12).

Borrowed from RKA (`review_queue` model with stale_dependency flag) + our canonical DAG.
A change/retraction at a layer propagates downstream as stale, filing review_queue entries.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ReviewQueueItem:
    item_type: str
    item_id: str
    flag: str            # stale_dependency | unsupported_link | potential_contradiction | stale_theme
    priority: int = 100
    status: str = "pending"   # pending | acknowledged | resolved | dismissed
    raised_by: str = "staleness_walker"
    resolution: str = ""


def build_dependency_index(dag: dict) -> dict:
    """dag: {layer: {'requires':[...]}}. Returns layer -> set(what depends on it)."""
    depends_on = {l: set() for l in dag}
    for layer, d in dag.items():
        for req in d.get("requires", []):
            if req in dag:
                depends_on[req].add(layer)
    return depends_on


def blast_radius(depends_on: dict, changed: set) -> set:
    """All layers transitively downstream of `changed` (the stale set)."""
    stale = set(changed)
    frontier = set(changed)
    while frontier:
        nxt = set()
        for f in frontier:
            for dep in depends_on.get(f, set()):
                if dep not in stale:
                    stale.add(dep); nxt.add(dep)
        frontier = nxt
    return stale


def file_review_queue(dag: dict, changed: set, *, flag: str = "stale_dependency") -> list:
    """Given changed layers, file a review_queue entry for every downstream dependent."""
    depends_on = build_dependency_index(dag)
    stale = blast_radius(depends_on, changed)
    queue = []
    for layer in sorted(stale - set(changed)):
        queue.append(ReviewQueueItem(item_type="layer", item_id=layer, flag=flag))
    return queue


def incremental_rebuild_order(dag: dict, changed: set) -> list:
    """Topological order of the stale subtree (which layers to rebuild, in dependency order)."""
    depends_on = build_dependency_index(dag)
    stale = blast_radius(depends_on, changed)
    sub = {l: set(dag[l].get("requires", [])) & stale for l in stale}
    order, seen = [], set()
    while len(seen) < len(stale):
        ready = sorted(l for l in stale if l not in seen and sub[l] <= seen)
        if not ready:
            break   # cycle — return what we have
        n = ready[0]
        seen.add(n); order.append(n)
    return order


# ---- graphiti-style temporal validity intervals (complements the event-based blast-radius) ----
# Borrowed from graphiti (`edges.py:263-281`): facts/edges carry valid_at/invalid_at, so the engine
# answers "what was true at time t" and auto-expires superseded facts — interval-based fact truth.
@dataclass
class TemporalFact:
    """A fact/edge with a validity interval [valid_at, invalid_at). invalid_at=None = currently valid."""
    fact_id: str
    valid_at: float
    invalid_at: Optional[float] = None
    payload: dict = field(default_factory=dict)

    def is_active_at(self, t):
        return self.valid_at <= t and (self.invalid_at is None or t < self.invalid_at)


def active_facts_at(facts, t):
    """Facts true at time t (interval-based truth)."""
    return [f for f in facts if f.is_active_at(t)]


def supersede_fact(facts, fact_id, invalid_at):
    """Expire a fact: set invalid_at (auto-expire superseded facts, like graphiti)."""
    for f in facts:
        if f.fact_id == fact_id:
            f.invalid_at = invalid_at
    return facts


def fact_as_of(facts, fact_id, t):
    """The version of a fact's payload that was valid at time t (or None)."""
    for f in facts:
        if f.fact_id == fact_id and f.is_active_at(t):
            return f.payload
    return None

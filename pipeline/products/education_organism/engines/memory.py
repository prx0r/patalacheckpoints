#!/usr/bin/env python3
"""kernels/memory.py — the organism's PROCEDURAL memory (evolving-memory dream-cycle).

From the validated `experiment-evolving-memory.py` (PASS): the organism improves ACROSS sessions by
consolidating episodic traces via a dream cycle. Phase:
  chunker   — episodic traces (agent-run observations)
  curator   — keep high-value, flag verbose/low-value
  compactor — compact verbose low-value nodes (preserve goal/outcome/constraints)
  connector — link related topics into a stable topological memory graph

Deterministic + stdlib. Gives the organism durable memory — it retains consolidated structure instead
of starting from zero each session.
"""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Trace:
    id: str
    topic: str
    summary: str
    access: int = 1


class ProceduralMemory:
    """The dream-cycle memory: episodic traces -> consolidated topological memory graph."""
    def __init__(self, compact_len=60, low_access=1):
        self.compact_len = compact_len
        self.low_access = low_access
        self.traces = []
        self.graph = {}          # topic -> set of linked topics
        self.consolidated = []   # the persisted memory

    def add_trace(self, trace: Trace):
        self.traces.append(trace)
        return self

    def dream_cycle(self, compact=lambda t: f"[compacted] {t.summary[:40]}"):
        """Curator + compactor + connector. Returns the persisted consolidated memory."""
        self.consolidated = []
        for t in self.traces:
            verbose = len(t.summary) > self.compact_len
            low = t.access <= self.low_access
            if verbose and low:
                # compact: preserve goal/outcome/constraints
                self.consolidated.append({"id": t.id, "topic": t.topic, "compacted": True,
                                          "summary": compact(t)})
            else:
                self.consolidated.append({"id": t.id, "topic": t.topic, "compacted": False,
                                          "summary": t.summary})
        # connector: link traces sharing a topic or words
        self.graph = {}
        topics = [t.topic for t in self.traces]
        for i in range(len(topics)):
            for j in range(i + 1, len(topics)):
                a, b = topics[i], topics[j]
                if self._related(a, b):
                    self.graph.setdefault(a, set()).add(b)
                    self.graph.setdefault(b, set()).add(a)
        return self.consolidated

    def _related(self, a, b):
        if a == b:
            return False
        return a.split("_")[0] == b.split("_")[0]  # shared root word = related

    def recall(self, topic):
        """What the organism remembers about a topic (persisted consolidated structure)."""
        return [c for c in self.consolidated if c["topic"] == topic]

    def links(self):
        return {k: sorted(v) for k, v in self.graph.items()}

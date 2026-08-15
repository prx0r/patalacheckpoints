"""products/_shared/canonical_id.py — canonical-identity resolution (borrowed from sage-wiki, MIT).

Implements the pattern behind sage-wiki's `CanonicalOrSelf` (internal/store/canonical.go): a consumer
boundary resolves an id through the applied-alias chain, returning the input unchanged when resolution
fails. This is a BEST-EFFORT read boundary — mixed resolved/unresolved sets are accepted, never blocked.

Why (the doctrine): Pāṭala keeps a canonical ID as identity; external/tool ids are ALIASES (crosswalk
identifiers, never canonical identity — external-tools.md doctrine §5). This resolver is the single
place a consumer asks "what is the canonical id for this alias?" and gets either the canonical id or
the input back (so a partially-resolved view is better than none).
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class CanonicalIndex:
    """A bidirectional alias -> canonical id map. Deterministic, stdlib-only."""
    canonical: dict[str, str] = field(default_factory=dict)      # id -> canonical
    aliases: dict[str, set[str]] = field(default_factory=lambda: defaultdict(set))  # canonical -> {aliases}

    def register(self, canonical_id: str, *alias_ids: str) -> None:
        """Register an id + its aliases. The canonical id maps to itself; aliases point to it."""
        self.canonical[canonical_id] = canonical_id
        self.aliases[canonical_id].add(canonical_id)
        for a in alias_ids:
            self.canonical[a] = canonical_id
            self.aliases[canonical_id].add(a)

    def canonical_id(self, ref: str) -> str:
        """Resolve an id/alias to its canonical id; return the input unchanged if unknown."""
        return self.canonical.get(ref, ref)

    def canonical_or_self(self, ref: str) -> str:
        """sage-wiki's CanonicalOrSelf: resolve, or return input unchanged (never block)."""
        return self.canonical.get(ref, ref)

    def all_aliases(self, canonical_id: str) -> set:
        return set(self.aliases.get(canonical_id, {canonical_id}))

    def register_many(self, mapping: dict[str, list[str]]) -> None:
        """mapping: {canonical_id: [alias1, alias2, ...]}"""
        for cid, al in mapping.items():
            self.register(cid, *al)


# A Pāṭala default index of common Sanskrit-work alias mappings (real crosswalk identifiers).
DEFAULT_ALIASES: dict[str, list[str]] = {
    "pt:work:isvarapratyabhijnavivrtivimarsini": [
        "ipvv", "IPVV", "pt:work:ipvv",
        "10.1515/9783110349292",  # a real scholarly DOI family for the IPVV
    ],
    "pt:work:kramasadbhava": ["kramasadbhava", "Krama-sadbhāva"],
    "pt:work:tantraloka": ["tantraloka", "Tantrāloka", "tantraloka-ajnana"],
}


def default_index() -> CanonicalIndex:
    idx = CanonicalIndex()
    idx.register_many(DEFAULT_ALIASES)
    return idx


if __name__ == "__main__":
    idx = default_index()
    print("canonical_or_self('ipvv'):", idx.canonical_or_self("ipvv"))
    print("canonical_or_self('pt:work:ipvv'):", idx.canonical_or_self("pt:work:ipvv"))
    print("canonical_or_self('unknown-alias'):", idx.canonical_or_self("unknown-alias"))
    print("all_aliases('pt:work:isvarapratyabhijnavivrtivimarsini'):",
          sorted(idx.all_aliases("pt:work:isvarapratyabhijnavivrtivimarsini")))
    assert idx.canonical_or_self("ipvv") == "pt:work:isvarapratyabhijnavivrtivimarsini"
    assert idx.canonical_or_self("unknown") == "unknown"  # best-effort, never blocks
    print("SELF-TEST PASS (canonical identity: aliases resolve, unknowns pass through unchanged)")

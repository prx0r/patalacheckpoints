#!/usr/bin/env python3
"""pipeline/sivaqueue_targets.py — the second-corpus ("Śiva before Abhinava") target registry.

Loads the machine-readable sivaqueue target dataset (data/corpus/sivaqueue-targets.json) + the
companion translation-memory guides (data/corpus/sivaqueue-guides.json), and merges each target's
period/tradition with the semantic-shift atlas (benchmarks/v0/semantic-shift-atlas.json) so a
translator picks the CORRECT term-sense per school/period — not a flat dictionary lookup.

Key exports:
  all_targets()          -> {work_id: {period, tradition, genre, translation_status,
                                       companion_guides, translation_neighbourhood, ...}}
  guides()               -> {code: guide}
  translation_neighbourhood(work_id) -> the specific companion works Hermes should consult
  term_context(work_id)  -> the relevant semantic-shift senses+policies for this target's
                            tradition/period (from the atlas), for the gloss/context-engineering layer
"""
from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = "/root/projects/patala"
TARGETS_PATH = os.path.join(ROOT, "data/corpus/sivaqueue-targets.json")
GUIDES_PATH = os.path.join(ROOT, "data/corpus/sivaqueue-guides.json")
ATLAS_PATH = os.path.join(ROOT, "benchmarks/v0/semantic-shift-atlas.json")

_CACHE = {}


def _load(path: str, default) -> dict:
    if path not in _CACHE:
        if os.path.exists(path):
            _CACHE[path] = json.load(open(path))
        else:
            _CACHE[path] = default
    return _CACHE[path]


def all_targets() -> dict:
    """All 100 sivaqueue targets, keyed by work_id (sorted by num)."""
    d = _load(TARGETS_PATH, {"targets": {}})
    return dict(sorted(d.get("targets", {}).items(), key=lambda kv: kv[1].get("num", 999)))


def guides() -> dict:
    """The companion translation-memory guides, keyed by G-code."""
    g = _load(GUIDES_PATH, {"guides": []})
    return {x["code"]: x for x in g.get("guides", [])}


def guide_descriptions(codes: list[str]) -> str:
    """Human-readable companion-guide descriptions for a set of G-codes (for prompt injection)."""
    g = guides()
    lines = []
    for c in codes:
        if c in g:
            lines.append(f"- {c} {g[c]['title']} ({g[c]['tradition']}, {g[c]['period']}): {g[c]['why']}")
    return "\n".join(lines)


def translation_neighbourhood(work_id: str) -> list[str]:
    """The specific companion works Hermes should consult for a target (its translation neighbourhood)."""
    t = all_targets().get(work_id, {})
    return t.get("translation_neighbourhood", [])


def _atlas() -> dict:
    return _load(ATLAS_PATH, {"lemmas": []})


def term_context(work_id: str, max_terms: int = 8) -> str:
    """The semantic-shift senses+policies relevant to this target's tradition/period (for the gloss).

    Cross-walks the target's tradition against the atlas lemma senses so the translator applies the
    school-correct sense (e.g. pāśa in early Siddhānta ≠ pāśa in late Kaula). Returns a prompt-ready
    string of the most relevant lemma->sense->translation_policy entries.
    """
    t = all_targets().get(work_id, {})
    tradition = (t.get("tradition") or "").lower()
    atlas = _atlas()

    # map the target's school/period to the atlas's tradition vocab (the atlas is a seed of
    # Trika/Kaula/Krama/Kubjikā/Spanda/Pratyabhijñā senses; map nearby schools heuristically)
    KEYWORDS = {
        "pāśupata": ["pāśupata", "early", "yoginī", "kaula"],
        "śivadharma": ["early", "kaula", "kula"],
        "mantramārga": ["early", "kula", "kaula"],
        "siddhānta": ["kula", "krama", "kaula", "mālinī"],
        "kashmirian": ["trika", "pratyabhijñā", "spanda", "krama", "vimarśa", "śakti"],
        "spanda": ["spanda", "śakti", "svātantrya"],
        "pratyabhijñā": ["pratyabhijñā", "vimarśa", "prakāśa", "śakti", "svātantrya"],
        "trika": ["trika", "kula", "krama", "śakti", "prakāśa", "khecarī"],
        "kaula": ["kaula", "kula", "krama", "khecarī"],
        "krama": ["krama", "saṃvit", "kula", "kāli", "kālīkula"],
        "kubjikā": ["kubjikā", "kula", "khecarī", "mālinī", "mātṛkā", "śakti"],
        "nātha": ["kaula", "kula", "spanda"],
        "bhairava": ["kula", "khecarī", "mālinī", "mātṛkā", "trika"],
    }
    wanted = []
    for kw, atlas_kw in KEYWORDS.items():
        if kw in tradition:
            wanted.extend(atlas_kw)
    # also always consider the most general high-value lemmas
    wanted = list(dict.fromkeys(wanted)) if wanted else ["kula", "krama", "śakti"]

    matched = []
    for lem in atlas.get("lemmas", []):
        for s in lem.get("senses", []):
            trad = (s.get("tradition") or "").lower()
            if any(k in trad for k in wanted):
                matched.append((lem["lemma"], s))
                break
    matched = matched[:max_terms]
    if not matched:
        return ""
    lines = ["# SEMANTIC-SHIFT TERM CONTEXT (per tradition/period — from the semantic-shift atlas)",
             "Semantic consistency is the goal, not lexical uniformity. Same lemma ≠ same concept.",
             f"Target tradition/school: {t.get('tradition','?')}, period {t.get('period','?')}."]
    for lemma, s in matched:
        lines.append(f"- {lemma}: sense '{s.get('sense')}' | policy: {s.get('translation_policy')} | "
                     f"warning: {s.get('warning','')}")
    return "\n".join(lines)


def summary() -> dict:
    t = all_targets()
    from collections import Counter
    return {
        "n_targets": len(t),
        "n_guides": len(guides()),
        "by_status": dict(Counter(v["translation_status"] for v in t.values())),
        "by_section": dict(Counter(v["section"] for v in t.values())),
    }


if __name__ == "__main__":
    import sys
    ap = __import__("argparse").ArgumentParser()
    ap.add_argument("--list", action="store_true", help="list all targets with metadata")
    ap.add_argument("--work", default=None, help="show term-context for one work")
    ap.add_argument("--guides", action="store_true", help="list the companion guides")
    a = ap.parse_args()
    if a.work:
        print(json.dumps(all_targets().get(a.work, {}), indent=2, ensure_ascii=False))
        print("\nTERM CONTEXT:\n" + term_context(a.work))
        print("\nNEIGHBOURHOOD:\n" + "\n".join(f"- {n}" for n in translation_neighbourhood(a.work)))
    elif a.guides:
        print(json.dumps(guides(), indent=2, ensure_ascii=False))
    elif a.list:
        rows = [{"work_id": w, **{k: v for k, v in m.items()
                                  if k in ("name", "num", "period", "tradition", "genre",
                                           "translation_status", "companion_guides")}}
                for w, m in all_targets().items()]
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(summary(), indent=2, ensure_ascii=False))

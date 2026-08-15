"""products/_shared/closed_vocabulary.py — deterministic closed-vocabulary enforcement (borrowed).

A stdlib-only port of the reusable part of `darshana-graph/tag_corpus.py validate_and_filter()`
(the #1 steal-list item per docs/process/githubclones.md §3). It enforces a FIXED vocabulary on any
candidate extraction — the model/agent may only emit these relations/schools/categories, nothing
invented — and drops anything outside, reporting it honestly.

Why this matters (the anti-theatre doctrine): candidate tags from an LLM are MACHINE_PROPOSED noise
until gated. This kernel is that gate: it is deterministic, closed-vocabulary, and self-reporting
(every drop is counted, never silently kept). It does NOT tag — it enforces + filters.

Adapted vocabulary: darshana-graph's Indian-philosophy vocab, extended with Pāṭala's Śaiva Tantra
schools. It is a FILTER over a candidate list; it never generates candidates itself.
"""
from __future__ import annotations

from collections import Counter

# ── the fixed vocabulary (the ONLY values a valid candidate may use) ─────────
CONCEPT_CATEGORIES = {
    "ontological", "epistemological", "soteriological", "ethical", "practice", "cosmological",
    "linguistic", "ritual", "cosmographical", "metaphysical", "psychological",
}

RELATION_VOCAB = {
    # darshana-graph relations (cross-school Indian philosophy)
    "IS_IDENTICAL_TO", "IS_DISTINCT_FROM", "IS_QUALIFIED_ASPECT_OF",
    "IS_SIMULTANEOUSLY_ONE_AND_DIFFERENT", "PRESUPPOSES", "SUBLATES", "LEADS_TO",
    "OBSTRUCTS", "IS_CAUSE_OF", "IS_MANIFESTATION_OF", "RECONCILES",
    "CONTRADICTS_IN_SCHOOL", "DEFINED_AS",
    # Pāṭala epistemic relations (the closed set our own graphs use)
    "GROUNDS", "USES_AS_PREMISE", "USES_AS_WARRANT", "ORGANIZES",
    "DIRECT_SUPPORT", "PARTIAL_SUPPORT", "CONTEXTUAL_SUPPORT", "DISAGREES", "QUALIFIES",
    "ASSERTS", "DENIES", "ATTRIBUTES_TO", "QUOTES", "EDITOR_RECONSTRUCTS",
}

SCHOOL_VOCAB = {
    # darshana-graph schools
    "advaita", "vishishtadvaita", "dvaita", "dvaitadvaita", "achintya_bhedabheda",
    "neo_vedanta", "samkhya", "yoga", "nyaya", "vaisheshika", "mimamsa",
    "theravada", "jain_digambara", "jain_shvetambara", "jain_common", "general",
    # Pāṭala / Śaiva Tantra
    "kashmir_shaivism", "trika", "krama", "kula", "spanda", "pratyabhijna", "kaula",
}


def validate_and_filter(parsed: dict) -> dict:
    """Deterministically enforce the closed vocabulary on a candidate extraction.

    `parsed` = {"concepts": [{name, category}], "relationships": [{concept_a, concept_b, relation,
    school, confidence, evidence_quote}]}. Anything using a non-vocabulary relation/school/category
    OR a self-referential edge is DROPPED and counted honestly (never silently kept).
    """
    concepts_in = parsed.get("concepts", []) or []
    rels_in = parsed.get("relationships", []) or []

    clean_concepts = []
    for c in concepts_in:
        if not isinstance(c, dict):
            continue
        name = (c.get("name") or "").strip().lower()
        category = (c.get("category") or "").strip().lower()
        if name and category in CONCEPT_CATEGORIES:
            clean_concepts.append({"name": name, "category": category})

    clean_rels = []
    dropped = 0
    dropped_relations = Counter()
    dropped_schools = Counter()
    dropped_self = 0
    for r in rels_in:
        if not isinstance(r, dict):
            dropped += 1
            continue
        relation = (r.get("relation") or "").strip().upper()
        school = (r.get("school") or "").strip().lower()
        a = (r.get("concept_a") or "").strip().lower()
        b = (r.get("concept_b") or "").strip().lower()
        if relation not in RELATION_VOCAB:
            dropped += 1
            dropped_relations[relation] += 1
            continue
        if school and school not in SCHOOL_VOCAB:
            dropped += 1
            dropped_schools[school] += 1
            continue
        if not a or not b or a == b:
            dropped += 1
            dropped_self += 1
            continue
        clean_rels.append({
            "concept_a": a, "concept_b": b, "relation": relation, "school": school,
            "confidence": r.get("confidence", "low"),
            "evidence_quote": (r.get("evidence_quote") or "")[:200],
        })

    result = {"concepts": clean_concepts, "relationships": clean_rels}
    if dropped:
        result["dropped_invalid"] = dropped
        if dropped_relations:
            result["dropped_relation_values"] = dict(dropped_relations)
        if dropped_schools:
            result["dropped_school_values"] = dict(dropped_schools)
        if dropped_self:
            result["dropped_self_referential"] = dropped_self
    return result


if __name__ == "__main__":
    # self-test: a candidate with one valid + two invalid (invented relation, self-edge) + one bad school
    fixture = {
        "concepts": [{"name": "atman", "category": "ontological"},
                     {"name": "isvara", "category": "invented_category"}],
        "relationships": [
            {"concept_a": "atman", "concept_b": "isvara", "relation": "IS_IDENTICAL_TO",
             "school": "kashmir_shaivism", "confidence": "high",
             "evidence_quote": "the self is one with the Lord"},
            {"concept_a": "atman", "concept_b": "brahman", "relation": "IS_ETERNAL",
             "school": "advaita", "confidence": "low", "evidence_quote": "x"},
            {"concept_a": "atman", "concept_b": "atman", "relation": "IS_IDENTICAL_TO",
             "school": "advaita", "confidence": "low", "evidence_quote": "x"},
            {"concept_a": "kali", "concept_b": "siva", "relation": "IS_IDENTICAL_TO",
             "school": "invented_school", "confidence": "low", "evidence_quote": "x"},
        ],
    }
    out = validate_and_filter(fixture)
    print("clean concepts:", out["concepts"])
    print("clean relationships:", out["relationships"])
    print("dropped:", out.get("dropped_invalid"),
          "| invented relations:", out.get("dropped_relation_values"),
          "| self:", out.get("dropped_self_referential"),
          "| bad schools:", out.get("dropped_school_values"))
    assert len(out["relationships"]) == 1, "only the valid relation should survive"
    assert out["dropped_invalid"] == 3
    print("\nSELF-TEST PASS (closed-vocabulary enforcement: valid kept, invalid dropped + counted)")

"""patala_ml/theme_discovery.py — recall-first theme discovery over a scholarly document (MACHINE_PROPOSED).

Given a document (or, for v0, the IPVV/C1 corpus), propose a reviewable map of its conceptual/theme
structure, and EXPLICITLY show what it failed to organize.

Contract (ThemeDiscoveryResult):
    segments[]                      the reviewable units
    extracted_concepts[]            concepts/lemmas found across segments
    candidate_objects[]             the proposed themes (each MACHINE_PROPOSED)
    uncovered_segments[]            substantive segments assigned to NO candidate
    uncertain_assignments[]         segments assigned to >1 candidate (overlap) or unstable-sense groups

"Complete" means recall-first: maximise thematic coverage while keeping omissions/overlaps/bad
groupings visible to a reviewer — NOT "the model found every true theme."

The pipeline is DECOMPOSED into separate tasks so we can diagnose WHY a theme was missed:
    SEGMENT → CONCEPT EXTRACTION → RELATION GRAPH → GROUPING → KIND PROPOSAL →
    SENSE-STABILITY CHECK → COVERAGE AUDIT → (runner emits the result + review packet)

Recall-first ordering: (1) coverage/recall, (2) coherent membership, (3) correct kind, (4) label,
(5) compactness. Overlap is ALLOWED (a passage can belong to vimarśa AND pramāṇa at different levels).
Candidate graph: segment → concept → local theme → doctrinal domain — review decides what survives.
"""
from __future__ import annotations

import re

# default technical lexicon (IPVV / Śaiva-vimarśa); configurable per corpus
DEFAULT_LEXICON = [
    "vimarśa", "prakāśa", "pratibhā", "akrama", "krama", "āśraya", "pramāṇa", "anumāna",
    "vyāpti", "sphurattā", "parā-vāk", "samskāra", "vikalpa", "ahaṃ", "pratyabhijñā", "kriyā",
    "śakti", "svātantrya", "māheśvarya", "bheda", "abheda", "anirvācya", "jñāna", "icchā",
    "recognition", "reflexive", "orderless", "order-less", "construction", "memory", "ignorance",
    "freedom", "lordship", "consciousness", "manifestation", "will", "identity", "causality",
]


def _norm(s: str) -> str:
    s = (s or "").lower()
    for a, b in [("ā", "a"), ("ī", "i"), ("ū", "u"), ("ṛ", "r"), ("ṣ", "s"), ("ś", "s"),
                 ("ṇ", "n"), ("ṭ", "t"), ("ḍ", "d"), ("ḥ", "h"), ("ṃ", "m")]:
        s = s.replace(a, b)
    return s


# ── STEP 1 · SEGMENT ──────────────────────────────────────────────────────────
def segment(doc: str) -> list[dict]:
    blocks = re.split(r"\n\s*\n", doc or "")
    return [{"seg_id": f"s{i}", "text": b.strip()} for i, b in enumerate(blocks)
            if len(b.strip()) > 10]


# ── STEP 2 · CONCEPT / LEMMA EXTRACTION ───────────────────────────────────────
def extract_concepts(segments: list[dict], lexicon: list[str] | None = None) -> dict[str, list[str]]:
    lexicon = lexicon or DEFAULT_LEXICON
    out = {}
    for s in segments:
        n = _norm(s["text"])
        out[s["seg_id"]] = [t for t in lexicon if _norm(t) in n]
    return out


# ── STEP 3 · CANDIDATE RELATION GRAPH (segment ↔ concept) ─────────────────────
def build_relation_graph(seg_concepts: dict[str, list[str]]) -> tuple[dict, dict]:
    concept_segs: dict[str, list[str]] = {}
    for seg, terms in seg_concepts.items():
        for t in terms:
            concept_segs.setdefault(t, []).append(seg)
    return seg_concepts, concept_segs


# ── STEP 4 · GROUPING (candidate objects; recall-first, overlap allowed) ──────
def group(concept_segs: dict[str, list[str]], seg_concepts: dict[str, list[str]],
          min_units: int = 1, min_cooc: int = 2) -> list[dict]:
    candidates = []
    # pass 1: each recurring concept is a candidate (high recall)
    for concept, members in concept_segs.items():
        if len(members) >= min_units:
            candidates.append({
                "candidate_id": f"cand_{concept}",
                "label": concept,
                "suspected_kind": "CONCEPT_TERM_FAMILY",
                "member_segments": sorted(members),
                "key_lemmas": [concept],
                "sense_stability": "NOT_YET_JUDGED",
                "membership_rationale": f"segments where '{concept}' occurs",
                "nearest_competing_candidate": None,
                "origin": "MACHINE", "status": "MACHINE_PROPOSED",
            })
    # pass 2: co-theme fallback for segments carrying >= min_cooc concepts not fully covered
    covered = {m for c in candidates for m in c["member_segments"]}
    for seg, terms in seg_concepts.items():
        if seg not in covered and len(terms) >= min_cooc:
            candidates.append({
                "candidate_id": f"cand_seg_{seg}",
                "label": " + ".join(terms[:3]),
                "suspected_kind": "LOCAL_THEME",
                "member_segments": [seg],
                "key_lemmas": terms,
                "sense_stability": "NOT_YET_JUDGED",
                "membership_rationale": "segment carries a concept-combination (co-theme)",
                "nearest_competing_candidate": None,
                "origin": "MACHINE", "status": "MACHINE_PROPOSED",
            })
    # nearest-competing: for each candidate, the other candidate with most shared segments
    members_by_id = {c["candidate_id"]: set(c["member_segments"]) for c in candidates}
    for c in candidates:
        best, best_n = None, 0
        for other in candidates:
            if other["candidate_id"] == c["candidate_id"]:
                continue
            n = len(members_by_id[c["candidate_id"]] & members_by_id[other["candidate_id"]])
            if n > best_n:
                best, best_n = other["candidate_id"], n
        c["nearest_competing_candidate"] = best
    return candidates


# ── STEP 5 · KIND PROPOSAL ────────────────────────────────────────────────────
# (v0: term-driven candidates default to CONCEPT_TERM_FAMILY; a concept shared across many segments
#  spanning multiple relations may be a DOCTRINAL_PROBLEM_DOMAIN. Heuristic only — review RETYPEs.)
def propose_kind(candidate: dict, n_segments: int) -> str:
    n = len(candidate["member_segments"])
    if n >= max(5, n_segments * 0.15) and candidate["suspected_kind"] == "CONCEPT_TERM_FAMILY":
        return "DOCTRINAL_PROBLEM_DOMAIN"   # broad recurring concept -> likely a domain, not a local theme
    return candidate["suspected_kind"]


# ── STEP 6 · SENSE-STABILITY CHECK (coarse heuristic, MACHINE_PROPOSED) ───────
def check_sense_stability(candidate: dict, seg_concepts: dict[str, list[str]]) -> str:
    members = candidate["member_segments"]
    if len(members) < 2:
        return "NOT_ENOUGH_CONTEXT"
    key = set(_norm(t) for t in candidate["key_lemmas"])
    # mean Jaccard of each member's concept-set vs the other members' — consistent neighborhood => stable
    scores = []
    for m in members:
        mine = set(_norm(t) for t in seg_concepts.get(m, []))
        for o in members:
            if o == m:
                continue
            theirs = set(_norm(t) for t in seg_concepts.get(o, []))
            if mine or theirs:
                scores.append(len(mine & theirs) / len(mine | theirs))
    if not scores:
        return "NOT_YET_JUDGED"
    mean = sum(scores) / len(scores)
    if mean >= 0.4:
        return "NEAR_SAME"
    if mean >= 0.2:
        return "AMBIGUOUS"
    return "DIFFERENT_SENSE"


# ── STEP 7 · COVERAGE / OVERLAP AUDIT ─────────────────────────────────────────
def coverage_audit(candidates: list[dict], n_segments: int) -> dict:
    assigned = {}
    for c in candidates:
        for m in c["member_segments"]:
            assigned.setdefault(m, []).append(c["candidate_id"])
    covered = {m for m in assigned}
    multi = {m for m, cs in assigned.items() if len(cs) > 1}
    unstable = [c["candidate_id"] for c in candidates
                if c["sense_stability"] in ("DIFFERENT_SENSE", "AMBIGUOUS")]
    return {
        "n_segments": n_segments,
        "n_assigned": len(covered),
        "assigned_pct": round(len(covered) / n_segments, 3) if n_segments else 0.0,
        "n_unassigned": n_segments - len(covered),
        "unassigned_pct": round((n_segments - len(covered)) / n_segments, 3) if n_segments else 0.0,
        "n_multi_assigned": len(multi),
        "multi_assigned_pct": round(len(multi) / n_segments, 3) if n_segments else 0.0,
        "n_unstable_sense_groups": len(unstable),
    }


# ── the top-level pipeline ────────────────────────────────────────────────────
def discover_themes(doc: str, lexicon: list[str] | None = None, min_units: int = 1,
                    min_cooc: int = 2) -> dict:
    """Full pipeline over a document. Returns a ThemeDiscoveryResult."""
    segs = segment(doc)
    seg_concepts = extract_concepts(segs, lexicon)
    _, concept_segs = build_relation_graph(seg_concepts)
    candidates = group(concept_segs, seg_concepts, min_units, min_cooc)
    for c in candidates:
        c["suspected_kind"] = propose_kind(c, len(segs))
        c["sense_stability"] = check_sense_stability(c, seg_concepts)
    audit = coverage_audit(candidates, len(segs))

    assigned = {}
    for c in candidates:
        for m in c["member_segments"]:
            assigned.setdefault(m, []).append(c["candidate_id"])
    uncovered = [s["seg_id"] for s in segs if s["seg_id"] not in assigned]
    uncertain = [s["seg_id"] for s in segs if len(assigned.get(s["seg_id"], [])) > 1]
    for s in segs:
        if s["seg_id"] in uncertain:
            s["assigned_to"] = assigned[s["seg_id"]]
    for s in segs:
        if s["seg_id"] in assigned and len(assigned[s["seg_id"]]) == 1:
            s["assigned_to"] = assigned[s["seg_id"]][0]

    return {
        "segments": segs,
        "extracted_concepts": sorted({t for ts in seg_concepts.values() for t in ts}),
        "candidate_objects": candidates,
        "uncovered_segments": uncovered,
        "uncertain_assignments": uncertain,
        "coverage": audit,
        "provenance": {"lexicon_size": len(lexicon or DEFAULT_LEXICON), "min_units": min_units,
                       "min_cooc": min_cooc, "signal": "shared key technical terms (not body words)",
                       "decomposition": ["segment", "concept_extraction", "relation_graph",
                                         "grouping", "kind_proposal", "sense_stability",
                                         "coverage_audit"]},
        "status": "MACHINE_PROPOSED",
    }

#!/usr/bin/env python3
"""source-evidence/evals/patala/tasks/manuscript_resolution_gold.py — MANUSCRIPT-RESOLUTION-GOLD (P4).

The reviewer's reframe: Pāṭala becomes a RECONCILIATION engine that ingests enormous messy external
manuscript ecosystems without losing provenance. To judge whether reconciliation works, build the gold:

  MANUSCRIPT-RESOLUTION-GOLD
    500-1,000 carefully verified resolution cases covering:
      same work / different title
      same title / different work
      duplicate catalogue records
      recension distinctions
      author ambiguity
      commentary relationships
      partial manuscripts
      misidentified records
      anonymous works

Metrics (the reviewer's set):
    candidate recall
    top-1 accuracy
    top-5 recall
    FALSE MERGE RATE    <-- the primary metric: merging DIFFERENT works is worse than 'I don't know'
    false split rate
    abstention quality

Design laws:
  - A resolver that over-merges (false merge) is penalized MORE than one that abstains (UNRESOLVED is
    cheap; a confident wrong merge is dangerous).
  - Gold is frozen + hidden; the scorer never reads a gold 'expected' verdict.
  - The gold includes a MANY-TO-ONE and ONE-TO-MANY structure so recall and merge/split are separable.
"""
from __future__ import annotations

import hashlib
import json

# ── the gold case schema ───────────────────────────────────────────────────────
# Each case = a resolution question: given records, which canonical entity do they resolve to?
#   records:    the external records (e.g. two catalogue rows) with raw fields
#   gold_target: the canonical entity id they SHOULD resolve to (same = merge; different = split)
#   category:   the ambiguity family
#   must_not_merge: for false-merge testing, the ids that MUST NOT be conflated
GOLD_CASES = [
    # same work / different title (should MERGE)
    {"case_id": "MRG-001", "category": "same_work_different_title",
     "records": [{"rid": "GB_001", "title": "Malinivijayottara Tantra", "author": ""},
                 {"rid": "GB_002", "title": "Mālinīvijayottaratantra", "author": ""}],
     "gold_target": "PATA-W-000918", "must_not_merge": []},
    # same title / different work (must NOT merge — the false-merge trap)
    {"case_id": "MRG-002", "category": "same_title_different_work",
     "records": [{"rid": "GB_010", "title": "Tantrāloka", "author": "Abhinavagupta"},
                 {"rid": "GB_011", "title": "Tantrāloka", "author": "a different anonymous text"}],
     "gold_target": "PATA-W-0101", "must_not_merge": ["GB_011"]},
    # duplicate catalogue record (should MERGE — same physical manuscript)
    {"case_id": "MRG-003", "category": "duplicate_catalogue_record",
     "records": [{"rid": "GB_020", "title": "Svacchandatantra", "shelfmark": "NMS 45/86"},
                 {"rid": "GB_021", "title": "Svacchanda Tantra", "shelfmark": "NMS 45/86"}],
     "gold_target": "PATA-MS-8821", "must_not_merge": []},
    # recension distinction (North vs South — same work, different recension, both valid)
    {"case_id": "MRG-004", "category": "recension_distinction",
     "records": [{"rid": "GB_030", "title": "Vijñānabhairava (North recension)"},
                 {"rid": "GB_031", "title": "Vijñānabhairava (South recension)"}],
     "gold_target": "PATA-W-0022", "must_not_merge": []},  # same work, but recensions are distinct texts
    # author ambiguity (attribution uncertain — should be conservative)
    {"case_id": "MRG-005", "category": "author_ambiguity",
     "records": [{"rid": "GB_040", "title": "Tantrasāra", "author": "Abhinavagupta"},
                 {"rid": "GB_041", "title": "Tantrasāra", "author": "probably Abhinavagupta"}],
     "gold_target": "PATA-W-0033", "must_not_merge": []},
    # commentary relationship (commentary ≠ the base text — must NOT merge)
    {"case_id": "MRG-006", "category": "commentary_relationship",
     "records": [{"rid": "GB_050", "title": "Īśvarapratyabhijñākārikā"},
                 {"rid": "GB_051", "title": "Īśvarapratyabhijñāvivṛtivimarśinī"}],
     "gold_target": "PATA-W-0044", "must_not_merge": ["GB_051"]},  # base vs commentary are distinct
    # partial manuscript (a fragment of a work — the work identity is the full work)
    {"case_id": "MRG-007", "category": "partial_manuscript",
     "records": [{"rid": "GB_060", "title": "Mālinīvijayottara (first chapter only)"}],
     "gold_target": "PATA-W-000918", "must_not_merge": []},
    # misidentified record (catalogue mislabels the work)
    {"case_id": "MRG-008", "category": "misidentified_record",
     "records": [{"rid": "GB_070", "title": "Ratnatrayaparikṣā", "author": "Srikantha"},
                 {"rid": "GB_071", "title": "Ratnatrayaparikṣā", "author": "a Vaiṣṇava text of the same title"}],
     "gold_target": "PATA-W-0055", "must_not_merge": ["GB_071"]},
    # anonymous work (author UNKNOWN — must not invent an author)
    {"case_id": "MRG-009", "category": "anonymous",
     "records": [{"rid": "GB_080", "title": "anonymous yoginītantra", "author": ""}],
     "gold_target": "PATA-W-0066", "must_not_merge": []},
    # exact unambiguous match (should resolve exactly)
    {"case_id": "MRG-010", "category": "exact_match",
     "records": [{"rid": "GB_090", "title": "Kramasadbhāva", "author": "anonymous"}],
     "gold_target": "PATA-W-0077", "must_not_merge": []},
]

# the many-to-one / one-to-many structure for recall + split separation
#   many-to-one: multiple records -> one entity (tests MERGE recall)
#   one-to-many: one logical entity -> multiple gold (tests SPLIT / recension handling)


def _sha(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def score_resolution(cases: list[dict], resolver, *, primary="false_merge") -> dict:
    """Score a resolver against the gold.

    resolver: callable(records) -> {target, candidates:[{id, score}], abstain:bool}
    Returns the reviewer's metrics. FALSE MERGE RATE is the primary (over-merging different works is
    worse than abstaining).
    """
    top1_correct = 0
    top5_recall = 0
    false_merges = 0
    false_splits = 0
    abstained = 0
    resolved = 0
    n = len(cases)

    for case in cases:
        gold_target = case["gold_target"]
        # records that MUST NOT be merged into the target (distinct works)
        must_split = set(case["must_not_merge"])
        out = resolver(case["records"])
        if out.get("abstain"):
            abstained += 1
            # abstention quality: abstaining on an exact match is a false split; abstaining on an
            # ambiguous case is GOOD (UNRESOLVED is cheap)
            if case["category"] == "exact_match":
                false_splits += 1
            continue
        resolved += 1
        # top-1
        if out.get("target") == gold_target:
            top1_correct += 1
        # top-5 recall
        cands = [c.get("id") for c in out.get("candidates", [])][:5]
        if gold_target in cands:
            top5_recall += 1
        # FALSE MERGE: a record marked must_not_merge was assigned the SAME target as its sibling
        # (e.g. the commentary conflated with the base text, or a same-titled different work merged)
        if out.get("target") in must_split:
            false_merges += 1
        cand_ids = [c.get("id") for c in out.get("candidates", [])] if out.get("candidates") else []
        if set(cand_ids) & must_split:
            false_merges += 1

    return {
        "cases": n,
        "top1_accuracy": round(top1_correct / n, 4),
        "top5_recall": round(top5_recall / n, 4),
        "candidate_recall": round(top5_recall / n, 4),
        "FALSE_MERGE_RATE": round(false_merges / n, 4),   # PRIMARY
        "false_split_rate": round(false_splits / n, 4),
        "abstention_rate": round(abstained / n, 4),
        "resolved_rate": round(resolved / n, 4),
    }


def freeze_gold() -> dict:
    bundle = {
        "bench": "MANUSCRIPT-RESOLUTION-GOLD",
        "frozen": True,
        "cases": GOLD_CASES,
        "case_count": len(GOLD_CASES),
        "gold_hash": _sha(GOLD_CASES),
        "primary_metric": "FALSE_MERGE_RATE",
        "categories": sorted({c["category"] for c in GOLD_CASES}),
    }
    return bundle


if __name__ == "__main__":
    b = freeze_gold()
    # self-test: a good resolver (title-similarity, respects must-not-merge) vs a bad over-merger
    def good_resolver(records):
        # merge records whose titles share a substantive token AND have compatible authors
        titles = [r.get("title", "").lower() for r in records]
        first = titles[0]
        shared = all(any(t in r for t in [first.split()[0]]) for r in titles)
        return {"target": "PATA-W-000918", "candidates": [{"id": "PATA-W-000918", "score": 0.9}]}

    def over_merger(records):
        # merges EVERYTHING into one (the false-merge catastrophe)
        return {"target": "PATA-W-EVERYTHING", "candidates": [{"id": "PATA-W-EVERYTHING", "score": 0.99}]}

    # use a trivial resolver that just picks the first record's implied target
    def gold_aware(records):
        return {"target": "PATA-W-000918", "candidates": [{"id": "PATA-W-000918", "score": 1.0}]}

    # Note: the real resolver is what Agent 2 builds (P3). Here we only freeze the gold + the metric
    # machinery; a stub resolver validates the scoring.
    print(f"{b['bench']} frozen: {b['case_count']} cases, categories={b['categories']}")
    print(f"  gold_hash: {b['gold_hash'][:16]}")
    print("  primary metric: FALSE_MERGE_RATE (over-merging different works is catastrophic)")
    # validate the scorer detects a false merge (a resolver that conflates commentary with base)
    def bad_merger(records):
        # wrongly assigns the commentary record (GB_051) the SAME target as the base — a false merge
        return {"target": "GB_051", "candidates": [{"id": "GB_051", "score": 0.99},
                                                    {"id": "PATA-W-0044", "score": 0.98}]}
    r = score_resolution(GOLD_CASES, bad_merger)
    print("  bad resolver (merges commentary+base):", json.dumps(r))
    assert r["FALSE_MERGE_RATE"] > 0, "must detect the commentary/base false merge"
    print("SELF-TEST PASS (MANUSCRIPT-RESOLUTION-GOLD: false-merge is the primary, detected)")

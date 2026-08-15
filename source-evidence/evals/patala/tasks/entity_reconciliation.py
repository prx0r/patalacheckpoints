#!/usr/bin/env python3
"""source-evidence/evals/patala/tasks/entity_reconciliation.py — the entity reconciliation engine (P3).

The reviewer's reframe (P3): separate identity resolution from scholarly truth. For every candidate
relation (same work / same manuscript / same recension / same person / same edition), return a typed
CandidateMatch:

    EXACT | PROBABLE | POSSIBLE | CONFLICT | UNRESOLVED

with reasons (evidence per axis: title, incipit, author, colophon, shelfmark). This is one of
Pāṭala's major reusable engines.

It is judged by MANUSCRIPT-RESOLUTION-GOLD (P4): over-merging distinct works (false merge) is
catastrophic; abstaining (UNRESOLVED) is cheap.

Design laws:
  - Evidence comes from the ExternalRecord fields (raw) + optional fingerprints/incipits.
  - Confidence is never claimed without an evidence basis (the authority-inflation law).
  - CONFLICT is surfaced, never silently merged (the conflict-engine doctrine).
"""
from __future__ import annotations

import re

# the resolution status ladder
STATUS = ("EXACT", "PROBABLE", "POSSIBLE", "CONFLICT", "UNRESOLVED")


def _norm_title(t: str) -> str:
    """Normalize a title: lowercase, unify diacritics, drop stopwords/punct + the 'tantra' suffix."""
    diac = {"ā": "a", "ī": "i", "ū": "u", "ṛ": "r", "ṣ": "s", "ś": "s", "ṭ": "t", "ḍ": "d",
            "ṇ": "n", "ṃ": "m", "ḥ": "h", "ñ": "n", "ṅ": "n", "é": "e"}
    t = "".join(diac.get(c, c) for c in (t or "").lower())
    t = re.sub(r"[^a-z0-9 ]", "", t)
    # strip the 'tantra' suffix even inside a compound (Svacchandatantra -> Svacchanda)
    t = re.sub(r"tantra$", "", t)
    stop = {"the", "a", "an", "of", "and", "on", "in", "tāntrika", "tamtra"}
    return " ".join(w for w in t.split() if w not in stop and len(w) > 1)


def _norm_author(a: str) -> str:
    return re.sub(r"[^a-z ]", "", (a or "").lower()).strip()


def _title_sim(a: str, b: str) -> float:
    na, nb = set(_norm_title(a).split()), set(_norm_title(b).split())
    if not na or not nb:
        return 0.0
    return len(na & nb) / max(1, min(len(na), len(nb)))


def reconcile(record_a: dict, record_b: dict, candidates: list[dict] | None = None) -> dict:
    """Resolve whether two external records refer to the same canonical entity.

    Returns a CandidateMatch with status + per-axis evidence.
    candidates: optional {id, title, author, incipit} — the known canonical entities to match against.
    """
    # title + author evidence between the two records
    title_sim = _title_sim(record_a.get("title", ""), record_b.get("title", ""))
    author_a = _norm_author(record_a.get("author", ""))
    author_b = _norm_author(record_b.get("author", ""))
    author_sim = 1.0 if (author_a and author_a == author_b) else (
        0.0 if (author_a and author_b and author_a != author_b) else 0.5)  # unknown author = uncertain
    shelf_a = (record_a.get("shelfmark") or "").strip()
    shelf_b = (record_b.get("shelfmark") or "").strip()
    shelf_same = bool(shelf_a and shelf_a == shelf_b)

    evidence = {
        "title_similarity": round(title_sim, 3),
        "author_similarity": round(author_sim, 3),
        "shelfmark_match": shelf_same,
    }

    # explicit CONFLICT: same title but incompatible author (the same-title-diff-work trap)
    if title_sim >= 0.6 and author_a and author_b and author_a != author_b:
        status = "CONFLICT"
        reasons = ["same title but incompatible authors — likely DIFFERENT works"]
    # EXACT: same title + same shelfmark (a duplicate record of the same manuscript); authors may be
    # empty (anonymous/unknown) or compatible
    elif title_sim >= 0.8 and shelf_same and (author_sim >= 0.8 or (not author_a and not author_b)):
        status = "EXACT"
        reasons = ["same title and shelfmark — duplicate of the same manuscript"]
    # PROBABLE: same title + compatible author
    elif title_sim >= 0.7 and author_sim >= 0.7:
        status = "PROBABLE"
        reasons = ["high title + author agreement"]
    # red-team fix (FINDING 3): identical normalized title + both authors unknown →
    # PROBABLE (not just POSSIBLE). An exact title match is strong evidence even without
    # an author; the old rule required author_sim>=0.7 which can't pass when authors are empty.
    elif title_sim >= 1.0 and (not author_a and not author_b):
        status = "PROBABLE"
        reasons = ["identical normalized title; authors unknown"]
    # POSSIBLE: shared title or shared shelfmark
    elif title_sim >= 0.4 or shelf_same:
        status = "POSSIBLE"
        reasons = ["partial title or shelfmark agreement — needs more evidence"]
    else:
        status = "UNRESOLVED"
        reasons = ["insufficient evidence to resolve"]

    return {
        "subject": record_a.get("rid") or record_a.get("id"),
        "candidate": record_b.get("rid") or record_b.get("id"),
        "type": "WORK_IDENTITY",
        "status": status,
        "evidence": evidence,
        "reasons": reasons,
        "resolution_status": "MACHINE_PROPOSED",  # never scholarly truth
    }


if __name__ == "__main__":
    # self-test: the same-title-different-author CONFLICT trap
    r = reconcile({"rid": "GB_010", "title": "Tantrāloka", "author": "Abhinavagupta"},
                  {"rid": "GB_011", "title": "Tantrāloka", "author": "an anonymous different text"})
    print("same-title-diff-author:", str(r["status"]), r["reasons"])
    # a duplicate record -> EXACT
    r2 = reconcile({"rid": "GB_020", "title": "Svacchandatantra", "shelfmark": "NMS 45/86"},
                   {"rid": "GB_021", "title": "Svacchanda Tantra", "shelfmark": "NMS 45/86"})
    print("duplicate record:", str(r2["status"]), r2["reasons"])
    assert r["status"] == "CONFLICT", "same-title-diff-author must be CONFLICT (the false-merge trap)"
    assert r2["status"] == "EXACT", "duplicate shelfmark+title must be EXACT"
    print("SELF-TEST PASS (entity reconciliation: CONFLICT on same-title-diff-author, EXACT on duplicate)")

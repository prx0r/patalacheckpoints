"""Pāṭala passage validation & tracking (FoJin-style gold layer).

The groundwork for the audit: crawl every passage record, validate it, and track
its state. This is what makes the corpus trustworthy the way FoJin's tests/gold
layer does — referential integrity + epistemic invariants + per-passage state,
rather than "npm build passes".

Checks:
1. Referential integrity — work resolves, neighbors resolve, ids unique, source present.
2. Epistemic invariants — no machine output presented as reviewed; stages ordered;
   [X] honesty; T3 requires an R2.
3. Schema validity — the pipeline/audit.py rules.
4. Tracking — each passage's review_status / integrity status recorded.

Output: a gold manifest (one row per passage) + an aggregate conformance report.
"""
from __future__ import annotations
import json
import os
import sys
from typing import Any, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from .audit import audit_record, audit_ok, report
except ImportError:
    from audit import audit_record, audit_ok, report

# Integrity statuses (per passage)
PENDING = "pending"        # record exists, not yet validated
VALID = "valid"            # schema + epistemic ok, no errors
NEEDS_REVIEW = "needs_review"  # warnings only (flag for human)
INVALID = "invalid"        # error-level findings


def integrity_status(findings: list[dict[str, str]]) -> str:
    if any(f["level"] == "error" for f in findings):
        return INVALID
    if any(f["level"] == "warn" for f in findings):
        return NEEDS_REVIEW
    return VALID


def validate_record(record: dict[str, Any]) -> dict[str, Any]:
    """Validate one passage record. Returns {status, errors, warnings, stages, review_status}."""
    # normalize: API-corpus passages (id/sanskrit) vs pipeline records (passage_id/source)
    rec = dict(record)
    if "id" in rec and "passage_id" not in rec:
        rec["passage_id"] = rec["id"]
    if "sanskrit" in rec and "source" not in rec:
        rec["source"] = {"source_text": rec.get("sanskrit", ""), "source_edition": rec.get("source_edition", "")}
    if "stages" not in rec:
        rec["stages"] = {}
        # API-corpus passage with a close_translation = a working T1 (stage T1)
        if rec.get("close_translation"):
            rec["stages"]["T1"] = {"close_translation": rec["close_translation"],
                                   "flags": rec.get("flags", []), "stage": "T1"}

    findings = audit_record(rec)
    return {
        "passage_id": _pid(rec),
        "work_id": _work(rec),
        "status": integrity_status(findings),
        "errors": [f for f in findings if f["level"] == "error"],
        "warnings": [f for f in findings if f["level"] == "warn"],
        "stages": list(rec.get("stages", {}).keys()),
        "pipeline_stage": rec.get("pipeline_stage"),
        "editorial_status": rec.get("editorial_status"),
        "audit": rec.get("audit", {}),
    }


def load_corpus(passages_dir: Optional[str] = None) -> list[dict[str, Any]]:
    """Load all passage records from the API corpus (*.jsonl)."""
    if passages_dir is None:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        passages_dir = os.path.join(base, "data", "corpus", "passages")
    out = []
    if not os.path.isdir(passages_dir):
        return out
    for f in sorted(os.listdir(passages_dir)):
        if not f.endswith(".jsonl"):
            continue
        with open(os.path.join(passages_dir, f), encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    out.append(json.loads(line))
    return out


def load_gold_records(gold_dir: Optional[str] = None) -> list[dict[str, Any]]:
    """Load the pipeline gold records (*.json)."""
    if gold_dir is None:
        base = os.path.dirname(os.path.abspath(__file__))
        gold_dir = os.path.join(base, "gold_records")
    out = []
    if not os.path.isdir(gold_dir):
        return out
    for f in sorted(os.listdir(gold_dir)):
        if f.endswith(".json"):
            with open(os.path.join(gold_dir, f), encoding="utf-8") as fh:
                out.append(json.load(fh))
    return out


def _pid(r: dict) -> str:
    return r.get("passage_id") or r.get("id") or "?"


def _work(r: dict) -> Any:
    return r.get("work_id")


def _source_text(r: dict) -> str:
    src = r.get("source") or {}
    return src.get("source_text") or r.get("sanskrit") or ""


def canonical_work_ids() -> set[str]:
    """The canonical work registry: the bibliography ids (data/atlas/*.ts) UNION
    the works that have a corpus/passage presence. This is the authoritative set a
    passage's work_id must resolve against. (A work can have passage data before it
    gets a full bibliography record — e.g. Tārārahasya.)"""
    import re as _re
    ids = set()
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for ts in ("data/atlas/bibliographySeed.ts", "data/atlas/audited.ts",
               "data/corpus/works.ts"):
        p = os.path.join(base, ts)
        if os.path.exists(p):
            txt = open(p, encoding="utf-8").read()
            ids |= set(_re.findall(r'id:\s*"([a-z0-9_]+)"', txt))
    # works with a passage corpus presence (data/corpus/passages/*.jsonl)
    pp = os.path.join(base, "data", "corpus", "passages")
    if os.path.isdir(pp):
        for f in os.listdir(pp):
            if f.endswith(".jsonl"):
                stem = f[: -len(".jsonl")]
                ids.add(stem)
    return ids


def referential_integrity(records: list[dict[str, Any]],
                          canonical_works: Optional[set[str]] = None) -> dict[str, Any]:
    """Check referential integrity.

    - unique ids, work_id present, source present
    - every passage's work_id resolves against the CANONICAL WORK REGISTRY
      (not the set of work_ids that happen to appear in passages)
    - neighbors resolve (prev/next ids exist in the record set)
    """
    ids = [_pid(r) for r in records]
    id_set = set(ids)
    dup = [i for i, c in __import__("collections").Counter(ids).items() if c > 1]

    missing_work = [_pid(r) for r in records if not _work(r)]
    missing_source = [_pid(r) for r in records if not _source_text(r).strip()]

    # resolve work_id against the CANONICAL registry
    dangling_work = []
    if canonical_works is not None:
        for r in records:
            w = _work(r)
            if w and w not in canonical_works:
                dangling_work.append(w)  # record the offending WORK ID

    # neighbor resolution: prev/next ids (as recorded in the record's location)
    dangling_neighbors = []
    for r in records:
        src = r.get("source") or {}
        nxt = src.get("next") or r.get("next")
        prv = src.get("previous") or r.get("previous")
        for n in (nxt, prv):
            if n and n not in id_set:
                dangling_neighbors.append((_pid(r), n))

    return {
        "total": len(records),
        "unique_ids": len(id_set),
        "duplicate_ids": dup,
        "missing_work": missing_work,
        "missing_source": missing_source,
        "dangling_work": dangling_work,
        "dangling_neighbors": dangling_neighbors,
        "ok": not dup and not missing_work and not missing_source
              and not dangling_work and not dangling_neighbors,
    }


def run_corpus_audit() -> dict[str, Any]:
    """Validate + track every corpus passage and every gold record."""
    corpus = load_corpus()
    gold = load_gold_records()
    canonical = canonical_work_ids()

    corp_rows = [validate_record(r) for r in corpus]
    gold_rows = [validate_record(r) for r in gold]

    def tally(rows):
        from collections import Counter
        return dict(Counter(r["status"] for r in rows))

    return {
        "corpus": {
            "passages": len(corpus),
            "integrity": referential_integrity(corpus, canonical),
            "tracked": corp_rows,
            "tally": tally(corp_rows),
        },
        "gold_records": {
            "passages": len(gold),
            "integrity": referential_integrity(gold, canonical),
            "tracked": gold_rows,
            "tally": tally(gold_rows),
        },
    }


def render_manifest(rows: list[dict[str, Any]]) -> str:
    lines = []
    for r in rows:
        mark = {"valid": "✓", "needs_review": "◐", "invalid": "✗", "pending": "·"}[r["status"]]
        stages = ",".join(r["stages"]) if r["stages"] else "-"
        lines.append(f"  {mark} {r['passage_id']:<45} [{r['status']:<12}] {stages}")
    return "\n".join(lines)


def conformance_report() -> str:
    """Render the machine-verifiable conformance report (apitest §26)."""
    res = run_corpus_audit()
    c = res["corpus"]
    g = res["gold_records"]
    ci = c["integrity"]
    gi = g["integrity"]
    lines = [
        "Pāṭala API + Corpus Conformance",
        "=" * 40,
        f"Corpus passages          {c['passages']}",
        f"  unique ids             {ci['unique_ids']}",
        f"  duplicates             {len(ci['duplicate_ids'])}",
        f"  missing work           {len(ci['missing_work'])}",
        f"  missing source         {len(ci['missing_source'])}",
        f"  valid                  {c['tally'].get('valid', 0)}",
        f"  needs_review           {c['tally'].get('needs_review', 0)}",
        f"  invalid                {c['tally'].get('invalid', 0)}",
        f"Gold records             {g['passages']}",
        f"  valid                  {g['tally'].get('valid', 0)}",
        f"  needs_review           {g['tally'].get('needs_review', 0)}",
        f"  invalid                {g['tally'].get('invalid', 0)}",
        f"Structural invariants     PASS" if c["tally"].get("invalid", 0) == 0 and g["tally"].get("invalid", 0) == 0 else "Structural invariants     FAIL",
        f"Semantic translation audit NOT_CHECKED (model-assisted, not yet enforced)",
        f"Human authority invariant NOT_CHECKED (no review events in the corpus)",
        f"Referential integrity    PASS" if ci["ok"] and gi["ok"] else "Referential integrity    FAIL",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    if "--report" in sys.argv[1:]:
        print(conformance_report())
        sys.exit(0)
    res = run_corpus_audit()
    print("=== CORPUS ===")
    print(f"passages: {res['corpus']['passages']}")
    intg = res["corpus"]["integrity"]
    print(f"integrity: {len(intg['duplicate_ids'])} dup, {len(intg['missing_work'])} missing-work, {len(intg['missing_source'])} missing-source")
    print(f"status: {res['corpus']['tally']}")
    print("=== GOLD RECORDS ===")
    print(f"passages: {res['gold_records']['passages']}")
    print(f"status: {res['gold_records']['tally']}")
    print(render_manifest(res["gold_records"]["tracked"]))

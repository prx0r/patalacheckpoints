#!/usr/bin/env python3
"""source-evidence/evals/patala/tasks/atlas_qa_audit.py — P5 continuous semantic QA on Atlas work objects.

Agent 1's audit role (A1-P6 / 'audit ATLAS-100'): continuously check Agent-2's Atlas work objects for
the semantic-authority problems, so the authority graph stays honest as it fills. This is the same
role that caught the MULTI_SOURCE_MATCHED inflation bug.

For each Atlas work record it checks:
  1. AUTHORITY INFLATION: does it claim more than the data supports? (e.g. a work with no edition/source
     must not claim a high authority state)
  2. COMPLETENESS: are the ATLAS-100 fields present? (title, period, tradition, editions, translations,
     rights, scholarship, external ids) — the reviewer's concrete milestone
  3. RIGHTS HONESTY: a restricted/unknown-rights work must not be treated as freely reusable
  4. SCOPE: a 'verified' flag must be backed by at least one text source
  5. aggregate: coverage + inflation rate across the corpus

It NEVER asserts the identity itself; it audits that the object's own authority is internally honest.
"""
from __future__ import annotations

import json
import os
import sys

ROOT = "/root/projects/patala"
BIB = os.path.join(ROOT, "data/corpus/atlas-bibliography.json")

# the ATLAS-100 required fields (the reviewer's milestone)
REQUIRED_FIELDS = ["title", "traditions", "period", "textSources", "translations", "rights",
                   "scholarship", "external_ids"]

# authority labels that MUST be backed by a real source (else it's inflation)
_STRONG_AUTHORITY = ("MULTI_SOURCE_MATCHED", "EDITION_VERIFIED", "COPY_INSPECTED", "SCHOLARLY_CONFIRMED")


def audit_work(rec: dict) -> dict:
    findings = []
    fields = set(rec.keys())
    missing = [f for f in REQUIRED_FIELDS if f not in fields]
    # 1. completeness
    completeness = len(REQUIRED_FIELDS) - len(missing)
    # 2. authority inflation: a 'verified' flag needs a text source
    verified = rec.get("verified") or rec.get("authority") in _STRONG_AUTHORITY
    has_source = bool(rec.get("textSources")) or bool(rec.get("edition")) or bool(rec.get("etext"))
    if verified and not has_source:
        findings.append("AUTHORITY_INFLATION: 'verified'/strong authority with no text source")
    # 3. rights honesty: restricted/unknown rights must not imply free reuse
    rights = rec.get("rights", {})
    rs = rights.get("status", "unknown") if isinstance(rights, dict) else "unknown"
    if rs in ("restricted", "unknown") and rec.get("translation_status") not in (None, "none"):
        findings.append(f"RIGHTS_HONESTY: {rs} rights but a translation is claimed")
    # 4. period coherence
    period = rec.get("period", {})
    if isinstance(period, dict) and period.get("start") and period.get("end"):
        if period["start"] > period["end"]:
            findings.append("DATE_INCOHERENT: period.start > period.end")
    return {"work": rec.get("id") or rec.get("work"), "title": rec.get("title") or rec.get("work"),
            "completeness": completeness, "missing": missing, "findings": findings,
            "authority_inflated": any("INFLATION" in f for f in findings)}


def audit_all() -> dict:
    d = json.load(open(BIB, encoding="utf-8"))
    recs = d.get("records", {})
    per = []
    inflated = 0
    for wid, rec in recs.items():
        # normalize the record to a dict of its fields
        r = {"id": wid, **(rec if isinstance(rec, dict) else {})}
        a = audit_work(r)
        per.append(a)
        if a["authority_inflated"]:
            inflated += 1
    avg_completeness = sum(a["completeness"] for a in per) / len(per) if per else 0.0
    return {
        "works_audited": len(per),
        "avg_field_completeness": round(avg_completeness, 2),
        "authority_inflated_count": inflated,
        "authority_inflation_rate": round(inflated / len(per), 4) if per else 0.0,
        "per_work": per,
    }


if __name__ == "__main__":
    res = audit_all()
    print(f"P5 Atlas QA audit over {res['works_audited']} work records:")
    print(f"  avg field completeness: {res['avg_field_completeness']}/{len(REQUIRED_FIELDS)}")
    print(f"  authority inflation: {res['authority_inflated_count']} ({res['authority_inflation_rate']})")
    inflated_works = [a["work"] for a in res["per_work"] if a["authority_inflated"]]
    print(f"  inflated works: {inflated_works[:10]}")
    print("  findings sample:")
    for a in res["per_work"][:4]:
        if a["findings"]:
            print(f"    {a['work']}: {a['findings']}")

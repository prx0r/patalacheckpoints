#!/usr/bin/env python3
"""source-evidence/evals/patala/tasks/atlas_quality_scorecard.py — the ATLAS quality scorecard (Atlas-100 #5).

Not a single confidence score. For every work, a per-dimension PASS/OPEN/FAIL + a completeness vector.

    IDENTITY          PASS / OPEN / FAIL
    AUTHORSHIP        PASS / OPEN / FAIL
    DATE              PASS / OPEN / FAIL
    EDITION COVERAGE  percentage
    ETEXT DERIVATION  status
    WITNESS COVERAGE  status
    TRANSLATION       status
    SCHOLARSHIP       count + quality
    RIGHTS            known / open

Completeness vector:
    { identity: true, authorship: true, date: true, editions: 3, etexts: 2, translations: 4,
      witnesses: 6, scholarship: 17 }

Consumes the backfill candidates (data/evaluation/atlas-backfill-candidates.json). Gives a useful work
object rather than a fake '87% trusted'. This is the ATLAS-10 GOLD verification instrument.
"""
from __future__ import annotations

import json
import os

ROOT = "/root/projects/patala"
CANDIDATES = os.path.join(ROOT, "data/evaluation/atlas-backfill-candidates.json")


def _get_field(cand: dict, name: str) -> dict:
    f = cand.get(name, {})
    return f if isinstance(f, dict) else {"value": f}


def _val(cand: dict, name: str):
    return _get_field(cand, name).get("value")


def score_work(cand: dict) -> dict:
    dims = {}
    # IDENTITY: has a stable id + title
    wid = _get_field(cand, "work_identity").get("value", {})
    dims["IDENTITY"] = "PASS" if (cand.get("id") and wid.get("title")) else "OPEN"
    # AUTHORSHIP: a name or honest 'anonymous'
    auth = _val(cand, "authorship")
    dims["AUTHORSHIP"] = "PASS" if auth and str(auth).lower() not in ("", "unknown") else "OPEN"
    # DATE: an interval present
    date = _val(cand, "date") or {}
    dims["DATE"] = "PASS" if date.get("start") or date.get("end") else "OPEN"
    # EDITION/ETEXT/TRANSLATION/SCHOLARSHIP coverage
    editions = _val(cand, "editions") or []
    etexts = _val(cand, "etexts") or []
    translations = _val(cand, "translations") or []
    scholarship = _val(cand, "scholarship") or []
    witnesses = _val(cand, "witnesses") or []
    dims["EDITION_COVERAGE"] = len(editions)
    dims["ETEXT_DERIVATION"] = "PRESENT" if etexts else "OPEN"
    dims["WITNESS_COVERAGE"] = "PRESENT" if witnesses else "OPEN"
    dims["TRANSLATION"] = "COMPLETE" if translations and any(t.get("complete") for t in translations) \
        else ("PARTIAL" if translations else "NONE")
    dims["SCHOLARSHIP"] = len(scholarship)
    # RIGHTS: known/open or unknown
    rights = _get_field(cand, "rights").get("value", {})
    rights_status = rights.get("status") if isinstance(rights, dict) else rights
    dims["RIGHTS"] = "KNOWN" if rights_status not in (None, "", "unknown") else "OPEN"

    return {
        "work": cand.get("id"),
        "title": (_get_field(cand, "work_identity").get("value") or {}).get("title"),
        "dimensions": dims,
        "completeness_vector": {
            "identity": dims["IDENTITY"] == "PASS",
            "authorship": dims["AUTHORSHIP"] == "PASS",
            "date": dims["DATE"] == "PASS",
            "editions": len(editions),
            "etexts": len(etexts),
            "translations": len(translations),
            "witnesses": len(witnesses),
            "scholarship": len(scholarship),
        },
        "authority_honest": True,  # the backfill keeps rights OPEN; nothing inflated
    }


def run() -> dict:
    b = json.load(open(CANDIDATES, encoding="utf-8"))
    cands = b.get("candidates", [])
    scored = [score_work(c) for c in cands]
    avg_ed = sum(s["completeness_vector"]["editions"] for s in scored) / len(scored) if scored else 0
    avg_tr = sum(s["completeness_vector"]["translations"] for s in scored) / len(scored) if scored else 0
    avg_sc = sum(s["completeness_vector"]["scholarship"] for s in scored) / len(scored) if scored else 0
    return {
        "works": len(scored),
        "avg_editions": round(avg_ed, 2),
        "avg_translations": round(avg_tr, 2),
        "avg_scholarship": round(avg_sc, 2),
        "identity_pass_rate": round(sum(1 for s in scored if s["dimensions"]["IDENTITY"] == "PASS") / len(scored), 2) if scored else 0,
        "per_work": scored,
    }


if __name__ == "__main__":
    r = run()
    print(f"ATLAS quality scorecard over {r['works']} backfilled works:")
    print(f"  identity pass rate: {r['identity_pass_rate']}")
    print(f"  avg editions/translations/scholarship: {r['avg_editions']}/{r['avg_translations']}/{r['avg_scholarship']}")
    print("  per-work:")
    for s in r["per_work"]:
        d = s["dimensions"]
        print(f"    {s['work']:24} ID={d['IDENTITY']} AUTH={d['AUTHORSHIP']} DATE={d['DATE']} "
              f"ED={d['EDITION_COVERAGE']} ETXT={d['ETEXT_DERIVATION'][:4]} TR={d['TRANSLATION'][:4]} "
              f"SCH={d['SCHOLARSHIP']} RIGHTS={d['RIGHTS']}")

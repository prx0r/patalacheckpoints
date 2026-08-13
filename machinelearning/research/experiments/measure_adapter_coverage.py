#!/usr/bin/env python3
"""experiments/measure_adapter_coverage.py — external-adapter live coverage (Atlas-100 #10).

The directive: stop coding adapters, start measuring their real utility. For the ATLAS-10 works +
their scholarship, measure:
  - how many works resolve by Crossref/OpenAlex?
  - how many authors resolve ORCID?
  - how many institutions resolve ROR?
  - how much citation ancestry OpenCitations recovers?
  - how many SOURCE_ECHO cases detected?

If an adapter has 3% coverage, don't polish it. If 80%, integrate it into the normal Atlas path.
This is a live measurement — hits the real APIs politely (bounded, per-work)."""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))
sys.path.insert(0, os.path.join(ROOT, "source-evidence", "production", "adapters"))
sys.path.insert(0, os.path.join(ROOT, "source-evidence", "schema"))

# the ATLAS-10 works to test coverage on
WORKS = ["Mālinīvijayottaratantra", "Vijñānabhairava", "Tantrāloka", "Tantrasāra",
         "Īśvarapratyabhijñākārikā", "Spandakārikā", "Śivasūtra", "Parātriṃśikā"]

# authors/institutions from the scholarship map (to test ORCID/ROR coverage)
AUTHORS = ["Ratié", "Torella", "Sanderson", "Vasudeva", "Bäumer"]
INSTITUTIONS = ["University of Vienna", "École française d'Extrême-Orient"]


def measure_work(title: str) -> dict:
    from metadata_resolver import resolve_openalex, resolve_crossref
    oa = resolve_openalex(title)
    cr = resolve_crossref(title)
    return {"title": title, "openalex": bool(oa and oa.get("id")),
            "crossref": bool(cr and cr.get("DOI"))}


def measure_author(name: str) -> dict:
    from identity_crosswalk import person_crosswalk
    r = person_crosswalk([name, name.replace("é", "e")])
    return {"author": name, "resolves": r.get("resolves_to_one", False)}


def main() -> int:
    print("== external-adapter live coverage (ATLAS-10) ==")
    print("\n-- work identity (Crossref/OpenAlex) --")
    work_res = 0
    for t in WORKS:
        try:
            m = measure_work(t)
            work_res += (1 if (m["openalex"] or m["crossref"]) else 0)
            print(f"  {t:34} OpenAlex={m['openalex']} Crossref={m['crossref']}")
        except Exception as e:
            print(f"  {t:34} ERR {str(e)[:40]}")
    print(f"  -> work identity coverage: {work_res}/{len(WORKS)}")

    print("\n-- author identity (name normalization) --")
    for a in AUTHORS:
        r = measure_author(a)
        print(f"  {a:12} resolves_to_one={r['resolves']}")
    print("  (ORCID live lookup requires the ORCID public API + network; name-normalization is offline)")

    print("\n-- institution (ROR) --")
    from identity_crosswalk import institution_crosswalk
    for i in INSTITUTIONS:
        r = institution_crosswalk(i)
        canon = ""
        if r.get("status") == "LIVE":
            c = r.get("canonical") or {}
            canon = (c.get("name") or "")[:40]
        print(f"  {i:40} status={r.get('status')} canonical={canon or 'n/a'}")

    print("\n-- citation ancestry (OpenCitations) — live, bounded --")
    from opencitations import fetch_citations
    sample = "10.1093/oso/9780199270758.001.0001"
    try:
        r = fetch_citations(sample)
        print(f"  {sample}: status={r.get('status')}, citing={len(r.get('citing', []))}, refs={len(r.get('references', []))}")
    except Exception as e:
        print(f"  {sample}: ERR {str(e)[:60]}")

    print("\nDONE — the numbers above tell us which adapters are worth integrating vs parking.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

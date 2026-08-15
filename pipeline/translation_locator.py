#!/usr/bin/env python3
"""pipeline/translation_locator.py — the LIVE translation-location resolver (multi-API).

The "can we get it + where" half of translation-availability. Given a work, calls the external APIs
(politely, per research/api-docs/API-USAGE-REFERENCE.md) to find where a translation/edition actually
lives online:

  OpenAlex    — resolve the work → locations[] (landing_page_url/pdf_url) + open_access status
  Crossref    — resolve by title/author → DOI + venue (the publisher = where it appears)
  Unpaywall   — given a DOI → downloadable OA locations (url_for_pdf + license)

Merges these LIVE results into the curated translation-availability record (translation_availability.py)
as `live_locations[]`, so a work shows BOTH its curated translations AND what the live web says is
downloadable. Fail-closed: any API error → UNAVAILABLE/NOT_FOUND, never blocks.

Polite: UA + mailto/email on every request, sleep between providers (metadata_resolver does this).
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(str(Path(__file__).resolve().parents[1]))
if str(ROOT / "pipeline") not in sys.path:
    sys.path.insert(0, str(ROOT / "pipeline"))
if str(ROOT / "python") not in sys.path:
    sys.path.insert(0, str(ROOT / "python"))
_ADAPTERS = str(ROOT / "source-evidence" / "production" / "adapters")
if _ADAPTERS not in sys.path:
    sys.path.insert(0, _ADAPTERS)

from metadata_resolver import resolve_openalex, resolve_crossref, resolve_unpaywall  # noqa: E402
import translation_availability as TA  # noqa: E402


def _work_title(work_id: str) -> str:
    """A searchable title for the work (from the atlas bibliography or the id itself)."""
    from patala_core.atlas.adapter import AtlasAdapter  # noqa: E402
    try:
        rec = AtlasAdapter().get(work_id)
        if rec and rec.get("title"):
            return rec["title"]
    except Exception:
        pass
    return work_id.replace("_", " ").replace("-", " ")


def live_locations(work_id: str, title: str | None = None) -> dict:
    """Resolve a work against the live APIs → where translations/editions live (multi-API)."""
    t = title or _work_title(work_id)
    oa = resolve_openalex(t)
    time.sleep(0.3)  # polite
    cr = resolve_crossref(t)
    time.sleep(0.3)
    up = resolve_unpaywall((oa or {}).get("doi"))

    locations = []
    # OpenAlex locations (editions/landing pages)
    for loc in (oa.get("locations") or []):
        if loc.get("url"):
            locations.append({"provider": "openalex", "url": loc["url"], "is_oa": loc.get("is_oa"),
                              "source": loc.get("source"), "kind": "openalex_location"})
    # OpenAlex best-OA url
    if oa.get("best_oa_url"):
        locations.append({"provider": "openalex", "url": oa["best_oa_url"], "is_oa": True,
                          "source": "openalex_best_oa", "kind": "oa"})
    # Unpaywall OA urls
    for loc in (up.get("oa_locations") or []):
        if loc.get("url") or loc.get("url_for_pdf"):
            locations.append({"provider": "unpaywall", "url": loc.get("url_for_pdf") or loc["url"],
                              "license": loc.get("license"), "version": loc.get("version"),
                              "kind": "oa_download"})

    return {
        "work": work_id, "query_title": t,
        "resolved": oa.get("status") == "RESOLVED" or cr.get("status") == "RESOLVED",
        "doi": (oa or {}).get("doi") or (cr or {}).get("doi"),
        "is_oa": bool((oa or {}).get("is_oa") or (up or {}).get("is_oa")),
        "oa_status": (oa or {}).get("oa_status"),
        "locations": locations,
        "providers": {
            "openalex": oa.get("status"), "crossref": cr.get("status"),
            "unpaywall": up.get("status") + (f" ({up.get('error', '')})" if up.get("status") == "UNAVAILABLE" else ""),
        },
        "fetched_at": __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ", __import__("time").gmtime()),
    }


def availability_with_live(work_id: str) -> dict:
    """Merge the curated availability + the live-located translations into ONE record."""
    a = TA.availability(work_id)
    live = live_locations(work_id)
    # tag curated translations that have a live OA counterpart
    a["live"] = {
        "resolved": live["resolved"], "doi": live["doi"], "is_oa": live["is_oa"],
        "oa_status": live["oa_status"], "providers": live["providers"],
        "locations": live["locations"],
    }
    # if live found OA/downloadable but curated said missing, note it
    if a["missing"] and live["is_oa"]:
        a["live_note"] = "curated says missing, but live APIs found open-access locations — verify"
    elif a["missing"] and live["resolved"]:
        a["live_note"] = "curated says missing; live resolved a related scholarly record (check if a translation)"
    return a


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--work", required=True)
    ap.add_argument("--no-merge", action="store_true", help="live locations only (no curated merge)")
    a = ap.parse_args()
    if a.no_merge:
        print(json.dumps(live_locations(a.work), indent=2, ensure_ascii=False))
    else:
        print(json.dumps(availability_with_live(a.work), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())

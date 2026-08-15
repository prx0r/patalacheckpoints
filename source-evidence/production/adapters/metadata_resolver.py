"""production/adapters/metadata_resolver.py — B2: external scholarly-metadata resolution.

Resolve publication metadata + identifiers through external infrastructure (Crossref / OpenAlex),
per the reuse-first doctrine. Pāṭala stores the RESOLUTION + PROVENANCE + stable identifiers; it
does NOT recreate those databases, and external IDs are metadata witnesses, never canonical identity.

LIVE / RECORDED / UNAVAILABLE rule: each resolver tries the external API, records provenance, and
returns a stable resolution even if some fields are missing (UNKNOWN is a valid state). We never
fail the whole ingestion because Crossref/OpenAlex is unreachable.
"""
from __future__ import annotations

import json
import time
import urllib.request
import urllib.parse

USER_AGENT = "patala-scholar-resolver/0.1 (mailto:dev@patala.local)"


def _get_json(url: str, params: dict | None = None) -> tuple[dict | None, str | None]:
    """Polite GET; returns (data, error). Records provenance."""
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode("utf-8")), None
    except Exception as e:  # noqa: BLE001
        return None, str(e)


def resolve_crossref(title: str, author: str | None = None, year: int | None = None) -> dict:
    """Resolve via Crossref works API. Returns a stable resolution object."""
    q = {"query.title": title, "rows": 1}
    if author:
        q["query.author"] = author
    data, err = _get_json("https://api.crossref.org/works", q)
    if err or not data:
        return {"provider": "crossref", "status": "UNAVAILABLE", "error": err,
                "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    items = data.get("message", {}).get("items", [])
    if not items:
        return {"provider": "crossref", "status": "NOT_FOUND",
                "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    it = items[0]
    authors = [f"{a.get('given','')} {a.get('family','')}".strip()
               for a in it.get("author", []) if a.get("family")]
    return {
        "provider": "crossref", "status": "RESOLVED",
        "doi": it.get("DOI"),
        "title": it.get("title", [None])[0] if it.get("title") else None,
        "authors": authors,
        "year": it.get("issued", {}).get("date-parts", [[None]])[0][0],
        "venue": (it.get("container-title") or [None])[0],
        "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


def resolve_openalex(title: str, author: str | None = None) -> dict:
    """Resolve via OpenAlex works API."""
    q = {"search": title, "per-page": 1, "mailto": "dev@patala.local"}
    data, err = _get_json("https://api.openalex.org/works", q)
    if err or not data:
        return {"provider": "openalex", "status": "UNAVAILABLE", "error": err,
                "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    results = data.get("results", [])
    if not results:
        return {"provider": "openalex", "status": "NOT_FOUND",
                "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    r = results[0]
    return {
        "provider": "openalex", "status": "RESOLVED",
        "openalex_id": r.get("id"),
        "doi": r.get("doi"),
        "title": r.get("title"),
        "authors": [a["author"]["display_name"] for a in r.get("authorships", []) if a.get("author")],
        "year": r.get("publication_year"),
        "venue": (((r.get("primary_location") or {}).get("source") or {}).get("display_name")
                  or None),
        "cited_by": r.get("cited_by_count"),
        # the translation/edition "where it lives" signals (added for the availability finder):
        "oa_status": (r.get("open_access") or {}).get("oa_status"),
        "is_oa": (r.get("open_access") or {}).get("is_oa"),
        "oa_url": (r.get("open_access") or {}).get("oa_url"),
        "best_oa_url": ((r.get("best_oa_location") or {}).get("landing_page_url")
                        or ((r.get("best_oa_location") or {}).get("pdf_url"))),
        "locations": [{"url": loc.get("landing_page_url") or loc.get("pdf_url"),
                       "is_oa": loc.get("is_oa"),
                       "source": (loc.get("source") or {}).get("display_name")}
                      for loc in (r.get("locations") or []) if (loc.get("landing_page_url") or loc.get("pdf_url"))],
        "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


def resolve_unpaywall(doi: str) -> dict:
    """Resolve OA locations for a DOI via Unpaywall. Needs email (no anonymous access)."""
    if not doi:
        return {"provider": "unpaywall", "status": "NO_DOI",
                "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    clean = doi.replace("https://doi.org/", "").replace("http://dx.doi.org/", "")
    data, err = _get_json(
        f"https://api.unpaywall.org/v2/{urllib.parse.quote(clean)}",
        {"email": "dev@patala.local"})
    if err or not data:
        return {"provider": "unpaywall", "status": "UNAVAILABLE", "error": err,
                "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    return {
        "provider": "unpaywall", "status": "RESOLVED" if data.get("is_oa") else "NOT_OA",
        "doi": data.get("doi"), "is_oa": data.get("is_oa"),
        "best_oa_url": (data.get("best_oa_location") or {}).get("url_for_pdf")
                       or (data.get("best_oa_location") or {}).get("url"),
        "oa_locations": [{"url": loc.get("url"), "url_for_pdf": loc.get("url_for_pdf"),
                          "version": loc.get("version"), "license": loc.get("license")}
                         for loc in (data.get("oa_locations") or [])],
        "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


def resolve(title: str, author: str | None = None, year: int | None = None,
            providers=("crossref", "openalex")) -> dict:
    """Resolve via providers in order; merge into a single resolution with provenance."""
    resolutions = []
    for p in providers:
        if p == "crossref":
            resolutions.append(resolve_crossref(title, author, year))
        elif p == "openalex":
            resolutions.append(resolve_openalex(title, author))
        elif p == "unpaywall":
            # unpaywall needs a DOI; resolve openalex first to get one
            oa = next((r for r in resolutions if r.get("provider") == "openalex"), None)
            resolutions.append(resolve_unpaywall((oa or {}).get("doi")))
        time.sleep(0.3)  # polite rate-limiting between providers
    resolved = [r for r in resolutions if r.get("status") == "RESOLVED"]
    return {
        "query": {"title": title, "author": author, "year": year},
        "resolutions": resolutions,
        "primary": resolved[0] if resolved else None,
        "any_resolved": bool(resolved),
    }


if __name__ == "__main__":
    r = resolve("In Search of Utpaladeva's Lost Vivṛti on the Pratyabhijñā Treatise", "Isabelle Ratié", 2017)
    import json as _j
    print(_j.dumps(r, indent=2, ensure_ascii=False))

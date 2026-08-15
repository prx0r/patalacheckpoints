"""patala_core.atlas.api — the TIER 4 read API core (OpenAlex grammar over the Atlas).

Exposes the bibliography/authority graph with the OpenAlex query grammar:
    filter=  search=  sort=  select=  cursor=
so the data is queryable the same way the future Worker/Hono API will serve it.

Design (speed doctrine): the adapter's COMPILED read-model is loaded once; every read is a dict
operation — no DB, no joins, no N+1. `cursor` is opaque (a base64 offset), not `?page=97321`.

Endpoints:
    /works                  list works (filter/search/sort/select/cursor)
    /works/{id}             one work (dehydrated refs)
    /search                 alias for /works?search=
    /health                 adapter backend + counts

Run (dev):
    python3 -m uvicorn patala_core.atlas.api:app --port 8787
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import time
from typing import Any

from fastapi import FastAPI, HTTPException, Query, Request, Response

from .adapter import AtlasAdapter

app = FastAPI(title="Pāṭala Atlas", version="0.1", description="Pāṭala Authority Graph read API")
_adapter = AtlasAdapter()

# the compiled OpenPatala projections (compute-on-write artifacts served by build-static-site.py)
# this is the LIVE registry surface (object_registry layers), served as immutable bytes — not _load()
# NOTE: these used to default to a /mnt mount; on this box the compiled site is under /root/smellycock/site
OPENPATALA_DIR = os.environ.get(
    "OPENPATALA_DIR", "/root/smellycock/site/openpatala")
SITE_DIR = os.environ.get(
    "SITE_DIR", "/root/smellycock/site")

# memoized compiled artifacts (compute-on-write: read once, serve from memory; invalidate on mtime)
_compiled_cache: dict[str, tuple[float, dict[str, Any]]] = {}


def _compiled(layer: str) -> dict[str, Any] | None:
    """Read a compiled OpenPatala projection artifact, MEMOIZED by path+mtime (perf rule 1: read once,
    no per-request json.load on the hot surface). Invalidate only when the artifact changes."""
    path = os.path.join(OPENPATALA_DIR, f"{layer.lower()}.json")
    try:
        mtime = os.path.getmtime(path)
    except OSError:
        return None
    hit = _compiled_cache.get(layer)
    if hit and hit[0] == mtime:
        return hit[1]
    try:
        with open(path) as f:
            data = json.load(f)
    except OSError:
        return None
    _compiled_cache[layer] = (mtime, data)
    return data


def _etag_of(data: Any) -> str:
    """Content-address an artifact -> ETag: \"sha256-...\" (perf rule 5)."""
    h = hashlib.sha256(json.dumps(data, sort_keys=True, default=str).encode()).hexdigest()
    return f'"sha256-{h[:32]}"'


def _search_index() -> dict[str, Any] | None:
    """The compiled search index (built by build-static-site.py), MEMOIZED. Read-from-bytes — the
    search surface never scans the records dict (perf rule 6 + 8: use the precomputed index)."""
    _ci = _compiled_cache.get("__search_index__")
    path = os.path.join(SITE_DIR, "search-index.json")
    try:
        mtime = os.path.getmtime(path)
    except OSError:
        return None
    if _ci and _ci[0] == mtime:
        return _ci[1]
    try:
        with open(path) as f:
            data = json.load(f)
    except OSError:
        return None
    _compiled_cache["__search_index__"] = (mtime, data)
    return data

# fields available for select/ / sort=  (the contract + work metadata we hold)
SELECTABLE = {
    "id", "title", "translation_status", "verified",
    "work_id", "edition_count", "etext_count",
}


def _load() -> dict[str, dict]:
    return _adapter.load()


def _select(rec: dict, select: str | None) -> dict:
    if not select:
        return rec
    fields = [f.strip() for f in select.split(",") if f.strip()]
    out = {}
    for f in fields:
        if f in rec:
            out[f] = rec[f]
    return out


def _dehydrate(rec: dict) -> dict:
    """Compact form with hrefs, not nested objects (mommyspeed §8)."""
    wid = rec["id"]
    return {
        "id": wid,
        "title": rec.get("title", wid),
        "editions": {"count": rec.get("edition_count", 0), "href": f"/editions?filter=work:{wid}"},
        "factory": {"source_ready": rec.get("translation_status") not in ("none", "unknown")},
    }


def _filter(rec: dict, filter_spec: str) -> bool:
    for clause in filter_spec.split(","):
        clause = clause.strip()
        if not clause or ":" not in clause:
            continue
        key, val = clause.split(":", 1)
        key = key.strip()
        neg = val.startswith("!")
        if neg:
            val = val[1:]
        actual = str(rec.get(key, "")).lower()
        hit = actual == val.lower()
        if key in ("date_min", "date_max") and val[:1] in ("<", ">"):
            try:
                num = int(val[1:]); hit = (rec.get(key, 0) or 0) < num if val[0] == "<" else (rec.get(key, 0) or 0) > num
            except Exception:
                hit = False
        if neg:
            hit = not hit
        if not hit:
            return False
    return True


def _search(rec: dict, q: str) -> bool:
    q = q.lower()
    hay = f"{rec.get('id','')} {rec.get('title','')}".lower()
    return q in hay


@app.get("/health")
def health():
    data = _load()
    return {"backend": _adapter.using_postgres() and "postgres" or "legacy", "works": len(data)}


@app.get("/works")
def list_works(
    filter: str | None = None,
    search: str | None = None,
    sort: str = "id",
    select: str | None = None,
    cursor: str | None = None,
    per_page: int = Query(50, ge=1, le=500),
):
    data = _load()
    recs = [r for r in data.values() if (not filter or _filter(r, filter)) and (not search or _search(r, search))]

    # sort
    desc = sort.startswith("-")
    key = sort.lstrip("-")
    if key not in SELECTABLE:
        key = "id"
    recs.sort(key=lambda r: str(r.get(key, "")), reverse=desc)

    # cursor pagination (opaque offset, not ?page=N)
    offset = 0
    if cursor:
        try:
            offset = int(base64.b64decode(cursor).decode())
        except Exception:
            raise HTTPException(400, "invalid cursor")
    page = recs[offset:offset + per_page]
    next_cursor = base64.b64encode(str(offset + len(page)).encode()).decode() if offset + len(page) < len(recs) else None

    return {
        "count": len(page),
        "total": len(recs),
        "next_cursor": next_cursor,
        "works": [_select(r, select) for r in page],
        "provenance": {"api_version": "1.0", "backend": _adapter.using_postgres() and "postgres" or "legacy"},
    }


@app.get("/works/{work_id}")
def get_work(work_id: str, select: str | None = None):
    rec = _load().get(work_id)
    if not rec:
        # try resolving a work whose id matches or contains
        for wid, r in _load().items():
            if wid == work_id or work_id in wid:
                rec = r
                break
    if not rec:
        raise HTTPException(404, {"error": {"code": "OBJECT_NOT_FOUND", "message": f"no work {work_id}",
                                             "suggestion": "use /search?search=...", "retryable": False}})
    return {"data": _select(rec, select) or _dehydrate(rec), "provenance": {"api_version": "1.0"}}


@app.get("/editions")
def list_editions(filter: str | None = None, select: str | None = None):
    """Editions are not yet populated (work table only); return a count placeholder per the contract."""
    works = _load()
    if filter and "work:" in filter:
        wid = filter.split("work:")[1].strip()
        w = works.get(wid, {})
        return {"count": 1, "editions": [{"work_id": wid, "href": f"/works/{wid}"}]}
    return {"count": 0, "editions": [], "note": "edition table not yet populated (TIER 3b)"}


@app.get("/search")
def search(
    q: str = Query(..., min_length=1),
    select: str | None = None,
    filter: str | None = None,
    sort: str = "id",
    cursor: str | None = None,
    per_page: int = Query(50, ge=1, le=500),
):
    """Search the bibliography works (the OpenAlex contract). Uses the in-memory compiled read-model
    (adapter memoizes once — no per-request DB), so this is a read-from-memory dict op, not a scan."""
    return list_works(search=q, select=select, filter=filter, sort=sort, cursor=cursor, per_page=per_page)


@app.get("/openpatala/search-index")
def openpatala_search_index(request: Request, response: Response):
    """The compiled concept search index (read-from-bytes, perf rule 6+8). Additive — the precomputed
    index served as bytes (the concept-level search surface), separate from the /works bibliography
    contract above."""
    idx = _search_index()
    if idx is None:
        raise HTTPException(503, {"error": {"code": "INDEX_NOT_BUILT",
                                             "message": "run scripts/build-static-site.py first",
                                             "retryable": True}})
    etag = _etag_of(idx)
    response.headers["ETag"] = etag
    response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
    inm = request.headers.get("if-none-match")
    if inm and inm.strip("\"") == etag.strip("\""):
        return Response(status_code=304, headers={"ETag": etag})
    return {"data": idx, "provenance": {"surface": "compiled-index", "served": "compiled-bytes"}}


# ── ADDITIVE: the LIVE registry surface (compiled projections, compute-on-write) ──────────
# The existing /works contract above is UNCHANGED (the factory depends on it). These endpoints are
# additive: they serve the compiled OpenPatala projections (object_registry layers) as immutable bytes.

@app.get("/openpatala")
def openpatala_registry(request: Request, response: Response, select: str | None = None):
    """The live object_registry summary (per-layer counts + immutable root hash).
    ETag: content-addressed (perf rule 5); ?select= projects fields (perf rule 3)."""
    reg = _compiled("registry")
    if not reg:
        raise HTTPException(503, {"error": {"code": "PROJECTIONS_NOT_BUILT",
                                             "message": "run scripts/build-static-site.py first",
                                             "retryable": True}})
    data = {
        "counts": reg.get("counts", {}),
        "layers": reg.get("layers", {}),
        "root_hash": reg.get("root_hash", ""),
    }
    etag = _etag_of(data)
    response.headers["ETag"] = etag
    response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
    inm = request.headers.get("if-none-match")
    if inm and inm.strip("\"") == etag.strip("\""):
        return Response(status_code=304, headers={"ETag": etag})
    if select:
        fields = [f.strip() for f in select.split(",") if f.strip()]
        data = {k: v for k, v in data.items() if k in fields}
    return {"data": data, "provenance": {"surface": "live-registry", "served": "compiled-bytes"}}


@app.get("/openpatala/{layer}")
def openpatala_layer(layer: str, request: Request, response: Response, select: str | None = None):
    """One compiled layer projection (e.g. /openpatala/l0 -> the L0 count artifact).
    ETag + 304 (perf rule 5); ?select= projection (perf rule 3)."""
    rec = _compiled(layer)
    if not rec:
        raise HTTPException(404, {"error": {"code": "LAYER_NOT_FOUND", "message": f"no compiled layer {layer}",
                                             "retryable": False}})
    data = rec if not select else {k: v for k, v in rec.items() if k in select.split(",")}
    etag = _etag_of(rec)
    response.headers["ETag"] = etag
    response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
    inm = request.headers.get("if-none-match")
    if inm and inm.strip("\"") == etag.strip("\""):
        return Response(status_code=304, headers={"ETag": etag})
    return {"data": data, "provenance": {"surface": "live-registry", "served": "compiled-bytes"}}


@app.get("/resolve")
def resolve_work(
    title: str = Query(...),
    author: str | None = None,
    provider: str = "openalex",
):
    """CP4 — the identity crosswalk ("who/what is this"): resolve a work against the modern
    scholarship graph (OpenAlex / Crossref) + ORCID/ROR for people/institutions. Live, additive.

    Design: crosswalk = identity EVIDENCE, not scholarly correctness. Returns RESOLVED / NOT_FOUND /
    UNAVAILABLE with the provider id — the Atlas never claims a crosswalk hit is the canonical work.
    """
    try:
        import sys as _sys
        from pathlib import Path as _Path
        _root = _Path(__file__).resolve().parents[3]  # patala_core->atlas->python->repo root
        _adapters = str(_root / "source-evidence" / "production" / "adapters")
        if _adapters not in _sys.path:
            _sys.path.insert(0, _adapters)
        from metadata_resolver import resolve_openalex, resolve_crossref
    except Exception as _e:  # noqa: BLE001
        raise HTTPException(500, {"error": {"code": "CROSSWALK_UNAVAILABLE",
                                             "message": f"metadata_resolver not importable: {_e}",
                                             "retryable": False}})
    fn = resolve_openalex if provider == "openalex" else resolve_crossref
    try:
        r = fn(title, author)
    except Exception as e:  # noqa: BLE001
        return {"data": {"status": "UNAVAILABLE", "provider": provider, "error": str(e)},
                "provenance": {"surface": "identity-crosswalk", "live": True}}
    return {"data": r, "provenance": {"surface": "identity-crosswalk", "live": True, "provider": provider}}

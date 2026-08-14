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
import json
import os
from typing import Any

from fastapi import FastAPI, HTTPException, Query

from .adapter import AtlasAdapter

app = FastAPI(title="Pāṭala Atlas", version="0.1", description="Pāṭala Authority Graph read API")
_adapter = AtlasAdapter()

# the compiled OpenPatala projections (compute-on-write artifacts served by build-static-site.py)
# this is the LIVE registry surface (object_registry layers), served as immutable bytes — not _load()
OPENPATALA_DIR = os.environ.get(
    "OPENPATALA_DIR", "/mnt/HC_Volume_106427611/ip-graph/site/openpatala")


def _compiled(layer: str) -> dict[str, Any] | None:
    """Read a compiled OpenPatala projection artifact (immutable bytes, compute-on-write)."""
    path = os.path.join(OPENPATALA_DIR, f"{layer.lower()}.json")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)

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
    return list_works(search=q, select=select, filter=filter, sort=sort, cursor=cursor, per_page=per_page)


# ── ADDITIVE: the LIVE registry surface (compiled projections, compute-on-write) ──────────
# The existing /works contract above is UNCHANGED (the factory depends on it). These endpoints are
# additive: they serve the compiled OpenPatala projections (object_registry layers) as immutable bytes.

@app.get("/openpatala")
def openpatala_registry():
    """The live object_registry summary (per-layer counts + immutable root hash)."""
    reg = _compiled("registry")
    if not reg:
        raise HTTPException(503, {"error": {"code": "PROJECTIONS_NOT_BUILT",
                                             "message": "run scripts/build-static-site.py first",
                                             "retryable": True}})
    return {"data": {
        "counts": reg.get("counts", {}),
        "layers": reg.get("layers", {}),
        "root_hash": reg.get("root_hash", ""),
    }, "provenance": {"surface": "live-registry", "served": "compiled-bytes"}}


@app.get("/openpatala/{layer}")
def openpatala_layer(layer: str):
    """One compiled layer projection (e.g. /openpatala/l0 -> the L0 count artifact)."""
    rec = _compiled(layer)
    if not rec:
        raise HTTPException(404, {"error": {"code": "LAYER_NOT_FOUND", "message": f"no compiled layer {layer}",
                                             "retryable": False}})
    return {"data": rec, "provenance": {"surface": "live-registry", "served": "compiled-bytes"}}


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
        _root = _Path(__file__).resolve().parents[3]  # /root/projects/patala (atlas->core->python->root)
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

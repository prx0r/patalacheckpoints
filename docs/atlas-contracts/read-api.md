# TIER 4 — the OpenAlex-grammar read API

*2026-08-13. Exposes the Pāṭala Authority Graph with the OpenAlex query grammar, read-only, over the
compiled Atlas read-model. This is the contract the future Cloudflare Worker/Hono API mirrors.*

## What was built

```text
python/patala_core/atlas/api.py   — FastAPI read API over the adapter (dev)
python/patala_core/atlas/test_api.py — OpenAlex-grammar tests (ALL PASS)
```

## The query grammar (copied from OpenAlex's product architecture)

| Param | Meaning | Example |
|---|---|---|
| `filter=` | exact attribute filters (`!` = negation, `,` = AND, `<`/`>` numeric) | `?filter=translation_status:complete` |
| `search=` | substring search over id/title | `?search=tantraloka` |
| `select=` | field projection (compact payloads, token-efficient for agents) | `?select=id,title` |
| `sort=` | `field` or `-field` (desc) | `?sort=-title` |
| `cursor=` | opaque cursor pagination (base64 offset, NOT `?page=N`) | `?per_page=10&cursor=...` |

## Endpoints

```text
GET /health                       backend (postgres|legacy) + count
GET /works                        list (filter/search/select/sort/cursor)
GET /works/{id}                   one work (dehydrated refs)
GET /editions                     editions (placeholder until TIER 3b populates the table)
GET /search                       alias for /works?search=
```

## Dehydrated references (mommyspeed §8)

A single work returns compact refs, not nested universes:

```json
{ "id": "malinivijayottara", "title": "Mālinīvijayottaratantra",
  "editions": { "count": 0, "href": "/editions?filter=work:malinivijayottara" },
  "factory": { "source_ready": true } }
```

## Agent-actionable errors (§26)

```json
{ "detail": { "error": { "code": "OBJECT_NOT_FOUND",
   "message": "no work nonexistent",
   "suggestion": "use /search?search=...", "retryable": false } } }
```

## Speed doctrine

The adapter's **compiled read-model** is loaded once; every read is a dict operation — no DB, no joins,
no N+1. Filter/search/sort run in-memory over the compiled model. Cursor pagination avoids offset scans
and is a single slice.

## Production path (later)

In prod this becomes a Cloudflare Worker (TypeScript + Hono) + Hyperdrive → Neon, serving the same
grammar. The Python `api.py` is the canonical contract + the dev/seed implementation; the Worker mirrors
it. Split into `/v1/public` (no key) and `/v1/research` (auth) per the access-policy.

## Exit gate (met)

A researcher with no repo access can `curl /works/...` → discover a work, filter, search, select fields,
and page via cursor — through the API alone. Tests ALL PASS.

# PĀṬALA API — REFERENCE (the OpenAlex-grammar read API + translation-availability)

*2026-08-15 · the complete reference for the Pāṭala read API. It speaks the OpenAlex query grammar
(`filter/search/sort/select/cursor`) over the Sanskrit canon + the translation-availability index (the
product). Every response carries honest provenance; nothing claims `verified=true` unless real. The
perf doctrine holds: compiled bytes, ETag→304, read-from-memory, live APIs only at build time.*

---

## 1. RUN IT

```bash
cd /root/patalacheckpoints
PYTHONPATH=/root/patalacheckpoints/python OPENPATALA_DIR=/root/smellycock/site/openpatala \
  SITE_DIR=/root/smellycock/site \
  /root/patalacheckpoints/.venv-atlas/bin/python3 -m uvicorn patala_core.atlas.api:app --port 8791
```

Deps: `fastapi`/`uvicorn` in `.venv-atlas`. Data: the compiled projections + `translation-availability.json`
(built by `pipeline/build_translation_index.py`).

---

## 2. THE ENDPOINTS

### 2.1 `/health` — status
```json
{"backend": "postgres|legacy", "works": 254}
```

### 2.2 `/works` — list works (OpenAlex grammar)
**Query params:** `filter=` · `search=` · `sort=` (`-field`) · `select=` · `cursor=` · `per_page=` (1-500, default 50)
```bash
# filter + select + cursor
GET /works?filter=translation_status:complete&select=id,title&per_page=20
# search
GET /works?search=tantraloka
```
**Response:**
```json
{"count": 20, "total": 254, "next_cursor": "b64...", "works": [{"id": "...", "title": "..."}],
 "provenance": {"api_version": "1.0", "backend": "legacy",
                "warnings": ["unknown select field: X"]}}
```

### 2.3 `/works/{work_id}` — one work
```bash
GET /works/malinivijayottara?select=id,title,translation_status
```
404 → agent-actionable `{error:{code,message,suggestion,retryable}}`.

### 2.4 ⭐ `/works/{work_id}/translations` — the product (translation-availability)
**What it is:** for one work, which translations exist (full/partial/missing), languages, urls,
copyright, factory state, and live-located copies. Serves the **compiled bytes with ETag→304**.
```bash
GET /works/kiranatantra/translations
```
```json
{"data": {"work": "kiranatantra", "coverage": "partial", "has_english": true,
          "languages": ["en","it"], "missing": false,
          "translations": [{"language":"en","translator":"Dominic Goodall","url":"...",
                             "coverage":"opening of Vidyāpāda","complete":false,"tier":"A"}],
          "copyright_hint": "UNDETERMINED",
          "factory": {"next_action": "BUILD_L0_SOURCE_MODE"},
          "live": {"resolved": true, "doi": "10.1080/...", "is_oa": false,
                    "locations": [{"provider":"openalex","url":"..."}]}},
 "provenance": {"surface": "translation-availability", "served": "compiled-bytes"}}
```

### 2.5 ⭐ `/translations` — list translation-availability across works
**Query params:** `search=` (work id/title) · `filter=coverage:full|partial|none, has_english:true|false,
missing:true|false` · `cursor=` · `per_page=`
```bash
# the untranslated targets (the product's headline)
GET /translations?filter=missing:true
# → 192 untranslated works
GET /translations?filter=coverage:full&per_page=5
```
ETag→304 on the compiled index.

### 2.6 `/editions` — editions (placeholder until populated)
### 2.7 `/search` — alias for `/works?search=`
### 2.8 `/openpatala` + `/openpatala/{layer}` — live registry (ETag→304, `select=`)
### 2.9 `/resolve` — identity crosswalk (OpenAlex/Crossref/Unpaywall, live)

---

## 3. THE OPENALEX GRAMMAR (alignment)

| OpenAlex feature | Pāṭala | Notes |
|---|---|---|
| `filter=` | ✅ | exact-match + range on date fields |
| `search=` | ✅ | substring on id+title |
| `sort=` | ✅ | `-field` desc |
| `select=` | ✅ | field projection + `warnings[]` on unknown |
| `cursor=` | ✅ | opaque base64 (not `?page=N`) |
| `per_page` | ✅ | bounded 1-500 |
| ETag/304 | ✅ | `ETag: "sha256-…"` + `If-None-Match`→304 |
| immutable cache | ✅ | `Cache-Control: public, max-age=31536000, immutable` |

---

## 4. THE PERF DOCTRINE (how the API is fast)

- **Compute on write** — `build_translation_index.py` runs the live APIs (OpenAlex/Unpaywall/Crossref)
  at BUILD time, caches; readers get compiled bytes.
- **Read from memory** — `_compiled()` / `_translation_index()` memoize by mtime; no per-request DB/API.
- **ETag→304** — conditional requests return 304 with 0 bytes (verified).
- **0-JS site** — Astro reads the same compiled JSON.

---

## 5. THE HONESTY CONTRACT

- `status: MACHINE_PROPOSED`, NEVER `verified=true`.
- External IDs (M00532, DOIs, OpenAlex IDs) are **crosswalks in provenance**, never canonical identity.
- `UNKNOWN`/`NOT_FOUND`/`UNAVAILABLE` are valid states — the API never fabricates.
- Every external API call records `fetched_at` + uses `mailto` (polite pool).
- **Live APIs run ONLY at build time, never per-request** (perf rule 1 + politeness).

---

## 6. TESTING STATUS (see `research/testing/`)

- atlas-api tests: **ALL PASS**
- translation_availability: **11/11**
- translation_locator: **10/10**
- assess: **16/16**
- red-teamed twice; all findings fixed; defense-in-depth confirmed

---

*The Pāṭala API is the OpenAlex-grammar surface over the Sanskrit canon + the translation-availability
index. It is fast (compiled bytes + ETag), honest (provenance, no fake verified), and documented. The
translation-availability endpoints are the greenfield product nobody else has built for Sanskrit.*

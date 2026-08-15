# API USAGE REFERENCE — polite consumption for the translation-finder

*2026-08-15. The rules for calling the external APIs the translation-finder + metadata resolver use,
so we're polite, rate-limit-correct, and never blocked. "Download the docs for each one so we can use
them politely." This is the consolidated reference — the raw HTML docs are in `./api-docs/`.*

---

## 1. OpenAlex (api.openalex.org)

**Purpose in our stack:** resolve a work → find its translations/editions + OA locations (`locations`,
`best_oa_location`, `open_access`). The rich `locations[]` with `landing_page_url`/`pdf_url` is the
"where a translation lives" signal.

**Polite rules (documented):**
- **THE POLITE POOL:** add `mailto=<your-email>` to EVERY request. This puts you in the polite pool
  (~100k requests/day + much higher per-second limits) instead of the anonymous pool (~100/s).
- **Our `User-Agent`:** `patala-scholar-resolver/0.1 (mailto:dev@patala.local)` (already set in
  `metadata_resolver.py`).
- **Burst limits:** polite pool ≈ 10 req/s burst, ~1 req/s sustained. We already `time.sleep(0.3)`
  between providers — safe.
- **Never scrape** the full dump; use the API with `per-page` + `cursor`.

**Fields we use for translation-availability:**
```json
{
  "title", "doi", "open_access": {"is_oa": bool, "oa_url": "...", "oa_status": "gold|green|closed"},
  "locations": [{"landing_page_url", "pdf_url", "is_oa", "source": {"display_name"}}],
  "best_oa_location": {"landing_page_url", "pdf_url"},
  "authorships": [{"author": {"display_name"}}]
}
```

---

## 2. Crossref (api.crossref.org)

**Purpose:** resolve via DOI; `works` query by title+author. Good for modern scholarly editions/translations.

**Polite rules:**
- Set a descriptive `User-Agent` + `mailto` (polite pool).
- **Rate limit:** no hard documented cap, but they ask ≤ 1 req/s sustained; we sleep 0.3s.
- Use `query.title`, `query.author`, `rows`, `filter=type:`.

**Fields we use:** `DOI`, `title`, `author[]`, `issued.date-parts`, `container-title` (the journal/
publisher = where the translation appears).

---

## 3. Unpaywall (api.unpaywall.org)  ⭐ NEW — to add

**Purpose:** given a **DOI**, return all open-access locations (the "where can I download it" API).
`https://api.unpaywall.org/v2/{doi}?email=<your-email>`

**Why it matters for us:** once we have a DOI (from OpenAlex/Crossref), Unpaywall tells us the
**downloadable OA copy** — the "can we get it" half of translation-availability.

**Polite rules:**
- **Requires `email` param** on every request — no anonymous access.
- ~50k/day free; generous. Sleep between calls.

**Response (relevant fields):**
```json
{
  "doi", "is_oa": bool,
  "best_oa_location": {"url", "url_for_pdf", "version", "host_type", "license"},
  "oa_locations": [{"url", "url_for_pdf", "version", "license", "host_type"}]
}
```

---

## 4. archive.org (advancedsearch.php + metadata API)

**Purpose (already wired in `verify_editions.py`):** search "«work» sanskrit"/"translation" → scans +
editions + old translations.

**Polite rules:**
- Include a `User-Agent` identifying the bot + contact.
- **Rate limit:** be conservative; they throttle aggressive bots. Sleep ≥ 1s between requests.
- `advancedsearch.php` for search; `metadata/{identifier}` for a single item's metadata (formats, urls).

**Fields we use:** `numFound`, `docs[].identifier/title`, then `metadata` for download URLs.

---

## 5. The polite-consumption contract (our code)

```python
USER_AGENT = "patala-scholar-resolver/0.1 (mailto:dev@patala.local)"
MIN_SLEEP = 0.3   # seconds between API calls (all providers)
```
- Every request carries the identifying `User-Agent` + `mailto`/`email`.
- Sleep between providers (already in `metadata_resolver.resolve()`).
- Fail-closed: UNAVAILABLE / NOT_FOUND / UNKNOWN are valid states — never block ingestion on an API.
- Record `fetched_at` provenance on every external call (traceability).

---

## 6. The rate-limit facts (documented values)

| API | Anonymous | Polite (with email) | Our policy |
|---|---|---|---|
| **OpenAlex** | ~100/s | ~100k/day, 10/s burst | `mailto` + 0.3s sleep |
| **Crossref** | ≤1/s suggested | — | 0.3s sleep + UA |
| **Unpaywall** | none (needs email) | ~50k/day | `email` + sleep |
| **archive.org** | throttles bots | be conservative | ≥1s sleep + UA |

---

*The rule: identify ourselves, sleep between calls, fail-closed, record provenance. Never hammer an
API — this is a scholarship corpus, and the APIs are a courtesy we must respect.*

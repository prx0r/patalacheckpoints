# Pāṭala — Development Plan (API-first, bibliography-first)

> **ARCHIVED IMPLEMENTATION PLAN.** Superseded for sequencing by `PROCESS_NOTES.md` and
> the current milestones (Milestone A2 / B1 / B2 / C). Its enduring principles stand —
> API-first, provenance non-negotiable, bibliography as spine, UI last — but its literal
> phase order no longer drives development (much of it is already built). Read
> `PROCESS_NOTES.md`, `STATE_OF_PLAY.md`, and `experiments/advice-response.md` for the
> current plan.

> **Status note (2026-08-10):** The project is now named **Pāṭala** (was Tantrakośa). This document is the original plan; the *current* validated state and milestones live in `CHECKPOINTS.md` and `PROCESS_NOTES.md`, and the strategy in `NORTHSTAR.md`. Checkpoints 1–9 are done: AI-readable bibliography (69 works), corpus manifest, 4k+ stable verse passages, translation contract (4 separated policies), MCP evidence engine (12 tools), our T1 corpus + OCHS manuscript witnesses (1,542, resolved to 18 works), term senses/occurrences, `get_passage_context`, a `resolve/work` proposer, the six formal primitives (assertion/evidence/provenance/review/rights/crosswalk), the raw-corpus concordance, `/api/health` + `/api/stats` + `/api`, and an OpenAPI spec + 72-check verification suite + 7 executable doc examples.

*2026-08-10. The build order for Pāṭala. **The governing decision: the API/MCP contract is the product.** The bibliography is the source of truth; the OpenAPI spec is the contract; the site is a render of the API. Anything we build — reader, workshop, audit, TTS, resources, commentary — is a new endpoint + MCP tool added to that one contract, never a separate silo. This is the machine-facing layer made primary (per `HANDOVER_MCP_API.md`).*

---

## 0. The core decisions (read first)

1. **Schema-first, not code-first.** One schema (`data/atlas/bibliographyTypes.ts`) is the single source of truth for the `BibliographyRecord`. The OpenAPI spec, the API responses, and the TS types are **derived from the same definitions** so they can never drift. If the bibliography schema changes, the API changes with it by construction.
2. **The bibliography is the spine and it is AI-readable.** The `BibliographyRecord` is extended so an agent can answer "which Krama texts lack a complete English translation?" from the JSON alone, with every claim resolving to an evidence-tier — not from prose.
3. **The API/MCP is spec'd first; features are endpoints.** The contract below is the fixed surface. Every future feature (passage reader, term concordance, parallels, audit, TTS, resources, scholar profiles) is defined as an endpoint + an MCP tool in this document *before* any UI is built. The UI is the last thing.
4. **Provenance is non-negotiable.** Every response carries a provenance block and every resource carries its tier (A critical · B text-repo · C scholarly-discovery · D niche-traditional · E discovery/mirror). This is what makes the corpus trustworthy to scholars *and* to agents.
5. **The seven foundations (from `foundationalideas.md`) are the data-model rules**: stable passage IDs, a provenance ledger, proper witness/source model, transcription-vs-normalized-vs-edited separation, terminology as a first-class object, many-to-many translation alignment, versioned annotations. The API surface below is built on these — they are constraints on the schema, not optional features.

---

## 1. The contract — the stable API surface

Every ID is stable (`tantra:text:kubjikamata:3.14`). Every response wraps the `provenance` envelope. The v1 surface (already partially live at `/api/texts`):

| Endpoint | Purpose | Status |
|---|---|---|
| `GET /api` | API index / discoverability | ✅ live |
| `GET /api/health` | operational status + dataset revision | ✅ live |
| `GET /api/stats` | corpus credibility signals | ✅ live |
| `GET /api/texts` | bibliography list; filter by tradition / status / verified | ✅ live |
| `GET /api/texts/:id` | one text's full bibliography record | ✅ live |
| `GET /api/texts/:id/translations` | our working (T1) translations, verse-anchored | ✅ live |
| `GET /api/works` | the work registry | ✅ live |
| `GET /api/works/:id` | one work's metadata | ✅ live |
| `GET /api/works/:id/manuscripts` | a work's OCHS witnesses | ✅ live |
| `GET /api/passages/:id` | a verse-anchored passage (Sanskrit + edition) | ✅ live |
| `GET /api/context/passages/:id` | the deterministic evidence bundle | ✅ live |
| `GET /api/search/passages` | substring search over the corpus | ✅ live |
| `GET /api/manuscripts` | the OCHS manuscript layer (all / by work / by q) | ✅ live |
| `GET /api/relations/:work_id` | typed + confidence + evidence edges | ✅ live |
| `GET /api/terms` | the accepted term ledger | ✅ live |
| `GET /api/terms/:lemma/senses` | accepted senses for a lemma | ✅ live |
| `GET /api/terms/:lemma/occurrences` | surface occurrences (substring, lemmatized:false) | ✅ live |
| `GET /api/term-proposals` | machine/human proposals (never auto-accepted) | ✅ live |
| `GET /api/assertions` | contested claims as reviewable objects | ✅ live |
| `GET /api/crosswalks` | our↔external object mappings | ✅ live |
| `GET /api/concordance` | raw-corpus word tracking (~500 texts) | ✅ live |
| `POST /api/resolve/work` | candidate work identity (machine proposal only) | ✅ live |
| `GET /api/occurrences` | a lemma across texts/traditions/dates | 🔲 next |
| `GET /api/term/history` | a lemma's sense-trajectory | 🔲 |
| `GET /api/parallels` | close parallels for a passage | 🔲 |
| `GET /api/translations` | translation-status + linked translations for a passage | 🔲 |
| `GET /api/commentaries` | traditional/scholarly glosses for a passage | 🔲 |
| `POST /api/audit` | evidence-backed audit of a proposed translation | 🔲 |
| `GET /api/resources` | the Resources layer (from `RESOURCES_SEED.md`) | 🔲 |
| `POST /api/tts/sanskrit` | Sanskrit TTS | 🔲 |
| `GET /api/resolve/:urn` | stable-ID resolver | 🔲 |

The provenance envelope on every response:

```json
{
  "data": {},
  "provenance": { "note": "...", "generated_at": "...", "api_version": "1.0" },
  "warnings": [],
  "license": {}
}
```

**The rule: no endpoint, no UI.** A feature is built as a route-handler + an OpenAPI entry + an MCP tool. If it isn't in this table, it isn't built yet. When it is built, it moves from 🔲 to ✅ here.

---

## 2. Phase 1 — make the bibliography AI-readable (do this first)

The current `BibliographyRecord` (in `bibliographyTypes.ts`) is already close. What it needs to become genuinely machine-consumable:

- **Stable IDs as the identity.** `id: "kubjikamata"` → canonical `urn: "tantra:text:kubjikamata"`. Never let the URL be the identity. Keep aliases on segmentation change.
- **Evidence blocks, not free-text.** `statusEvidence` becomes a structured array: `[{ type: "bibliographic_search", source, url, date, finding }]`. `statusLabel` keeps the exact "No complete English translation located" phrasing.
- **`uncoveredRanges`** on translation records (e.g. `["1.400–end"]`) so an agent can compute gaps, not just read a status word.
- **`related[]` becomes evidence-bearing edges** (aligning with the atlas): `[{ target, relationshipType: "quoted-by" | "borrows-from" | "conceptual-parallel" | "comments-on", scholarlySource, confidence: "established"|"strong"|"possible", relevantPassages[] }]`.
- **Separate root vs commentary** records (already the convention; enforce it).
- **Translation-typology** (`scholarly | traditional | independent | working`) + the three-site-badges: PUBLISHED / WORKING (AI-assisted, not peer reviewed) / COMMUNITY REVIEWED.
- **The own-corpus wiring:** the T1/T2/T3 stack (`translations/01_t1_working/...`, `03_t2_alternate`, `05_t3_final`) surfaces as `type: "working"` translations with a per-text status line (`T1-done → R1-done → ...`), a `sourceTextUsed` pointer, and a `notPeerReviewed: true` flag.
- **Acquisition registry:** `targetacquired.md`'s ACQUIRE / manuscript-request / locate-witness statuses become a field on the record.

### The audit order (per the migration spec)
Trika-10 ✅ → Krama-10 → Kubjikā-10 → Kaula-10 → Bhairava-10 → Pratyabhijñā-10 → Siddhānta-10. Each school moved into `audited.ts` at full depth. The seed (70 texts, `verified:false`) stays a clearly-marked section until audited.

### Cleanup before proceeding
- `data/atlas/bibliography.ts` (the old 744-line seed with its own local `BibliographyRecord`/`BibliographyResource` interfaces) is redundant with `bibliographySeed.ts` + `bibliographyTypes.ts`. Reconcile so there is exactly one schema and one seed file.

---

## 3. Phase 2 — the read API + OpenAPI spec

The deliverable is **the API docs**, not the route code. Order:

1. **OpenAPI spec** (`docs/openapi.yaml` or generated from the types) covering every endpoint in §1, with the `BibliographyRecord` schema as its central component.
2. **`GET /api/texts`** — already live; bring it to the full record (structured evidence, uncoveredRanges, edges, working-translation wiring).
3. **`GET /api/texts/:id`** — the full `BibliographyRecord` by stable id/urn.
4. **`GET /api/passages/:id`** — parse `01_t1_working/*.md` into verse-anchored records `{work, chapter, verse, sanskrit, translation, flags}`; serve by `tantra:text:kubjikamata:3.14`. This is the first endpoint that actually needs the corpus, not just the bibliography.
5. **`GET /api/resources`** — the `RESOURCES_SEED.md` federation as typed, tradition-tagged, tiered resource objects.

**Data source for now:** serve the TS data directly (no DB yet). The passage-index reads the `.md` translation files on disk. A JSON/SQLite store only arrives when the corpus demands it.

---

## 4. Phase 3 — the MCP server

Expose the read API as MCP tools so an LLM can call them inside a chat or a translation agent. The tool surface maps 1:1 to the endpoints:

```
search_texts · read_passage · find_term_occurrences · get_term_history ·
find_parallel_passages · get_translation_context · get_commentary ·
get_manuscript_variants · audit_translation · search_resources · tts_sanskrit
```

The MCP is **read-only over the API** — it never writes corpus truth. It carries the provenance hierarchy in every tool result so the agent treats site-generated material as provisional (working translations, AI analysis) vs primary (critical editions, traditional commentaries). This is the FoJin principle we're adopting.

---

## 5. Phase 4 — the provenance-driven features (on top of the API)

These are the features that only make sense once the contract exists, because they consume the corpus through the API:

- **`POST /api/audit`** — evidence-backed warnings (NEGATION / TERM_DRIFT / UNSUPPORTED_ADDITION / PARALLEL_CONFLICT / COMMENTARY_CONFLICT / GRAMMATICAL_UNCERTAINTY / SOURCE_UNCERTAINTY), modeled on `R1_CONTENT_ENGINEERING.md`. An audit surfaces evidence for review; it never claims a translation is "wrong."
- **`GET /api/occurrences` + `GET /api/term/history`** — the diachronic semantic concordance (the killer feature from `apideas.md`), seeded from the glossary dossiers and the R1 cross-text parallel-map.
- **`GET /api/parallels`** — parallel types kept separate (EXACT QUOTATION / VERY CLOSE / TERMINOLOGICAL / CONCEPTUAL).
- **`POST /api/tts/sanskrit`** — IAST/Devanāgarī, śloka/mantra/prose modes, pada-segmentation, synchronized audio.
- **The UI** (last): the `/texts`, `/traditions`, `/people`, `/concepts` routes and the passage reader render the API. The research-sidecar (meaning/occurrences/glosses/parallels/commentary per selected term) from `foundationalideas.md` §killer is one component reading the occurrence/history/commentary endpoints.

---

## 6. The rule going forward

**Everything is an endpoint.** When you want to add a capability:
1. Write it into the endpoint table (§1) + the OpenAPI spec.
2. Add the MCP tool that maps to it.
3. Build the route-handler + the data it reads.
4. Build the UI that renders it (last).

If it can't be expressed as an endpoint + MCP tool, it's probably not part of the hub — or the contract needs extending first. The bibliography (AI-readable, provenance-led, stable-ID'd) is the spine everything hangs from, exactly as `endgame2.md` puts it: *"the bibliography becomes the index joining everything together: manuscript → Sanskrit → published translation → working translation → scholarship → lecture → commentary → AI retrieval."*

---

## 7. Immediate next actions (in order)

- [ ] **Reconcile the seed files** — one schema (`bibliographyTypes.ts`), one seed (`bibliographySeed.ts`); retire the duplicate `bibliography.ts` interfaces.
- [ ] **Extend `BibliographyRecord`** for full AI-readability (urn, structured `statusEvidence[]`, `uncoveredRanges`, evidence-bearing `related[]`, working-translation wiring, acquisition status).
- [ ] **Write the OpenAPI spec** (`docs/openapi.yaml`) with the full endpoint table.
- [ ] **Bring `/api/texts` to the full record**; add `/api/texts/:id`.
- [ ] **Continue the school audits** (Krama-10 next) into `audited.ts` at full depth.
- [ ] **Add the MCP server** exposing the read tools.
- [ ] Then the corpus-bound features (passages, occurrences, parallels, audit, TTS) — each as endpoint + MCP tool, then a render.

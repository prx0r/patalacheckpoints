# Handover — the Tantra Hub MCP + API (the machine-facing translation infrastructure)

*2026-08-10. For the agent who builds the API/MCP layer. The vision (per `docs/endgame2.md` + `patala/HANDOVER_SITE.md`): the Tantra Hub isn't just a website — it's a **scholarly translation environment that retrieves context on demand**, so an AI (ChatGPT/Claude/Codex/a specialist agent) can do the work we've been doing by hand (finding sources, identifying translation-status, comparing terminology, auditing translations), with every claim resolving to a cited source. The API + API docs are the highest-priority deliverable.*

---

## The goal, in one line

> Expose the corpus + the translation pipeline + the anchors + the bibliography + the TTS as a **retrieval-and-audit API**, then a **model-context-protocol (MCP) server** so an LLM can call it inside a chat or a translation agent — producing evidence-backed translations and audits, not hallucinated ones.

## The core workflow (the formal translation flow, machine-ified)

```text
Translator opens an untranslated verse (stable ID)
        ↓
selects a difficult term (e.g. vimarśa)
        ↓
MCP calls get_term_context()          → lemma in this text / ±150y texts / same school /
                                           adjacent schools / commentary glosses / published
                                           translations / parallels / borrowings / variants
        ↓
LLM proposes a translation
        ↓
MCP calls audit_translation()         → evidence-backed warnings (see §A)
        ↓
human reviews → versioned community text
```

## A. The API endpoints (the core surface)

All on stable IDs (`tantra:text:kubjikamata:3.14`, `tantra:tradition:krama`, `tantra:concept:vimarśa`, `tantra:person:abhinavagupta`).

| Endpoint | Purpose | Example |
|---|---|---|
| `GET /texts` | the bibliography (filter by tradition, translation-status, has-sanskrit...) | `?tradition=krama&english_complete=false` |
| `GET /texts/:id` | a text's full bibliography record (the `BibliographyRecord`) | `/texts/kubjikamata` |
| `GET /passages/:id` | a passage: Sanskrit + working translation + commentary + parallels | `/passages/tantra:text:kubjikamata:3.14` |
| `GET /occurrences` | a lemma across texts/traditions/dates | `?lemma=vimarśa&tradition=trika&date_from=850&date_to=1050` |
| `GET /term/history` | a lemma's sense-trajectory (the dossiers) | `?lemma=kula` |
| `GET /parallels` | close parallels for a passage | `?passage=kubjikamata:3.14` |
| `GET /translations` | the translation-status + the linked translations | `?passage=ipk:1.5.12` |
| `GET /commentaries` | the traditional/scholarly glosses | `?passage=tantraloka:3.67` |
| `GET /manuscripts` | the witnesses + the variants | `?text=tantrasadbhava` |
| `POST /audit` | the evidence-backed audit of a proposed translation | `{ id, proposed, ... }` |
| `POST /tts/sanskrit` | Sanskrit TTS (Devanagari/IAST, śloka/mantra mode) | `{ text, mode: "śloka" }` |

## The audit types (the `audit_translation` contract — model on the R1-work)

The R1s we ran are the prototype of this. An audit returns **evidence-backed warnings**, not vague critique:

```json
{
  "warnings": [
    { "type": "NEGATION", "detail": "Possible omitted na.", "evidence": "KMT 3.14 source" },
    { "type": "TERM_DRIFT", "detail": "śakti translated differently from neighbouring occurrences." },
    { "type": "UNSUPPORTED_ADDITION", "detail": "English concept has no obvious Sanskrit support." },
    { "type": "PARALLEL_CONFLICT", "detail": "Close parallel (TĀ 3.xx) translated differently." },
    { "type": "COMMENTARY_CONFLICT", "detail": "Jayaratha's gloss does not support the reading." },
    { "type": "GRAMMATICAL_UNCERTAINTY", "detail": "Compound admits two parses." },
    { "type": "SOURCE_UNCERTAINTY", "detail": "Witnesses disagree at the locus." }
  ],
  "review_only": true  // ≠ "translation wrong" — differs from parallels/gloss; evidence →
}
```

## The provenance hierarchy (the single most important principle)

Every returned object carries its **evidence-tier**, so agents treat site-generated material as provisional, not scholarship:

```text
MANUSCRIPT
CRITICAL EDITION
PUBLISHED TRANSLATION
TRADITIONAL COMMENTARY
PEER-REVIEWED SCHOLARSHIP
SCHOLAR LECTURE
COMMUNITY CONTRIBUTION
SITE WORKING TRANSLATION
AI-GENERATED ANALYSIS
```

An agent is instructed: prefer critical editions + traditional commentaries as primary evidence; use peer-reviewed scholarship for interpretation; treat Tantra Hub working translations + AI analyses as provisional.

## B. The data sources (what the API reads)

- **The bibliography**: `patala/data/atlas/bibliographyTypes.ts` (the `BibliographyRecord` schema — root-vs-commentary, coverage, style, tiers) + `audited.ts` (the Trika-10) + `bibliographySeed.ts` (the 70-text seed). The API serves these.
- **The corpus / Sanskrit**: `sanskritree/sources/` (the muktabodha-lib ~500 texts, the gretil2, the round3 acquisitions: KMT, Timirodghāṭana, Ciñciṇī, Kramasadbhāva, Śambhunirṇaya...). The concordance (`sanskritree/.concordance_index.json`) is the full-text index.
- **The translations**: `sanskritree/translations/01_t1_working/*.md` (the working T1s — the KMT full, the Kulasāra, the Tārārahasya, the Kramasadbhāva 1–4, etc.) + `02_r1_review/*.md` (the audits) — these seed the `passages` + `translations` + `commentary` endpoints.
- **The dossiers / anchors**: `sanskritree/saivamap/dossiers/*.md` (the 24 lemmas), `sanskritree/corpus/targets/canonical_reference_map.md`, and the Dyczkowski-stack (`/root/projects/tantraloka/texts-clean/*`) as the anchor-texts.
- **The stable-ID mapping**: the canonical `tantra:` scheme (from `docs/endgame2.md`).

## C. The build plan (the recommended order)

1. **The data layer**: a JSON/SQLite store (or serve the TS directly) — the bibliography records + the passage-index + the concordance. The `BibliographyRecord` + the `get_text_status`/`get_related_texts` first.
2. **The read API**: a Next.js route-handler layer (`app/api/*`) or a small standalone Node/Express server exposing the endpoints above, with **OpenAPI docs** (the API docs = the deliverable). Every response carries its `evidence-tier`.
3. **The passage + translation endpoints**: parse the `01_t1_working/*.md` into verse-anchored records (the `{work, chapter, verse, sanskrit, translation, flags}`) → serve `passages/:id`, `translations`, `commentaries`.
4. **The audit endpoint**: `POST /audit` — wire the R1-findings as the audit-types, comparing the proposed rendering against the concordance (occurrences), the parallels, and the glossary-dossiers.
5. **The TTS endpoint**: `POST /tts/sanskrit` (Devanagari/IAST, śloka/mantra/prose modes, pada-verse segmentation, speed) → every Sanskrit passage gets a play-button; a stable audio ID (`/audio/tantraloka:1.1`).
6. **The MCP server**: a model-context-protocol server exposing the API as MCP tools (`get_passage`, `find_parallel_passages`, `get_term_context`, `audit_translation`, `get_text_status`, `get_manuscript_variants`, `get_traditional_commentary`, `tts_sanskrit`), so an LLM can call it inside ChatGPT/Claude/Codex.

## D. The scholar-facing web layer (reuse the API)

The website renders the same API: the bibliography pages (already built at `/bibliography`), the per-text pages with the dropdowns (translations / Sanskrit-sources / scholarship, tier-badges), the text-reader (Sanskrit | working translation | commentary), and the TTS play-buttons. The API is the single source of truth; the site is a render of it.

## The resources to read (from the main repo)
- `docs/endgame2.md` — the full spec (the machine-facing layer, the audit-types, the provenance hierarchy, the TTS).
- `sanskritree/translations/_meta/R1_CONTENT_ENGINEERING.md` — the R1-findings = the model for the `audit` endpoint.
- `sanskritree/corpus/targets/targetacquired.md` — the acquisitions (the corpus the API exposes).
- `sanskritree/CONTEXT_AND_ANCHORS.md` — the reading-list.
- `patala/data/atlas/bibliographyTypes.ts` + `audited.ts` — the bibliography schema (the API's first endpoint).

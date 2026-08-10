# apideas — the Tantra Hub Research API (proposal)

*2026-08-10. The strongest version: NOT "an API for Tantra content" but a **research API for working with difficult historical Sanskrit corpora**, with Tantra as the first deep domain. The pieces exist separately (Muktabodha 570+ e-texts, GRETIL, Sanskrit Heritage, Bilara segment-addresses, Crossref/OpenAlex, FoJin-MCP); **what is missing is the join between them.** This is the proposal for the API + MCP + institutional layer. The moat is the accumulated **relationship-data** (manuscript→text→edition→translation→scholar→term→passage→audit), not the Sanskrit itself.*

---

## The base + the envelope

```text
https://api.tantrahub.org/v1/
```

Every response carries a provenance block (non-negotiable):

```json
{
  "data": {},
  "provenance": [],
  "warnings": [],
  "license": {},
  "generated_at": "...",
  "api_version": "1.0"
}
```

## 1. Stable identifiers (FoJin's best idea — permanent resolvable IDs)

```text
th:text:tantraloka            th:text:tantraloka:3.67
th:text:kubjikamata:3.14
th:person:abhinavagupta
th:tradition:krama
th:term:vimarsa
th:ms:ngmpp:A41-3
th:work:ratie:2010:dreamer-yogin
```

```http
GET /resolve/{urn}        # → Sanskrit, source-edition, translations, commentaries, a permanent reader URL
```

## 2. Text catalogue

```http
GET /texts
GET /texts/{id}
GET /texts?tradition=krama&author=abhinavagupta&date_from=850&date_to=1050
GET /texts?translation_status=no_complete_english&has_etext=true&has_manuscript=true
```

Record: `id, title, alternate_titles, traditions[], date{earliest,latest,certainty,evidence[]}, sanskrit_sources[], manuscripts[], translations[], commentaries[], scholarship[], related_texts[]`.

This fixes the recurring pain: **"What actually exists for this text?"**

## 3. Translation registry (one of the real moats)

```http
GET /texts/{id}/translations
```

```json
{
  "text": "malinislokavarttika",
  "status": "partial",
  "translations": [{ "language": "en", "translator": "Jürgen Hanneder", "coverage": "1.1-1.399", "complete": false, "kind": "scholarly", "publication_year": 1998, "url": "...", "license": "copyright" }],
  "uncovered_ranges": ["1.400-end"],
  "status_checked": "2026-08-10"
}
```

```http
GET /translations/missing?tradition=krama
```

An agent can now answer "which Krama works have no complete English translation?" without Googling badly.

## 4. Passage API (the basic unit of research)

```http
GET /passages/{urn}
```

```json
{
  "urn": "th:text:tantraloka:3.67",
  "sanskrit": "...",
  "edition": { "editor": "...", "publication": "...", "page": 123 },
  "translations": [{ "translator": "...", "text": "...", "status": "published" }],
  "commentaries": [],
  "variants": [],
  "citations": []
}
```

Adopt **Bilara's immutable-segment-ID** principle: root / translation / comment / variant all align to the same segment.

## 5. The killer feature: historical term search

```http
GET /terms/{lemma}/occurrences?tradition=krama&author=&text=&date_from=850&date_to=1050&genre=&region=&window=2
```

```json
{
  "lemma": "kula",
  "hits": [
    { "passage": "th:text:...", "date": 925, "tradition": ["Krama"], "sanskrit": "...", "translation": "...", "local_context": "...", "sense": "..." }
  ]
}
```

So an LLM translating "kula" asks `find_term_occurrences(term="kula", traditions=["Krama","Kaula"], date="850-1050")` instead of getting "family; clan" from Monier-Williams. **A Tantra-specific diachronic semantic concordance tied to translations/commentaries/manuscript-provenance** — that's the join nobody provides.

## 6. Term-history endpoint

```http
GET /terms/{lemma}/history
```

Return the sense-trajectory (Bhairava corpus 850–950 → Utpaladeva c.950 → Abhinava c.1000 → Kṣemarāja 11th-c.) with the actual passages under each node — and crucially:

```json
{ "claims": [ { "claim": "...", "status": "scholarly_consensus" | "site_reconstruction", "evidence": [...] } ] }
```

Never let AI-generated historical interpretation masquerade as primary evidence.

## 7. Parallel-passage search (potentially the single best translation tool)

```http
POST /parallels/search
```

```json
{ "passage": "th:text:kubjikamata:3.14", "traditions": ["Kubjikā","Trika","Kaula"], "date_window": 200, "limit": 20 }
```

Return the parallel **types kept separate**:

```text
EXACT QUOTATION           0.98   Tantrasadbhāva 6.13
VERY CLOSE PARALLEL       0.91   Triśirobhairava fragment 17
TERMINOLOGICAL PARALLEL   0.82   Tantrāloka 29.14
CONCEPTUAL SIMILARITY     0.71   ...
```

Distinguish quotation / adaptation / lexical-parallel / merely-semantic-similarity.

## 8. Translation-context endpoint (purpose-built for LLM translators)

```http
POST /translation/context
```

Input `{ "passage": "th:text:...", "target_language": "en" }` → the whole **translation evidence packet**: root, morphology[], dictionary_entries[], same-text/same-author/same-tradition/contemporary usage[], parallel_passages[], traditional_commentary[], published_translations[], scholarly_discussion[], manuscript_variants[].

## 9. Translation-audit API (one of the most monetisable pieces)

```http
POST /translations/audit
```

Input `{ "passage_urn": "th:text:...", "translation": "..." }` → findings:

```text
NEGATION_MISMATCH · TERM_POLICY_DRIFT · NUMBER_MISMATCH · UNSUPPORTED_ADDITION ·
OMISSION · GRAMMATICAL_AMBIGUITY · COMMENTARY_CONFLICT · PARALLEL_CONFLICT ·
MANUSCRIPT_VARIANT · LOW_CONFIDENCE_PARSE
```

```json
{ "status": "review", "findings": [{ "type": "TERM_POLICY_DRIFT", "severity": "medium", "term": "kula", "message": "Rendering differs from nearby usage.", "evidence": ["th:text:...","th:text:..."] }] }
```

It **never pretends audits prove a translation wrong** — it surfaces evidence for human review.

## 10. Manuscript API

```http
GET /manuscripts  GET /manuscripts/{id}  GET /texts/{id}/manuscripts
```

Fields: shelfmark, repository, ngmpp_reel, script, folios, complete, date, scan{available,access}, transcription{}, edition{}. Later support **IIIF manifests** (`GET /manuscripts/{id}/iiif`) so scholars compare folios/transcriptions in the reader without Tantra Hub owning the images.

## 11. Bibliography API (federate Crossref/OpenAlex, don't reinvent)

```http
GET /scholarship?text=tantraloka  GET /scholarship?concept=vimarsa  GET /scholars/isabelle-ratie
```

Use DOI / ORCID / OpenAlex-ID / Crossref / ISBN / WorldCat. Our contribution is the **text↔passage↔concept↔article relationship** that Crossref has no idea about:

```text
THIS ARTICLE → discusses → ĪPK 1.3.7
THIS ARTICLE → discusses concept → apoha
THIS LECTURE → comments on → Tantrāloka 3.1–20
```

## 12. Resource API (the weird gold)

```http
GET /resources?tradition=krama&type=lecture&access=free&provider=mahanaya
```

Resource types: critical_edition, manuscript, etext, translation, commentary, article, book, lecture, course, audio, dictionary, legacy_site, bibliography, software. This is where obscure things like ShivaShakti and Ambā stay useful.

## 13. Sanskrit NLP (normalized layer over existing tools — don't rebuild)

```http
POST /sanskrit/analyse  POST /sanskrit/sandhi  POST /sanskrit/morphology  POST /sanskrit/transliterate
```

```json
{ "tokens": [{ "surface": "śaktir", "lemma": "śakti", "case": "nom", "number": "sg", "gender": "f" }], "analyses": [{ "provider": "heritage", "confidence": null }], "alternative_analyses": [...] }
```

Do **not** hide disagreement. Sanskrit Heritage is the upstream integration.

## 14. Sanskrit TTS

```http
POST /audio/sanskrit
```

Input `{ "text": "...", "scheme": "iast", "mode": "verse", "speed": 0.85 }` → `{ "audio_url": "...", "segments": [{ "text": "...", "start_ms": 0, "end_ms": 913 }] }` (timing-aligned, so the site highlights Sanskrit while spoken). Modes: verse / prose / metrical / pedagogical. A plausible **paid compute endpoint** later.

## 15. MCP (first-class)

Initial tools:

```text
search_texts · read_passage · find_term_usage · find_parallel_passages ·
get_translation_context · get_translations · get_commentary ·
search_scholarship · lookup_manuscript · audit_translation
```

The UX: "Claude, translate this verse" → the agent calls read_passage → analyse_sanskrit → find_term_usage → find_parallel_passages → get_commentary → get_published_translations → propose → audit. **That's the research workflow we currently do manually.** FoJin proves the read-only-MCP viability.

## 16. Research packets (for institutions)

```http
POST /research/packet   { "text": "tantrasadbhava", "chapter": 3 }
```

Generates SOURCE TEXT / MANUSCRIPT WITNESSES / EDITIONS / TRANSLATIONS / CITED SCHOLARSHIP / TECHNICAL TERMS / PARALLELS / CITATIONS / OPEN QUESTIONS, exportable as JSON / TEI-XML / Markdown / PDF / Zotero-RIS / BibTeX. Where academics stop thinking "interesting website" and start thinking **research infrastructure**.

---

## Open versus paid

**Free/public** (how the site becomes canonical): text-metadata, translation-status, bibliography, resource-directory, stable-URNs, basic passage-retrieval + search, external-links, manuscript-metadata, low-volume MCP. **Never paywall "has this text been translated?"** — that kills the network effect.

**Paid individual/research** (expensive computation): high-volume semantic search, parallel discovery, translation-context packets, translation-audits, bulk TTS, large exports, private projects, larger API-quotas. Tiers: Researcher Pro / Lab / Institution.

## The institutional product (more interesting financially than consumers)

1. **Private institutional corpus** — 2,000 scans + transcriptions + private notes + unpublished editions → private search/RAG/translation-workspace/term-concordance/scholar-annotations/MCP. *Their materials never become public unless they choose.*
2. **Digitisation infrastructure** — scan-ingestion, metadata-normalization, IIIF, transcription-workspace, stable-IDs, TEI-export, API.
3. **Translation projects** — a funded critical-edition (e.g. the Jayadrathayāmala): workspace, segment-alignment, translation-memory, version-history, review, citation, audit, publication, API.
4. **Institutional API licences** — copy the Crossref model: open-API (reasonable limits) + institution-API (quotas, bulk, SLA, priority, private-datasets, SSO, audit-logs). An institution pays for reliability + integration + compute + private infrastructure + support, not `GET /texts`.
5. **Hosted research environments** — "Tantra Hub Scholar Cloud": a project (members, private transcripts/drafts/annotations, public selected-editions), annual fee.

## Who could realistically collaborate

- **Text holders**: Muktabodha, IFP, EFEO, manuscript libraries, archives. (Muktabodha + IFP/EFEO already digitised 2,000+ transcripts / 200,000 pages and are transcribing 75 more.)
- **Scholarly projects**: Hamburg tantric studies, Kaula Studies, individual critical-edition projects.
- **Universities**: South Asian Studies, Religious Studies, Sanskrit, Digital Humanities.
- **Publishers**: critical editions, translation series.
- **Tools**: GRETIL, Sanskrit Heritage, OpenAlex/Crossref.

The pitch: **"We are building an open interoperability and research layer over existing Sanskrit archives. We don't replace your collection or claim ownership. We make it easier to discover, cite, compare, translate and computationally study — with provenance always returning to you."**

## The actual moat

It isn't owning the Sanskrit (keep it open/federated). The moat is the accumulated **relationship-data**:

```text
this manuscript → witnesses this text
this edition → uses these manuscripts
this translation → covers verses 1–399
this scholar → interprets this passage
this term → occurs in these 87 passages
this passage → is adapted from this earlier text
this commentary → glosses this word
this translation → triggered these audit warnings
```

After five years *that graph* is hard to reproduce — and unlike generic embeddings, it's useful to both humans and machines.

## The mission (technical)

> **Tantra Hub is a provenance-preserving interoperability layer for Sanskrit textual scholarship.**

Tantra is the first corpus, but don't hard-code it so it's the only possible corpus:

```text
/api/corpora/tantra   /api/corpora/nyaya
/api/corpora/buddhist-sanskrit   /api/corpora/vedanta
```

## The v0 (just these eight endpoints)

```http
GET  /texts
GET  /texts/{id}
GET  /passages/{urn}
GET  /search
GET  /terms/{term}/occurrences
GET  /resources
POST /translation/context
POST /translations/audit
```

Those eight already create something that doesn't currently exist for this field.

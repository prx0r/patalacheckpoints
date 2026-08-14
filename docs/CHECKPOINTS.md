> **ARCHIVED / SUPERSEDED** — kept for history only. Do NOT follow as current. See `docs/INDEX.md` + `docs/DOCS-AUDIT.json` for the canonical doc for this concern.

# Tantra Hub — Build Checkpoints

*A running log of validated milestones. Each checkpoint = a target that is **functioning, validated, and integrated into the API** — nothing is "done" until the API can serve it. The API/MCP is a loose surface that grows as we build useful things, not a rigid pre-spec.*

---

## Checkpoint 4 — ✅ Translation contract + MCP v1 + proof chapter

**Status: VALIDATED.** MCP server initializes and all 6 tools return real evidence via a stdio JSON-RPC test against the live site. Build clean.

### Target
Turn the translation process into a formal, evidence-grounded skill that an MCP serves — so ChatGPT/Claude can translate in our house style, and each translation emits reusable structured data, not prose.

### Delivered
- **`docs/TRANSLATION_SKILL.md`** — the frozen T1 contract: source hierarchy, ambiguity/[X] handling, Sanskrit retention, close-vs-reading, terminology consistency, parallel-constrains-not-dictates, no-copying of existing translations, audit checklist, mandatory provenance, publishable-T1 gate, and the **required machine output schema** (`passage_id`, `source`, `close_translation`, `reading_translation`, `lexical_decisions[]`, `grammatical_notes[]`, `ambiguities[]`, `evidence_used[]`, `parallels[]`, `existing_translation_comparisons[]`, `unresolved[]`, `confidence`, `pipeline_stage`). Maps 1:1 to the house T1 markdown.
- **`docs/STYLE_GUIDE.md`** — house voice: retention list, IAST, capitalisation policy, compound parse handling, supplied-English auditability, range-not-default, anti-anachronism rule.
- **`research_roles` on the manifest** — anchor function vs tradition membership (tantraloka = synthesis/citation_source; kramasadbhava = primary_scripture/translation_target/terminology_anchor).
- **`data/terms.json`** — the small evidence-based term ledger (15 lemmas: kula, krama, śakti, khecarī, vimarśa, prakāśa, spanda, saṃvit, parāmarśa, svātantrya, visarga, mātṛkā, uccāra, āveśa, śūnya), each with senses + preferred renderings + avoid + notes.
- **`mcp/` server (v1)** — 6 evidence-retrieval tools over the live API + term ledger + corpus translations: `get_work`, `get_source_passage`, `search_passages`, `get_related_works`, `find_term_occurrences`, `get_existing_translations`. Read-only; the model stays the translator.
- **Proof chapter** — `docs/PROOF_T1_kramasadbhava.md`: Kramasadbhāva maṅgala 1.8–1.12 translated under the contract into the machine schema (close + reading, 2 term decisions on tracked lemmas, 5 `[X]` ambiguities, 3 candidate parallels, evidence + existing-translation comparisons).

### Validated
- MCP: initialize ok; 6 tools listed; `get_source_passage` → Sanskrit + edition; `find_term_occurrences` → senses + 3 occurrences; `get_existing_translations` → files + excerpt; `get_related_works` → edges.
- `npm run build` clean (MCP lives in its own `mcp/` dir with the SDK, isolated from the Next build).

### Notes / next (candidate Checkpoint 5)
- The proof demonstrates the factory on one text. To make the MCP broadly useful, grow the **anchor neighborhoods** deliberately (per `TRANSLATION_SKILL_SPEC.md`): around Kramasadbhāva (Devīpañcaśataka, Mahānayaprakāśa, Kramastotra) and around Kubjikāmata (Ṣaṭsāhasra, Śrīmatottara, Kularatnoddyota, Ciñciṇī) — NOT all 500 Muktabodha files.
- v1.1 MCP (once the lemma layer matures): `get_term_senses`, `find_parallel_passages`, `get_translation_context`, `audit_translation`.

---

## Checkpoint 3 — ✅ The corpus manifest (works registry + passage layer), served by the API

**Status: VALIDATED.** `npm run build` clean; `/api/works`, `/api/relations/:work_id`, `/api/passages/:id`, `/api/search/passages` smoke-tested live.

### Target
Make the corpus computable (per `CORPUS_MANIFEST.md`): what texts do we have, what are they, where do they sit historically, and how do we retrieve exact passages — so the MCP can mediate the corpus instead of ChatGPT facing a directory of Sanskrit files.

### Delivered
- **Work registry** (`data/corpus/works.ts`): all 69 works (audited + seed) as `CorpusWork` — stable id + urn, traditions with explicit certainty, date range with certainty (omitted where unknown), translation status, source editions. Exposed via `GET /api/works` (filter by tradition/status/verified) + `GET /api/works/:id`.
- **Relations** (`data/corpus/relations.ts`): atlas edges (typed + confidence + evidence) as `CorpusRelation`. Exposed via `GET /api/relations/:work_id` — the ranking substrate (direct textual relative > same tradition).
- **Passage layer** (`scripts/segment-kramasadbhava.mjs` + `data/corpus/passages/kramasadbhava.jsonl`): segmented Kramasadbhāva (570 passages, chs. 1–7) into verse-anchored passages with stable IDs `tantra:text:kramasadbhava:{ch}.{verse}`. Loaded via `data/corpus/passages.ts` (lazy, cached).
- **Passage API**: `GET /api/passages/:id` (by id or urn) + `GET /api/search/passages?q=` (coarse substring over sanskrit + id; `work_id` + `limit` filters).

### Validated
- `/api/works` → 69; `?tradition=Krama` → 11; `/api/works/kramasadbhava` → krama / partial.
- `/api/relations/spandakarika` → 3 typed edges (contains / develops-from / contains).
- `/api/passages/tantra:text:kramasadbhava:1.2` → Sanskrit + location.
- `/api/search/passages?q=bhairava` → 48 hits.
- 404 on miss; 400 on missing search query.

### Notes / next (candidate Checkpoint 4)
- The segmenter is format-specific to clean `||ch/verse` IAST files. GRETIL/HTML e-texts (kubjikamata, tantraloka) need their own parsers — segment them next to grow the passage corpus.
- Then the **MCP server** (v1 tools from `TRANSLATION_SKILL_SPEC.md`: get_source_passage, read_passage, search_corpus, find_term, get_related_texts) on top of this manifest.

---

## Checkpoint 2 — ✅ Full-depth bibliography for all schools, served by the API

**Status: VALIDATED.** `npm run build` clean; `/api/texts` + `/api/texts/:id` smoke-tested live.

### Target
Bring all 60 school records (`seed60.md`) to the same full `BibliographyRecord` depth as the audited Trika-10, so the API serves a consistent, AI-readable record for every text.

### Delivered
- **Rewrote `bibliographySeed.ts` as full `BibliographyRecord[]`** (verified:false, **58 records**), enriched from `seed60.md` — the 6 schools at full depth: Siddhānta (10), Bhairava/Vidyāpīṭha (8), Kaula (10), Krama/Kālīkula (10), Kubjikā/Paścimāmnāya (10), Pratyabhijñā (10). Fields now include: coverage-qualified `translations[]` (language / translator / coverage / type / tier), tiered `textSources[]`, `manuscripts[]` (NGMPP/NAK sigla), `scholarship[]`, `statusEvidence` (the audit finding), and the 10 seed corrections (Ajitāgama complete, Kāmikā/Pauṣkara/Sarvajñānottara partial, Kulārṇavatantra multiple, Śivadṛṣṭi large-portion, Netra chs.1–8 forthcoming, Niśvāsa Guhyasūtra distinction, Manthānabhairava khaṇḍa distinction, Utpaladeva's Vivṛti fragmentary).
- **Cross-listing resolved without duplication.** Tantrasadbhāva + Mālinīvijayottara (cross-listed in seed60) already live full-depth in `audited.ts` (verified:true) with both tradition tags; they are not duplicated in the seed, so a given `id` is never returned twice. Seed = 58; total API = 69 (11 audited + 58 seed).
- **Dropped the lossy `seedToRecord` mapping** from `/api/texts` + `/api/texts/:id` — both routes now serve `[...audited, ...seed]` directly (both already `BibliographyRecord`), one consistent shape, no data loss.
- **Updated `/bibliography` seed section** to render the new full-depth shape (`r.work` / `r.statusLabel`).

### Validated
- `/api/texts` → 69; `?verified=true` → 11 (Trika-10); `?verified=false` → 58.
- `?tradition=Krama&status=none` → 3 (kulasāra, kramavilāsastotra, kaulasūtra).
- `/api/texts/netratantra` → full depth (translations w/ translator+coverage, textSources, manuscripts, status partial).
- `/api/texts/ajitagama` → correction reflected (complete, 5-vol annotated).
- `/api/texts/isvarapratyabhijnavivrtti` → fragmentary/partial.
- 404 handling intact.

### Next (candidate Checkpoint 3)
- The `/api/resources` endpoint (federate `RESOURCES_SEED.md` as typed, tradition-tagged, tiered objects) — the natural next surface item on the loose API.
- Then `/api/passages/:id` (parse the working T1s into verse-anchored passages) once resources land.

---

## Checkpoint 1 — ✅ The AI-readable bibliography, served by the API

**Status: VALIDATED.** `npm run build` clean; `/api/texts` and `/api/texts/:id` smoke-tested live (200 on hits, 404 on miss).

### Target
The bibliography (the "WHAT EXISTS?" spine) becomes the single AI-readable source of truth, served by one consistent API record shape for audited and seed alike.

### Delivered
- **One schema, one seed.** Removed the dead duplicate `data/atlas/bibliography.ts`. `bibliographyTypes.ts` is the single schema; `bibliographySeed.ts` (69 records) + `audited.ts` (Trika-10) are the data; `data/atlas/index.ts` exports them.
- **`GET /api/texts`** — serves the full `BibliographyRecord` for every text (10 audited + 69 seed = **79 records**), filterable by `tradition`, `status` (complete|partial|none), and `verified`; defaults to including the seed. Every record carries a stable `urn` (`tantra:text:{id}`), `statusChecked` (evidence-date), provenance-tiered resources, and the "No complete English translation located" phrasing.
- **`GET /api/texts/:id`** — returns one full record by **either** the stable id (`/api/texts/kubjikamata`) **or** the urn (`/api/texts/tantra:text:kubjikamata`). 404 with a `not_found` hint on miss.
- **Seed → record mapping** preserves depth: `sanskrit_etext`/`critical_edition` → `textSources` (tiered); `scholarly_translation`/`online_translation`/`edition_translation` → `translations` (typed, tiered); `manuscript` → `manuscripts`; status derived from `englishComplete`/`englishPartial`.

### Validated
- `/api/texts` → 79 records; `?tradition=Krama&status=none` → 3 (kramavilāsastotra, cidgaganacandrikā, kaulasūtra), each with a clean statusLabel.
- `/api/texts/kubjikamata` → full record (urn, partial status, verified:false, textSources).
- `/api/texts/tantra:text:kubjikamata` → resolves the urn.
- `/api/texts/nope` → 404.
- `npm run build` → clean; `/api/texts` + `/api/texts/[id]` are dynamic routes.

### Next (candidate Checkpoint 2)
- Bring the `seed60.md` richer audit (Siddhānta/Bhairava/Kaula/Krama/Kubjikā/Pratyabhijñā records with coverage, non-English, manuscript IDs) into the structured seed so the API serves full-depth records for all 70, not just the Trika-10.
- Then the next endpoints on the loose surface as needed: `/api/resources`, `/api/passages/:id`.

## Checkpoint 5 — ✅ Our own translation corpus ingested & served by the API/MCP

**Status: VALIDATED.** Passage corpus grew from 570 → **4,016 passages** across 5 works; working translations served via API + MCP; build clean.

### Target
Make the translation pipeline's output (our T1s) visible to the API/MCP — the missing link between the (huge) translation corpus and the (thin) passage layer.

### Delivered
- **`scripts/segment-t1.mjs`** — robust segmenter for our T1 markdown, handling both house layouts (inline-Sanskrit and marker-on-own-line); extracts Sanskrit + close_translation + `[X]`/typed flags + provenance.
- **Passage corpus**: kubjikamata (2437), kulasara (711), kramasadbhava (570 raw), timirodghatana (231), tararahasya (67). Every translated passage now carries its working translation + source edition.
- **`/api/texts/:id/translations`** — our working (T1) translations for a work, verse-anchored, with a provenance note ("NOT peer reviewed; provisional; never copy verbatim").
- **`/api/works`** now reports `working_translations` (T1 coverage count) per work.
- **`search_passages`** now searches Sanskrit + working translation + id.
- **MCP v1.1**: added `get_term_senses` (ledger) + `get_working_translations`; **renamed `find_term_occurrences` → `search_surface_occurrences`** (honest: `match_method:"substring", lemmatized:false`). 8 tools validated via stdio test.

### Validated
- `/api/works` → kubjikamata 2437, kulasara 711, timirodghatana 231 working translations.
- `/api/texts/kubjikamata/translations` → 2437 passages, stage T1.
- timirodghatana → 169/231 passages carry flags.
- search finds translation text (q=kavaca → kubjikamata 10.1 etc.).
- MCP: 8 tools listed; search_surface_occurrences returns substring/lemmatized:false; get_term_senses(kula) → 2 senses; get_working_translations(kubjikamata) → 2437.

### Notes / next
- The corpus now has real density in the Krama/Kubjikā/Kaula space. Next growth per the plan: Devīpañcaśataka, Mahānayaprakāśa, Kramastotra (the Kramasadbhāva neighborhood), then the Kubjikā set (Ṣaṭsāhasra, Śrīmatottara, Kularatnoddyota, Ciñciṇī).
- `data/term_proposals.jsonl` established (proposals, not auto-accepted) — translation emits proposals; only review promotes to `terms.json`.

## Contract restructure — the review-driven split (post-5)

**Applied the peer review of TRANSLATION_SKILL.md.** The single skill doc is now four separated policies + a compiled instruction, so changing the schema can't change translation philosophy:

- `EVIDENCE_POLICY.md` — base text vs textual vs interpretive evidence (corrected hierarchy); the core rule (nothing overrides the passage's grammar); retrieval boundaries (substring ≠ lemma, copyright-safe existing-translation access); term proposals vs accepted (no self-contamination).
- `TRANSLATION_SCHEMA.md` — the revised machine schema (typed flags TXT/GRAM/LEX/DOCT/WIT/SUP; per-dimension `assessment` not scalar confidence; `alignments[]`; `decision_id`s; version lineage; `policy{}` versioning; 7-kind parallels taxonomy; evidence objects separate tier from role).
- `REVIEW_PROTOCOL.md` — T0→T3.1 pipeline; independent-first-pass (Pass A frozen before Pass B); `eligible_for_review` replaces "publishable"; review events; term-proposal promotion (proposed→reviewed→accepted).
- `TRANSLATION_SKILL.md` — rewritten as the thin compiled instruction with the **8 core rules**, referencing the four policies.
- Manifest: `rights` field added to every work (status/license/redistribution/api_fulltext/model_training) — open-to-humanity / commercially-valuable-to-machines distinction reserved for later.
- MCP: `find_term_occurrences` → `search_surface_occurrences` (match_method:"substring", lemmatized:false); added `get_term_senses` (ledger) + `get_working_translations`.
- `data/terms.json` (accepted) vs `data/term_proposals.jsonl` (proposals) established.

Build clean; MCP validated (8 tools).

## Checkpoint 6 — ✅ OCHS manuscript witnesses ingested & resolved to our works

**Status: VALIDATED.** `data/manuscripts.json` (1,542 records) ingested from OCHS's public metadata xlsx; resolved to 18 of our works; served by API + MCP. Build clean.

### Target
Adopt OCHS's manuscript labeling (the value, not their redundant GRETIL texts) as the upstream manuscript-witness layer, resolved into our work authority graph — per `positioningpartners.md`.

### Delivered
- **`scripts/convert-ochs.py`** → `data/manuscripts.json`: 1,542 records, adopting OCHS's own field names (title, titleIndic, alternateTitles, author, language, script, provenance, repository, catalogueIds [NAK/NGMPP], dates, material, condition, folios, incipit/colophon, translations, secondaryLiterature) + `custodian: OCHS`, `licence: CC-BY-NC-SA-4.0`, `source_url`, and a `raw` passthrough of all original fields.
- **`data/corpus/manuscripts.ts`** — the `Manuscript` type + a **curated** OCHS-slug→work resolution map (hand-cleaned to drop false positives like Makutottararahasya≠Tārārahasya). Helpers: getManuscripts, manuscriptsForWork, workForManuscript, workManuscriptCounts.
- **API**: `GET /api/manuscripts` (all, or `?work_id=` / `?q=`), `GET /api/works/:id/manuscripts`, and `/api/works` now reports per-work `manuscripts` counts.
- **MCP**: added `get_manuscripts` tool (9 tools total).

### Validated
- `/api/manuscripts` → 1,542; `/api/works/kubjikamata/manuscripts` → 1; `/api/works` → 18 works now carry manuscript witness counts (netratantra 5, sivasutra 5, mrgendragama 3, spandakarika 3, tantraloka 2, kubjikamata 1 + 2437 working translations, etc.); `?q=netratantra` → 2.
- MCP: 9 tools; `get_manuscripts(netratantra)` → 5.

### Notes / next
- Images are NOT tagged/bulk-downloadable (Reference image empty in export, S3 listing denied) → link out later, don't ingest.
- 24 works have curated witnesses; the map is extendable. The remaining Śaiva/Śākta records (beyond our current 69 works) can be matched later as new works are added.
- The metadata xlsx is CC BY-NC-SA 4.0 — record the licence on every record (done); keep OCHS as custodian (done).

## Checkpoint 7 — ✅ Low-hanging northstar alignment: passage context, term surface, work resolver

**Status: VALIDATED.** New endpoints + MCP tools live; build clean.

### Target
Do the low-hanging fruit that the northstar (`NORTHSTAR.md`) and the review advice point to first: the deterministic evidence bundle, the term-sense/occurrence surface, and a minimal work-identity proposer — without the heavy layers (review graph, manuscript resolver ML, benchmark).

### Delivered
- **`GET /api/context/passages/:id`** (get_passage_context) — the deterministic evidence packet: passage + work metadata + OCHS manuscript witnesses + neighboring passages + tracked term senses + related works + rights. **No generated interpretation.**
- **`GET /api/terms/:lemma/senses`** — accepted senses from the ledger (review-promoted only; proposal count shown).
- **`GET /api/terms/:lemma/occurrences`** — surface occurrences; honest (`match_method:"substring", lemmatized:false`).
- **`POST /api/resolve/work`** — ranked candidate work identities from title/incipit/alternateTitles (matches works + resolved OCHS titles); returns `status:"machine_proposed"` — **proposal only, never an assertion** (northstar: AI proposes ≠ Pāṭala asserts).
- **`data/corpus/terms.ts`** — ledger + proposals loader.
- **MCP**: added `get_passage_context` + `find_term_occurrences` (11 tools total).
- **`DEV_PLAN.md`** reconciled (renamed to Pāṭala + status note pointing to current docs).

### Validated
- `/api/terms/kula/senses` → 2 senses + 1 proposal; `/api/terms/vimarsa/occurrences` → substring/lemmatized:false.
- `/api/context/passages/kramasadbhava:1.9` → passage + work + neighbors (1.8/1.10) + tracked terms + rights; deterministic.
- `POST /api/resolve/work` (title "Kubjikamatatantra") → `machine_proposed`, kubjikamata 0.8, evidence "title match (1.00)"; empty body → 400.
- MCP: 11 tools; `get_passage_context` → work Kramasadbhāva; `find_term_occurrences(kula, kubjikamata)` → 207, substring/lemmatized:false.

### Notes / next
- Remaining northstar milestones: **real MCP client integration + the 25-verse closed-loop translation proof** (the 3-month milestone), then the review/decision graph (scholar identities + review events) — the first real step up the moat stack.

## Checkpoint 8 — ✅ Open-API discoverability + corpus stats (low-hanging fruit)

**Status: VALIDATED.** Build clean; all new endpoints live-tested.

### Target
Low-hanging fruit aligned with the northstar's "open API" + credibility-signal framing: let any agent/consumer discover the surface and see the corpus's data depth at a glance.

### Delivered (17 API routes now)
- **`GET /api`** — the open API index (endpoints grouped + the Pāṭala principles).
- **`GET /api/stats`** — corpus credibility signals: works (69, 11 verified), passages (4,016; 3,446 with working translation), manuscript witnesses (1,542), accepted terms (15), proposals (1), works-with-manuscripts/translations.
- **`GET /api/terms`** — full accepted ledger summary (with per-lemma proposal counts).
- **`GET /api/term-proposals`** — the machine/human proposals (filter by lemma/status; never auto-accepted).

### Validated
- `/api` → name "Pāṭala", 8 endpoint groups.
- `/api/stats` → 69 works / 4,016 passages / 1,542 manuscript witnesses / 15 terms / 1 proposal.
- `/api/terms` → 15; `/api/term-proposals` → kula (proposed).
- `/api/context/passages/kubjikamata:1.1` → shows its OCHS witness `pt:ms:ochs_000_000_039_kubjikamatatantra` + 4 tracked terms.
- `POST /api/resolve/work` (Amṛteśatantram + its incipit) → `machine_proposed`, candidate **netratantra**.

### Notes / next
The API surface now covers the northstar's near-term reads. Remaining milestone: **real MCP client integration + the 25-verse closed-loop translation proof**, then the review/decision graph (the first step up the moat stack).

## Checkpoint 9 — ✅ The six formal primitives (nextdev.md) — identity/assertion/evidence/provenance/review/rights

**Status: VALIDATED.** Build clean; assertions/crosswalks/stats live.

### Target
Per nextdev.md: harden the epistemic core before adding more features — represent contested scholarly claims (dates, traditions, term senses, parallels, manuscript IDs) as first-class, reviewable objects rather than bare fields. The moat starts at the review layer.

### Delivered
- **`data/corpus/primitives.ts`** — the six lean primitives: Assertion (subject/predicate/value + status + certainty + origin + evidence + review_events), Evidence (resource/locator/role), ReviewEvent (who/what/decision/why/when, scoped), Crosswalk (our ↔ external, same_as/witness_of/...), Rights (operational permission matrix, unknown valid), plus the global epistemic-states / certainty / origin vocabularies (per nextdev).
- **`data/primitives.json`** — seeded from real data: kramasadbhava date, kubjikamata tradition (expert_reviewed), kula term-sense; one review event; OCHS crosswalks.
- **`GET /api/assertions`** — contested claims as objects (filter by subject; each shows its review events).
- **`GET /api/crosswalks`** — our-object ↔ external-object mappings (generalizes the OCHS resolution into a first-class federation concept).
- **`Rights`** — expanded to the operational matrix (may_embed/rag/evaluation/commercial_feed added to the existing redistribution/api_fulltext/model_training; unknown is valid) + `DEFAULT_RIGHTS()`.
- **`/api/stats`** — evidence-coverage & review-depth signals: assertions (3), with-evidence (3), reviewed (1), reviews (1), crosswalks (2) — raw facts, not a synthetic "quality score."

### Validated
- `/api/assertions?subject=pt:work:kubjikamata` → 1 assertion (tradition, expert_reviewed, 1 review).
- `/api/crosswalks?our_id=pt:work:netratantra` → witness_of ochs_000_000_002_amrtesatantram (confirmed_match).
- `/api/stats.primitives` → assertions 3 / with-evidence 3 / reviewed 1 / reviews 1 / crosswalks 2.
- The 5 awkward cases (nextdev) all now have a representation path: catalogue-name variants → crosswalks; date disagreement → two assertions; possible quotation → assertion+evidence; rights-unknown → Rights matrix; term reinterpretation → assertion+review.

### Notes / next
- The assertion/evidence/review layer is now in place (seeded small). Next: the closed-loop translation proof + scholar review workspace on top of these primitives.

## Checkpoint 9b — ✅ Raw-corpus concordance exposed (concordance.py is now used)

**Status: VALIDATED.** The existing `sanskritree/scripts/concordance.py` (raw-corpus word tracker, anti-echo: never our translations) is now wired into the Pāṭala API + MCP.

### Delivered
- Added `--json` mode to `concordance.py` (structured output; header moved off stdout).
- **`GET /api/concordance?q=...&texts=...&context=&max=`** — runs concordance.py over the raw ~505-text corpus (Muktabodha + GRETIL), returning `{terms, corpus, texts, total, results:{file:{count, occurrences[]}}}` with per-hit context. Path configurable via `TANTRA_CORPUS_ROOT`.
- **MCP `concordance` tool** (12 tools total).

### Validated
- `/api/concordance?q=khecarī` → 196 texts / 1,141 occurrences (e.g. Śrīvidyārṇavatantra 44).
- `/api/concordance?q=kula akula` → 438 texts / 18,722 occurrences.
- Multi-term, `texts=` filter, `context=` all work; 400 on missing q.
- MCP: `concordance` tool added.

### Notes
- The raw-corpus index (`.concordance_index.json`) is ~132MB — the subprocess reloads it per request. Fine as a local/dev scholarly tool; for deployment, precompute/cache server-side or index at the database layer.
- This is the *surface-level* raw occurrence layer (normalized substring, not lemmatized). The full lemma-index layer (northstar: `find_lemma_occurrences`) remains future, built on this + morphology.

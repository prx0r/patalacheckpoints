# Handover — building out the Tantra Hub (essays.tantrafiles.xyz)

*2026-08-10. For the next agent who continues building the site. This captures: (A) the vision (the endgame-spec 2), (B) where the site is now, (C) the bibliography work in flight, (D) what the new agent must do next, and (E) the context/anchors/registers to read. The site lives at `/root/projects/patala` (Next.js 16, Turbopack, Tailwind v4 CSS-first). **See also `HANDOVER_MCP_API.md` — the machine-facing layer (the retrieval/audit API + the MCP server + the TTS + the formal translation-flow), the highest-priority build.***

---

## A. The vision (read `docs/endgame2.md` in the main repo — it is the spec)

The site is a **Tantra Hub / living bibliography**, not a translation-dump and not a scoring database. The mission: **make the textual landscape of Tantra navigable.** Three layers:

```text
DISCOVER   articles · explainers · lectures
EXPLORE    tradition map · people · concepts · timelines
SOURCE     texts · Sanskrit · translations · manuscripts · bibliography
```

The spine is the **bibliography** — the "WHAT EXISTS?" record per text:

```text
SCHOOL → TEXT → WHAT EXISTS?
```

The bibliography is **LLM-readable AND scholar-friendly**: root-vs-commentary are separate records; translations carry language/coverage/style; text-sources carry type+coverage+editor+year; every resource carries a **provenance tier** (A critical / B text-repo / C scholarly-discovery / D niche-traditional / E discovery-only) — a provenance class, NOT intellectual quality. Every translation-status claim carries its **evidence + status_checked date**, phrased "No complete English translation located" (not "Untranslated").

Two big architectural ideas (from the spec):
- **The translation workshop** — the AI-assisted working translation, honestly labelled "Not peer reviewed," open to verse-level scholar corrections → a versioned community text. (Bilara-for-Tantra embedded in a bibliography.)
- **The machine-facing layer** — stable IDs (`tantra:text:kubjikamata:3.14`), an API/MCP (`get_passage / find_parallel_passages / audit_translation / get_text_status`), and the **provenance hierarchy** so agents treat site-generated material as provisional, not critical scholarship.
- The model case is **FoJin** (corpus-aggregation → cited-AI-answers) vs ours (living-scholarly-hub → bibliography → reader → workshop → commentary → media → AI-retrieval). Ours is the "what exists / where can I read it / what's translated / how do scholars understand it" center of gravity.

---

## B. Where the site is now

- **The atlas graph** (`app/page.tsx`): the original one-page ReactFlow graph — traditions/texts/people/concepts as draggable retro-windows with typed+confidence-weighted edges (the reference-map's "not a family tree" rule). Data in `data/atlas/{traditions,texts,people,concepts,relations}.ts`, consumed via `data/atlas/index.ts`.
- **The `/bibliography` page** (`app/bibliography/page.tsx`): a list page, currently rendering the OLD seed schema (see C — it is being migrated).
- **SITE_STATUS.md** — the site's growth-rules + the sync-gap discipline (every translation milestone carries a "site-update" line; T3s/dossiers must reach `data/atlas/`).
- **Deployment:** NOT deployed. `npm run build` is the check. (Cloudflare token invalid; local `npm run dev`.)
- **Current visual skin:** the CSS palette is in `app/globals.css` (the Śaiva manuscript-tech: `--void`, `--bone` [ivory], `--ash`, `--saffron`, `--vermilion`). Note: `globals.css` is NOT imported in the layout, and Tailwind v4 uses CSS-first config (no `tailwind.config.js`) — so Tailwind utility colors like `text-ivory` do NOT exist; use `text-[color:var(--bone)]` / `text-[color:var(--saffron)]` or add an `@theme` block.

## C. The bibliography work IN FLIGHT (finish this first)

A full audit of the seed found the coarse "translated = yes/no" was wrong. The new standard (the gold record):

```ts
// data/atlas/bibliographyTypes.ts — the new shared types
BibliographyRecord {
  id, work, traditions[], period?, verified,           // verified=false = seed
  textSources[] { type: critical_edition|edition|etext|scan, coverage, editor, year, provider, tier },
  translations[] { language, translator, work, coverage, complete, type: scholarly|traditional|independent|working, year, url, tier, note },
  translationStatus: complete|partial|none, statusLabel, statusChecked, statusEvidence?,
  scholarship[], related[], manuscripts[], notes[]
}
```

**Done:** `data/atlas/audited.ts` — the **audited Trika-10** (Mālinīvijayottara, Vijñānabhairava, Parātriṃśikā root, Parātriṃśikāvivaraṇa, Tantrāloka, Tantrasāra, Mālinīślokavārttika, Tantrasadbhāva, Śivasūtra+Vimarśinī, Spandakārikā+Spandanirṇaya, Parātriṃśikā Laghuvṛtti), at full depth (coverage-ranges, root-vs-commentary, style, tiers, evidence).

**Done:** `data/atlas/bibliographySeed.ts` — the original 70-text seed preserved as `seed: SeedRecord[]` (the OLD looser schema, `verified:false`).

**DONE — the migration is complete (the build passes):** `data/atlas/index.ts` exports `audited` + `seed` + the new types; `app/bibliography/page.tsx` renders the audited Trika-10 (the scholar dropdowns: translations / Sanskrit-sources / scholarship, with tier-badges, the status-evidence, the notes) plus a clearly-marked "Seed — not yet audited" section for the 70-text `seed`. `npm run build` is clean; `/bibliography` is a static route.

## D. The next steps (in priority order)

1. **Finish the bibliography migration** (C above) — the audited Trika-10 at full depth, the seed as a separate verified:false section, the page with the scholar dropdowns.
2. **Audit the next schools** (per the spec: "then the passes are Krama 10 → Kubjikā 10 → Kaula 10 → Bhairava 10 → Pratyabhijñā 10 → Siddhānta 10, rather than dumping all 70 before they're verified"). Move each audited school into `audited.ts` at full depth. Do NOT treat the current 70 as publication-ready.
3. **Wire the site's own corpus** into the bibliography as `type: "working"` translations (our T1s/R1s: KMT full, Kulasāra, Tārārahasya, Timirodghāṭana, Kramasadbhāva paṭala 1, Ciñciṇī [acquired], etc.) — the "Working translation / not peer reviewed" badge.
4. **The text-reader layer** — the Bilara-style segment view (Sanskrit | working translation | commentary) with the concordance-evidence panels. The translated corpus (`translations/01_t1_working/*.md`) is the source.
5. **The per-entity routes** — `/traditions/[slug]`, `/texts/[slug]`, `/concepts/[slug]`, `/people/[slug]` (the `app/[type]/[slug]/` folders are scaffolded but empty).
6. **The stable-ID + API/MCP layer** — `tantra:text:id`, `get_text_status`, `audit_translation` (the audit-types from the spec: NEGATION / TERM DRIFT / UNSUPPORTED ADDITION / PARALLEL CONFLICT / COMMENTARY CONFLICT / GRAMMATICAL UNCERTAINTY / SOURCE UNCERTAINTY).

## E. Context, anchors, and registers (read before building)

From the main repo (`/root/projects/sanskritree`):
- **`CONTEXT_AND_ANCHORS.md`** — the ordered reading-list: the pipeline docs, the dossiers, the anchor-stack, the working-set.
- **`docs/endgame2.md`** — the spec (the vision). Also `docs/endgame1.md` + `corpus/learning/ENDGAME_SITE_SPEC.md`.
- **`corpus/targets/canonical_reference_map.md`** — the school-taxonomy + the lemma-trajectories (kula, krama, śakti, khecarī...) — the atlas's source of truth.
- **`corpus/targets/targetacquired.md`** + **`sources/round3/MANIFEST.md`** — the acquisitions (Ciñciṇī, Kramasadbhāva, Śambhunirṇaya, Bang-TaSa; the Muktabodha-only [ACQ] set).
- **`translations/_meta/R1_CONTENT_ENGINEERING.md`** — the R1-findings (the audit-types in practice) — the model for the `audit_translation()` API.
- **The registers** (`untranslated.md`, `untranslated2.md`, `targetacquired.md`) — the "what exists / what's translated" data for the bibliography.
- **`STATUS.md`** (translations) — the pipeline state, the R1-batch, the Kramasadbhāva T1.

The site's own spec + status: **`patala/SITE_STATUS.md`** (the growth-rules), **`data/atlas/*.ts`**, **`lib/atlas.ts`** (the entity/relation types).

---

## The site-update discipline (from SITE_STATUS)
- Data is king; components are dumb. Edit `data/atlas/*` to grow the site.
- Relations are NOT `parent:` fields — every edge is typed + confidence + evidence.
- Every translation-status assertion carries its evidence + `status_checked`.
- Every research milestone should touch `data/atlas/` (the "site-update" line) or it's a signal the sync was forgotten.
- Deployment check: `npm run build`. Never hard-code research into components.

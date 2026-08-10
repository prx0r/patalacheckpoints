# Pāṭala — Agent Reference & Navigation Map

*Compiled 2026-08-10 after a full read-through of the repo. Use this to navigate fast and to know what's actually next. The governing principle everywhere: **API/MCP first, UI last** — "no endpoint, no feature." Nothing is "done" until the API serves it. Do NOT overengineer: the API/MCP is a loose surface that grows as we build useful things, not a rigid pre-spec.*

---

## 0. One-paragraph orientation

Pāṭala (was `essays-tantrafiles`, at `/root/projects/patala`) is the **Tantra Hub** — a scholarly *authority/provenance/expert-validation* layer between manuscript repositories and AI. It is NOT a translation dump, an OCR engine, or a scan archive (those layers have incumbents: Gyan Bharatam, Muktabodha, OCHS, GRETIL). The moat = the **verified graph**: identity, provenance, expert disagreement, human-validation signals, relationships. Core invariant: **"AI proposes ≠ Pāṭala asserts"** — only human review creates accepted knowledge. The source corpus lives in `/root/projects/sanskritree` (= `/mnt/HC_Volume_106427611/sanskritree`, same path via symlink).

---

## 1. Fast file map

### Strategic / endgame docs (read these to know WHY)
| File | What it is |
|---|---|
| `docs/NORTHSTAR.md` | **The master strategy** (1735 lines): positioning, market, moat stack, economics, 24-month roadmap, outreach emails |
| `docs/nextdev.md` | **The 6 formal primitives** (Identity, Assertion, Evidence, Provenance, Review, Rights) — the epistemic core everything hangs off |
| `docs/endgame1.md` | The critical-translation-laboratory vision (the original product framing) |
| `docs/endgame2.md` | The Tantra-Hub spec (bibliography spine, reader, workshop, machine layer, provenance hierarchy) |
| `docs/endgame3.md` | One infrastructure, several interfaces (consumer / scholar / machine / institution) |
| `docs/endgame4.md` | The economic thesis (84000 model, evaluation suite, scholar network, open-to-humanity) |
| `docs/endgame5year.md` | 2026–2031 strategic window (funding landscape: IKS, BHU, NEH, Endangered Archives) |
| `docs/foundationalideas.md` | The 7+ foundational data-model decisions (stable IDs, provenance, TEI-witnesses, alignment) |
| `docs/apideas.md` | The research-API proposal (the full endpoint vision; what the API is heading toward) |
| `docs/positioningpartners.md` | Competitive landscape + partner strategy (Muktabodha/OCHS/Kaula Studies etc.) |
| `docs/RESOURCES_SEED.md` | The 35+ external resources (Muktabodha, GRETIL, Mahānaya, ShivaShakti...) to federate |

### Translation system docs (read these to translate)
| File | What it is |
|---|---|
| `docs/TRANSLATION_SKILL.md` | **The compiled instruction injected into the translator** (thin orchestrator; points to the 4 policies) |
| `docs/STYLE_GUIDE.md` | House voice: retention list, capitalisation, compounds, no-anachronism |
| `docs/EVIDENCE_POLICY.md` | How to reason with evidence; grammar-over-parallel; no self-contamination of term ledger |
| `docs/TRANSLATION_SCHEMA.md` | The machine data shape (typed flags, assessment, alignments, decision ids, versioning) |
| `docs/REVIEW_PROTOCOL.md` | The pipeline T0→T3.1, independent-first-pass rule, review events, term promotion |
| `docs/TRANSLATION_SKILL_SPEC.md` | The buildable slice: the `translate` command + the minimal MCP + 3 small data files |
| `docs/TRANSLATION_PROTOCOL.md` | The fuller data-model vision (translation-memory, parallels, dossiers, 8 entities) |
| `docs/PROOF_T1_kramasadbhava.md` | The working proof: Kramasadbhāva 1.8–1.12 in the house schema via the MCP |

### Status / process docs (read these to know WHERE)
| File | What it is |
|---|---|
| `docs/CHECKPOINTS.md` | **Validated milestones 1→9b** (what actually works) — the source of truth for progress |
| `docs/PROCESS_NOTES.md` | How we work + the honest known-gaps + next steps |
| `docs/DEV_PLAN.md` | The (older) build plan — superseded by CHECKPOINTS/PROCESS_NOTES/NORTHSTAR |
| `docs/CORPUS_MANIFEST.md` | The corpus architecture (work→edition→passage→token) |
| `SITE_STATUS.md` | Site growth-rules + the sync-gap discipline |
| `HANDOVER_SITE.md` | The site-builder handover |
| `HANDOVER_MCP_API.md` | The machine-facing handover (API/MCP) — highest-priority layer |

### Code
| Path | What it is |
|---|---|
| `app/api/**` | 17 route handlers (the API surface). Index: `app/api/route.ts` |
| `app/bibliography/page.tsx` | The bibliography UI (renders `audited` + `seed`) |
| `app/page.tsx` | The atlas graph (ReactFlow); `components/atlas/*` |
| `app/{traditions,texts,concepts,people}/[slug]/` | **Scaffolded but EMPTY** (per-entity pages — not built) |
| `data/atlas/` | `bibliographyTypes.ts` (schema), `audited.ts` (Trika-10, verified), `bibliographySeed.ts` (58 seed, verified:false), `{traditions,texts,people,concepts,relations}.ts` (the graph) |
| `data/corpus/` | `works.ts` (registry), `passages.ts` (loader), `terms.ts` (ledger+proposals), `manuscripts.ts` (OCHS resolution), `relations.ts`, `primitives.ts` (the 6 primitives) |
| `data/corpus/passages/*.jsonl` | 4,016 segmented verses (5 works: kubjikamata 2437, kulasara 711, kramasadbhava 570, timirodghatana 231, tararahasya 67) |
| `data/manuscripts.json` | 1,542 OCHS manuscript records |
| `data/terms.json` | 15 accepted term senses (kula, krama, śakti...) |
| `data/term_proposals.jsonl` | 1 proposal (kula) — never auto-accepted |
| `data/primitives.json` | Seeded assertions/reviews/crosswalks |
| `mcp/index.mjs` | The MCP server (12 tools), read-only, proxies the API + reads corpus files |
| `scripts/` | `segment-t1.mjs`, `segment-kramasadbhava.mjs`, `convert-ochs.py` |

### The source corpus (the input)
`/root/projects/sanskritree/`: `translations/01_t1_working` (141 files) · `02_r1_review` (36) · `03_t2_alternate` · `04_r2_adjudication` · `05_t3_final` · `06_c1_interpretation` · `saivamap/dossiers/` (24 lemmas) · `sources/` (Muktabodha ~500, GRETIL, round3 acquisitions) · `scripts/concordance.py` (raw-corpus tracker, ~132MB index, anti-echo). Translation status: `translations/STATUS.md`.

---

## 2. What's actually built (validated, per CHECKPOINTS)

1. AI-readable bibliography served by `/api/texts` + `/api/texts/:id` (69 records, URNs, tiers, statusChecked)
2. Full-depth bibliography for all schools (69 = 11 audited Trika + 58 seed, verified:false)
3. Corpus manifest: `/api/works`, `/api/relations/:work_id`, `/api/passages/:id`, `/api/search/passages`
4. Translation contract + MCP v1 + proof chapter (Kramasadbhāva 1.8–1.12)
5. Our T1 corpus ingested (4,016 passages) + `/api/texts/:id/translations` (working T1s)
6. OCHS manuscript witnesses (1,542 records, resolved to 18 works) + `/api/manuscripts`, `/api/works/:id/manuscripts`
7. Northstar alignment: `/api/context/passages/:id` (evidence bundle), `/api/terms/:lemma/senses` + `/occurrences`, `POST /api/resolve/work` (machine_proposed)
8. Discoverability: `/api` index, `/api/stats`, `/api/terms`, `/api/term-proposals`
9. The 6 formal primitives: `/api/assertions`, `/api/crosswalks`, `/api/stats.primitives`; `Rights` matrix
9b. Raw-corpus concordance: `/api/concordance` + MCP `concordance` tool

**MCP tools (12):** `get_work` · `get_source_passage` · `search_passages` · `get_related_works` · `get_term_senses` · `search_surface_occurrences` (honest: substring/lemmatized:false) · `get_working_translations` · `get_manuscripts` · `get_existing_translations` · `get_passage_context` · `find_term_occurrences` · `concordance`.

---

## 3. The current gaps / honest caveats (from PROCESS_NOTES + my read)

- **The MCP has never been wired into a real client session** to run a full translation end-to-end. The tools work (stdio-tested); the contract exists; but no model has yet translated a passage *through the loop with the skill injected*. **This is THE missing milestone.**
- Passage corpus = 5 works only. Many translated T2/T3s + untranslated sources (Devīpañcaśataka, Kramastotra, Mahānayaprakāśa) not yet segmented.
- 58 seed records `verified:false` (full-depth shape but not gold-audited).
- Per-entity routes (`/traditions/[slug]`, `/texts/[slug]`, `/concepts/[slug]`, `/people/[slug]`) are empty scaffolds.
- `data/atlas/concepts.ts`/`people.ts`/`texts.ts` may not include the newest T3'd texts' dossiers (sync-gap per SITE_STATUS §4).
- `globals.css` is NOT imported in `layout.tsx`; Tailwind v4 has no `@theme` block → utility colors like `text-ivory` don't exist (use `text-[color:var(--bone)]`).
- NOT deployed (invalid Cloudflare token); local `npm run dev`/`build` only.
- `data/occurrences.json` (the coarse precomputed per-lemma index from `TRANSLATION_SKILL_SPEC.md`) — I did NOT find this file; it's a listed v1 deliverable that may be missing.

---

## 4. What's next — in the RIGHT order (priority)

### THE milestone: the closed-loop translation proof (real MCP client)
Wire a real agent (Hermes/opencode/Claude/ChatGPT) to the Pāṭala MCP and translate a passage with the skill injected — the thing that proves the whole stack. Per NORTHSTAR, name it **"closed-loop evidence-bearing translation and review,"** not "connect MCP."
- Run `translate` on one clean chapter (candidates: Timirodghāṭana, or a Kulasāra paṭala — both genuinely-untranslated, in the working corpus).
- Confirm output has: stable passage IDs, `terms:` ledger, `reading:` (T3.1) beside the close draft, typed `[X]` flags, provenance header, `review_status: eligible_for_review`.
- Confirm a human can run R1→T2→R2→T3→T3.1→C1 on top without reformatting.
- Then record it as a Checkpoint. **This is the single most valuable next action.**

### Then (in order)
1. **Segment more of the corpus** — Devīpañcaśataka, Kramastotra, Mahānayaprakāśa (untranslated sources) and/or the T2/T3s. Grows the passage corpus the MCP serves.
2. **`/api/occurrences`** (term co-occurrence in context) — cheap over the 4k-passage corpus.
3. **The 25-verse closed-loop proof at scale** (the NORTHSTAR 3-month milestone) — 25 contiguous Kramasadbhāva verses.
4. **Build `data/occurrences.json`** if missing (the coarse per-lemma index).
5. **The review/decision graph** — scholar identities + review events (the first step up the moat stack; the primitives exist, need the workflow on top).
6. **Resources endpoint** (`/api/resources` from `RESOURCES_SEED.md`) — typed, tradition-tagged, tiered objects.

### Deferred (don't build yet — avoid overengineering)
- Full-text/vector concordance (concordance.py grep-based is fine now).
- Automatic parallel detection (capture manually during translation, validate later).
- `audit_translation` as a real endpoint (v1 = the model following the audit checklist).
- TEI export, scholar-review UI, versioning DB, TTS endpoint, manuscript ML resolver, benchmark.

---

## 5. Quick wins (low-effort, high-value, safe)

1. **Wire a real MCP client and run ONE chapter through the loop.** Highest value / highest leverage. Everything else is secondary until this proves the stack.
2. **Create `data/occurrences.json`** (grep the corpus once → per-lemma coarse `{work, range}`) — it's a listed v1 deliverable that appears missing, and it unblocks `find_lemma_occurrences` honesty.
3. **Sync the newest T3'd texts + 24 dossiers into `data/atlas/`** — the SITE_STATUS sync-gap (Jñānakārikā, Ajaḍapramātṛsiddhi, Kaularahasya, Kulapradīpa, Kubjikātantra, Śivasūtra, + the dossier lemmas already partially in `relations.ts`). Data-is-king; components are dumb.
4. **Segment Devīpañcaśataka / Kramastotra / Mahānayaprakāśa** into the passage corpus (they're the Kramasadbhāva neighborhood — the anchor set the translation loop needs).
5. **Fix the site housekeeping:** import `globals.css` in `layout.tsx` (or add a Tailwind `@theme` block) so utility colors work; fill the empty `[slug]` route scaffolds with minimal renderers reading `data/atlas/`.
6. **Add `/api/resources`** from `RESOURCES_SEED.md` — it's the natural next surface item, typed/tagged/tiered, small.

---

## 6. Fresh-eyes observations (things possibly being missed)

- **The closed loop is the linchpin and it's not yet run.** All the infrastructure (MCP, schema, proof-chapter, 4k passages) is built but the actual *agent-in-the-loop* test is the one thing that validates it. It's explicitly the #1 next step in both HANDOVERs and PROCESS_NOTES — don't get distracted by adding endpoints/features until it's done.
- **The `data/occurrences.json` deliverable may be missing** (spec'd in `TRANSLATION_SKILL_SPEC.md` §3, never validated in CHECKPOINTS). Easy to add, unblocks honest lemma context.
- **Concordance performance**: `concordance.py` reloads a ~132MB index per request (noted in CHECKPOINT 9b). Fine locally; will need server-side caching before any deployment. Flag for later, not now.
- **Right-alignment risk**: the bibliographic `texts`/`works` and the atlas `texts.ts`/`relations.ts` are separate structures. `works.ts` derives from the bibliography; the atlas graph is separate. Keep them consistent when adding a text (the sync-discipline in SITE_STATUS is the guardrail).
- **Deployment blocker is only a token.** The code builds clean; a Cloudflare Pages token with `Pages: Edit` (or a git-connected project, as `tantrafiles-hub` does) is all that stands between this and live. Low effort to unblock when wanted.
- **Don't build the big layers** (parallel detection, audit engine, TTS, benchmark, manuscript ML) yet — the NORTHSTAR/NORTHSTAR-style guidance and PROCESS_NOTES both explicitly defer them. The MCP + closed loop + corpus density are the real path.

---

## 7. Build/verify commands

```bash
cd /root/projects/patala
npm run dev       # local dev (localhost:3000)
npm run build     # THE verification — must stay clean
node mcp/index.mjs  # MCP stdio server (needs the site running for API proxy)
```

Env for MCP: `TANTRA_API_BASE` (default `http://localhost:3000`), `TANTRA_CORPUS` (default `/mnt/HC_Volume_106427611/sanskritree/translations`), `TANTRA_CORPUS_ROOT` (concordance, default `/mnt/HC_Volume_106427611/sanskritree`).

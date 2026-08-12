# Pāṭala — Implementation vs Vision: Gaps & Opportunities

*2026-08-12. A point-by-point comparison of the live Pāṭala implementation against the vision docs
(`NORTHSTAR.md`, `ENDGAME_SITE_SPEC.md`, `nextdev2.md`, `PATALAML.md` + `REVIEW_PATALAML_VS_CODEBASE.md`).
For each gap: what exists, what the vision wants, and the concrete highest-value build.*

---

## 0. Where the implementation is today (ground truth)

- **Next.js 16 app (TypeScript)**, static corpus in `data/corpus/` (TS modules, no runtime parsing),
  29-route API, MCP server (`mcp/index.mjs`), pipeline.
- **Core model** (`data/corpus/translation.ts`): `PublishedTranslation` with source_spans /
  target_spans / alignments / decisions / evidence / review_state / **c1**.
- **Primitives** (`data/corpus/primitives.ts`): Identity / Assertion / Evidence / Provenance /
  Review / Rights — plus `assertions.ts`, `trajectories.ts`.
- **The reader is the product** (`app/read/[work]/[locator]/page.tsx`): phrase-clickable,
  hover-align Sanskrit/English, decision side-panel, READ/AUDIT toggle, **C1 Commentary toggle**
  (renders `pub.c1.verse_commentary`).
- **IPVV integrated** (largely uncommitted): 1.5.11 published unit (hand-authored, C1-rich), 38
  generated units (V2-A…V3-P), overview page, work/text/concept registration, `lib/citation.ts` +
  `/api/resolve` + `resolve_ref` MCP tool, `/api/spines` + `get_school_spine` MCP tool.
- **13 MCP tools**: get_work, get_source_passage, resolve_ref, search_passages, get_related_works,
  get_school_spine, get_term_senses, search_surface_occurrences, get_working_translations,
  get_passage_context, find_term_occurrences, get_term_history, concordance, get_manuscripts,
  get_existing_translations.

---

## 1. C1 is the missing link in the IPVV surface

**What exists:** the reader has a Commentary toggle wired to `pub.c1`; the 1.5.11 unit demonstrates it.

**The gap:** the **38 generated IPVV units (V2-A…V3-P) are token-level T1 hyperliteral glosses with
NO `c1` field and NO decisions.** The Commentary toggle is empty for them. Meanwhile the IPVV stack
already has **63 finished C1 read/ renderings** + **10 structured `c1/source/` records** sitting in
`/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv/c1/`.

**The build:** the reader's Commentary toggle is the exact slot where the 63 C1 read/ renderings
drop in. This is nextdev2 §B ("C1 content engine"). Do NOT regenerate C1 via Hermes (STATE_OF_PLAY:
the C1s are editorial, produced with the main model + anchored context — that work is already done).

---

## 2. The `c1/source/` structured records are incomplete (53 of 63)

**What exists:** `c1/source/` has only **10 of 63** structured records (SUMMARY / FUNCTION / KEY
TERMS / LOCAL CONTEXT / EXPLANATION / BOUNDARY / RELATED).

**Why it matters:** the structured record is what the API/MCP and the THEMES embedding should use.
Completing the 53 (mechanical derivation from the read/ bodies: SUMMARY ≈ body, KEY TERMS from
Terms:, BOUNDARY from the body, RELATED from See also) improves both the THEMES input and the machine
surface.

**The build:** generate the 53 remaining `c1/source/` records.

---

## 3. THEMES is entirely unexposed

**What exists in the stack:** THEMES is **piloted, not built** over the full 63 C1s. The spec
(`specs/SPEC_THEME_CLUSTERING.md`) + dossier spec (`specs/SPEC_THEME.md`) + the proven pilot
(`specs/THEMES_PILOT_REPORT.md`) all exist in the IPVV stack.

**The gap in Pāṭala:** no `/api/themes`, no MCP tool, no theme node in the data model at all.
The ML roadmap's flagship experiment (§4 graph representation learning, §5 relation motifs) and
PATALAML #2 (multi-resolution retrieval) both assume themes exist.

**The build:** build THEMES over the 63 C1s (community detection over the hybrid graph →
ThemeProposal → human-adjudicated ACCEPTED THEMES), then expose as `/api/themes` + an MCP tool, and
link each passage → its theme(s) in the published object. This is the single highest-value next
action in the whole project.

---

## 4. The deterministic verification floor is specced but not served

**What exists:** `contradicts` role is first-class (`primitives.ts`, `trajectories.ts`,
`translation.ts`); `derived_from`/`version_of`/`witness_of` crosswalk relationships model provenance;
`/api/resolve` resolves any node back to source. The whole stack IS a derivation DAG.

**What the vision wants** (REVIEW_PATALAML_VS_CODEBASE #6/#8/#10 + PLATFORM_PROVENANCE_PRESERVING_GENERATION
§12): first-class validation APIs — `/find-counterevidence`, `/verify-claim`, `/trace-dependency`,
`/minimal-evidence`, `/verify-quote`, `/verify-relation`.

**The build:** these are **thin services over existing data** — the highest-leverage, cheapest
wins. They implement "AI proposes ≠ Pāṭala asserts" as machine-access.

---

## 5. Multi-resolution / query-adaptive retrieval is structure-without-service

**What exists:** the layered stack IS the natural resolution ladder
(token/span → passage → C1 → theme → work → cross-work → tradition), and `canonical-spines.ts` gives
cross-work structure. `search_passages` is substring-only (`match_method: substring`, `lemmatized:
false` — honestly labeled).

**What the vision wants** (PATALAML #2, #3): query-adaptive retrieval; late-interaction (ColBERT) for
Sanskrit/technical terms.

**The build:** expose the resolution ladder as a real query-adaptive service; later add real
embeddings (late-interaction for Sanskrit is greenfield). The substring search is a deliberate
honest stub, not the moat.

---

## 6. Graph/hypergraph representation learning (the genuinely-new ML)

**What exists:** the hybrid relation-graph spec (7 edge types) + ThemeProposal spec; TranslationDecision
is already an n-ary object (source_span_ids + target_span_ids + alternatives + evidence + review).

**What's new** (REVIEW #4/#5, PATALAML §1/§4/§5): learning C1 representations from text + Sanskrit
terms + sequence + explicit links + argument roles; relation-motif discovery; GNN/hypergraph
embeddings. The flagship experiment is the **hybrid C1 graph vs embeddings-only theme discovery**.

**The build:** this comes AFTER THEMES is built and exposed (need the accepted-theme data to learn
over). It's the research-grade payoff, not the immediate build.

---

## 7. Other smaller gaps

- **Per-school learning pages** (`/traditions/*`) — nextdev2 §A — exist in skeleton (the `/learning`
  and `/traditions/[slug]` layers were committed) but the IPVV/Pratyabhijñā school content could be
  deepened from the 22-essay recognition library.
- **Dossiers → `/concepts/{lemma}`** — `data/atlas/concepts.ts` holds 20 concept dossiers; the IPVV
  stack's `concept-deepdives/` (whattheheckismemory, etc.) could feed more.
- **The Tantrāloka workbook** → `/learning/tantraloka-workbook` pathway (nextdev2 §C) is unbuilt.
- **The Pāṭala benchmark** (PATALAML #20) — `gold.ts` + the QA toolchain is an embryonic seed; needs
  formalization. Long-term, not now.
- **Semantic layers** — entailment lattice (#9), vertical-fidelity classifier (#11): new, after the
  service layer + vector layer exist.

---

## 8. The priority ordering (given what exists)

| Priority | Build | Why | Cost | Status |
|---|---|---|---|---|
| **1** | **THEMES over 63 C1s + expose `/api/themes` + MCP tool** | the flagship; everything downstream consumes it; piloted & proven | Medium (algorithm + data) | **DONE (2026-08-12)** — deterministic themes exposed |
| **2** | **Wire the 63 C1 read/ renderings into the reader's Commentary toggle** | instant visible value; content already exists | Low | **DONE (2026-08-12)** — `verse_commentary[]`, V1 multi-C1 |
| **3** | **Complete the 53 `c1/source/` structured records** | better THEMES input + machine surface | Low (mechanical) | **DONE (2026-08-12)** — 63 total |
| **4** | **Serve the deterministic floor** (`/find-counterevidence`, `/verify-claim`, `/trace-dependency`, `/minimal-evidence`) | thin, high-value, over existing data | Low | **DONE (2026-08-12)** — `/api/verify/*` + MCP |
| **5** | **PARALLELS** (cross-text witnesses per theme) | the comparative layer; feeds essays | Medium | pending |
| **6** | **Vector layer** (late-interaction for Sanskrit) | unblocks semantic retrieval + graph embeddings | High (infra) | pending (ML) |
| **7** | **Graph/hypergraph representation learning** | the research-grade payoff | High (ML) | pending (ML) |
| **8** | Per-school pages · dossiers · workbook · benchmark | content + eval surface | Varies | benchmark seed documented |

---

## The meta-insight (why this is the right position)

**Most of Pāṭala-ML is not greenfield.** The existing `data/corpus/` model (assertions, evidence
roles incl. `contradicts`, crosswalk provenance, translation decisions as n-ary objects, term
trajectories, gold fixtures, the resolve kernel, the canonical spines, the theme-clustering spec)
already implements the ontology behind ≥10 of the 20 PATALAML ideas. The real work is twofold:

1. **Expose** existing primitives as services (`/find-counterevidence`, `/verify-claim`,
   `/trace-dependency`, `/minimal-evidence`) — thin, high-value.
2. **Learn over** existing structure (late-interaction retrieval, graph/hypergraph embeddings,
   entailment, vertical fidelity) — the genuinely new ML.

The layered supervision (source · decision · commentary · theme · claim · essay · pedagogy) is the
ML gold, and the IPVV stack already holds most of it as structured data. The immediate highest-value
build is **THEMES + C1 wiring** — making the IPVV's already-complete commentary layer visible and
machine-queryable in Pāṭala.

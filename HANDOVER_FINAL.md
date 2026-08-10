# Pāṭala — Handover + Intuitive Notes + Top Tips

*2026-08-10. The single entry point for the next agent. This is the **final consolidated
handover**. Read it top to bottom — it tells you what Pāṭala is, where it genuinely stands,
what to build next, and the intuitive shortcuts that will save you hours.*

**Repo:** https://github.com/prx0r/patala (branch `main`, commit `2665d0c`). Local `/root/projects/patala`.

---

## 1. What Pāṭala is (one mental model)

**Pāṭala is provenance + adjudication infrastructure for tantric textual knowledge.**

NOT a translation factory, NOT an archive, NOT an OCR/lemmatisation/RAG project.

The one sentence that captures it:

> Every interpretive decision in a published translation is inspectable — click a phrase,
> see the decision, the alternatives, the evidence, the review, the version history.

**The core loop:**
```
PUBLISHED TRANSLATION
  → TARGET SPAN
  → ALIGNMENT (source ↔ target)
  → TRANSLATION DECISION
  → EVIDENCE
  → REVIEW EVENTS
  → VERSION LINEAGE
```

**The six primitives** (Identity / Assertion / Evidence / Provenance / Review / Rights) are
the substrate. Everything is a view over them.

**The invariant:** *machines propose, humans review.* "AI proposes ≠ Pāṭala asserts."

---

## 2. Where it genuinely stands (honest)

### Built, tested, proven (105/105 tests)
- **The publishable auditable translation object** — `source span → decision → target span`
  with first-class evidence, review, version lineage. Proven on Kramasadbhāva 1.8.
- **The auditable reader** — `/read/kramasadbhava/1.8`: hover-aligns Sanskrit/English,
  phrase-click decision panel, READ/AUDIT toggle, prev/next.
- **The 25-verse unit** — `compile_published.py` turns T1 results into 25 `PublishedTranslation`
  objects (16 with working T1, 2 OPEN cruxes), honest OPEN/evidence_missing defaults.
- **The text overview** — `/texts/kramasadbhava` (unit summary + per-passage read links).
- **The C1-target queue** — `GET /api/texts/kramasadbhava/decisions?open=true`.
- **The API** — 19+ routes, 13 MCP tools. **The six primitives + scholarly graph + lint.**
- **The pipeline** — T1→T3 via Hermes (Milestone A1 proven); C1 is editorial (your main model).

### De-emphasized (do NOT reopen)
- **Model-interface / translation-generation rabbit holes.** Hermes owns plumbing. C1s are
  written by the editorial model with anchored context, NOT machine-generated.
- Broad 58-record bibliography sweep (just-in-time only). Giant graph migration. RAG/embeddings.
- The `essays.tantrafiles.xyz` name — it's Pāṭala now (the layout title is updated; a few
  doc files still say the old domain, harmless).

---

## 3. The strategic docs (read these for direction)

| Doc | What it is |
|---|---|
| `docs/nextdev2.md` | **the forward plan** (reader-is-the-product, school pages, C1 engine, scaling) |
| `docs/LEARNING_STRATEGY.md` | **research-once/distill-repeatedly** content architecture |
| `PROCESS_NOTES.md` | the strategy + reset |
| `STATE_OF_PLAY.md` | the honest state |
| `HANDOVER_NEXT.md` | previous handover |
| `docs/SCHOLARLY_GRAPH.md` | the canonical data model |
| `docs/endgame2.md` + `endgame3.md` | the hub + learning vision |
| `docs/PEER_REVIEW_REDTEAM.md` | the 7 invariants |

---

## 4. The intuitive "how it works" map

### The product object lives in `data/corpus/`
```
translation.ts    the schema: SourceSpan, TargetSpan, Alignment, TranslationDecision,
                  EvidenceItem/Use, PublishedTranslation, deriveReviewState
published.ts      the registry (serves the reader + decisions endpoints)
units/kramasadbhava-1.8-published.ts     the hand-authored reference (richest)
units/kramasadbhava-1-25-generated.ts   the compiled unit (generated, don't edit by hand)
```

### The reader is one component
`app/read/[work]/[locator]/page.tsx` — a single self-contained client component. It fetches
`/api/passages/:id/translation` and renders:
- Sanskrit from `source_spans`, English from `target_spans`
- hover-alignment via `Alignment`
- click a decision phrase → `DecisionPanel` (fetches `/api/decisions/:id`)

**It's data-agnostic** — any published passage renders without redesign. To add passages,
add `PublishedTranslation` objects to `published.ts`.

### To generate a published object from a translation
`pipeline/compile_published.py` — deterministic, no model calls. Reads the passage corpus +
gold_records T1s, emits conservative Level-1 objects (spans, alignment, OPEN/evidence_missing
where unknown). **It never invents evidence.**

### The compiler → registry flow
```
sanskritree (passages.jsonl + gold_records)
   → compile_published.py
   → data/corpus/units/*-generated.ts
   → published.ts (registry)
   → /api/passages/:id/translation + /api/decisions/:id
   → the reader
```

---

## 5. Top tips (the hard-won shortcuts)

1. **The reader is the product; don't rebuild it.** If a passage 404s, the fix is adding a
   `PublishedTranslation` to `published.ts`, not touching the component.
2. **Never edit `*-generated.ts` by hand** — re-run `compile_published.py`. Hand-authored
   files (like `1.8-published.ts`) are the exceptions; keep them richer than generated ones.
3. **The registry preserves hand-authored 1.8** — the compiler's generated 1.8 is filtered
   out so it doesn't clobber the richer manual one. Don't break that.
4. **"OPEN + evidence_missing" is a valid, honest state**, not a failure. Don't make the
   compiler block because every phrase lacks research.
5. **C1s are editorial, not machine.** Write them with your main model + anchored context
   per `skills/write-commentary`. The decisions queue (`?open=true`, `?evidence_gap=true`)
   tells you WHICH passages deserve a C1 first — don't guess.
6. **`status` ≠ `evidence_state` ≠ `editorial_status`.** A decision can be OPEN + partially
   grounded + proposed. Keep the three dimensions separate; that's the whole point.
7. **Hover-alignment is the killer UX.** It works because `Alignment` links source↔target
   span ids. Don't lose that when adding features.
8. **Test everything through the API suite** (`npm test`). 105 checks. If the suite 404s,
   it's usually a registry conflict (a generated file overwriting a hand-authored one) or a
   stale dev server — restart it.

---

## 6. The roadmap (what to build next)

1. **Write 5 C1s** for the strongest passages (use the decisions queue to pick them),
   per `LEARNING_STRATEGY.md` + `skills/write-commentary`. Each C1 → reader Commentary block
   + feeds the concept pages.
2. **Turn the Tantrāloka workbook** (`sanskritree/corpus/learning/REFERENCE_TANTRALOKA_WORKBOOK.txt`)
   into 20–30 questions in prerequisite order; write 5 master notes + explainers.
3. **Per-school pages** (`/traditions/krama`, then trika/kubjika/kaula) from `saivamap/` +
   dossiers + C1s → reader. Do this AFTER the reader has real depth.
4. **The semantic flywheel** (later): once ~20 grounded sense assignments exist, make
   term-history an output of audited work, not hand-authored.

**Deferred forever-ish:** consumer app, marketplace, payments, courses platform, retreats,
RAG, custom OCR, all-69 bibliography sweep.

---

## 7. How to run

```bash
cd /root/projects/patala
npm run dev          # the site + API (localhost:3000)
npm test             # 105-check suite (needs the API up)
npm run build        # the verification

# regenerate the 25 published objects:
python3 pipeline/compile_published.py

# validations:
python3 pipeline/validate.py --report
python3 pipeline/validate_graph.py
python3 pipeline/check_gold.py
python3 pipeline/validate_trajectories.py
```

Hermes key: `OPENCODE_GO_API_KEY` in `~/.hermes/.env`. Hermes config: `~/.hermes/config.yaml`
(`tantrakosa` MCP → `http://localhost:3000`).

---

## 8. Files the next agent must read first

| File | Why |
|---|---|
| `docs/nextdev2.md` | the plan |
| `docs/LEARNING_STRATEGY.md` | the content architecture |
| `data/corpus/translation.ts` | the product schema |
| `data/corpus/published.ts` | the registry |
| `app/read/[work]/[locator]/page.tsx` | the reader (the product surface) |
| `pipeline/compile_published.py` | how published objects are made |
| `skills/write-commentary/SKILL.md` | how to write a C1 |
| `sanskritree/saivamap/` | the per-school content tree |
| `sanskritree/corpus/learning/REFERENCE_TANTRALOKA_WORKBOOK.txt` | the Learn-Trika seed |

---

## 9. The one-line truth

> We're not trying to get T1–T3 working — that works. We're turning T1–T3's hidden
> reasoning into a **publishable evidence graph attached phrase-by-phrase to the
> translation**, and now using it to generate real scholarship (C1s) and learning content.
> The site shell is done. **Fill the machine with scholarship now.**

# Pāṭala — Handover for the Next Agent

*2026-08-10. The single entry point. Read `STATE_OF_PLAY.md` + `PROCESS_NOTES.md` for the
strategy and `docs/SCHOLARLY_GRAPH.md` for the data model. This handover tells you where
Pāṭala actually is — against NORTHSTAR's roadmap and the canonical reference map — and
exactly what matters next.*

---

## 1. What Pāṭala is (one line)

**Provenance + adjudication infrastructure for tantric textual knowledge** — the
authority/evidence/review layer *between* manuscript repositories (Muktabodha, OCHS,
GRETIL) and the people/AI that use them. NOT a translation factory, NOT an archive, NOT
an OCR/lemmatisation/RAG project (those commoditize).

Core loop:
```
SOURCE → PASSAGE → ASSERTIONS → EVIDENCE → REVIEW → ACCEPTED/DISPUTED → COMMENTARY → GRAPH
```
built on the **six primitives** (Identity, Assertion, Evidence, Provenance, Review,
Rights) and the **scholarly graph** (Work/Witness/Passage/SourceSpan/Person/Term/Sense/
Resource + annotations).

**Core invariant:** *machines propose, humans review.* "AI proposes ≠ Pāṭala asserts."

**Repo:** https://github.com/prx0r/patala (branch `main`). Local `/root/projects/patala`.

---

## 2. Where we are vs NORTHSTAR's roadmap (Aug–Oct 2026)

| NORTHSTAR item (Aug–Oct 2026) | Status |
|---|---|
| Freeze evidence and rights schemas | ✅ done (`primitives.ts`, `graph.ts`, `contracts.py`) |
| Real MCP client integration | ✅ 13 MCP tools; connects to Hermes |
| `get_passage_context` | ✅ done |
| 25-passage closed-loop translation test | 🟡 Milestone A1 proven (1 verse); 25-verse not done |
| Term proposal/review governance | ✅ terms.json vs term_proposals.jsonl; review events scoped |

**Not started** (Nov 2026+): TEI adapter, scholar workspace, review queues, manuscript
authority schema (resolve_work exists), institutional ingest, benchmark seed.

---

## 3. Where we are vs the reference map's ingestion order

The reference map's concentric order:
```
Trika/Spanda/Pratyabhijñā anchors → Krama/Kālīkula → Kubjikā root → bridge works → large Yāmala → Sarvāmnāya
```

**Corpus segmented (7 works):** kubjikamata (2437), kulasara (711), kramasadbhava (563),
cidgaganacandrika (312), timirodghatana (231), maharthamanjari (74), tararahasya (67).
**1/68 works translation-ready (derived):** kramasadbhava.

The **five levels of authority** (Source → Passage → Translation → Sense → Synthesis)
are the model — and Pāṭala is building the "Sense" and "Synthesis" layers (term
trajectories, dossiers) which the reference map calls the differentiated value.

---

## 4. What's genuinely built (validated)

### The pipeline (`pipeline/`)
- **Durable state machine** (`state_machine.py`): load/transition/run/audit/persist/
  reload; prerequisite-gated; versioned stages; stage-local audits; invalid-stage RETRY.
- **Stage contracts** (`contracts.py`): empty/`{}` strict output is INVALID (fixed the
  silent-empty bug the 1.8 run exposed).
- **Scholarly graph** (`graph.ts` + `docs/SCHOLARLY_GRAPH.md`): the canonical object/
  annotation model + a validation lint (`validate_graph.py`).
- **Six primitives** (`primitives.ts`): Assertion/Evidence/Review/Crosswalk/Rights.
- `model.py` shells out to **`hermes -z`** (Hermes owns provider reliability/retries).

### Proven (Milestone A1)
Kramasadbhāva 1.8 ran source→T1→R1→T2→R2→T3 with **real interpretive disagreement**
found and adjudicated: `devadeveśi` = "mistress of the god of gods" (devadeva-īśī), and
the `nirānande` crux surfaced (later shown to need PREFERRED/OPEN, not CONSTRAINED —
the whole reason C1/evidence matters).

### The API/MCP
19 API routes, 13 MCP tools, **84/84 test suite**, OpenAPI spec, docs-site nav.

---

## 5. The critical decision (do NOT reopen)

We spent a lot of time on **model-interface / translation-generation optimization**
(JSON mode, response_format, retries, C1-via-Hermes). Verdict: **stop.** 

- Translation generation is NOT the valuable artifact. The user can produce translations
  fine with their main model + anchored context.
- Hermes owns the plumbing (retry, backoff, provider switching).
- The value is the **structure**: identity, evidence, review, provenance, the graph.

> **No more model-interface rabbit holes unless Hermes can't run batches at all.**

---

## 6. The roadmap (the 3 milestones)

1. **Milestone A** — one complete scholarly object. **A1 proven** (machine adjudication
   loop). C1 + evidence dossier + audit still pending — **do this with the user's main
   model, not Hermes**, as a structured object.
2. **Milestone B** — a contiguous **25-verse research unit** (kramasadbhāva 1.1–25):
   passage objects + section-level lexical network + cross-passage parallels, not 25
   isolated translations.
3. **Milestone C** — one real Krama/Śaiva scholar conversation on the strongest passages.

---

## 7. What's next (priority)

1. **Milestone B** — a 25-verse research unit (this is the most productive next thing).
2. **Enrich the scholarly graph** — start encoding the segmented corpus as graph objects
   (works/witnesses/passages/annotations) so the API serves the graph.
3. **Term-sense → assertion wiring** — the `nirānanda` case shows a real need: sense
   assignments as first-class annotations with evidence (the trajectory engine already
   points this way).
4. **One scholar conversation** (Milestone C) once there's a small corpus of strong C1s.

---

## 8. Files to read first

| File | What it is |
|---|---|
| `STATE_OF_PLAY.md` | the honest reset + current direction |
| `PROCESS_NOTES.md` | the strategy + where we are |
| `HANDOVER.md` (root) | the previous consolidated handover |
| `docs/SCHOLARLY_GRAPH.md` | the canonical data model (the durable foundation) |
| `docs/NORTHSTAR.md` | the master strategy + roadmap |
| `docs/PEER_REVIEW_REDTEAM.md` | the 7 invariants |
| `experiments/milestone-a-kramasadbhava-1.8.md` | the 1.8 result + the nirānanda lesson |
| `../sanskritree/corpus/targets/canonical_reference_map.md` | the historical map + ingestion order |

## 9. How to run

```bash
cd /root/projects/patala
npm run dev        # the API (localhost:3000)
npm test           # 84-check suite
python3 pipeline/validate.py --report
python3 pipeline/validate_trajectories.py
python3 pipeline/validate_graph.py
```

## 10. Honest caveats

- **Only 1 work translation-ready** (kramasadbhava); the corpus is 7 segmented works.
- **58 bibliography records are seed/verified:false** — readiness is derived, not asserted.
- **Milestone A1 stopped at T3** (T3.1 + C1 pending); done via Hermes, slow backend.
- `data/manuscripts.json` (5.5MB) + `kubjikamata.jsonl` (1.5MB) are gitignored.
- The docs live in two repos (`patala/docs/` + `sanskritree/corpus/targets/`); keep in sync.

---

## Update — the publishable auditable translation object (built)

The core product is now built and proven on Kramasadbhāva 1.8:

- **`data/corpus/translation.ts`** — the canonical schema: SourceSpan / TargetSpan /
  Alignment (many-to-many, with method) / **TranslationDecision** / **EvidenceItem**
  (first-class) / EvidenceUse. Three dimensions on every decision:
  `status` (CONSTRAINED/PREFERRED/OPEN) ≠ `evidence_state` (grounded/partially_grounded/...) ≠
  `editorial_status` (proposed/reviewed/accepted — derived from ReviewEvents, never manual).
  `surface_rendering` vs `adjudicated_reading` (OPEN keeps a surface text without falsely
  resolving the crux).
- **`units/kramasadbhava-1.8-published.ts`** — the real instance: 9 source spans, 9 target
  spans, 9 alignments, 3 decisions (devadeveśi PREFERRED/grounded, nirānande OPEN/
  partially_grounded + technical alternative, paramānande CONSTRAINED), 6 resolvable
  EvidenceItems. `review_state` is DERIVED.
- **APIs**: `GET /api/passages/:id/translation` (phrase-clickable: spans + alignments +
  decisions + evidence) and `GET /api/decisions/:id` (full audit trail, evidence resolved
  to items, unresolved flagged). **101/101 tests.**
- **Evidence is first-class and validated**: every decision→evidence edge resolves
  (fixed the dangling nirānanda technical link); `validate_graph.py` + `check_gold.py`
  (gold-fixture regression — nirānanda must stay OPEN, not falsely settled).

This is the product: click a phrase → see the decision, its evidence cards, review state,
and version lineage.

## The clear next build (scale, don't redesign)
Generate `PublishedTranslation` candidates for the 25-verse unit (Hermes emits spans +
alignments + decision proposals; the pattern is proven on 1.8). Fail loudly where
evidence/decision generation is incomplete. Then the phrase-click reader (a tiny drawer,
not a full UI) once a handful exist.

# 06 — THE COMMENTARIAL GRAPH (secondary scholarship → living interpretation)

*Part of `docs/process/README.md`. This is the **secondary-scholarship layer**: turning thousands of
papers (Ratié, Torella, Dyczkowski, Sanderson...) into a **computable commentary layer** over the
primary-source graph — not a pile of PDFs and not just embeddings for RAG.*

**The core transformation:**
```text
PAPER → SCHOLAR CONTRIBUTION PACKET → graph objects → Ask/Read/Learn/Essay/Video
```

**The central distinction (never blur these):**
```text
PRIMARY SOURCE SAYS X          ≠   RATIÉ INTERPRETS SOURCE AS X   ≠   PĀṬALA CURRENTLY ACCEPTS X
```

Raw research: `source-evidence/docs/tools/docs-cache/commentarialgraph-research.md`.
References: ORKG · SocraticKG · SciClaim · full-text argument mining · OpenAlex/ORCID/CRediT.

---

## 1. What it IS

Secondary papers become a **live history of interpretation**:
```text
                      PRIMARY PASSAGE
                            │
          ┌──────────────────┼──────────────────┐
          ↓                  ↓                  ↓
     Scholar A           Scholar B          Scholar C
   interprets X        interprets Y        qualifies X
          │                  │                  │
          └──────────────────┼──────────────────┘
                             ↓
                        Debate / Crux
                             ↓
                     Pāṭala adjudication
```
An answer can say: *"The primary text establishes A. Ratié reads this as B. Torella emphasizes C.
They diverge on D."* — every clause resolving downward to the exact scholarly object.

## 2. The object ontology (Pāṭala-native, deeper than ORKG)

**`ScholarlyWork`** — the paper (identity via OpenAlex/DOI/ORCID; external identity/enrichment, never
replacing our canonical objects).

**`ScholarPosition`** — one scholar's scoped claim:
```yaml
ScholarPosition:
  id, scholar_id, work_id
  proposition, type: INTERPRETATION
  about: [CONCEPT-x, PASSAGE-x, ARGUMENT-x]
  modality: asserted | probable | tentative | rejected
  source_span: {page, paragraph}
  evidence_used: [PASSAGE-x, WORK-x]
  confidence: {extraction: .94}
  review_state: MACHINE_EXTRACTED
```

**`Question` + `ScholarAnswer`** — every contribution generates canonical questions; answers cluster
under one question (Q-119 → Scholar A/B/C answers → Pāṭala synthesis).

**`ScholarContributionPacket`** — the full set of object types from one paper:
Question · Claim · Interpretation · Definition · Distinction · Argument · EvidenceUse · Objection ·
Reply · Agreement · Disagreement · Qualification · Comparison · CitationUse · ResearchGap · Quote ·
PedagogicalSeed · MediaSeed.

**`AttributionEvent`** — first-class scholar credit (DIRECT_QUOTE / PARAPHRASED_POSITION /
EVIDENCE_SOURCE / INTERPRETIVE_DEPENDENCY / CONTRASTED_POSITION / PEDAGOGICAL_SOURCE) → drives the
scholar-impact page + economics.

**`Quote` / `Paraphrase`** — the exact-vs-paraphrased separation. `[QUOTE:Q881]` tokens expand only in
an authorized renderer; everything else is `Paraphrase` with `fidelity_status`.

**`RightsState`** — per-paper copyright/quote/derivative policy. `INTERNAL EXTRACTION ≠ PUBLIC
REPUBLICATION`.

## 3. Citation roles (philosophical, not just "CITES")

```text
CITES_AS_SUPPORT · CITES_AS_OPPONENT · CITES_AS_PRECEDENT · CITES_FOR_TRANSLATION ·
CITES_FOR_TEXTUAL_READING · CITES_FOR_DEFINITION · CITES_AS_PARALLEL ·
CITES_AS_COUNTEREXAMPLE · CITES_FOR_HISTORICAL_CONTEXT
```

## 4. The ingestion pipeline (paper → packet)

Raw research: `source-evidence/docs/tools/docs-cache/commentarialgraph-research.md` +
`externalpaper-research.md` (the verified compiler + verifier ensemble + ecosystem repos).

```text
PDF
 → 0 RIGHTS + IDENTITY (DOI/OpenAlex/author/ORCID/license)
 → 1 STRUCTURE (headings/pages/paragraphs/footnotes/bibliography)
 → 2 SCHOLARLY INTERROGATION (section → canonical QA candidates)
 → 3 ATOMIC EXTRACTION (claims/interpretations/evidence/definitions/objections/distinctions/citations)
 → 4 ARGUMENT RECONSTRUCTION (premise/conclusion/support/attack/qualify)
 → 5 PRIMARY-SOURCE ALIGNMENT (resolve Sanskrit refs → Pāṭala IDs)
 → 6 SCHOLAR ALIGNMENT (resolve citations → Work + Scholar IDs)
 → 7 CANONICALIZATION (merge equivalent questions/concepts/positions)
 → 8 ADVERSARIAL PASS (check overstatement/polarity/attribution/source support/alternative)
 → 9 SCHOLAR CONTRIBUTION PACKET
 → 10 GRAPH PROPOSAL (MACHINE_PROPOSED)
 → 11 SURFACES (Ask/Read/Learn/Scholar/Media)
```

**The document substrate** (reuse, don't rebuild): **Docling** (layout/content) + **GROBID** (scholarly
metadata/citations) → structured work → **SpanLedger** (page/block/sentence/note). S2ORC-doc2json is
the schema reference (RawDocument/StructuredDocument/BibliographyEntry/CitationMention/BodySpan/
Section). Marker/Nougat are fallbacks.

**The safer route (SocraticKG pattern):** QA as an intermediate representation BEFORE triple extraction —
use **Pāṭala scholarly-interrogator questions**, not generic 5W1H:
```text
What question is answered? What position is advanced? What primary passage is interpreted?
What does this reading depend on? What alternative is rejected? What evidence is given?
Who is being followed/corrected? Where is the author uncertain? What downstream proposition follows?
```

**Verifier ensemble** (evidence checks, not just extraction):
```text
RefChecker → atomic claim decomposition + fidelity
CIBER      → deliberate refutation retrieval (not similarity self-confirm)
GraphCheck → graph-vs-graph relational drift (long-form)
CLAIMCHECK → claim-targeted critique (scholar-review objections)
RARR       → revise unsupported generated output
```
**Extraction programs:** DSPy typed modules (QuestionExtractor, PositionExtractor, EvidenceLinker,
ArgumentExtractor) with measurable outputs → optimized against Pāṭala gold review data.

**The hyperedge representation** (geometricengine pattern): a scholarly contribution is a
**hyperedge + typed incidences** (Scholar X · Work W · SourceSpan S · Question Q · Claim C · Passage P ·
Concept K · Scholar Y), not flattened pairwise edges. Paper → SectionEpisode → DiscourseMove
(POSE_QUESTION/STATE_POSITION/INTRODUCE_EVIDENCE/INTERPRET_PASSAGE/QUALIFY/RAISE_OBJECTION/
ANSWER_OBJECTION/SYNTHESIZE) → transitions recover argumentative flow.

## 5. "Research once; render repeatedly" (essay = a graph projection)

Don't save `essay.md` as canonical. Save a **`Synthesis`**:
```yaml
Synthesis:
  question_id, thesis, proposition_ids[], evidence_use_ids[],
  scholar_position_ids[], objection_ids[], crux_ids[], uncertainty, review_state
```
Then `essay.md` is ONE renderer → beginner essay / scholarly essay / video / interactive argument / AI
answer — **no intellectual drift between formats**.

The essay layer already derives from `ArgumentSynthesis` (see `docs/process` + agent1atlas). The
commentarial graph supplies **knowledge, argument patterns, distinctions, citations and intellectual
structure** — NOT prose imitation. Pāṭala writes its own house style.

## 6. The compounding loop

```text
1,000 papers → 20,000 Questions, 80,000 Positions, 40,000 EvidenceUses
  → consumer app → 500,000 user questions
  → map to canonical Questions
     → answer exists → render
     → answer missing → search paper corpus → recover latent answer → new graph objects
```
Unanswered user demand tells us what to ingest more deeply; scholars review → canonicalize → essays/
videos/learning → more users → more questions.

## 7. Scholar economics / attribution

- **Contribution impact** (a new scholarly metric): Works/Positions/Passages linked, answers/lessons/
  essays/videos informed — NOT "paper has 421 citations."
- **`AttributionEvent`** is the accounting atom; `credit ≠ permission` (copyright separate).
- `AttributionEvent` → the scholar-economics vision (commissioned review, adjudication, licensed
  commentary, course contribution) with agreed revenue-sharing where licensed.

---

## 8. How it links to the rest of Pāṭala

```
PRIMARY GRAPH (01-ingestion / 02-atlas / 03-factory)
   ↓  (evidence-use, propositions, arguments)
COMMENTARIAL GRAPH (this layer) — ScholarPositions over primary passages
   ↓  (Question → ScholarAnswer → Synthesis)
ESSAY / EDUCATION / REVIEW / MEDIA (projections)
   ↓
SCHOLAR CREDIT + ECONOMICS (AttributionEvent)
```

This layer is where the existing Pāṭala source graph becomes a **living intellectual tradition** rather
than "an unusually good digital edition."

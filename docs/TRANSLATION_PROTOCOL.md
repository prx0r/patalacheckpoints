# The Translation Protocol — structured scholarly data generation

*The translation is the prima materia. Not one blob — a versioned set of passage-level claims linked to Sanskrit evidence. From it derive the concordance, term history, commentary, audits, TTS, MCP, and scholar review.*

> **Never store "a translation" as one blob. Store a translation as a versioned set of passage-level claims linked to Sanskrit evidence.**

The translation unit:

```text
WORK
  ↓
SOURCE EDITION / WITNESS
  ↓
PASSAGE
  ↓
TOKEN / LEMMA / PARSE
  ↓
TRANSLATION SEGMENT
  ↓
ANNOTATIONS / TERM DECISIONS / PARALLELS
  ↓
REVIEW EVENTS
  ↓
PUBLISHED VERSION
```

That gives maximal reuse.

## 1. The canonical translation object

```json
{
  "passage_id": "pt:kubjikamata:3.14",

  "source": {
    "edition_id": "kubjikamata-goudriaan-schoterman-1988",
    "source_text": "...",
    "source_range": "3.14"
  },

  "translation": {
    "text": "...",
    "status": "working",
    "version": 3,
    "translator_type": "ai_assisted",
    "review_state": "unreviewed"
  },

  "alignment": [],

  "terms": [],

  "grammar_notes": [],

  "parallels": [],

  "commentary": [],

  "review_events": []
}
```

## 2. Three translation layers

For each passage:

### A. Close translation
As structurally faithful as reasonable. For scholarship, audits, comparisons, AI agents, grammar.

### B. Reading translation
Natural English, still defensible. The default site reader.

### C. Commentary/paraphrase
Explains what is happening without pretending to be translation.

```text
Sanskrit

Close
"The goddess, abiding in the wheel..."

Reading
"The Goddess dwells within the circle..."

Commentary
Here 'wheel' probably refers to...
```

## 3. Formalise lexical decisions while translating

Populate lemmas and terminology during translation, not afterward. Capture the important ones automatically + manually:

```json
{
  "surface": "vimarśaḥ",
  "lemma": "vimarśa",
  "morphology": { "case": "nominative", "number": "singular", "gender": "masculine" },
  "translation_here": "reflexive awareness",
  "sense_id": "vimarsa.pratyabhijna.02",
  "certainty": "medium"
}
```

This powers click-word dictionary, concordance, diachronic search, consistency audit, MCP retrieval, glossary.

## 4. Distinguish lemma from sense

Not `vimarśa = reflexive awareness`. Instead:

```text
LEMMA: vimarśa

SENSE A  general consideration/reflection
SENSE B  Pratyabhijñā technical reflexive awareness
SENSE C  specific ritual/contextual usage
```

with evidence passages. A glossary then becomes evidence-derived, not written once by an LLM.

## 5. Every translation decision can carry evidence

For difficult phrases:

```json
{
  "claim": "kula is rendered as 'totality' here",
  "evidence": [
    { "type": "same_text", "passage": "..." },
    { "type": "commentary", "passage": "..." },
    { "type": "scholarship", "citation": "..." }
  ],
  "confidence": "medium"
}
```

Use it for: technical terms, ambiguous compounds, syntactically uncertain passages, contested interpretations, unusual additions in English.

## 6. Peer review is part of the data model

```text
REVIEW EVENT 014
passage: Kubjikāmata 3.14
reviewer: Scholar X
finding: "kula should probably not be translated 'family' here"
type: terminology
suggested: "totality"
evidence: Tantrasadbhāva 4.7; Tantrāloka 29.23
status: accepted
```

Badges derived from history: WORKING (AI-assisted) → HUMAN REVIEWED (1 reviewer) → SCHOLAR REVIEWED (2 domain specialists) → EDITORIALLY STABLE.

## 7. Version everything

```text
v1  AI draft
v2  grammar correction
v3  terminology harmonised
v4  reviewer correction
v5  published
```

```http
GET /passages/.../translation            # current stable
GET /passages/.../translation?version=3  # any version
```

## 8. Translation style guide

Not "translate beautifully but accurately." Explicit policy:

- **Sanskrit retention** — keep untranslated where technically important (śakti, kula, krama, spanda, vimarśa), only where English would obscure the technical sense.
- **Compounds** — prefer readable English; record the parse separately.
- **Supplied English** — anything materially supplied for readability should be auditable.
- **Ambiguity** — `translation = preferred reading`, `note = alternative`. Do not merge both into fuzzy English.
- **Technical consistency** — same sense normally receives the same English rendering unless local context warrants deviation.
- **Capitalisation** — explicit policy for Śiva/śiva, Goddess/goddess, Consciousness/consciousness, Power/power.
- **Metaphysical interpretation** — don't insert later-school doctrine into earlier texts unless commentary/evidence supports it.

## 9. Formal translation pipeline

```text
0. SOURCE CONTROL      choose edition/witness
1. SEGMENTATION        stable passage IDs
2. SANSKRIT ANALYSIS   tokenisation, lemmatisation, sandhi, morphology, compound candidates
3. CLOSE DRAFT         minimal interpretation
4. CONTEXT RETRIEVAL   same-text, same-school, same-period usage, parallels, commentaries, existing translations
5. TERMINOLOGY PASS    resolve technical terms
6. READING TRANSLATION produce clean English
7. AUDIT               negation, numbers, omission, addition, term drift, grammar, parallel conflict
8. HUMAN EDIT          your review
9. SCHOLAR REVIEW      optional / targeted
10. RELEASE            version + provenance
```

This becomes both the human workflow and the instructions for MCP agents.

## 10. The MCP returns evidence, not "translate for me"

Avoid one magical `translate_passage()`. Give the model research primitives:

```text
get_source_passage
analyse_sanskrit
find_lemma_occurrences
find_same_author_usage
find_same_tradition_usage
find_period_usage
find_parallel_passages
get_commentaries
get_existing_translations
get_term_policy
audit_translation
```

Then the translation prompt orchestrates them. This reduces the risk of the MCP becoming an opaque translation vending machine.

## 11. Anchor corpora need explicit metadata

```json
{
  "traditions": [ { "id": "krama", "confidence": "high" } ],
  "date": { "not_before": 900, "not_after": 1000, "preferred": 950, "certainty": "medium" },
  "region": ["Kashmir"],
  "genres": ["tantra", "ritual", "doctrine"]
}
```

Dates/traditions carry scholarly evidence. Retrieval ranks:

```text
same text > same author > direct textual relatives > same tradition > neighboring tradition
> same period > general tantric Sanskrit > wider Sanskrit corpus
```

## 12. Explicit "translation memory"

```text
Sanskrit segment | English segment | lemmas | sense IDs | tradition | date | translator | quality status
```

When a similar construction appears: "This construction appears 12 times in reviewed material." CAT software for historical Sanskrit, informed by philology.

## 13. Populate parallels as you translate

Save genuinely useful parallels as `candidate_parallel`, then validate. Two products for one effort: **translations + textual relationship graph**. Also save lemma occurrences, sense evidence, bibliography links, commentary references, uncertain parses.

## 14. Do not manually annotate everything

Three tiers:

- **Automatically generated** — tokens, candidate lemmas, morphology, lexical hits, embeddings, candidate parallels
- **Human-confirmed** — selected lemma analysis, accepted parallel, preferred term sense, translation alignment
- **Scholar-validated** — difficult readings, contested interpretation, manuscript decision, high-value terminology

## 15. Translation dossier per chapter

```text
KUBJIKĀMATA — CHAPTER 3
TRANSLATION →
SOURCE         edition used, manuscripts represented
TERMINOLOGY    41 tracked technical lemmas
PARALLELS      27 validated
UNCERTAINTIES  8 unresolved readings
SCHOLARSHIP    14 sources
REVIEW         AI audit ✓, editorial pass ✓, scholar review pending
DOWNLOAD       reader, Markdown, JSON, TEI
```

## 16. Structured derivative assets, automatically

One translation populates: TEXT READER · GLOSSARY · TERM HISTORY · CONCORDANCE · SEARCH · TTS · API · MCP translation memory · COMMENTARY · BIBLIOGRAPHY · ATLAS textual relations · STATISTICS (coverage).

## What to implement immediately

Eight entities:

```text
Work  Passage  SourceWitness  Translation  Alignment  LemmaOccurrence  Annotation  ReviewEvent
```

Then soon after:

```text
TermSense  ParallelRelation  BibliographicResource
```

Create one canonical translation schema + style guide. Take **one manageable, genuinely untranslated text with good Sanskrit** and run an entire chapter through the new workflow — producing clean Sanskrit, stable IDs, close translation, reading translation, lemma data, term senses, parallels, commentary notes, audits, versions, review record, API output. If that chapter works, the factory is built; after that every translation makes the whole site smarter.

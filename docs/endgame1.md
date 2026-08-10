# The Endgame

The end product is not an automatic Sanskrit-to-English translator. It is a **machine-assisted critical translation laboratory** capable of taking an unedited or untranslated Tantric work from manuscript witnesses to a publishable, auditable translation.

For every translated sentence, the system should answer:

1. What Sanskrit reading was translated?
2. Which manuscripts or editions support it?
3. How was it segmented?
4. Which morphology and compound structure were selected?
5. What syntactic and semantic roles were assigned?
6. Which dictionary senses, commentaries and parallels support the interpretation?
7. Which plausible alternatives were rejected?
8. Which English words correspond to which source claims?
9. What remains uncertain?
10. Who approved the final decision?

The real goal: **Reduce expert translation from reconstructing everything manually to adjudicating explicit, ranked and traceable alternatives.**

---

## Why previous approaches are insufficient

### 1. End-to-end machine translation
Fails for untranslated Tantra — no domain-matched parallel data. Even fluent output can conceal wrong segmentation, reversed agent/patient, collapsed compounds, invented subjects, commentary imported into root text, etc.

### 2. Sequential Sanskrit NLP pipelines
Error propagation — a wrong sandhi split prevents correct lemma → syntax → translation. Sanskrit graph-based research shows joint inference is necessary.

### 3. Lexicon-driven analysis alone
Heritage is excellent for candidate generation but fails on rare technical vocabulary, lineage-specific usages, unusual compounds.

### 4. Neural Sanskrit analyzers alone
ByT5-Sanskrit is robust but suffers distribution shift on technical Śaiva/Śākta Tantra.

### 5. Flat compound classification
Tantric Sanskrit has nested multi-member compounds where [[A B] C] ≠ [A [B C]].

### 6. Verse-isolated translation
Tantric texts contain ellipsis, cross-verse pronoun resolution, ritual sequences, deliberate polysemy.

### 7. Single-edition input
The source text itself may be uncertain. Textual criticism must be upstream of translation.

---

## The complete development plan (12 stages)

### Stage 0 — Define the scholarly product
Each translated passage produces a **Translation Proof Bundle** with source witnesses, critical reading, variants, segmentations, morphology, compound trees, syntax, semantic frames, lexical senses, commentary evidence, parallels, translations, alignments, formal checks, human decisions, uncertainties.

Three translation layers: Literal construal, Philological translation, Interpretive translation.

### Stage 1 — Gold adjudication system
Web interface for expert annotation with structured reason codes. Initial gold corpus: 9 Bhairavastava + 20 Spandakārikā + 10 held-out Vijñānabhairava.

### Stage 2 — Source and critical-edition layer
Ingest every available witness. TEI-compatible concepts: WITNESS, READING, APPARATUS, LEMMA, CORRECTION, CONJECTURE, DAMAGED_SPAN.

### Stage 3 — High-recall linguistic candidate ensemble
Heritage + Vidyut + ByT5-Sanskrit. Target: >98% segmentation recall, >95% morphology recall.

### Stage 4 — Joint structural analysis
Explicit structured scoring over variables: reading, segmentation, morphology, compound tree, dependency, coreference, frame, sense.

### Stage 5 — Tantric lexical-semantic memory
Lazy senses from real passages with scoped hypotheses per tradition/school/author. Retrieval hierarchy: commentary → same work → same author → same lineage → related Tantra → grammar → general.

### Stage 6 — Commentary and intertext graph
Commentaries as claims, not retrieval blobs. Evidence levels: explicit root → explicit commentary → inferred parallel → traditional interpretation → modern reconstruction.

### Stage 7 — Semantic representation before English
Language-neutral semantic plan with predicate, agent, object, manner, location. Every field points to source evidence.

### Stage 8 — Constrained translation generation
Pass A: realization plan (JSON). Pass B: English rendering (literal/philological/interpretive). Pass C: deterministic audit. Pass D: adversarial critic.

### Stage 9 — Formal and deterministic verification
Lean verifies structural consequences: segment coverage, exclusivity, licensed bindings, negation scope, ritual sequence, commentary labeling.

### Stage 10 — Active learning
Prioritize passages by uncertainty, engine disagreement, novel vocabulary, expected recurrence.

### Stage 11 — Learned ranking
After 1,000-3,000 real judgments: logistic → gradient boosting → pairwise ranker → path-based → GNN → HGT → sheaf.

### Stage 12 — Full untranslated-text pilot
Choose a short, untranslated Trika work. Measure: 2× reduction in translation time, >95% source-span alignment, <1% unsupported additions.

---

## Ultimate vision

A user opens an untranslated verse and sees:

```
Critical reading confidence: 0.78
Three meaningful textual variants

Preferred segmentation:
  supported by Heritage, ByT5 and two same-author parallels

Preferred compound tree:
  0.64 probability
  one defensible alternative at 0.29

Technical sense:
  attested in commentary passages X and Y
  general dictionary sense rejected

Translation:
  "..."

Literal construal:
  "..."

Supplied words:
  [the practitioner]

Unresolved:
  whether genitive attaches to A or B

Reviewer status:
  morphology approved
  semantics disputed
  translation provisional
```

> **Not fabricated certainty, but dramatically accelerated, evidence-visible philology.**

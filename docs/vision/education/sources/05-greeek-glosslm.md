Yes—**GlossLM is worth testing**, but it is not “needed” as a permanent dependency. Its value is that it gives Pāṭala an external multilingual glossing baseline and validates a bigger architectural idea: **T1 can be a language-agnostic intermediate layer** rather than a Sanskrit-only hack.

That matters a lot for expansion.

Right now Pāṭala is:

```text
Sanskrit source
→ T1 transliteral/interlinear gloss
→ L0 structured representation
→ argument map
→ L2 readable translation
→ L200 audit
→ C1 commentary
```

The parts that are genuinely Sanskrit-specific are mostly the **front-end compiler**:

```text
segmentation
morphology
lemma analysis
sandhi
technical lexicon
source conventions
```

Everything after a normalized T1/L0 representation is much more portable:

```text
T1/L0
→ proposition extraction
→ argument mapping
→ translation fidelity
→ audit
→ evidence
→ peer review
→ correction propagation
→ term tracking
```

So the long-term architecture should become:

```text
                UNIVERSAL PĀṬALA CORE
                         │
       ┌─────────────────┼─────────────────┐
       │                 │                 │
 SanskritCompiler    GreekCompiler      PaliCompiler
       │                 │                 │
       ▼                 ▼                 ▼
      T1                T1                T1
       └─────────────────┼─────────────────┘
                         ▼
                        L0
                         ↓
                     ARGMAP
                         ↓
                        L2
                         ↓
                       L200
                         ↓
                        C1
                         ↓
                 epistemic graph
```

That is the key.

## GlossLM is evidence that this abstraction is sensible

GlossLM was trained on interlinear glossed text across roughly 1,800 languages, so its whole premise is that there are learnable regularities in mapping source-language forms into structured gloss representations across languages.

For Pāṭala, that suggests the universal boundary should be:

> **Every language-specific compiler must emit a standardized semantic/philological intermediate representation.**

Not:

> Every tradition needs its own entire Pāṭala stack.

That is a huge simplification.

For Greek, for example:

```text
Greek text
→ Greek tokenizer/morphology
→ lemma
→ literal gloss
→ T1
```

Then the same:

```text
L0 → ARGMAP → L2 → L200 → C1
```

could potentially run with only domain-specific prompts/contracts.

For Pāli:

```text
Pāli morphology + lexicon
→ T1
→ same core
```

For Tibetan:

```text
segmentation + grammatical analysis
→ T1
→ same core
```

Even for Latin or Arabic, the same architecture is plausible.

## But don't overgeneralize T1

The universal object should not assume Sanskrit grammar.

Bad:

```json
{
  "vibhakti": 6,
  "karaka": "agent"
}
```

as mandatory universal fields.

Better:

```json
{
  "surface": "...",
  "lemma": "...",
  "morph_features": {
    "case": "...",
    "number": "...",
    "gender": "..."
  },
  "literal_gloss": "...",
  "sense_candidates": [],
  "analysis_witnesses": []
}
```

Then language compilers can add extensions:

```text
Sanskrit:
  sandhi
  samāsa
  kāraka

Greek:
  tense/aspect/mood
  participle structure

Tibetan:
  particle analysis
  clause segmentation
```

The core remains stable.

## The really portable layer is probably L0

This is why the T1/L0 distinction you locked was smart.

T1 can retain human-readable, tradition-specific interlinear conventions.

L0 becomes:

```text
ordered units
source spans
lemmas
morphology
literal glosses
ambiguity
provenance
```

Once something reaches L0, much of the rest of Pāṭala does not need to know whether it originated in Sanskrit or Greek.

That is a strong compiler architecture.

## And the scholar products immediately generalize

Once this is true, almost every product you specced becomes cross-tradition automatically.

**Lemma/Term Tracker**

```text
vimarśa
logos
dhamma
nous
```

all use the same `Lemma → Sense → SenseUse → Evidence → Review` graph.

**Translation Compare**

Compare editions/translations in any language.

**Argument Audit**

Arguments become propositions/inferences regardless of source language.

**Peer Assessment**

Same ReviewEvent schema.

**Scholarly Diff**

Same dependency propagation.

**Trust API**

Same proposition/evidence/review interface.

That's where Pāṭala becomes much bigger than Tantra.

## But Tantra/Sanskrit should remain the proving ground

I would not expand the production corpus yet.

Sanskrit, particularly Abhinavagupta and tantric commentary, is an excellent stress test because it is hard:

```text
dense compounds
ellipsis
technical polysemy
commentarial structure
multiple philosophical speakers
cross-text technical vocabulary
```

If the universal kernel survives that, easier traditions should be much more tractable.

So the sequence should be:

```text
1. Prove Sanskrit compiler.
2. Freeze universal T1/L0 contract.
3. Identify exactly which fields are Sanskrit-specific.
4. Implement ONE second compiler.
5. Run the same Inspect contracts.
6. See what actually breaks.
7. Generalize only from observed breakage.
```

I would choose **Pāli or Classical Greek** as the second test.

Pāli gives a closely related Indic morphology/philology environment, so it tests portability without changing everything at once.

Greek is the stronger generalization test because it forces you to prove Pāṭala isn't secretly encoded around Sanskrit grammar.

The ideal eventual claim is not:

> “Pāṭala supports Sanskrit, Greek, Pāli…”

It is:

> **Pāṭala defines a language-independent scholarly compiler kernel, with language-specific front-end compilers whose outputs satisfy the same proof contracts.**

That is much more powerful.

And GlossLM is useful precisely because it gives you an already-existing multilingual precedent for the **source → structured gloss** boundary. It helps validate the architecture, even if Agent 2 ultimately beats it badly on Sanskrit.

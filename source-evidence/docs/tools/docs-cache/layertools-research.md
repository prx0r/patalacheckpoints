Yes. There is no single project that has solved **Pāṭala’s full problem**, but several research lines have already solved large chunks of the formal verification problem. The useful move is to compose them into one evaluation kernel rather than inventing bespoke scoring for every layer.

The strongest reusable stack I found is:

```text
STRUCTURE
StructEval / structured-output benchmarks
        ↓
ATOMIC CLAIM DECOMPOSITION
RefChecker / FActScore
        ↓
SOURCE ↔ OUTPUT ENTAILMENT
AlignScore / NLI
        ↓
ABSTENTION / RISK CONTROL
Conformal prediction / CIC
        ↓
MUTATION TESTING
Metamorphic testing
        ↓
EVAL ORCHESTRATION
Inspect AI
```

That is extremely close to the contract system we just designed.

## 1. T1: there is a whole field for exactly this — Interlinear Glossed Text

This was the biggest find.

Your T1:

```text
Sanskrit
→ segmentation
→ literal word/phrase gloss
→ morphological/lexical interpretation
```

is conceptually very close to **Interlinear Glossed Text (IGT)**.

**GlossLM** built a corpus of more than 450k IGT examples across roughly 1,800 languages and trained a model specifically for automatic gloss generation. Their work treats automatic glossing as a structured prediction problem rather than generic translation. ([arXiv][1])

Even more directly, Ginn et al. tested **LLMs for interlinear glossing**, including in-context example selection, and found that targeted example selection materially improves performance; prompted LLM approaches could beat standard transformer baselines in their experiments, though supervised systems remained stronger overall. ([arXiv][2])

### Pāṭala implication

Do not invent “T1 evaluation” from zero.

Borrow the IGT paradigm:

```text
SOURCE UNIT
↓
SEGMENTATION
↓
MORPHEME / TOKEN ALIGNMENT
↓
GLOSS
↓
GRAMMATICAL / LEXICAL FEATURES
```

Your tantric T1 is richer and less conventional than Leipzig-style IGT, but the evaluation architecture is transferable.

I would define:

```text
T1 benchmark =
    segmentation F1
  + token↔gloss alignment
  + gloss accuracy
  + lexical-sense accuracy
  + morphology contribution
  + abstention
```

rather than translation BLEU.

---

# 2. Sanskrit preprocessing: ByT5-Sanskrit is highly relevant

The strongest directly relevant Sanskrit-specific system I found remains **ByT5-Sanskrit**.

It was trained jointly for:

* word segmentation,
* lemmatization,
* morphosyntactic tagging,

and also reports strong results for Vedic dependency parsing and OCR post-correction. The authors explicitly describe using it as preprocessing in a Sanskrit machine-translation pipeline. ([arXiv][3])

This gives us a much better T1 architecture:

```text
SOURCE
 ↓
Vidyut / Heritage                 deterministic witnesses
 ↓
ByT5-Sanskrit                     learned linguistic witness
 ↓
LLM T1 agent                      semantic gloss/sense
 ↓
T1 verifier
```

Not:

```text
LLM figures everything out itself
```

You can make disagreement itself useful:

```text
Vidyut = X
ByT5   = X
LLM    = X
→ strong machine consensus

Vidyut = X
ByT5   = Y
LLM    = X
→ flag

all disagree
→ OPEN
```

Still not scholarship, but a much stronger machine-analysis substrate.

---

# 3. RefChecker is almost exactly the verifier architecture we need above T1

This may be the most reusable existing codebase.

RefChecker doesn't score a whole generated answer with one fuzzy number. It:

```text
generated text
      ↓
claim extractor
      ↓
fine-grained claim triplets
      ↓
checker against reference
      ↓
Entailment / Neutral / Contradiction
      ↓
aggregation
```

Their paper reports that this finer claim-triplet granularity performs better for hallucination detection than checking at whole-response, sentence or sub-sentence granularity. ([arXiv][4])

And the GitHub implementation is modular: extractor, checker and aggregation are independently replaceable; it supports LLM checkers, NLI checkers and AlignScore. ([GitHub][5])

### This maps beautifully to L2

Instead of asking:

> Is this translation similar to the T1?

Do:

```text
L2
↓
atomic semantic units
↓
for each:
   is it licensed by
   SOURCE + T1 + ARGMAP?
↓
ENTAILED
NEUTRAL / UNSUPPORTED
CONTRADICTED
```

Then:

```text
OUTPUT_LICENSE =
entailed_claims / substantive_claims
```

This is almost exactly your proposed L2 licensing metric.

## Also C1 / Essay / Education

Same machinery.

```text
C1 sentence
→ atomic claims
→ L200/source support

Essay sentence
→ atomic claims
→ theme/synthesis support

Education claim
→ essay support
```

You could fork the **architecture**, perhaps even code components, rather than reimplementing claim decomposition.

---

# 4. FActScore gives us another crucial piece: atomic factual precision

FActScore decomposes long generated text into atomic facts and measures what fraction are supported by a trusted source. ([arXiv][6])

This is almost directly:

[
License(O)=
\frac{#\text{atomic claims supported upstream}}
{#\text{atomic substantive claims in output}}
]

That's one of the core equations we independently arrived at.

So for Pāṭala:

```text
L2-License
C1-License
Essay-License
Education-License
```

can all share one generalized atomic-support evaluator.

Pāṭala's version becomes richer because the “trusted source” isn't generic retrieval:

```text
source object
T1
L0
argument map
L200
C1
theme
synthesis
```

Each layer has an explicit permitted dependency set.

That's your innovation.

---

# 5. AlignScore can supply the cheap semantic entailment layer

AlignScore was trained as a general information-alignment function using about 4.7 million examples across NLI, QA, paraphrase detection, fact verification, retrieval, semantic similarity and summarization. It was tested across 22 factual-consistency datasets. ([arXiv][7])

This is interesting because it means we don't necessarily need an expensive LLM critic for every claim.

Potential architecture:

```text
claim
 ↓
deterministic checks
 ↓
AlignScore/NLI cheap verifier
 ↓
if obvious PASS/FAIL → record
if borderline         → LLM critic
 ↓
if critic uncertain   → OPEN / human
```

That's much cheaper.

For example:

```text
Essay sentence
  ↓
candidate evidence span
  ↓
AlignScore = obvious entailment
  → pass machine check

AlignScore borderline
  ↓
strong LLM verifier
```

I would benchmark this against an all-LLM verifier rather than assume it works for Sanskrit philosophy, but the architecture is solid.

---

# 6. The enormous find: **metamorphic testing**

This formalizes our mutation idea almost perfectly.

The central problem with LLM evaluation is the **oracle problem**:

> for arbitrary generated text, what is the exact correct answer?

Metamorphic testing avoids requiring a gold answer for every case.

Instead you specify relationships that **must remain true when inputs change in controlled ways**.

A 2025 study surveyed **191 metamorphic relations** for NLP tasks and implemented 36 of them across roughly 560,000 LLM tests. ([arXiv][8])

A 2026 systematic survey covers 93 studies and explicitly describes metamorphic testing as a scalable strategy for testing LLM systems where exact expected outputs are unavailable. ([arXiv][9])

This is exactly what Pāṭala needs.

We independently called them:

```text
NEGATION_DROP
SCOPE_STRENGTHENING
OBJECTION_AS_AUTHOR_VIEW
QUALIFIER_DROP
PARAPHRASE_EXPANSION
...
```

In formal testing language those become **Metamorphic Relations (MRs).**

Example:

### MR-NEGATION

Given valid source:

```text
X does NOT establish Y
```

mutation:

```text
X establishes Y
```

required verifier behavior:

```text
original → PASS
mutation → FAIL: POLARITY
```

### MR-QUALIFIER

```text
possibly X
→ X
```

must reduce validity.

### MR-SPEAKER

```text
Opponent: X
→ Author: X
```

must fail attribution.

### MR-EVIDENCE

Remove one load-bearing evidence edge:

```text
valid Argument → invalid/incomplete Argument
```

The system should notice.

---

# 7. This means our “mutation suite” should formally become Pāṭala Metamorphic Tests

I'd explicitly adopt the terminology.

For every semantic layer:

```text
contracts/t1/METAMORPHIC-RELATIONS.yaml
contracts/argmap/METAMORPHIC-RELATIONS.yaml
contracts/l2/METAMORPHIC-RELATIONS.yaml
...
```

Example:

```yaml
- id: MR-L2-NEGATION-01
  invariant: polarity_conservation
  transform: remove_negation
  expected:
    original: PASS
    mutant: FAIL
  error_class: POLARITY_CHANGE
```

Then generate thousands of test cases mechanically.

This gives Pāṭala something far more rigorous than an LLM judge saying:

> 8/10 faithful.

---

# 8. Conformal prediction solves our abstention problem much more formally

This is another major upgrade.

We were thinking:

```text
if model uncertain:
    OPEN
```

But thresholds chosen ad hoc are weak.

**Conformal Language Modeling** adapts conformal prediction to generative LMs, providing statistical coverage guarantees for candidate output sets and even component-level correctness. ([arXiv][10])

More recently, a 2026 paper proposes a confidence-interval calibration method that chooses an acceptance threshold subject to a user-specified maximum error rate among accepted predictions, with finite-sample guarantees under its assumptions. ([arXiv][11])

That's very interesting for Pāṭala.

Instead of:

```text
score > .8 → accept
```

we could eventually use:

```text
CALIBRATION GOLD
↓
choose threshold τ
such that
P(error | machine accepts) <= α
with confidence 1-δ
```

So we could define:

```text
T1 MACHINE-ACCEPTED
target risk α = 5%

ARGMAP MACHINE-ACCEPTED
target risk α = 2%

L200 DIRECT_SUPPORT
target risk α = 1%
```

The thresholds are learned/calibrated from human gold rather than invented.

This could become genuinely powerful.

---

# 9. This gives a formal meaning to `OPEN`

At the moment OPEN is ontological/epistemic vocabulary.

We can add a statistically calibrated machine layer:

```text
MODEL PROPOSAL
     ↓
verifier score / uncertainty
     ↓
conformal/selective calibration
     ↓
MACHINE_ACCEPTABLE
or
ABSTAIN
```

Important:

```text
MACHINE_ACCEPTABLE
≠
SCHOLARLY_ACCEPTED
```

But now the former has empirical risk guarantees rather than vibes.

That is exactly the kind of separation Pāṭala wants.

---

# 10. Structured-output evaluation is also mostly solved infrastructure

There are now several systems specifically benchmarking whether LLMs produce correct structured output.

**StructEval** is a TMLR-accepted framework specifically for evaluating structured model output. ([GitHub][12])

Cleanlab's **Structured Output Benchmark** takes a slightly different angle: carefully cleaned ground truth and evaluation scripts for extraction-style structured generation, motivated by the observation that benchmark annotations themselves frequently contain errors or ambiguities. ([GitHub][13])

For Pāṭala, this says:

Don't count:

```text
JSON parsed = layer valid
```

Instead separate:

```text
Schema correctness
Field correctness
Relation correctness
Semantic correctness
```

So G0 can use StructEval-like ideas while G2 uses RefChecker/AlignScore/our gold.

---

# 11. Inspect AI really should be the outer evaluation runtime

After this search I'm even more convinced.

Inspect already provides:

* datasets,
* model invocation,
* agents/tools,
* model-graded evals,
* custom scorers,
* extensibility,
* reproducible logs,

and maintains a separate registry of community evaluations. ([GitHub][14])

So don't build:

```text
patala_eval_runner.py
patala_eval_logs.py
patala_model_runner.py
patala_eval_cli.py
...
```

Use:

```text
Inspect Task
```

for each contract.

Example:

```text
patala_t1
patala_argmap
patala_l2
patala_l200
patala_c1
patala_theme
patala_essay
```

And Pāṭala only supplies:

```text
dataset
solver/skill
custom scorers
metamorphic transforms
certificate exporter
```

---

# 12. Therefore I would change our architecture to this

This is the reusable **Pāṭala Verification Kernel**:

```text
                    PĀṬALA LAYER OUTPUT
                           │
            ┌──────────────┼───────────────┐
            ▼              ▼               ▼
       SCHEMA CHECK    ATOMICIZER     PROVENANCE CHECK
       StructEval-ish   RefChecker       native
            │              │               │
            └───────┬──────┴───────────────┘
                    ▼
             CLAIM / EDGE UNITS
                    │
            ┌───────┴────────┐
            ▼                ▼
       CHEAP VERIFIER     DOMAIN RULES
       NLI/AlignScore     native Pāṭala
            │                │
            └───────┬────────┘
                    ▼
              LLM CRITIC
          only difficult cases
                    │
                    ▼
         CALIBRATED ABSTENTION
        conformal/selective rule
                    │
           ┌────────┴─────────┐
           ▼                  ▼
     MACHINE PASS            OPEN
           │
           ▼
    METAMORPHIC TESTS
           │
           ▼
      LAYER CERTIFICATE
```

This is much better than writing an LLM judge prompt for every layer.

---

# 13. Mapping existing work onto every Pāṭala layer

| Layer     | Primary borrowed machinery              | Pāṭala-specific work                    |
| --------- | --------------------------------------- | --------------------------------------- |
| SOURCE    | deterministic testing                   | provenance, witnesses, spans            |
| **T1**    | **GlossLM / IGT + ByT5-Sanskrit**       | tantric lexical senses, false certainty |
| L0        | structured output / roundtrip           | canonical schema                        |
| ARGMAP    | structured extraction + relation F1     | grounding/inference/dialectic ontology  |
| L2        | **RefChecker + FActScore + AlignScore** | source/T1/argmap licensing              |
| L200      | structured classification               | MT/IA/OPEN ontology                     |
| C1        | RefChecker/FActScore                    | passage-local boundary                  |
| THEME     | clustering metrics + relation scoring   | evidence-backed theme definition        |
| ESSAY     | **atomic factuality + entailment**      | authority conservation                  |
| EDUCATION | entailment / factual consistency        | pedagogic simplification conservation   |

The genuinely bespoke pieces become surprisingly small.

---

# 14. The moat is therefore **not the evaluators**

This is strategically important.

Most of the generic methodology is becoming commodity.

What Pāṭala owns is:

### 1. The layer ontology

```text
SOURCE→T1→L0→ARGMAP→L2→L200→C1→...
```

### 2. Gold expert data

Especially difficult Sanskrit philosophical decisions.

### 3. Failure taxonomy

```text
FALSE_DISAMBIGUATION
CLAIM_SURFACE_INFLATION
GROUNDING_AS_INFERENCE
OBJECTION_AS_AUTHOR_VIEW
...
```

### 4. Metamorphic relations

The transformations that encode scholarly invariants.

### 5. Dependency graph

What downstream objects become stale.

### 6. Human adjudications

The genuinely scarce asset.

Everything else can be external infrastructure.

---

# 15. The architecture I'd actually implement now

Before Agent 2 writes another worker, build **one reusable verifier interface**:

```python
LayerVerifier.verify(
    output,
    upstream,
    contract
) -> LayerEvaluation
```

Conceptually returns:

```json
{
  "schema": {},
  "coverage": {},
  "claims": [],
  "entailment": {},
  "domain_errors": [],
  "metamorphic": {},
  "abstention": {},
  "status": "PASS | FAIL | OPEN"
}
```

Then plug in:

```text
T1Verifier
ArgumentMapVerifier
L2Verifier
...
```

Each adds domain-specific scorers.

But the execution/eval machinery remains shared.

---

# 16. Immediate Agent-2 research/build order

I would **not** integrate ten projects at once.

### First: T1

Use:

```text
ByT5-Sanskrit
+
IGT/GlossLM evaluation ideas
+
existing IPVV T1 gold
+
metamorphic mutations
+
Inspect
```

Build:

```text
PATALA-T1-EVAL-v0
```

This establishes the general contract architecture.

### Second: L0

Easy deterministic transformation proof.

### Third: Argument map

Build structural precision/recall + metamorphic relations.

### Fourth: L2

Use RefChecker's architecture.

```text
L2 → atomic claims
upstream → reference
claim → entail/neutral/contradict
```

This will prove whether the generalized verifier abstraction actually works.

Only then scale through the rest.

---

# 17. The really exciting formal combination

We can potentially get to:

[
\boxed{
\text{Layer passes}
===================

G_{\text{deterministic}}
\land
G_{\text{semantic}}
\land
G_{\text{metamorphic}}
\land
G_{\text{risk}}
}
]

where:

### Deterministic

hard invariants.

### Semantic

expert-gold / entailment metrics.

### Metamorphic

expected invariants survive/catch controlled transformations.

### Risk

accepted machine predictions are calibrated to a bounded observed/error-risk regime.

That is a much stronger definition of “AI layer works” than nearly any agent pipeline uses today.

And the important conclusion from the research is:

> **We do not need to invent the mathematical/evaluation paradigm. The pieces exist. Pāṭala's research contribution is combining IGT evaluation, atomic claim verification, entailment, metamorphic testing and risk-calibrated abstention into a provenance-aware multi-layer scholarly compiler.**

That is where I would concentrate the research effort.

[1]: https://arxiv.org/abs/2403.06399?utm_source=chatgpt.com "GlossLM: A Massively Multilingual Corpus and Pretrained Model for Interlinear Glossed Text"
[2]: https://arxiv.org/abs/2406.18895?utm_source=chatgpt.com "Can we teach language models to gloss endangered languages?"
[3]: https://arxiv.org/abs/2409.13920?utm_source=chatgpt.com "One Model is All You Need: ByT5-Sanskrit, a Unified Model for Sanskrit NLP Tasks"
[4]: https://arxiv.org/abs/2405.14486?utm_source=chatgpt.com "RefChecker: Reference-based Fine-grained Hallucination Checker and Benchmark for Large Language Models"
[5]: https://github.com/amazon-science/RefChecker?utm_source=chatgpt.com "GitHub - amazon-science/RefChecker: RefChecker provides automatic checking pipeline and benchmark dataset for detecting fine-grained hallucinations generated by Large Language Models. · GitHub"
[6]: https://arxiv.org/abs/2305.14251?utm_source=chatgpt.com "FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation"
[7]: https://arxiv.org/abs/2305.16739?utm_source=chatgpt.com "AlignScore: Evaluating Factual Consistency with a Unified Alignment Function"
[8]: https://arxiv.org/abs/2511.02108?utm_source=chatgpt.com "Metamorphic Testing of Large Language Models for Natural Language Processing"
[9]: https://arxiv.org/abs/2605.13898?utm_source=chatgpt.com "Bidirectional Empowerment of Metamorphic Testing and Large Language Models: A Systematic Survey"
[10]: https://arxiv.org/abs/2306.10193?utm_source=chatgpt.com "Conformal Language Modeling"
[11]: https://arxiv.org/abs/2607.04430?utm_source=chatgpt.com "Uncertainty-Aware Abstention in Large Language Models with Provable Alignment Guarantees"
[12]: https://github.com/TIGER-AI-Lab/StructEval?utm_source=chatgpt.com "GitHub - TIGER-AI-Lab/StructEval: Evaluating LLMs' abilities to generate structural output [TMLR2025] · GitHub"
[13]: https://github.com/cleanlab/structured-output-benchmark/?utm_source=chatgpt.com "GitHub - cleanlab/structured-output-benchmark: A Structured Output Benchmark whose 'ground-truth' is actually right · GitHub"
[14]: https://github.com/UKGovernmentBEIS/inspect_ai?utm_source=chatgpt.com "GitHub - UKGovernmentBEIS/inspect_ai: Inspect: A framework for large language model evaluations · GitHub"

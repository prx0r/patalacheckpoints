Yes. The key is **not to bolt six libraries into production**. Upgrade Pāṭala into a two-plane architecture:

```text
PRODUCTION COMPILER
SOURCE → T1 → L0 → ARGMAP → L2 → L200 → C1 → THEME → ESSAY → EDUCATION

                    │ every object
                    ▼

VERIFICATION PLANE
Inspect AI
 ├─ deterministic contract scorer
 ├─ semantic scorer
 ├─ RefChecker-style atomic verification
 ├─ AlignScore cheap consistency witness
 ├─ metamorphic tests
 ├─ calibrated abstention
 └─ certificate emitter
```

That separation is what makes this much more legitimate: **external ML methods test Pāṭala; they do not get to define Pāṭala truth.**

## What is actually free/open

“Free” here means **no software/model license fee**. Running models can still consume your own compute or paid API tokens.

| Component            | License/status                                                                                  | Decision                                                          |
| -------------------- | ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| **Inspect AI**       | MIT, active UK AI Security Institute framework                                                  | **Integrate directly**                                            |
| **RefChecker**       | Apache-2.0; repo archived Apr 8, 2026                                                           | **Pin/fork adapter; don't depend on upstream future development** |
| **FActScore**        | MIT                                                                                             | **Reuse atomic-fact methodology/code selectively**                |
| **AlignScore**       | MIT                                                                                             | **Integrate as optional local semantic witness**                  |
| **GlossLM weights**  | Apache-2.0 model page                                                                           | **Benchmark T1 against it**                                       |
| **StructEval**       | Apache-2.0                                                                                      | **Borrow methodology, probably don't install runtime**            |
| **ByT5-Sanskrit**    | model downloadable, but the primary HF page I found does not expose a clear license declaration | **Do not treat weights as redistribution-cleared yet**            |
| conformal prediction | research method                                                                                 | **Implement small native calibration layer**                      |
| metamorphic testing  | research method                                                                                 | **Implement natively in Pāṭala contracts**                        |

Inspect is explicitly MIT and provides datasets, solvers, scorers, model-graded evaluation, logs and extension mechanisms. ([GitHub][1]) RefChecker's code is Apache-2.0, but Amazon archived the repository in April 2026, so it is usable but should be insulated behind your own interface. ([GitHub][2]) FActScore is MIT and explicitly supports registering a custom knowledge source, which is important because Pāṭala's authoritative upstream objects—not Wikipedia—should be the reference. ([GitHub][3]) AlignScore itself is MIT.

GlossLM's published model is Apache-2.0 and comes from work on more than 450k IGT examples covering about 1,800 languages. ([Hugging Face][4]) StructEval is currently Apache-2.0 and specifically studies structured-output evaluation. ([GitHub][5]) ByT5-Sanskrit is directly relevant technically—it was trained/evaluated for Sanskrit segmentation, lemmatization and morphosyntactic tagging—but I would not redistribute its checkpoint inside Pāṭala until its weight license is explicitly confirmed; the currently indexed primary model page exposes the files but not a license declaration. ([arXiv][6])

---

# 1. Make Inspect AI the evaluation runtime

This should be the biggest immediate upgrade.

Install it in the **research/eval environment**, not the translation runtime:

```bash
pip install inspect-ai
```

Then create:

```text
evals/
  patala/
    t1.py
    l0.py
    argument_map.py
    l2.py
    l200.py
    c1.py
    theme.py
    essay.py
    education.py

    scorers/
      structure.py
      coverage.py
      atomic_support.py
      alignment.py
      metamorphic.py
      calibration.py

    datasets/
      t1/
        examples.jsonl
        dev.jsonl
        test.jsonl
```

Inspect was designed specifically as an extensible LLM-evaluation framework and maintains reproducible evaluation logs, which means it can replace a lot of bespoke benchmark-runner infrastructure. ([GitHub][1])

Your T1 evaluation becomes conceptually:

```python
@task
def patala_t1():
    return Task(
        dataset=...,
        solver=t1_skill_solver(),
        scorer=[
            t1_structure(),
            t1_coverage(),
            t1_gloss(),
            false_certainty(),
            metamorphic(),
        ],
    )
```

Then the command becomes something like:

```bash
inspect eval evals/patala/t1.py \
  --model openai/deepseek-v4-flash
```

Hermes/Pāṭala may invoke the model in production.

**Inspect measures whether it actually works.**

That distinction matters.

---

# 2. Introduce one native `LayerContract`

Do this before integrating anything else.

```python
LayerContract(
    layer="T1",

    upstream=["SOURCE"],

    deterministic=[
        "schema",
        "source_binding",
        "coverage",
        "input_hash",
    ],

    semantic=[
        "segmentation",
        "literal_gloss",
        "technical_sense",
        "false_certainty",
        "abstention",
    ],

    metamorphic=[
        "NEGATION",
        "CASE_ROLE",
        "LEXICAL_SENSE",
        "FALSE_DISAMBIGUATION",
    ],

    gates={
        "engineering": ...,
        "semantic": ...,
        "autonomous": ...
    }
)
```

Everything else plugs into this.

Not:

```text
RefChecker objects
AlignScore objects
Inspect objects
```

inside your canonical corpus.

Instead:

```text
Pāṭala object
   ↓
LayerContract
   ↓
external evaluators
   ↓
EvaluationEvidence
```

---

# 3. T1: integrate GlossLM as a **baseline**, not authority

GlossLM's research task is unusually close to T1: automatic interlinear gloss generation using standardized IGT data. ([arXiv][7])

Download/use its Apache-2.0 model separately:

```text
research/models/glosslm/
```

Then build an adapter:

```python
class GlossLMBaseline:
    def gloss(source: str) -> GlossPrediction:
        ...
```

Do **not** make:

```text
GlossLM says X
→ T1 = X
```

Instead:

```text
SOURCE
   │
   ├── Pāṭala T1 agent
   ├── GlossLM baseline
   └── deterministic Sanskrit witnesses

             ↓

       benchmark comparison
```

Now your paper/result can say:

> Pāṭala T1 agent beats a published multilingual gloss-generation baseline on our frozen Sanskrit philosophical test set.

That is far more meaningful than:

> our prompt looks good.

GlossLM becomes your **external baseline**.

---

# 4. T1 also gets a Sanskrit linguistic witness

ByT5-Sanskrit was built specifically around Sanskrit segmentation, lemmatization and morphosyntactic tagging, and the paper reports strong performance on those tasks. ([arXiv][6])

Architecture:

```text
                RAW SANSKRIT
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
     Vidyut       Heritage    ByT5-Sanskrit
        │            │            │
        └────────────┼────────────┘
                     ▼
             LinguisticWitness
                     │
                     ▼
                  T1 Agent
```

But until checkpoint licensing is clarified:

```text
ByT5 = research/eval optional dependency
```

not:

```text
ByT5 weights committed into repo
```

And certainly not:

```text
ByT5 output = correct Sanskrit
```

It remains another machine witness.

---

# 5. RefChecker becomes the architecture for **output licensing**

This is probably the biggest semantic-verification upgrade.

RefChecker decomposes generated text into fine-grained claims and evaluates them against references as entailment, neutral or contradiction. Its architecture explicitly separates extraction, checking and aggregation. ([GitHub][2])

Wrap it:

```text
evals/patala/adapters/refchecker.py
```

with a Pāṭala interface:

```python
verify_claims(
    output=L2,
    reference=[T1, argument_map]
)
```

Result:

```json
{
  "claims": [
    {
      "claim": "...",
      "relation": "ENTAILED",
      "support_refs": [...]
    },
    {
      "claim": "...",
      "relation": "NEUTRAL"
    }
  ]
}
```

Then translate their vocabulary:

```text
RefChecker ENTAILMENT
        ↓
Pāṭala MACHINE_LICENSED

RefChecker NEUTRAL
        ↓
Pāṭala UNSUPPORTED_CANDIDATE

RefChecker CONTRADICTION
        ↓
Pāṭala CONTRADICTION_CANDIDATE
```

**Never**:

```text
RefChecker entailment
=
scholarly truth
```

---

# 6. Use the same verifier for L2, C1, Essay and Education

This massively reduces custom work.

## L2

```text
reference =
SOURCE + T1 + argument map

claim =
atomic statements extracted from L2
```

Question:

> Is each L2 claim licensed upstream?

## C1

```text
reference =
L200 + L2 + passage evidence

claim =
C1 assertions
```

Question:

> Did commentary add anything it cannot support?

## Essay

```text
reference =
Theme + Arguments + Evidence

claim =
essay assertions
```

## Education

```text
reference =
Essay

claim =
pedagogical assertions
```

So one generic kernel:

```python
AtomicLicenseVerifier(output, permitted_upstream)
```

works across four layers.

That is a serious simplification.

---

# 7. Add FActScore's atomic-fact idea, but don't adopt its old pipeline wholesale

FActScore's core idea is exactly useful: decompose long text into atomic claims and score what fraction are supported. It also permits a custom knowledge source. ([GitHub][3])

But its reference implementation is built around older retrieval/model assumptions and can use paid OpenAI calls. ([GitHub][3])

Therefore:

**Reuse:**

```text
atomic decomposition paradigm
factual precision metric
response/abstention distinction
```

Don't necessarily reuse:

```text
Wikipedia retrieval
old Llama pipeline
default OpenAI evaluator
```

Pāṭala's generalized metric becomes:

[
\text{UpstreamLicensePrecision}
===============================

\frac{\text{atomic output claims supported upstream}}
{\text{all substantive atomic output claims}}
]

This metric should appear on:

```text
L2
C1
THEME
ESSAY
EDUCATION
```

---

# 8. AlignScore should be a cheap **witness**, not your final judge

AlignScore asks whether information in a claim is contained in its context, using an alignment model trained over several related language-understanding tasks. ([GitHub][8])

It's MIT licensed.

But its released implementation/checkpoints are RoBERTa-based and the repository recommends an older PyTorch version, so I would isolate it from your main environment. ([GitHub][8])

Use:

```text
research/venvs/alignscore/
```

or Docker.

Then:

```text
atomic claim
    ↓
AlignScore
    ↓
cheap candidate score

high confidence
    ↓
record machine witness

borderline
    ↓
LLM critic

still uncertain
    ↓
OPEN
```

Do not let `0.87` become epistemic truth.

Store:

```json
{
  "method": "AlignScore",
  "score": 0.87,
  "role": "MACHINE_WITNESS"
}
```

---

# 9. Don't really integrate StructEval

I would **cite and borrow from it**, not add it as a production dependency.

StructEval is intended specifically for evaluating structured LLM output and includes inference/rendering/evaluation infrastructure. ([GitHub][5])

But Pāṭala already has:

```text
schemas
registry
validators
canonical object shapes
```

Installing StructEval's rendering stack, Playwright, Graphviz, ImageMagick, etc. would add complexity without solving your main problem. Its documented dependencies are substantially heavier than what Pāṭala needs. ([GitHub][5])

Borrow the principle:

```text
STRUCTURAL VALIDITY
≠
SEMANTIC VALIDITY
```

and implement G0 yourself.

---

# 10. Formalize all your historical failures as metamorphic tests

This is where Pāṭala can become unusually serious.

Metamorphic testing is specifically meant for systems where exact expected answers are difficult to specify: instead of requiring an oracle for every arbitrary output, you test necessary relationships across controlled transformations. Recent LLM work has catalogued 191 such relations and tested a representative subset at large scale; a 2026 systematic survey covers 93 studies. ([arXiv][9])

Create:

```text
contracts/metamorphic/
```

and then:

```text
universal.yaml
t1.yaml
argument-map.yaml
l2.yaml
l200.yaml
c1.yaml
essay.yaml
```

Example:

```yaml
id: MR-L2-NEGATION-001
layer: L2

transform:
  type: DROP_NEGATION

invariant:
  name: POLARITY_CONSERVATION

expected:
  original: PASS
  mutant: FAIL

failure_class:
  POLARITY_CHANGE
```

Other relations should come directly from your actual failures:

```text
FALSE_DISAMBIGUATION
TECHNICAL_SENSE_FLATTENING
CASE_ROLE_SWAP

OBJECTION_AS_AUTHOR_VIEW
GROUNDING_AS_INFERENCE
INFERENCE_DIRECTION_FLIP

PARAPHRASE_EXPANSION
CLAIM_SURFACE_INFLATION
QUALIFIER_DROP
MODALITY_STRENGTHENING

CORROBORATION_AS_APPROVAL
EVIDENCE_LAUNDERING
```

This becomes part of the moat.

---

# 11. Implement conformal/risk calibration natively

Don't add a giant dependency.

Conformal Language Modeling demonstrates that conformal methods can give statistical coverage guarantees for sets of generated answers and can identify subsets/components judged correct under stated assumptions. ([arXiv][10])

Pāṭala doesn't initially need the entire generation-set algorithm.

You need **risk-calibrated abstention**.

Take your DEV calibration set:

```text
verifier score   human correctness

.98              correct
.95              correct
.91              wrong
.88              correct
...
```

Then choose a threshold from frozen calibration data.

Eventually:

```text
score >= τ_T1
→ MACHINE_ACCEPTABLE

score < τ_T1
→ OPEN
```

Store the calibration evidence:

```json
{
  "threshold": 0.93,
  "calibration_set": "T1-CAL-v2",
  "n": 240,
  "observed_error": 0.031,
  "method": "risk_control_v1"
}
```

The point is not to say:

> 93% = true.

It's:

> Our acceptance policy was calibrated on independent human gold and achieved measured risk X on held-out data.

That is dramatically more defensible.

---

# 12. Build one unified `VerificationEvidence` object

Every external tool should end here:

```json
{
  "evaluation_id": "eval:T1:abc123",

  "object_ref": "pt:t1:...",
  "object_version": "v3",

  "contract": "T1-v1.2",

  "methods": [
    {
      "name": "deterministic",
      "version": "...",
      "result": {}
    },
    {
      "name": "GlossLM",
      "version": "...",
      "result": {}
    },
    {
      "name": "AlignScore",
      "version": "...",
      "result": {}
    },
    {
      "name": "LLM_CRITIC",
      "model": "...",
      "prompt_hash": "...",
      "result": {}
    }
  ],

  "metamorphic_suite": "...",

  "gold_split": "TEST-v1",

  "status": "SEMANTICALLY_VALIDATED"
}
```

External evaluators remain evidence.

Pāṭala decides the state transition.

---

# 13. Then the autonomy controller changes subtly

Current idea:

```text
generate
→ validator
→ commit
```

Upgrade:

```text
GENERATE
   ↓
G0 structural validation
   ↓
COMMIT MACHINE_PROPOSED
   ↓
run verification suite
   ↓
G1 deterministic integrity
G2 semantic evaluation
G3 metamorphic tests
   ↓
risk calibration
   ↓
SEMANTICALLY_VALIDATED
or
OPEN / REVIEW_REQUIRED
```

That means the generative factory can continue producing work **without pretending every output has passed semantic validation**.

Very important.

---

# 14. Exactly how I would assign Agent 2 now

### Upgrade A — infrastructure

Install:

```text
inspect-ai
```

Add optional isolated eval dependencies:

```text
refchecker
factscore
alignscore
```

Pin exact versions and record their licenses in:

```text
THIRD_PARTY.yml
```

Example:

```yaml
inspect_ai:
  license: MIT
  role: evaluation runtime

refchecker:
  license: Apache-2.0
  upstream_status: archived-2026-04-08
  role: claim extraction/checking reference

factscore:
  license: MIT
  role: atomic decomposition methodology

alignscore:
  license: MIT
  role: semantic machine witness

glosslm:
  license: Apache-2.0
  role: T1 external baseline
```

---

# 15. Upgrade B — build `PATALA-EVALS`

```text
evals/
  README.md

  core/
    layer_contract.py
    evaluation_evidence.py
    certificates.py

  scorers/
    deterministic.py
    atomic_support.py
    semantic_alignment.py
    metamorphic.py
    risk.py

  adapters/
    refchecker.py
    alignscore.py
    glosslm.py

  tasks/
    t1.py
```

Don't build the other eight tasks yet.

**T1 only.**

---

# 16. Upgrade C — make T1 the proof-of-concept

Run the same frozen TEST against:

```text
Pāṭala T1 agent
GlossLM
raw DeepSeek prompt
raw Claude/GPT/etc when desired
```

Measure:

```text
segmentation F1
source coverage
gloss accuracy
technical-term accuracy
unsupported addition
false certainty
abstention precision
abstention recall
metamorphic detection rate
review minutes / 1000 tokens
```

GlossLM gives you an external published baseline rather than only comparing variants of your own system. Its underlying work specifically concerns automatic IGT generation, making it relevant as a baseline even though it was not designed for tantric Sanskrit. ([arXiv][7])

---

# 17. Upgrade D — only once T1 passes, derive L0

Then:

```text
T1
↓
t1_extract.py
↓
L0
```

L0 does **not need RefChecker or GlossLM**.

Its contract is:

```text
roundtrip
coverage
mapping
provenance
schema
hash
```

This should be essentially deterministic.

That's cleaner science.

---

# 18. Then replicate the kernel upward

Once T1 and L0 prove the framework:

```text
ARGMAP
  structural edge/node F1
  + LLM critic
  + metamorphic suite

L2
  RefChecker atomic licensing
  + AlignScore witness
  + domain mutations

L200
  classification benchmark
  + false-positive MT rate

C1
  atomic licensing against L200
  + locality mutations

THEME
  member/role gold
  + lexical-coincidence mutations

ESSAY
  atomic licensing
  + C.1 paraphrase mutations

EDUCATION
  atomic licensing
  + simplification mutations
```

Same infrastructure.

Different contract.

---

# 19. How this makes Pāṭala substantially more legitimate

Right now a skeptical researcher could ask:

> “How do you know your agent output is good?”

and we have lots of internal answers.

After this upgrade, the answer becomes:

```text
1. Canonical task definition published.
2. Frozen expert-gold dataset published.
3. DEV/TEST separation published.
4. External baselines included.
5. Every model run reproducibly logged by Inspect.
6. Structural and semantic correctness reported separately.
7. Controlled metamorphic failures tested.
8. Abstention/error calibration measured.
9. All generated objects carry exact model/prompt/code hashes.
10. Results emit immutable evaluation certificates.
11. Human disagreements become versioned adjudication data.
```

Inspect already exists specifically to support reproducible LLM evaluations rather than ad hoc model demos. ([GitHub][1])

Then Pāṭala can release:

```text
PĀṬALA-T1 v1
A benchmark for Sanskrit philosophical interlinear translation
```

with:

```text
paper
dataset card
task specification
gold
scorer
baseline results
Inspect eval
metamorphic suite
leaderboard
```

That is a real research artifact.

---

# 20. And this creates your eventual paper

Something like:

> **Pāṭala: Contract-Based Verification for Autonomous Translation of Premodern Sanskrit Philosophy**

The interesting contribution would not be:

> we made an AI translate Sanskrit.

It would be:

> **we define translation as a sequence of typed scholarly transformations, give each transformation an independently testable contract, combine deterministic validation, external ML witnesses, atomic entailment checking, metamorphic testing and calibrated abstention, and preserve all outputs in a versioned provenance graph.**

That is a far stronger research claim.

And critically, most of the commodity infrastructure is permissively licensed, so Pāṭala can keep its bespoke work concentrated exactly where it should be: **canonical layer semantics, expert gold, failure taxonomies, metamorphic scholarly invariants, dependency propagation and adjudication history.** ([GitHub][1])

[1]: https://github.com/UKGovernmentBEIS/inspect_ai?utm_source=chatgpt.com "GitHub - UKGovernmentBEIS/inspect_ai: Inspect: A framework for large language model evaluations · GitHub"
[2]: https://github.com/amazon-science/RefChecker?utm_source=chatgpt.com "GitHub - amazon-science/RefChecker: RefChecker provides automatic checking pipeline and benchmark dataset for detecting fine-grained hallucinations generated by Large Language Models. · GitHub"
[3]: https://github.com/shmsw25/factscore?utm_source=chatgpt.com "GitHub - shmsw25/FActScore: A package to evaluate factuality of long-form generation. Original implementation of our EMNLP 2023 paper \"FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation\" · GitHub"
[4]: https://huggingface.co/lecslab/glosslm?utm_source=chatgpt.com "lecslab/glosslm · Hugging Face"
[5]: https://github.com/TIGER-AI-Lab/StructEval?utm_source=chatgpt.com "GitHub - TIGER-AI-Lab/StructEval: Evaluating LLMs' abilities to generate structural output [TMLR2025] · GitHub"
[6]: https://arxiv.org/abs/2409.13920?utm_source=chatgpt.com "One Model is All You Need: ByT5-Sanskrit, a Unified Model for Sanskrit NLP Tasks"
[7]: https://arxiv.org/abs/2403.06399?utm_source=chatgpt.com "GlossLM: A Massively Multilingual Corpus and Pretrained Model for Interlinear Glossed Text"
[8]: https://github.com/yuh-zha/AlignScore?utm_source=chatgpt.com "GitHub - yuh-zha/AlignScore: ACL2023 - AlignScore, a metric for factual consistency evaluation. · GitHub"
[9]: https://arxiv.org/abs/2511.02108?utm_source=chatgpt.com "Metamorphic Testing of Large Language Models for Natural Language Processing"
[10]: https://arxiv.org/abs/2306.10193?utm_source=chatgpt.com "Conformal Language Modeling"

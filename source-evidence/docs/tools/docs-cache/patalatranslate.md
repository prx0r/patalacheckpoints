Yes. Translation deserves its **own Pāṭala subsystem**. After going through the current Sanskrit work, WMT evaluation research, alignment methods, and personal GitHub builds, I think the frontier architecture is much sharper than “generate several translations and have another LLM judge them.”

The key idea is:

> **A translation cannot generally be mathematically proven equivalent to a source text. But it can be made proof-carrying.**

Meaning every published translation carries a machine-readable bundle showing **what Sanskrit was read, how it was parsed, which target spans realize which source obligations, what could not be verified, what alternative readings exist, and which independent checks/reviewers passed it**.

That is significantly stronger than a COMET score.

---

# 1. The Sanskrit frontier has just moved a lot: Mitrasamgraha

**Paper:** `https://arxiv.org/abs/2601.07314`

Mitrasamgraha is probably the most important dataset for your translation layer right now. It contains **391,548 Sanskrit–English bitext pairs** spanning more than three millennia and multiple genres, plus **5,587 post-corrected validation pairs and 5,552 post-corrected test pairs**. The authors specifically note persistent failures on compounds, philosophical concepts and layered metaphor even after fine-tuning NLLB/Gemma models. ([arXiv][1])

That means I would immediately make it:

```text
PĀṬALA TRANSLATION BENCHMARK
              │
              ├── temporal slice
              ├── genre
              ├── philosophical prose
              ├── poetry
              ├── scientific Sanskrit
              └── post-corrected gold
```

Do not just train on it.

Use it to discover **error families**.

For example:

```text
Mitrasamgraha errors
      ↓
cluster
      ↓
compound semantic loss
scope loss
case-role inversion
negation loss
implicit subject error
technical-term substitution
metaphor literalisation
unlicensed explicitation
```

Those become Pāṭala validators.

---

# 2. MITRA is even crazier for cross-source translation verification

**Paper:** `https://arxiv.org/abs/2601.06400`

**Repo:** `https://github.com/dharmamitra/mitra-parallel`

MITRA contains roughly **1.74 million sentence-level parallel pairs** across Sanskrit, Buddhist Chinese and Tibetan and ships domain-specific MT and embedding models. Its Gemma 2 MITRA models were trained specifically for these historical languages rather than ordinary modern multilingual MT. ([arXiv][2])

This changes your Buddhist/Sanskrit translation architecture.

Suppose:

```text
Sanskrit S
   ↓
candidate English E
```

You may also have:

```text
Sanskrit S
   ↔ Tibetan T
   ↔ Chinese C
```

Then Pāṭala can ask:

```text
What semantic commitments survive across:

S
T
C
E
?
```

Not as majority voting.

Instead, as **independent historical witnesses to interpretation**.

Example:

```text
Sanskrit:
ambiguous construction

Tibetan:
explicitly resolves X

Chinese:
appears to resolve X

commentary:
resolves X

English candidate:
resolves Y

              ↓

TRANSLATION REVIEW FLAG
```

That's enormously more powerful than conventional MT evaluation.

---

# 3. The best personal project here may actually be FoJin

`https://github.com/xr843/fojin`

This is exactly the level of weird useful personal implementation we've been hunting.

FoJin already imports MITRA alignments and has a human-review-gated alignment pipeline. It uses margin-based routing to separate likely matches from uncertain matches, performs paragraph→sentence refinement with a bertalign-style dynamic program, stores stable character offsets, exposes cross-lingual parallel-sentence search, and maintains an explicit alignment evaluation harness. ([GitHub][3])

The architecture is:

```text
candidate parallel
      ↓
cheap similarity
      ↓
confidence margin
      │
 ┌────┼────────────┐
 ▼    ▼            ▼
reject uncertain candidate
      │
      ▼
   verifier
      │
      ▼
human review
      │
      ▼
verified alignment
```

This is almost exactly how your translation alignments should work.

### I would clone FoJin immediately.

Specifically inspect:

```text
build_alignments.py
refine_sentence_alignments.py
services/sentence_align.py
alignment eval harness
MITRA import
stable-offset representation
```

Do **not** rebuild all of this.

---

# 4. ByT5-Sanskrit should become one of your proof generators

**Paper:** `https://arxiv.org/abs/2409.13920`

The crucial thing about ByT5-Sanskrit is not “use this model to translate.”

It's that it gives you a Sanskrit-specific analytical layer. It reports state-of-the-art or near-state-of-the-art results across word segmentation, lemmatization, morphosyntactic tagging, Vedic dependency parsing and OCR correction. ([arXiv][4])

That means:

```text
SOURCE
  ↓
ByT5-Sanskrit
  ↓
SourceAnalysisCandidate
{
    segmentation
    lemma
    morphology
    dependency
}
```

Now compare the translation against those grammatical obligations.

Example Sanskrit:

```text
X-ena Y kriyate
```

analysis produces:

```text
X
case=instrumental

Y
...

kriyate
passive
```

Candidate English:

```text
"X performs Y"
```

Potential flag:

```text
VOICE / ROLE MISMATCH
```

The important principle:

> **ByT5 doesn't decide the translation. It generates independently inspectable constraints.**

That's exactly the role deterministic/Sanskrit-specialized models should play.

---

# 5. Keep the old Sanskrit Heritage machinery too

Python wrapper:

`https://github.com/hrishikeshrt/heritage`

This gives programmatic access to the Sanskrit Heritage morphological machinery, including segmentation/morphological analysis, declensions, conjugations and sandhi. ([GitHub][5])

So I'd run **multiple independent analyzers**:

```text
              Sanskrit
                 │
        ┌────────┼────────┐
        ▼        ▼        ▼
      Vidyut  Heritage   ByT5
        │        │        │
        └────────┼────────┘
                 ▼
          analysis lattice
```

Agreement becomes strong evidence.

Disagreement becomes:

```text
ANALYSIS_UNCERTAIN
```

rather than the LLM silently choosing one.

That is exactly what a scholarly translation platform should expose.

---

# 6. `skrutable` is another excellent tiny Sanskrit tool

`https://github.com/tylergneill/skrutable`

It combines transliteration, meter/scansion, sandhi and compound splitting in a small Python toolkit. ([GitHub][6])

Don't overlook meter.

For verse:

```text
candidate segmentation
        ↓
does meter still work?
```

Meter can act as an **independent structural constraint** on segmentation.

That gives:

```text
Segmentation A
grammar ✓
meter ✓

Segmentation B
grammar ✓
meter ✗
```

Not proof, but useful additional evidence.

---

# 7. `OliverHellwig/sanskrit` is a quiet goldmine

`https://github.com/OliverHellwig/sanskrit`

Hellwig's repo contains corpora, DCS data, texts, translations and quantitative Sanskrit research materials. ([GitHub][7])

And Ambuda has independently sanitized DCS data:

`https://github.com/ambuda-org/dcs`

The latter explicitly applies corrections over the Digital Corpus of Sanskrit data. ([GitHub][8])

This gives you huge amounts of:

```text
form
lemma
morphology
context
```

for checking whether your analysis of a difficult occurrence is consistent with attested Sanskrit usage.

---

# 8. Now the general MT audit frontier: xCOMET

**Repo:** `https://github.com/Unbabel/COMET`

**Paper:** `https://arxiv.org/abs/2310.10482`

xCOMET is still essential because it moved evaluation from:

```text
translation = 0.87
```

to:

```text
span 17–23
severity=major
translation error
```

It produces sentence scores plus localized minor/major/critical error spans and can run reference-based or reference-free variants. COMET now also supports document context through DocCOMET. Sanskrit is among the languages represented by its underlying multilingual backbone. ([GitHub][9])

For Pāṭala:

```text
XCOMET ERROR
       ↓
TranslationAuditCandidate
       ↓
must be independently validated
```

Do **not** let xCOMET itself veto a Sanskrit translation.

Its training distribution is overwhelmingly not classical Śaiva philosophical Sanskrit.

Use it as a smoke detector.

---

# 9. Google's 2025 frontier: MetricX-25 + GemSpanEval

Paper:

`https://arxiv.org/abs/2510.24707`

GemSpanEval formulates translation error detection as a generative task that outputs:

```text
error span
context
severity
category
```

while MetricX-25 predicts overall translation quality. Both were submitted to the WMT25 evaluation task and are Gemma-3-based. ([arXiv][10])

This gives another independent auditor:

```text
xCOMET
   vs
GemSpanEval
   vs
LLM MQM reviewer
```

If all three independently flag the same English phrase:

```text
priority ↑↑↑
```

If only one flags it:

```text
weak evidence
```

That is how I'd use learned evaluators.

---

# 10. OTTAWA is extremely important for your omission/addition problem

**Paper:** `https://arxiv.org/abs/2406.01919`

OTTAWA was specifically designed to detect **hallucination and omission in machine translation** using optimal-transport word alignment. Its clever move is to explicitly model **null alignment**, allowing source or target tokens to remain unmatched. ([arXiv][11])

Conceptually:

```text
SANSKRIT TOKENS

s1 → e4
s2 → e7
s3 → NULL   ← possible omission

ENGLISH TOKENS

e1 ← s1
e2 ← NULL   ← possible addition
```

This is almost tailor-made for your existing Pāṭala concerns.

I'd implement:

```text
SOURCE_COVERAGE
TARGET_GROUNDING
```

separately.

[
C_s =
\frac{\text{source semantic units aligned}}
{\text{source semantic units}}
]

[
G_t =
\frac{\text{target semantic units grounded}}
{\text{target semantic units}}
]

Low (C_s):

> possible omission.

Low (G_t):

> possible unsupported addition.

That is much more interpretable than BLEU/COMET.

---

# 11. `awesome-align`

`https://github.com/neulab/awesome-align`

This is an excellent practical word-alignment implementation using multilingual BERT. It returns explicit word pairs and optional alignment probabilities and can be fine-tuned on your own parallel corpus. ([GitHub][12])

I'd benchmark:

```text
awesome-align
OTTAWA
MITRA embeddings
LLM alignment
```

on a manually annotated Pāṭala Sanskrit↔English gold set.

Then choose by error family, not one global winner.

---

# 12. `bertalign`

GitHub project:

`https://github.com/bfsujason/bertalign`

It is actively maintained as of 2026 and focuses on multilingual **sentence-level alignment** using sentence embeddings. ([GitHub][13])

This should operate one level above word alignment:

```text
Work
 ↓
chapter alignment
 ↓
passage alignment
 ↓
sentence alignment
 ↓
word/span alignment
```

Hierarchical alignment is much safer than globally comparing every source sentence with every target sentence.

---

# 13. A very interesting research idea: word alignment itself as training preference

Paper:

`https://arxiv.org/abs/2405.09223`

The authors found alignment quality correlates with hallucination/omission and used better alignments as a preference signal for optimizing translation models. ([arXiv][14])

That gives you a future training signal.

Instead of:

```text
Human prefers translation A
```

you could derive:

```text
A:
source coverage 98%
grounding 99%

B:
source coverage 91%
grounding 93%

→ prefer A
```

Then combine that with scholar judgments.

---

# 14. Bi-directional entailment should become another Pāṭala test

Older paper, but still conceptually excellent:

`https://arxiv.org/abs/1911.00681`

The idea is to require:

```text
source meaning ⇒ translation meaning

AND

translation meaning ⇒ source meaning
```

rather than one-way semantic similarity. ([arXiv][15])

For Sanskrit you can't naïvely feed both languages into an English NLI model.

But you can use **semantic propositions** as an intermediate representation.

Example:

```text
SOURCE ANALYSIS
      ↓
propositions Ps

TRANSLATION
      ↓
propositions Pt
```

then test approximately:

[
P_s \models P_t
]

and:

[
P_t \models P_s
]

Failure first direction:

```text
translation adds semantic strength
```

Failure reverse direction:

```text
translation omits semantic content
```

This is basically the formalized version of the semantic-strength problem you've already uncovered in Pāṭala.

---

# 15. MQM should become the error vocabulary

Google's human WMT MQM dataset/code:

`https://github.com/google/wmt-mqm-human-evaluation`

MQM human evaluators mark explicit spans and classify errors under categories including:

```text
Accuracy
Fluency
Terminology
Style
Locale
```

with severity separated into major/minor/neutral. ([GitHub][16])

Pāṭala needs a **Sanskrit scholarly extension** of MQM.

Something like:

```text
ACCURACY
├ omission
├ addition
├ mistranslation
├ semantic-strength inflation
├ semantic-strength weakening
├ negation
├ modality
├ scope
├ argument-role inversion
└ coreference

SANSKRIT
├ segmentation
├ morphology
├ case-role
├ compound-analysis
├ syntax
├ ellipsis
├ technical-term
├ commentary-dependence
└ textual-reading

PHILOSOPHICAL
├ proposition inflation
├ ontological import
├ epistemic-strength shift
├ causal-strength shift
├ identity/similarity conflation
└ interpretation presented as translation
```

**This could itself become a valuable scholarly standard.**

---

# 16. Important 2026 warning: automatic evaluators do NOT agree perfectly with humans

Paper:

`https://arxiv.org/abs/2605.24904`

A May 2026 study comparing LLM MQM span judges and xCOMET-XXL against expert human span annotations found agreement on naturally occurring translation errors is non-trivial. ([arXiv][17])

This is exactly why:

```text
COMET PASS
```

cannot mean:

```text
translation verified
```

Your system should say:

```text
XCOMET:
no major errors detected

OTTAWA:
source coverage 0.97

morphological obligations:
14/15 satisfied

term consistency:
pass

human:
not reviewed
```

That's epistemically accurate.

---

# 17. Also: don't throw entire books into an LLM judge

This 2025 study is useful:

`https://arxiv.org/abs/2505.01761`

It found that as evaluation context gets longer, LLM judges tend to identify **fewer error spans**, degrading ranking accuracy; focused-sentence prompting and specialized fine-tuning mitigate the effect. ([arXiv][18])

Therefore Pāṭala should do:

```text
document context available
        +
current passage highlighted
        +
local source/target focus
```

not:

```text
"Here are 30 pages. Find errors."
```

This validates your passage-centric object model.

---

# 18. BSC's MT-Lens — do not build the metric harness from scratch

`https://github.com/bsc-lt/mt-evaluation`

MT-Lens already unifies multiple translation backends and evaluation metrics including XCOMET, COMET, MetricX, BLEURT, ChrF and TER in one configurable evaluation framework. ([GitHub][19])

This is likely your base evaluation runner.

I would fork/wrap it:

```text
MT-Lens
   +
Pāṭala Sanskrit audits
```

Add:

```text
OTTAWA
morphology coverage
compound audit
term audit
negation audit
scope audit
semantic-strength audit
parallel witness audit
```

Much less work.

---

# 19. Amazon's span meta-evaluation toolkit is also important

`https://github.com/amazon-science/span-mt-metaeval`

This project evaluates the **evaluators themselves** against human WMT MQM annotations. ([GitHub][20])

That is a critical concept for Pāṭala.

You don't merely benchmark:

```text
translator
```

You benchmark:

```text
auditor
```

For example:

```text
NegationAuditor v3

precision 0.97
recall    0.91
false-positive families:
  quoted negation
  lexicalized privatives
```

Auditors themselves become versioned, evaluated scholarly machinery.

That is very Pāṭala.

---

# 20. Google's `mt-metrics-eval`

`https://github.com/google-research/mt-metrics-eval`

It packages WMT sources, references, system outputs, human MQM scores and metric scores specifically for developing and statistically evaluating MT metrics. ([GitHub][21])

Use it as your **meta-evaluation benchmark harness**.

Not Sanskrit-specific, but critical for testing whether your new audit metrics are sane before claiming anything.

---

# 21. Sāmayik — useful, but don't confuse it with classical Sanskrit

`https://github.com/ayushbits/saamayik`

Sāmayik contains around **52k English–Sanskrit parallel sentences**, including educational, technical, biblical and spiritual material plus an explicit out-of-domain split. ([GitHub][22])

Use it for:

```text
general Sanskrit-English competence
domain-shift testing
modern prose
```

not as your main Tantric/philosophical benchmark.

Mitrasamgraha is much more important for that.

---

# 22. AI4Bharat IndicTrans2 — baseline, not scholarly translator

`https://github.com/AI4Bharat/IndicTrans2`

IndicTrans2 explicitly supports Sanskrit↔English and releases training/evaluation infrastructure and multilingual models. ([GitHub][23])

It's useful as a **candidate generator / baseline**:

```text
Candidate 1 frontier LLM
Candidate 2 domain LLM
Candidate 3 MITRA model
Candidate 4 IndicTrans2
```

Disagreements are extremely useful.

If four independent systems translate a construction differently:

```text
uncertainty ↑
```

This should trigger deeper analysis.

---

# 23. AI4Bharat's IndicLLMSuite has a human-audit pipeline worth stealing

`https://github.com/AI4Bharat/IndicLLMSuite`

The repo includes large Indic datasets plus **Setu**, structure-preserving translation/transliteration pipelines, and actual human data-audit portals. Sanskrit is included among its supported languages. ([GitHub][24])

Mine:

```text
human verification portal
structure-preserving translation
data provenance
audit workflow
```

not its entire LLM stack.

---

# 24. There is another subtle insight from the Sanskrit poetry work

Paper:

`https://arxiv.org/abs/2511.08145`

The 2025 Sanskrit poetry→prose study found a domain-specialized ByT5-Sanskrit model beat instruction-driven general-purpose LLMs, and frames **anvaya reconstruction** as a distinct task involving compound segmentation, dependency resolution and syntactic linearization. ([arXiv][25])

This suggests a huge architectural improvement:

## Don't go directly Sanskrit → English.

Instead:

```text
ORIGINAL SANSKRIT
        ↓
segmentation
        ↓
morphology
        ↓
ANVAYA
canonical prose-order reconstruction
        ↓
semantic proposition structure
        ↓
ENGLISH
```

For verse, this is particularly strong.

And even philosophical prose may benefit from a normalized syntactic representation.

---

# 25. Therefore I think translation needs its own intermediate representation

Call it something like:

```text
Translation IR
```

Example:

```json
{
  "source_span": "S17",
  "tokens": [...],
  "analyses": [...],

  "syntax": {
    "predicate": "...",
    "arguments": [...]
  },

  "semantic_obligations": [
    {
      "id": "O1",
      "type": "negation",
      "source_span": [18, 22]
    },
    {
      "id": "O2",
      "type": "instrumental-role"
    },
    {
      "id": "O3",
      "type": "epistemic-modality"
    }
  ],

  "target_realizations": [...],

  "unresolved": [...]
}
```

Now translation verification is not:

```text
"Does this sound accurate?"
```

but:

```text
Were obligations O1...On preserved?
```

That is a much harder target for hallucination.

---

# 26. The Pāṭala Translation Proof should be a first-class object

I'd make:

```text
TranslationProof
```

not merely:

```text
translation.score
```

Something like:

```text
TranslationProof
│
├── source_identity
│     ├ witness
│     ├ edition
│     └ source_hash
│
├── source_analysis
│     ├ segmentation candidates
│     ├ morphology
│     ├ syntax
│     └ compound analyses
│
├── alignment
│     ├ sentence
│     ├ word/span
│     ├ unaligned_source
│     └ unaligned_target
│
├── semantic_obligations
│     ├ negation
│     ├ modality
│     ├ scope
│     ├ quantification
│     ├ identity
│     ├ causality
│     └ argument roles
│
├── terminology
│     ├ lexical senses
│     ├ previous occurrences
│     └ parallel translations
│
├── independent_audits
│     ├ xCOMET
│     ├ GemSpanEval
│     ├ OTTAWA
│     ├ entailment
│     ├ term consistency
│     └ Sanskrit grammar
│
├── parallels
│     ├ commentary
│     ├ Tibetan
│     ├ Chinese
│     └ other translations
│
├── unresolved_issues
│
└── review
      ├ agent reviewers
      ├ scholar reviewers
      └ adjudication
```

Now we're talking.

---

# 27. Crucially, no single aggregate score

I would **not** produce:

```text
Translation quality = 94%
```

That hides too much.

Use a vector:

```text
SOURCE COVERAGE       0.99
TARGET GROUNDING      0.96
MORPHOLOGY            PASS
SYNTAX                PASS
NEGATION              PASS
MODALITY              PASS
TERM CONSISTENCY      WARN
SEMANTIC ENTAILMENT   WARN
XCOMET                 PASS
PARALLEL WITNESS      CONFLICT
HUMAN REVIEW           PENDING
```

Then:

```text
publication gate:
BLOCKED
reason:
PARALLEL_WITNESS_CONFLICT
```

That's dramatically more useful.

---

# 28. Different auditors should be intentionally redundant

The system I would build is:

```text
                       SANSKRIT
                          │
              ┌───────────┼─────────────┐
              │           │             │
              ▼           ▼             ▼
           ByT5       Heritage       Vidyut
              │           │             │
              └───────────┼─────────────┘
                          ▼
                  ANALYSIS LATTICE
                          │
                          ▼
                  candidate translation
                          │
          ┌───────────────┼─────────────────┐
          │               │                 │
          ▼               ▼                 ▼
       OTTAWA          xCOMET          GemSpanEval
    coverage/addition   MQM spans       MQM spans
          │               │                 │
          ├───────────────┼─────────────────┤
          │               │                 │
          ▼               ▼                 ▼
      entailment       terminology      rule checks
      source↔target     consistency     neg/scope/etc
          │               │                 │
          └───────────────┼─────────────────┘
                          ▼
                 cross-source parallels
                MITRA/commentaries/etc
                          │
                          ▼
                    REVIEW QUEUE
```

The independence matters.

If every auditor is another prompt to the same underlying model, you don't have independent verification.

---

# 29. The most important repo shortlist for translation

If I were making:

```text
research/translation/
```

I'd clone these first:

```text
https://github.com/xr843/fojin

https://github.com/Unbabel/COMET
https://github.com/bsc-lt/mt-evaluation
https://github.com/amazon-science/span-mt-metaeval
https://github.com/google-research/mt-metrics-eval
https://github.com/google/wmt-mqm-human-evaluation

https://github.com/neulab/awesome-align
https://github.com/bfsujason/bertalign

https://github.com/ambuda-org/dcs
https://github.com/OliverHellwig/sanskrit
https://github.com/hrishikeshrt/heritage
https://github.com/tylergneill/skrutable

https://github.com/ayushbits/saamayik
https://github.com/AI4Bharat/IndicTrans2
https://github.com/AI4Bharat/IndicLLMSuite

https://github.com/dharmamitra/mitra-parallel
```

And these papers beside them:

```text
https://arxiv.org/abs/2601.07314   Mitrasamgraha
https://arxiv.org/abs/2601.06400   MITRA

https://arxiv.org/abs/2409.13920   ByT5-Sanskrit
https://arxiv.org/abs/2511.08145   Sanskrit anvaya

https://arxiv.org/abs/2310.10482   xCOMET
https://arxiv.org/abs/2510.24707   MetricX-25 / GemSpanEval
https://arxiv.org/abs/2406.01919   OTTAWA
https://arxiv.org/abs/2405.09223   alignment preference

https://arxiv.org/abs/2605.24904   evaluator vs human audit
https://arxiv.org/abs/2505.01761   long-context judge failure
```

---

# 30. What I would build first in Pāṭala

Not a better translator.

A **Translation Audit Compiler**.

```text
patala translate-proof SOURCE TRANSLATION
```

producing:

```text
translation-proof.json
```

with:

```text
1. exact immutable source
2. Sanskrit analyses
3. alignment map
4. unaligned source spans
5. ungrounded English spans
6. grammatical obligations
7. term/sense decisions
8. negation/scope/modality checks
9. semantic-strength checks
10. parallel evidence
11. learned metric audit
12. disagreements
13. reviewer decisions
```

Then translation generation becomes interchangeable:

```text
Claude
GPT
Gemma-MITRA
IndicTrans
human scholar
future model
```

It doesn't matter nearly as much.

Because **the moat becomes the verifier**.

That is the translation analogue of the whole Pāṭala vision: future models will keep getting better at generating English, but the durable asset is the system that can say exactly **why this English is licensed by this Sanskrit, where that judgment came from, what remains uncertain, and who has verified it**.

[1]: https://arxiv.org/abs/2601.07314?utm_source=chatgpt.com "Mitrasamgraha: A Comprehensive Classical Sanskrit Machine Translation Dataset"
[2]: https://arxiv.org/abs/2601.06400?utm_source=chatgpt.com "MITRA: A Large-Scale Parallel Corpus and Multilingual Pretrained Language Model for Machine Translation and Semantic Retrieval for Pāli, Sanskrit, Buddhist Chinese, and Tibetan"
[3]: https://github.com/xr843/fojin?utm_source=chatgpt.com "GitHub - xr843/fojin: Buddhist Digital Text Platform — 10,500+ texts, 613 sources, trilingual cross-canon, AI Q&A (RAG), knowledge graph, full-text search · GitHub"
[4]: https://arxiv.org/abs/2409.13920?utm_source=chatgpt.com "One Model is All You Need: ByT5-Sanskrit, a Unified Model for Sanskrit NLP Tasks"
[5]: https://github.com/hrishikeshrt/heritage?utm_source=chatgpt.com "GitHub - hrishikeshrt/heritage: Heritage.py -- Python Interface to The Sanskrit Heritage Site · GitHub"
[6]: https://github.com/tylergneill/skrutable?utm_source=chatgpt.com "GitHub - tylergneill/skrutable: Toolkit for manipulating Sanskrit text with Python · GitHub"
[7]: https://github.com/OliverHellwig/sanskrit?utm_source=chatgpt.com "GitHub - OliverHellwig/sanskrit: Data for the quantitative study of (Vedic) Sanskrit · GitHub"
[8]: https://github.com/ambuda-org/dcs?utm_source=chatgpt.com "GitHub - ambuda-org/dcs: Sanitized data from the Digital Corpus of Sanskrit · GitHub"
[9]: https://github.com/Unbabel/COMET?utm_source=chatgpt.com "GitHub - Unbabel/COMET: A Neural Framework for MT Evaluation · GitHub"
[10]: https://arxiv.org/abs/2510.24707?utm_source=chatgpt.com "MetricX-25 and GemSpanEval: Google Translate Submissions to the WMT25 Evaluation Shared Task"
[11]: https://arxiv.org/abs/2406.01919?utm_source=chatgpt.com "OTTAWA: Optimal TransporT Adaptive Word Aligner for Hallucination and Omission Translation Errors Detection"
[12]: https://github.com/neulab/awesome-align?utm_source=chatgpt.com "GitHub - neulab/awesome-align: A neural word aligner based on multilingual BERT · GitHub"
[13]: https://github.com/topics/translation-memory?utm_source=chatgpt.com "translation-memory · GitHub Topics · GitHub"
[14]: https://arxiv.org/abs/2405.09223?utm_source=chatgpt.com "Word Alignment as Preference for Machine Translation"
[15]: https://arxiv.org/abs/1911.00681?utm_source=chatgpt.com "Machine Translation Evaluation using Bi-directional Entailment"
[16]: https://github.com/google/wmt-mqm-human-evaluation?utm_source=chatgpt.com "GitHub - google/wmt-mqm-human-evaluation · GitHub"
[17]: https://arxiv.org/abs/2605.24904?utm_source=chatgpt.com "Quantifying the Impact of Translation Errors on Multilingual LLM Evaluation"
[18]: https://arxiv.org/abs/2505.01761?utm_source=chatgpt.com "Same evaluation, more tokens: On the effect of input length for machine translation evaluation using Large Language Models"
[19]: https://github.com/langtech-bsc/mt-evaluation?utm_source=chatgpt.com "GitHub - langtech-bsc/mt-evaluation: A framework for evaluating Machine Translation models. · GitHub"
[20]: https://github.com/amazon-science/span-mt-metaeval?utm_source=chatgpt.com "GitHub - amazon-science/span-mt-metaeval · GitHub"
[21]: https://github.com/google-research/mt-metrics-eval?utm_source=chatgpt.com "GitHub - google-research/mt-metrics-eval: Tools for evaluating the performance of MT metrics on data from recent WMT metrics shared tasks. · GitHub"
[22]: https://github.com/ayushbits/saamayik?utm_source=chatgpt.com "GitHub - ayushbits/Saamayik: Source code and dataset for the paper 'Saamayik: A Benchmark and Dataset for English-Sanskrit Translation' · GitHub"
[23]: https://github.com/ai4bharat/IndicTrans2?utm_source=chatgpt.com "GitHub - AI4Bharat/IndicTrans2: Translation models for 22 scheduled languages of India · GitHub"
[24]: https://github.com/AI4Bharat/IndicLLMSuite?utm_source=chatgpt.com "GitHub - AI4Bharat/IndicLLMSuite: A blueprint for creating Pretraining and Fine-Tuning datasets for Indic languages · GitHub"
[25]: https://arxiv.org/abs/2511.08145?utm_source=chatgpt.com "Still Not There: Can LLMs Outperform Smaller Task-Specific Seq2Seq Models on the Poetry-to-Prose Conversion Task?"

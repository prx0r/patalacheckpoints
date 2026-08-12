# Project 00 — Autonomous Translation Factory

## Objective
Build the missing bridge in the current repo: `RAW_SANSKRIT → canonical auditable L0`. Do not begin with beautiful book translation. First make the machine produce source-linked word/phrase analysis with explicit uncertainty.

Current Pāṭala surfaces:
- https://github.com/prx0r/patala/blob/agent2/pipeline/corpus_state.py
- https://github.com/prx0r/patala/blob/agent2/pipeline/model.py
- https://github.com/prx0r/patala/blob/agent2/docs/BUILD_NOTES_L0_P0.md
- https://github.com/prx0r/patala/blob/agent2/skills/translate-work/SKILL.md
- https://github.com/prx0r/patala/blob/agent2/skills/translate-passage/SKILL.md

`corpus_state.py` already encodes the architectural gap: AND_GLOSS is supported; RAW_SANSKRIT requires a source-L0 mode.

## Reuse, do not rebuild

### Vidyut
https://github.com/ambuda-org/vidyut

Use as the primary linguistic witness for segmentation, morphology, sandhi/prakriyā and lexical infrastructure. Pāṭala owns the selected reading, disagreement state, provenance and review—not Sanskrit morphology itself.

### Sanskrit Heritage / Heritage.py
https://github.com/hrishikeshrt/heritage
https://sanskrit.inria.fr/

Use as an independent analysis witness. Preserve disagreement rather than collapsing two analyzers to one “confidence.”

### SanskritShala
https://arxiv.org/abs/2302.09527
https://arxiv.org/abs/2308.08807

Its task decomposition is directly useful: word segmentation, morphology, dependency parsing, compound identification, human correction. Reuse datasets/models where licensing permits; do not promote neural output directly to accepted Pāṭala state.

### Sanskrit corpora / retrieval
https://github.com/ambuda-org/dcs
https://github.com/cltk/sanskrit_text_dcs
https://github.com/ambuda-org/gretil
https://github.com/ambuda-org/ambuda
https://github.com/ambuda-org/data
https://github.com/AI4Bharat/indicnlp_catalog
https://github.com/tylergneill/skrutable

Use for lexical/construction retrieval and difficult-case evidence. Prevent exact target-translation leakage in benchmark runs.

### New 2026 Sanskrit MT resources
Mitrasamgraha:
https://arxiv.org/abs/2601.07314

MITRA:
https://arxiv.org/abs/2601.06400

Mitrasamgraha provides a very large Classical Sanskrit-English corpus and makes generic Sanskrit MT less differentiating. It explicitly leaves compounds and philosophical concepts difficult—exactly where Pāṭala should specialize. MITRA is valuable later for multilingual parallel mining and Buddhist cross-language retrieval.

## RAW-L0 record
Each record should preserve:
- exact source span;
- surface form;
- selected segmentation plus alternatives;
- selected lemma/morphology plus Vidyut/Heritage raw witnesses;
- compound analysis;
- literal word/phrase gloss;
- evidence refs;
- independent statuses per dimension;
- `review_state: MACHINE_PROPOSED`.

Do not force 1 Sanskrit token = 1 English word. Compounds and constructions need constituent analysis plus phrase-level English.

## Proof ladder
1. P0 SOURCE: source span, coverage, ordering, roundtrip.
2. P1 SEGMENTATION.
3. P2 MORPHOLOGY.
4. P3 LEXICAL/GLOSS.
5. P4 ALIGNMENT.
6. P5 SYNTAX only when downstream failure proves it necessary.

A P0 pass never proves semantic correctness.

## Best experiment: Sanskrit-only IPVV replay
Hide existing English for held-out IPVV spans. Give the agent Sanskrit + approved analyzers/lexica, then regenerate L0.

Measure:
- exact source coverage;
- segmentation F1;
- lemma/morphology accuracy;
- compound analysis;
- literal-gloss expert acceptance;
- polarity/negation preservation;
- false-certainty rate;
- abstention usefulness.

False certainty should be a top-line metric.

## Agent loop
`source → Vidyut → Heritage → historical retrieval → Agent 3 proposal → adversarial check → revise/abstain → deterministic audit → MACHINE_PROPOSED L0`.

## Build order
F0 `pipeline/raw_l0.py` for one passage.
F1 attach analyzer witnesses.
F2 preserve existing P0 verifier; add semantic checks separately.
F3 Sanskrit-only IPVV replay.
F4 review 50–100 difficult/error-cluster cases.
F5 first cross-work run on Kramasadbhāva.
F6 only then enable bounded passage/chunk batch scheduling.

## Set-it-loose certificate
Before unattended batching report:
- P0 coverage / bad spans / unknown chars;
- segmentation and morphology metrics;
- gloss acceptance;
- false-certainty and abstention metrics;
- hard-failure rate;
- model cost per 1k Sanskrit tokens;
- human review minutes per 1k Sanskrit tokens.

The real optimization target is review burden, not merely API cost.

# PĀṬALA — Full Vision / Moat / Product Audit
Date: 2026-08-13
Scope: consolidated checkpoint repo `prx0r/patalacheckpoints`, with emphasis on unseen canonical vision, functionality, economics, source-evidence, benchmark, corpus/kernel and review-engine files.

## Executive conclusion

Pāṭala is no longer best understood as a Sanskrit translation project, a RAG system, a Tantra website, or even an AI peer-review app.

The coherent system underneath the repo is:

> **A scholarly intelligence infrastructure whose technical kernel is a versioned, provenance-bearing epistemic dependency graph, whose institutional moat is accumulated expert judgment, correction history, source authority/rights, and adoption of stable scholarly identities.**

The most valuable native capability is not generation. It is **epistemic conservation**:
- exact source identity survives upward;
- interpretation stays distinguishable from source;
- attribution and scope survive paraphrase;
- arguments remember what they depend on;
- reviews mutate state without erasing history;
- downstream consequences can be recomputed.

The strongest first commercial/scholar wedge is not a giant Workbench. It is a closed loop:

```text
AUTONOMOUS FACTORY
    ↓
HARD CASES
    ↓
PĀṬALA BENCHMARK
    ↓
TRANSLATION AUDIT
    ↓
SCHOLAR CORRECTIONS
    ↓
NEW GOLD + REVIEW EVENTS
    ↓
BETTER FACTORY / AUDIT
```

That loop is a miniature of the whole company.

---

# 1. What is actually Pāṭala-native

The repo's own reuse doctrine is right: own only what generic scholarly/NLP infrastructure does not already provide.

## 1.1 Irreducible epistemic kernel

### Identity
- stable Pāṭala IDs
- Work / Witness / CanonicalPassage / SourceSpan / ObjectVersion
- external IDs as crosswalks, never replacements

### Source-side epistemics
- SourceAssertion
- TranslationDecision
- PhilologicalProof
- SemanticAlignment
- term/sense decisions

### Reasoning-side epistemics
- Proposition with derivation provenance
- Commitment
- Inference
- Argument
- DebateFrame
- Defeater / Attack
- Crux

### Authority / review
- ReviewEvent
- immutable review history
- reviewer identity + scope + object version
- abstention
- supersession
- adjudication state

### Dependency
- explicit typed dependency edges
- deterministic DerivedState
- ImpactReport
- stale/reconsideration propagation

That is the actual technical constitution.

---

# 2. What is the moat?

The moat is compound, not singular.

## 2.1 Computational moat
The fine-grained epistemic graph:

```text
source span
→ reading
→ translation decision
→ proposition
→ inference
→ argument
→ synthesis
→ public claim
```

with typed dependencies and revision propagation.

This is the part generic RAG does not provide.

## 2.2 Data moat
Not "a Sanskrit corpus."

The high-value data is:
- difficult expert-adjudicated cases;
- machine failure cases;
- alternative readings;
- reasons for rejection;
- scope/attribution corrections;
- historical term senses;
- argument reconstructions;
- review histories;
- counterfactual impact data.

The strongest dataset is therefore the **executable-corrections dataset**:

```text
source
→ machine proposal
→ critique
→ alternatives
→ human judgment
→ corrected object
→ downstream consequences
```

## 2.3 Institutional moat
- expert network;
- named reviewer histories;
- ORCID-linked credit;
- scholar reputation / authority;
- institutional partnerships;
- unique manuscript access;
- legitimate digitization/training/redistribution rights;
- brand trust.

## 2.4 Adoption moat
Stable IDs and machine interfaces become increasingly valuable once external agents cite/resolve Pāṭala objects.

The endgame is not "users visit our website."
It is:

```text
outside AI/researcher says X
→ resolve X through Pāṭala
→ exact source + interpretation + review history appears
```

When that becomes normal, Pāṭala becomes infrastructure.

---

# 3. The single most important conceptual idea

## Executable corrections

This is the strongest idea in the repo.

Normal scholarship:

```text
paper v1
reviewer writes prose
author changes paper
old reasoning disappears into history
```

Pāṭala:

```text
ReviewEvent
→ exact target version
→ decision + rationale + evidence
→ supersession
→ deterministic state recomputation
→ affected inferences / conclusions / syntheses identified
→ future agents inherit correction
```

This is genuinely stronger than "AI reviewer."

It means expert judgment becomes **machine-actionable institutional memory**.

Protect this architecture.

---

# 4. The second most important idea

## Derivational propositions

A proposition must remember what kind of object it is.

These must never collapse:

```text
AUTHOR EXPLICITLY ASSERTS X
EDITOR PARAPHRASES X
PĀṬALA RECONSTRUCTS X
X IS REQUIRED AS AN IMPLICIT PREMISE
OPPONENT ASSERTS X
MODERN SCHOLAR ATTRIBUTES X
```

That distinction is more foundational than any single logic engine.

A huge fraction of AI scholarship errors are really derivation/attribution failures.

---

# 5. The third most important idea

## Argument-under-a-frame

The semantic-commensurability docs are among the most important in the repo.

Before saying A contradicts B:

1. same debate frame?
2. same target?
3. same term sense?
4. same explanatory level?
5. same scope/modality?
6. only then contradiction?

This prevents fake conflict.

Pāṭala should treat:
- genuine contradiction;
- scope mismatch;
- conceptual mismatch;
- different question;
- non-comparability

as distinct first-class outputs.

This is much more valuable than a generic "argument graph."

---

# 6. What should be external infrastructure?

Pāṭala should aggressively reuse.

## Sanskrit / primary text
- Vidyut — morphology, segmentation, lexical machinery
- Sanskrit Heritage — independent morphology witness
- SanskritShala — task decomposition / model/data precedent
- Ambuda / DCS / GRETIL — corpus retrieval witnesses
- TEI — critical-edition/manuscript interchange
- CTS-compatible identity — canonical text/passages
- DTS — external text retrieval API
- IIIF — images/manuscript/page assets

## Modern scholarship ingestion
- GROBID — PDF → structured extraction witness
- Docling — non-PDF / richer document extraction
- JATS — consume publisher XML when available
- Zotero — bibliography CRUD/sync/citation management
- Crossref / OpenAlex / OpenCitations — metadata/citation witnesses
- Unpaywall — OA discovery
- RO-Crate — packaging/export
- W3C Web Annotation — resilient span selection
- PROV-O — generic provenance semantics
- CiTO — publication citation relations
- ORCID — researcher identity
- ROR — organization identity
- DataCite/Crossref — public identifiers/review artifacts

## Retrieval / research support
- PaperQA2 — candidate evidence retrieval
- Tantivy BM25 — lexical baseline
- broad literature tools — discovery, not epistemic authority

## Annotation / review workflow
- INCEpTION — gold/adjudication lab
- Hypothesis/Recogito concepts — annotation UX
- OpenReview/Kotahi/Janeway/PubPub — generic publication/review workflow
- COAR Notify — external review-event interoperability

## Evaluation
- Inspect AI — benchmark runtime
- mt-metrics-eval — metric statistics
- xCOMET / MetricX — baselines / error-shape inspiration
- FEVER / SciFact / CLAIM-BENCH / CLAIMCHECK — benchmark precedents
- xAIF / oAMF — argument interchange adapters

## Execution
- Hermes — replaceable agent/runtime layer
- model providers — replaceable

The rule:

> **External systems can own execution and generic structure. Pāṭala owns warranted authority and the dependency semantics between scholarly judgments.**

---

# 7. What Pāṭala should NOT build

Do not build:
- a Sanskrit morphology engine;
- a journal management platform;
- ORCID;
- DOI infrastructure;
- a global citation graph;
- a generic PDF parser;
- a generic annotation backend;
- a generic vector search product;
- a generic LLM eval framework;
- a generic argument ontology;
- a general academic search engine;
- a giant bespoke agent runtime;
- a single universal "quality score."

If a mature external tool can be swapped out without changing Pāṭala IDs or epistemic objects, that is good architecture.

---

# 8. First real products

## Product 0 — Autonomous Translation Factory
This is internal infrastructure, not the public wedge.

Purpose:
- RAW Sanskrit → canonical auditable L0;
- source coverage;
- morphology witnesses;
- explicit ambiguity;
- machine-proposed gloss/translation;
- fail-closed verification.

Why first:
The rest of the stack needs repeated difficult source objects.

The factory creates the raw material for benchmarks and audits.

Success metric is not throughput alone.

Track:
- review minutes per 1k tokens;
- false-certainty rate;
- abstention usefulness;
- source coverage;
- morphology disagreement;
- cost;
- hard failure rate.

---

## Product 1 — PĀṬALA-IPVV Benchmark

This is the first strategic asset.

Do not position it as:
"another Sanskrit MT benchmark."

Position it as:

> **expert-adjudicated evaluation of difficult premodern Sanskrit scholarship.**

Benchmark layers:

```text
T1 SOURCE
segmentation / morphology / syntax / alignment

T2 TRANSLATION
omission / addition / polarity / modality / agency / term sense

T3 INTERPRETATION
speaker / pūrvapakṣa / scope / rival reading / certainty

T4 ARGUMENT
proposition / commitment / inference / alignment / crux
```

Critical error taxonomy:
- OMISSION
- UNSUPPORTED_ADDITION
- POLARITY_NEGATION
- MODALITY
- AGENCY
- SYNTACTIC_ATTACHMENT
- COMPOUND_PARSE
- TECHNICAL_TERM_SENSE
- SPEAKER_ATTRIBUTION
- PURVAPAKSA_SIDDHANTA
- SCOPE
- CONCEPTUAL_DISTINCTION
- RIVAL_READING_IGNORED
- UNSAFE_CERTAINTY

Why this matters:
- establishes credibility;
- measures your own system honestly;
- gives AI labs something concrete;
- creates expert-review work;
- produces private eval assets;
- becomes the calibration layer for Audit.

Keep:
- public dev;
- public reproducibility slice;
- private locked official eval;
- fresh continually added cases.

Never expose all gold.

---

## Product 2 — Translation Audit

This is the best first scholar-facing product.

Job:
> "I translated this Sanskrit. Show me what is mechanically wrong, what may be wrong, and which findings are actually calibrated."

UI:
```text
SANSKRIT | TRANSLATION | FINDINGS
```

Tabs:
- Overview
- Alignment
- Terms
- Grammar
- Rival Readings
- Provenance

Three epistemic classes:

### v0 deterministic
Can ship first:
- source normalization;
- span resolution;
- coverage;
- alignment bookkeeping;
- omission/addition candidates;
- terminology consistency;
- provenance completeness.

### v1 model-proposed
- scope risk;
- attribution risk;
- polarity risk;
- rival parse;
- technical term mismatch.

Always clearly MACHINE_PROPOSED.

### v2 calibrated
Detector-by-detector only after:
- expert fixtures;
- held-out eval;
- false-positive measurement;
- threshold freeze.

High-value action:
**Attack this reading**

But never pretend the attack is authoritative until reviewed.

Why this is the best wedge:
- clear job-to-be-done;
- low onboarding;
- visible value in one passage;
- naturally creates scholar corrections;
- those corrections become benchmark cases;
- directly demonstrates Pāṭala's unique evidence depth.

---

# 9. Translation Audit should contain several "products" as modes

Do not launch separate apps for:

- Translation Comparison
- Term Audit
- Adversarial Translation Review
- Proof Certificate

These are modes/artifacts of the same Audit substrate.

## Compare Readings
Same Sanskrit + A/B/C:
- agreement;
- substantive divergence;
- term-policy differences;
- scope differences;
- interpretive consequences;
- source support.

## Term Audit
For `vimarśa`, `śakti`, etc:
- every occurrence;
- morphology;
- candidate sense;
- historical context;
- renderings;
- drift;
- justified exceptions;
- unresolved cases.

## Attack This Reading
Generate strongest rival analysis and show exact source-dependent consequences.

## Proof bundle
Audit output can export an auditable certificate.
Do not make the certificate a separate product.

---

# 10. Product 3 — Pāṭala Review

This is probably the strongest eventual scholar product, but should come after Audit/Benchmark maturity.

Input:
- article;
- chapter;
- thesis section;
- translation study.

Compiler stages:

```text
ingest
→ claims
→ citation resolution
→ source grounding
→ argument reconstruction
→ commitment / attribution
→ counterevidence
→ semantic alignment
→ dependency tracing
→ crux analysis
→ critique validation
```

Output should look like compiler diagnostics:

```text
ERROR
quoted passage not found

WARNING
claim attributes opponent position to author

WARNING
conclusion depends on OPEN translation decision

INFO
rival reading preserves source but narrows scope

CRUX
removing premise P destroys the only support chain for C
```

Never:
`72/100 paper quality`.

The defensible feature is:
**every criticism resolves to exact evidence and dependency structure.**

---

# 11. Product 4 — Scholar Workbench

This is not the wedge.

It is the eventual lock-in environment.

The unit of scholarship becomes:

```text
ResearchQuestion
→ Evidence
→ Readings
→ Terms
→ Propositions
→ Positions
→ Arguments
→ Counterevidence
→ Cruxes
→ Review history
→ Outputs
```

The key interaction is not generic AI chat.

It is typed scholar action:

- ADD_EVIDENCE
- PROPOSE_TRANSLATION
- PROPOSE_TERM_SENSE
- PROPOSE_PROPOSITION
- ATTRIBUTE_COMMITMENT
- ADD_SUPPORT
- ADD_ATTACK
- ADD_RIVAL_READING
- MARK_SCOPE
- OPEN_QUESTION
- ACCEPT
- REJECT
- REVISE
- ABSTAIN

That event stream is strategically valuable.

Build Workbench only after the graph is rich enough that scholars gain more than they lose by leaving Word/Obsidian.

---

# 12. Consumer product

The consumer Tantra Hub remains useful, but it should be downstream.

Its mission:
> **Make the textual landscape of Tantra navigable.**

The consumer surface should expose:
- traditions;
- texts;
- timelines;
- Sanskrit;
- translations;
- bibliography;
- manuscripts;
- scholarship;
- commentary;
- relations;
- accessible explainers.

But the core rule remains:
consumer UX can simplify machinery, but **meaningful uncertainty must survive projection**.

Do not hide:
- genuine dispute;
- unresolved reading;
- contested attribution;
- uncertain dating.

Hide implementation detail, not epistemic state.

---

# 13. The full flywheel

```text
                 SOURCES
                    ↓
            AUTONOMOUS FACTORY
                    ↓
           MACHINE PROPOSALS
                    ↓
             PĀṬALA AUDIT
                    ↓
            SCHOLAR JUDGMENT
                    ↓
      IMMUTABLE REVIEW / CORRECTION
                    ↓
        EXECUTABLE DEPENDENCY UPDATE
                    ↓
     BENCHMARK / TRAINING / EVAL CASE
                    ↓
         BETTER MODEL + BETTER AUDIT
                    ↓
      LOWER SCHOLAR REVIEW BURDEN
                    ↓
          HARDER QUESTIONS BECOME
               ECONOMICALLY VIABLE
```

This is the strongest business/research loop in the project.

---

# 14. What is "goated"

The genuinely exceptional ideas in the repo are:

1. **Executable corrections**
2. **Derivational propositions**
3. **Commitment / speaker-state tracking**
4. **Argument-under-a-frame**
5. **Semantic commensurability before contradiction**
6. **Crux as counterfactual dependency**
7. **Audit findings with epistemic classes rather than AI confidence**
8. **The anti-theatre doctrine**
9. **Evaluation plane separated from production graph**
10. **Stable primary-text identity + source-spans + provenance**
11. **External standards as adapters, never ontology masters**
12. **Expert judgment as structured institutional memory**
13. **False certainty / abstention as top-line metrics**
14. **Review burden as factory optimization target**
15. **Products as projections of one core**

These should be protected from feature creep.

---

# 15. Important repo contradictions / implementation issues found in audit

## 15.1 Stale state-machine statement
`pipeline/corpus_state.py` says RAW_SANSKRIT L0 mode is "NOT YET BUILT", but the checkpoint contains:
- `raw_l0.py`
- `l0_worker.py`
- `auto_raw_l0.py`

So documentation/state transition code is stale relative to implementation.

Fix:
- update ledger semantics;
- distinguish "implemented", "validated", "production-ready."

Do not let stale comments control autonomous scheduling.

## 15.2 "VERIFIED" is overloaded
Some code uses `l0_status="VERIFIED"` when canonical files exist / deterministic checks pass.

But the doctrine reserves semantic caution.

Recommendation:
split:
- `SOURCE_INTEGRITY_PASS`
- `STRUCTURE_PASS`
- `MORPHOLOGY_WITNESSED`
- `SEMANTIC_REVIEW_PENDING`

Avoid generic `VERIFIED`.

## 15.3 Review engine prototype is conceptually stronger than enforcement
The review engine's model is excellent, but the prototype still needs hardening before public scholarly claims:
- reviewer independence;
- object-version existence validation;
- replacement-version binding;
- multi-reviewer uniqueness;
- adjudication authority;
- persistent ledger storage;
- concurrency;
- cryptographic/result lineage;
- scope ontology;
- reviewer credential/authorization model.

Do not market current test count as "peer review solved."

## 15.4 Existing graph model and newer epistemic IR risk duplication
`data/corpus/graph.ts` has generic Objects/Annotations while newer layers introduce:
- Proposition;
- Commitment;
- SourceAssertion;
- CorroborationEvent;
- ReviewEvent;
- DebateFrame;
- SemanticAlignment.

You need one canonical boundary.

Recommendation:
- identity objects stay generic;
- generic Annotation becomes extension mechanism only;
- epistemically meaningful types get explicit schemas;
- avoid burying critical semantics in `payload: Record<string, unknown>`.

## 15.5 Review states are fragmented
Repo contains variants such as:
- machine_proposed;
- checked;
- expert_reviewed;
- editorially_accepted;
- CANDIDATE;
- SINGLE_REVIEWED;
- DOUBLE_REVIEWED;
- ADJUDICATED;
- SCHOLARLY_CORROBORATED;
- SPAN_VERIFIED.

These describe different axes.

Do not make one enum do all jobs.

Freeze orthogonal axes:

```text
ORIGIN
machine / human / institution

SOFTWARE VALIDATION
unchecked / structural_pass / integrity_pass

EVIDENCE STATUS
unsupported / supported / conflict / underdetermined

REVIEW STATUS
unreviewed / single / double / adjudicated / specialist

PUBLICATION STATUS
draft / released / superseded / withdrawn
```

## 15.6 "Scholarly corroborated" needs strict semantics
Never allow:
`scholar wrote something similar`
to silently mean:
`Pāṭala accepts this proposition`.

Corroboration records:
- who;
- exact span;
- relation;
- independence;
- semantic alignment;
- defeaters;
- extraction/review status.

## 15.7 Consumer uncertainty rule needs correction
"Consumer never sees unresolved state" is unsafe.

Better:
> consumer never sees raw machinery, but meaningful uncertainty is preserved.

---

# 16. Recommended canonical architecture

```text
                 EXTERNAL SOURCE SYSTEMS
      GRETIL / Ambuda / PDFs / Manuscripts / JATS / TEI
                           │
                           ▼
──────────────────── IDENTITY / WITNESS ────────────────────
Work · Witness · Passage · Span · Person · Org · Rights
                           │
                           ▼
──────────────────── SOURCE / PHILOLOGY ────────────────────
PhilologicalProof · TranslationDecision · TermSense
                           │
                           ▼
──────────────────── INTERPRETATION ────────────────────────
SourceAssertion · Proposition · Commitment
                           │
                           ▼
──────────────────── REASONING ─────────────────────────────
ResearchQuestion · DebateFrame · SemanticAlignment
Inference · Argument · Attack · Defeater · Crux
                           │
                           ▼
──────────────────── AUTHORITY / HISTORY ───────────────────
ReviewEvent · ObjectVersion · Supersession · DerivedState
                           │
                           ▼
──────────────────── DEPENDENCY ENGINE ─────────────────────
ImpactReport · stale state · counterfactual recomputation
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
         AUDIT/REVIEW    API/MCP      CONSUMER
             │
             ▼
          WORKBENCH

──────────────────── EVALUATION PLANE ──────────────────────
Benchmarks / Inspect AI / private gold / fresh cases
tests production, never becomes its own authority
```

---

# 17. Canonical build doctrine

Before building any feature ask:

### Q1
Does a mature external project already solve the generic version?

If yes: integrate.

### Q2
Does this feature create or manipulate Pāṭala-native epistemic objects?

If no: probably do not build.

### Q3
What independent experiment would falsify the claimed capability?

If none: infrastructure only.

### Q4
What user consumes this object?

If no real consumer: likely ontology theater.

### Q5
Does this preserve uncertainty downward/upward?

If no: reject design.

---

# 18. Recommended near-term execution

## Phase A — Harden the factory
- resolve stale RAW-L0 state-machine semantics;
- clean `VERIFIED` naming;
- evaluate RAW-L0 on hidden IPVV;
- cross-work Kramasadbhāva;
- track false certainty and review burden;
- freeze canonical passage/source identity.

## Phase B — Build benchmark v0.1
Start with 50–100 truly difficult IPVV cases rather than thousands of easy passages.

Prioritize:
- omission;
- addition;
- negation;
- speaker;
- scope;
- technical sense;
- rival reading;
- argument extraction.

Keep private locked split immediately.

Use Inspect AI.

## Phase C — Ship Audit v0
One simple scholar interaction.

Input:
- Sanskrit;
- translation.

Output:
- deterministic source/coverage/alignment/term findings;
- provenance;
- unresolved state.

No grand semantic claims.

## Phase D — Add model-proposed Attack / Term / Compare modes
All proposals visibly remain proposals.

Capture every human response as ReviewEvent / benchmark candidate.

## Phase E — Publish State of AI Sanskrit
Evaluate major systems/models on the public + private benchmark.

This creates:
- legitimacy;
- outside interest;
- model-provider relevance;
- scholar recruiting;
- recurring benchmark identity.

## Phase F — Pāṭala Review
Start with native Pāṭala arguments, then Pāṭala-generated essays, then source-resolvable external papers.

Do not jump straight to arbitrary PDFs.

## Phase G — Workbench
Only after experts repeatedly use Audit/Review and you understand their workflow.

---

# 19. Business logic

The strongest commercial logic is not charging readers for translations.

Potential revenue:
- benchmark/evaluation services;
- enterprise model evaluation;
- API at scale;
- institutional research workspaces;
- translation audit;
- manuscript/source projects;
- paid specialist adjudication workflows;
- custom corpus curation;
- grants;
- philanthropy;
- sponsored critical editions;
- premium educational/media products later.

Open core data/interfaces can increase authority.
Scarce high-quality adjudication, private evals, institutional integrations, rights-cleared corpora and expert networks create defensibility.

---

# 20. One-sentence internal north star

> **Pāṭala turns scholarly claims into versioned, source-resolving, reviewable computational objects whose authority and dependencies can be inspected, challenged, corrected and propagated.**

Public-facing:

> **A computable scholarly tradition: every claim resolves to its source.**

Business-facing:

> **The trust and evaluation layer for AI-mediated scholarship in difficult historical traditions.**

Scholar-facing:

> **Evidence-visible philology and research review that turns corrections into reusable scholarly state.**

---

# 21. Final ranking

## Build/protect at all costs
1. stable IDs and source resolution
2. SourceAssertion
3. Proposition derivation
4. Commitment
5. SemanticAlignment / DebateFrame
6. ReviewEvent + immutable version history
7. dependency propagation
8. expert gold
9. benchmark/eval discipline
10. Audit feedback → gold loop

## Important but replaceable machinery
- Hermes
- model vendors
- morphology engines
- retrieval engines
- vector stores
- GROBID
- annotation tools
- review workflow apps
- frontend frameworks

## Valuable later projections
- Review
- Workbench
- Tantra Hub
- media
- courses
- AI teacher
- cross-tradition engine

## Avoid as premature expansion
- generic scholar social network
- journal platform
- new annotation backend
- global citation search
- custom PDF stack
- huge ontology
- universal philosophical theorem prover
- one "truth score"

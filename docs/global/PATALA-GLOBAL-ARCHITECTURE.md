Yes. At this point I would stop thinking of the vision docs as a collection of ideas and freeze a **Pāṭala Global Architecture v0.1** underneath all of them.

The repository already says there is one vision, not thirteen products: a single computable scholarly tradition whose evidence graph is rendered through different interfaces.  Vision 12 makes the same claim at the product level: one core, five permission-scoped surfaces.

There are also two documentation inconsistencies worth correcting in the eventual architecture commit:

* `CORE-BIBLE.md` still gives the abbreviated old spine `Sanskrit → L0 → translation → C1...`, whereas the canonical production stack is now `SOURCE → L0/L1 → L2 → L200 → C1 → THEMES → ...`.
* `hermes-execution.md` still mentions the retired `T1→L2→C1` translation path in its Vision-01 mapping.

Those should become downstream projections of this spec rather than parallel architectural authorities.

# PĀṬALA GLOBAL ARCHITECTURE v0.1

## 1. One sentence

> **Pāṭala is a versioned epistemic dependency graph over primary texts and scholarship, where external open infrastructure performs commodity scholarly work, Hermes performs replaceable execution, and Pāṭala owns the semantics of evidence, interpretation, argument, disagreement, review and downstream consequence.**

Everything else is a projection.

---

# 2. The seven architectural planes

```text
┌────────────────────────────────────────────────────────────┐
│ 7. PRODUCT SURFACES                                        │
│ Consumer · Scholar · Contributor · Reviewer · Developer    │
│ Benchmarks · Review · Assistant · Workbench · Education    │
└────────────────────────────┬───────────────────────────────┘
                             │
┌────────────────────────────▼───────────────────────────────┐
│ 6. PROJECTION / APPLICATION                                │
│ essays · courses · media · reports · benchmark tasks       │
│ audit views · research workspaces                          │
└────────────────────────────┬───────────────────────────────┘
                             │
┌────────────────────────────▼───────────────────────────────┐
│ 5. EPISTEMIC CORE — THE MOAT                               │
│ SourceAssertion · EvidenceUse · CorroborationEvent         │
│ Proposition · Commitment · DebateFrame                     │
│ SemanticAlignment · Argument · Attack · Crux               │
│ ArgumentSynthesis · ReviewEvent · ImpactReport             │
└────────────────────────────┬───────────────────────────────┘
                             │
┌────────────────────────────▼───────────────────────────────┐
│ 4. DOMAIN COMPILERS                                        │
│ Sanskrit: L0/L1 → L2 → L200 → C1 → THEMES                 │
│ Scholarship: Source → Witness → Span → SourceAssertion     │
└────────────────────────────┬───────────────────────────────┘
                             │
┌────────────────────────────▼───────────────────────────────┐
│ 3. SOURCE / RESEARCH SUBSTRATE                              │
│ stable IDs · bibliography · spans · witnesses · rights     │
│ search · provenance · external-ID crosswalks               │
└────────────────────────────┬───────────────────────────────┘
                             │
┌────────────────────────────▼───────────────────────────────┐
│ 2. EXECUTION / CONTROL                                     │
│ Pāṭala controller · registries · DAG · eligibility         │
│ validation · commit · staleness · certificates             │
│ Hermes = replaceable execution kernel                      │
└────────────────────────────┬───────────────────────────────┘
                             │
┌────────────────────────────▼───────────────────────────────┐
│ 1. BORROWED OPEN INFRASTRUCTURE                             │
│ GROBID · Docling · Zotero · PaperQA2 · OpenAlex            │
│ OpenCitations · Inspect · INCEpTION · Recogito · STORM     │
│ OpenReview/Kotahi · COAR Notify · Manubot · ORCID etc.     │
└────────────────────────────────────────────────────────────┘
```

The constitutional rule:

```text
Higher layers may depend on lower layers.

Lower layers must NEVER acquire epistemic authority
merely because a higher-layer tool says they should.
```

---

# 3. Plane 1 — commodity infrastructure: reuse aggressively

This is the “cheating” layer.

## Documents

```text
scholarly PDF     → GROBID
other documents   → Docling
bad citations     → AnyStyle fallback
```

Pāṭala should not implement document layout recognition, reference extraction or general file conversion.

## Bibliography / scholarly graph

```text
local bibliography     Zotero
DOI metadata            Crossref
global works/authors    OpenAlex
citation network        OpenCitations
OA locations            Unpaywall / existing PaperQA clients
people                  ORCID
institutions            ROR
projects                 RAiD
contribution roles      CRediT
```

Pāṭala owns crosswalks, not the world's bibliography.

## Research retrieval

```text
lexical/full-text       Tantivy
paper QA/RAG             PaperQA2
research expansion       SciRAG
perspective exploration  STORM / Co-STORM
```

These return **candidate evidence**.

They do not decide epistemic support.

## Annotation / adjudication

```text
benchmark gold       INCEpTION
Workbench selection  Recogito Text Annotator
public annotation    Hypothesis if useful
```

## Evaluation

```text
runtime              Inspect AI
logs/viewer          Inspect EvalLog/View
anti-cheat           Inspect Scanners
```

No custom benchmark framework.

## Scholarly workflow

```text
review workflows     OpenReview / Kotahi / Janeway
federation           COAR Notify
publishing           Manubot / PubPub
```

Pāṭala Review is **not** a journal-management system.

## Packaging/interchange

```text
corpora/benchmarks   RO-Crate
articles             JATS
critical texts       TEI
images/manuscripts   IIIF
text APIs            DTS
canonical citations  CTS-compatible
argument export      xAIF later
claim publishing     nanopubs later
```

Adapters only.

---

# 4. Plane 2 — execution architecture

There should be exactly **one autonomous controller**.

```text
Hermes cron
    ↓
patala-controller tick
    ↓
read registries / epistemic DAG
    ↓
deterministically determine eligible jobs
    ↓
dispatch bounded execution
    ↓
validate
    ↓
commit / fail / review-required
```

Hermes owns:

```text
processes
model invocation
cron
kanban
profiles
skills deployment
timeouts
tool calls
worktrees
```

Pāṭala owns:

```text
object identity
eligibility
input hashes
canonical state
epistemic status
immutability
supersession
dependency invalidation
review policy
```

The repo's Hermes doctrine already says Hermes is replaceable and the epistemic graph/review engine remain Pāṭala-owned.

Critical invariant:

```text
Hermes task DONE ≠ Pāṭala object ACCEPTED
```

---

# 5. Plane 3 — minimal universal source substrate

> **The Atlas upgrade (Vision 15).** This plane is where the **Pāṭala Atlas / Sanskrit Research Graph**
> lives — the authoritative identity/provenance layer the factory is downstream of. Keep the *universal
> substrate* minimal (below), but frame it as the Atlas: `Work / Edition / Witness / Surrogate /
> Transcription / E-text / Source` kept **distinct** (never collapse identity into one boolean), with
> authority evidence per record. Layering: **Atlas** (what exists + which version/witness) → **Factory**
> (what can we derive?) → **Epistemic Core** (what is supported?). See
> `docs/vision/vision-15-patala-atlas-sanskrit-research-graph.md`.

Keep this tiny.

```text
Source
Witness
Span
Asset
ExternalIdentifier
```

That's basically it.

### `Source`

Intellectual/bibliographic object.

### `Witness`

Concrete representation:

```text
PDF
OCR
JATS
HTML
TEI
scan
```

### `Span`

Stable target inside a witness:

```text
human locator
machine locator
text quote
hash
```

### `Asset`

Figure/table/image/audio/etc.

### `ExternalIdentifier`

```text
DOI
OpenAlex
Zotero
ORCID
ROR
CTS
ISBN
etc.
```

No giant custom bibliographic ontology.

---

# 6. Plane 4A — primary-text compiler

This must now be canonical everywhere:

```text
SOURCE
  ↓
L0/L1
  ↓
L2 READ
  ↓
L200 AUDIT
  ↓
C1
  ↓
THEMES
```

Semantics:

### L0/L1

> What exactly is physically/linguistically present?

Losslessness, tokens, morphology, controlled translation.

### L2

> What does the text say in readable language?

### L200

> How was that reading derived?

This is the **proof-carrying seam**:

```text
MaterialTranslationDecision
InterpretiveAssertion
derivation map
source-layer attribution
cross-reference
open item
review state
```

### C1

> What is this passage saying/doing?

Passage-local interpretation.

### THEMES

> How does an idea develop across passages/work?

Machine proposals, never “cluster = accepted theme.”

---

# 7. Plane 4B — scholarship compiler

Separate path:

```text
Publication
     ↓
Witness
     ↓
Span
     ↓
SourceAssertion
```

The key native object:

```text
SourceAssertion
```

means:

> Actor A, at exact span S, commits to/attributes/denies proposition P under scope Q.

Not merely:

> similar words occur here.

This is where raw RAG becomes usable evidence.

---

# 8. The convergence point

The primary-text path and scholar-literature path meet here:

```text
PRIMARY TEXT                       SCHOLARSHIP

L200 / C1                          SourceAssertion
    │                                   │
    ▼                                   ▼
 Proposition ◀────── EvidenceUse / CorroborationEvent
    │
    ▼
 Argument
```

This is the center of Pāṭala.

---

# 9. Plane 5 — the actual Pāṭala-native ontology

I would freeze the native core around roughly these objects.

## Evidence

```text
SourceAssertion
EvidenceUse
CorroborationEvent
Derivation
```

## Semantics

```text
Proposition
Commitment
SemanticAlignment
EpistemicRegime
DebateFrame
```

## Reasoning

```text
InferenceRule
InferenceApplication
Argument
Attack
Preference
Crux
ArgumentSynthesis
```

## Human correction

```text
ReviewEvent
Adjudication
Supersession
ImpactReport
```

## Authority dimensions

Do not use one scalar ladder.

Use at least:

```text
generation_status
evidence_status
review_status
publication_status
```

Example:

```json
{
  "generation_status": "ENGINEERING_VALIDATED",
  "evidence_status": "SCHOLARLY_CORROBORATED",
  "review_status": "NOT_INDEPENDENTLY_REVIEWED",
  "publication_status": "PUBLIC"
}
```

Much cleaner.

---

# 10. The universal dependency rule

Every meaningful object stores explicit dependencies:

```text
object
  depends_on [
    object/version,
    relation,
    load_bearing?,
    epistemic_role
  ]
```

Then correction works automatically.

```text
L2 v3 superseded
     ↓
L200 stale
     ↓
C1 stale
     ↓
Proposition maybe stale
     ↓
Argument maybe stale
     ↓
Synthesis maybe stale
     ↓
Essay/Education affected
```

That is probably Pāṭala's single most important systems property.

---

# 11. Plane 6 — projections

These should be **loss-constrained renderers**, not new knowledge-generation silos.

```text
ArgumentSynthesis
    ├─ Essay
    ├─ Review report
    ├─ Lesson
    ├─ FAQ
    ├─ video script
    ├─ glossary
    └─ AI answer
```

Invariant:

[
authority(projection) \leq authority(parent)
]

and:

[
content(projection)
\subseteq
content(parent) \cup grounded\ additions
]

This unifies Agent 1's epistemic conservation work with the media/education visions.

---

# 12. Plane 7 — five product surfaces

Vision 12 already gives the right split.

## Consumer

```text
Reader
Tantra Hub
Atlas
Learning
AI teacher
Essays
Media
```

Read-only projection of sufficiently qualified objects.

## Scholar

```text
Translation Audit
Compare Readings
Term Audit
Pāṭala Review
Thesis Stress Test
Scholar Assistant
Explore / Perspective Collector
```

## Contributor

```text
source acquisition
manuscript upload
transcription
edition contribution
translation proposal
```

## Developer

```text
API
MCP
DTS adapter
benchmark API
BYOA
```

## Reviewer

```text
review queue
claim adjudication
translation adjudication
crux resolution
promotion decisions
credit
```

Same graph underneath all five.

---

# 13. Apply the architecture to every Vision

## Vision 01 — Translation laboratory

**Pāṭala owns**

```text
L0/L1/L2/L200/C1 contracts
validators
registries
source dependency
```

**Reuse**

```text
Hermes execution
Vidyut/Heritage morphology
existing model APIs
TEI/DTS adapters
```

**Proof**

L0 certificate → L200 certificate → C1 certificate.

---

## Vision 02 — Tantra Hub

**Pāṭala owns**

```text
read projections
source resolver
graph relationships
```

**Reuse**

```text
Zotero bibliography
CSL formatting
Recogito annotation
IIIF where needed
```

Do not build a bibliography manager.

---

## Vision 03 — one infrastructure, many interfaces

This becomes the **seven-plane architecture itself**.

No separate implementation.

---

## Vision 04 — economics/moat

The repo says expert corrections and provenance are the scarce compounding assets.

Architecture implements that as:

```text
ReviewEvent
+
Contributor identity
+
downstream dependency/usage graph
```

Reuse:

```text
ORCID
CRediT
RAiD
Crossref
Open Collective/payment provider later
```

---

## Vision 05 — five-year strategic window

Not software.

It determines prioritization:

```text
build hard-to-copy data
before generic AI makes generation irrelevant
```

Therefore certificates/benchmarks/review data outrank UI polish.

---

## Vision 06 — Pāṭala Review

This vision calls for translation review, hostile reading, argument audit, thesis stress tests, dependency analysis, term audit and “research compiler” behavior.

Architecture:

```text
paper
↓
GROBID/Docling
↓
SourceAssertions / candidate propositions
↓
PaperQA2/SciRAG counterevidence
↓
Argument reconstruction
↓
Nyāya/contextual audit
↓
Crux discovery
↓
ReviewReport
```

Reuse workflow:

```text
OpenReview/Kotahi
COAR Notify
```

Pāṭala builds only the epistemic compiler.

---

## Vision 07 — New Scholar

The vision explicitly describes structured inquiry, perspective comparison, tension discovery and scholar-directed exploration.

Reuse:

```text
STORM/Co-STORM interaction model
PaperQA2 evidence retrieval
Recogito text selection
INCEpTION controlled annotation
```

Pāṭala supplies:

```text
real Positions
Commitments
Frames
Arguments
Cruxes
```

so the “mind map” becomes persistent scholarship rather than ephemeral chat.

---

## Vision 08 — Scholar economics

The vision calls for scoped bounties, ORCID/CRediT credit, editorial territory and durable attribution.

Reuse:

```text
ORCID
CRediT
RAiD
Crossref review DOI
Open Collective / Stripe/etc.
```

Pāṭala owns:

```text
who reviewed WHAT exact object
what judgment they made
what it affected
```

Never a global scholar score.

---

## Vision 09 — media/cross-tradition

Architecture:

```text
qualified epistemic objects
↓
controlled projections
↓
essay / lesson / audio / video
```

Reuse your existing rendering stack.

No media-side knowledge database.

---

## Vision 10 — partnerships

No major technical subsystem.

Pāṭala exposes:

```text
RO-Crate datasets
DTS APIs
MCP
benchmark reports
review outputs
institution-scoped projects
```

Partners plug into existing standards rather than bespoke exports.

---

## Vision 11 — Śiva before Abhinava

This is mostly **more corpus through the same compilers**.

Do not build “historical Śaivism architecture.”

Add:

```text
chronology relation
tradition relation
influence hypothesis
evidence grade
```

to generic graph primitives.

Reuse same factory.

---

## Vision 12 — multi-surface platform

Already solved by:

```text
one epistemic core
+
permissions
+
five render surfaces
```

No separate databases/codebases.

---

## Vision 13 — product portfolio

The current doctrine ranks benchmark + translation audit very highly.

Under this architecture:

### Translation Audit

```text
L0/L1/L2/L200 validators
+
corpus term retrieval
+
model-proposed rival reading
```

### Benchmark

```text
Inspect AI
+
Pāṭala datasets/scorers
```

### Pāṭala Review

epistemic compiler.

### Workbench

persistent graph editor/explorer.

Everything is one stack.

---

# 14. Benchmarks become a separate constitutional plane

Never produce benchmark gold from the graph being evaluated.

```text
                         PRODUCTION GRAPH
                              │
                              │ system under test
                              ▼
┌────────────────────────────────────────────────────┐
│                   EVALUATION PLANE                 │
│                                                    │
│ TantraFact                                         │
│ ArgumentBench                                      │
│ TranslationBench                                   │
│ CorroborationBench                                 │
│ PāṭalaQA                                           │
│ CitationBench                                      │
└────────────────────────────────────────────────────┘
```

Runtime:

```text
Inspect AI
```

Gold workflow:

```text
machine proposal
↓
INCEpTION adjudication/reference creation
↓
frozen benchmark
↓
Inspect
```

---

# 15. Benchmark family

I would define six, not dozens.

### TranslationBench

Tests:

```text
segmentation
omission/addition
negation
scope
referent
term sense
syntactic attachment
ambiguity
```

### ArgumentBench

```text
propositions
commitments
premise/conclusion
inference
boundary
abstention
```

### CorroborationBench

```text
claim → scholarly evidence relation
```

with hard negatives.

### TantraFact

```text
SUPPORTED
REFUTED
UNDERDETERMINED
```

plus exact failure layer:

```text
source
span
attribution
scope
warrant
conclusion
```

### CitationBench

Does claimed evidence actually support the cited claim?

### PāṭalaQA

Question → grounded answer with strict epistemic attribution.

That's enough.

---

# 16. The product feedback loop

This should be explicit in the architecture.

```text
Factory
   ↓
machine proposal
   ↓
Audit / Assistant / Review
   ↓
interesting failures
   ↓
benchmark candidates
   ↓
adjudication
   ↓
reference dataset
   ↓
better evaluation
   ↓
better factory / review system
```

And separately:

```text
Scholar correction
   ↓
ReviewEvent
   ↓
graph improves
   ↓
products improve
   ↓
more scholars use products
   ↓
more corrections
```

Those are Pāṭala's two compounding loops.

---

# 17. A single runtime contract for every generative skill

Every skill should have this shape:

```text
SKILL CONTRACT

INPUT TYPE
exact canonical refs

PRECONDITIONS
deterministic eligibility

MODEL PERMISSION
what may be inferred/proposed

OUTPUT TYPE
strict schema

ABSTENTION
explicit permitted outcome

VALIDATOR
non-model gate

AUTHORITY CEILING
maximum state this skill can produce

FAILURE STATE
what happens on timeout/malformed output

CERTIFICATE
benchmark required before scaling
```

Example:

```text
L200 skill

input:
  L0/L1 + L2 refs

model may:
  propose MT / IA / open items

model may not:
  rewrite source
  change L2
  accept own interpretation

max authority:
  MACHINE_PROPOSED

validator:
  Task-2 + provenance/ref checks

certificate:
  hidden L200 reference set
```

This makes skills portable across Hermes or another future runtime.

---

# 18. Global object namespace

I would standardize identifiers loosely now:

```text
pt:work:
pt:passage:
pt:witness:
pt:span:

pt:l0:
pt:l2:
pt:l200:
pt:c1:

pt:source-assertion:
pt:prop:
pt:argument:
pt:crux:
pt:synthesis:

pt:review:
pt:corroboration:
pt:impact:

pt:benchmark:
pt:fixture:
pt:run:

pt:person:
pt:org:
pt:project:
```

External IDs are properties/crosswalks.

Never make:

```text
OpenAlex W123
```

the canonical internal identity.

---

# 19. Three DAGs, not one

This should be explicit.

## Epistemic DAG

```text
evidence → proposition → argument → synthesis
```

## Derivation DAG

```text
source → L0 → L2 → L200 → C1 → projection
```

## Execution DAG

```text
job A → job B → job C
```

They overlap but are semantically distinct.

Hermes controls execution DAG.

Pāṭala owns epistemic + derivation DAGs.

---

# 20. Permissions

Vision 12's surfaces should map to capabilities, not app names.

```text
corpus:read
evidence:read
review:read

proposal:create
annotation:create

source:contribute
translation:propose

review:submit
review:adjudicate

publish:project
benchmark:run

admin:ontology
```

Machine agents:

```text
read + propose
```

never:

```text
adjudicate
```

unless explicitly implementing a non-authoritative simulated benchmark path.

---

# 21. Repository shape

I would move toward something like:

```text
patala/
├── core/
│   ├── ids/
│   ├── provenance/
│   ├── dependency/
│   ├── authority/
│   └── permissions/
│
├── source-evidence/
│   ├── resolver/
│   ├── assertions/
│   ├── corroboration/
│   ├── adapters/
│   └── docs/
│
├── translation/
│   ├── l0_l1/
│   ├── l2/
│   ├── l200/
│   └── c1/
│
├── philosophy/
│   ├── propositions/
│   ├── arguments/
│   ├── frames/
│   ├── cruxes/
│   └── synthesis/
│
├── review/
│   ├── events/
│   ├── impact/
│   └── adjudication/
│
├── evals/
│   ├── translation/
│   ├── argument/
│   ├── corroboration/
│   ├── tantrafact/
│   └── qa/
│
├── integrations/
│   ├── grobid/
│   ├── zotero/
│   ├── paperqa/
│   ├── inspect/
│   ├── inception/
│   ├── openreview/
│   └── ...
│
├── skills/
│   ├── l0/
│   ├── l2/
│   ├── l200/
│   ├── c1/
│   ├── scholar-corroborate/
│   └── adversarial-review/
│
└── surfaces/
    ├── consumer/
    ├── scholar/
    ├── reviewer/
    ├── contributor/
    └── developer/
```

This is conceptual; don't reorganize the repo yet just to satisfy it.

---

# 22. What **not** to build

This needs to be part of the spec.

```text
NO custom PDF parser
NO global bibliography DB
NO citation graph crawler
NO annotation framework
NO general benchmark runner
NO journal workflow
NO ORCID replacement
NO DOI system
NO full-text search engine from scratch
NO generic RAG framework
NO global researcher reputation score
NO generic payments/accounting stack
NO second epistemic database for another product surface
```

If a proposed feature falls into those classes, integration research comes first.

---

# 23. The genuinely hard research questions

Once the commodity systems disappear, the project gets wonderfully clear.

### R1

Can `SourceAssertion` faithfully recover what a scholar is **actually committing to**, including opponent attribution, qualification and scope?

### R2

Can Pāṭala reliably determine whether evidence supports a proposition without semantic strengthening?

### R3

Can arguments be reconstructed with high precision and useful abstention?

### R4

Can the system find the **minimal crux** whose resolution changes conclusion status?

### R5

Can authority and uncertainty survive:

```text
source
→ interpretation
→ argument
→ synthesis
→ prose
→ education
```

without laundering?

### R6

Can expert correction propagate correctly through the dependency graph?

Those six questions are much closer to Pāṭala's actual research contribution.

---

# 24. Near-term architecture milestones

I would now run **four parallel proof tracks**.

## Track A — Factory

```text
L0 certificate
↓
L200 fix/certificate
↓
C1 autonomous contract
```

## Track B — Source evidence

```text
GROBID/Zotero pilot
↓
SourceAssertion
↓
CorroborationEvent
↓
product resolver proof
```

## Track C — Evaluation

```text
Inspect integration
↓
port current Argument corruption tests
↓
TranslationBench v0
↓
CorroborationBench
```

## Track D — Scholar product

```text
PaperQA2 pilot
↓
Recogito highlight → ReviewProposal
↓
one adversarial review vertical
```

All four converge here:

```text
                PĀṬALA REVIEW v0

document / translation / thesis
              ↓
          evidence
              ↓
         propositions
              ↓
          arguments
              ↓
            crux
              ↓
     adversarial report
              ↓
       ReviewProposal
              ↓
        human action
              ↓
       ImpactReport
```

That would be the first product proving most of the vision simultaneously.

---

# 25. The architecture criterion for every future feature

Ask four questions.

```text
1. Is this commodity infrastructure?
   → reuse it.

2. Does this create a new canonical epistemic object?
   → justify it rigorously.

3. Is this merely another view of an existing object?
   → projection, not new storage.

4. How is the claimed capability empirically falsified?
   → benchmark/certificate before promotion.
```

If every agent follows that, Pāṭala should stop accumulating architectural weeds.

---

## The deepest simplification

The 13 visions reduce to:

```text
                 SOURCES
                    ↓
              INTERPRETATION
                    ↓
                 CLAIMS
                    ↓
                ARGUMENTS
                    ↓
                  CRUXES
                    ↓
                 REVIEW
                    ↓
              CORRECTIONS
                    ↓
                 USAGE
              ↙          ↘
         SCHOLARS       PRODUCTS
              ↘          ↙
               MORE TRUST
```

Everything outside that loop should be borrowed wherever possible.

Everything inside that loop is where Pāṭala should be uncompromising.

I would make this a new canonical document—probably `docs/architecture/PATALA-GLOBAL-ARCHITECTURE.md`—and then revise the vision index/Core Bible/Hermes map so each points downward to it rather than independently describing implementation. That would finally give future agents **one answer to “what are we actually building?”** while preserving all 13 vision docs as product/strategy lenses rather than competing architectures.

# Global Pāṭala Dev Plan — from current state to full platform

The cleanest way to organize everything now is around **one canonical scholarly graph**, with Agent 2 building the substrate and production machinery, Agent 1 defining and proving the epistemic semantics, and both converging at exact versioned objects.

The whole project becomes:

```text
AUTHORITY GRAPH
Work → Edition → Witness → EText → Source
                │
                ▼
FACTORY
SOURCE → T1 → L0 → ARGMAP → L2 → L200 → C1
                │
                ▼
EPISTEMIC CORE
Proposition → Argument → Crux → ArgumentSynthesis
                │
                ▼
HUMAN AUTHORITY
ReviewEvent → Proposal → Adjudication → supersession
                │
                ▼
PROJECTIONS
Review / Essay / Education / API / Media
```

The key division:

```text
AGENT 2 = BUILD + MATERIALIZE + RUN
AGENT 1 = DEFINE + EVALUATE + PROVE
```

Neither should independently invent shared schemas anymore.

---

# Phase 0 — current blockers

## G2 — close the real correction loop

### Agent 2

Consume Agent 1's frozen T1/L0 findings.

```text
EvaluationFinding
→ worker fix
→ targeted rebuild
→ supersession
→ dependency invalidation
→ new T1/L0
→ EvaluationCandidate
```

Deliver:

```text
old version preserved
new version committed
ImpactReport
MachineTranslationProof refreshed
```

### Agent 1

Blindly rerun frozen regressions.

Must demonstrate:

```text
T1 FAIL → PASS
L0 FAIL → PASS
unrelated objects unchanged
finding → RESOLVED
```

### Exit

This is the first project-level hard gate.

Do not call the factory trustworthy until this closes.

---

# Phase 1 — canonical convergence contract

This should happen **before Agent 2 builds the Atlas database deeply and before Agent 1 builds synthesis**.

Call it:

# `G5A — CANONICAL OBJECT CONTRACT`

The two agents agree on only the universal envelope.

## Shared canonical types

```text
ObjectId
ObjectVersionId
SchemaRef
AuthorityVector
DependencyEdge
ObjectEvent
```

Canonical envelope:

```json
{
  "object_id": "...",
  "version_id": "...",
  "object_type": "...",

  "schema": {
    "name": "...",
    "version": "..."
  },

  "derived_from": [],
  "source_refs": [],

  "authority": {
    "generation": "...",
    "evidence": "...",
    "review": "...",
    "publication": "..."
  },

  "payload_hash": "...",
  "created_at": "..."
}
```

## Agent 1 owns

Typed semantic payload contracts:

```text
PropositionContent
CommitmentContent
ArgumentContent
CruxContent
ReviewEventContent
ArgumentSynthesisContent
...
```

Pydantic.

## Agent 2 owns

Persistence representation:

```text
scholarly_object
scholarly_object_version
object_dependency
object_event
```

Postgres.

### Critical correction

Replace:

```python
content: dict[str, Any]
```

with typed discriminated Pydantic models.

And stop treating `epistemic_ceiling` as independently canonical.

Authority vector stays canonical.

### Exit

Agent 1 can emit any valid object and Agent 2 can persist it **without knowing its philosophical internals**.

That is the actual convergence seam.

---

# Phase 2 — Atlas foundation

This is primarily Agent 2.

# `A5 — AUTHORITY GRAPH v1`

## Agent 2 — Atlas DB

Build Postgres entities:

```text
Work
Person
Institution
Edition
Witness
Surrogate
Transcription
EText
Source

ExternalIdentifier
NameVariant
Relationship

Asset
AssetVersion
Rights
AuthorityEvidence
```

Migrate current bibliography.

Requirements:

```text
all current IDs preserved/mapped
no metadata loss
JSON export remains available
factory can resolve old references
```

Canonical truths become:

```text
Postgres = entity truth
R2       = byte truth
event log = history truth
```

---

# Phase 3 — R2 artifact substrate

## Agent 2

Implement:

```text
put_asset()
get_asset()
verify_asset()
presign_upload()
```

SHA-256 addressing.

Four buckets:

```text
patala-public
patala-source
patala-manuscripts
patala-artifacts
```

Migrate clean Sanskrit.

Each Source should eventually resolve:

```text
Source
→ EText
→ Edition
→ Work

and

Source
→ AssetVersion
→ SHA256 bytes
```

### Agent 1

No new feature work here.

Instead define source-related evaluation boundaries:

```text
what counts as source identity?
what constitutes edition evidence?
what source uncertainty must propagate downstream?
```

Agent 1 should **not validate bibliography metadata manually**.

It defines the contract by which uncertainty limits downstream claims.

---

# Phase 4 — global API v1

Agent 2 owns implementation.

Cloudflare stack:

```text
Cloudflare Worker
→ Hyperdrive
→ Neon/Postgres

R2 direct bindings
Cloudflare Cache
```

Endpoints:

```text
/works
/editions
/witnesses
/etexts
/people
/institutions
/passages

/search
/resolve
```

Support:

```text
filter
search
select
sort
cursor
```

Also publish OpenAPI.

Agent-oriented compact response must exist from day one.

### Exit

An external agent can retrieve:

```text
Work
→ Edition
→ EText
→ Source
```

without repo knowledge.

---

# Phase 5 — source reconciliation

# `A6 — SOURCE AUTHORITY`

Agent 2 implements the resolver adapters progressively.

Not all at once.

Order:

```text
1 GRETIL / SARIT / Muktabodha
2 Google Books / HathiTrust / LoC
3 NCC
4 NMM / NGMCP
5 IIIF repositories
6 WorldCat where available
```

Interface:

```python
resolve_work()
resolve_edition()
resolve_witness()
resolve_etext()
```

Returns:

```text
AuthorityEvidence[]
```

Never truth.

Authority ladder:

```text
DISCOVERED
CATALOG_MATCHED
MULTI_SOURCE_MATCHED
COPY_INSPECTED
EDITION_VERIFIED
TEXT_DERIVATION_VERIFIED
SCHOLAR_CONFIRMED
```

## Agent 1

Define machine evaluation for reconciliation mistakes:

```text
WORK_COLLAPSE
HOMONYMOUS_TITLE_MERGE
EDITION_MISMATCH
ETEXT_DERIVATION_INFLATION
UNSUPPORTED_AUTHORSHIP
UNSUPPORTED_DATE_PRECISION
```

This becomes Atlas NAT.

Same idea as ARGMAP NAT, but for source authority.

---

# Phase 6 — ARGMAP reality gate

Agent 2 eventually emits the real ARGMAP corpus.

## Agent 2

```text
real SOURCE
→ T1
→ L0
→ ARGMAP
```

Emit exact `EvaluationCandidate`s.

## Agent 1

Run existing ARGMAP NAT.

Freeze natural failures.

Only qualifying ARGMAP can feed proposition production.

```text
load-bearing ARGMAP fail
→ Proposition eligibility = BLOCKED
```

### Exit

The proposition engine is no longer merely demonstrated over gold/synthetic objects.

It is running over actual factory material.

---

# Phase 7 — real epistemic core

Most architecture already exists.

Agent 1 defines/evaluates.

Agent 2 produces/materializes.

Pipeline:

```text
ARGMAP
↓
Proposition
↓
Commitment
↓
GroundingLink
↓
InferenceApplication
↓
Argument
↓
Attack
↓
Crux
```

## Agent 1

Own:

```text
semantic definitions
eligibility
mutation suites
evaluation
Nyāya profile
crux correctness
```

## Agent 2

Own:

```text
bulk production
exact versions
dependency edges
persistence
rebuilds
materialization
```

### Key contract

Agent 2 may generate:

```text
PropositionCandidate
ArgumentCandidate
CruxCandidate
```

Agent 1 determines whether they satisfy the epistemic contract.

---

# Phase 8 — synthesis core

This is the next major Agent 1 frontier.

# `G5B — ARGUMENT SYNTHESIS`

Do not jump directly from arguments to essays.

Build:

```text
ResearchQuestion
DebateFrame
Position
ArgumentSynthesis
```

`ArgumentSynthesis` collects:

```text
research question
positions
arguments
attacks
replies
cruxes
supporting evidence
counterevidence
scope constraints
open questions
unresolved disagreements
```

Example structure:

```text
RQ
│
├ Position A
│  ├ ARG1
│  └ ARG2
│
├ Position B
│  └ ARG3 attacks ARG1
│
└ Crux
   └ proposition P17
```

## Agent 1

Defines synthesis semantics and evaluation.

Mutation suite:

```text
POSITION_COLLAPSE
RIVAL_AS_CONSENSUS
CRUX_OMISSION
COUNTEREVIDENCE_DROP
SCOPE_INFLATION
ARGUMENT_DIRECTION_REVERSAL
UNRESOLVED_AS_RESOLVED
```

## Agent 2

Bulk-generates SynthesisCandidates from eligible arguments.

Persists them and dependencies.

### Exit

You now have the canonical intellectual object every downstream product can consume.

---

# Phase 9 — universal context compiler

This should replace growing one-off packet implementations.

# `A7 — ScholarlyContextBundle`

Agent 2 generalizes current ReviewBundle.

API:

```python
materialize_context(
    target_version,
    profile
)
```

Profiles:

```text
PUBLIC
AGENT
REVIEW
ESSAY
EDUCATION
MEDIA
```

Canonical bundle core:

```text
target
identity/provenance
content
source
upstream dependencies
evidence
arguments
cruxes
scholarship
reviews
authority
downstream impact
open questions
```

Then:

```text
ReviewBundle
= ContextBundle + review actions

EssayBundle
= ContextBundle + composition constraints

EducationBundle
= ContextBundle + learning structure
```

Important:

> Bundles are disposable read models. Never canonical scholarly truth.

---

# Phase 10 — human authority goes real

Current G4 is structurally built.

Now exercise it on actual corpus data.

## Agent 2

Materialize one real:

```text
ReviewBundle
```

with exact Atlas source provenance.

Support:

```text
ReviewEvent
→ ReviewProposal
→ new version
→ supersession
→ dependency invalidation
→ ImpactReport
→ projection rebuild
```

## Agent 1

Validate:

```text
review targets correct exact version
review cannot mutate target
evidence is scoped correctly
human promotion boundary held
dissent preserved
```

Then invite one actual scholar.

### Exit

A real human correction changes a source/translation/proposition and Pāṭala automatically identifies downstream consequences.

That is probably the most important product demonstration after G2.

---

# Phase 11 — Pāṭala Review v1

Now build the first scholar product.

Agent 2 owns UI/infrastructure.

Agent 1 owns review semantics and machine pre-review.

One screen:

```text
SOURCE / Sanskrit
TRANSLATION
T1/L0
translation decision
argument consequence
scholarship
machine findings

WHAT DEPENDS ON THIS?

[Accept]
[Qualify]
[Dispute]
[Alternative]
[Abstain]
```

No giant workbench yet.

### Core UX principle

The killer interaction remains:

> **Show me exactly what changes if I reject this.**

---

# Phase 12 — essay compiler

Only after synthesis is real.

# `G6 — ESSAY COMPILER`

Pipeline:

```text
ArgumentSynthesis
↓
EssayPlan
↓
EssayClaim[]
↓
SentenceEvidenceAudit
↓
Prose
```

## Agent 1

Define:

```text
EssayClaim schema
scope fidelity
claim strength
counterevidence requirements
synthesis-to-essay loss metrics
```

Reuse existing prose-faithfulness work.

## Agent 2

Build:

```text
EssayCompiler
bulk materialization
dependency tracking
stale/rebuild
site projection
```

An essay must become invalid/stale if its supporting synthesis changes.

---

# Phase 13 — education compiler

Parallel after synthesis stabilizes.

Pipeline:

```text
ArgumentSynthesis
↓
LearningClaim
↓
LearningSkill
↓
LearningInteraction
↓
MasteryEvidence
```

First interactions:

```text
speaker classify
premise attach
warrant reconstruct
crux identify
counterevidence select
source ground
translation repair
```

## Agent 1

Defines pedagogic epistemic fidelity:

```text
what exactly is tested?
what misconception does a distractor represent?
does lesson preserve unresolved disagreement?
```

## Agent 2

Builds the interaction engine and materialization.

Cloudflare can later supply:

```text
TTS
images
video delivery
```

but the educational semantics remain Pāṭala-native.

---

# Phase 14 — unified site

Now the front-end converges.

Final:

```text
Astro
+
React islands
+
Cloudflare static assets
```

Surfaces:

```text
/atlas
/texts
/arguments
/review
/essays
/learn
/scholars
```

All read from the same Authority + Scholarly Graph.

There is no separate:

```text
essay DB
education DB
argument DB
```

Only projections.

---

# Phase 15 — agent-native API

This becomes a serious product.

Routes:

```text
/context/{id}
/trace/{id}
/bundle/{type}/{id}
/compare/{a}/{b}
/evidence/{id}
/resolve
```

Example:

```text
GET /context/PTPROP...
```

returns one bounded epistemic neighborhood.

MCP wrappers:

```text
resolve_work
find_sources
get_context
trace_claim
find_arguments
compare_positions
inspect_crux
review_target
```

External AI systems should not need to understand Pāṭala's internal tables.

---

# Phase 16 — manuscripts

Only after one clean source→review vertical exists.

Agent 2 owns ingestion infrastructure:

```text
upload / IIIF manifest
↓
Witness
↓
Surrogate
↓
OCR/HTR/transcription
↓
SourceCandidate
↓
source resolution
↓
factory
```

Reuse:

```text
IIIF
TEI
Transkribus
Kraken
```

No custom HTR.

## Agent 1

Evaluates:

```text
transcription confidence
variant interpretation
edition decisions
downstream semantic impact
```

This is where Pāṭala eventually gets extremely interesting:

```text
manuscript variant
→ translation decision
→ proposition
→ argument
→ essay
```

---

# Phase 17 — textual criticism layer

Longer term:

```text
Witness A
Witness B
Witness C
    ↓
Collation
    ↓
VariantReading
    ↓
EditionDecision
    ↓
CriticalText
```

Objects:

```text
VariantReading
WitnessSupport
EditionDecision
CriticalReading
```

Agent 2 performs collation/materialization.

Agent 1 evaluates the meaning/authority of editorial choices.

Then you can ask:

> Which manuscript variants actually alter a philosophical conclusion?

That's a major unique feature.

---

# Phase 18 — scholar infrastructure

Only after real review behavior exists.

Add:

```text
ORCID
reviewer identity
domain scopes
scholar profile
review provenance
usage accounting
```

Then:

```text
Crossref peer review records
nanopubs
citable ReviewEvents
```

Eventually economic layer:

```text
bounties
usage attribution
Scholar Dividend
```

Do not build that first.

---

# Phase 19 — open data / legitimacy

Agent 2:

```text
JSONL snapshots
Parquet snapshots
RO-Crate releases
OpenAPI
Python SDK
TypeScript SDK
```

Agent 1:

```text
public benchmarks
evaluation protocols
gold provenance
known failure disclosures
```

Public release:

```text
manifest
hashes
schema versions
model metadata
benchmark version
review states
```

Later:

```text
Sigstore/Rekor
```

---

# Phase 20 — operational infrastructure

Only once usage demands it.

Agent 2 / Agent 3:

```text
OpenLineage
Marquez
OpenTelemetry
```

Cloudflare handles:

```text
edge
cache
queues
R2
API
```

Hermes handles:

```text
job orchestration
agent coordination
```

Pāṭala handles:

```text
scholarly state
```

Keep those worlds separate.

---

# Agent responsibilities, permanently

## Agent 1 — Epistemic verifier

Owns:

```text
semantic contracts
evaluation datasets
NAT harnesses
failure taxonomies
gold objects
authority rules
argument semantics
crux semantics
synthesis semantics
review semantics
essay fidelity
education fidelity
benchmarks
```

Agent 1 asks:

> **Does this object deserve the claims being made about it?**

It should avoid:

```text
production scheduling
storage
UI
bulk generation
database plumbing
deployment
```

---

# Agent 2 — Scholarly compiler/factory engineer

Owns:

```text
Atlas
Postgres
R2
source ingestion
factory
regeneration
dependencies
ImpactReport
object persistence
materialized bundles
API
site projections
bulk pipelines
snapshot publication
```

Agent 2 asks:

> **Can this object be produced, versioned, stored, rebuilt, retrieved and propagated correctly?**

It should not decide:

```text
argument truth
scholarly correctness
review validity
gold labels
```

---

# Agent 3 eventually — operational control plane

Only when needed.

Own:

```text
which job next?
what is blocked?
which resources available?
what failed?
which lane owns it?
what release is ready?
```

Never scholarly semantics.

---

# The shared seam between Agent 1 and Agent 2

Everything should cross through two objects.

## Production → evaluation

```text
EvaluationCandidate
```

## Evaluation → production

```text
EvaluationFinding
```

And everything persistent shares:

```text
CanonicalObjectEnvelope
```

That's it.

No casual cross-lane mutation.

---

# The definitive milestone ladder

I would rewrite the global roadmap as:

```text
G2   Real correction loop
     Agent2 repair → Agent1 blind PASS

G3   Real ARGMAP evaluation
     factory ARGMAP → NAT

G4   Epistemic core
     Proposition → Argument → Crux
     [structurally built; prove on real corpus]

G5   Canonical graph convergence
     shared envelope + Atlas persistence

G6   Synthesis
     ResearchQuestion → DebateFrame →
     Position → ArgumentSynthesis

G7   Human authority
     real ReviewBundle + real scholar correction

G8   Scholar product
     Translation Audit / Pāṭala Review

G9   Essay compiler
     synthesis → claims → audited prose

G10  Education compiler
     synthesis → learning objects

G11  Agent API
     context / trace / bundle / MCP

G12  Manuscript ingestion
     IIIF/witness → source → factory

G13  Textual criticism
     variants → edition decisions → semantic impact

G14  Scholar network
     ORCID / attribution / citable reviews

G15  Open trust infrastructure
     snapshots / attestations / Rekor

G16  Cross-tradition compilers
     Sanskrit → Pāli → Greek etc.
```

---

# The one vertical to use as the project proof

While all this is being built, keep forcing everything through **one real work**.

For that work:

```text
Atlas identity
↓
verified edition/EText
↓
R2 asset
↓
SOURCE
↓
T1
↓
L0
↓
ARGMAP
↓
ARGMAP NAT
↓
Propositions
↓
Argument
↓
Crux
↓
ArgumentSynthesis
↓
ReviewBundle
↓
human review
↓
Essay
↓
Lesson
↓
API
↓
site
```

When **one object chain does all of that**, scaling to the 61-work queue becomes much more mechanical.

---

# The single architectural invariant to enforce everywhere

Every product object must answer:

```text
WHAT EXACT OBJECTS DID THIS COME FROM?
```

And the reverse:

```text
WHAT EXACT OBJECTS DEPEND ON THIS?
```

If those two traversals work across:

```text
manuscript
→ source
→ translation
→ proposition
→ argument
→ synthesis
→ review
→ essay
→ lesson
```

then you have the final Pāṭala architecture.

Everything else is UI, throughput, and scale.

That is the global development plan I would now freeze and have both agents work against.

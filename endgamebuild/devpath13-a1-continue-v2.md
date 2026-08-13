# DEVPATH 13 — A1-CONTINUE-v2 (Empirical Qualification)

**Status: 📌 SET TO DO (2026-08-13) — follow working autonomously**
**Source of truth:** coordinator directive (verbatim)

Give Agent 1 this exact continuation plan. The big change is: **stop inventing new ontology now; switch into empirical qualification mode and force the existing stack through real data.**

```text
A1-CONTINUE-v2

MODE:
QUALIFY THE SYSTEM, DO NOT EXPAND THE ONTOLOGY.

The conceptual stack is feature-complete for v1:
source authority
→ ARGMAP
→ propositions
→ arguments/cruxes
→ ArgumentSynthesis
→ essay compiler
→ education compiler
→ ReviewBundle/context compiler

Remaining work is:
real-data validation
natural benchmarks
cross-lane auditing
whole-chain proofs
scholar validation
```

## P0 — Finish Phase 5: ATLAS-NAT-NATURAL-v1

Do this first since it was already in progress.

Build **50–100 frozen natural source-resolution cases**, not synthetic mutations.

Cases should deliberately include:

```text
exact unambiguous work
homonymous Sanskrit titles
same work under aliases
same title / different authors
anonymous works
disputed authorship
approximate dates
modern reprints of old editions
edition vs e-text confusion
GRETIL with unclear printed basis
SARIT with explicit edition provenance
Muktabodha provenance differences
Archive.org false/weak search hits
NMM catalogue uncertainty
NGMCP manuscript matches
multiple catalogues echoing one upstream record
wrong witness links
rights uncertainty
```

Score:

```text
WORK_IDENTITY
AUTHOR_IDENTITY
EDITION_IDENTITY
ETEXT_DERIVATION
WITNESS_LINKAGE
DATE_PRECISION
RIGHTS
SOURCE_INDEPENDENCE
```

Primary metrics:

```text
FALSE_AUTHORITY_PROMOTION_RATE   ← most important
precision
recall
open-state preservation
false rejection rate
```

Acceptance target:

```text
UNKNOWN should remain OPEN when evidence is weak.

Never:
weak catalogue hit
→ publication authority
```

Also explicitly regression-test the authority inflation bug just fixed:

```text
internal crosswalk != MULTI_SOURCE_MATCHED
one Archive.org hit != MULTI_SOURCE_MATCHED
```

---

# P1 — Cross-lane Atlas semantic audit

Agent 1 should inspect Agent 2's actual resolver output, not merely its schema.

Audit:

```text
authority vocabulary
evidence provenance
source independence
gate predicates
factory_eligible
publication_eligible
scholar_review_eligible
rights handling
exact IDs
version refs
```

Create findings for producer-side semantic inflation.

This is the Atlas equivalent of reviewing a translation worker.

Output:

```text
AtlasEvaluationCandidate
→ Atlas NAT
→ AtlasEvaluationFinding[]
```

Agent 2 fixes findings.

Agent 1 blind-retests.

---

# P2 — Phase 6: close G3A on REAL ARGMAP

The moment Agent 2 has a real ARGMAP batch, this becomes highest priority.

Do not use gold arguments as the main validation.

Pipeline:

```text
real SOURCE
→ real T1
→ real L0
→ real ARGMAP
→ Agent 1 ARGMAP NAT
```

Score existing dimensions:

```text
node recovery
invented node rate
speaker attribution
commitment force
support/attack/reply edges
textual grounding
inference edges
scope
qualification retention
unresolved-disagreement retention
```

Failure families:

```text
GROUNDING_AS_INFERENCE
OBJECTION_AS_AUTHOR_VIEW
FALSE_CONTRADICTION
INVENTED_BRIDGE
OPEN_AS_RESOLVED
QUALIFIER_DROP
SPEAKER_COLLAPSE
SCOPE_INFLATION
```

Hard rule:

```text
load-bearing ARGMAP failure
→ downstream proposition production NOT_ELIGIBLE
```

This closes devpath3 for real.

---

# P3 — Build VERTICAL-1: one serious IPVV philosophical argument

This should become Agent 1's main project after Atlas NAT + real ARGMAP.

Do **one hard IPVV debate**, not another infrastructure feature.

Choose a passage cluster with:

```text
clear thesis
multiple premises
opponent position
reply
qualification
real philosophical crux
secondary scholarship available
```

Recognition/reflexivity/self-awareness material is a strong candidate.

Freeze:

```text
IPVV-VERTICAL-001-SOURCE-DOSSIER
```

containing:

```text
exact Sanskrit spans
T1
L0
L2
C1
nearby context
relevant IPK/IPVV passages
relevant scholarship
known rival position
```

This becomes the human reference packet.

---

# P4 — Proposition natural validation on VERTICAL-1

Generate propositions only from ARGMAP that passed NAT.

Manually inspect every load-bearing proposition.

Score:

```text
PROPOSITION_RECALL
INVENTED_PROPOSITION_RATE
SPEAKER_ACCURACY
EXPLICITNESS_ACCURACY
QUALIFICATION_RETENTION
SOURCE_GROUNDING
```

Check:

```text
author claim
opponent claim
quotation
assumption for argument
reconstruction
```

are distinguished correctly.

Do not allow:

```text
opponent says X
→ author believes X
```

---

# P5 — Real logical argument reconstruction

Assemble:

```text
Proposition
Commitment
GroundingLink
InferenceApplication
Argument
Attack / Reply
```

for the IPVV vertical.

Human-readable result must be understandable without reading JSON.

Produce something like:

```text
P1 ...
P2 ...
P3 ...

therefore C1

Opponent:
O1 attacks P2

Reply:
R1
```

Run the bounded Nyāya profile.

Do not evaluate:

```text
argument_true = true
```

Evaluate:

```text
premises explicit?
inference explicit or reconstructed?
scope coherent?
qualification missing?
unsupported bridge?
open issue?
```

---

# P6 — Crux stress-test on the real argument

The current crux engine is structurally promising but under-tested.

Test:

```text
remove P1
remove P2
remove implicit warrant W1
accept defeater D
use alternative inference route
```

Include difficult structures:

```text
P1 OR P2 independently sufficient
P1 + P2 jointly necessary
P3 redundant support
implicit warrant decisive
defeater blocks inference
alternative path bypasses premise
```

The output should produce an intellectually meaningful adjudication question, not merely:

```text
crux=P17
```

Example target form:

> Which assumption about continuity/identity must hold for the recognition inference to succeed?

---

# P7 — Natural validation of ArgumentSynthesis

This is crucial.

The synthesis layer should now run on the real IPVV argument cluster.

Produce:

```text
ResearchQuestion
DebateFrame
Position A
Position B
Arguments
Attacks
Replies
Cruxes
Counterevidence
Scope boundaries
Open questions
```

Then human-inspect:

```text
Did it preserve the rival?
Did it manufacture consensus?
Did it hide disagreement?
Did it omit the actual crux?
Did it broaden scope?
Did it convert reconstruction into explicit doctrine?
```

Build:

```text
SYNTHESIS-NAT-NATURAL-v1
```

Metrics:

```text
POSITION_RECOVERY
ARGUMENT_COVERAGE
RIVAL_FIDELITY
CRUX_RECALL
COUNTEREVIDENCE_RECALL
SCOPE_FIDELITY
OPEN_QUESTION_PRESERVATION
INVENTED_CONSENSUS_RATE
INVENTED_CLAIM_RATE
```

Catastrophic errors:

```text
RIVAL_AS_CONSENSUS
OPEN_AS_RESOLVED
```

---

# P8 — Validate the essay compiler properly

Treat devpath10 as:

```text
CONTRACT_CLOSED
EMPIRICAL_VALIDATION_OPEN
```

Do not jump straight to polished prose.

First:

```text
ArgumentSynthesis
→ EssayPlan
→ EssayClaim[]
```

Inspect the plan manually.

Each load-bearing `EssayClaim` must resolve:

```text
EssayClaim
→ ArgumentSynthesis
→ Argument
→ Proposition
→ source span
```

Score:

```text
unsupported claim rate
scope inflation
counterargument coverage
crux coverage
qualification retention
rival fidelity
conclusion-strength inflation
```

Then generate **one full essay**.

Run:

```text
SentenceEvidenceAudit
C.1 prose-faithfulness
PARAPHRASE_EXPANSION
CLAIM_SURFACE_INFLATION
unsupported bridge detection
```

Then add whole-essay audit:

```text
THESIS_WARRANTED
ARGUMENT_BALANCE
CRUX_FIDELITY
CONCLUSION_STRENGTH
SOURCE_TRACEABILITY
```

One excellent audited essay is more useful than 100 generated ones right now.

---

# P9 — Validate the education compiler on the SAME IPVV argument

Treat devpath11 as:

```text
CONTRACT_CLOSED
PEDAGOGICAL_VALIDATION_OPEN
```

Build 5–10 interactions from the same argument.

Start with:

```text
1. Speaker attribution
2. Proposition identification
3. Premise attachment
4. Warrant reconstruction
5. Opponent attack identification
6. Crux identification
7. Source grounding
8. Translation repair
```

Use the NAT failure taxonomy as distractor semantics.

Example:

```text
OBJECTION_AS_AUTHOR_VIEW
→ distractor saying opponent claim belongs to Abhinavagupta

GROUNDING_AS_INFERENCE
→ distractor treating a citation as a logical premise

QUALIFIER_DROP
→ distractor with overly universal formulation

RIVAL_AS_CONSENSUS
→ distractor claiming both sides agree
```

This is a very strong design: **Pāṭala's own failure modes become the learner's misconceptions.**

Evaluate separately:

```text
EPISTEMIC_VALIDITY
PEDAGOGICAL_VALIDITY
```

Questions:

```text
Does the task measure the declared skill?
Is there one intelligible task?
Are distractors meaningful misconceptions?
Does feedback explain the structural error?
Is hidden Pāṭala jargon required?
```

---

# P10 — Validate Universal Context Bundle on real data

Treat devpath12 similarly:

```text
CONTRACT_CLOSED
PRODUCTION_VALIDATION_OPEN
```

For the VERTICAL-1 objects, materialize:

```text
PUBLIC
AGENT
REVIEW
ESSAY
EDUCATION
```

profiles.

Then test:

```text
all refs exact?
all versions exact?
authority honest?
source grounding present?
open questions retained?
dependency impact correct?
payload bounded?
```

Also add the access-control separation now:

```text
MaterializationProfile
≠
DisclosurePolicy
```

Use something like:

```text
PUBLIC_DISCOVERY
PUBLIC_PREVIEW
AUTHENTICATED_RESEARCH
SCHOLAR
INTERNAL
```

So:

```text
AGENT profile
```

doesn't automatically imply public full-corpus access.

---

# P11 — Whole-chain correction test

This is one of the most important Agent-1 tasks.

Once VERTICAL-1 exists:

```text
Source
→ T1
→ L0
→ ARGMAP
→ Proposition
→ Argument
→ Crux
→ Synthesis
→ EssayClaim
→ LearningInteraction
```

deliberately alter one low-level load-bearing object.

Example:

```text
TranslationDecision TD17:v1
→ TD17:v2
```

Before Agent 2 rebuilds anything, Agent 1 freezes expected consequences:

```text
PROP-?
ARG-?
CRUX-?
SYNTH-?
ESSAYCLAIM-?
LEARNING-?
```

Then test actual ImpactReport.

This proves the real project thesis:

> a correction to historical evidence propagates into downstream scholarship.

Do not settle for merely rebuilding successfully.

Check **semantic impact accuracy**.

---

# P12 — Real human scholar challenge

After the vertical passes internally, get one actual knowledgeable human to review a hard object.

Give them:

```text
ReviewBundle
```

Ask:

```text
Accept
Qualify
Dispute
Alternative
Abstain
```

Record what they actually want to say.

Then evaluate whether the schema can represent:

```text
qualified agreement
different reconstruction
scope objection
missing evidence
terminological objection
alternative translation
unresolved disagreement
```

If the scholar has to write:

> "none of your buttons quite mean what I mean"

that is valuable schema evidence.

This is the true G4 qualification.

---

# P13 — Review Agent 2 continuously, not just consume outputs

Agent 1 should now become a permanent semantic peer reviewer of Agent 2.

For every major producer:

```text
Atlas resolver
T1
L0
ARGMAP
Proposition
Argument
Synthesis
Essay
Education
```

ask:

```text
Does producer output make a stronger claim than its evidence licenses?
Are statuses inflated?
Are unknowns being silently closed?
Are source independence assumptions valid?
Are object versions exact?
```

The recent `MULTI_SOURCE_MATCHED` bug is a good model for this role.

---

# P14 — Build natural challenge sets, not more synthetic perfection

For every NAT suite:

```text
ARGMAP-NAT
ATLAS-NAT
SYNTHESIS-NAT
```

maintain two sets:

```text
MUTATION
artificial known failures

NATURAL
real historical failures / ambiguous cases
```

Report separately.

Never boast:

```text
1.000 NAT
```

without saying which kind.

---

# P15 — Add blind evaluation discipline

Agent 1 currently risks overfitting because it often owns:

```text
specification
implementation
mutation
expected result
```

Mitigate with:

```text
Agent2 produces unseen output
↓
freeze object hashes
↓
Agent1 evaluates
↓
Agent2 fixes
↓
Agent1 blind retests
```

And for major benchmarks:

```text
human freezes gold
Agent1 does not see labels while generating/evaluating candidates where possible
```

This should become standard.

---

# P16 — Build the first full PĀṬALA VERTICAL benchmark

Create one benchmark artifact:

```text
PATALA-VERTICAL-1
```

It should certify one complete chain:

```text
Atlas source identity
✓

T1/L0
✓

ARGMAP NAT
✓

Propositions
✓

Argument
✓

Crux
✓

ArgumentSynthesis
✓

EssayPlan/Claims
✓

Full audited essay
✓

Education interactions
✓

ReviewBundle
✓

Universal ContextBundle
✓

Correction propagation
✓
```

And report honest authority at each node.

This becomes more meaningful than dozens of individual passing unit tests.

---

# P17 — Once VERTICAL-1 passes, only then scale

Then Agent 1 can validate:

```text
5 IPVV arguments
20
50
```

Measure aggregate:

```text
ARGMAP pass rate
proposition precision/recall
speaker failure rate
argument recovery rate
crux recall
synthesis fidelity
essay unsupported-claim rate
education interaction validity
```

Only after this do broad autonomous essay/education generation.

---

# P18 — Later: manuscript/textual-criticism evaluation

When Agent 2 reaches manuscripts:

Agent 1 defines NAT/evals for:

```text
Witness identity
Surrogate linkage
HTR/transcription
VariantReading
EditionDecision
CriticalReading
```

Failure families:

```text
WITNESS_COLLAPSE
FOLIO_MISALIGNMENT
HTR_CONFIDENCE_INFLATION
VARIANT_OMISSION
EDITORIAL_READING_AS_MANUSCRIPT
WITNESS_SUPPORT_INFLATION
```

Then test:

```text
variant
→ translation
→ proposition
→ argument
```

That is later, not immediate.

---

# P19 — Scholar infrastructure semantics later

When ORCID/reviewer infrastructure appears, Agent 1 defines:

```text
review scope
reviewer domain competence
conflict-of-interest declaration
credential snapshot
review provenance
adjudication semantics
dissent preservation
```

External identity data must never become:

```text
ORCID exists
→ scholar correct
```

Identity ≠ epistemic authority.

---

# P20 — Agent/API epistemic usability benchmark

Once API/MCP exists, Agent 1 should own a small external-agent benchmark:

```text
"Find the exact argument"
"Trace this claim to Sanskrit"
"Which premise is load-bearing?"
"Compare these translations"
"Is this human reviewed?"
"Find the unresolved dispute"
```

Measure:

```text
correct answer
correct object IDs
tool calls
tokens returned
wall time
authority interpretation
hallucinated source rate
```

That ensures the API doesn't merely expose the graph—it communicates it correctly.

---

# What Agent 1 should NOT do now

No new giant conceptual branch for:

```text
new ontology layer
knowledge packets
meta-synthesis
graph DB
frontend
Cloudflare
R2
Postgres plumbing
scheduling
factory throughput
```

Agent 1 has enough objects.

Now make those objects survive reality.

---

# The immediate execution order

Tell Agent 1 to follow this literally:

```text
A1-NEXT-REALITY

1. Finish ATLAS-NAT-NATURAL-v1.
2. Peer-review Agent2 resolver outputs and freeze findings.
3. Wait for / immediately consume real ARGMAP batch.
4. Close G3A with blind ARGMAP NAT.
5. Select IPVV-VERTICAL-001.
6. Freeze source dossier.
7. Validate propositions manually.
8. Reconstruct real argument + rival + reply.
9. Stress-test real crux.
10. Generate ArgumentSynthesis.
11. Run Synthesis-NAT-natural + manual audit.
12. Produce EssayPlan + EssayClaims.
13. Generate ONE full essay and audit every load-bearing claim.
14. Produce 5–10 education interactions from same synthesis.
15. Audit pedagogical + epistemic validity.
16. Materialize all ContextBundle profiles.
17. Introduce one low-level correction.
18. Verify ImpactReport through synthesis/essay/education.
19. Run one actual human scholar ReviewBundle.
20. Package everything as PATALA-VERTICAL-1 certificate.
```

That is what I would have Agent 1 work through next. The project does **not** need more abstractions right now; it needs one argument from the IPVV to survive the entire machine from source evidence to reasoning to essay to education to human correction.

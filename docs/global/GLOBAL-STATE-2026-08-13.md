# ELAD HANDOVER — PĀṬALA / AGENT 1

**Role:** work alongside Agent 1 as architectural/epistemic reviewer.
**Date:** 2026-08-13
**Current lane:** `origin/agent1-argument-layer-a1b` until Agent 0 deliberately reconciles the branch fork.

This handover captures the things Agent 1 repeatedly lost sight of, the important discoveries from peer review, the current architecture, the falsifications we want preserved, and the near-term execution order.

---

# 1. THE BIG PICTURE

Pāṭala is **not primarily an AI Sanskrit translator or essay generator**.

The durable project is a trust/research infrastructure where machine-generated scholarship can be traced through:

```text
source
→ textual analysis
→ propositions
→ arguments
→ audits
→ higher-order synthesis
→ production objects
→ prose
→ scholar review
→ correction/version history
→ reusable benchmark/trust assets
```

The moat is approximately:

[
M = D \times P \times V \times N \times A
]

where:

* **D** = unique/curated data;
* **P** = provenance depth;
* **V** = verified scholarly judgments;
* **N** = contributor/network effects;
* **A** = adoption of identifiers/interfaces.

The multiplicative intuition matters:

> A corpus is copyable. An argument graph is copyable. An AI translation is increasingly copyable.
> A canonical corpus + exact provenance + review history + expert judgments + persistent IDs + network of scholars + external integrations is much harder to displace.

The project should therefore optimize for:

```text
WHAT CAN MACHINES TRUST?
```

rather than:

```text
HOW MUCH TEXT CAN MACHINES GENERATE?
```

---

# 2. PERMANENT EPISTEMIC DISCIPLINE

Every Agent 1 build should distinguish:

```text
SOFTWARE validity
→ tests

EMPIRICAL validity
→ benchmark performance

SCHOLARLY validity
→ independent experts
```

Never collapse them.

Likewise:

```text
GATE_ACCEPTED
≠
EVIDENCE_ACCEPTED
≠
SCHOLARLY_SUPPORTED
```

and:

```text
ENGINEERING_VALIDATED
≠
SCHOLARLY_CORROBORATED
≠
INDEPENDENT_REVIEWED
```

Useful state vocabulary:

```text
MACHINE_PROPOSED
ENGINEERING_VALIDATED
MULTI_MODEL_CORROBORATED
SCHOLARLY_CORROBORATED_PRELIMINARY
SCHOLARLY_CORROBORATED
INDEPENDENT_REVIEWED
```

Plus orthogonal descriptors such as:

```text
HISTORICALLY_ATTESTED
STRUCTURALLY_COHERENT
RECONSTRUCTED
UNRESOLVED
UNSOURCED_RECONSTRUCTION
```

Tests passing proves only the software implemented the specified behavior.

It does **not** prove the Sanskrit interpretation, argument reconstruction, or philosophical conclusion is correct.

---

# 3. REASONING DISCIPLINE

For any argument or essay:

1. define the debate frame;
2. identify exact propositions;
3. distinguish proposition from warrant;
4. distinguish evidence from inference;
5. distinguish validity from soundness;
6. inspect scope;
7. inspect modality;
8. inspect speaker/attribution;
9. inspect level of analysis;
10. surface defeaters;
11. preserve alternatives;
12. identify unresolved cruxes;
13. state what the conclusion **does not** establish.

False scholarly assertion is treated as a severe failure.

Precision > coverage.

Abstention is a legitimate successful output.

---

# 4. THE ARCHITECTURE AGENT 1 MUST KEEP IN HIS HEAD

This is the current architecture:

```text
SOURCE / Sanskrit
       ↓
L0 / L2 / C1
       ↓
Propositions
       ↓
Local Arguments
       ↓
ContextualArgumentAudit
       │
       ├──────── Themes
       │
       ↓
ResearchPack
       ↓
ArgumentSynthesis
       ↓
SynthesisAudit
       ↓
 ┌─────┼─────────────┐
 ↓     ↓             ↓
EO   EssayPlan   ArgumentMap
       ↓
     Essay
       ↓
SentenceEvidenceAudit
       ↓
Scholar Review
```

Each object has a distinct responsibility.

### Themes

```text
Where in the conceptual landscape?
```

Themes are navigation/context.

They are **not inferential premises**.

### Argument

```text
What does this local textual unit argue?
```

### ContextualArgumentAudit

```text
Does the reconstructed local argument trigger known structural defects
or contextual contradiction candidates?
```

### ResearchPack

```text
Which materials belong to this inquiry?
```

It is a selection/composition object.

It **does not reason**.

### ArgumentSynthesis

```text
Given several lower-order arguments, what larger argument can defensibly
be reconstructed, through which explicit new warrants?
```

This is the missing layer we discovered only recently.

### EO

A presentation/projection.

**Not canonical reasoning.**

### Essay

Readable communication.

It owns no new truth.

---

# 5. ONE OF THE MOST IMPORTANT DISCOVERIES: ARGUMENTSYNTHESIS

Before this layer existed, the pipeline effectively did:

```text
ARG-002
+
ARG-004
→ essay magically connects them
```

That means the LLM could introduce an unstated inference while writing prose.

We fixed that with:

```text
ArgumentSynthesis
```

Definition:

> **Argument = reasoning reconstructed from a local textual unit.**

> **ArgumentSynthesis = a new higher-order argument constructed from multiple lower-order arguments/evidence objects.**

First canonical synthesis:

```text
SYN-IPVV-REFLEXION-CORE-001
```

Core reasoning:

```text
P1:
the I-reflexive awareness is not shown to be conceptual construction

P2:
conscious manifestation involves reflexive self-awareness / vimarśa

NEW BRIDGE:
SYN-INF-001

C:
reflexivity belongs intrinsically to manifestation
```

The crucial rule:

```text
P1 + P2
DO NOT AUTOMATICALLY ENTAIL
C
```

The bridge is therefore first-class:

```text
SYN-INF-001

origin = RECONSTRUCTED
support_state = UNRESOLVED
```

This separation was another important discovery:

```text
RECONSTRUCTED
```

answers:

> Where did the inference come from?

while:

```text
UNRESOLVED
```

answers:

> How well supported is it?

Never collapse provenance and evaluation.

---

# 6. WEAKEST-GOVERNS DEPENDENCY PROPAGATION

Another core mechanism:

Wrong:

```text
argument A passed
+
argument B passed
=
synthesis strongly supported
```

Correct:

```text
synthesis conclusion
depends on
P1
P2
bridge warrant
open cruxes
```

Therefore:

[
Ceiling(S) =
\min {status(d) : d \in LoadBearing(S)}
]

**Only load-bearing dependencies cap the result.**

Dependencies need roles such as:

```text
LOAD_BEARING_PREMISE
LOAD_BEARING_INFERENCE
CONTEXT
ILLUSTRATION
RIVAL
QUALIFIER
```

This distinction matters because a weak background example should not cap an otherwise strong argument.

The first synthesis currently has:

```text
G2-CONC
→ SCHOLARLY_CORROBORATED_PRELIMINARY

G4-CONC
→ MACHINE_PROPOSED

SYN-INF-001
→ UNRESOLVED
```

therefore:

```text
epistemic_ceiling = UNRESOLVED
```

---

# 7. TWO AXES, NOT ONE

A major peer-review correction was recognizing:

```text
epistemic status
```

and:

```text
structural audit status
```

are different dimensions.

Example:

```text
G2-CONC

epistemic_status:
SCHOLARLY_CORROBORATED_PRELIMINARY

structural_audit:
NOT_AUDITED
```

This is perfectly coherent.

Do not force them onto a single ladder.

The synthesis therefore carries:

```text
epistemic_ceiling = UNRESOLVED

structural_audit_state = INCOMPLETE
```

Until a real persisted ContextualArgumentAudit exists:

```text
structural_gate_outcome
```

must not magically become:

```text
accepted
```

---

# 8. THE NYĀYA GATE: WHAT IT ACTUALLY IS NOW

Agent 1 repeatedly reverted to the stale idea:

```text
golds
→ corroboration
→ extractor
→ Nyāya later
```

Wrong.

The argument IR prerequisite has already been crossed.

Current architecture:

```text
build_argument()
→ ArgumentProposal

audit_argument(argument, comparison_graph)
→ ContextualArgumentAudit
```

Important separation:

```text
construction
≠
validation
```

`build_argument()` constructs.

`audit_argument()` contextually audits.

The gate is now an active:

> **bounded structural defect checker + contextual contradiction-candidate nominator.**

Nyāya-inspired defect families:

```text
asiddha
viruddha
savyabhicara
satpratipaksa
badhita
```

But do **not** describe it as:

> “Does the argument actually work philosophically?”

It establishes something narrower.

A clean result is an engineering/structural result.

It does not establish historical or philosophical correctness.

---

# 9. VIRUDDHA: IMPORTANT FALSIFICATION TO PRESERVE

This is one of the best examples of the project's intended epistemic discipline.

The first graph-aware contradiction detector produced alleged cross-gold disagreements.

Examples included something equivalent to:

```text
"pratibhā is order-less"

vs

"pratibhā is not constituted by order"
```

The system initially treated these as disagreements.

Peer review showed they were **false positives**.

Another fired because of junk lexical overlap.

The findings were explicitly retracted.

Do not rewrite history as though v2 worked perfectly from the start.

Current viruddha v2:

* removes function-word junk;
* handles Unicode/diacritics better;
* excludes certain reconstructed/opponent-attributed propositions from established targets;
* includes explicit defeaters.

Its outputs are:

```text
VIRUDDHA_CANDIDATE
semantic_status = UNRESOLVED
```

Possible defeaters:

```text
SCOPE_DIFFERENCE
MODALITY_DIFFERENCE
SPEAKER_DIFFERENCE
TEMPORAL_DIFFERENCE
QUALIFICATION
LEVEL_DIFFERENCE
NON_EQUIVALENT_PREDICATE
```

Permanent rule:

> **STOP improving viruddha for now.**

Do not turn it into a semantic contradiction oracle.

Candidate ≠ fixture ≠ adjudicated disagreement.

---

# 10. CORROBORATION: ANOTHER THING AGENT 1 KEPT FALLING BACK INTO

We started doing proposition-by-proposition scholar corroboration.

It became a treadmill.

One especially useful failure occurred when a Ratié paper was initially treated as evidence for a proposition it did not actually address.

That exposed the key rule:

```text
topical similarity
≠
evidence relevance
```

Corroboration is now:

> **opportunistic, not a global pipeline stage.**

Use published scholarship when:

* proposition is load-bearing;
* model review disputes it;
* multiple plausible readings exist;
* it matters to a benchmark fixture;
* it materially changes synthesis/essay.

Do **not** require every proposition to go through a giant scholarship dossier before progress continues.

Evidence relations:

```text
SUPPORTS
QUALIFIES
CONTRADICTS
ALTERNATIVE
NO_DIRECT_EVIDENCE
```

Promotion checks include:

```text
PRIMARY
INDEPENDENCE
RELEVANCE
RELATION
TRACEABILITY
SCOPE
```

And evidence role taxonomy:

```text
T = TEXTUAL_ATTESTATION
R = RECONSTRUCTION
E = EMPIRICAL_EVIDENCE
C = COMPARATIVE
H = HYPOTHESIS
X = UNRESOLVED_CONFLICT
```

---

# 11. EO — WHAT WE LEARNED

EO was briefly at risk of becoming the canonical synthesis schema.

We rejected that.

Why?

EO is shaped around a five-member Nyāya presentation:

```text
pratijñā
hetu
udāharaṇa
upanaya
nigamana
```

But actual IPVV reasoning can be:

* reductive;
* transcendental;
* dialectical;
* objection/reply;
* cumulative;
* exegetical;
* disjunctive;
* recursive.

Therefore:

```text
ArgumentSynthesis = Pāṭala-native canonical reasoning

EO = downstream projection
```

Adapters:

```text
synthesis_to_eo()
synthesis_to_essay_plan()
synthesis_to_argument_map()
```

---

# 12. COMMIT B'S CENTRAL INVARIANT

Commit B proved:

[
authority(P(x)) \leq authority(x)
]

where (P) is the EO projection.

In words:

> A presentation may simplify, but may never become more authoritative than its source object.

Commit B tests reject:

* manufactured structural `accepted`;
* `strongly_supported` under an unresolved synthesis;
* invented provenance refs;
* dropped universal-Self boundary;
* `RECONSTRUCTED → ASSERTED` laundering;
* unsourced rival → `live`.

This is a very good permanent concept:

> **monotone no-strengthening projection**

Use it elsewhere in Pāṭala.

---

# 13. COMMIT C: FIRST ACTUAL PROSE VERTICAL

Commit C produced:

```text
SYN-IPVV-REFLEXION-CORE-001
→ EO
→ EssayPlan
→ actual mini-essay
→ SentenceEvidenceAudit
```

and five adversarial prose mutations.

Those mutations catch:

### A. Strength inflation

```text
"The synthesis suggests X"
→
"The argument proves X"
```

### B. Authorship laundering

```text
"Pāṭala reconstructs X"
→
"Abhinavagupta argues/proves X"
```

when X is really `SYN-CONC-001`.

### C. Boundary erasure

Remove:

```text
does not establish universal Self
```

### D. Rival laundering

```text
"The Buddhist fallback can be reconstructed as..."
→
"The Buddhist position is..."
```

despite no source.

### E. Warrant erasure

```text
G2 + G4
→ therefore synthesis conclusion
```

while bypassing `SYN-INF-001`.

All currently fail as intended.

The honest capability claim is only:

> **For one IPVV synthesis, Pāṭala can produce a provenance-linked essay and deterministically catch specified epistemic-laundering mutations.**

Do not say:

> “Pāṭala writes reliable scholarly essays.”

---

# 14. NEWEST IMPORTANT FINDING: METADATA CAN BE RIGHT WHILE PROSE IS STILL WRONG

This may be the highest-value result from Commit C.

The SentenceEvidenceAudit can correctly say:

```text
claim_ref = G2-TC2
speaker = Abhinavagupta
render_mode = ATTRIBUTED
```

while the prose itself quietly adds something stronger than `G2-TC2`.

That means:

```text
correct provenance metadata
≠
faithful paraphrase
```

Call the failure:

```text
PARAPHRASE_EXPANSION
```

or:

```text
CLAIM_SURFACE_INFLATION
```

Examples discovered in the current essay:

### S003

Current prose says construction is:

> “always an operation upon independently given elements.”

But the source proposition is closer to:

> conceptual construction combines/differentiates/determines contents.

“Independently given elements” imports stronger metaphysics/reconstruction.

### S004

Current prose says the I-awareness is:

> “the single, un-doubted self-grasp that every construction presupposes.”

But `G2-TC2` only establishes something closer to:

> the I-awareness is not one more constructed relation.

The “every construction presupposes it” claim belongs at a stronger reconstructed level.

### S007

Especially important:

The essay labels:

```text
attribution = AUTHOR
assertion_strength = TEXTUAL
```

for `G4-CONC`.

But `gold004.py` itself marks:

```text
G4-CONC.explicitness = RECONSTRUCTED
```

So the metadata itself is too strong.

This should be C.1's focus.

---

# 15. C.1 — IMMEDIATE RECOMMENDED WORK

Before xAIF or new integrations:

1. tighten S003;
2. tighten S004;
3. reclassify S007 as reconstructed/qualified;
4. add a paraphrase-faithfulness dimension.

Suggested relation:

```text
semantic_relation_to_claim =
    EXACT
    CONSERVATIVE_PARAPHRASE
    EXPANSIVE
```

For load-bearing prose:

```text
EXPANSIVE
→ reject
```

unless the additional content has its own supporting claim/inference refs.

Example negative mutation:

Good:

> “The passage distinguishes the I-awareness from conceptual construction.”

Bad:

> “The passage therefore shows that the I-awareness is the universal precondition of every cognition.”

The bad sentence should require additional argument/synthesis support.

Do **not** solve this by keyword regexes.

The real question is:

> Does the surface sentence semantically exceed the commitment of the referenced proposition?

For the first essay this may be manually curated.

Do not build an LLM judge yet.

---

# 16. DO NOT OVERFIT THE ESSAY TO THE VALIDATOR

Another permanent lesson.

Not every sentence needs provenance.

Sentence roles:

```text
LOAD_BEARING
EXPLANATORY
TRANSITION
SIGNPOST
```

Only load-bearing scholarly sentences require the full:

```text
claim
→ inference
→ source
```

chain.

Otherwise you create dreadful robotic writing that technically passes the audit.

Pāṭala needs both:

```text
epistemic integrity
+
actual readable scholarship
```

---

# 17. SCHOLARLY VISION

There are three important vision docs in the project:

### scholar-proof

Deep bet:

```text
identity
→ judgment
→ provenance
→ usage
→ dividend
```

Trusted human judgment attached to exact identifiable claims.

### scholar-acquisition

The scholar, not the PDF, becomes the strategic unit.

Pāṭala aims at:

```text
rights-cleared scholarly commons
+
provenance graph
+
economic layer
```

### vision-08 economics

Recruit experts through:

* paid adjudication;
* durable credit;
* ORCID/CRediT/DOI legibility;
* intellectual territory;
* persistent disagreement;
* potentially usage-linked dividends.

This is not secondary product fluff.

It may be the real network moat.

---

# 18. EXTERNAL STANDARDS: THE INTERESTING CONVERGENCE

A deep survey found that Pāṭala independently reinvented structures similar to mature standards.

Important conclusion:

> **Architectural similarity validates compatibility, not correctness.**

Never say:

```text
"SEPIO validates Pāṭala"
```

Say:

```text
"Pāṭala is strongly alignable with SEPIO."
```

---

# 19. SEPIO

SEPIO broadly models:

```text
assertion
→ evidence line
→ agent
→ derivation
```

Pāṭala already has analogues:

```text
EvidenceRole
EvidenceUse
Origin
DerivationMethod
review_events
supersedes
```

Recommendation:

> alignment contract, not SEPIO runtime.

Do not import OWL/LinkML machinery unless an actual interoperability requirement demands it.

---

# 20. xAIF

Probably the cheapest concrete interoperability win.

Existing Pāṭala `aifgraph.py` was already AIF-inspired.

Approximate mapping:

```text
Pāṭala Proposition
↔
AIF I-node

Pāṭala Inference
↔
AIF RA-node

Pāṭala Conflict
↔
AIF CA-node
```

Future adapter:

```text
Pāṭala Argument IR
↔
xAIF
```

Hard requirement:

> Anything xAIF cannot express remains an explicit Pāṭala extension.

Never mutate Pāṭala's internal ontology merely to fit xAIF.

Round-trip tests should preserve:

* proposition IDs;
* inference edges;
* attack/conflict edges;
* attribution/commitment where representable;
* Pāṭala extension metadata.

---

# 21. NANOPUBLICATIONS

Extremely aligned with the scholar-stamp vision.

Nanopub structure:

```text
Assertion
Provenance
PublicationInfo
```

Pāṭala review objects are already close.

Adopt principles rather than RDF stack:

* stable identity;
* immutable published object;
* attached provenance;
* named agent;
* timestamp;
* supersession rather than mutation;
* citability;
* license/attribution.

The currently identified missing field is especially:

```text
license / attribution
```

---

# 22. SCHOLAR-STAMP — POTENTIALLY HIGHER STRATEGIC VALUE THAN xAIF

The future object should resemble:

```json
{
  "review_id": "REV-IPVV-G2-CONC-001",
  "subject_ref": "ARG-GOLD-002:G2-CONC",

  "judgment": {
    "relation": "SUPPORTS",
    "decision": "ACCEPT_WITH_QUALIFICATION",
    "scope": "local proposition only"
  },

  "reviewer": {
    "name": "...",
    "orcid": "..."
  },

  "provenance": {
    "evidence_refs": ["..."],
    "reviewed_version": "...",
    "timestamp": "...",
    "method": "SCHOLAR_ADJUDICATION"
  },

  "publication_info": {
    "stable_id": "...",
    "license": "...",
    "citation": "...",
    "supersedes": null
  }
}
```

The product vision:

> A scholar's judgment should itself become a durable scholarly artifact.

Then a scholar can say:

> I adjudicated this exact proposition; the judgment is immutable, citable, ORCID-linked, versioned, and its downstream use can be measured.

That converts review from invisible platform labor into:

```text
scholarly output
+
reputation asset
+
network node
+
potential economic asset
```

This may be the deepest strategic piece of Pāṭala.

---

# 23. TANTRAFACT

SciFact/MultiVerS-inspired future benchmark.

Potential core labels:

```text
SUPPORTED
REFUTED
UNDERDETERMINED
```

with exact rationale spans.

Pāṭala should probably also track reasons like:

```text
SCOPE_MISMATCH
ATTRIBUTION_MISMATCH
TEXTUALLY_SUPPORTED_BUT_INFERENTIALLY_OPEN
```

But do not launch a huge synthetic benchmark.

Future useful pilot:

```text
20–30 propositions
2 independent scholars
adjudication of disagreements
```

That is worth vastly more than hundreds of machine-created examples.

---

# 24. SPARE / VPR / FoVer

Interesting conceptually.

### SPARE

Step-wise reasoning alignment + first divergence.

Potential future mapping:

```text
reference = reviewed Argument Gold
trace = LLM or scholar reasoning
output = first divergent reasoning step
```

This is exactly the kind of evaluation Pāṭala eventually wants.

But wait for reviewed gold.

### VPR / FoVer

Useful rationale for heterogeneous verification:

```text
source verifier
morphology verifier
logic verifier
formal verifier
scholar verifier
```

Conceptual support only.

Do not build around them now.

---

# 25. NAVYA-NYĀYA / SCL

Interesting but narrow.

SCL relation vocabulary such as:

```text
pratiyogin
anuyogin
sambandha
```

could inform **proposition-internal technical semantic representation**.

But it does not replace:

```text
Proposition
Inference
Commitment
Attack
Argument
ArgumentSynthesis
```

Think:

```text
inside Proposition.content
```

not:

```text
new master IR
```

---

# 26. STANDARDS VS MOAT

This distinction should be permanent:

```text
STANDARDIZATION LAYER
SEPIO
PROV-O
xAIF
nanopub
ORCID
DOI
        ↓
makes Pāṭala legible + portable


PĀṬALA DOMAIN/TRUST LAYER
Sanskrit provenance
philological alignment
argument reconstruction
epistemic ceilings
crux propagation
review history
scholar adjudication
        ↓
the actual intellectual moat


ECONOMIC/NETWORK LAYER
scholar identity
durable credit
usage graph
intellectual territory
dividend
        ↓
network moat
```

Adapters outward.

Never reshape canonical Pāṭala objects around external standards.

---

# 27. CURRENT INTEGRATION DOC

Agent 1 wrote:

```text
docs/integrations/ARGUMENT-EVIDENCE-STANDARDS-ALIGNMENT.md
```

It captures:

* SEPIO;
* xAIF;
* nanopubs;
* SPARE;
* SCL;
* deferred FoVer/VPR;
* TantraFact;
* “what these do not establish”;
* adapter-not-ontology principle.

Recommendation was to commit this as a **docs-only commit** to the `a1b` branch because the worktree is unstable.

Do not let it interrupt C.1.

---

# 28. GIT STATE — IMPORTANT

A genuine branch fork occurred.

Original:

```text
origin/agent1-argument-layer
```

was stuck around:

```text
44fdabb
→ a3cb27f
→ 1b91898
```

while the newer work lived on a divergent line involving Agent 2 state.

Agent 1 correctly did **not** force-push.

Safe current branch:

```text
origin/agent1-argument-layer-a1b
```

Important commits:

```text
0efc1df
Commit A.1
canonical ArgumentSynthesis provenance fixes

32083e6
Commit B
EO projection

d8b123b
Commit B refinement / monotone projection proof

32563bc
Git reconciliation handoff

a2c4591
Commit C
actual essay + SentenceEvidenceAudit

398958f
Commit C refinement
EssayPlan + attribution + sentence roles
```

Git reconciliation handoff:

```text
handover/agent-1-ml/GIT-RECONCILIATION-2026-08-12.md
```

Until Agent 0 deliberately reconciles branches:

> Treat `origin/agent1-argument-layer-a1b` as Agent 1's authoritative execution line.

Do not force-push or casually rewrite history.

The worktree has repeatedly reverted files unexpectedly.

Remote state is safer than assumed local state.

---

# 29. IMPORTANT PEER-REVIEW BUGS THAT HAVE ALREADY BEEN FIXED

These are useful because they show recurring failure modes.

## Fake negative test

Earlier code mutated an object but ran validation against the unchanged disk object.

Lesson:

> A negative test must actually send the mutated object through the production validator.

## Stale `gid`

Evidence provenance accidentally pointed to the wrong gold argument.

Lesson:

> Build provenance from authoritative proposition maps, never ambient loop variables.

## Missing refs represented as fake content

A fallback such as:

```python
"(missing)"
```

was truthy and therefore slipped through.

Lesson:

> Missing evidence must hard fail.

## Structural acceptance laundered as evidential support

Earlier EO effectively collapsed:

```text
gate passed
→ evidence accepted
```

Fixed by separate fields:

```text
structural_gate_outcome
epistemic_status
```

## Hardcoded render ceiling

Fixed by dependency-driven propagation.

## Fake audit IDs

Prototype synthesis invented IDs that merely looked legitimate.

Fixed by:

```text
NOT_AUDITED
audit_refs = []
```

until persistent objects exist.

## Hardcoded epistemic status table

Prototype manually restated proposition statuses.

Fixed by resolving states from actual gold/proposition objects.

## Vacuous symbol-table check

Earlier inference validation contained a condition that could logically never fire.

Lesson:

> Always inspect whether a test's predicate can actually become false.

## Synthesis input membership trusted itself

Fixed by verifying:

```text
argument_ref + proposition_ref
```

against the authoritative registry.

## `STRUCTURALLY_COHERENT` asserted without evaluation

Fixed to:

```text
NOT_EVALUATED
```

until an actual computation supports the stronger status.

## `boundary.establishes`

Too strong under unresolved synthesis.

Changed toward:

```text
currently_supports
```

with explicit status.

These are not trivial implementation bugs. They are recurring patterns of **epistemic theatre**.

---

# 30. DO NOT REOPEN THESE AREAS

Unless a concrete failure requires it, Agent 1 should not:

* re-audit the five golds;
* expand Nyāya;
* tune viruddha again;
* restart systematic corroboration;
* build another evidence matrix;
* generalize ResearchPack;
* generalize EO;
* build bulk essay generation;
* add embedding/ranking systems;
* add LLM judges;
* build DSPy/HippoRAG/PPR;
* build crux ML;
* build argument ranking;
* reshape canonical objects for external standards.

One vertical first.

---

# 31. AGENT 2 IS A SEPARATE CONCURRENT LANE

Do not accidentally send Agent 1 back into Agent 2 work.

Agent 2 owns:

```text
raw Sanskrit
→ source-preserving MACHINE_PROPOSED L0
```

especially:

```text
pipeline/raw_l0.py
```

with requirements:

* 100% source character accounting;
* exact span round-trip;
* originals untouched;
* analyzer disagreement preserved;
* uncertainty/abstention;
* no T1/L2/C1 generation at this stage;
* deterministic audit artifact.

Agent 1 should not re-audit Agent 2 or build the translation factory.

The lanes meet because Agent 2 expands trustworthy substrate and Agent 1 expands trustworthy reasoning/output.

---

# 32. REVIEW THE FIRST ESSAY ON TWO COMPLETELY DIFFERENT AXES

This is critical.

### Axis A — epistemic integrity

Ask:

* does every load-bearing sentence resolve?
* does synthesis reasoning go through its warrant?
* are attributions correct?
* are unresolved statuses preserved?
* are boundaries visible?
* are rivals sourced appropriately?
* is paraphrase conservative?

### Axis B — intellectual/writing quality

Ask:

* is this interesting?
* is it philosophically sharp?
* does it actually explain something?
* is it repetitive?
* is the framing historically responsible?
* does it state the strongest objection?
* is it readable?
* would a scholar learn anything?
* does the essay feel like a database rendered into prose?

Passing A while failing B is still a product failure.

---

# 33. THE FIRST ESSAY'S CURRENT INTELLECTUAL CLAIM

Keep it narrow.

Question:

> Does reflexivity belong intrinsically to manifestation?

Local materials:

### ARG-002

Roughly:

> Linguistic articulation does not show that the underlying self-awareness is itself constructed by conceptual determination.

### ARG-004

Roughly:

> Conscious manifestation is distinguished from inert showing by reflexive awareness / vimarśa.

### Synthesis

Potential bridge:

> Taken jointly, these motivate treating reflexivity as intrinsic to manifestation.

But:

```text
SYN-INF-001 = RECONSTRUCTED
support = UNRESOLVED
```

So do **not** derive:

* universal Self;
* one consciousness;
* consciousness fundamental;
* full Śaiva metaphysics.

Those remain separate claims.

---

# 34. MAIN PAPER CONTEXT

Longer-term Agent 1 work feeds the user's main paper:

**Recognition, or the Felt Re-cognition of the Self**

Core idea:

> Recognition may be the event where felt/valenced experience, cognitive re-cognition and a consciousness-primary metaphysics converge, followed by a restructuring of perception.

Broad structure:

```text
PART I — THE EVENT
recognition
camatkāra / felt character
Solms / feeling / uncertainty
convergence

PART II — AFTER
perceptual rerendering
active inference / Seth / Levin
Ñāṇavīra / Ñāṇananda
transformed subject

PART III — IMPLICATIONS
what follows, carefully bounded
```

But do not jump there until the small reflexion-core vertical proves the method.

---

# 35. WHAT ELAD SHOULD DO AS REVIEWER

Your job is not to help Agent 1 build faster at any cost.

Your job is to attack places where architecture can generate **false confidence**.

Repeated questions to ask:

### Object level

```text
Where did this field actually come from?
```

### Inference level

```text
What warrant makes these premises support this conclusion?
```

### Status level

```text
Which exact dependency earned this status?
```

### Provenance level

```text
Does this reference resolve to the claimed object?
```

### Test level

```text
Does this negative test actually exercise the production path?
```

### Scholarship level

```text
Does the cited scholar address this exact proposition?
```

### Prose level

```text
Does this sentence say more than its claim_ref?
```

### Architecture level

```text
Is this component doing reasoning it should merely project?
```

### Scope level

```text
What stronger claim would a careless reader infer here?
```

### Product level

```text
Would a scholar care?
```

---

# 36. NEAR-TERM EXECUTION ORDER

Current recommended order:

```text
NOW
│
├─ commit standards integration doc as docs-only
│
├─ C.1 prose-faithfulness refinement
│    ├─ fix S003
│    ├─ fix S004
│    ├─ fix/reclassify S007
│    └─ add CLAIM_SURFACE_INFLATION / PARAPHRASE_EXPANSION test
│
└─ peer-review actual essay
     ├─ epistemic integrity
     └─ philosophical/writing quality
```

Then, assuming first vertical is good:

```text
scholar-stamp invariant contract
        ↓
SEPIO/PROV-O alignment contract
        ↓
xAIF round-trip adapter
        ↓
tiny human-adjudicated TantraFact pilot
```

I would now put **scholar-stamp ahead of xAIF strategically**, even though xAIF is the cheapest technical integration.

Reason:

> xAIF gives interoperability.
> Scholar-stamp creates the core expert incentive/reputation loop.

---

# 37. THE DEEPEST CURRENT PRODUCT HYPOTHESIS

Pāṭala could become valuable because in an AI-rich world:

```text
generation becomes cheap
```

while:

```text
trusted adjudication becomes scarce
```

The scarce asset becomes:

> Who reviewed this claim? Against what evidence? At what version? With what exact judgment? What later work depends on it? What changed after disagreement?

Pāṭala can turn that into a graph.

The scholar therefore becomes a high-value node, not merely a content supplier.

This is the direction where the technical architecture, scholarly vision and economics converge.

---

# 38. ONE-SENTENCE HANDOVER

> **Agent 1 has successfully built the first source→argument→synthesis→EO→essay→sentence-audit vertical, but the newest and most important

I reviewed the live GitHub branch topology, recent commit histories, cross-agent handover log, branch comparisons, and the actual argument/evidence commits. The previous summary was materially incomplete.

The key realization is that **Pāṭala has undergone two parallel transformations at once**:

1. **Agent 2 turned the Sanskrit/corpus substrate into a proof-carrying source layer and then expanded outward into corpus acquisition + historical atlas work.**
2. **Agent 1 turned the philosophical layer from “five hand-built gold arguments” into an epistemically constrained chain that can synthesize an argument, project it into an Evidence Object, and generate prose without silently strengthening claims.**

And the newest `agent1-argument-layer-a1b` branch is not an independent fork floating beside Agent 2. It **contains Agent 2’s current head and then adds six Agent-1 argument-layer commits on top of it**. GitHub reports `agent1-argument-layer-a1b` as exactly 6 commits ahead of `agent2`, with `agent2` itself as its merge base.

So the actual lineage is much cleaner than the branch names make it look.

---

# 1. Current Git topology

The important heads I found are:

| Branch                      | Head      | Meaning                                        |
| --------------------------- | --------- | ---------------------------------------------- |
| `main`                      | `e9e938e` | old integration checkpoint                     |
| `agent1`                    | `cdfd467` | independent-model-reviewed five argument golds |
| `agent2`                    | `03aba5e` | huge integration/L0/corpus/history lane        |
| `agent1-argument-layer`     | `1b91898` | initial canonical ArgumentSynthesis line       |
| `agent1-argument-layer-a1b` | `398958f` | **latest reconciled full vertical**            |

`main` stopped at the moment Agent 2 closed the first end-to-end Sanskrit→C1 proof seam. That commit explicitly says the vertical object's P0 proof changed from `STALE` to `EXACT / REFERENCE_RESOLVED`, with round-trip passing and zero unresolved references.

Everything important after that has happened off main.

Most significantly:

* `agent2` is **87 commits ahead of `main`**.
* `agent1-argument-layer-a1b` is **93 commits ahead of `main`**.
* those extra six commits are exactly the final argument-synthesis → EO → essay vertical layered on Agent 2's state.

That makes `398958f` the best representation of the integrated technical state I found.

---

# 2. The journey actually starts with the Sanskrit floor

A lot of what happened looks like “ML work,” but the most important architectural development was Agent 2 discovering that the Sanskrit substrate itself was not yet audit-grade.

The handoff log records a serious bug in the early L0 representation:

* `char_start` / `char_end` were calculated against the whole joined chunk,
* `source_text` contained only the local line,
* therefore **2187/2187 records could not resolve their stored offsets against their stored `source_text`**,
* hundreds of lines had token-span gaps,
* but crucially, the underlying extracted content was still correct when indexed against the full chunk.

That was not cosmetic. It meant the purported Sanskrit evidence coordinate system could not actually support the “click from argument down to the Sanskrit span” promise.

Agent 2 then repaired that at the representation level rather than patching consumers.

The new model became:

```text
chunk
  ├── absolute chunk_char_start/end
  ├── relative line_char_start/end
  ├── exact raw_fragment
  ├── source hash
  └── explicit coverage classification
```

and `verify_l0.py` began producing deterministic P0 proof objects containing:

```text
source_sha256
span_integrity
ordering
coverage
roundtrip
```

with failure rather than silent omission when those invariants break.

This was one of the foundational moves in the project.

---

# 3. L0 went from partial extraction to an actual proof floor

The repair then became systematic.

Agent 2 fixed tokenizer loss around:

* closing parentheses,
* blockquote wrapping,
* capitalization of `[And]-`,
* punctuation/quotes inside glosses,
* multi-line source attribution,
* editorial markers,
* uppercase IAST,
* irregular reviewed exceptions.

The flagship V2/V3 IPVV corpus eventually reached:

> **35/35 chunks P0 PASS, zero unknown characters, exact spans, no overlaps, complete classification.**

The handoff explicitly calls this **LOSSLESS** for the flagship V2/V3 source layer.

Then the separate V1 legacy format got its own extractor rather than being forced into a V2/V3 parser.

That matters because the architecture evolved away from:

> “make Sanskrit machine-readable”

toward:

> **“every Sanskrit transformation carries a machine-verifiable proof of what was preserved, classified, omitted, or remains open.”**

That distinction is absolutely central to the moat you have been trying to build.

---

# 4. Agent 2 also established an important “adequacy doctrine”

This is another major conceptual advance hidden in the commits.

Agent 2's later work explicitly added the rule:

> a supporting component should stop once it is adequate for its consumer; uncertainty should be propagated rather than artificially eliminated.

That principle appears around the P4 L0↔L2 work. The resulting alignment witness achieved about:

* resolution recall ≈ **0.93**
* precision ≈ **0.89**
* abstention ≈ **1.0**
* an independent Vidyut analyzed-only agreement of ≈ **0.81**

and was deliberately frozen as a **SUPPORTED_MACHINE_WITNESS**, not upgraded to some grand “verified translation alignment” claim.

This doctrine then appears implicitly throughout the argument layer:

```text
do not make every subsystem perfect
        ↓
make its uncertainty explicit
        ↓
carry that uncertainty upward
        ↓
prevent downstream components from claiming more
```

That is becoming the unifying Pāṭala epistemic philosophy.

---

# 5. The morphology experiments are unusually important because Agent 2 allowed negative results

The Vidyut P2 morphology work did not magically “prove Sanskrit.”

The first full pass produced roughly:

* 28.2% confirmed,
* 26.9% ambiguously supported,
* 29.5% conflict,
* 11.8% unanalyzed.

But investigation showed much of the apparent conflict was representational: L0 stored surface forms while Vidyut often returned stems or compound analyses.

A second independent Heritage witness was then used.

On the first 500-record ensemble:

* control agreement ≈ **85%**
* around **72% of Vidyut conflicts were resolved by Heritage**
* the genuinely double-conflicting portion fell to roughly **8%**

and the larger 4,600-record run was broadly stable:

* control agreement ≈ **84.1%**
* conflict resolution ≈ **71.6%**
* double conflict ≈ **9.2%**

The important outcome was not “P2 solved morphology.”

It was:

> **P2 became a calibrated machine witness with a sharply defined human-review frontier.**

The handoff explicitly refuses to promote it to human-validated status until blind review occurs.

That is exactly the kind of epistemic discipline Pāṭala needs.

---

# 6. The old Sanskritree engine was mined rather than blindly reused

Another good architectural decision: Agent 2 audited the old Sanskritree engine and separated genuinely reusable modules from dead architecture.

Reusable pieces identified included:

* lexical-sense ranking,
* alignment span types,
* analysis-lattice / analyzer adapters,
* failure taxonomies.

But the old LLM translation/factor-graph machinery and old Lean/Nyāya proof direction were explicitly treated as superseded or non-authoritative.

This is important because Pāṭala is no longer trying to become:

> “a better Sanskrit translation model.”

It is becoming:

> **a substrate where translations, interpretations and arguments have typed provenance and contestable epistemic states.**

---

# 7. P3 produced an important negative result too

Agent 2 constructed an initial lexical-sense benchmark and tested the inherited ranker.

The old ranker scored around **0.76 top-1**, while a much simpler lexical/embedding baseline reached about **0.81** and handled abstention substantially better.

So the existing ranker was **not promoted**.

The project recorded that as a formal negative result instead of pretending the sophisticated subsystem was useful.

That is another sign the repository is developing something much more valuable than feature count:

**an internal culture of epistemic anti-theatre.**

---

# 8. Meanwhile Agent 1 built the five philosophical gold objects

On the philosophical side, the first breakthrough was the set of five IPVV argument golds.

But the critical development was not simply creating them.

A separate model review was run and persisted as a `ReviewEvent`, explicitly marked:

```text
reviewer_kind = AI_MODEL
scope = RECONSTRUCTION_CONSISTENCY
status = MODEL_INDEPENDENT_REVIEWED
NOT specialist-reviewed
```

The review revised four arguments and rejected one as textual gold.

The changes reveal the IR becoming much sharper.

### ARG-001

A speculative regress/transcendental layer was removed.

The knower/Lord identification was reclassified from inference to **grounding**.

### ARG-002

The Buddhist reply stopped being represented as a simple objection/reply inference.

It became a **conceptual distinction**, while the dialectical relation remained `RESPONDS_TO`.

The implicit bridge was changed to:

`IMPLIES_ON_RECONSTRUCTION`

rather than pretending it was an explicit textual premise.

### ARG-003

This was the most important correction.

It was demoted entirely from textual gold to:

`ALT_RATIONAL_RECONSTRUCTION`

because the regress reasoning was editorial rather than present as a textual argument.

### ARG-004

The identification between parā-vāk and lordship was reclassified as **TEXTUAL GROUNDING**, not inference.

### ARG-005

Again, objection → answer was separated from inference and represented as a dialectical relation.

The systematic cross-passage reading was grounded across passages instead of represented as if it were locally derived.

The review distilled four IR lessons:

```text
inference ≠ dialectical relation
grounding ≠ inference
support_scope must be explicit
reconstruction force must be explicit
```

That is a major ontology maturation.

---

# 9. Agent 1 and Agent 2 then actually met at the proof seam

This is where the project stops looking like two unrelated agents.

Agent 1's gold objects consumed Agent 2's L0/P0 proof references.

The mainline integration commit recorded that Agent 2 regenerated the authoritative proof and the Agent-1 vertical object changed:

```text
STALE
   ↓
EXACT / REFERENCE_RESOLVED
```

with zero unresolved references.

So for the first time the chain became genuinely traversable:

```text
Sanskrit
↓
L0 token/span
↓
P0 proof
↓
passage
↓
C1/L2 interpretation
↓
argument proposition
↓
inference
```

That is the true first Pāṭala vertical.

---

# 10. The original Agent-1 branch stops here for a reason

`agent1` ends at `cdfd467`.

That branch contains the independently model-reviewed golds, but not the later synthesis → EO → prose work.

The reason later branches exist is that the project then moved from:

> **represent arguments correctly**

to:

> **determine whether those epistemically constrained argument objects can safely drive higher-order synthesis and natural-language output.**

That demanded another architectural layer.

---

# 11. The first ArgumentSynthesis attempt was explicitly thrown away

This is one of the most important details in the newer history.

The `agent1-argument-layer` branch at `1b91898` says the canonical synthesis was rebuilt because the earlier prototype was disposable.

The new rule was:

> **derive the synthesis from actual stored objects, never from hardcoded prototype statuses.**

That commit introduced the real synthesis object:

`SYN-IPVV-REFLEXION-CORE-001`

Its crucial properties were:

### Epistemic state is resolved from source objects

No hardcoded map such as:

```python
PROP_EPISTEMIC_STATUS = {...}
```

Instead each dependency resolves to the source gold object's actual current state.

### Missing audits remain missing

There were no persisted `ContextualArgumentAudit`s.

So dependencies say:

```text
audit_state = NOT_AUDITED
audit_refs = []
```

rather than inventing review objects.

### Thesis identity is graph-native

`SYN-CONC-001` is not merely a prose sentence.

It is the actual conclusion node of `SYN-INF-001`.

### Origin and support are different dimensions

This is subtle and extremely important.

The synthesis bridge can be:

```text
origin = RECONSTRUCTED
support_state = UNRESOLVED
```

Those are not collapsed into one label.

A reconstruction can have evidence; evidence can remain unresolved.

### Only load-bearing dependencies govern the ceiling

The synthesis has:

```text
LOAD_BEARING_PREMISE
LOAD_BEARING_INFERENCE
```

and the epistemic ceiling is computed by `WEAKEST-GOVERNS` over those dependencies.

Themes remain metadata rather than getting accidentally promoted to premises.

This is a very good design.

---

# 12. Peer review immediately found additional provenance seams

The next commit, `0efc1df`, is essentially “ArgumentSynthesis v1 was directionally right but still too trusting.”

It tightened:

* argument-ref/proposition-ref pairing,
* existence checking against the authoritative gold symbol table,
* structural audit state,
* internal consistency claims,
* boundary language.

Most importantly, it separated **structural audit state** from **epistemic ceiling**.

So now these are independent axes:

```text
epistemic_ceiling = UNRESOLVED

structural_audit_state = INCOMPLETE
```

That is a deep conceptual improvement.

It means:

> “the evidence does not justify certainty”

and

> “we have not formally audited the argument structure”

are no longer conflated.

The commit also removed an unjustified hardcoded:

`STRUCTURALLY_COHERENT`

and replaced it with:

`NOT_EVALUATED`.

And boundary language shifted from:

`establishes`

to the deliberately weaker:

`currently_supports`.

GitHub's compare shows this as the first of the six commits on top of Agent 2.

---

# 13. Commit B is where the architecture becomes genuinely powerful

The next major stage is:

`ArgumentSynthesis → Evidence Object v2`

But the project deliberately refused to let EO become another independent reasoning system.

The commit message says explicitly:

> EO is a **projection** of canonical `ArgumentSynthesis`, not a fresh builder that runs another gate.

This is exactly the right abstraction.

The invariant became:

[
authority(P(x)) \le authority(x)
]

where (P) is projection into the downstream representation.

In plain terms:

> **No downstream representation is allowed to become more certain than its source.**

That could end up being one of Pāṭala's core invariants.

---

# 14. The EO layer is therefore intentionally monotonic

Commit B derives EO evidence directly from synthesis dependencies.

It preserves:

```text
structural_gate_outcome ≠ epistemic_status
```

and enforces:

```text
if structural_audit_state == INCOMPLETE
then structural_gate_outcome = NOT_AUDITED
```

Never magically:

`accepted`.

Likewise, with an unresolved synthesis ceiling, the EO's conclusion cannot become:

`grounded`,
`proven`,
or equivalent.

The EO must instead remain something like:

`structurally_suggestive`

with rendering constrained toward qualification or abstention.

The reconstructed synthesis bridge is carried through explicitly as an inference with a warrant rather than being flattened into prose.

---

# 15. Commit B refinement adds adversarial anti-laundering

Then `d8b123b` turns that projection design into a real anti-inflation proof.

The explicit organizing rule becomes:

> `MONOTONE_NO_STRENGTHENING`.

It then tests the obvious failure modes.

### Manufactured structural acceptance

If a downstream object says an unaudited dependency was “accepted”, validation fails.

### Epistemic strengthening

If an unresolved synthesis becomes `strongly_supported`, validation fails.

### Invented provenance

If EO cites a source outside the synthesis dependency closure, validation fails.

### Boundary deletion

The universal-Self boundary must survive projection.

Dropping it fails validation.

### Inference laundering

A bridge marked:

`RECONSTRUCTED`

cannot become:

`ASSERTED`

simply because it moved into EO.

### Rival laundering

An unsourced Buddhist opponent stays:

`UNSOURCED_RECONSTRUCTION`.

It cannot silently become a live, sourced rival.

The actual EO extension records this distinction.

This is extremely consequential.

Pāṭala is no longer merely storing provenance.

It is beginning to enforce **epistemic conservation laws across representation changes**.

---

# 16. Commit C proves the difficult part: prose

This is where the repository becomes much more interesting than a graph project.

`a2c4591` asks:

> Can readable prose be generated from the constrained object **without rhetoric destroying its epistemic distinctions?**

The result is a ~380-word real essay on:

> whether reflexivity belongs intrinsically to manifestation.

The mini-essay contains:

```text
problem
ARG-002
ARG-004
synthesis
validity-vs-soundness limitation
boundary
unsourced rival
```

and every load-bearing sentence carries metadata such as:

```text
claim_refs
inference_refs
source_refs
render_mode
speaker
assertion_strength
```

The core trick is that **only load-bearing sentences require full epistemic chains**.

Transitions and stylistic prose can remain natural.

That prevents the essay from becoming unreadable metadata soup.

The commit then introduces five adversarial prose mutations:

```text
A. strength inflation
B. authorship laundering
C. boundary erasure
D. rival laundering
E. warrant erasure / bypass
```

and each must deterministically fail.

The commit itself states the proper narrow claim:

> For one IPVV synthesis, Pāṭala can produce a provenance-linked essay and deterministically catch specified epistemic-laundering mutations.

It explicitly says this does **not** establish that Pāṭala generally writes reliable scholarly essays.

This is one of the strongest commits in the repository.

---

# 17. The final refinement makes authorship laundering even harder

`398958f`, the current integrated head, adds two especially useful pieces.

First, an `EssayPlan` mapping sections to sentences.

It is deliberately not generalized into a grand schema yet.

Second, each sentence now has explicit attribution:

```text
SYNTHESIS
AUTHOR
```

This allows the checker to catch a reconstructed synthesis proposition being rhetorically attributed to Abhinavagupta.

That is a very real scholarly failure mode:

```text
Pāṭala reconstructed X from A + B
        ↓
essay renderer writes
“Abhinavagupta argues X”
```

even though Abhinavagupta never explicitly made X.

The new checker rejects exactly that laundering.

The same commit also exercises:

```text
LOAD_BEARING
EXPLANATORY
TRANSITION
SIGNPOST
```

so the provenance requirement is sensitive to rhetorical function rather than naively applying to every sentence.

And the thesis carries:

`assertion_strength = SUGGESTIVE`

because its ceiling remains unresolved.

---

# 18. The integrated vertical now looks like this

This is the strongest way I would represent current Pāṭala:

```text
                        SOURCE LAYER
                             │
                             ▼
                    Sanskrit witness
                             │
                             ▼
                 exact L0 token/span IDs
                             │
                             ▼
                    P0 lossless proof
                             │
                             ▼
                         passage
                             │
                             ▼
                      C1 / L2 reading
                             │
                             ▼
               ┌─────────────────────────┐
               │   ARGUMENT GOLD OBJECT  │
               │                         │
               │ proposition             │
               │ grounding               │
               │ inference               │
               │ dialectical relation    │
               │ commitment force        │
               │ support_scope           │
               │ crux                     │
               └────────────┬────────────┘
                            │
                            ▼
                 independent MODEL review
                            │
                            ▼
                  ArgumentSynthesis
                            │
          ┌─────────────────┴─────────────────┐
          │                                   │
          ▼                                   ▼
 resolved dependency graph           epistemic ceiling
          │                                   │
          └──────────────┬────────────────────┘
                         ▼
                   SYN-INF-001
                         │
                         ▼
                   SYN-CONC-001
                         │
                         ▼
                  Evidence Object
                 monotone projection
                         │
                         ▼
                     EssayPlan
                         │
                         ▼
                  readable essay
                         │
                         ▼
              SentenceEvidenceAudit
                         │
              adversarial mutations
                         │
                         ▼
               PASS / epistemic FAIL
```

That is no longer just architecture diagrams.

**Each major transition now has at least one executable vertical witness.**

---

# 19. Agent 2 did not stop at L0

The recent Agent-2 branch also grew the corpus itself.

One later commit acquired a set of Śaiva source witnesses, including texts such as:

* Gaṇakārikā,
* Sūkṣmasvāyambhuva,
* Sarvajñānottara,
* Siddhāntasārapaddhati,
* Prāyaścittasamuccaya,
* Jñānaratnāvalī,
* Piṅgalāmata,
* Dviśatikālottara,
* Śivadharmaśāstra,
* Śivadharmottara,
* Īśānaśivagurudevapaddhati,

and seeded **135 bibliography records** into the atlas while maintaining an explicit acquisition-status/couldn't-get register.

That is exactly the right direction for scaling beyond “IPVV as special-case demo.”

---

# 20. And Agent 2 began turning the corpus into historical structure

The current `agent2` head is the **Śiva Source Tree**.

It introduces a diachronic history model spanning roughly:

```text
PIE
→ Proto-Indo-Iranian
→ Vedic Rudra
→ Pāśupata
→ Mantramārga
→ Śaiva Siddhānta
→ Bhairava
→ Kaula
→ Krama
→ Trika
```

plus:

* Buddhist pramāṇa,
* Nyāya,
* an Indus parallel branch,
* transformation chains,
* bibliography anchors,
* periods/epistemic eras,
* a ten-hop acquisition roadmap.

Crucially, the commit says the schema is **provisional and non-canonical**.

That is the correct status.

It is not pretending that a clean historical graph is itself settled historiography.

It is an atlas/navigation substrate that can later attach:

```text
texts
scholarship
translations
arguments
evidence
uncertainty
```

---

# 21. What Agent 1 and Agent 2 have actually become

The original division was something like:

```text
Agent 1 = ML / argument
Agent 2 = integration / Sanskrit
```

That description is now too shallow.

I would describe the mature division as:

## Agent 2 — epistemic substrate

Agent 2 increasingly owns the **world that claims resolve into**:

```text
source acquisition
text witnesses
L0
span proof
morphology witnesses
alignment witnesses
bibliography
historical corpus topology
API/product integration
```

Its question is essentially:

> **What exactly exists, where did it come from, and can I resolve it reproducibly?**

## Agent 1 — epistemic transformation

Agent 1 increasingly owns the **rules governing what may be said from that substrate**:

```text
argument reconstruction
grounding
inference
commitment
review
synthesis
cruxes
epistemic ceilings
projection
essay rendering
anti-laundering
```

Its question is:

> **Given what we have, what are we actually justified in claiming?**

That is an excellent division.

---

# 22. The real architecture is therefore emerging as two coupled proofs

Pāṭala is converging toward two different forms of proof.

### Proof downward

> Can this claim resolve all the way down to its actual textual substrate?

```text
claim
→ proposition
→ grounding
→ passage
→ L0
→ exact Sanskrit span
→ source hash
```

Agent 2 has made that increasingly strong.

### Proof upward

> Can this evidence pass through interpretation, synthesis and prose without becoming stronger than its source warrants?

```text
source claim
→ argument
→ synthesis
→ EO
→ essay sentence
```

Agent 1 has now made this executable.

The combination is the interesting thing.

Neither alone is Pāṭala.

---

# 23. This reframes what the moat actually is

I would now formulate the technical moat more strongly than before.

It is not merely:

> corpus + graph + provenance.

It is:

[
\text{Pāṭala moat}
==================

\text{resolution depth}
\times
\text{epistemic monotonicity}
\times
\text{review history}
\times
\text{scholarly adjudication}
\times
\text{network adoption}
]

The unusual component is **epistemic monotonicity**.

A lot of knowledge systems can tell you where a sentence came from.

Pāṭala is beginning to answer:

> **Did that sentence become more authoritative while passing through reconstruction, synthesis, serialization, or rhetoric?**

That is a much harder and more valuable problem.

---

# 24. What is genuinely done now

I would classify the project as follows.

### Source substrate

**Strong prototype / near-foundational**

* IPVV P0 lossless floor.
* Exact source resolution.
* Stable passage/spans.
* Proof objects.
* Reproducible source hashes.

### Morphology/alignment

**Calibrated machine witnesses**

Useful enough for downstream work, deliberately not overclaimed.

### Argument IR

**Real and tested**

Five gold arguments exist.

They survived an independent model reconstruction-consistency review and changed substantially because of it.

### Argument synthesis

**Real vertical proven once**

Actual object resolution.

Explicit load-bearing dependency graph.

Weakest-governs ceiling.

Explicit reconstructed bridge.

### EO projection

**Real vertical proven once**

Projection, not independent derivation.

Monotone no-strengthening.

Boundary/crux preservation.

Anti-laundering tests.

### Essay generation

**Real vertical proven once**

Readable prose exists.

Load-bearing sentences resolve backward.

Five adversarial corruption classes are caught.

### Historical atlas

**Promising but provisional**

Useful navigation/product substrate.

Not canonical historiography.

### Human specialist validation

**Still the largest missing epistemic layer.**

---

# 25. The most important thing that is *not* done

There is still a potentially dangerous gap between:

```text
MODEL_INDEPENDENT_REVIEWED
```

and:

```text
SPECIALIST_REVIEWED
```

The repository itself is being admirably explicit about this.

The gold review says **not specialist-reviewed**.

The prose commit says **do not generalize** from one essay.

The morphology layer says machine calibrated, not human validated.

Those caveats should remain first-class.

They are not weaknesses to hide.

They are exactly how Pāṭala distinguishes itself from systems that turn “the model agreed with itself” into “verified scholarship.”

---

# 26. I would freeze several invariants now

After looking across the whole journey, I would treat these as near-core constitution-level principles.

```text
I1. No proposition without provenance or explicit reconstruction status.

I2. Grounding is not inference.

I3. Dialectical relation is not inference.

I4. Origin status and evidential support are orthogonal.

I5. Structural validity and epistemic support are orthogonal.

I6. The weakest load-bearing dependency governs the ceiling.

I7. Downstream projections may preserve or weaken authority,
    never strengthen it.

I8. Boundaries and cruxes are first-class information;
    projection may not erase them.

I9. Unsourced opponents remain visibly unsourced.

I10. Machine review, specialist review, and textual evidence
     are distinct forms of authority.

I11. Rhetorical fluency grants zero epistemic privilege.

I12. Missing review means NOT_AUDITED, not presumed valid.
```

These are much more important now than adding another 30 ontology node types.

---

# 27. I would also freeze the branch interpretation

The practical branch state appears to be:

```text
main
  │
  └── e9e938e
       │
       ├── agent1
       │    └── cdfd467
       │         model-reviewed five golds
       │
       └── long integration history
             │
             └── agent2
                  └── 03aba5e
                       L0 + witnesses + corpus + history
                       │
                       └── agent1-argument-layer-a1b
                            ├── 0efc1df  synthesis hardening
                            ├── 32083e6  EO Commit B
                            ├── d8b123b  monotone B refinement
                            ├── 32563bc  reconciliation handover
                            ├── a2c4591  essay Commit C
                            └── 398958f  attribution/role refinement
```

The original `agent1-argument-layer` head `1b91898` is useful historically because it records the canonical synthesis rebuild, but **`a1b` is the more complete path now**.

---

# 28. What I think has happened strategically

The project started from:

> “We translated a monster Sanskrit work. How do we make this valuable?”

Then it became:

> corpus + provenance + translation infrastructure.

Then:

> philosophy graph + arguments + benchmarks.

But the recent work has converged on something sharper:

> **Pāṭala is infrastructure for preserving warranted authority as knowledge moves from source → interpretation → argument → synthesis → public explanation.**

That applies far beyond Sanskrit eventually.

But Sanskrit/Tantra is actually a very good place to establish it because the problem is unusually difficult:

* manuscripts/editions disagree,
* translations are interpretive,
* technical vocabulary shifts,
* traditions dispute one another,
* scholars reconstruct unstated arguments,
* later commentators reinterpret earlier thinkers,
* modern writers routinely collapse all of this into prose.

If Pāṭala works there, easier domains become plausible.

---

# 29. The next technical challenge is not another serializer

Given the state of the repo, I would **not** make xAIF, SEPIO, nanopub, ASPIC+, or another ontology the next major engineering campaign.

The repo has finally reached the stage where it needs **independent adversaries** more than new abstractions.

The strongest next experiment is:

```text
choose 3–5 vertical arguments
        │
        ├── one straightforward textual argument
        ├── one cross-passage reconstruction
        ├── one Buddhist objection/reply
        ├── one contested scholarly interpretation
        └── one argument where Pāṭala should abstain
        │
        ▼
give packets to specialists
        │
        ▼
capture disagreements as structured ReviewEvents
        │
        ▼
modify the objects
        │
        ▼
rerun synthesis → EO → essay
        │
        ▼
measure whether corrections propagate automatically
```

That last part is the **killer test**.

Not merely:

> “Can a scholar review an argument?”

But:

> **If a scholar changes one load-bearing judgement at the bottom, does the epistemic consequence propagate all the way into the final prose without human repair?**

If Pāṭala demonstrates that convincingly, the architecture moves from “interesting” to genuinely distinctive.

---

# 30. The flagship demo I would build

A Pāṭala user should eventually see an essay sentence such as:

> “The available passages suggest that reflexivity belongs intrinsically to manifestation…”

and be able to expand it into:

```text
WHY “suggest”?

epistemic ceiling
└── UNRESOLVED

because
└── SYN-INF-001
    ├── G2-CONC
    │   └── ARG-GOLD-002
    │       └── exact IPVV passage
    │           └── Sanskrit span
    └── G4-CONC
        └── ARG-GOLD-004
            └── exact IPVV passage
                └── Sanskrit span

bridge status
└── RECONSTRUCTED

structural audit
└── INCOMPLETE

does not establish
├── universal Self
├── all manifestation = one consciousness
└── consciousness is fundamental simpliciter

reviews
├── builder model
├── independent model
└── specialist: pending
```

Then imagine a scholar rejecting `G4-CONC`.

The visible sentence automatically weakens or disappears.

**That is the product.**

The essay is merely one view over the evidence graph.

---

# 31. My revised state assessment

After this Git review, I would score the project differently from my previous answer:

```text
SOURCE IDENTITY / PROVENANCE       ██████████
L0 LOSSLESS FLOOR                  ██████████
MACHINE PHILOLOGY WITNESSES        ████████░░
PASSAGE / C1 RESOLUTION            ██████████

ARGUMENT IR                        █████████░
ARGUMENT GOLD                      ████████░░
MODEL INDEPENDENT REVIEW           █████████░
SPECIALIST REVIEW                  ██░░░░░░░░

ARGUMENT SYNTHESIS                 █████████░
EPISTEMIC CEILING PROPAGATION      ██████████
EO MONOTONE PROJECTION             ██████████
BOUNDARY / CRUX PRESERVATION       ██████████

ESSAY GENERATION                   ████████░░
SENTENCE EVIDENCE AUDIT            █████████░
ADVERSARIAL LAUNDERING TESTS       █████████░
MULTI-ARGUMENT GENERALIZATION      ███░░░░░░░

CORPUS EXPANSION                   ███████░░░
HISTORICAL ATLAS                   ██████░░░░

SCHOLAR ADJUDICATION NETWORK       ██░░░░░░░░
EXTERNAL STANDARDS                 ██░░░░░░░░
PUBLIC TRUST PRODUCT               ████░░░░░░
```

The important thing is that **the middle of the stack is now much stronger than I realized**.

You already have the beginnings of a real epistemic compiler:

```text
source
  → interpretation
  → argument
  → synthesis
  → projection
  → rhetoric
```

with invariant checking between stages.

That is the most significant architectural progress in the recent repository history.

---

# 32. The single sentence version

**Pāṭala has evolved from a provenance-aware Sanskrit corpus into a proof-carrying epistemic pipeline where Agent 2 establishes what the evidence actually is and Agent 1 enforces how much authority may survive as that evidence is transformed into arguments, synthesis, evidence objects and prose.**

The next moat-defining milestone is no longer “build the graph.”

It is:

> **prove that external scholarly corrections propagate monotonically from Sanskrit evidence all the way to final human-readable claims.**

If that works across a handful of genuinely contested IPVV cases, you have the first convincing version of the thing we have been circling around for the last several conversations: **trust infrastructure for scholarship in the AI era.**

---

# CURRENT DIRECTION (2026-08-13 — supersedes the stale parts above where they conflict)

Agent 1 is **frozen** (vertical peer-review-clean relative to the current objects). The forward work is the
**scholar-corpus foundation**:

- **S0 source-evidence substrate** (`source-evidence/`): Publication → Witness → StableSpan → SourceAssertion →
  CorroborationEvent, composed from standards (FaBiO/PROV-O/Web Annotation/CiTO/RO-Crate/IIIF) and REUSING mature
  open systems (GROBID/Zotero/OpenAlex/OpenCitations/RO-Crate/ORKG/OpenReview). Pāṭala owns only the thin resolver
  + the epistemic seam (SourceAssertion, CorroborationEvent, authority/review, dependency propagation).
- **Scholar oracle:** published scholarship is the scalable scholarly CORROBORATION oracle (can promote matched
  claims to SCHOLARLY_CORROBORATED without a live reviewer) — but it is NOT review/adjudication of Pāṭala's exact
  object. Corroboration is proposition-by-proposition via CorroborationEvents, preserves disagreement, and tracks
  independence (never raw source count).
- **Evaluation plane:** TantraFact / ArgumentBench / PāṭalaQA / CorroborationBench / CitationBench sit OUTSIDE
  the production graph and test it (TantraFact must not be generated from the graph it evaluates). The most
  Pāṭala-native benchmark asks "at what layer does support fail?" (SOURCE → SPAN → ATTRIBUTION → SCOPE → WARRANT →
  CONCLUSION).
- **Two-source-side architecture:** primary text (SOUCE→L0/L1→L2→L200→C1) + scholarship
  (Publication→Witness→Span→SourceAssertion) converge at Proposition ↔ CorroborationEvent ↔ SourceAssertion.

Guiding docs: `source-evidence/docs/` (schema-stack, evaluation-and-ids, reuse-first-stack) + `source-evidence/docs/tools/`.

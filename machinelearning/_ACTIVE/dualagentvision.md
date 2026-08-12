# DUAL-AGENT VISION — Pāṭala as one scholarly derivation graph

Yes. The clean way to think about it is:

> **Pāṭala is one scholarly derivation graph with progressively more powerful pipelines operating over it.**

The visions are not separate products. Translation verification, theme discovery, argument reconstruction, essay generation, adversarial peer review, scholar tooling, MCP, collaborative editions — they are all **different projections and transformations of the same underlying scholarly objects**.

The roadmap should therefore be organized around **which new object/relationship becomes trustworthy enough to exist**, not around flashy features.

## The master architecture

Everything ultimately lives in one graph:

```text
SOURCE
│
├── Witness / Edition
├── Passage
├── SourceSpan
│
▼
L0 ANALYSIS
│
├── Segmentation
├── Morphology
├── Syntax
├── Lexical Sense
├── Alignment
├── PhilologicalProof
│
▼
TRANSLATION
│
├── L2 Reading
├── TranslationDecision
├── Alternatives
├── Review
│
▼
COMMENTARY
│
├── C1
├── InterpretiveAssertion
├── Boundary
│
▼
THEMES
│
├── ThemeProposal
├── Membership
├── Role
├── Tension
│
▼
ARGUMENT
│
├── Proposition
├── Premise
├── Objection
├── Inference
├── Conclusion
├── Qualification
│
▼
SYNTHESIS
│
├── EssayClaim
├── EssayPlan
├── EssaySentence
├── Provenance
│
▼
SCHOLAR WORKBENCH
│
├── Translation Audit
├── Thesis Stress Test
├── Counterevidence
├── Adversarial Peer Review
├── Impact Analysis
│
▼
PUBLICATION / API / MCP
```

The rule at every level:

```text
DETERMINISTIC FACT
        or
MACHINE_PROPOSED
        or
HUMAN_REVIEWED
        or
ACCEPTED

never blur them.
```

And every higher node points downward.

That is the whole project.

---

# Roadmap

I would make this the canonical execution roadmap.

## PHASE 0 — Evaluation substrate

**Current move.**

Build:

```text
PATALA BENCHMARK SUITE v0

RETRIEVAL
EVIDENCE
STRUCTURE
FIDELITY
```

Seed it with:

* existing retrieval fixtures after validation;
* `ARG-GOLD-001`;
* difficult support/counterevidence examples;
* controlled fidelity corruptions.

Also freeze:

```text
benchmark version
gold state
split policy
metrics
run format
leakage rules
```

### Gate

No new `INFER` component can be called successful unless evaluated here.

### Vision unlocked

Not visible to users yet, but this is what lets every later claim be empirical rather than theater.

---

# PHASE 1 — Philological proof floor

**L0 agent owns this.**

Fix coordinates and make L0 genuinely lossless:

```text
T1
↓
exact source spans
↓
L0 tokenization
↓
roundtrip
```

Then progressively add:

```text
P0 source integrity
P1 segmentation/sandhi
P2 morphology
P3 syntax
P4 Sanskrit↔English alignment
P5 lexical evidence
```

Using Vidyut first, then independent witnesses.

Output must be stable objects:

```text
PhilologicalProof
```

not logs.

### Gate

For supported passages:

```text
0 unknown semantic characters
0 bad source spans
0 silent omissions
proof records resolve
```

### Vision checkpoint

Now `/verify-translation` becomes real.

A scholar can submit Sanskrit + translation and receive:

```text
source coverage
morphology
syntax
alignment
possible omissions
possible additions
term issues
open cruxes
```

**First genuinely useful external scholar API.**

---

# PHASE 2 — Retrieval becomes serious

Once the benchmark exists:

```text
BM25
vs dense
vs hybrid
vs late interaction
```

Do this over actual Pāṭala objects:

```text
passages
C1s
terms
translation decisions
evidence
```

Do not jump to GNNs.

### Gate

A retrieval method enters production only if it beats the simple baseline on the frozen benchmark.

### Vision checkpoint

This unlocks the scholar's **Explore** experience:

> “Show me passages relevant to reflexive awareness.”

> “Find other uses of this compound.”

> “Find passages that complicate this interpretation.”

Now the system starts reducing mechanical research labor.

---

# PHASE 3 — THEMES become accepted scholarly objects

You already have machine clusters.

Now unify:

```text
themes.ts
+
clusters.json
```

into:

```text
ThemeProposal
↓
editor adjudication
↓
AcceptedTheme
```

Allow overlap.

Membership carries:

```text
CORE
SUPPORTING
CONTRAST
TANGENTIAL
```

and role:

```text
DEFINES
ESTABLISHES
DEVELOPS
QUALIFIES
CONTRASTS
```

Do not accept all nine just because clustering produced them.

### Gate

At least several themes are genuinely reviewed and their memberships survive source inspection.

### Vision checkpoint

Now scholar exploration shifts from:

> “find passages”

to:

> **“show me the intellectual terrain.”**

You get:

```text
concept trajectories
tensions
clusters of passages
counterexamples
development across the work
```

This is where Pāṭala begins helping scholars **discover paper ideas**.

---

# PHASE 4 — Argument Gold before argument automation

This is where your recent cleanup becomes foundational.

Expand:

```text
ARG-GOLD-001
```

to perhaps:

```text
5–10 serious hand-reconstructed arguments
```

Each with:

```text
TEXTUAL_CLAIM
INTERPRETIVE_CLAIM
IMPLICIT_PREMISE
CONCLUSION
OBJECTION
QUALIFICATION

explicitness
source grounding
real IDs
inference relation
boundary
```

### Gate

Only then evaluate automatic extraction.

Tasks:

```text
proposition recovery
role classification
grounding
explicitness
relation extraction
inference recovery
scope fidelity
```

### Vision checkpoint

Now `/extract-argument` stops being a schema demo.

A scholar can give Pāṭala a passage and ask:

> “What exactly is the reasoning here?”

and receive a **machine proposal** that is structurally comparable with human gold.

---

# PHASE 5 — Argument extraction becomes a real model

Now build the extractor.

Potentially:

```text
C1 + L200 + L2
→ candidate propositions
→ grounding
→ relations
→ argument graph
```

But extraction is always proposal:

```text
MACHINE_PROPOSED
```

Human accepts/rejects.

Then store accepted argument graphs in the corpus.

### Gate

It must beat trivial baselines on `PATALA-STRUCTURE`.

Not passage overlap.

Actual argumentative recovery.

### Vision checkpoint

Now scholar tools become powerful:

```text
"What premises does this conclusion depend on?"

"Where is the implicit premise?"

"Show objections to this claim."

"What changes if I reject this interpretation?"
```

This is the start of the **logical research companion**.

---

# PHASE 6 — Semantic verification

This is the second major frontier.

Build separately:

```text
verify_claim_structure
```

already deterministic,

and:

```text
verify_claim_semantic
```

model-based.

Check:

```text
entailment
scope
polarity
agent/patient
attribution
certainty
boundary
```

Also build:

```text
discover_counterevidence
```

as distinct from curated counterevidence.

### Gate

Benchmark against adversarial examples.

Especially:

```text
scope expansion
certainty inflation
lost negation
false attribution
boundary erasure
```

### Vision checkpoint

Now the scholar can ask:

> **“Attack this interpretation.”**

This is the beginning of Pāṭala Review.

---

# PHASE 7 — Provenance-carrying synthesis

Only now return to essays.

The pipeline:

```text
AcceptedTheme
↓
Accepted / reviewed ArgumentGraph
↓
EssayPlan
↓
EssayClaims
↓
claim verification
↓
sentence generation
↓
sentence provenance
↓
adversarial semantic verification
↓
essay
```

The essay is **not canonical**.

The claim graph is.

Every substantive sentence resolves:

```text
sentence
→ EssayClaim
→ Argument
→ C1
→ Translation
→ PhilologicalProof
→ Sanskrit
```

### Gate

One gold essay should have:

```text
100% substantive claims represented
100% claim provenance resolvable
0 unsupported sentences
0 silent scope strengthening
0 silent certainty inflation
```

### Vision checkpoint

Now Pāṭala changes **how essays are written**.

The scholar works on:

```text
question
tension
perspective
claim structure
counterevidence
framing
```

rather than manually maintaining citations and source chains.

The essay becomes a rendering of a scholarly inquiry.

---

# PHASE 8 — Scholar Workbench

This is where all the pipelines become one product.

Build **Explore / Workbench** around a research question.

Example:

> “What exactly does Abhinavagupta mean by vimarśa?”

Workbench automatically assembles:

```text
PRIMARY PASSAGES

TERM TRAJECTORY

TRANSLATION DISAGREEMENTS

C1 INTERPRETATIONS

THEMES

ARGUMENTS

COUNTEREVIDENCE

SCHOLARSHIP

MY NOTES

MY CLAIMS

MY ESSAY PLAN
```

The scholar isn't chatting with a bot.

They are **navigating a structured field of evidence and interpretation**.

### Vision checkpoint

This realizes the “new scholar” model:

> AI handles corpus navigation and mechanical comparison; the scholar chooses what is interesting and judges what the evidence means.

---

# PHASE 9 — Adversarial scholarly companion

Now package the existing machinery into external workflows.

### Translation Review

```text
/verify-translation
```

### Translation adversary

```text
/adversarial-translation-review
```

### Thesis stress-test

```text
/stress-test-thesis
```

### Argument audit

```text
/audit-argument
```

### Counterevidence

```text
/find-counterevidence
/discover-counterevidence
```

### Term audit

```text
/audit-term
```

### Dependency analysis

```text
/impact-analysis
```

### Draft peer review

```text
/adversarial-peer-review
```

This is not six new technologies.

It is six orchestrations over:

```text
resolve
retrieval
proofs
claims
arguments
themes
counterevidence
verification
```

### Vision checkpoint

This is **Pāṭala Review**:

> upload scholarship and have the strongest available structured critic try to break it.

That could become the first serious commercial scholar product.

---

# PHASE 10 — API + MCP as the actual platform

Only after those primitives work well.

Expose things like:

```text
resolve_passage

verify_translation

find_parallels

compare_readings

audit_term

extract_argument

find_counterevidence

stress_test_thesis

trace_dependency

verify_claim

review_draft
```

Now any AI client can use Pāṭala as its scholarly epistemic backend.

So a future ChatGPT/Claude/agent doesn't need to hallucinate tantra scholarship.

It asks Pāṭala:

```text
"Does the evidence really support this?"
```

That is the platform moat.

---

# PHASE 11 — Collaborative scholarship

Then invite scholars into the graph.

Objects gain actual review workflows:

```text
Machine proposal
↓
Scholar A review
↓
Scholar B counter-reading
↓
editor adjudication
```

Preserve disagreement permanently.

Add:

```text
ORCID
attribution
review histories
DOIs/releases
CRediT roles
```

And eventually paid cruxes:

```text
OPEN ISSUE

translation crux
argument reconstruction
textual variant
concept dossier
```

### Vision checkpoint

Pāṭala stops being an AI project with academics reviewing it.

It becomes a **scholarly network in which AI generates candidate work and humans provide scarce judgment**.

---

# PHASE 12 — Economic layer

Then build incentives around contribution.

```text
FREE PUBLIC SCHOLARSHIP
texts
translations
evidence
commentary

PAID SCHOLAR TOOLING
private workspaces
adversarial review
API
bulk analysis
institutional access

FUNDED SCHOLARSHIP
microgrants
editorial fellowships
translation crux bounties

ATTRIBUTED CONTRIBUTIONS
review
adjudication
critical notes
essays
courses
```

This is important because now scholars have reasons to participate:

```text
better tools
money
citation
visibility
editorial influence
research opportunities
```

---

# PHASE 13 — Generalize beyond IPVV

Only after one work functions end-to-end.

Then ingest:

```text
another Pratyabhijñā work
↓
Tantrāloka
↓
other Śaiva works
↓
Buddhist / Nyāya interlocutors
```

And test:

```text
train/tune on IPVV
↓
held-out work
```

Now you can finally ask whether Pāṭala has built general computational philology rather than IPVV-specific machinery.

### Vision checkpoint

Cross-textual questions become possible:

> “How does the function of recognition change from Utpaladeva to Abhinavagupta?”

> “Where does Abhinavagupta inherit a Buddhist argumentative structure?”

That's when the graph becomes an intellectual-history engine.

---

# The two-agent division should stay extremely simple

## Agent L0 — **vertical truth**

Owns:

```text
SOURCE
↓
segmentation
↓
morphology
↓
syntax
↓
alignment
↓
translation proof
```

Its question is always:

> **Is this reading licensed by the source?**

Outputs stable proof objects.

---

## Agent ML — **horizontal and upward derivation**

Owns:

```text
C1
↓
themes
↓
arguments
↓
claims
↓
synthesis
↓
review
```

Its question is:

> **Does this higher-order representation legitimately derive from the scholarly objects beneath it?**

---

## Shared boundary

They join at:

```text
Passage ID
TranslationDecision ID
PhilologicalProof ID
C1 ID
```

Never by filename, guessed locator, title string, or fuzzy match.

That recent fabricated-ID failure is exactly why this boundary should be contractual.

---

# And yes: most future “products” are orchestration

Once the primitives work, something like adversarial peer review is largely:

```text
paper
↓
claim extractor
↓
quote resolver
↓
translation checker
↓
retrieval
↓
counterevidence
↓
argument graph
↓
semantic verifier
↓
report renderer
```

A scholar workbench is:

```text
question
↓
retrieval
↓
themes
↓
arguments
↓
evidence
↓
notes/claims
```

A beginner guide is:

```text
Theme
↓
accepted claims
↓
controlled simplification
↓
vertical fidelity check
```

A podcast script is:

```text
EssayClaim graph
↓
different rendering
↓
same provenance
```

That's why the architecture matters so much.

You are not building 30 applications.

You are building perhaps **10 trustworthy scholarly primitives**, then composing them.

---

# The checkpoint ladder I would put at the top of the repo

```text
CP0  BENCHMARK
We can measure ourselves honestly.

CP1  SOURCE PROOF
We can mechanically certify the source→L0 floor.

CP2  RETRIEVAL
We can reliably find relevant evidence.

CP3  THEMES
We can propose and adjudicate intellectual structure.

CP4  ARGUMENT
We can reconstruct actual reasoning.

CP5  VERIFICATION
We can test whether claims outrun evidence.

CP6  SYNTHESIS
We can produce provenance-carrying essays.

CP7  SCHOLAR WORKBENCH
We can help humans discover and develop ideas.

CP8  ADVERSARIAL REVIEW
We can seriously attack scholarly work.

CP9  API/MCP
Other tools can use the scholarly intelligence.

CP10 COLLABORATIVE EDITION
External scholars can contribute and adjudicate.

CP11 ECONOMIC NETWORK
Contributions receive credit and compensation.

CP12 CROSS-CORPUS
The machinery generalizes beyond IPVV.
```

That gives both agents a north star.

The most useful principle for preventing another weeds episode is:

> **Every engineering task must name the checkpoint it advances, the scholarly object it makes more trustworthy, and the benchmark/proof that will demonstrate success.**

If an agent proposes something and cannot answer those three questions, don't build it.

That lets you naturally encroach on the much bigger vision without ever needing a giant rewrite. Each checkpoint simply makes one more kind of scholarly claim trustworthy enough for the next pipeline to consume.

## 1. One universal definition of “layer done”

Every canonical layer should have a **LayerContract** with five gates:

```text
G0 — OBJECT CONTRACT
Does it produce the correct canonical object/file shape?

G1 — DETERMINISTIC INTEGRITY
IDs, hashes, provenance, coverage, dependencies, schema, replay.

G2 — SEMANTIC / ML VALIDITY
Does the object actually mean/do what the layer claims?

G3 — ADVERSARIAL VALIDITY
Can we mutate exactly the errors we fear and reliably catch them?

G4 — AUTONOMOUS PROOF
Can the controller produce it on unseen real material,
fail closed, resume, retry, replay and avoid duplicates?
```

Then optionally:

```text
G5 — HUMAN CALIBRATION
On the difficult cases, how often does a specialist agree?
How many review minutes does 1,000 tokens require?
```

A layer state becomes:

```text
NOT_BUILT
BUILT
ENGINEERING_VALIDATED       # G0-G1
SEMANTICALLY_VALIDATED      # G2-G3
AUTONOMOUSLY_PROVEN         # G4
SCHOLAR_CALIBRATED          # G5
```

This is substantially better than the current overloaded:

```text
BUILT / REAL / PASS
```

because we can say precisely:

> T1 worker BUILT, engineering-valid, but not semantically validated.

rather than “T1 works.”

---

# 2. Every layer gets the same evaluation packet

I would standardize a directory:

```text
contracts/
  source/
  t1/
  l0/
  argument-map/
  l2/
  l200/
  c1/
  theme/
  essay/
  education/
```

Each contains exactly:

```text
CONTRACT.md
schema.json
validator.py

eval/
  GOLD.jsonl
  DEV.jsonl
  TEST.jsonl
  MUTATIONS.jsonl
  scorer.py

skill/
  SKILL.md

certificates/
  <run-id>.json
```

And every certificate has:

```json
{
  "layer": "T1",
  "worker_sha": "...",
  "skill_sha": "...",
  "model": "...",
  "gold_version": "...",
  "test_split": "...",

  "G0_object_contract": "PASS",
  "G1_integrity": "PASS",

  "semantic_metrics": {},
  "mutation_metrics": {},
  "autonomy_metrics": {},

  "known_failures": [],
  "status": "SEMANTICALLY_VALIDATED"
}
```

**The skill and evaluator should be coupled.**

The skill says how to produce the object.

The contract says what counts as success.

The evaluator decides whether the producer actually met the contract.

This becomes the core development loop:

```text
SKILL
 ↓
MODEL
 ↓
OBJECT
 ↓
CONTRACT EVAL
 ↓
error taxonomy
 ↓
improve skill/model/context
 ↓
rerun DEV
 ↓
freeze
 ↓
one blind TEST run
```

That is your ML infrastructure.

---

# 3. Critical distinction: not every layer needs ML

This is important.

We should use ML only where correctness contains a semantic judgment.

For example:

```text
SOURCE → mostly deterministic
T1     → strongly semantic / ML
L0     → deterministic transform of T1
ARGMAP → strongly semantic / ML
L2     → strongly semantic / ML
L200   → hybrid
C1     → semantic / ML
THEME  → semantic / graph
ESSAY  → semantic / inference conservation
EDU    → semantic / pedagogic conservation
```

Don't force neural scoring into L0 just because we want “ML verification.”

The current semantic-equivalence proposal is partly based on the now-obsolete RAW→L0 conception. It explicitly describes MODE_B creating glosses from raw Sanskrit, whereas the locked canonical stack says **T1 creates the gloss and L0 structurally encodes T1**.

Therefore:

> **Move most of the proposed L0 semantic benchmark upward to T1.**

That is a major cleanup.

---

# 4. SOURCE contract

Canonical claim:

> This is the source text we say it is, and every downstream span can resolve into it.

### Deterministic contract

```text
SOURCE-1 exact bytes preserved
SOURCE-2 canonical source ID
SOURCE-3 witness/edition provenance
SOURCE-4 passage locators resolve
SOURCE-5 hashes reproduce
SOURCE-6 Unicode normalization recorded
SOURCE-7 no silent OCR repair
SOURCE-8 lacuna/corruption explicitly represented
```

### Metrics

```text
character coverage       100%
unaccounted characters   0
bad spans                0
hash mismatch            0
locator collision        0
silent normalization     0
```

### Adversarial fixtures

Mutate:

```text
drop avagraha
alter anusvāra
swap line
delete verse
duplicate verse
change locator
introduce OCR ?
change one character
normalize without recording
```

Validator must catch them.

### ML?

Normally **none**.

OCR restoration can have ML assistance, but:

```text
OCR_PROPOSED ≠ SOURCE_CERTIFIED
```

### SOURCE done

```text
G0 PASS
G1 PASS
G3 mutations 100% caught
G4 autonomous ingestion replay-safe
```

No semantic ML gate necessary.

---

# 5. T1 — the most important foundation benchmark

This should become **CP1 proper**.

Canonical claim:

> For the Sanskrit source, this is a faithful transliteral word/phrase-level reading that exposes rather than hides uncertainty.

This is your first genuinely difficult AI layer.

## Gold

The real IPVV T1 exemplars become gold.

But split **by passage/work/context**, not random tokens.

Ideally:

```text
TRAIN/EXAMPLES
DEV
TEST
```

and never expose TEST exemplars to the agent.

Eventually add:

* IPVV
* Kramasadbhāva
* Kubjikā
* another stylistically distinct Śaiva text

because otherwise you're proving “IPVV imitation.”

## T1 dimensions

Don't collapse this to BLEU or semantic similarity.

Measure separately:

### A. Coverage

```text
Sanskrit lexical material represented?
```

Metrics:

```text
token/phrase coverage recall
omission rate
unsupported insertion rate
```

### B. Segmentation

```text
compound boundaries
sandhi resolution
phrase grouping
```

Score against gold boundary decisions.

### C. Lemma/morphology contribution

Not necessarily whether every morphology tag is perfect, but:

> did the translation preserve what case/number/tense/negation/etc. contributes?

### D. Literal gloss adequacy

For each unit:

```text
CORRECT
ACCEPTABLE_ALTERNATIVE
TOO_BROAD
TOO_NARROW
WRONG_SENSE
UNSUPPORTED
ABSTAIN
```

### E. Technical-term sense

Especially:

```text
vimarśa
śakti
prakāśa
krama
kula
saṃvid
pramātṛ
vikalpa
```

This deserves a separate metric because generic lexical correctness can hide catastrophic philosophical errors.

### F. False certainty

This is probably the killer metric:

```text
gold = genuinely ambiguous
model = confidently chooses one reading
```

Measure:

[
FCR = \frac{\text{confident incorrect resolutions}}
{\text{genuinely ambiguous cases}}
]

I'd rather have slightly lower gloss recall with dramatically lower false certainty.

### G. Abstention quality

Measure both:

```text
abstention precision
abstention recall
```

Not “more OPEN = safer.”

An agent that says OPEN everywhere is useless.

---

# 6. T1 adversarial benchmark

This could become excellent.

Take correct T1 gold and programmatically inject exactly one defect:

```text
NEGATION_DROP
CASE_ROLE_SWAP
COMPOUND_MISPARSE
TECHNICAL_SENSE_FLATTENING
MODALITY_STRENGTHENING
AGENT_PATIENT_SWAP
OMISSION
ADDITION
NUMBER_CHANGE
TEMPORAL_CHANGE
FALSE_DISAMBIGUATION
LEXICAL_SENSE_SUBSTITUTION
```

Then ask the verifier:

```text
valid / invalid
error span
error class
```

This lets you evaluate the **critic/evaluator separately from the generator**.

That is important.

We want:

```text
T1_GENERATOR
T1_VERIFIER
```

potentially different models/prompts.

Generator quality and verifier quality become separate benchmarks.

---

# 7. L0 contract becomes beautifully simple

Once T1 is canonical:

> L0 is a lossless structured encoding of committed T1.

No AI needs to “understand Sanskrit” here.

Contract:

```text
T1 → L0 → T1
```

should be round-trip equivalent.

### Metrics

```text
T1 units represented        100%
gloss transfer              100%
source links                100%
order preservation          100%
unmapped content            0
invented records            0
schema validity             100%
```

And:

```text
semantic_status(L0) = semantic_status(T1)
```

L0 **inherits** the epistemic quality of its T1 parent.

Do not run another semantic model over L0 and pretend this independently verifies T1.

That would duplicate/confuse authority.

### Adversarial tests

```text
drop record
wrong source span
wrong lemma association
swap glosses
duplicate token
wrong parent T1 ID
wrong hash
reorder records
```

### L0 done

This can be **provable almost formally**.

If all transformations are deterministic and round-trip-safe:

```text
L0 AUTONOMOUSLY_PROVEN
```

can be extremely strong.

---

# 8. Argument-map contract

This is likely the second hardest semantic layer.

Canonical claim:

> This map correctly represents the local dialectical/argumentative structure needed to interpret the passage.

Do **not** evaluate with generic semantic similarity.

Represent it structurally:

```text
nodes:
  proposition
  question
  objection
  response
  conclusion
  contextual premise
  OPEN

edges:
  supports
  objects_to
  responds_to
  grounds
  qualifies
```

Your previous Agent-1 work gives a crucial lesson here:

```text
grounding ≠ inference ≠ dialectical relation
```

Keep those distinct.

### Metrics

#### Node recovery

```text
proposition precision/recall
```

#### Role classification

```text
premise
conclusion
objection
response
context
qualification
```

Macro-F1.

#### Edge recovery

Exact typed relation precision/recall.

#### Speaker attribution

Critical for commentary texts.

#### Scope

Does the proposition belong to:

```text
author
opponent
quoted kārikā
prior commentator
hypothetical interlocutor
```

#### OPEN/crux recovery

Can it identify genuinely unresolved inferential gaps?

#### Unsupported inference rate

Probably the killer metric:

[
UIR=
\frac{\text{generated argumentative edges not licensed by passage}}
{\text{generated argumentative edges}}
]

We want this extremely low.

---

# 9. Argument-map adversarial suite

Mutations:

```text
OBJECTION_AS_AUTHOR_VIEW
GROUNDING_AS_INFERENCE
RESPONSE_DIRECTION_FLIP
PREMISE_CONCLUSION_SWAP
MISSING_QUALIFIER
SCOPE_EXPANSION
INVENTED_BRIDGE
FALSE_CONTRADICTION
OPEN_AS_RESOLVED
```

Agent 1 has already encountered almost all these failure modes.

Turn those historical failures directly into benchmark fixtures.

That's how the system compounds.

---

# 10. L2 contract

Canonical claim:

> This is readable English that conserves the content of SOURCE + T1/L0 under the interpretation fixed by the argument map.

This is **not** “does it resemble the human translation?”

Multiple English renderings can be good.

So evaluate conservation dimensions.

## L2 dimensions

### Source coverage

Every materially relevant T1 unit has a realization or explicit supply explanation.

### Addition

Nothing materially new appears without being licensed.

### Negation/polarity

Exact.

### Modality

Don't turn:

```text
may → is
could → must
suggests → proves
```

### Quantification/scope

```text
some/all
local/general
conditional/unconditional
```

### Speaker attribution

Never put opponent claim into Abhinava's mouth.

### Technical-term stability

Context-sensitive but traceable.

### Argument preservation

Readable prose must retain the logical relation identified by argument map.

### Paraphrase-strength conservation

This is exactly the C.1 lesson from Agent 1:

```text
CLAIM_SURFACE_INFLATION
PARAPHRASE_EXPANSION
```

should be first-class L2 mutations.

---

# 11. L2 evaluation should be bidirectional

A useful conceptual test:

```text
T1/argmap → L2
```

asks:

> Does L2 cover the source?

And:

```text
L2 → T1/argmap
```

asks:

> Is every substantive L2 assertion licensed upstream?

So two metrics:

```text
SOURCE_COVERAGE
OUTPUT_LICENSE
```

This is much better than one similarity score.

Formally:

[
Coverage(L2)=\frac{\text{licensed source propositions realized}}
{\text{source propositions requiring realization}}
]

[
License(L2)=\frac{\text{substantive L2 claims licensed upstream}}
{\text{substantive L2 claims}}
]

You want both high.

---

# 12. L200 contract

You already learned the main lesson here.

Canonical claim:

> L200 faithfully explains **how L2 was derived** and identifies material translation/interpretive decisions.

Not:

> generate lots of interesting translation observations.

Existing live benchmark already exposed the original open-ended model's false-positive problem. The DEV plan records this layer as a constrained candidate→classifier design.

Keep that.

### Metrics

```text
MT decision precision
MT decision recall

IA precision
IA recall

OPEN precision
OPEN recall

derivation-link correctness
source-span correctness
decision-category accuracy
false certainty
```

Most important:

```text
FALSE_POSITIVE_MT
LAUNDERING
```

### Adversarial

```text
invent non-material decision
omit actual supply
misclassify IA as translation decision
resolve OPEN
wrong source span
wrong L2 target
invent rationale
```

L200 is probably where **precision > recall** most strongly.

---

# 13. C1 contract

Canonical claim:

> This is a passage-local explanation licensed by the translation/audit and nothing more.

Structure already gives:

```text
SUMMARY
FUNCTION
KEY TERMS
EXPLANATION
BOUNDARY
RELATED
```

### Evaluation dimensions

```text
summary fidelity
argument-function correctness
term explanation correctness
boundary compliance
source localization
unsupported interpretation
```

The crucial distinction:

```text
C1 may explain
C1 may not silently synthesize beyond passage
```

So measure:

### Locality precision

What proportion of commentary claims are actually supported by this passage / its declared context?

### Boundary violations

Did C1 introduce:

```text
cross-text doctrine
modern comparison
historical claim
metaphysical generalization
```

without explicit upstream support?

### Adversarial mutations

```text
PASSAGE_TO_TRADITION_GENERALIZATION
MODERN_ANALOGY_INSERTION
UNSUPPORTED_HISTORICAL_CLAIM
AUTHOR_INTENTION_INVENTION
COMMENTARY_STRENGTHENING
```

---

# 14. THEME contract

This one needs to be very strict because clustering can create enormous epistemic theatre.

Canonical claim:

> These C1 claims form an evidence-backed scholarly theme for a specific reason.

Not:

> embeddings put these passages near each other.

You already learned this with the 63/63 machine themes.

### Theme object should include

```text
theme proposition
members
member role
evidence strength
boundary
counterexamples
why grouped
```

### Metrics

#### Membership precision

Of proposed members, how many genuinely instantiate/support the theme?

#### Membership recall

Lower priority initially.

#### Role accuracy

```text
CORE
SUPPORT
QUALIFICATION
COUNTEREXAMPLE
CONTEXT
```

#### Theme specificity

Does the theme say more than its members license?

#### False-theme rate

Clusters that are lexical coincidence but not conceptual unity.

### Adversarial

```text
LEXICAL_ONLY_CLUSTER
ONE_TERM_MULTIPLE_SENSES
SAME_TOPIC_DIFFERENT_CLAIM
CONTRADICTORY_MEMBERS_AS_SUPPORT
THEME_TOO_BROAD
```

---

# 15. ESSAY contract

This can reuse the excellent invariant you already established:

[
authority(P(x)) \le authority(x)
]

For every sentence:

```text
sentence
→ exact parent claim(s)
→ transformation type
→ authority ceiling
```

### Metrics

```text
sentence evidence coverage
unsupported sentence rate
authority strengthening rate
claim-surface inflation
qualifier retention
counterargument preservation
crux preservation
```

The killer metric:

```text
UNLICENSED_SUBSTANTIVE_SENTENCE_RATE
```

should approach zero.

### Adversarial

This is where Agent 1's C/C.1 mutations become gold:

```text
PARAPHRASE_EXPANSION
CLAIM_SURFACE_INFLATION
QUALIFIER_DROP
MODALITY_STRENGTHENING
EVIDENCE_LAUNDERING
SYNTHESIS_AS_SOURCE_CLAIM
CORROBORATION_AS_APPROVAL
```

This layer already has unusually good historical failure data. Use all of it.

---

# 16. EDUCATION contract

Canonical claim:

> This is pedagogical simplification that preserves the epistemic structure of the essay.

You don't need “scholarly sophistication.”

You need **faithful simplification**.

### Metrics

```text
core claim retention
qualification retention
false simplification
invented example implication
pedagogic clarity
dependency resolvability
```

Most important failure:

```text
SIMPLIFICATION → FALSE CLAIM
```

Examples can be explanatory without becoming evidence.

So mark:

```text
EXAMPLE
ANALOGY
SOURCE_CLAIM
```

explicitly.

---

# 17. I would also make “critic competence” a separate benchmark

This is potentially huge.

For each semantic layer:

```text
GENERATOR benchmark
VERIFIER benchmark
```

Because you might discover:

```text
DeepSeek:
great generator
weak critic

Claude:
strong critic
more expensive generator
```

Then autonomous factory becomes:

```text
cheap/fast model proposes
        ↓
critic model evaluates
        ↓
deterministic validator
        ↓
commit MACHINE_PROPOSED
```

You can empirically choose this.

Not by vibes.

For example T1:

```text
T1-GEN-v1
T1-VERIFY-v1
```

L2:

```text
L2-GEN-v1
L2-VERIFY-v1
```

This lets Pāṭala optimize:

[
\text{cost} \times \text{false certainty} \times \text{review burden}
]

rather than just model benchmark score.

---

# 18. Held-out splits need to become sacred

I would freeze:

```text
EXEMPLAR = may appear in skill as examples
DEV      = iterate prompts/model
TEST     = blind evaluation only
NAT      = naturally occurring future cases
```

And preferably split at **passage families / works**, not random sentences, wherever possible.

Otherwise Abhinava-specific recurring language leaks across train and test.

The current ML proposal already recognizes that held-out evaluation and circularity matter; that discipline should now be generalized to every semantic layer.

---

# 19. Exact checkpoint ladder I would give Agent 2

Forget “full stack wired.”

That phrase should disappear until the canonical stack is actually proved.

## CP0 — Contracts frozen

For every layer:

```text
artifact definition
dependencies
validator
semantic dimensions
mutation taxonomy
gold location
certificate schema
```

No worker changes yet.

## CP1 — T1

```text
SOURCE
→ autonomous AI T1
→ G0/G1 PASS
→ DEV measured
→ mutations measured
→ blind TEST
→ AUTONOMOUSLY_PROVEN
```

This is the current frontier.

## CP2 — L0

```text
T1 → deterministic L0
round-trip/isomorphism proof
AUTONOMOUSLY_PROVEN
```

Should be relatively quick.

## CP3 — Argument map

```text
SOURCE + T1/L0
→ model map
→ structural + semantic benchmark
→ autonomous proof
```

## CP4 — L2

```text
upstream → readable translation
coverage + licensing + adversarial fidelity
```

## CP5 — L200

Existing constrained benchmark.

## CP6 — C1

Passage-local commentary benchmark.

## CP7 — Theme

Evidence-backed theme benchmark.

## CP8 — Essay

SentenceEvidenceAudit + adversarial faithfulness.

## CP9 — Education

Faithful pedagogic compression.

## CP10 — Full factory

Fresh unseen work:

```text
SOURCE
→ T1
→ L0
→ ARGMAP
→ L2
→ L200
→ C1
→ THEME
→ ESSAY
→ EDUCATION
```

with:

```text
crash/resume
bounded retries
zero duplicate canonical commits
provenance resolution
failure isolation
staleness propagation
certificate per layer
```

Only **then**:

> full autonomous stack proven.

---

# 20. And yes, update Agent 2's docs immediately

Three specific corrections:

**`DEV-PLAN.md`:**
remove/retract:

> “full autonomous stack wired”

as a meaningful success claim.

Replace with:

> controller shells exist for several downstream layers; canonical T1 worker is the current first unsatisfied layer contract.

Its current statement that every layer has a canonical handler is inconsistent with the locked stack because T1 is explicitly still “to build.”

**`CHECKPOINTS-INTEGRATION.md`:**
replace RAW-Sanskrit→L0 CP1 with:

```text
SOURCE → T1
```

and move deterministic T1→L0 into CP2. Its current diagram still skips T1 despite the new canonical order.

**`ML-L0-SEMANTIC-EQUIVALENCE-PROPOSAL.md`:**
rename/reframe it as something like:

```text
ML-T1-SEMANTIC-VALIDATION.md
```

Most of its semantic work — gloss equivalence, false certainty, technical senses, abstention — belongs to **T1** now. L0 becomes largely a deterministic representation contract.

That gives Agent 2 an extremely clean operating rule:

> **One layer at a time. Freeze its contract. Build the producer. Beat the baseline on DEV. Pass adversarial mutations. Run blind TEST once. Prove unattended execution. Emit certificate. Only then unlock the next layer.**

That is how I would turn the IPVV stack into a genuinely ML-verifiable autonomous translation compiler rather than an accumulation of workers and passing unit tests.

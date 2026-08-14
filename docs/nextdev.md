> **ARCHIVED / SUPERSEDED** — kept for history only. Do NOT follow as current. See `docs/INDEX.md` + `docs/DOCS-AUDIT.json` for the canonical doc for this concern.

Yes. The right move now is to define a **small number of formal primitives** that everything else hangs off. Not giant schemas. Not fifty entity types. Just enough structure that every important claim can be traced, reviewed, reversed, and extended later.

I’d build Tantrakośa around **six core systems**.

## 1. Identity system — “what thing are we talking about?”

This is the foundation.

Every persistent object gets a stable internal ID:

```text
WORK
PASSAGE
SOURCE
PERSON
TERM
MANUSCRIPT
```

That’s enough for now.

The rules should be:

* IDs never change once public.
* Titles/names can change; IDs cannot.
* External IDs are aliases, not replacements.
* Every object can carry multiple external identifiers.
* Never encode mutable interpretation into the ID.

So the system can eventually say:

```text
Tantrakośa work
↔ Muktabodha ID
↔ NGMPP ID
↔ OCHS record
↔ Gyan Bharatam record
↔ GRETIL source
```

The main job is **resolution**:

> Are these two records talking about the same thing?

Do not try to solve all identity automatically. Support:

```text
unresolved
candidate match
confirmed match
rejected match
```

That alone scales enormously.

---

# 2. Assertion system — “what are we claiming?”

This is probably the most important design decision.

Don't store important scholarly claims as naked fields.

Instead of thinking:

```text
date = 950–1050
tradition = Krama
author = X
```

conceptually think:

```text
ASSERTION

subject
predicate
value
```

Examples:

```text
WORK X
has date
900–1000

WORK X
belongs to
Krama

PASSAGE X
parallels
PASSAGE Y

MANUSCRIPT X
witnesses
WORK Y
```

Then every assertion can carry:

```text
status
certainty
evidence
creator
created_at
review history
```

This means disagreement doesn't destroy your database.

You can hold:

```text
Assertion A:
date = 900–975

Assertion B:
date = 950–1050
```

with different evidence.

Then an editorial state says which one Tantrakośa currently prefers.

**Do this for claims that may reasonably be contested.**

Do *not* do this for everything.

Don't turn:

```text
filename
API slug
page number
```

into assertions.

Rule of thumb:

> If a scholar could legitimately say “I disagree,” model it as an assertion.

That keeps the system clean.

---

# 3. Evidence system — “why should I believe this?”

Every scholarly assertion should be able to point to evidence.

Keep the evidence model extremely simple initially.

An evidence item needs:

```text
resource
locator
role
note
```

`resource` = article, book, edition, manuscript, passage, etc.

`locator` = page, verse, folio, section.

`role` describes **why it matters**, e.g.:

```text
supports
contradicts
defines
dates
identifies
quotes
parallel
commentary
```

The crucial thing is that evidence itself does not magically make something true.

So:

```text
ASSERTION
   ↓
EVIDENCE LINKS
   ↓
SOURCE
```

And eventually:

```text
ASSERTION
   ↓
REVIEW EVENTS
```

This gives you the inspectability you want.

---

# 4. Provenance system — “where did this object come from?”

Keep provenance separate from evidence.

They sound similar but aren't.

Evidence says:

> Why do we believe this claim?

Provenance says:

> Where did this digital thing originate?

For every source text / manuscript image / transcription / translation, know:

```text
who supplied it
where it came from
what edition/witness it represents
when acquired/imported
what transformation we performed
what version we currently hold
```

Think lineage:

```text
physical manuscript
↓
photograph
↓
institutional scan
↓
OCR
↓
human-corrected transcription
↓
normalized Sanskrit
↓
segmented Tantrakośa text
```

You don't need every level immediately.

But the system must allow the chain.

Most importantly:

**never overwrite provenance.**

If you normalize spelling, preserve the fact that it was normalized.

If you correct OCR:

```text
original
→ transformed version
```

not:

```text
old text disappears
```

---

# 5. Review system — “who checked what?”

This is where your future moat starts.

Don't make review a property:

```text
reviewed: true
```

Make it an event.

A review event should answer:

```text
WHO
reviewed WHAT
WHAT decision
WHY
WHEN
```

Possible outcomes:

```text
accept
reject
revise
needs specialist
abstain
```

And scope matters.

Someone might review:

```text
work identity
date
translation
term sense
parallel
manuscript identification
```

not “the record.”

That matters because:

> Professor X reviewed this work

is dangerously vague.

Instead:

> Professor X accepted the identification of manuscript M as a witness of work W.

Much stronger.

And reviews should never vanish.

```text
proposal
↓
review
↓
accepted
↓
later challenged
↓
new review
```

You retain the history.

---

# 6. Rights system — “what are we actually allowed to do?”

Build this now because it becomes painful later.

Don't reduce rights to:

```text
license = CC-BY
```

You need operational permissions.

For any resource, be able to answer independently:

```text
may display?
may download?
may redistribute?
may expose full text through API?
may index/search?
may embed?
may use in RAG?
may create embeddings?
may use for model training?
may use for evaluation?
may commercially license derivative data?
```

Each can be:

```text
yes
no
unknown
conditional
```

**Unknown is critical.**

Never interpret “publicly accessible” as “commercial ML training allowed.”

That saves you from enormous problems later.

---

# The elegant part: everything else becomes derived

Once you have these six:

```text
IDENTITIES
ASSERTIONS
EVIDENCE
PROVENANCE
REVIEWS
RIGHTS
```

almost everything we've imagined can be constructed on top.

For example:

## Term sense

Not a giant special architecture.

It's:

```text
TERM identity
+
ASSERTION:
"term X has sense Y
in scope Z"
+
EVIDENCE
+
REVIEWS
```

## Textual parallel

```text
ASSERTION:
PASSAGE A parallels PASSAGE B

type:
possible quotation

evidence:
lexical overlap
historical relationship

status:
machine proposed

review:
scholar accepts
```

## Manuscript identification

```text
ASSERTION:
MANUSCRIPT M witnesses WORK W

evidence:
catalogue
incipit
colophon
text match

status:
expert reviewed
```

## Date

Same system.

## Tradition classification

Same system.

## Authorship

Same system.

That's the beauty.

You don't need 40 bespoke intellectual structures.

---

# Then define epistemic states globally

I would make one small universal status vocabulary.

Something like:

```text
machine_proposed
human_proposed
checked
expert_reviewed
editorially_accepted
disputed
rejected
```

Potentially simplify further:

```text
PROPOSED
REVIEWED
ACCEPTED
DISPUTED
REJECTED
```

And separately store **who/what produced it**:

```text
machine
editor
scholar
institution
```

Don't encode both dimensions into one field if possible.

So:

```text
status = accepted
origin = machine
```

could mean a machine proposed it originally, but it was subsequently accepted by appropriate review.

This is cleaner than `machine_reviewed_gold_final_v2`.

---

# Certainty should also be tiny

Avoid percentages unless an algorithm actually generates a calibrated score.

For scholarly assertions:

```text
certain
probable
possible
uncertain
```

That's enough.

Machine predictions can have numerical scores separately.

Thus:

```text
machine_score = .86
```

is not:

```text
scholarly_certainty = .86
```

Very important distinction.

---

# You also need a clean distinction between OBJECTS and CLAIMS

This will prevent a lot of future mess.

### Objects

Things that exist in your system:

```text
Work
Passage
Manuscript
Person
Term
Resource
```

### Claims

Statements about those things:

```text
this manuscript witnesses this work
this work belongs to Krama
this passage quotes that passage
this term has this technical sense
```

### Events

Things humans/machines did:

```text
import
review
correction
translation
transcription
```

This three-part model is enough for an enormous system:

```text
OBJECTS
↓
CLAIMS
↓
EVIDENCE
↓
EVENTS
```

---

# I'd introduce “Resource” as a deliberately broad bucket

Avoid:

```text
Book
Article
Website
PDF
Video
Lecture
Dataset
Edition
```

all becoming complicated independent systems immediately.

Have:

```text
RESOURCE
```

with a type:

```text
edition
article
book
lecture
video
dataset
website
catalogue
```

Later, special types can get additional structures if genuinely necessary.

This keeps bibliography/media manageable.

---

# Same with people

One `Person` initially.

Don't build:

```text
Scholar
Teacher
Translator
Pandit
Practitioner
Editor
Reviewer
```

as separate database classes.

Use roles:

```text
person
roles[]
expertise[]
affiliations[]
```

Someone can simultaneously be:

```text
scholar
translator
teacher
reviewer
```

Then crucially keep **expertise scoped**.

Not:

```text
verified scholar = yes
```

but conceptually:

```text
review_scope:
Krama
Sanskrit textual criticism
Newari manuscript studies
```

Eventually review permissions can use that.

---

# Institutions are similarly simple

Treat:

```text
BHU
Muktabodha
OCHS
IFP
Gyan Bharatam
```

as Organizations.

Then represent relations:

```text
PERSON affiliated_with ORGANIZATION

RESOURCE held_by ORGANIZATION

MANUSCRIPT catalogued_by ORGANIZATION
```

Again: don't make bespoke logic.

---

# Passage IDs are worth preserving exactly as a core primitive

You're already doing something right here.

The passage is the fundamental **addressable scholarly unit**.

But don't assume:

```text
verse = passage
```

forever.

Think:

```text
PASSAGE

belongs to work
has locator
has sequence
has source span
```

Then Tantrāloka can have:

```text
chapter
verse
```

prose texts might have:

```text
chapter
section
sentence
```

manuscripts could eventually reference:

```text
folio
line
```

Stable ID independent of display locator.

That's important.

---

# You need Source vs Work separated ruthlessly

This is another major foundation.

`Kramasadbhāva` is a **Work**.

Dyczkowski's edition is a **Source/Edition Resource**.

Muktabodha's e-text derived from some source is another **digital source representation**.

A manuscript is another witness.

So:

```text
WORK
abstract intellectual object

SOURCE/WITNESS
one concrete representation

PASSAGE
your addressable representation of text
```

Never let:

```text
work.sanskrit = "..."
```

become the conceptual model.

Eventually:

```text
WORK
  ↓
SOURCE A
SOURCE B
SOURCE C
  ↓
PASSAGE READINGS
```

You don't need a critical apparatus implementation now.

Just don't close the door.

---

# Build “crosswalk” as a first-class concept

This will be huge institutionally.

A crosswalk says:

```text
our object X
corresponds to
external object Y
```

with relationship:

```text
same
likely_same
derived_from
version_of
witness_of
references
```

Then you can import OCHS without copying its epistemology.

Example conceptually:

```text
tk:work:X
same_as
OCHS work record Y
```

or:

```text
tk:manuscript:M
same_as
NGMPP catalog record Z
```

and preserve both identifiers.

Your whole federation eventually rests on this.

---

# For AI: proposals are disposable, decisions are durable

This should become a system-wide principle.

AI outputs should generally live in a **proposal layer**:

```text
AI candidate identity
AI translation draft
AI candidate parallel
AI candidate term sense
AI OCR
```

Nothing becomes authoritative merely because the model produced it.

Pipeline:

```text
AI
↓
PROPOSAL
↓
REVIEW
↓
ASSERTION
```

or:

```text
proposal rejected
```

Crucially, **keep rejected proposals** where useful.

Why?

Because rejected examples become incredible evaluation/training material.

```text
model guessed X
expert said Y
because Z
```

That's gold.

---

# I would define five types of “machine proposal” initially

No more.

```text
IDENTITY
RELATION
TERM_SENSE
TRANSLATION
TEXT_CORRECTION
```

Later manuscript OCR etc.

Every machine proposal carries:

```text
model/version
prompt/pipeline version
inputs
timestamp
score if available
```

That's enough to reproduce why something appeared.

---

# Translation should fit into the same architecture

Don't let translation become a parallel universe.

Translation = an object/version containing:

```text
passage
source
translation text
creator
stage
```

Then individual interpretive decisions can be assertions/evidence.

So:

```text
TRANSLATION
```

is the output.

But:

```text
"vimarśa here means reflexive awareness"
```

is an assertion.

This matters later because a second translation can reuse the scholarly decision without copying the prose.

**The real corpus intelligence sits beneath the English sentence.**

---

# Separate observations from interpretations

Useful general rule.

For example manuscript:

### Observation

```text
colophon reads X
script appears Newari
12 folios present
```

### Interpretation

```text
therefore manuscript is witness of Kubjikāmata
likely 11th century
```

Those should not be collapsed.

Similarly with text reuse:

### Observation

```text
strings overlap 84%
```

### Interpretation

```text
B quotes A
```

AI is excellent at generating observations/candidates.

Scholars are crucial in adjudicating interpretation.

That's exactly the moat division we want.

---

# Don't build a generic knowledge graph UI yet

Have the graph internally.

But externally, expose **questions scholars actually ask**.

For example:

```text
What witnesses exist?

What editions exist?

Where else does this term occur?

Why is this passage translated this way?

What texts are historically related?

What claims about this work are disputed?
```

These become views over the same primitives.

The graph is architecture, not necessarily product UX.

---

# A useful “claim card” becomes the universal UI primitive

Eventually every contested thing could render something like:

```text
CLAIM

Kramasadbhāva predates X

STATUS
Accepted

CERTAINTY
Probable

SUPPORTED BY
3 sources

REVIEWED BY
2 specialists

LAST CHANGED
2028

[Evidence]
[History]
[Challenge]
```

Same UI works for:

```text
dates
authorship
relations
term senses
manuscript identities
```

This is very scalable.

---

# Every change should create history, never mutate silently

At minimum:

```text
created_at
created_by
updated_at
```

But for scholarly objects, ideally append-only events.

Don't necessarily implement event sourcing everywhere now.

Simpler:

```text
current record
+
revision log
```

Each revision:

```text
before
after
who
why
when
```

Enough.

Git can even provide some of this initially.

Do not invent enterprise event infrastructure yet.

---

# Use Git where Git is already good

For your early stage:

Good in Git:

```text
schemas
term ledger
work metadata
translation records
relation records
docs
reviewed datasets
```

Git gives:

```text
diff
history
blame
rollback
PR review
```

That's fantastic for the first years.

Database becomes necessary for:

```text
search
accounts
permissions
review queues
large ingestion
institutional work
```

Don't migrate all authority data into opaque mutable database rows prematurely.

You can have:

```text
Git = canonical scholarly data
DB = indexed/read/application layer
```

for quite a while.

That's actually attractive academically because the corpus remains inspectable.

---

# Define validation rules rather than giant schemas

This is probably the most practical answer to “how do we avoid overengineering?”

Instead of creating incredibly detailed representations, define **invariants**.

For example:

### Work invariants

```text
must have stable ID
must have canonical display title
may have multiple aliases
every external identity must include its source
no uncertain tradition/date without certainty state
```

### Assertion invariants

```text
must identify subject
must identify predicate
must identify creator/origin
accepted assertions require evidence or explicit editorial rationale
```

### Review invariants

```text
review cannot silently alter assertion
reviewer identified
decision explicit
time recorded
```

### Resource invariants

```text
must preserve original URL/identifier
must record access source
rights cannot default to open
```

### AI invariants

```text
machine output cannot directly become accepted
model/version recorded
machine and human confidence never conflated
```

That's better than prematurely specifying 200 fields.

---

# Think in terms of “minimum defensible record”

Every object should have a minimum standard before it becomes public.

For a work:

```text
identity
title
source of identity
tradition claim + evidence
approximate date claim + evidence where known
bibliography
provenance status
```

For a manuscript:

```text
custodian/repository
external shelfmark
source catalogue
digital-surrogate link if allowed
identity status
rights status
```

For a relation:

```text
source
target
relation type
status
evidence
```

For a term sense:

```text
term
proposed sense
scope
example evidence
status
```

That's it.

As scholarship improves, records deepen.

---

# You also need “unknown” everywhere

Academic systems get corrupted when they force certainty.

Allow:

```text
author = unknown

date = unknown

rights = unknown

work identity = unresolved

relation = possible

tradition = disputed
```

Do not force fake values for UI cleanliness.

The ability to represent ignorance precisely is actually a feature.

---

# Make provenance visible in API responses

This is worth designing now.

Not:

```text
GET work
→ magical authoritative object
```

but conceptually:

```text
data
provenance
assertion_states
warnings
```

Warnings could include:

```text
not reviewed
conflicting dates
source rights unknown
machine-derived relation
```

This makes AI consumption much safer.

---

# One elegant quality metric: evidence coverage

Don't invent a “Tantrakośa score.”

Instead measure interpretable things:

```text
% assertions with evidence
% reviewed
% externally sourced
% externally verified
% disputed
% rights resolved
```

For a work you could internally know:

```text
identity verified
date reviewed
tradition reviewed
3/7 manuscript records reviewed
translation unreviewed
```

Much more useful than `quality: 87`.

---

# Another useful metric: review depth

Something can be:

```text
one editor checked
```

versus:

```text
two independent specialists agreed
```

Don't necessarily make a hierarchy of 12 levels.

Simply store the events.

The UI can later derive:

```text
2 expert reviews
```

Again, raw facts > synthetic scores.

---

# The institutional import system can eventually be almost stupidly simple

Input:

```text
external records
```

Pipeline:

```text
1 NORMALIZE FORMAT
2 RESOLVE IDENTITIES
3 PROPOSE ENRICHMENTS
4 FLAG UNCERTAINTY
5 ROUTE HARD CASES
6 EXPORT RESULTS
```

That's basically the whole product.

Every stage outputs inspectable objects.

No magical “AI enrich” black box.

---

# Same for scholars

Scholar workflow:

```text
SEARCH
↓
OPEN OBJECT
↓
SEE CLAIM
↓
SEE EVIDENCE
↓
ACCEPT / CHALLENGE / REVISE
↓
CREDIT RECORDED
```

That's enough for a first scholar workspace.

You don't need messaging, social feeds, collaboration rooms, notifications, etc.

---

# Your next implementation exercise

I would literally sit with these six systems and try to represent **five awkward cases**:

1. Two catalogues use different names for the same work.
2. Two scholars disagree about a date.
3. AI detects a possible quotation between two passages.
4. A manuscript is viewable online but training rights are unknown.
5. A scholar changes the interpretation of a technical term after seeing another passage.

If your primitives represent all five **without special hacks**, the architecture is probably healthy.

Then try another five.

That's how I'd evolve this—not by trying to predict every possible field.

## The whole thing should reduce to this

```text
OBJECT
what is it?

ASSERTION
what are we saying about it?

EVIDENCE
why?

PROVENANCE
where did the material come from?

REVIEW
who checked the claim?

RIGHTS
what may we do with it?
```

And then one absolute rule:

> **Machines may propose. Sources may support. Humans may review. Tantrakośa records the history rather than pretending uncertainty never existed.**

If we preserve that invariant, you can bolt on manuscripts, translations, terminology, lectures, institutions, AI benchmarks, even Yogakośa later without fundamentally redesigning the epistemic core. That is the clean formal system I'd play with first.

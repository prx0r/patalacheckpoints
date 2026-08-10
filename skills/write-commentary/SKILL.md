---
name: write-commentary
description: "Produce the C1 capstone scholarly commentary for a passage or work. C1 is a separate workflow from translation (T1→T3.1): it reviews the whole stack, does targeted research, and emits structured proposals. Use when asked to write a C1, explain a passage, or build a referenceable commentary."
version: 1.0.0
author: Pāṭala
metadata:
  hermes:
    tags: [commentary, c1, sanskrit, tantra, scholarly, patala]
    related_skills: [translate-work, validate-passage, use-api]
---

# Produce C1 — the capstone commentary

## Purpose

C1 is the capstone scholarly commentary layer for a passage or work.

It is not:

a free-form essay,

a paraphrase of T3,

an AI summary of doctrine,

a devotional gloss,

a dump of every possible parallel,

or a claim that the current translation is final.

It should read like a very sharp modern scholarly commentary: concise, explanatory, source-aware, and explicit about uncertainty.

The governing question is:

> What is this passage actually saying, how do we know, what remains uncertain, and what evidence makes the preferred reading more likely than its rivals?

C1 should be useful to:

a serious reader trying to understand the passage,

a translator checking a decision,

a scholar tracing evidence,

a future C1 referencing an earlier C1,

an essay/video/research agent building higher-level synthesis.

1. Inputs

Before writing C1, inspect every available layer for the target passage/work.

Minimum preferred stack:

source Sanskrit
T1
R1 / adversarial crux map
T2 / strongest defensible rival
R2 / adjudicated decisions
T3
T3.1
bibliography record

Also inspect, when available:

neighboring passages
source edition metadata
anchor translations
commentaries
term ledger
term-history trajectories
term occurrences
known parallels
manuscript / variant notes
existing C1s
dossiers
reference map
bibliographic scholarship

Never assume a layer exists. Inspect first.

If a required layer is absent, continue only if the available evidence is sufficient and mark the gap explicitly.

2. Research order

Use evidence in this order.

A. Local project evidence first

Search the repository/corpus before the open web.

Priority:

1. target Sanskrit passage
2. T1 / R1 / T2 / R2 / T3 / T3.1
3. neighboring passages in the same work
4. existing commentary/anchor files
5. term ledger + term histories
6. dossiers / reference map
7. parallel passages already in the corpus
8. existing C1s
9. bibliography records

Prefer stable passage/resource IDs whenever available.

Do not cite a filename when a stable passage/resource ID exists.

B. Then targeted web research

Search the web only to answer concrete unresolved questions.

Good research questions:

What is the historical setting of this school/text?
How is this technical term used in closely related texts?
Does a traditional commentary explicitly gloss this word?
Does another primary text quote or closely parallel this passage?
How do major scholars understand this crux?
Is there an edition / translation / article the local bibliography missed?

Do NOT browse vaguely for "meaning of tantra term X" and then import generic summaries.

C. Wisdom Library

Wisdom Library may be used as a discovery/convenience source for:

searchable Sanskrit/English text,

traditional commentaries,

cross-references,

titles and aliases,

locating passages worth checking.

But treat it as a research aid, not automatic authority.

When a Wisdom Library page yields an important claim:

identify the underlying text/commentary,

capture the exact work + passage/location if possible,

prefer the primary text / scholarly edition / project corpus as the final evidence target,

do not cite Wisdom Library's generic explanatory prose as if it were primary evidence.

D. External scholarship

Prefer:

primary texts,

critical editions,

peer-reviewed articles/books,

publications by specialists,

institutional repositories,

reliable manuscript catalogues.

Existing translations are evidence for how another translator solved a problem, not proof that the solution is correct.

3. Evidence hierarchy

Never bend the passage to fit doctrine.

Use this hierarchy:

current Sanskrit / textual state
→ grammar and syntax
→ same-work context
→ direct primary-text parallels
→ traditional commentaries
→ historical school/context evidence
→ modern specialist scholarship
→ existing translations
→ broader comparative interpretation

A later commentary may illuminate an earlier root text, but must not be silently projected backward into it.

A conceptual parallel is weaker than a direct verbal or syntactic parallel.

A famous interpretation is not stronger merely because it is famous.

4. Build an evidence packet before drafting

Do not write C1 directly from T3.

First construct an internal evidence packet.

For each target passage record:

PASSAGE
- passage_id
- Sanskrit
- T3
- T3.1

DECISIONS
- R1 cruxes
- T2 rivals
- R2 decisions
- hard core
- OPEN / PREFERRED / RECONSTRUCTED points

TERMS
- important technical terms
- accepted senses
- relevant trajectory nodes
- passage-specific lexical decisions

CONTEXT
- preceding/following passage
- section/chapter frame
- ritual/philosophical/liturgical setting
- date/tradition/genre where supportable

EVIDENCE
- primary parallels
- commentary glosses
- anchor translations
- scholarship
- textual variants

UNRESOLVED
- exact open questions
- missing evidence

Only after the packet is assembled should C1 prose be written.

5. C1 writing style

Target style:

Dyczkowski-like explanatory density, but shorter, clearer, and more explicit about evidence and uncertainty.

C1 should be:

concise,

technically precise,

readable,

minimally rhetorical,

direct about what each sentence contributes.

Prefer 150–500 words per ordinary verse/passage.

Use more only when the passage genuinely contains multiple cruxes.

Avoid:

generic introductions,

spiritualized filler,

repetition of the translation,

"this profound verse teaches...",

long histories unrelated to the specific wording,

pretending every term activates the entire later system.

6. Required C1 structure

For an ordinary passage, produce these sections internally even if the final rendering is compact.

A. Core sense

One to three sentences answering:

What is being said here?

This should explain the proposition/action/ritual instruction, not merely rephrase T3.

B. Why this reading

Explain the decisive evidence:

grammar
lexical choice
same-work context
parallel
commentary
school-specific usage

Use the smallest sufficient evidence chain.

Example logic:

X is taken here as "..." rather than "..." because the construction requires ..., and the same usage occurs at [passage]. A later commentary explicitly glosses the term as ..., which supports but does not independently determine the root reading.

C. The crux / uncertainty

If there is a real uncertainty, state it directly.

Example:

The uncertain point is nirānande. The form permits ..., while the pairing with paramānande favors .... The latter is therefore preferred, but the former remains viable.

Do not create an uncertainty section when the passage is secure.

D. Larger significance

Only after the local meaning is established, explain the wider doctrinal/ritual significance.

Keep this tied to evidence.

Bad:

This demonstrates the nondual nature of everything.

Better:

In the Krama setting, this pairing anticipates the contrast between sequential manifestation and the awareness in which that sequence is apprehended; compare [passage].

7. Sentence-level epistemic discipline

Every nontrivial claim must be one of:

TEXTUAL
what the Sanskrit directly says

GRAMMATICAL
what syntax/morphology supports

INTERPRETIVE
the preferred explanation of the passage

HISTORICAL
claim about period/tradition/development

ATTRIBUTED
a named commentary/scholar's interpretation

SYNTHESIS
Pāṭala's current best synthesis across evidence

Do not blur them.

Where useful, write explicitly:

"The text says..."
"Grammatically..."
"Bhāskara glosses..."
"Sanderson argues..."
"Pāṭala therefore prefers..."

Do not use vague authority phrases such as:

"traditionally understood as",

"scholars say",

"in Tantra this means",unless the supporting source is actually identified.

8. C1 may challenge T3

C1 is allowed to discover that T3 is inadequate.

It must never silently mutate T3.

If C1 finds a serious problem, emit:

TranslationChallenge
- target passage/version
- challenged decision
- current reading
- proposed revision
- evidence
- severity

Then route it back through adjudication for a future T3 version.

C1 may say:

The current T3 is probably too strong here...

It may not simply replace the translation in the commentary and pretend nothing changed.

9. Existing C1s are evidence, not scripture

When another C1 is relevant:

cite/reference it by stable ID,

identify what claim is being reused,

follow its evidence when needed,

do not create circular support.

Bad:

C1-A supports C1-B
C1-B supports C1-A

Good:

C1-A → cites primary passage P
C1-B → reuses claim from C1-A
     → can still trace claim back to P

Every C1 must remain peelable back to primary/resource evidence.

10. Structured outputs

In addition to prose commentary, emit structured proposals where warranted.

Possible outputs:

TermSenseAssignment
TermHistoryAssertion
ParallelAssertion
TextRelation
DoctrinalAssertion
BibliographicClaim
TranslationChallenge
CommentaryClaim
ResearchQuestion

All such outputs are PROPOSALS unless review promotes them.

Never auto-write them into accepted ledgers.

Each proposal should carry:

id
target
claim
evidence_links
origin = machine
status = proposed
certainty
derived_from_c1

11. C1 evidence requirements

A C1 can be produced with different evidence depths, but the state must be explicit.

Recommended evidence state:

C1_EVIDENCE_COMPLETE

requires:

source passage resolved,

T3/R2 available,

all R2 OPEN/RECONSTRUCTED decisions represented,

important technical terms checked,

neighboring context checked,

local corpus parallels checked,

bibliography checked,

targeted external research performed where needed,

important external claims tied to identifiable sources,

no unsupported certainty.

If some are unavailable:

C1_EVIDENCE_PARTIAL

and list the missing items.

Do not label a C1 complete merely because prose exists.

12. Web-search discipline

Before each web query, formulate the unresolved question.

Examples:

"Kramasadbhāva nirānanda parallel Sanskrit"
"Krama nirānanda Mahākālī"
"Kramasadbhāva scholarship Krama date"
"site:wisdomlib.org khecarī Tantra"
"Tantrāloka 3.143 kula akula translation"

Search narrowly.

When multiple sources repeat the same claim, prefer the earliest/primary/specialist source rather than counting repetition as corroboration.

Record:

query,

useful result,

source identity,

claim it supports,

whether it changed the commentary.

Do not cite search-result snippets as evidence.

13. Anti-hallucination rules

NEVER:

invent a Sanskrit parallel,

invent a verse number,

invent a commentary gloss,

invent manuscript evidence,

infer a school's doctrine merely from the text's later reception,

call a machine-generated claim "reviewed",

present a generic dictionary meaning as the local sense,

convert an absent source into evidence,

claim chronology from array/order alone,

hide a disagreement that R2 marked OPEN.

If a source cannot be verified:

UNVERIFIED_REFERENCE

and do not use it as decisive evidence.

14. Workflow

For each passage:

INSPECT
↓
load all available stack layers

CONTEXTUALIZE
↓
neighbors + work/section + bibliography

RESEARCH
↓
local corpus first
then targeted web/Wisdom Library/scholarship

BUILD EVIDENCE PACKET
↓
cruxes + decisions + evidence + uncertainty

WRITE C1
↓
core sense
why this reading
uncertainty
larger significance

SELF-AUDIT
↓
does every nontrivial claim have a source or explicit synthesis status?

EMIT PROPOSALS
↓
terms / parallels / challenges / claims / questions

SAVE
↓
C1 prose + evidence manifest + proposal bundle

15. Self-audit checklist

Before marking C1 ready:

I read the Sanskrit, not only T3.

I inspected R1 cruxes and R2 decisions.

I checked whether T2 exposed a materially different reading.

I checked neighboring passages.

I checked relevant term senses/term history.

I searched the local corpus for known parallels.

I checked anchors/commentaries when available.

I used web research only for concrete unresolved questions.

Important web claims are tied to identifiable sources.

I distinguish root text from later commentary.

I state OPEN uncertainty rather than flattening it.

I do not use vague "Tantra says..." claims.

C1 does not silently change T3.

Structured outputs remain proposals.

Another agent can trace every important claim backward.

If any failed item materially affects the interpretation, do not mark C1 complete.

16. Output format

Recommended stored artifact:

---
c1_id: ...
passage_id: ...
work_id: ...
derived_from_t3: ...
evidence_state: complete | partial
origin: machine
editorial_status: proposed
---

# C1 Commentary

[razor-sharp commentary]

## Cruxes
[only if needed]

## Evidence
- [stable passage/resource id] — what it supports
- [...]

## Open questions
- [...]

## Structured proposals
- [...]

For a work-level C1, group passage commentaries by section and add only a short work-level synthesis where repeated evidence warrants it.

17. Stop condition

C1 is done when:

A careful reader can understand what the passage says, why that interpretation was chosen over serious rivals, what remains uncertain, and exactly where to inspect the supporting evidence — without reading the entire translation pipeline.

It is NOT done merely because:

every field is populated,

a long commentary was produced,

web research returned many sources,

or the prose sounds authoritative.

The goal is maximum explanatory value per sentence, with a traceable evidence chain.

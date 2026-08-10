# Advice Response — Pāṭala next phase

All files read. Here is the advisory, grounded in what is actually in the repo (I verified the pipeline, the graph types, the term ledger, the trajectories, the occurrence endpoint, the 1.8 run record, and the kramasadbhava passage index).

════════════════════════════════════════════════════════════════
PĀṬALA — NEXT-PHASE ADVISORY
════════════════════════════════════════════════════════════════

1. THE #1 PRIORITY (and the first concrete step)
────────────────────────────────────────────────
Milestone B — the 25-verse research unit — is the single highest-leverage next
action, but only if it is executed as a graph-annotated research object, not as
25 translations. Your question 1 candidates (b) and (c) are not separate phases;
they are modes of Milestone B. The unit forces the graph encoding and the
sense-assignment wiring to become real at the smallest scale that matters, and
it produces the material for Milestone C. Doing (b) alone (bulk-converting 4,395
passages into graph objects) is busywork with zero scholarly payoff. Doing (c)
alone (building abstract sense-assignment primitives) has no test corpus to
validate them against. The unit gives both a reason to exist.

FIRST CONCRETE STEP (this week):
Define the unit as a first-class object. Create data/corpus/units.ts with a
new "unit" GraphObjectType (one enum value in data/corpus/graph.ts, one
interface, lint coverage in pipeline/validate_graph.py), and instantiate:

  data/corpus/units/kramasadbhava-stuti-1.ts
  { id: "pt:unit:kramasadbhava:stuti-1", work: "kramasadbhava",
    range: { chapter: 1, verses: "1.1–1.28" }, genre: "stuti",
    structure: "vocative-chain epithets; body-locus sequence",
    term_families: ["ananda", "kali", "kula", "krama", "body-loci",
                    "bindu-nada-visarga", "sunya-vyapti"],
    known_cruxes: ["nirānande 1.8"] }

Boundary decision worth making now: 1.1–1.25 is a round number, but 1.1–1.28 is
the real textual unit — the stuti closes at 1.28 with "etat stutipadaṃ kṛtvā
tathedaṃ vākyamabravīt" ("having made this hymn, [he] then spoke this speech");
1.29 opens the dialogue section (śrībhairava uvāca). I would take 1.1–1.28 and
note the deviation in the manifest. A Krama specialist will immediately
recognize 1.12–1.27 as a map of the goddess onto the subtle-body stations
(dvādaśānta, ṣoḍaśānta, brahmadvāra, kaṇṭha, tālu, hṛtpadma, kanda, kauṇḍalya)
plus the emission hierarchy (visarga → nāda → bindu) — that is the "repeated
deity vocabulary" your question 2 asks about, and it is exactly what makes the
unit cohesive rather than 25 isolated verses.

Concurrently: seed the unit's T1s from what already exists. pipeline/
gold_records/ already holds T1-stage records for ~17 of the unit's verses
(gold_from_t1.py ingests them from the sanskritree T1 corpus), and
data/corpus/passages/kramasadbhava.jsonl has clean Sanskrit for all 563 verses.
Do NOT re-run T1 through the model for verses that already have it. Write a
small batch driver (pipeline/run_unit.py) that walks the unit's passage ids,
loads or seeds T1, then runs R1→T2→R2→T3→T3.1 per record and persists failures
with reasons — this is exactly the working rule's success criterion ("issue
translate 1.1–1.28, come back later, get 27 completed + 1 failed with reason").
Also fix the known trivial blocker first: raise the hermes subprocess timeout
in pipeline/model.py so T3.1 stops timing out (the one loose end of A1).

2. RANKING THE FIVE CANDIDATES (your question 1)
────────────────────────────────────────────────
(a) Milestone B (25-verse research unit)  → DO FIRST. It subsumes (b) and (c).
(b) Encode corpus as scholarly graph      → NOT STANDALONE. Fold into B: encode
   only what the unit touches (its 28 passages, its terms, its witnesses).
   The graph grows by use, not by bulk conversion. Your own 7th invariant
   ("convenient bundles are projections, not the canonical model") argues
   against mass-importing anything not yet reviewed.
(c) Term-sense → assertion wiring         → NOT STANDALONE. It is Phase 2 of B
   (below), driven by the nirānanda re-adjudication. The primitive already
   exists in graph.ts (sense_assignment, term_history_assertion annotation
   types, ReviewScope "term_sense"); what is missing is the first real
   instance with evidence and a review event.
(d) Bibliography deepening                → JUST-IN-TIME ONLY. Where a C1 hits a
   wall (e.g. the Mahānaya edition record, if nirānanda research needs it),
   deepen the specific record in data/atlas/audited.ts. The unit's C1s will
   tell you which records matter. A standalone audit sweep of 58 seed records
   is the translation-factory trap in new clothes.
(e) Reader/workshop UI                    → LAST, per DEV_PLAN §0.3 ("the UI is
   the last thing"). The dossier generator (Phase 4 below) is the UI
   substitute until there is depth to render.

3. THE PHASED PLAN (goal + demonstrable artifact each)
────────────────────────────────────────────────
Phase 0 — THE UNIT OBJECT (this week)
  Goal: the research unit exists as an addressable object; the batch loop is
  proven at 25-verse scale.
  Artifact: data/corpus/units/kramasadbhava-stuti-1.ts + 28 stacked passage
  records in the state machine (1.8 already done; 27 new, seeded T1 where
  gold records exist) + the "unit" GraphObjectType in graph.ts with lint
  coverage (validate_graph.py gains: unit passages exist and fall inside the
  declared range).

Phase 1 — THE LEXICAL NETWORK (the "not 25 isolated translations" part)
  Goal: repeated epithet vocabulary of the unit becomes machine-proposed,
  reviewable term_occurrence annotations targeting passage ids.
  Artifact: pipeline/lexical_network.py — a deterministic extractor over the
  unit's 28 Sanskrit passages emitting {target: pt:passage:..., type:
  term_occurrence, payload: {lemma, surface, span}} records, plus a quick
  human confirmation pass by you (it is 28 verses; confirmation is minutes,
  not weeks). The ānanda family alone gives four live occurrences:
  paramānande 1.8, nirānande 1.8, ānandapadamadhyasthe 1.15,
  āhlādapadagarbhe 1.15. saṃhārakramage 1.22 is a gorgeous test case: does
  "krama" here carry the school-technical resonance or the ordinary
  "sequence"? That single decision is a trajectory question, not a
  translation question.

Phase 2 — SENSE ASSIGNMENTS AS AUDITED ANNOTATIONS (the nirānanda fix)
  Goal: per-occurrence sense assignments with evidence + review events become
  real; the nirānanda case is re-adjudicated and the R2 CONSTRAINED verdict is
  either confirmed or overturned on evidence, not vibes.
  Artifact: the first complete instance of the chain (see section 4 below) —
  occurrence annotation → sense_assignment with evidence (Mahānaya's
  "Bliss of Stillness" rendering of 1.8, nirācārānanda in the Kubjikā
  material, Dyczkowski's edition) → ReviewEvent scoped term_sense, reviewer
  = you → trajectory node with grounded_by pointing at the assignment. The
  nirānanda dossier is a committed file, not a chat exchange.

Phase 3 — THE C1 LAYER (your main model, not Hermes)
  Goal: 28 C1s as structured annotations (type: commentary) per the
  write-commentary skill and pipeline/schema.py's stage_C1 contract, each
  emitting TermSenseAssignment / TermHistoryAssertion / ParallelAssertion /
  TranslationChallenge proposals. You review the strongest 5–8; ReviewEvents
  recorded.
  Artifact: data/c1/ (or annotations with type commentary) + the review trail.

Phase 4 — THE DEMONSTRABLE ARTIFACT (the month's deliverable)
  Goal: one page a specialist can react to in one sitting, generated FROM the
  graph so it is provably an output of the audited work.
  Artifact: scripts/build_unit_dossier.py rendering the unit's annotations
  into docs/dossiers/kramasadbhava-stuti-1.md (see section 6) + the 5
  strongest passages prepared in the Milestone C format (Sanskrit / close
  translation / crux / alternative / evidence / C1).

Phase 5 — AFTER THE MONTH
  Milestone C (one real Krama/Śaiva specialist conversation on the dossier).
  Then: next unit (1.29–1.60, the praśna section, is the natural continuation),
  then just-in-time bibliography deepening where the C1s exposed gaps, then —
  and only then — the reader/workshop UI rendering the API.

4. THE NIRĀNANDA GAP — MAKING SENSE ASSIGNMENTS FIRST-CLASS
────────────────────────────────────────────────
The gap today is concrete and visible in the code:
  - GET /api/terms/:lemma/occurrences (app/api/terms/[lemma]/occurrences/
    route.ts) is honest substring search with lemmatized:false — there is NO
    occurrence layer at all. The comment in the route even says so.
  - data/terms.json senses carry string evidence ("Sanderson: ..."), not
    structured evidence links.
  - data/corpus/trajectories.ts is hand-authored curated interpretation
    (origin: reference_map | dossier | manual) — fine as the Synthesis layer,
    but nothing in the system grounds it in per-passage audited assignments.
  - The graph model already HAS everything needed (graph.ts: term_occurrence,
    sense_assignment, term_history_assertion, ReviewScope "term_sense",
    origin/status/certainty separated). It is unused.

The fix is not a new primitive. It is the first real instances:

  1. terms.json gains a nirānanda entry with two senses:
     nirānanda.privative ("bliss-less", certain — morphology alone supports
     this) and nirānanda.krama.technical ("the bliss of stillness / beyond
     the bliss-absence pair", traditions: [krama]) — the second enters via
     data/term_proposals.jsonl first (kind: editor, your model, not machine),
     and is promoted to accepted by a review event.
  2. One occurrence annotation targeting pt:passage:kramasadbhava:1.8
     (payload: {lemma: nirānanda, surface: nirānande}).
  3. One sense_assignment annotation TARGETING THE OCCURRENCE (annotations on
     annotations, exactly as SCHOLARLY_GRAPH.md §2 models) with
     evidence: [{resource: Mahānaya ed. record, locator: "1.8", role:
     "parallel"}, {resource: Kubjikā material record, locator: "nirācārānanda",
     role: "defines"}, {resource: Dyczkowski ed., role: "supports"}],
     status: "checked" (you), certainty: "probable".
  4. One ReviewEvent: {target: assignment-id, scope: "term_sense", reviewer:
     {kind: "editor", id: you}, outcome: "accept", reason: "..."} — or, if you
     want the specialist's verdict to be the deciding one, outcome
     "needs_specialist" and the dossier carries that state honestly (that is
     itself a great Milestone C opener).
  5. TrajectoryNode "nirānanda.krama.bliss-of-stillness" added to
     trajectories.ts with grounded_by: [assignment-id] — and the history
     endpoint (app/api/terms/[lemma]/history/route.ts) starts serving the
     assignment + review trail alongside the curated trajectory, labeled.
  6. validate_graph.py extends: occurrences target existing passages;
     assignments resolve to terms.json or proposals; review events reference
     real annotation ids; machine-origin never accepted; review scopes valid.

Then the term-history engine becomes an output of audited work in the honest,
small way: each trajectory node carries the annotation ids that ground it, and
the nirānanda node's status flips only because a review event exists. A
full generator (derive trajectories from accepted assignments) is a later
script, once there are ~20 grounded nodes — building it for one node is fake
work. The R2 classification from the 1.8 run ("CONSTRAINED") should be
revisited as a lexical_decision annotation with the R2 payload as its
predecessor and the new evidence attached — that makes the whole "the
adjudicator was overconfident" lesson into a versioned, reviewable object
instead of a note in an experiment file.

5. HERMES ACCUMULATES vs. YOUR MAIN MODEL PRODUCES (question 2)
────────────────────────────────────────────────
Hermes (the pipeline, state_machine.py + model.py, run as a batch):
  - the stacked passage records T1→R1→T2→R2→T3→T3.1 (seeded T1 from gold
    records, not regenerated)
  - R1 crux maps and R2 decision taxonomies (these are already first-class
    stage payloads in pipeline/schema.py)
  - machine-proposed term_occurrence annotations (Phase 1 extractor) and
    machine-proposed parallel candidates
  - the failure log with reasons — that is output, not noise
  All of it origin=machine, status=proposed. Hermes never writes accepted
  knowledge. The state machine is the accumulation device; the batch driver
  is its unit-level face.

Your main model (you, with anchored context — per the strategic reset, this is
NOT a hermes -z job; pipeline/c1_18.py exists but the verdict in
STATE_OF_PLAY.md stands: do not chase C1-via-Hermes):
  - the C1s: 150–500-word interpretation per passage per the write-commentary
    skill's style and structure sections, as stage_C1-shaped records +
    graph annotations (type: commentary)
  - the section-level synthesis: the stuti's structure map, the doctrinal
    frame (twelve Kālīs, the body-locus hierarchy), the reading of the unit
    as a whole — this is what makes the unit cohesive and it cannot be
    machine-generated
  - every structured proposal the skill's §10 lists: TermSenseAssignment,
    TermHistoryAssertion, ParallelAssertion, TranslationChallenge,
    ResearchQuestion — each carrying evidence links, origin=editor, status=
    proposed
  - the review events (as editor), and later the specialist's (Milestone C)
  These enter as proposals too; only your review event promotes them.

The rule that keeps the object cohesive: every C1 claim must be peelable to
passage ids and resource ids (the skill's §9 "peelable back to primary/
resource evidence"), and the unit manifest is the index that ties the 28
passage objects, the ~40 occurrence annotations, the sense assignments, and
the C1s together. The unit object is what stops this from being "25 isolated
translations" — every artifact references pt:unit:kramasadbhava:stuti-1.

6. THE SMALLEST ARTIFACT TO SHOW A KRAMA SPECIALIST THIS MONTH
────────────────────────────────────────────────
A single generated dossier: docs/dossiers/kramasadbhava-stuti-1.md, produced
by scripts/build_unit_dossier.py from the annotations (never hand-written —
it must be an output of the system), roughly 3–5 pages:

  1. Unit frame: Kramasadbhāva 1.1–1.28, the opening stuti of the Goddess;
     source edition cited (Dyczkowski ed., Muktabodha, MS 1-76 Saivatantra
     144; NGMPP A 209/23 — this already lives in the passage index).
  2. The structure map: the vocative-chain frame (1.7–1.8: pādau jagrāha
     ... stutipūrvam), the ānanda family, the body-locus sequence
     (brahmadvāra → kaṇṭha → tālu → hṛtpadma → dvādaśānta/ṣoḍaśānta →
     kanda/kauṇḍalya), the emission hierarchy (visarga → nāda → bindu), the
     four states (jāgrat/svapna/suṣupti/turyā at 1.26).
  3. Compact Sanskrit + working T3 for the 28 verses.
  4. The ānanda-family dossier: all four occurrences with their sense
     assignments, evidence, and review status — including the nirānanda
     re-adjudication with the Mahānaya and nirācārānanda evidence. This is
     the project's whole thesis on one page: the adjudicator's CONSTRAINED
     verdict, the external evidence, the reviewed outcome, the reviewer.
  5. Three C1s: 1.8 (the nirānanda crux), 1.3 (Kālī on Bhairava, the
     Mahākālakalāśinī locus), 1.22–1.23 (krama + the kanda/kauṇḍalya
     stations).
  6. A review legend (origin / status / certainty — the three dimensions
     never conflated) and 3–5 sharp questions to the specialist, e.g.:
     "Is saṃhārakramage (1.22) a technical Krama echo or ordinary
     'sequence'?" and "Does nirānande's pairing with paramānande (1.8) force
     the privative, or does the technical 'stillness' sense better fit the
     stuti's hierarchy?"

A specialist can read that in an hour, and every line traces to a passage id,
annotation id, or review event. It is simultaneously the Milestone C
conversation starter and the proof that the infrastructure produces scholarly
artifacts — the strategic reset's thesis, demonstrated.

7. WHAT NOT TO DO NEXT
────────────────────────────────────────────────
- Do NOT regenerate T1 through the model for verses that already have T1
  records (gold_records) — seed and run R1→T3.1 only. Model calls on the
  least-valuable stage are the translation-factory trap.
- Do NOT chase C1-via-Hermes (pipeline/c1_18.py stays a reference, not a
  product). The backend latency and the strategic verdict both say: your main
  model produces C1s.
- Do NOT bulk-encode the 7 segmented works into the graph. Encode the unit.
- Do NOT build an abstract sense-assignment subsystem; build the nirānanda
  instance. One reviewed instance beats a schema with no data.
- Do NOT start a Sanskrit lemmatizer / lemma-index project. The substring
  honesty in the occurrences route is the right posture; curated per-passage
  annotations are the upgrade path, and a real inflection-aware lemmatizer is
  a multi-month rabbit hole with a commercial-grade alternative already
  existing (the red team's instinct, and DEV_PLAN's "later capability",
  are correct).
- Do NOT touch the 🔲 DEV_PLAN endpoints (occurrences with filters, term/
  history beyond the trajectory, parallels, audit, commentaries, TTS) until
  the unit exists to serve. audit_translation in particular consumes corpus
  depth that only the unit creates.
- Do NOT do the bibliography audit sweep (58 seed records) as a workstream.
  Just-in-time only.
- Do NOT open a DB layer; TS/JSON data at this scale is right.
- Do NOT start the reader/workshop UI. The dossier generator is the UI until
  Milestone C says otherwise.

8. THE FIRST WEEK, CONCRETELY
────────────────────────────────────────────────
1. Add "unit" to GraphObjectType in data/corpus/graph.ts + validate_graph.py
   lint (unit range resolves against the passage index).
2. Write data/corpus/units/kramasadbhava-stuti-1.ts (decide 1.1–1.28).
3. Raise the hermes subprocess timeout in pipeline/model.py (the T3.1 fix).
4. Write pipeline/run_unit.py (seed T1 from gold records, run R1→T3.1 per
   passage, persist failures with reasons) and launch the batch.
5. While it runs: write pipeline/lexical_network.py against the 28 Sanskrit
   passages (deterministic, no model calls).

After that, the phases above take over. The one thing everything else hangs
off is step 1–2: the unit as an object. That is the single highest-leverage
action, and it is one file.

One caution: the batch (step 4) is the only place where model plumbing may
legitimately demand attention — and only if it prevents the batch from
running at all. That is the working rule's own exception, so it stays
consistent with the strategic reset rather than reopening the rabbit hole.
# Requesting Strategic Advice — What's Next for Pāṭala

*2026-08-10. A request for extensive advice. Please read the three strategic docs and my
current state, then propose a concrete plan for the next phase.*

---

## The confirmed current state (verified)

- **Automated translation pipeline works** (T1→R1→T2→R2→T3 via the durable state machine,
  `model.py` shelling to `hermes -z`). **C1 we do ourselves** with a main model + anchored
  context — we are NOT chasing machine C1 generation.
- **Milestone A1 proven**: Kramasadbhāva 1.8 ran the full machine-adjudication loop with
  real interpretive disagreement found + resolved. The `nirānanda` crux showed the real
  need: the adjudicator was overconfident (CONSTRAINED) without historical lexical evidence.
- **The six primitives + scholarly graph** are built and linted (Identity/Assertion/
  Evidence/Provenance/Review/Rights; Work/Witness/Passage/SourceSpan/Person/Term/Sense/
  Resource + annotations).
- **API/MCP**: 43 routes, 29 MCP tools, 84/84 tests, OpenAPI, docs-site nav.
- **Corpus**: 7 works segmented; 1 work (kramasadbhava) translation-ready (derived).
- **Strategic reset**: Pāṭala is provenance + adjudication infrastructure, not a
  translation factory. Hermes owns model plumbing. The moat = evidence-backed scholarly
  judgments (Sense + Synthesis layers).

---

## The three strategic docs to ground the plan

### `docs/endgame2.md` (the Tantra Hub)
The destination is a **living bibliography + text-reader + translation-workshop + commentary +
media hub**, built on:
- a **bibliography spine** ("WHAT EXISTS?" per text: title, school, sources, translations,
  scholarship, relations)
- a **reader** (Sanskrit | English | commentary, verse-anchored)
- a **translation workshop** (verse-level scholar corrections → versioned community text)
- **stable IDs** (`tantra:text:kubjikamata:3.14`) + a **provenance hierarchy** so agents
  treat site-generated material as provisional
- the machine-facing layer: API/MCP, `audit_translation`, TTS, provenance hierarchy

### `docs/nextdev.md` (the six primitives)
Everything is a view over: **Identity, Assertion, Evidence, Provenance, Review, Rights**.
- objects vs claims vs events
- `status` ≠ `certainty`; machine proposes, humans review
- crosswalks (resolve, don't duplicate); rights matrix with `unknown` valid
- passage IDs as the fundamental addressable unit

### `docs/DEV_PLAN.md` (the API-first build order)
- API/MCP is the product; the site renders the API
- "no endpoint, no UI"; provenance non-negotiable
- phase order: bibliography AI-readable → read API + OpenAPI → MCP → provenance features
  → UI last

---

## The specific questions I need your advice on

1. **What is the single highest-leverage next phase** given the pipeline works and C1 is
   manual? Rank: (a) Milestone B (25-verse research unit), (b) encode the corpus as the
   scholarly graph, (c) term-sense→assertion wiring (the nirānanda gap), (d) the
   bibliography deepening, (e) the reader/workshop UI.

2. **How should we do the 25-verse research unit (Milestone B)** — as a contiguous
   *research object* (passages + section-level lexical network + cross-passage parallels +
   repeated deity vocabulary), not 25 isolated translations? What should Hermes accumulate
   vs. what should the user's main model produce (the C1s)?

3. **The nirānanda gap**: how do we make "sense assignments as first-class annotations
   with evidence" a real, reviewable primitive — so a term-history claim carries its
   passages + scholarship + reviewer, and the trajectory engine becomes an *output* of
   the audited translation/commentary process rather than hand-authored?

4. **Sequence of the next milestones** — what order, and what's the smallest unit that
   produces a demonstrable scholarly artifact I can show a Krama specialist?

5. **What should we NOT do** next (given the strategic reset)?

Please propose a concrete, phased plan (with a clear first action) grounded in the three
docs and my current state.

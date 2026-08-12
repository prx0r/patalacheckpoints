# Pāṭala — Process Notes & Current State (2026-08-10)

*The living account of what Pāṭala is, where the build stands, and where it's going.
Companion to `HANDOVER.md` (the handover) and `docs/PIPELINE_SOURCE_MANUAL.md` (the
code manual). This file records the *why* and *where-we-are* — the strategic
reorientations, the decisions made, and the honest state of each subsystem.*

---

## 1. The mission (reaffirmed)

Pāṭala is **not** a translation-prompt project. It is:

> **Provenance + adjudication infrastructure for tantric textual knowledge.**

The automated translation pipeline is **one subsystem** — a boring Hermes job that
runs, retries, records failures, and moves on. The real product is the scholarly loop:

```
SOURCE IDENTITY
→ PASSAGE IDENTITY
→ ASSERTIONS / TRANSLATION DECISIONS
→ EVIDENCE
→ REVIEW
→ ACCEPTED / DISPUTED CURRENT STATE
→ COMMENTARY
→ REUSABLE KNOWLEDGE GRAPH
```

**The six primitives are the real architecture** (per `nextdev.md`):

```
IDENTITY · ASSERTION · EVIDENCE · PROVENANCE · REVIEW · RIGHTS
```

Everything else — translation choices, term-history claims, parallels, bibliography
claims, even C1 commentary — is a view over those primitives. A translation choice is:
an *Assertion* → targeting a *passage* → supported by *evidence* → machine *provenance*
→ human *review*.

---

## 2. Where we are (honest)

### The pipeline is built and proven, but the model backend is the bottleneck
- **Durable state machine** (`pipeline/state_machine.py`): load → transition → run →
  audit → persist → reload. Prerequisite-gated transitions, versioned stages,
  stage-local audits, invalid-stage RETRY. **Verified with deterministic mocks.**
- **Stage-contract layer** (`pipeline/contracts.py`): empty/`{}` strict output is now
  INVALID, not silently accepted. The `kramasadbhāva-1.8-v1` run exposed the bug
  (R1/T2/R2 were silently empty); it's fixed and mock-verified.
- **Model interface switched to Hermes**: `model.py` now shells out to `hermes -z`
  instead of calling the API directly. Hermes owns provider reliability, retries,
  JSON repair, backoff. We keep the schemas/contracts/audit.
- **Milestone A in progress**: building one complete scholarly object for
  `kramasadbhāva 1.8` (T1→R1→T2→R2→T3→T3.1→C1) through the real Hermes path. T1 done
  (real content); advancing through the stages.

### The corpus & bibliography
- 4,395 segmented passages (7 works); referential integrity clean.
- 1,542 OCHS manuscript witnesses resolved to 18 works.
- 15 accepted term senses + trajectories (kula, krama, khecarī, śakti, vimarśa, visarga).
- **1/68 works translation-ready (derived)** — Kramasadbhāva (the first). The gate is
  honest: readiness is *derived* from stable source_id + rights + coverage, not asserted.

### The API/MCP
- 19 API routes, 13 MCP tools, 83/83 test suite passing, OpenAPI spec, docs-site nav.

---

## 3. The strategic reorientation (this session)

We went deep into the model-interface rabbit hole (JSON mode, response_format, retries,
repair). The verdict that pulled us back:

> **No more model-interface rabbit holes unless they prevent Hermes from running
> batches at all. Hermes owns plumbing. We own the scholarly model.**

The automated translation is only the middle box in the real flywheel:

```
SOURCES → STRUCTURED CORPUS → MACHINE ANALYSIS → HUMAN ADJUDICATION
→ VALIDATED KNOWLEDGE → { C1s, API/MCP } → dossiers → essays → videos/courses
→ more readers → scholars/contributors → CORPUS
```

**Success in ~6 months is NOT "100,000 translated verses."** It is:
```
5–10 works properly identified
1–3 works deeply segmented
100–300 serious passage records
50 excellent C1s
20–30 reviewed lexical decisions
useful term trajectories
several known parallels
full provenance
a handful of corrections from real experts
one scholar genuinely using the system
```
That's a growing history of **evidence-backed scholarly judgments** — the thing AI
can't trivially recreate.

---

## 4. The three milestones (the real roadmap)

### Milestone A — one complete scholarly object
`kramasadbhāva 1.8`: source → translation stack → C1 → evidence → structured claims →
audit. Use whatever model works. We are validating the *scholarly artifact*, not the API.

### Milestone B — a coherent small corpus
`kramasadbhāva 1.1–25` (or another contiguous unit), automated by Hermes. Inspect:
translation quality, C1 quality, term consistency, cross-C1 references, evidence
coverage, failure patterns.

### Milestone C — external scholarly feedback
Take 5 strongest passages, present (Sanskrit / close translation / key crux /
alternative / evidence / C1) to a real Krama/Śaiva specialist. Ask: what's wrong?
what evidence is missing? would this format save you time? **One strong conversation
here beats another month of agent infra.**

---

## 5. The immediate working rule

> **No more model-interface rabbit holes unless they prevent Hermes from running
> batches at all.**

Hermes owns: retry, JSON repair, provider switching, timeouts, backoff, schema
compliance, persistence, resumption, logging. The success criterion is:

> I issue `translate kramasadbhava 1.1–1.50`, come back later, and get 46 completed
> records + 4 explicitly failed records with reasons.

That's what automation is for. We spend attention on: **what objects exist, what
claims mean, what counts as evidence, how review works, how C1s become cumulative
knowledge, and how scholars/institutions can participate.**

---

## 6. The strategic docs map (read these for direction)

| Doc | What it is |
|---|---|
| `docs/NORTHSTAR.md` | the master strategy (positioning, moat, economics, roadmap) |
| `docs/nextdev.md` | the six primitives (the real architecture) |
| `docs/endgame1..5year.md` | the vision specs (translation lab, hub, infra, economics, 5-year) |
| `docs/ENDGAME_SITE_SPEC.md` | the reader site (five levels of authority) |
| `../sanskritree/corpus/targets/canonical_reference_map.md` | the historical map + glossary dossiers |
| `../sanskritree/corpus/targets/markguidance.md` | the Recognition Enquiry (Pratyabhijñā) |
| `../sanskritree/corpus/targets/leapfrog_map.md` + `leapfrog_guide.md` | the corpus-ladder strategy |
| `../sanskritree/corpus/targets/translation_flow_spec.md` | the T1→C1 flow spec |
| `docs/positioningpartners.md` | the partnership strategy (the connective layer) |
| `docs/PEER_REVIEW_REDTEAM.md` | the red-team verdict + 7 invariants |
| `docs/STACKED_ARTIFACT_SPEC.md` | the per-work stacked artifact |
| `docs/PIPELINE_SOURCE_MANUAL.md` | the code manual |

---

## 7. The invariants (locked)

1. Stable IDs never depend on mutable wording.
2. Work ≠ witness ≠ digital representation ≠ canonical passage.
3. Annotations are independent from the base text and independently addressable.
4. Machine output always enters as a proposal, never authority.
5. Every meaningful scholarly judgment can carry evidence and review history.
6. Translation prose and interpretive decisions have independent version histories.
7. Convenient API bundles are projections over normalized scholarly data, not the
   canonical data model.

---

## 8. What's next (priority)

1. **Finish Milestone A** — get `kramasadbhāva 1.8` to a real C1 through Hermes.
2. **Run Milestone B** — a 25-verse contiguous unit, automated.
3. **Write the scholarly-graph schema doc** (Work/Witness/Passage/SourceSpan/Person/
   Term/Sense/Resource + annotations) — the canonical model that must survive years.
4. **Milestone C** — one real scholar conversation.
5. **Deepen the bibliography just-in-time** — only where C1 exposes missing info.

**Not now:** scholar dashboard, marketplace, payments, fancy RAG, custom OCR, all-69
bibliography completion, consumer UI.

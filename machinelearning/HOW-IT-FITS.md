# HOW IT ALL FITS — the docs → existing systems → auditable arguments → vision

*2026-08-12. The synthesis: how every piece of ML/scholarly work we've built or found applies to Pāṭala's
EXISTING systems, how to actually generate logical arguments with auditable roots, and the visionary use
cases beyond what's obvious. Grounded in the verified current state, not aspiration.*

---

## 0. The current system (verified — the substrate everything runs on)

Pāṭala already has, live and working:
- **29 API routes** incl. `resolve`, `verify/{quote,claim-structure,trace-dependency,counterevidence}`,
  `themes`, `hub`, `passages`, `relations`, `spines`.
- **10 MCP tools**: get_work, get_source_passage, resolve_ref, search_passages, verify_quote,
  verify_claim_structure, trace_dependency, find_counterevidence, get_work_hub, get_themes.
- **49 published IPVV passages** (source + L2 + C1 + c1_source), lazy-JSON store.
- **`hub.ts`** tracking outputs per source; **`themes.ts`** (deterministic themes); **`lib/verify.ts`**
  (the deterministic floor).
- **The research library**: 22 recognition essays, 3 LOGICAL-ARGUMENT files, the PUSHING method +
  questionnaire DNA.

So the *infrastructure* for auditable arguments is 80% there. What's missing is the **typed argument
object + the derived state-of-play** — and the truth-engine system already solves both.

---

## 1. How the docs apply to the existing systems (the map)

| Existing system | The docs that feed it | The concrete application |
|---|---|---|
| `/api/verify/claim-structure` | `truthreview.md`, `nyaya-truthmap-gate.py` | upgrade to **`/verify/claim-semantic`**: add the Nyāya hetvābhāsa (savyabhicara/viruddha/asiddha/satpratipaksa/badhita) + falsifier-required checks on top of the structural floor |
| `/api/themes` + `themes.ts` | `mlpushing.md`, `QUESTIONNAIRE_REAL_DNA.md` | the themes become the **question-shapes**; a theme = a question-family; discovery = the PUSHING DNA |
| `/api/hub` | `COMPOUNDING_RESEARCH_SYSTEM.md`, `mlpipeline.md` | add `logical_argument` as a first-class kind with the `ArgumentTruthPacket` type (conclusion→premises→passages) |
| `/api/resolve` | `ml-truthmap.md`, `proof_engine/` | the auditable root: every argument premise resolves to a passage → Sanskrit |
| The 22 essays | `mlpipeline.md`, GenProve/TRACER | essays become **provenance-carrying**: each sentence tagged Quotation/Compression/Inference + its argument packet + passages |
| The 3 LOGICAL-ARGUMENT files | `SPEC_ARGUMENT_TRUTH_PACKET.md`, EO-v2 | reformat as typed truth-packets (they already have the Nyāya 5-member shape) |
| The PUSHING sessions | `mlpushing.md`, `patala_ml/pushing.py` | parsed into `PushingRecord`s → seed the argument packets + question-growth |

---

## 2. How to generate logical arguments with auditable roots (the pipeline)

```
1. PUSHING (exists)          a tension + quoted passages   → PushingRecord
2. ARGUMENT (build)          the tension formalized as an ArgumentTruthPacket:
                               conclusion ← premise[0..n] ← each premise's passage_ids
3. RESOLVE (exists)          each passage_id → /api/resolve → the real Sanskrit span
4. VERIFY (exists→extend)    /verify/claim-structure (structural) +
                             /verify/claim-semantic (Nyāya gate: hetvābhāsa, falsifier)
5. STRENGTH (build)          claim-strength DERIVED (not labeled):
                               FORMALLY_VALID_GIVEN_ENCODING (Lean, strict subset, human-reviewed
                                 encoding) · REVIEWED (human) · WELL_SUPPORTED (premises resolve +
                                 no surviving prosecution) · PLAUSIBLE (live objection) ·
                                 SPECULATIVE (probe)
6. STATE-OF-PLAY (build)     graph-derived synthesis (the truthreview acceptance test):
                               which candidates survive criticism, why, with every edge shown
7. ESSAY (build)             provenance-carrying prose: each sentence cites its argument packet
                               → premises → passages (GenProve/TRACER pattern)
```

**The auditable root guarantee:** an essay sentence → (Inference) → argument conclusion → premise →
`passage_id` → `/api/resolve` → Sanskrit. **Nothing is asserted without a resolvable path back to the
source text.**

**The critical design principle (from `truthreview.md` — inherit it):**
> "Make **argument state the primary state**. Runtime state (Bayes) is one evidence view inside the
> argument fabric, not the center."

The Bayesian engine is a **derived scorer**, not the truth. The argument graph + verify floor is the
truth. This is exactly Pāṭala's frozen "AI proposes ≠ Pāṭala asserts."

---

## 3. The visionary use cases (beyond "generate an argument")

### 3a. The epistemic gearbox becomes trustworthy
The depth ladder (GUIDE / C1 / L200+Sanskrit / THEME / ESSAY) + auditable arguments = an AI that
**retrieves by depth** and can *show its reasoning root* at any level. Ask "why is Śiva not just a god?"
→ GUIDE → "show the roots" → C1 → argument packet → Sanskrit. The auditable root is what makes the tutor
*trustworthy*, not just fluent.

### 3b. Provenance-anchored misconception maps
The PUSHING DNA + semantic-distance ladder → a misconception map where each entry ("Śiva = a god")
resolves to **why it fails, with the argument that shows it** (the licensed-vs-not rule from logicdog).
Not a teaching claim — an *auditable* teaching claim.

### 3c. Cross-tradition comparative matrix with typed relations
The comparative spec (question × text → answer-cell) + the truth-engine's `correspondences` table →
a matrix where each cell carries `OVERLAPS / BRIDGES / CONTRADICTS / DIFFERENT`, each backed by argument
packets. "Dharmakīrti vs Abhinavagupta on reflexivity" = a row lookup with a derived verdict.

### 3d. The disagreement-preserving engine
The truth-engine's `critique_pair` (lens→lens, pressure_type) + essay provenance = a system that
**holds live disagreements without flattening them**. The reflexivity debate (Dharmakīrti / Abhinavagupta
/ Ñāṇavīra, three live positions) is the model. This operationalizes the frozen research question:
*"Can models discover relationships experts accept without erasing disagreement?"*

### 3e. Belief-change tracking ("git blame for beliefs")
The truth-engine's `contribution_trace()` + `state_of_play_snapshots` → answer **"what changed after
this source was added / this criticism accepted?"** The essays become living documents whose provenance
can be diffed.

### 3f. The Vertical-Fidelity benchmark (the cross-domain artifact)
The provenance-carrying essays (Quotation/Compression/Inference) + the corruption set (NEGATION_LOSS,
SCOPE_STRENGTHENING, CERTAINTY_INFLATION, ATTRIBUTION_ERROR, BOUNDARY_ERASURE, AGENT_SWAP) → the
**Vertical Fidelity Benchmark for Multi-Resolution Scholarly Explanation** — the artifact that matters
outside Sanskrit studies.

### 3g. The computable scholarly tradition (the end-state)
All of the above = a corpus that **explains itself**: every claim resolves to source, every essay is a
derived projection over the argument graph, every disagreement is tracked, every simplification is
verifiable. Not a translation site — a **computable scholarly tradition** (the vision).

---

## 4. What to build (the honest, ordered queue)

| # | Build | Depends on | Effort |
|---|---|---|---|
| **1** | **`ArgumentProposal` type + parser** (AIF-informed; from the 3 LOGICAL-ARGUMENT files + C1s, pointing downward to Sanskrit) | nothing (my lane) | medium (NOT low — see `ML-ARGUMENT-REVIEW-CORRECTED.md`) |
| **2** | **`/verify/claim-semantic`** (Nyāya gate over the structural floor) | the `proof_engine` gate logic (exists) | low-medium |
| **3** | **Derived claim-strength scorer** (port the Bayesian propagation as the scorer) | #1 | low (code exists) |
| **4** | **Graph-derived state-of-play** (the truthreview acceptance test) | #1 | medium |
| **5** | **Provenance-carrying essay generation** (GenProve/TRACER pattern) | #4 | medium (frontier) |
| **6** | **Lean link** (strict subset, `FORMALLY_VALID_GIVEN_ENCODING`) | #2 | medium (optional) |

**#1 is the unlock.** It turns the 3 existing LOGICAL-ARGUMENT files + the C1s into typed, resolvable
argument objects — and everything downstream (strength, state-of-play, essays, comparative, vertical
fidelity) hangs off it.

---

## 5. The one-sentence summary

All our docs apply to Pāṭala's existing systems as **the missing argument layer**: the truth-engine gives
us the auditable-argument machinery (Nyāya gate, Bayesian scorer, proof engine, state-of-play design);
the PUSHING DNA gives us the question-generation; the provenance papers give us the essay mechanism. The
build is a **port + unify**, not a from-scratch: type the argument, resolve its roots, gate it, derive
its strength, derive its state-of-play, and generate provenance-carrying essays — turning Pāṭala into the
computable scholarly tradition the vision describes, where every claim resolves to Sanskrit and every
essay is a verified projection of the argument graph.

---

## 6. The role of the ML venv/models (vs the truth engine) — honest

There was a question about what the venv/models are *for* and how they relate to the truth engine. The
answer is that they do **different jobs** and connect at exactly one stage:

| | ML venv (retrieval) | Truth engine (arguments) |
|---|---|---|
| Job | **find** the relevant passages | **verify & grade** the claims built from those passages |
| Question | "which passage answers this query?" | "does this claim survive criticism, at what strength?" |
| Output | ranked passages | PROVED / WELL_SUPPORTED / PLAUSIBLE / HOLLOW + derived state-of-play |
| Tool | BM25 / dense embeddings | Nyāya gate · Bayesian scorer · Lean proof engine |

**The single connection:**
```
ML retrieval (find passages)  →  become the PREMISES of an argument  →  truth engine gates + grades
```
The ML venv feeds the *premise→passage* step; the truth engine does the *argument→strength→essay* step.

**The honest value ranking (be clear about this):**
1. **The corpus** (49 passages + C1s, verified, resolvable) — the real asset
2. **The verify floor** (deterministic checks — no ML)
3. **The truth-engine machinery** (Nyāya gate, Bayesian scorer, Lean bridge, state-of-play design — built)
4. **The auditable-argument design** (the `truthreview` acceptance test)
5. **The ML venv/models** — the *least* valuable; only establishes baselines. Reproducible + deletable
   via `research/requirements.txt` (rebuilt CPU-only at 1.4G, down from 5.1G of GPU waste).

So: don't protect the venv. It's a probe, not the product.

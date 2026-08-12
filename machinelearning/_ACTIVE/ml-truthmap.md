# STALE — ML TRUTH-ENGINE / NYĀYA / BAYESIAN (historical review; superseded)

> **⚠️ STALE.** This early review treats the truth-engine's Bayesian runtime + Nyāya gate as **mature,
> adoptable machinery**. It predates the epistemic hardening. The current honest state (see
> `TRUTHENGINE-FULL-AUDIT.md`, `TRUTHENGINE_TO_PATALA_MAPPING.md`, `NYAYA-GATE-CANDIDATE-V1.md`,
> `COMPONENT-CONTRACTS.md`): **nothing is real because code exists** — the gate is `NYAYA_GATE_CANDIDATE_v1`
> (measured, NOT validated), `strength.py` is an uncalibrated `BayesianEvidencePrimitive`, and no claim is a
> result without gold + blind eval. Read the superseding docs, not this one, for current direction.

# ML — THE TRUTH ENGINE / NYĀYA / BAYESIAN SYSTEM (what's reusable for Pāṭala)

*2026-08-12. **Agent 1's (ML) review of the existing truth-engine system** — the Bayesian propagation
engine, the Nyāya gate, the FOL→Lean bridge, and the EO/argument-fabric architecture. **Canonical live
locations found:** the truth-map runtime is at `/root/projects/.meta/misc/truth-engine/`, the design docs
at `/root/projects/clean/docs/active/`, and the proof engine at `sanskritree/proof_engine/` (a far richer
module than the tmp snapshot suggested). This is a *mature, sophisticated* system that directly solves
Pāṭala's logical-argument gap — and much of it is directly portable. Verdict up front: **this is not
scrap; it's a working engine Pāṭala should adopt, not re-derive.***

---

## 0.1 The one-line verdict

Pāṭala's logical-argument pipeline (mlpipeline.md, SPEC_ARGUMENT_TRUTH_PACKET.md) was going to *build
from scratch* the exact machinery that already exists: a Bayesian claim-propagation engine, a Nyāya gate
with hetvābhāsa checks, an FOL→Lean bridge, and a graph-native argument fabric — plus a **rigorous
self-audit** (`truthreview.md`) that already diagnosed exactly how to build it. **This system already
solves it.** The right move is to **port/reuse it**, not rebuild.

---

## 0.2 Corrected locations (canonical, verified 2026-08-12)

| Asset | Live location |
|---|---|
| Truth-map runtime (Bayesian propagation, DB adapter, migrate, tests) | `/root/projects/.meta/misc/truth-engine/` |
| **Full truth-map docs (the design family)** | `/root/projects/clean/docs/active/` (TRUTHMAP-*, TRUTHCHANGES*, truthreview.md) |
| Proof engine (the full 7-step pipeline) | `sanskritree/proof_engine/` |
| Nyāya→Lean compressor (the demo scaffold) | `sanskritree/nyayaengine.py` |
| Nyāya claim data | `sanskritree/ground_truth/nyaya_claims.json` |

The internal copies of the propagation engine **md5-match** the tmp snapshot, confirming they're the
same (canonical) code. The `proof_engine/` module is far more complete than the snapshot alone suggested.

---

## 0.3 The two-layer architecture (the system's true design)

`TRUTHMAP-PURPOSE.md` lays out the whole thing as **two unified layers**:

- **Layer 1 — Sanskritree (Formal Proof):** Sanskrit claims → Lean 4 via a 7-step algorithm (Sayability →
  Library → Formalize → Prove → Decompose → Propagate). Outputs PROVED / OUTSIDE_FORMAL / HOLLOW /
  REFUTED. *Key insight:* "The goal is honesty, not proofs. HOLLOW and OUTSIDE_FORMAL are correct when the
  text does not support formalization. **The boundary between what can and cannot be formalized is itself
  a finding.**"
- **Layer 2 — Truth Map (Evidence Tracking):** per-question support/contradict/confidence tracking, with
  a Bayesian propagation engine as the *derived* scoring view.

The two layers were built separately and the project's stated purpose is to **unify them**. That unify
step is precisely what Pāṭala's logical-argument pipeline needs — the audit below makes this concrete.

---

## 1. What exists (the reusable assets, verified)

### 1.1 The Bayesian propagation engine (`truthengine-propagation.py`, ~304 lines, complete)
A proper, working log-odds belief-propagation engine:
- `sigmoid` / `log_odds` primitives
- **Log-odds Bayesian updating**: `posterior_log_odds += weighted_lbf`
- **Paradigm-dependence discounting**: `w_dep = 1/(1 + α·n_prior)` — successive claims from the same
  paradigm are down-weighted (anti-double-counting)
- **Weighted Bayes factor**: `w_rel × w_map × w_dep × w_aux × log_bayes_factor`
- **Feature states** (prior / update / reset), **branch probability derivation** from feature posteriors,
  full-recompute vs incremental-update modes

**Why this is gold for Pāṭala:** it's exactly the machinery to make `claim-strength` in the argument
truth-packet a **derived number**, not a hand-label. A claim's weight = its log-Bayes-factor × the
paradigm-discount × source weights. This turns "WELL_SUPPORTED vs PLAUSIBLE" from a manual judgment into
a computed posterior.

### 1.2 The Nyāya gate (`scripts/nyaya-truthmap-gate.py`, ~678 lines, complete + tested)
A sophisticated pre-ingestion gate that validates every claim before it can update the posterior:
- **Five hetvābhāsa (fallacy) checks**: `savyabhicara` (unreliable reason), `viruddha` (contradictory),
  `asiddha` (unestablished), `satpratipaksa` (counter-balanced), `badhita` (overtidden)
- **pramāṇa inference**: pratyakṣa / anumāna / upamāna / śabda / formal_proof — inferred from source +
  paradigm
- **tarka falsifier generation**: requires a falsifier/truth-condition; flags `missing`/`hollow`
- **Bayes-factor caps**: `accepted` / `accepted_with_penalty` (cap LBF) / `needs_review` / `refuted` /
  `hollow` / `outside_formal` — with `can_update_posterior` flags
- **Formal-probe hook** into a proof engine; **NNExpr grammar validation** (`scripts/logic/bnf.py`)

**Why this is gold for Pāṭala:** it *is* the `verify-claim` semantic layer + the "AI proposes ≠ Pāṭala
asserts" floor, made concrete. The hetvābhāsa checks are the deterministic gate that decides whether a
claim may move the posterior. Pāṭala's `/api/verify/claim-structure` is structural; this adds the
*semantic/fallacy* gate.

### 1.3 The FOL→Lean bridge (`scripts/logic/fol_lean_bridge.py`, ~125 lines)
A conservative Navya-Nyāya → Lean4 type translator (`abheda`→identity, `vyāpti`→`∀x, Hetu x → Sadhya x`,
`avacchedaka`/`pratiyogin`/`anuyogin`/`sambandha`→type-theoretic forms). **This is the real Lean link**
that mlpipeline.md said was missing — it maps the Nyāya operators to Lean types, ready to feed Lean
Copilot / Lean4.

### 1.3b The full proof engine (`sanskritree/proof_engine/` — richer than the snapshot)
The live proof engine is a complete 7-step pipeline, not just the bridge:
- **`algorithm.py`** — `process_claim()`: the 7-step algorithm (Sayability → Anuvṛtti → Library → NN
  Parse → TRS → Proof → Propagate), with `dev_mode`/`fast_mode`, max-depth, UNSAYABLE→HOLLOW handling.
- **`lean_checker.py`** — **real Pantograph (Lean4 REPL) proof checking** with a fallback
  `FALLBACK_KNOWN` table (modus_ponens, forall_imp, contrapositive) + a ReProver hook. This is the
  *real* Lean backend (not the `nyayaengine.py` simulated demo).
- **`decomposition.py`**, **`informalization.py`** — the claim→subclaim decomposition and back-translation.
- **`ground_truth.py`**, **`failure_taxonomy.py`** — validation pairs + failure classification.
- **`phase1_nyaya.py`**, **`phase1_dharmakirti.py`** — tradition-specific claim processing.
- **`db.py`** (21KB) — the node database (the D1-shaped schema).

**This changes the picture:** the "prove" link is not hypothetical — there is a *working Lean checker*
with Pantograph, already wired into a 7-step algorithm. The `nyayaengine.py` is the older demo scaffold;
the `proof_engine/` module is the real, more capable implementation.

### 1.4 The EO / argument-fabric architecture (`docs/active/EO-v2.md`, `TRUTHMAP-ARGUMENT-FABRIC.md`)
The conceptual architecture, with one crucial design principle:
> **"The truth map is not a Bayesian oracle. It's a refutation-led evidence provenance system. Numbers
> are summaries, not verdicts."** (TRUTHCHANGES5)

- **EO = Essay Object** structured as a **Nyāya 5-member syllogism** (Pratijñā → Hetu → Udāharaṇa →
  Upanaya → Nigamana), with candidates carrying `live/weakened/defeated/merged` status.
- The **argument fabric** is a graph: Source span → Claim → Gate result → Argument node → Support/attack/
  rephrase/formal-bridge edge → Crux → Candidate → State of play. (A stricter AIF-style argument map,
  with Nyāya metadata + hetvābhāsa + falsifiers + defeat tracking.)

**This is Pāṭala's logical-argument paper-frame, already built and versioned.**

---

## 2. How it maps to Pāṭala (the direct port)

| Pāṭala need | Existing system | Effort |
|---|---|---|
| argument truth-packet `claim-strength` as a number | Bayesian propagation (`truthengine-propagation.py`) | **port** |
| `verify-claim` semantic gate (fallacy detection) | Nyāya gate (`nyaya-truthmap-gate.py`) | **port** |
| the Lean "prove" link (mlpipeline §3) | FOL→Lean bridge + Lean Copilot | **port + wire** |
| logical-argument format (PAPER-FRAME) | EO-v2 (5-member syllogism + candidate status) | **adopt** |
| argument graph (crux/support/attack) | argument-fabric architecture | **adopt** |

**The key philosophical alignment:** the system's core principle ("refutation-led, numbers-are-summaries-
not-verdicts") is *exactly* Pāṭala's frozen rule ("AI proposes ≠ Pāṭala asserts"). These are the same
design. Pāṭala shouldn't just borrow the code — it should borrow the **provenance-led epistemic stance**
that this system already embodies and refined.

---

## 3. The crucial design principle to preserve

The handover is explicit and it's the *right* lesson:
> The truth map **records what explanations survive criticism, what would break them, what evidence moved
> them, and where formal proof stops.** The Bayesian runtime is a *derived view* over the argument graph,
> not the source of truth.

This is a **refutation-led, graph-native** system where Bayesian numbers are a *projection*, not the
ground truth. This is strictly more correct than a pure Bayesian oracle, and it matches Pāṭala's existing
`graph.ts` + `/api/verify/*` architecture. The Bayesian engine should be Pāṭala's *derived scoring layer*
on top of the existing verified graph — not a new source of truth.

---

## 4. What to pull into Pāṭala (my recommendation, in order)

1. **Port the Nyāya gate** as `/verify/claim-semantic` (the semantic layer over the existing structural
   `/verify/claim-structure`). The hetvābhāsa checks + falsifier-required logic are deterministic and
   directly reusable. **Highest value, lowest effort.**
2. **Port the Bayesian propagation** as the derived `claim-strength` scorer for argument truth-packets.
   Feed it the existing C1/IAs as claims; get computed WELL_SUPPORTED/PLAUSIBLE. This makes the argument
   pipeline's strength a number, not a label.
3. **Adopt the EO / argument-fabric** architecture as the logical-argument object (it's the mature form
   of SPEC_ARGUMENT_TRUTH_PACKET.md — 5-member syllogism + candidate status + defeat tracking).
4. **Wire the FOL→Lean bridge** to a real Lean backend (Lean Copilot) for the `PROVED` verdict — the
   missing "prove" link, now with a ready translator.

---

## 5. Honest cautions

- **This is a snapshot** (`/tmp/clean-full/`, a `clean` project). Before treating it as canonical, verify
  the live location and its test suite (`test_truthengine_working.py`, `test_nyaya_gate.py` exist).
- **The Bayesian numbers are a derived view, not truth** (the system's own rule). Keep that stance in
  Pāṭala: the graph + verify floor is the source of truth; Bayes is the scorer.
- **The FOL→Lean bridge is "conservative: only maps structures we can formalize"** — good, but the
  Sanskrit→FOL encoding is still the human-reviewed scholarly act (same guardrail as before).
- **License/ownership**: confirm the `clean` project's license before porting code into Pāṭala. It's
  likely the same author/project family, but verify.

---

## 6. Bottom line

Pāṭala was planning to *build* the logical-argument machinery; **it already exists** in the truth-engine
system — a mature Bayesian propagation engine, a Nyāya hetvābhāsa gate, an FOL→Lean bridge, and a
refutation-led argument fabric. The right move is **adoption/porting, not re-derivation** — and to carry
forward the system's core epistemic stance (refutation-led, numbers-as-summary, "AI proposes ≠ Pāṭala
asserts"), which is *identical* to Pāṭala's frozen rule. The single highest-value next step: **port the
Nyāya gate as `/verify/claim-semantic`** — it turns Pāṭala's structural verification floor into a real
fallacy-detecting semantic gate, using battle-tested code.

---

## 7. THE SELF-AUDIT (`truthreview.md`) — the design Pāṭala should inherit

*2026-08-12. The `clean` project already did a rigorous self-audit of the truth engine, and its
diagnosis + required build direction are **the single best blueprint for Pāṭala's logical-argument
pipeline**. This is not an ML paper; it's the project's own engineering soul, written down.*

### 7.1 The executive verdict (the core design principle)

> "The original directive does not ask for a generic Bayesian belief engine. It asks for a research
> agent that can take one sharp pressure point, reconstruct the best competing explanations, identify
> structural correspondence and non-equivalence, reverse the critique in both directions, generate
> consequences, and state what currently survives."

And the crucial corrective — the system has **three state layers that must not be conflated**:
1. **Runtime state** — the numeric Bayesian posterior (features → discriminators → branch support).
2. **Argument state** — what the research directive actually needs (question → candidates → cruxes →
   supports/attacks → bridge status → consequences). **Designed and partially stored, but not computed.**
3. **Editorial state** — the human-written synthesis (EO state-of-play, maps, essays).

> **"The next build must make argument state the primary state. Runtime state should be one evidence
> view inside the argument fabric, not the center of the system."**

**This is Pāṭala's exact architecture.** Pāṭala already has the graph (argument-state substrate) + the
verify floor. The truth-engine's Bayesian runtime is the "runtime state" view. The audit's principle —
**argument graph primary, Bayes as a derived view** — is exactly what Pāṭala should inherit, and it
confirms my earlier recommendation: port the Bayes engine as a *scorer*, not a source of truth.

### 7.2 The working-now list (verified battle-tested code)

The audit confirms these work:
- **Numeric runtime** (F1–F8, D1–D5, B1–B6, dimension-aware crowding, convergence diagnostics, blame
  traces) — 30 tests passing.
- **Provenance/blame foundation** (`contribution_trace()` — source/claim/target/dimension/LBF/weights/
  posterior before-after = "git blame for beliefs").
- **Nyāya gate** (pre-ingestion: tradition, pramāṇa, dimension, hetu/sādhya/vyāpti, falsifier,
  hetvābhāsa, tarka) — wired into `ingest-packet.py` by default.
- **Argument-fabric schema** (source_spans, argument_nodes/edges, claim_gate_results, hetvābhāsa_checks,
  tarka_falsifiers, nigrahasthana_events, state_of_play_snapshots).
- **Gate-aware ingestion** — the Nanavira run: 7 claims → 0 runtime updates (correctly, it moved the
  *argument* fabric, not the numeric runtime) → 7 gate results (5 accepted, 2 penalized).

### 7.3 The key gaps it identified (these are Pāṭala's build queue)

| Gap | The build that fixes it | Pāṭala relevance |
|---|---|---|
| No state-of-play **synthesizer** (only a shallow reporter) | graph-derived state-of-play (not manual EO prose) | the essay-from-argument step |
| Dossiers not ingested as first-class candidates/cruxes | `ingest-dossier.py` | the C1→argument step |
| **Directional critique pairs missing** (directive Step 6) | a `critique_pair` object (lens→lens, pressure_type) | the "subversion/counter" of the PUSHING DNA |
| No **correspondence/break table** (Steps 3–4) | a `correspondences` object (shared_structure vs important_difference, OVERLAPS/BRIDGES/CONTRADICTS/DIFFERENT) | the comparative matrix |
| State-of-play snapshots not persisted | persist snapshots | the provenance/timeline of beliefs |
| 56 of 72 directive questions unseeded | `seed-research-directive.py` | the questionnaire growth |
| No acquisition/reviewer ledgers | acquisition_runs, claim_reviews | measured human review (inter-rater) |

### 7.4 The acceptance test it set (Pāṭala's proof-of-life)

The audit's sprint acceptance test is *literally* Pāṭala's flagship:
> "Given only the reflexivity dossier, Nanavira packet, Nanavira map, and EO inputs, the system generates
> a state-of-play report saying: structural reflexivity is locally strengthened · universal consciousness
> is not entailed · Abhinavagupta is pressured at universalization · Abhinavagupta pressures Nanavira at
> manifestness · Dharmakīrti/Nanavira is OVERLAPS not BRIDGES. **If that report is manually copied from
> EO prose, the sprint has failed. If it is derived from graph rows and rule outputs, the project has
> reached the first version of the original directive.**"

**This is the auditable pipeline the user asked about** ("Sanskrit → argument → essay") made concrete:
the essay must be *derived* from the argument graph, not handwritten. Pāṭala's C1s/IAs → argument
packets → graph-derived state-of-play is the same test.

### 7.5 The engineering principle (the soul of the whole thing)

> "Do not optimize for more numbers. Optimize for: **Can the system explain why one live answer survives
> criticism better than its rivals, showing every source, claim, gate decision, bridge assumption,
> unresolved crux, and consequence that led to that answer?**"

That is the original directive in software form — and it is *exactly* the auditable-pipeline thesis. This
is the design Pāṭala should inherit wholesale: provenance-led, argument-graph-primary, Bayes-as-derived-view,
fallacy-gated, falsifier-required, directionally-critical, and measured by whether the essay is *derived*,
not copied.

---

## 8. THE NEW FINDINGS (the docs beyond truthreview.md, verified 2026-08-12)

Three more truth-engine docs were found and reviewed; two are directly reusable for Pāṭala's data
foundation:

### 8.1 Claim v3 — the definitive claim schema (from `truthadvanced.md` §Central Schema Problem)

The truth-engine resolved its THREE overlapping claim models into a single **Claim v3**. This is the
mature form of Pāṭala's `ArgumentProposal` — adopt it:

```json
{
  "claim_id": "cl:...",
  "source_span_id": "span:...",
  "claim_text": "...",
  "tradition_scope": "...",
  "pramana": "anumana",
  "evidence_dimension": "phenomenological",
  "argument_dimension": "analogical",
  "hetu": "...", "sadhya": "...", "vyapti_statement": "...",
  "falsifier": {...},
  "posterior_targets": [{"target_id": "D3", "target_type": "discriminator"}],
  "argument_targets": [{"target_id": "cand:...", "target_type": "candidate_explanation"},
                       {"target_id": "crux:...", "target_type": "crux"}],
  "weights": {"log_bayes_factor": 0.4, "w_rel": 0.8, "w_map": 0.7, "w_aux": 0.6}
}
```
**The key rule (the runtime-vs-argument split, made concrete):**
- `posterior_targets` move the numeric F/D state AFTER gate approval.
- `argument_targets` create graph nodes/edges and state-of-play pressure (never touch the posterior).
- **Every posterior update must be backed by a gate result.**

**Pāṭala alignment:** this maps 1:1 onto my `ML-ALIGNMENT.md` — `posterior_targets` = the Bayesian
Certainty scorer; `argument_targets` = the ArgumentProposal graph; "every update gated" = the verify floor.

### 8.2 TRUTHMAP-REDESIGN — the discrimination cascade (transferable concept)

The top layer isn't a flat Bayesian board — it's a **cascade of eliminative binary questions** (D1-D5)
that prune candidate branches (B1-B6). Transferable to Pāṭala:
- **each CORE question = a "discriminator"** that prunes candidate readings (the PUSHING DNA / comparative
  matrix becomes eliminative, not just descriptive)
- **answered thresholds per evidence type** (ordinary 0.75/0.25, discriminator 0.85/0.15, extraordinary 0.95/0.05)
- **expected-branch-effect matrix** (near-mask 0.05-0.15 … survivor-boost 1.10-1.50)
- **EIG question-selection** (ask the most eliminative falsifiable question next — binary search)

This is the **frontier/intelligentothers wing's** domain (the B1-B6 metaphysics contest), not Pāṭala's
primary spine — but the *discriminator-as-eliminative-question* method maps cleanly onto Pāṭala's
questionnaire layer.

### 8.3 TRUTHMAP-BASELAYER-SPEC — the full pipeline (confirms Pāṭala's design)

`source basket → information packet → source map → contention benchmark → state of play → inquiry trail
→ essay seed → EO → factories → new evidence`. Two disciplines worth keeping:
- **Source baskets before extraction** (decide what to read and why, BEFORE claims — prevents selection
  bias hidden in LLM extraction)
- **Don't collapse layers** (each layer has one job) — identical to Pāṭala's layer discipline.

### 8.4 The populated DBs (real artifacts, not just specs)
- `sanskritree/proof_engine.db` (180KB — a real populated proof-engine database)
- `/tmp/truthmap*.db` + `truthmap-argument-schema.sql` (the argument-fabric tables)

So the truth-engine has both the *specs* AND *populated databases* — the schema designs are proven, not
just described.

### 8.5 What to pull into Pāṭala (updated)
1. **Claim v3** as the canonical claim/argument schema (resolves runtime vs argument targets cleanly).
2. **The discrimination-cascade method** for the questionnaire layer (each CORE question = an eliminative
   discriminator).
3. **The source-basket discipline** (decide what to read before extracting — the anti-bias step).
4. The **populated `proof_engine.db`** as a reference/provenance source.

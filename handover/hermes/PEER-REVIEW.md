# PEER REVIEW — the executable-corrections system (spec)

*2026-08-12. The peer-review design that turns Pāṭala from an "AI peer-review tool" into a **scholarly
operating system**: a scholar's judgment is not prose — it is a **graph mutation with provenance** that
recomputes downstream arguments, cruxes, themes, and syntheses. This spec grounds Phases 3–5 of
`DEV-PLAN.md` in the real primitives that already exist (`data/corpus/primitives.ts` ReviewEvent +
`graph.ts` supersedes + the SINGLE_REVIEWED→DOUBLE_REVIEWED→ADJUDICATED ladder).*

---

## 1. THE CORE CLAIM

> **Normal review = prose ("I don't think this works"). Pāṭala review = a graph mutation with provenance.**

A review is a first-class object that *changes the epistemic state of the target* and *ripples through the
dependency graph*. It is never just commentary.

```
REVIEW → graph recomputes → argument state changes → crux changes
      → paper synthesis changes → future agents inherit the correction
```

That is the bridge from peer-review tool to scholarly operating system.

---

## 2. THE REVIEW OBJECT (grounded in the existing ReviewEvent)

The primitive already exists (`data/corpus/primitives.ts`). Extend it for the graph-mutation use case:

```ts
interface ReviewEvent {
  id: string;                    // pt:review:<target>:<scope>:<n>
  target: string;                // any object id (proposition, inference, argument, translation, alignment, crux...)
  scope: ReviewScope;            // the existing enum + add: "proposition" | "inference" | "argument" | "alignment" | "crux"
  reviewer: { kind: "human"|"machine"|"scholar"; id: string };   // reviewer identity matters (correction #1)
  decision: "accept" | "reject" | "revise" | "needs_specialist" | "abstain";
  reason?: string;
  replacement_ref?: string;      // NEW: the object that supersedes this one (e.g. rule W14 → W19)
  evidence_refs?: string[];      // source spans / passages backing the judgment
  object_version: string;        // NEW: the immutable version of the target being reviewed
  state_ladder: "CANDIDATE"|"SINGLE_REVIEWED"|"DOUBLE_REVIEWED"|"ADJUDICATED"|"SPECIALIST_REVIEWED";
  created_at: string;
  created_by: string;
  supersedes?: string;           // if this review reverses a prior one
}
```

**Invariants:**
- A review is **immutable** once recorded. A later review `supersedes` it (correction #3: preserve history, don't rollback).
- `reviewer` identity + `scope` + `object_version` are required — you cannot review the wrong version.
- `decision=abstain` is valid and valuable (the abstention principle).

---

## 3. THE STATE MACHINE (the honest ladder — already the contract)

```
CANDIDATE ──(review 1 accept)──► SINGLE_REVIEWED ──(review 2 accept)──► DOUBLE_REVIEWED ──► ADJUDICATED
   │                                 │                                       │
   └──(review 1 reject/revise)──► revised/rejected ──(replacement)──► a new CANDIDATE
```

- **No machine output self-promotes.** Promotion (to `editorially_accepted`) is a scoped human policy action.
- `MACHINE_PROPOSED` → `CANDIDATE` requires at least the machine's own review-ready state; → `ACCEPTED` requires human adjudication.
- The ladder is per-`scope`: a translation review and an argument review are different ladders for the same target.

---

## 4. THE REVIEW PIPELINE (from REVIEW_PROTOCOL.md — already defined)

```
T0 machine draft (disposable)
T1 evidence-bearing working translation  → eligible_for_review
R1 human editorial pass                  → T2 (human-corrected scholarly working translation)
R2 specialist / domain review            → T3 (stable scholarly release)
C1 commentary / public explanation (may overturn)
```
Applied to *objects* (proposition/inference/alignment/crux), not just translations:
```
MACHINE_PROPOSED → CANDIDATE → SINGLE_REVIEWED → DOUBLE_REVIEWED → ADJUDICATED → editorially_accepted
```

---

## 5. THE GRAPH-MUTATION LOOP (the executable correction — the moat)

When a review changes a target's state, Pāṭala recomputes the dependency graph:

```
ReviewEvent: target=INF-182 · decision=REJECT · reason="premise P71 doesn't support rule W14"
             · replacement_ref=W19 · evidence_refs=[SourceSpan...]
        │
        ▼  [Pāṭala dependency engine — NOT a Hermes convention]
  compute downstream impact:
     - which arguments used INF-182?
     - which cruxes depend on it?
     - which themes/thesis candidates reference it?
     - which syntheses / paper drafts would change?
        │
        ▼
  emit an IMPACT REPORT (the "review dossier")
  + mark downstream objects affected/stale
  + future agents inherit the correction (recompute their outputs)
```

**The critical rule (correction #4):** Hermes hooks *trigger* this recomputation; **Pāṭala's dependency engine
determines** what changed. Hermes wakes it; Pāṭala decides.

---

## 6. THE SCHOLAR WORKBENCH (the primary surface — scholars never see Hermes)

A scholar reviewing ARG-002 sees:
```
REVIEW TASK
  ARG-002 · question: does V2-L license this reconstruction?
  exact Sanskrit · source/literal layer · translation · C1
  proposed propositions · proposed warrant · competing reconstruction · machine critique
  IMPACT: this judgment affects 2 arguments · 1 theme · 4 downstream claims
```
Actions: `ACCEPT / REVISE / REJECT / ABSTAIN / PROPOSE ALTERNATIVE / COMMENT`.
Submission → an immutable ReviewEvent → Hermes wakes Agent 1 to recompute. **Nothing agentic is visible.**

**The AI copilot inside the workbench:** a constrained patala profile that queries the MCP, compares
readings, launches blind critics, constructs alternatives — but **cannot accept/reject/promote**. The
scholar signs the judgment.

---

## 7. MACHINE PRE-REVIEW (peer review restructured, not replaced)

Before a human sees it, Pāṭala runs the machine pre-review pipeline:
```
DOCUMENT → claim extraction → citation resolution → corpus retrieval → argument extraction
        → terminology audit → counterevidence search → alternative reconstruction
        → source-grounding audit → Reviewer-2 attack → impact/crux analysis
```
Result (the "review dossier"):
```
17 claims extracted
  11 strongly grounded · 3 require qualification · 2 unsupported · 1 underdetermined
LOAD-BEARING ISSUE: claim C7 depends on treating vimarśa in V2L/V2O as SAME_SENSE.
If C7 rejected: 4 downstream conclusions weaken.
```
Then the human is asked only the high-value questions ("these two readings differ solely on whether X
scopes over Y — which is defensible?"). **Expert attention compression.**

---

## 8. THE REVIEW API (Phases 3–4 — the write boundary)

```
POST /api/objects/{id}/review
  { decision, reason, replacement_ref?, evidence_refs?, reviewer_id, scope, object_version }
  → creates immutable ReviewEvent
  → if reject/revise: marks target superseded + computes downstream impact
  → returns { review, impact_report, downstream_affected }

GET /api/review/{target}          → the review history + current state ladder
GET /api/review/queue             → the graph-aware review queue (ranked by impact/uncertainty/centrality)
POST /api/review/{id}/adjudicate  → scoped human promotion under policy
```

**The tool boundary (correction #2):** agents can only `patala_propose_review` / `patala_record_review`.
There is **no `patala_accept_claim` tool**. Promotion is a scoped policy action, not an agent tool.

---

## 9. THE INTEROPERABILITY STACK — integration-heavy, invention-light (the key strategic finding)

**The core principle (from the peer-review research):** Pāṭala's endgame is **integration-heavy,
invention-light**. There is an unusually rich open scholarly-infrastructure ecosystem. **Pāṭala's novel
layer is the fine-grained epistemic graph** (source spans → interpretations → claims → arguments →
reviews → cruxes) — NOT generic manuscript submission, reviewer assignment, annotation, researcher
identity, DOI plumbing, or publishing workflow. Those exist; interoperate with them.

### What Pāṭala must NOT rebuild (it exists)
```
❌ generic journal submission system        → OpenReview / Kotahi / Janeway / OJS
❌ reviewer identity / assignment framework → OpenReview
❌ browser annotation protocol              → Hypothesis
❌ researcher profiles                      → ORCID
❌ organization registry                    → ROR
❌ DOI infrastructure                       → Crossref / DataCite
❌ global citation graph                    → OpenAlex / OpenCitations
❌ peer-review-process metadata standard    → DocMaps / PReF
❌ repository event protocol                → COAR Notify
❌ XML scholarly publishing format          → JATS
❌ generic agent runtime                    → Hermes
```

### The Pāṭala interoperability target stack (adopt, don't reimplement)
```text
EXECUTION                    Hermes
HUMAN REVIEW WORKFLOW REF    OpenReview (conceptual/API reference); Kotahi later if Pāṭala runs its own venue
DOCUMENT ANNOTATION          Hypothesis
REVIEW PROCESS INTERCHANGE   DocMaps + PReF      (crosswalk: Pāṭala ReviewEvent ↔ DocMap process/event)
EXTERNAL EVENT INTEROP       COAR Notify
PEOPLE                       ORCID               (Pāṭala Contributor ID ↔ ORCID)
ORGANIZATIONS                ROR
PUBLIC REVIEW / ARTICLE PIDs Crossref            (peer reviews as first-class records, isReviewOf)
OTHER RESEARCH OUTPUT PIDs   DataCite
GLOBAL SCHOLARLY GRAPH       OpenAlex + OpenCitations
ARTICLE EXPORT               JATS
AGENT ACCESS                 Pāṭala API + MCP (A2A later)
```

### The key crosswalks (interoperate, don't blindly adopt ontologies)
```
Pāṭala ReviewEvent  ↔  DocMap process/event representation
Pāṭala Contributor ID ↔ ORCID   (→ "I reviewed 63 Pratyabhijñā propositions for Pāṭala" becomes recognized service)
Pāṭala ReviewEvent  →  public review artifact → DOI → Crossref isReviewOf → ORCID reviewer credit
Pāṭala = microscopic graph  vs  OpenAlex = macroscopic (paper→cites→paper): Pāṭala does
   claim → interpretation → Sanskrit span → argument → rebuttal → review
```

### The external-event distinction (do not confuse internal runtime with external protocol)
```
Hermes hooks     = Pāṭala's INTERNAL runtime triggers
COAR Notify      = Pāṭala's EXTERNAL scholarly-system event protocol
```
A repository asks Pāṭala for evaluation → Pāṭala returns review/endorsement → the external repo receives
the resulting event. Hermes hooks fire inside; COAR Notify broadcasts outside.

### The coolest endgame integration (the scholar's journey)
```
ARTICLE (written elsewhere)
  → Pāṭala MCP/API
  → Hermes Pāṭala Review
  → machine pre-review (claims/sources/arguments/cruxes)
  → remaining expert questions
  → OpenReview/Kotahi-like review workflow
  → ORCID-authenticated scholars
  → Pāṭala ReviewEvents
  → public review artifact
  → Crossref DOI
  → review credit → ORCID
  → DocMaps describes process
  → COAR Notify broadcasts event
  → Sciety-like aggregators / external agents consume it
```
**Nearly the whole outer institutional shell already exists.** Pāṭala's invention is what happens in the
**middle**: instead of peer review being a blob of prose attached to a PDF, the evaluation resolves down
to exact claims, arguments, readings, and source spans, and propagates consequences through the scholarly
graph. **Keep almost all original engineering effort there.**

### The peer-review community precedents to learn from
PREreview (community preprint review, REST API) · Sciety (many groups, different assessments over the same
objects) · Review Commons (evaluation as a portable object, not property of one journal) · PeerRef
(signed portable reviews) · PubPeer (post-publication correction, publication ≠ epistemic finality) ·
ScienceOpen (public post-publication review with DOIs) · F1000Research (publish-first, visible reviewer
identities). These should shape Pāṭala Review more than traditional anonymous PDF-review workflows.

---

## 10. BYOA + THE CORRECTIONS DATASET (Phase 5 — the moat, external)

**Bring Your Own Agent:** `mcp.patala.org` with OAuth scopes:
`corpus:read · bibliography:read · review:read · proposal:write · review:submit`.
External agents (Claude/ChatGPT/their own) resolve Pāṭala IDs + propose/record reviews without Pāṭala
running their model.

**The executable-corrections dataset** (from Hermes trajectories + ReviewEvents):
```
source → machine reconstruction → tools → alternatives → criticism → revision → review → human correction → final object
```
10,000 passages of *how difficult Sanskrit/philosophical judgments get corrected* = training/eval data for
translation, extraction, alignment, uncertainty calibration, review prioritization. **This is the moat.**

---

## 11. THE GUARDRAILS (from the corrected thesis)

1. Reviews are **immutable**; supersession preserves history, never erases it (≠ Hermes checkpoints).
2. No agent tool can **accept/promote**; only PROPOSE/RECORD; promotion is scoped human policy.
3. Reviewer **identity + scope + version** are mandatory (no reviewing the wrong object/version).
4. `UNDERDETERMINED`/`abstain` are valid, valuable outcomes.
5. Hermes hooks trigger recomputation; **Pāṭala's dependency engine determines** the impact.
6. Scholars use the Workbench / MCP — never install or see Hermes.

---

## 12. FALSIFICATION TEST (before claiming any of this "works")

> **What experiment would convince you this does NOT work?**

- A `REJECT` on an inference does NOT recompute its downstream arguments/cruxes (the mutation doesn't ripple).
- A review can be recorded against the wrong object version (version integrity broken).
- An agent can call a `patala_accept_*` tool (the boundary is leaky).
- The review ladder can skip from CANDIDATE to ADJUDICATED without the intermediate human steps.

If any of these hold, the executable-corrections system is theater, not an operating system.

---

## 13. THE ONE-SENTENCE CARRY-FORWARD

**Pāṭala peer review = a scholar's judgment is an immutable, provenance-carrying graph mutation that
recomputes downstream arguments/cruxes/themes/syntheses and is inherited by future agents — built on the
existing ReviewEvent + supersede primitives, exposed through the Scholar Workbench and the `patala_propose_review`
tool boundary, with Hermes triggering (never determining) the recomputation. Build Phases 3–5 of DEV-PLAN
in this order, gate each on the falsification tests above.**

---

## 14. PHASE 3A — BUILT: the executable-corrections vertical loop (2026-08-12)

The first **executable scholarly correction** is implemented and proven:
`pipeline/review_engine.py` (+ `pipeline/test_review_engine.py`, 15/15 pass).

**The five concepts are real:** `ReviewEvent` (append-only), `ObjectVersion` (immutable),
`DependencyEdge` (GROUNDS / USES_AS_PREMISE / USES_AS_WARRANT / ORGANIZES), `DerivedState`
(deterministically reduced from the ledger), `ImpactReport` (the product-facing output).

**The proven vertical loop (ARG-002, G2-TC2 v1 → v2):**
- a REVISE of G2-TC2:v1 creates an immutable ReviewEvent; v2 is created; v1 is retained
- the deterministic reducer → G2-INF1 NEED_REVIEW, G2-CONC NEED_REVIEW
- the impact report names exactly {G2-INF1, G2-CONC}; ARG-004 (unrelated) untouched
- the reducer is idempotent; a proposition REVISE does NOT stale its source grounding
- REJECT semantics: effective REJECTED, v1 still resolvable (REJECT ≠ delete)

**The doctrine holds:** ACCEPT ≠ truth · REJECT ≠ delete · REVISE ≠ overwrite.

**Next (per DEV-PLAN):** Phase 3B typed-dependency propagation is already partially proven here
(the 4 edge types); Phase 3C ImpactReport done; Phase 3D MCP tools
(`patala_get_review_state` / `patala_propose_review` / `patala_submit_review` / `patala_get_impact`)
and Phase 3E (tiny Workbench review screen) remain. Hermes A4 scheduling (Phase 3F) comes LAST.

---

## 15. PHASE 3D — BUILT: the review capability surface (MCP tools, 2026-08-12)

The executable-corrections review engine is now exposed as object-centric MCP tools (thin layer over
`pipeline/review_engine.py` — the ONLY place review-state logic lives). `mcp/index.mjs` + `review_engine.py`
(23/23 tests pass):

```
patala_get_review_state   → what the graph currently says about an object (state, reviews, supersession, deps)
patala_propose_review     → machine-safe: creates a ReviewProposal (origin=MACHINE, status=PROPOSED), NO state change
patala_submit_review      → the strongest boundary: requires actor_id + actor_kind + authorization_scope;
                            Pāṭala POLICY decides legality (machine actors cannot promote; scholars submit scoped)
patala_get_impact         → what a correction changes (directly + transitively affected, with reason path)
patala_simulate_review    → ZERO-WRITE hypothetical: 'what happens if G2-TC2 is rejected?' (counterfactual precursor)
```

**The executable constitution (tested):** MCP exposes the request; Pāṭala policy decides whether it is
legal. `submit_review` with actor_kind=machine is FORBIDDEN from creating a state-changing ReviewEvent; a
scholar may submit a scoped one. This is where "AI proposes ≠ Pāṭala asserts" becomes operational at the
tool boundary.

**Acceptance loop proven:** get_review_state(G2-TC2:v1) → propose_review(REVISE) → submit_review (machine
blocked, scholar allowed) → reducer computes new state → get_review_state → get_impact. Old version
resolves, review immutable, unrelated ARG-004 unaffected, reads deterministic.

**Next:** Phase 3E (tiny Workbench review screen — a human inspects one object, submits one correction,
sees downstream impact) then Phase 3F (Hermes A4 scheduling, LAST). Keep the MCP thin; do not let
scholarly-state logic leak into the tool layer.

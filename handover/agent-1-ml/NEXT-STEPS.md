# AGENT 1 (ML) — NEXT STEPS (current execution, 2026-08-12 · REVISED)

*This is the current near-term plan for the ML lane, replacing the previous build queue. Read
`AGENTS.md`, `AGENT1-HANDOVER.md`, `INDEX.md`, `_ACTIVE/IR-REVIEW-FINDINGS.md` first. The diagnosis that
shaped this plan: **Agent 1 has an epistemic bottleneck, not an engineering bottleneck.** More machine
evaluation against machine-created targets does not move the epistemic state forward.*

---

## 0. THE DIAGNOSIS (why this plan is short)

Agent 1 currently produces objects that are authored by a machine, reviewed by a machine, and evaluated
by machines. That is a **closed machine loop**:

```
M1 -> G_machine -> M2 -> metric against G_machine
```

That loop tells us how well one machine reproduces another machine's reconstruction. It does **not**
establish philosophical correctness. Every additional neural layer just adds one more machine judging
the last machine's output.

**Two epistemic labels must never be blurred (this vocabulary applies to the whole project, not just
Agent 1):**

```
ENGINEERING_VALIDATED  =  software behaves according to its specified machine target
SCHOLARLY_VALIDATED    =  the target itself has crossed independent scholarly review
```

Until a human crosses the gate, everything is at most `ENGINEERING_VALIDATED`.

---

## THE DOCTRINE OVER AGENT 1 (the decision rule)

> **When the missing oracle is human scholarly judgment, do not substitute another model. Either obtain
> the judgment, or work only on claims whose truth can be established mechanically.**

That gives Agent 1 exactly two legitimate modes right now:

```
  ( Human-reviewed epistemic progress )
  (          OR                       )
  ( construction-verifiable engineering progress )
```

Everything else waits. This is the anti-theatre doctrine made operational.

---

## THE REVISED QUEUE (the whole plan)

```
0. FIX WORKTREES / RECONCILE COMMITS
   ↓
1. GET ≥ 1 ARGUMENT INDEPENDENTLY REVIEWED          (the CP4 critical path)
   ↓
2. BUILD PĀṬALA-FIDELITY SYNTHETIC CORRUPTION SUITE  (construction-verifiable)
   ↓
3. ESTABLISH DETERMINISTIC GRAPH BASELINE            (construction-verifiable)
   ↓
4. WAIT FOR / SUPPORT HUMAN GOLD REVIEW
   ↓
5. ONLY AFTER REVIEW (all currently parked):
      extractor · external argument evaluator · semantic alignment experiments · retrieval experiments
```

Steps 1–3 can proceed concurrently where operationally possible. Step 0 is a hard precondition.

---

## 0. P0 — RESTORE A LEGITIMATE EXECUTION ENVIRONMENT

First resolve the worktree/branch problem (Axiom 11 / INCIDENT-2026-08-12-02) and reconcile the Agent 1
commits (`62cf778`, `263b1ec`, `44c2bd2`, `eb095ae`) onto the `agent1` branch in the Agent 1 worktree.

Until that is done:

```
NO new experimental work
NO benchmark mutations
NO gold edits
NO new model runs presented as canonical
```

This is operational rather than epistemic, but if lanes are meant to be isolated, violating that
invalidates the project's own reproducibility discipline.

---

## 1. P1 — HUMAN REVIEW IS THE BLOCKER (the CP4 critical path)

Make this explicit:

```
ARG-001..005
MACHINE_PROPOSED / CANDIDATE
        ↓
independent Sanskrit/philosophy review
        ↓
at least one INDEPENDENT_REVIEWED argument
        ↓
only now does downstream model evaluation become meaningful
```

The review packet (`benchmarks/v0/ARG-GOLD-REVIEW-PACKET.md`) already exists. So the job is to **stop
engineering around the dependency and optimize the review transaction.** The deliverable is not another
review-architecture document. It is:

```
1 reviewer
× 1 packet
× 5 arguments
× explicit rulings
```

And the first target can be **one clean argument** (ARG-002 v2) — the existing doctrine already says one
independently reviewed argument is enough to begin the external-evaluator pilot.

**The success metric is:**

> `count(INDEPENDENT_REVIEWED argument golds) > 0`

rather than *lines of CP4 code written*.

---

## 2. P2 — BUILD PĀṬALA-FIDELITY NOW (the best build without human judgment)

This is buildable today because the expected answer is generated **by construction**. Start from a
known-good, structurally verified object:

```
SOURCE → L0 → alignment → vertical object
```

Apply deterministic mutations and assert the verifier flags each one.

### Source integrity (expected: P0 MUST FAIL)
```
DROP_SPAN · DUPLICATE_SPAN · SHIFT_SPAN_START · SHIFT_SPAN_END · REORDER_TOKEN · INSERT_UNKNOWN_REGION
```

### L0 analysis (expected: relevant proof dimension must disagree / flag)
```
FLIP_LEMMA · CHANGE_CASE · CHANGE_NUMBER · CHANGE_GENDER · REPLACE_SURFACE
```

### Alignment (expected: alignment verifier detects corruption)
```
SHIFT_ANCHOR · REMOVE_ANCHOR · LINK_WRONG_TOKEN · SWAP_TWO_ANCHORS
```

### Dependency / provenance (expected: vertical integrity fails)
```
DELETE_GROUNDING_EDGE · POINT_TO_NONEXISTENT_REF · USE_STALE_PROOF · CHANGE_SOURCE_HASH
```

**The metric is verifier sensitivity to known injected error:**

```
Sensitivity(V, E) = P( V(x ⊕ e) = FAIL  |  e )
```

which lets us state, e.g., *"P0 detected 100/100 injected source-span corruptions"* — an empirical
claim requiring **no semantic oracle**.

### Boundary (keep these separate)
- Synthetic fidelity fixtures establish: **the verifier detects error types we deliberately inject.**
- They do NOT establish: **the verifier detects all naturally occurring errors.**

```
SYNTHETIC_SENSITIVITY  ≠  REAL_WORLD_RECALL
```

The latter eventually requires human gold.

---

## 3. P3 — ESTABLISH A DETERMINISTIC GRAPH BASELINE

If `same inputs + same code + same parameters` do not produce `same output`, that is unnecessary
epistemic noise. The requirement is stated carefully:

> **There must be at least one deterministic canonical baseline.**

Then later, once real theme gold exists:

```
k-core deterministic baseline  vs  Louvain  vs  Leiden  vs  semantic clustering
```

Don't assume determinism means *better* semantic clustering — but canonical infrastructure must be
reproducible.

**Required test (across separate processes/runs, not just identical calls in one interpreter):**

```python
assert hash(run(graph)) == hash(run(graph))
```

---

## 4. P4 — FREEZE THE SPECULATIVE MACHINERY

Until the human review crosses the gate, explicitly park:

```
REAL ARGUMENT EXTRACTOR · DSPy optimization · HippoRAG · PPR retrieval ·
cross-encoder semantic alignment · semantic microscope B–E · Nyāya evaluator expansion ·
crux ML · argument ranking
```

Not because these are bad ideas. Because their evaluation currently reduces to
`M1 → G_machine → M2 → metric against G_machine`, which does not establish philosophical correctness.

---

## 5. ONE ADDITION — USE THE REVIEW BOTTLENECK TO DESIGN THE SCHOLAR PRODUCT

The exact problem — *"I have five machine-proposed scholarly objects and need a human expert to
adjudicate them efficiently"* — **is literally the prototype of Pāṭala Workbench / Review.** So
instrument the human-review process:

```
minutes / argument
questions that caused confusion
evidence the reviewer needed but lacked
number of revisions
number of abstentions
which machine assertions were easiest / hardest to assess
```

The reviewer is effectively the **first real product user**. Do not merely obtain gold — learn **what
interface makes expert judgment cheap enough to scale.** That data may be worth more than another
retrieval experiment.

---

## 6. GUARDRAILS (unchanged, restated for this plan)

1. Route everything through `benchmarks/v0/` + record a `BenchmarkRun`.
2. Join on `Ref` IDs — never fuzzy.
3. Do NOT hack viruddha into the frozen `nyayagate.py`.
4. Do NOT build the parked machinery (P4) before review.
5. **Git discipline:** work only in the Agent 1 worktree on branch `agent1`; stage only your explicit
   paths + commit immediately; never force-push / rewrite another lane's commit.
6. Update `CLAIMS.md` + `theatre_check.py` honestly; drop a `SESSION-<date>.md` at session end.

---

## THE ONE-SENTENCE CARRY-FORWARD

**Agent 1's bottleneck is epistemic, not engineering: get ≥ 1 argument independently reviewed (the
success metric is `count(INDEPENDENT_REVIEWED) > 0`), build the construction-verifiable
PĀṬALA-FIDELITY corruption suite and a deterministic graph baseline in parallel, and freeze all
machine-eval-on-machine-gold machinery until the human gate crosses — using the review itself as the
first prototype of the scholar product.**

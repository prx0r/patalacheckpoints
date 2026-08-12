# AGENTS-DOCTRINE — the global epistemic-hardening rule for BOTH agents

*2026-08-12. The single governing rule every Pāṭala agent (L0 and ML) operates under. It is global because
it is about how the PROJECT validates claims, not about any one lane. Both handovers reference this.*

---

## THE ONE RULE

> **Nothing is "real" because code exists. It becomes real only when an independently defined task,
> human-grounded gold, and a reproducible evaluation show that it does what its name claims.**

---

## THE THREE CATEGORIES (freeze everything into these)

| Category | Meaning | Example |
|---|---|---|
| **A. INFRASTRUCTURE** | schemas, APIs, representations, renderers | AIF graph, EssayPlan, gold-chain renderer, schemas |
| **B. EVIDENCE** | human-grounded gold, accepted themes, reviewed claims, L0 proofs | ARG-GOLD-001, accepted arguments, L0 proof records |
| **C. RESULTS** | measured system behavior against frozen evidence | a benchmarked relation-F1 number |

**The mistake to never repeat: calling A → C.** Most built components are A (infrastructure). That is
fine. The error is presenting infrastructure as a validated capability.

---

## THE ANTI-THEATRE PROTOCOL (the 9-field contract)

Every component must fill all nine. If any is empty → `EXPERIMENTAL_INFRASTRUCTURE`, not a scholarly
capability.

```
NAME           what capability does it claim?
INPUT          what does it consume?
OUTPUT         what semantic claim does the output make?
AUTHORITY      deterministic / model-proposed / human-reviewed?
GOLD           what independently created evidence tests it?
BASELINE       what dumb/simple method must it beat?
METRIC         how is success measured?
FAILURE MODE   what does a false positive look like?
ADOPTION GATE  what evidence is required before production?
```

Full applied contracts: `COMPONENT-CONTRACTS.md`.

---

## THE EPISTEMIC LABELS (never used interchangeably)

```
BUILT            code exists
TESTED           software behavior tested
BENCHMARKED      evaluated against independent fixtures
VALIDATED        predefined threshold met
EDITOR_REVIEWED  actual human review occurred
PRODUCTION       validated + monitored
```
**164 tests passing ≠ scholarship correct.** Tests prove SOFTWARE validity, benchmarks prove EMPIRICAL
validity, experts prove SCHOLARLY validity. These are three different kinds of validity — never
interchangeable.

---

## THE BANNED WORDS (until independently justified)

- **Ban:** PROVED · TRUTH · VERIFIED SEMANTICALLY · CORRECT · EDITOR APPROVED · BEST · WINS
- **Use:** SUPPORTED BY · PASSED CHECK X · BENCHMARKED ON · MACHINE-PROPOSED · REVIEWED BY · NO CONFLICT DETECTED

This is cosmetic but forces conceptual precision. "B-STRUCT wins" was a lie; "B-STRUCT benchmarked on X
under circular gold" is honest.

---

## THE ABSTENTION PRINCIPLE (know when NOT to assert)

- **Precision over coverage for scholarship:** 40% coverage / 98% grounded > 95% coverage / 75% grounded.
- A good system must abstain: "NO UNIQUE ARGUMENT RECOVERABLE" is a valid, valuable output.
- A model that invents premises where none are recoverable = **severe failure**.
- Metrics include abstention accuracy + false-assertion rate.

---

## THE ADEQUACY DOCTRINE (stop validating when the consumer is served)

> **A supporting component stops when it becomes adequate for its consumer. It does not need to become
> independently perfect.**

The system is supposed to **propagate uncertainty upward**, not eliminate all uncertainty before
composition. An endlessly-tuned supporting layer (OCR, morphology, alignment, sense ranking, retrieval,
clustering, extraction) is *death by infinite validation* — it never produces the thing the layers are
supposed to enable.

- A component is **adequate** when a real consumer can use it to point downward and say: "this higher
  object is grounded approximately here, with these machine witnesses and this uncertainty."
- Its residual uncertainty is **metadata carried into the proposition/argument certificate**, not a blocker.
- Freeze it at that point with an honest status (e.g. `SUPPORTED_MACHINE_WITNESS`), record the evidence,
  and record **when to revisit** ("only when a real downstream failure demands it").
- Do NOT keep optimizing to squeeze a headline number (0.81→0.88) unless a downstream consumer actually
  fails because of it.

**The checkpoint test for a supporting layer:** *"Can its consumer now compose it with an honest
uncertainty label?"* If yes, it is done enough. Build the intellectual layer on top — that is where the
value is.

---

## HUMAN ADJUDICATION IS THE MISSING REALITY LAYER

Avoid the closed loop: *machine creates C1 → machine creates gold → machine evaluates machine.*
For serious fixtures: Author A constructs → Reviewer B independently reviews → disagreement recorded →
adjudication recorded. States: `SINGLE_REVIEWED → DOUBLE_REVIEWED → ADJUDICATED → SPECIALIST_REVIEWED`.

---

## RESULT LINEAGE (no result exists without it)

Every result carries:
```
result_id · benchmark_version · gold_version · model_version · code_commit · split · seed · config · date
```
"Model X achieved 0.71 relation F1" must resolve to an experiment. If it can't resolve, it doesn't exist.

---

## FALSIFICATION BEFORE PROMOTION

Before promoting any capability, the implementing agent must answer:
> **What experiment would convince you this does not work?**

If it can't answer, the capability isn't ready for evaluation. Examples:
- Argument extractor fails if: cannot recover >60% of hand-gold propositions OR false-grounding >5%.
- Nyāya gate fails if: high false-positive fallacy detection OR fails obvious adversarial fixtures.

---

## ADVERSARIAL TESTS NOT WRITTEN BY THE BUILDER

If Agent ML builds extraction, Agent ML must NOT create all its evaluation examples. Agent A generates
adversarial fixtures, Agent B implements, human adjudicates gold. Otherwise the evaluator unconsciously
learns the implementation's assumptions.

---

## CLAIMS.md — the project's own audit ledger

Maintain `CLAIMS.md`: every significant claim (P-001…) with STATUS / EVIDENCE / CAVEAT / REQUIRED.
The project audits itself using its own philosophy. See `CLAIMS.md` for the current state (P-001..P-008).

---

## THE PERMANENT CHECKPOINT TEST

> **Show me the independent evidence that this component performs the semantic function named in its API.**

If the answer is "tests pass / schema validates / looks good / model said so / code is sophisticated" →
it stays experimental.
If the answer is "here is the frozen gold, here was the prediction made blind, here is the metric, here
are the failures, here is the human adjudication" → it is no longer theatre. It is research.

---

## 7. THE ENFORCEMENT MECHANISM (not advisory)

The doctrine is enforced, not just documented:
- **`AGENTS.md`** (repo root) — auto-loaded on any agent entry; points here + to CLAIMS + to the gate.
- **`theatre_check.py --status`** — the mechanical gate. Run it before claiming any component is "done."
  It fails if a component is `EXPERIMENTAL_INFRASTRUCTURE` and you try to promote it.
- **`CLAIMS.md`** — the ledger. Update it honestly when you claim anything works.
- **`COMPONENT-CONTRACTS.md`** — the 9-field contracts; an empty field = not a capability.

A new agent cannot miss this: AGENTS.md is the first file loaded, README item #0 points to it, and
docs/INDEX lists it as "THE GOVERNING RULE — read first."

---

## 8. GIT DISCIPLINE — THE SHARED-TREE RULE (applies to EVERY agent)

The working tree and index are **shared by all agents**. One agent's git mistake contaminates every
other agent's branch. These rules are binding on agent1, agent2, and any future agent:

1. **Stage only your own explicit paths.** Never `git add -A` / `git add .` on a dirty shared tree —
   that sweeps another agent's staged files into your commit (this happened: Agent 2's `4cc78d1`
   absorbed Agent 1's staged ML files, then invasive surgery entangled both lanes).
2. **Commit immediately after staging your own paths.** Do not leave staged work sitting in the shared
   index — another agent's commit will collect it.
3. **Verify the branch before committing.** `git branch --show-current` — work on your own branch
   (`agent1` / `agent2` / ...), never commit to another lane's branch or `main` by accident.
4. **Never do invasive branch surgery on a dirty shared tree.** No `stash`, `cherry-pick`, `reset
   --hard`, `branch -D`, or force operations while there are uncommitted/staged changes from another
   agent. If a commit is misplaced, **flag it to Agent 0** (the coordinator) rather than attempting
   surgery yourself.
5. **Never force-push, never rewrite another lane's commit.** Append-only.
6. **If you discover a crossing, stop and report it** — do not try to untangle it alone; a coordinator
   merge is the safe fix.

> **The rule in one line: treat the shared tree as a public space — stage your own files, commit
> immediately, verify your branch, and never run surgery on it. A misplaced commit is a flag to Agent 0,
> not an invitation to `reset --hard`.**

---

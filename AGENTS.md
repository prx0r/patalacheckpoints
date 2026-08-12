# AGENTS.md — read this FIRST. The governing rule for every agent.

*This file is auto-loaded when any agent works in this repo. It is the FIRST thing you read. It exists
because this project repeatedly built "structurally-elegant-but-hollow" objects and reported them as
results. This file prevents that.*

---

## 0. THE ONE RULE (everything else follows)

> **Nothing is "real" because code exists. It becomes real only when an independently defined task,
> human-grounded gold, and a reproducible evaluation show that it does what its name claims.**

A tested schema is not a result. A typed container is not an argument. A hardcoded status is not an
audit. "N tests pass" is not "scholarship verified."

---

## 1. READ THESE, IN ORDER (do not skip)

1. **`onboarding/README.md`** — the single on-ramp: complete context (rule → vision → map → full
   system), then the specialization gate to your lane. It organizes the existing docs below; read it
   first, then the originals it points to.
2. **`machinelearning/_ACTIVE/AGENTS-DOCTRINE.md`** — the global anti-theatre rule both agents operate under.
   This is the master doctrine: the 3 categories, the 9-field contract, the epistemic labels, the banned
   words, the abstention principle, human adjudication, result lineage, falsification-before-promotion.
3. **`machinelearning/_ACTIVE/CLAIMS.md`** — the project's own audit ledger (P-001…P-008). Before you claim
   anything works, check: is it already claimed? What's its STATUS/EVIDENCE/CAVEAT? Update it honestly.
4. **`machinelearning/_ACTIVE/COMPONENT-CONTRACTS.md`** — the 9-field anti-theatre contract applied to every
   current component (argument, strength, nyaya-gate, aifgraph, essay, c1metrics). Each shows its honest
   status and adoption gate.
5. **`machinelearning/_ACTIVE/dualagentvision.md` + `dualagentvision-ADAPTED.md`** — the north star + the
   checkpoint map (CP0–CP12) of what our infra actually covers.
6. **`machinelearning/_ACTIVE/AGENT1-HANDOVER.md`** (if you are the ML agent) or
   **`handover/agent-2-integration/INDEX.md`** (if you are the L0/integration lane) — your lane's
   current state + doctrine. Cross-lane coordination: `handover/LOG.md`.

---

## 2. RUN THE GATE BEFORE YOU CLAIM ANYTHING IS "DONE"

```bash
python3 machinelearning/theatre_check.py --status
```

This prints the honest status of every component. If a component is `EXPERIMENTAL_INFRASTRUCTURE` (not
`CAPABILITY_CANDIDATE`), **do not present it as a working capability.** If you promote it, you must have
the evidence (gold + blind eval + metric + human adjudication) to do so.

---

## 3. THE PERMANENT CHECKPOINT TEST

Before adding a capability, answer:
> **What experiment would convince you this does NOT work?**

And for every claim:
> **Show me the independent evidence that this component performs the semantic function named in its
> API.**

If the answer is "tests pass / schema validates / looks good / model said so / code is sophisticated" —
it stays experimental. If it's "here is the frozen gold, the blind prediction, the metric, the failures,
the human adjudication" — it's research.

---

## 4. THE 3 CATEGORIES + THE BANNED WORDS

- **A. INFRASTRUCTURE** (schemas, renderers) · **B. EVIDENCE** (gold, reviews, proofs) ·
  **C. RESULTS** (measured behavior). Never call A → C.
- **Ban:** PROVED · TRUTH · CORRECT · EDITOR APPROVED · BEST · WINS
- **Use:** SUPPORTED BY · PASSED CHECK X · BENCHMARKED ON · MACHINE-PROPOSED · REVIEWED BY · NO CONFLICT DETECTED

---

## 5. THE TWO AGENTS (share the boundary contractually)

- **Agent L0** — vertical truth: SOURCE → L0 → morphology → syntax → alignment → philological proof.
  Question: *is this reading licensed by the source?*
- **Agent ML** — horizontal/upward: C1 → themes → arguments → claims → synthesis → review.
  Question: *does this higher representation legitimately derive from the objects beneath it?*
- **Join on:** Passage ID / TranslationDecision ID / PhilologicalProof ID / C1 ID — NEVER fuzzy.

---

## 6. RESULT LINEAGE (a result that can't resolve doesn't exist)

Every result carries: `result_id · benchmark_version · gold_version · model_version · code_commit ·
split · seed · config · date`. If "Model X achieved 0.71 F1" can't resolve to an experiment, it's not a result.

---

*This file is the enforcement mechanism for `machinelearning/_ACTIVE/AGENTS-DOCTRINE.md`. The doctrine is not
advisory — a new agent that skips it will repeat the theatre-building failure this project spent a
session undoing.*

# ARGUMENT GOLD & THE GATE — the vision

*2026-08-12. The strategic vision for the argument layer and how it unblocks the Nyāya gate. This is the
WHY behind the execution in `handover/agent-1-ml/NEXT-STEPS.md`. It belongs beside
`SEMANTIC-COMMENSURABILITY.md`, `NYAYA-GATE-CANDIDATE-V1.md`, and `SPEC_LOGICAL_ARGUMENTS_GOLD.md` as the
canonical framing for where the gate + argument graph are going.*

---

## 0. THE STATE (where we are)

The Nyāya gate is **frozen at `NYAYA_GATE_CANDIDATE_v1`** — measured, honest:
```
defect recall 4/5 · clean FP 0/5 · abstain 1/2
BENCHMARKED_PRELIMINARY · NOT_INDEPENDENTLY_VALIDATED · NOT_SEMANTIC_VERIFIER
```
Its **1 miss — viruddha** — is not a code bug. It is the exact point where the whole system's bottleneck
becomes visible: **you cannot detect "the text argues the opposite" without a real argument graph that
knows what the text establishes.** The gate did its job: it proved both its potential AND exactly why the
argument layer is the next build.

---

## 1. THE VISION (one sentence)

> **Build real Argument Gold first — then viruddha becomes a graph operation over argument-under-a-frame,
> not a keyword hack.**

The gate, counterevidence, adversarial review, and cross-argument comparison all require **real
proposition graphs** before they can be sound. The vision is: grow ARG-GOLD-001 into 5 (then 10) real,
hand-reconstructed arguments, grounded in the DebateFrame/SemanticAlignment layer — so that every future
"contradiction" is a *reasoned* relation-after-alignment, not a manufactured keyword collision.

---

## 2. THE 5 ARGUMENT STRUCTURES (the gold shapes)

Deliberately different — each trains the extractor + the gate on a distinct move:

```
ARG-001  transcendental        the order-less support (V2-O)          ← HAVE IT
ARG-002  objection → reply     the nanu→āha dialectic (V2-L)
ARG-003  reductio              the ordered-support regress (V2-O)
ARG-004  conceptual distinction vimarśa vs prakāśa (V2-H) or one-light (V3-C)
ARG-005  ambiguous              two defensible reconstructions (V3-I difference-real)
```

Each carries the full `Proposition` / `Inference` / `Grounding` / `Defeater` shape, a `boundary`, real
resolvable passage IDs, and — critically — the **DebateFrame/SemanticAlignment** wrapper. ARG-005
(ambiguous) is the crucial case: it records the semantic alignment between two readings, training viruddha
to NOT manufacture a contradiction where a human would say "these are two defensible readings."

---

## 3. THE DEEP PRINCIPLE (why this matters beyond the gate)

From `SEMANTIC-COMMENSURABILITY.md` — the real primitive is **argument-under-a-frame**, and the real
comparison primitive is **relation after semantic alignment**, not bare contradiction. The gate's
viruddha miss is the proof of this:

| Defect | Type | Needs |
|---|---|---|
| asiddha / savyabhicara / satpratipaksa / badhita | structural, local | a keyword/heuristic gate (partially works) |
| **viruddha** | **context-dependent** | **a real argument graph** (knows what the text establishes) |

So the vision is not "build a better gate." It is: **build the argument graph the gate was always going
to need** — and the gate plugs in at CP4 as an audit of the `Inference`, returning
`VIRUDDHA_CANDIDATE` (which the semantic/human layer confirms or rejects), never "viruddha = true."

---

## 4. THE EXECUTION ARC (how the vision lands)

```
Build 1   extend the gold schema with DebateFrame/SemanticAlignment fields
Build 2   create ARG-GOLD-002..005 (5 real arguments, hand-built, resolvable)
Build 3   a gold-consistency validator (passage_id resolves, no orphan nodes, boundary present)
Build 4   attempt automatic extraction blind against the 5 golds → measure
          (proposition P/R · role macro-F1 · grounding precision · explicitness · inference recovery ·
           scope errors · abstention)
Build 5   THEN viruddha as a graph operation over DebateFrames →
          VIRUDDHA_CANDIDATE → semantic layer decides
```
Exact execution: `handover/agent-1-ml/NEXT-STEPS.md`.

---

## 5. THE GUARDRAILS (do not violate)

1. **Do NOT hack viruddha into `nyayagate.py`** — it stays frozen at v1.
2. **Do NOT rush DOUBLE_REVIEWED** before broadening the gate fixtures to 30–50 (clear pos/neg/
   near-miss/ambiguous/insufficient-context/abstain-correct).
3. **Do NOT build the essay layer / Bayesian propagation / more clustering.**
4. **Every passage_id must resolve** — real `pt:passage:ipvv:chunk<...>`, never fuzzy.
5. **Route everything through `benchmarks/v0/`** + record a `BenchmarkRun`.
6. **Keep the honest vocabulary:** MACHINE_PROPOSED / BENCHMARKED_PRELIMINARY / SINGLE_REVIEWED — never
   PROVED / CORRECT / EDITOR APPROVED without a real review event.

---

## 6. THE SELF-CHECK (falsification, before claiming anything)

> **What experiment would convince you this does NOT work?**

- Argument Gold: a second reviewer finds a proposition that doesn't match the C1/source.
- Gold-consistency validator: a passage_id doesn't resolve; an inference references a missing node.
- Extraction: can't recover >60% of gold propositions, or false-grounding >5%.
- viruddha-via-graph: flags as VIRUDDHA a pair a human says are CONCEPTUAL_MISMATCH / QUESTION_MISMATCH.

---

## 7. THE CARRY-FORWARD (one sentence)

**The Nyāya gate is frozen (measured, honest); the next build is real Argument Gold (ARG-001..005) with
the DebateFrame/SemanticAlignment layer — because viruddha, counterevidence, and all cross-argument
comparison require argument-under-a-frame, and a real argument graph, before they can be sound. Build the
gold first, validate it's internally consistent, then test extraction against it blind — and only then
does viruddha become a graph operation rather than a keyword hack.**

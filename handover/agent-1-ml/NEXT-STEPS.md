# AGENT ML — NEXT STEPS (exact execution, 2026-08-12)

*The precise how-to for the next session. Read `AGENTS.md`, `AGENT1-HANDOVER.md`, `CHECKPOINTS-ML.md`,
`SESSION-2026-08-12.md`, `NYAYA-GATE-CANDIDATE-V1.md`, `SEMANTIC-COMMENSURABILITY.md` first. This is the
*execution* layer on top of those.*

---

## 0. WHERE YOU ARE (one paragraph)

The Nyāya gate is frozen at `NYAYA_GATE_CANDIDATE_v1` (defect recall 4/5, clean FP 0/5, abstain 1/2).
Its 1 miss — **viruddha** — exposed the real bottleneck: you need **real argument graphs** before you can
detect "the text argues the opposite." So the next build is **Argument Gold v0**: grow ARG-GOLD-001 into
5 real, hand-reconstructed arguments, structured for the DebateFrame/SemanticAlignment layer that
viruddha, counterevidence, and cross-argument comparison all require. Everything you build now must make
viruddha a *graph operation*, not a keyword hack.

---

## 1. THE GOAL: ARG-GOLD-001 → ARG-GOLD-005 (then 010)

Build 5 real arguments, deliberately different structures. Each is a `BenchmarkFixture` (task
`ARGUMENT_EXTRACTION`) with the full `Proposition`/`Inference`/`Grounding`/`Defeater` shape.

### The 5 structures (from `CHECKPOINTS-ML.md`)
```
ARG-001  transcendental   — the order-less support (you HAVE this: ARG-GOLD-001, V2-O)
ARG-002  objection → reply — a nanu→āha exchange (the IPVV's dialectic, e.g. V2-L the non-constructed I)
ARG-003  reductio          — the "if X then absurdity → ¬X" move (e.g. V2-O: if the support were ordered, regress)
ARG-004  conceptual distinction — a term-distinction (V2-H vimarśa vs prakāśa; or V3-C one-light)
ARG-005  ambiguous / two defensible reconstructions — a genuine crux with 2 readings (e.g. V3-I difference-real)
```

### The per-argument required fields (each, no exceptions)
```
fixture_id, benchmark_version="v0", task="ARGUMENT_EXTRACTION", split="EVAL_ONLY",
review_state="SINGLE_REVIEWED", allowed_training_use=false

expected:
  passage_id        (real, resolvable — pt:passage:ipvv:chunk<...>)
  nodes[]           Proposition objects:
                      proposition_id, text, kind (TEXTUAL_CLAIM|INTERPRETIVE_CLAIM|IMPLICIT_PREMISE|
                                                  CONCLUSION|OBJECTION|QUALIFICATION),
                      explicitness (EXPLICIT|RECONSTRUCTED|IMPLICIT),
                      grounding (passage_id, source_span_ids, c1_id, l200_assertion_id),
                      boundary, status="MACHINE_PROPOSED"
  inferences[]      Inference objects:
                      premise_ids, conclusion_ids, scheme
                      (NYAYA_ANUMANA|REDUCTIO|TRANSCENDENTAL|CONCEPTUAL_DISTINCTION|OBJECTION_REPLY|COUNTEREXAMPLE),
                      rationale, defeaters[]
  defeaters[]       Defeater objects: type (COUNTEREVIDENCE|RIVAL_READING|COUNTEREXAMPLE|FAILED_PREMISE|SCOPE_PROBLEM)
  boundary          what the argument does NOT claim
```

### The DebateFrame/SemanticAlignment wrapper (NEW — the anti-fake-contradiction layer)
Each gold argument should optionally carry (or at least be *able* to carry):
```
debate_frame: {
  question, object_of_dispute, concept_refs, shared_ground, disputed_ground,
  semantic_alignments: [ { left_term, right_term, relation, rationale } ]
}
```
For ARG-005 (ambiguous) especially, record the **semantic alignment** between the two readings — that's
the case that trains viruddha to NOT manufacture a contradiction.

---

## 2. THE SOURCES TO DRAW FROM (real passages, already on disk)

**IMPORTANT (verified 2026-08-12):** these C1 + L2 files are NOT in the patala repo. They live on the
**sanskritree mount**. Absolute paths:
```
C1:   /mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv/c1/read/
L2:   /mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv/pilot/   (pilot_V*_L2_read.md)
L200: /mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv/l200/
```
The passage_ids (`pt:passage:ipvv:chunk...`) resolve against `data/published/ipvv/index.json`.

| Argument | Source C1 (on mount) | L2 read (on mount) | Passage id (resolves) |
|---|---|---|---|
| ARG-001 transcendental | `c1/read/c1_V2O-orderless-support.md` | `pilot/pilot_V2O_L2_read.md` | `chunkV2-O-saptamo-vimarsa.md` |
| ARG-002 objection-reply | `c1/read/c1_V2L-nonconstructed-I.md` | `pilot/pilot_V2L_L2_read.md` | `chunkV2-L-sastho-vimarsa-smrti-apohana.md` |
| ARG-003 reductio | `c1/read/c1_V2O-orderless-support.md` | `pilot/pilot_V2O_L2_read.md` | `chunkV2-O-saptamo-vimarsa.md` |
| ARG-004 conceptual distinction | `c1/read/c1_V2H-vimarsa-paravak.md` | `pilot/pilot_V2H_L2_read.md` | `chunkV2-H-pancamo-vimarsa-k11-13.md` |
| ARG-005 ambiguous | `c1/read/c1_V3I-difference-real.md` | `pilot/pilot_V3I_L2_read.md` | `chunkV3-I-kriya-caturtho-close-k20-21.md` |

**Pattern for each:** read the C1 (the `> ` body), read the L2 (`pilot/pilot_<chunk>_L2_read.md`), extract
the actual propositions, then hand-construct the gold object. **Do NOT automate extraction yet** — these
are the gold fixtures a machine will be tested against.

---

## 3. THE EXACT NEXT BUILDS (in order, with what to touch)

### Build 1 — Extend the gold schema to carry DebateFrame/SemanticAlignment
- Touch: `patala_ml/gold.py` (add the DebateFrame/SemanticAlignment fields to `build_gold_v0` or a new
  `build_gold_series`), `benchmarks/v0/SCHEMA.md` (add the fields).
- Test: extend `test_gold.py` to assert the new fields are present + resolvable.

### Build 2 — Create ARG-GOLD-002..005
- Touch: `benchmarks/v0/structure/PAT-STRUCT-002.json` ... `-005.json` (the 5 real arguments).
- Each is a hand-built `BenchmarkFixture` with the full Proposition/Inference/Defeater shape.
- Verify each passes `ingest_fixture.py` (schema + source resolution + leakage).

### Build 3 — A gold-consistency validator
- Touch: a small script that walks all ARG-GOLD fixtures and checks: every passage_id resolves, every
  inference's premises/conclusion exist as nodes, no orphan nodes, boundary present.
- This is the "the gold is internally consistent" gate (like `test_gold.py` but across all 5).

### Build 4 — THEN (and only then) attempt automatic extraction
- Run the (still-primitive) extractor against the 5 golds blind.
- Measure: proposition precision/recall · role macro-F1 · grounding precision · explicitness accuracy ·
  inference recovery · scope errors · **abstention**.
- This tells you whether extraction is worth building out — with real gold to test against.

### Build 5 — THEN viruddha becomes a graph operation
- Once proposition graphs exist, viruddha = "retrieve accepted propositions related to H/S → does H
  support ¬S → VIRUDDHA_CANDIDATE → semantic layer decides." NOT a keyword hack.

---

## 4. THE GATES (what "done" means for each build)

- **Build 1 done:** DebateFrame/SemanticAlignment fields exist on the gold schema + tests pass.
- **Build 2 done:** 5 real arguments (ARG-001..005) in `benchmarks/v0/structure/`, each passing
  `ingest_fixture.py`, with real resolvable passage IDs + actual propositions + boundary + defeaters.
- **Build 3 done:** the gold-consistency validator passes on all 5.
- **Build 4 done:** blind extraction metrics recorded against the 5 golds (in a `BenchmarkRun`).
- **Build 5 done (future):** viruddha as a graph op over DebateFrames, still returning
  `VIRUDDHA_CANDIDATE` (not "viruddha = true").

---

## 5. THE GUARDRAILS (do not violate)

1. **Do NOT hack viruddha into `nyayagate.py`.** It stays frozen at v1.
2. **Do NOT rush DOUBLE_REVIEWED** on the 12 gate fixtures before broadening to 30–50 (clear pos/neg/
   near-miss/ambiguous/insufficient-context/abstain-correct).
3. **Do NOT build the essay layer / Bayesian propagation / more clustering.**
4. **Every passage_id must resolve** — real `pt:passage:ipvv:chunk<...>` IDs, never fuzzy.
5. **Route everything through `benchmarks/v0/`** + record a `BenchmarkRun` for any result.
6. **Update CLAIMS.md** (add P-009 for Argument Gold, P-010 for DebateFrame) + `theatre_check.py` as you go.
7. **Keep the honest vocabulary:** MACHINE_PROPOSED / BENCHMARKED_PRELIMINARY / SINGLE_REVIEWED — never
   PROVED / CORRECT / EDITOR APPROVED without a real review event.

---

## 6. THE "NO-BS" SELF-CHECK (before you declare anything done)

Ask of each build:
> **What experiment would convince you this does NOT work?**

- Argument Gold: "a second reviewer finds a proposition that doesn't match the C1/source."
- The gold-consistency validator: "a passage_id doesn't resolve; an inference references a missing node."
- Extraction: "can't recover >60% of gold propositions, or false-grounding >5%."
- viruddha-via-graph: "flags as VIRUDDHA a pair that a human says are CONCEPTUAL_MISMATCH or
  QUESTION_MISMATCH."

If you can't answer the falsification question, the capability isn't ready to claim.

---

## 7. THE ONE-SENTENCE CARRY-FORWARD

**The Nyāya gate is frozen (measured, honest); the next build is real Argument Gold (ARG-001..005)
with the DebateFrame/SemanticAlignment layer — because viruddha, counterevidence, and all cross-argument
comparison require argument-under-a-frame, and a real argument graph, before they can be sound. Build the
gold first, validate it's internally consistent, then test extraction against it blind — and only then
does viruddha become a graph operation rather than a keyword hack.**


---

**The canonical vision for this work:** `machinelearning/ARGUMENT-GOLD-VISION.md` — the strategic WHY behind these steps (Argument Gold unblocks the gate; viruddha becomes a graph op).

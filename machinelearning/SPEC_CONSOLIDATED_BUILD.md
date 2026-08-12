# PĀṬALA — CONSOLIDATED SPEC & BUILD PLAN (for review)

*2026-08-12. One document that puts **every thread we've worked on in the open**, states what exists,
what's proposed, and exactly what to build next — with justification. The user reviews this first;
then we build. It is the single map; the detailed docs below are the chapters.*

---

## 0. How to read this

- **State of the world** (§1) — what's real and committed right now.
- **All the threads** (§2) — every idea/vision/spec we've produced, with its status.
- **The plan** (§3) — the ordered build, each step justified.
- **Ownership** (§4) — who (which agent) builds what.
- **Review checklist** (§5) — what I need you to sign off on.

---

## 1. STATE OF THE WORLD (verified 2026-08-12)

### Committed (git clean base)
- **`4f4f9d3`** — the deterministic scholarly substrate: 49 IPVV passages (lazy JSON store,
  source + L2 + **C1 verse_commentary[]** + c1_source), verify services (quote/claim-structure/
  trace-dependency/counterevidence), themes, resolve kernel, hub. Tests pass, build green.
- **`bea6a19`** — the source-centric **hub** (`data/corpus/hub.ts` + `/api/hub` + `get_work_hub` MCP),
  the **PUSHING method** spec, and the **logical-arguments-as-gold** vision.

### In-flight (other agent, not mine to touch)
- `data/corpus/hub.ts` — adding the PUSHING guide + V3-I session.
- `machinelearning/SPEC_ARGUMENT_TRUTH_PACKET.md` — the argument-as-truth-packet spec (light).
- `machinelearning/COMPOUNDING_RESEARCH_SYSTEM.md` — the compounding vision.
- `docs/INDEX.md`.

### My lane (MachineLearning, committed + working)
- `machinelearning/` docs: `MLUSEINPATALA.md` (frozen strategy), `MLVISION.md`, `DEVPLAN.md`,
  `VISION-COMPUTABLE-TRADITION.md`, `IPVV-STACK-INTEGRATION.md`, `mlreview.md`, `mlcurriculum.md`,
  `mllogical.md`, `GAPS.md`, `DUAL_AGENT_TRACK.md`, `HANDOFF-LOG.md`, plus the PATALAML mirrors.
- `machinelearning/research/` — a working, committed, CPU-only ML package:
  `patala_ml/` (corpus, retrieval, metrics, eval, generate_tasks), task files, and **two real
  experiment results** with statistical rigor.

---

## 2. ALL THE THREADS (the full open ledger)

| Thread | Doc / artifact | Status | Note |
|---|---|---|---|
| **ML strategy** | `MLUSEINPATALA.md` | FROZEN | benchmark-first, EXPOSE/INFER, leakage, human-review gate |
| **Big vision** | `MLVISION.md` | done | self-improving scholarly intelligence, > FoJin |
| **Product vision** | `VISION-COMPUTABLE-TRADITION.md` | done | the epistemic gearbox, misconception maps, journeys |
| **Dev plan** | `DEVPLAN.md` | done | granular steps + tests |
| **Stack audit** | `IPVV-STACK-INTEGRATION.md` | done | verified corpus + wiring |
| **Resource registry** | `research/RESOURCES.md` | done | datasets, HF models, git refs |
| **Curriculum** | `mlcurriculum.md` | done | 26 verified papers + deliverables |
| **Dual agent** | `DUAL_AGENT_TRACK.md` | done | both lanes in depth + how they compound |
| **ML research lane** | `research/patala_ml/` | **working** | corpus loader, BM25/dense/hybrid, eval with CI |
| **Experiment E1** | `experiments/E1-fidelity-REPORT.md` | **result** | BM25 ≥ dense for C1→L2 fidelity |
| **Experiment E2** | `experiments/retrieval_bm25_dense_hybrid.json` | **result** | hybrid best R@5 on hard retrieval |
| **Logical args** | `SPEC_ARGUMENT_TRUTH_PACKET.md` (other) + `mllogical.md` (mine) | proposed | the argument as a typed truth-packet |
| **Hub / PUSHING** | `COMPOUNDING_RESEARCH_SYSTEM.md` (other) | proposed | source-as-hub + PUSHING→argument→proof→essay→learning |
| **Handoffs** | `HANDOFF-LOG.md` | 1 entry | E1 result + requested themes-with-evidence |

### The one coherent story across all threads
The project is building toward a **computable scholarly tradition**: one evidence graph, multiple
controlled explanatory projections (scholar → student → GEN-Z → media), each verified against the graph.
The two rails that make it real:
- **Agent 2 (integration):** structure the scholarship (C1, hub, logical arguments, PARALLELS, L200).
- **Agent 1 (me):** make the structure *learnable and verifiable* (baselines, benchmark, retrieval,
  the argument-verification floor, and the experiments that prove a model beats a baseline).

---

## 3. THE PLAN (what to build, in order, justified)

### Decision the reviewer must make FIRST
There is one fork in the road that shapes everything. I'll present both, recommend one.

**Option A — Finish the retrieval/eval lane first (recommended).** Complete the benchmark suite, the
Sanskrit tokenizer, and the full three-arm retrieval baselines, so every later claim is empirical.
Justification: the strategy's whole discipline is "benchmark before model." Without it, the
logical-argument work and the vision products are built on un-measured assertions.

**Option B — Build the argument truth-packet first.** The other agent's `SPEC_ARGUMENT_TRUTH_PACKET.md`
is ready; a worked example proves the PUSHING→argument→essay loop. Justification: it's the most
*computable* and the most *demonstrable* single artifact.

**My recommendation: Option A, but with a small slice of B as a proof-of-life.** Reason: A gives the
empirical floor; B gives a tangible win. They're not actually in conflict — the argument-packet and the
retrieval lane both need the same substrate. Do A's benchmark+baselines, then B's first worked argument
*as a test of the premise→support retrieval task* (which is exactly where the logical pipeline becomes
ML gold). This threads the needle.

### The concrete build queue (both options converge)

**Q1 — Formalize the Pāṭala Benchmark Suite (from `BENCHMARK_HANDOVER.md`).**
Convert the documented seed (gold.ts 2, qa_v1_gold 34, stall-log 60) into schema'd task files my
`eval.py` consumes, with the leakage-safe split policy (passage→chunk→vimarśa→work). Already have
49 retrieval + 22 structure + 49 fidelity fixtures generated from real see_also edges.
*Justification:* the single most important ML decision; everything else is measured against it.

**Q2 — Sanskrit-aware tokenizer (honest tier).**
Build the tokenizer with an explicit honesty label (surface / morphological / embedding-tolerating).
*Justification:* current search is `lemmatized:false` substring; dense retrieval already tolerates
inflection, which is *why* it may win on retrieval but not fidelity. Naming the tier keeps claims honest.

**Q3 — Full retrieval baselines on PATALA-RETRIEVAL (hard).**
Complete BM25/dense/hybrid with CIs on the hard, non-leaky task (partly done: hybrid R@5=0.735 best).
*Justification:* the thing every future model must beat.

**Q4 — The argument truth-packet worked example (Option B slice).**
Take one IPVV reflexivity tension → type it as an `ArgumentTruthPacket` → run `/verify-argument`
(structural floor: premises resolve, enums valid, status consistent) → **honest** verdict (no simulated
Lean "PROVED").
*Justification:* proves the loop end-to-end AND yields the first premise→support gold for retrieval.

**Q5 — The premise→support retrieval task (the logical ML win).**
From the typed arguments, derive premise→cited-passage gold pairs; run BM25 baseline.
*Justification:* gold derived from real scholarship, not invented — the flagship ML contribution of the
logical layer.

**Q6 — The THEMES four-arm experiment.**
text vs structure vs hybrid vs learned, gated on the benchmark, using Agent 2's themes-with-evidence.
*Justification:* the frozen flagship research question.

**Q7 — Vertical Fidelity benchmark (the cross-domain artifact).**
Paired L2→C1→Theme→Guide + corruption set. Requires Agent 2 to produce the pairs.
*Justification:* the most novel, potentially publishable-outside-Sanskrit artifact.

### The dependency graph
```
Q1 benchmark ──► Q3 baselines ──► Q6 THEMES experiment
        │              ▲
        └─► Q2 tokenizer┘
Q4 argument (needs Agent2 spec) ──► Q5 premise→support (needs Q1)
Q7 vertical fidelity (needs Agent2 pairs)
```

---

## 4. OWNERSHIP (per the dual-agent track)

| Work | Owner |
|---|---|
| Benchmark suite, tokenizer, baselines, THEMES experiment, Vertical-Fidelity eval | **Agent 1 (me)** |
| Argument-truth-packet schema + `/verify-argument` + truth-engine link | Agent 1 (proposed schema) — Agent 2 emits real records |
| themes-with-evidence (members + edge reasons), typed PARALLELS, L200-as-annotations, C1-pairs | **Agent 2** |
| Hub, PUSHING, logical-args specs, reader | Agent 2 |

---

## 5. REVIEW CHECKLIST (what I need your sign-off on)

1. **The fork (A vs B)** — confirm Option A-with-a-slice-of-B, or override.
2. **The order Q1–Q7** — reorder if you disagree.
3. **The argument-truth-packet** — you (or Agent 2) already drafted it; my `mllogical.md` adds the
   ML-eval angle (premise→support task, no fake-oracle). Confirm it's compatible.
4. **The honest-verdict rule** — agree that until real Lean exists, the truth-engine verdict is a
   *label* (`engine:manual`, `status:REVIEWED`), never a simulated "PROVED." This is a credibility
   protection.
5. **Version pin** — approve adding `data/published/ipvv/version.json` so my eval can detect a stale
   corpus snapshot.
6. **First concrete deliverable** — approve me starting Q1 (formalize the benchmark suite) now, since
   it's fully in my lane and unblocks everything.

---

## 6. WHAT I'LL BUILD IMMEDIATELY (on your go)

Start **Q1: formalize the Pāṭala Benchmark Suite** — schema-validate the existing fixtures, add the
leakage-safe split utility, wire the gold.ts + qa_v1_gold + stall-log seed into `eval.py`-consumable
task files, and record a reproducible run. This is 100% in my lane, touches nothing Agent 2 owns, and
unblocks Q3/Q5/Q6.

Then Q2 (tokenizer) and Q3 (full retrieval baselines) — both independent, both buildable now.

I will **not** build Q4–Q7 until you've reviewed the argument spec and confirmed the fork + order.

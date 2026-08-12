# CONTEXT ENGINEERING — the two-track agent system (shared context, then specialization)

*2026-08-12. How to brief a new agent (or pair of agents) so they share the vision context and then
diverge into their lanes without losing the common map. The principle: **share the foundation, split
the depth.** This is the operational form of `DUAL_AGENT_TRACK.md` and the sequencing in
`VISION_AND_NAVIGATION.md`.*

---

## 1. The model

```
SHARED CONTEXT  (the foundation — every agent gets this)
  VISION_AND_NAVIGATION.md   (the vision + progression + navigation)
  docs/INDEX.md              (the canonical reference)
  THE_COMPANION.md           (the full-system onboarding, sanskritree)
  the corpus + hub + verification floor  (the shared substrate)
        │
        ▼  (the split point — after STEP 3 of the progression)
AGENT 1 — ML/RESEARCH              AGENT 2 — INTEGRATION/CONTENT
  · benchmark, retrieval, tokenizer   · hub, PUSHING, comparative
  · experiments, vertical fidelity    · logical-args specs, reader
  · mllogical, mlpushing              · the essays, the Sanskrit work
        │                              │
        └────────── meet again at ─────┘
        the comparative matrix + the argument truth-packet (the shared outputs)
```

**Most of the context is shared** — the two lanes only diverge after the substrate (corpus +
verification + hub). That is the correct engineering: both need the same foundation, and neither
re-derives it.

---

## 2. The shared context (both agents MUST have this)

This is the "read first, in order" bundle. It gives the agent the *why*, the *order*, and the *map*:

| Doc | Why | Order |
|---|---|---|
| `VISION_AND_NAVIGATION.md` | the vision + the 8-step progression + navigation | 1 |
| `docs/INDEX.md` | the flat canonical reference (single source of truth per concern) | 2 |
| `THE_COMPANION.md` (sanskritree) | the full-system technical onboarding | 3 |
| `docs/PHASE1_IPVV_CORPUS_PROCESS_NOTES.md` | what the corpus is and how it was built | 4 |
| `machinelearning/IPVV-STACK-INTEGRATION.md` | the verified state of the stack + wiring | 5 |
| `data/corpus/hub.ts` + `/api/hub` | the source-centric organizing primitive | 6 |
| the verify/resolve/themes APIs | the deterministic floor | 7 |

**The shared-context test:** after reading these, an agent can state (a) the vision, (b) the 8-step
order, (c) where everything lives, (d) the current state. If they can't, they haven't finished the
shared context.

---

## 3. The split (per-lane context, after the shared foundation)

### AGENT 1 — ML/RESEARCH (owns the learnable/verifiable half)

Deep context:
- `machinelearning/MLUSEINPATALA.md` (the frozen ML strategy)
- `machinelearning/DEVPLAN.md` (the granular execution plan)
- `machinelearning/SPEC_CONSOLIDATED_BUILD.md` (the master map + Q1–Q7 queue)
- `machinelearning/MLVISION.md` + `VISION-COMPUTABLE-TRADITION.md` (the ML/product vision)
- `machinelearning/mllogical.md` + `mlpushing.md` (the ML reads of the logical/pushing work)
- `machinelearning/BENCHMARK_HANDOVER.md` (the benchmark seed)
- `machinelearning/research/patala_ml/` (the working ML package + experiments)

**Its contract:** benchmark-first, EXPOSE/INFER split, leakage-safe, honest verdicts (no fake
"PROVED"), human-review gate. It builds OVER the substrate Agent 2 exposes.

### AGENT 2 — INTEGRATION/CONTENT (owns the scholarly/integration half)

Deep context:
- `../research-library/pushing/PUSHING_GUIDE.md` + `AUTONOMOUS_PUSHING_AGENT_SPEC.md` (the method)
- `../research-library/pushing/QUESTIONNAIRE_REAL_DNA.md` + `SPEC_COMPARATIVE_PUSHING.md` (the
  questionnaire + comparative)
- `machinelearning/SPEC_LOGICAL_ARGUMENTS_GOLD.md` + `SPEC_ARGUMENT_TRUTH_PACKET.md` (the gold)
- `machinelearning/COMPOUNDING_RESEARCH_SYSTEM.md` (the hub/compounding vision)
- `../research-library/recognition/` (the essay library)
- the data/API/MCP/reader code

**Its contract:** expose structure (hub, comparative, PARALLELS, L200), produce the essays +
comparative matrix + argument truth-packets with passage anchors, keep docs canonical.

---

## 4. The handoff (how they meet)

| Agent 2 → Agent 1 | Agent 1 → Agent 2 |
|---|---|
| "Exposed X" (themes, comparative, hub) → Agent 1 builds retrieval/eval over it | "Needs X" (paired data, L200-as-annotations, themes-with-evidence) → Agent 2 produces it |
| The comparative matrix + argument truth-packets are the shared outputs both consume | The benchmark + retrieval results feed back into what's worth pushing |

Both log to `handover/LOG.md` (one entry per handoff: what, why, file, date).

---

## 5. The briefing recipe (for launching a new agent)

To brief a new agent, hand it this exact bundle:

1. **Say:** "Read `VISION_AND_NAVIGATION.md` first, then `docs/INDEX.md`, then `THE_COMPANION.md`."
   (This is the shared context.)
2. **Ask it to verify:** "State the vision, the 8-step order, where things live, and the current
   state." (The shared-context test.)
3. **Tell it its lane:** "You are Agent 1 (ML) — read the ML bundle and own the benchmark/retrieval/
   experiments. OR you are Agent 2 (integration) — read the PUSHING/comparative/logical bundle and
   own the hub, comparative, essays, and the argument truth-packets."
4. **Tell it the contract:** Agent 1 = benchmark-first, honest verdicts. Agent 2 = expose structure,
   keep docs canonical, anchor everything to passages.
5. **Point it at the handoff log:** check `handover/LOG.md` + the lane INDEXs
   (`handover/agent-1-ml/`, `handover/agent-2-integration/`) for the last state, and log any new
   handoff.

---

## 6. Why this works

- **Shared foundation, split depth** — both agents have the vision + the map; they only diverge on
  the specialized how-to. No re-deriving the substrate.
- **No context collision** — the shared docs are few and canonical; the lane docs are deep and
  non-overlapping.
- **The split point is principled** — it happens exactly where the work divides (after the corpus +
  verification + hub), not arbitrarily.
- **They meet on the shared outputs** (comparative matrix + argument truth-packets), which are the
  highest-value artifacts of the whole system.

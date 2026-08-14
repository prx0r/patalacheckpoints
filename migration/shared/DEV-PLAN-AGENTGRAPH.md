# DEV-PLAN-AGENTGRAPH.md — the frontier plan (agentgraph's lane in the two-sided build)

*2026-08-14 · status: AGENTGRAPH'S DEV PLAN · I am **agentgraph** (the ip-graph frontier lab at
`/mnt/HC_Volume_106427611/ip-graph`). This is my honest, sober plan for MY lane in the two-sided build
with **agentpatala** (production/tester at `/root/projects/patala`). Read `ROLE-SEPARATION.md` +
`HANDOFF-QUEUE.md` for the standing contract. This file records who I am, what I actually have, and what
I will build next — so both sides know the plan is agentgraph's.*

---

## WHO I AM (agentgraph)

**I am the frontier.** I build novel kernels from frontier papers (fojin, EleutherIA, SAGE, Darwin Godel,
HyperGraphRAG, ...), prove their mechanisms on real-data stand-ins, and map them to a Pāṭala layer/product.
**My "done" = kernel exists + imports + `validate-*.py` passes on real stand-in data (mechanism proven).**
I do NOT wire into the live Pāṭala system (that's agentpatala's lane).

---

## MY HONEST STATE (verified, not aspirational)

| Artifact | Count |
|---|---|
| Kernels in `lib/` | **37** |
| Experiments (matrix) | **75** |
| Tests passing | **75/75** |
| Theatre (real-data / mechanism / unproven) | **35 PROVEN / 39 mech / 0 unproven** |
| Cloned frontier repos | **48** |
| Fully-built (real-data validator) | **30** |
| Mechanism-only (synthetic) | **6** (education, pedagogy, organism, organism_loop, agent_delivery, evolve) |

**My lane in the shared queue:** the **27 FRONTIER kernels** (built + validated, not yet wired by
agentpatala) + the **NOT-BUILT gaps** assigned to me:
- `misconception.py` (the repair cascade — the flywheel's closing edge)
- Live TranslationProof auditors (xCOMET/MQM)
- Context paging (gap A)

---

## THE SOBER VERDICT ON MY OWN WORK

> **My machine is over-proven and under-fed.** 75 validators prove a *machine*, not a *corpus*. My job is
> the FRONTIER — so my depth gap is different from agentpatala's (who wires the corpus). But the same
> principle applies: I have too many proven kernels and not enough that close a real Pāṭala loop.

---

## MY DEV PLAN (depth over breadth — agentgraph's lane)

### P1 — close the NOT-BUILT gaps assigned to me (the highest value for the organism)
1. **`misconception.py` — the repair cascade** (the biggest gap in the shared queue). Build the kernel
   that closes the co-evolving loop: `MisconceptionLikelihood = f(cluster_size, persistence, ambiguity_signal,
   novice_rate)` → cross threshold → source flagged for scholar review → RKA propagate the fix → confusion
   measured to dissolve. This is the flywheel's closing edge — the single most important thing I can build.
2. **Live TranslationProof auditors** — wrap xCOMET/MQM/OTTAWA as real proof-generator auditor adapters
   (not just the container). This makes the TranslationProof moat *generative*, not just a container.

### P2 — the frontier experiments agentpatala can then integrate (my lane)
3. **Context paging (gap A)** — lossless context virtualization over the compiled bundles. The agent
   read-plane is incomplete without it; I build the kernel, agentpatala wires it.
4. **Promote the 6 MECHANISM-ONLY kernels to real-data** — the organism/education/evolution layer is the
   only partial layer (L09). I can give these real-data validators on the IPK corpus so agentpatala has
   proven-on-real mechanisms to integrate, not just synthetic.
5. **The remaining frontier steals** (from the arXiv GAP/BET list): ToG-2 alternating retrieval,
   G-reasoner graph-foundation, HyperGraphRAG n-ary argument (Bet 1) — as kernels with validators.

### P3 — keep the frontier honest
6. **Resync my docs to the code** — GAPS.md is stale (claims the read plane doesn't exist; it does).
   My contribution to trust: my docs always match my 75/75 + 37-kernel reality.

---

## WHAT I HAND AGENTPATALA (the handoff contract)

Every kernel I build ships as: **a kernel in `lib/` + a passing `validate-*.py` on real stand-in data +
a BUILT-BY-LAYER/COHERENCE-AUDIT line (what layer/product it serves).** Then agentpatala wires it into
real Pāṭala, tests on real IPVV/Hermes, and marks it INTEGRATED. The promotion gate is theirs.

---

## THE BOUNDARY I RESPECT

- I do NOT touch the Pāṭala live system (`pipeline/`, `app/`, the registry, the site, the real corpus).
- I do NOT claim anything is "production" — that's `INTEGRATED`, and only agentpatala grants it.
- I run in **separate processes** from agentpatala (the `schema.py` collision).

---

## THE FILES THAT DEFINE ME

| File | What it is |
|---|---|
| `ROLE-SEPARATION.md` | the standing two-sided contract |
| `HANDOFF-QUEUE.md` | the live kernel→integration truth (updated by both) |
| `DEV-PLAN-AGENTGRAPH.md` | **this file — my frontier dev plan** |
| (in my repo) `BUILT-BY-LAYER.md`, `COHERENCE-AUDIT.md`, `KERNELS-INDEX.md` | my build/integration map |
| (in my repo) `DEV-PLAN-HONEST.md` | my sober one-repo plan |

---

*This is agentgraph's plan. I am the frontier: I build and prove the mechanisms, hand them to agentpatala
to make real, and keep the queue honest. The organism gets real when my frontier closes its gaps and
agentpatala wires them into the live corpus.*

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

### P0 — THE MONA LISA: Tantrāloka from scratch, as the canonical full-stack test
Pick ONE great target and run the ENTIRE organism on it end-to-end — the graduation test at corpus scale.
**Tantrāloka (Abhinavagupta)** is the pick: it's the deepest, most load-bearing Śaiva work, it connects
directly to Abhinavagupta + recognition (the IPVV's sibling), and we have BOTH the Sanskrit root AND the
Dyczkowski translation for later validation.

**Audit update (2026-08-14):** a 4-agent completeness audit found THEATRE in my own Tantrāloka validators
(translation hand-fed proof fields; vs-Dyczkowski fabricated both readings; argument/fullstack hand-typed
the structure). The vs-Dyczkowski one is FIXED (now extracts Dyczkowski's real vol1 text, measures honestly
at 0.1). The others need real Hermes execution. The pushing crux compass is now wired (`pushing_miner.py`).

**The sources (already on disk):**
- **Sanskrit root**: `/root/projects/tantraloka/texts-original/gretil_tantraloka.txt` (17,684 lines, the
  Kashmir Series 1918-38 edition via GRETIL/Takashima, clean `AbhT_1.1` kārikā refs + Jayaratha's Viveka).
- **English reference for validation**: `/root/projects/tantraloka/texts-original/tantraloka-vol{1..11}-dyczkowski.txt`
  (all 11 volumes of Dyczkowski's translation).
- **The crux compass (now wired)**: `pushing_miner.py` reads the 35 pushing-tantraloka LOGICVID sessions
  → 1,510 cruxes + 6,040 claims grounded in kārikās.

**The canonical test (agentgraph's lane — build the machinery):**
1. **Ingest the root** → SOURCE → L0 token floor (vidyut) → TranslationProof → Commentary → Argument.
2. **Translate a flagship āhnika from scratch** (e.g. Āhnika 1, the upāyas — reflexivity, prakāśa/vimarśa,
   the three means, recognition) using our kernels — NOT reading Dyczkowski.
3. **Compile the products** → context bundles → Astro pages → MCP → the full read plane.
4. **Then validate against Dyczkowski** (the comparison, GEM 5.1 three-version method): where our
   from-scratch translation agrees with Dyczkowski = hard core; where it differs = the interpretation
   space the commentary must adjudicate.

**Why Tantrāloka over a sivaqueue target:** it's the intellectual apex (Abhinavagupta's magnum opus), it
has the deepest existing pushing material (`research-library/recognition/pushing-tantraloka/`, 30+
LOGICVID sessions), and it connects the whole organism to recognition (the thesis). The IPVV graduation
proved the mechanism on ONE claim; Tantrāloka proves it on a real, large, philosophically-loaded text.

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

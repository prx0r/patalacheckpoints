# BRAINSTORM — the autonomous Sanskrit ingestion organism (priority queue → coherent factory)

*2026-08-14 · grounded in the OG atlas blueprint (`docs/vision/atlas/atlas-engineering-blueprint.md`) +
the existing sivaqueue/agent3_queue + our LAYERS chain + 37 kernels. This is a DESIGN brainstorm for the
question: "how do we ingest a bunch of untranslated Sanskrit docs in a priority queue, autonomously, and
have it feed through the system populating every data structure/transformation as one coherent organism?"*

---

## THE CORE INSIGHT (from the OG atlas + agent3_queue)

The atlas blueprint says: **"The ingestion pipeline becomes a first-class system."** The agent3_queue
already encodes the loop:

```
CORPUS LEDGER → NEXT_VALID_ACTION → Agent3 → RAW-L0 → AUDIT → COMMIT VERSION → next
```

And we have the pieces to make it an ORGANISM (not a script):
- **`next_action.py`** — CALCULATE what to work on next (deterministic, not LLM-guess): the priority queue.
- **`sivaqueue_targets.py`** — the 100-work priority target registry (period/tradition/term-sense).
- **`source_registry.py`** — every source resolves to rights+health.
- **`vidyut_l0.py`** — the L0 token floor (SLP1).
- **LAYERS chain** — Source → Tokenization → DraftTranslation → Translation → TranslationProof →
  Commentary → Argument → Crux → Synthesis → Essay → Education.
- **The read plane** — context_compiler, bundle_router, seo, MCP.
- **The organism loop** — education/pedagogy/organism (learner probes feed back).
- **`staleness.py`** — a change propagates to every downstream (the reactive spine).

---

## THE DESIGN: the organism is a PRIORITY-DRIVEN REFINERY

```text
                ┌─────────────────────────────────────────────────┐
                │          THE INGESTION ORGANISM                │
                │                                                │
  RAW SANSKRIT  │  PRIORITY QUEUE      THE REFINERY            │  PRODUCTS
  (GRETIL, SARIT│   next_action.py      Source→Tokenization     │  (read plane)
   PANDiT, ...) │   (sivaqueue order)   →Draft→Translation      │
      │         │   + staleness         →Proof→Commentary       │  context bundles
      ▼         │   + learner demand     →Argument→Crux         │  SEO/Astro
  FETCH+RIGHTS  │         │             →Synthesis→Essay        │  MCP
  source_registry│         ▼             →Education             │  snapshots
      │         │  Job → do ONE → verify → commit → next        │
      └─────────┴────────────────────────────────────────────────┘
```

**The one loop that makes it an organism:**

```
1. SENSE   — sivaqueue targets (what exists) + learner probes (what's demanded)
2. PRIORITIZE — next_action.py CALCULATES P(v) = w1·D + w2·B + w3·U + w4·Q + w5·R − w6·C
3. INGEST   — fetch+rights (source_registry), dedupe by sha256
4. REFINE   — run the LAYERS chain (each step a kernel)
5. VERIFY   — integrity_gate + evidence_ledger + verification_ensemble (the immune system)
6. COMMIT   — content-addressed version + staleness blast-radius to downstream
7. SERVE    — compile context bundles → read plane
8. FEEDBACK — learners probe → misconception graph → back to step 2 (re-prioritize)
```

---

## HOW THE PRIORITY QUEUE WORKS (the deterministic scheduler)

Not "pick a random doc." The queue orders work by:
1. **`next_action.py` formula** — downstream load (how much collapses if wrong), betweenness, uncertainty,
   question demand (learner probes), review deficit (staleness), minus cost.
2. **`sivaqueue` order** — the Krama packet first, then tier-1 complete-Sanskrit corpora, then tier-0/2,
   then tier-3 flagships (already the target registry).
3. **Term-context awareness** — each target carries its period/tradition + semantic-shift term senses, so
   the translation picks the CORRECT sense per school (not a flat dictionary).

**The key reframe:** the priority is NOT static. It RE-COMPUTES each cycle because:
- a learner confusion on "vimarśa" raises Q for that passage,
- a source correction raises R (review deficit) for everything downstream,
- a new sivaqueue target raises D (downstream load) for its passages.

**The queue is the organism's attention.** It continuously asks "what is the most load-bearing,
most-contested, most-demanded piece of work right now?" and does exactly one of them, verifies, commits,
and re-asks.

---

## THE DATA STRUCTURES IT POPULATES (all of them, per layer)

| Layer | Data structure | Kernel |
|---|---|---|
| L01 Source | SOURCE objects (rights+health) | `source_registry` |
| L03 | L0 token floor (SLP1) | `vidyut_l0` |
| L03 | TranslationProof vector (non-aggregate) | `translation` |
| L03 | three-version agreement core | `translation_variant` |
| L04 | Argument (AIF) + Crux | `review`, `essay_ingest` |
| L05 | Integrity tri-state + evidence ledger | `integrity_gate`, `evidence_ledger` |
| L06 | Context bundles + cross-source alignments | `context_compiler`, `alignment_flywheel` |
| L07 | SEO pages + MCP tools | `seo`, `bundle_router` |
| L08 | Self-provenance of the whole | `system_provenance` |
| L09 | LearningClaims + misconception graph | `education`, `pedagogy`, `organism` |

Every one of these is a TRANSFORMATION of the previous layer's output — so ingesting one Sanskrit doc
and running it through the chain populates ALL of them, each gated + versioned.

---

## THE COHERENCE (why it's an organism, not a script)

The reason it coheres: **one derivation graph** (the LAYERS chain) is simultaneously:
- the **correctness graph** (a change must propagate down),
- the **staleness graph** (blast-radius on any mutation),
- the **scheduler** (next_action reads downstream load from it),
- the **retrieval graph** (context bundles compile from it),
- the **feedback graph** (learner probes re-prioritize it).

The atlas blueprint said "Postgres = entity truth, R2 = artifact truth, event log = history truth." Our
kernel set realizes that: content-addressed R2 bytes, a derivation DAG, and an event ledger — all feeding
one priority-driven refinery.

---

## WHAT'S ALREADY REAL vs WHAT'S THE BUILD

**Already real (kernels, 75/75):** the whole LAYERS chain (Source→Education), the read plane, the
deterministic scheduler (`next_action`), the priority target registry (`sivaqueue`), the autonomous loop
(`agent3_queue`), the immune system (`integrity_gate`+`evidence_ledger`+`verification_ensemble`), and the
self-proving (`system_provenance`).

**The build (to make it a working organism on real Sanskrit):**
1. **Wire `next_action.py` into `agent3_queue`** — replace the static ordering with the live formula
   (this is THE cohesion point: priority + autonomous loop).
2. **Wire `source_registry` + rights into ingestion** — every fetched doc resolves to rights+health
   before it enters the queue.
3. **Run the LAYERS chain on a real sivaqueue target** (e.g. the Krama packet) end-to-end — one target,
   all data structures populated, all gates pass.
4. **Wire the read plane** so a learner can actually probe → feed the misconception graph → re-prioritize.
5. **Scale the queue** — the 100 sivaqueue targets, each through the chain, each committed + versioned.

---

## THE ONE-LINE BRAINSTORM ANSWER

> **The organism is a priority-driven refinery.** `next_action.py` CALCULATES what to ingest next (from
> sivaqueue priority + downstream load + learner demand + staleness); the LAYERS chain refines each
> Sanskrit doc through every data structure (Source→…→Education), each step gated + content-addressed +
> versioned; staleness propagates every change to downstream; and learner probes feed back to re-prioritize
> the queue. One derivation graph = correctness + staleness + scheduler + retrieval + feedback. That's how
> untranslated Sanskrit docs autonomously flow through and populate everything as a coherent organism.

## Proofs / resolution
- The atlas blueprint: `docs/vision/atlas/atlas-engineering-blueprint.md` (§20 ingestion, §3-6 R2/sha256, §24 three-truths)
- The priority registry: `pipeline/sivaqueue_targets.py` (100 targets, term-context)
- The autonomous loop: `pipeline/agent3_queue.py` (ledger→next→L0→commit→next)
- The chain: `migration/v3/LAYERS.yaml` (Source→Education, requires/produces)
- The scheduler: `lib/next_action.py` (my repo)
- The kernels: `BUILT-BY-LAYER.md` (my repo)

# THE SHARED GOAL — the autonomous organism (ingest → transform → populate, as ONE coherent system)

*2026-08-14 · status: THE NORTH STAR · the shared goal both agentgraph and agentpatala build toward.
The zoom-out: **how do we ingest a batch of untranslated Sanskrit docs in a priority-based queue,
autonomously, and have it feed through the whole organism — populating every data structure and
transformation as one coherent living system.***

---

## THE ONE PICTURE (the autonomous organism)

```text
          ┌────────────── INGEST (the food, priority-ordered) ──────────────┐
          ▼                                                                │
   UNTRANSLATED SANSKRIT (100+ sivaqueue targets, priority-tiered)
          │  acquire: GRETIL / PANDiT / Muktabodha / manuscripts
          ▼  (priority: Krama packet first — lexicon compounds each hop)
   R2 Bronze (immutable, fingerprinted)
          ▼
   SOURCE ──► Tokenization (vidyut_l0) ──► T1 (word gloss)
          ──► Close ──► Reading ──► Commentary       ← the three-layer translation
          ──► TranslationProof (the moat)
          ──► Argument ──► Crux ──► Synthesis
          ▼
   ┌─ THE EPISTEMIC GATE (the immune system) ────────────────────────────────┐
   │  review (herdr) · scholar_review (citecheck) · integrity_gate ·         │
   │  evidence_ledger · verification_ensemble · next_action (the scheduler) │
   └──────────────────────────────────┬──────────────────────────────────────┘
          ▼ projection                 ▼ read plane
   Context bundles ────────► Astro/JSON-LD (humans) · bundles/MCP (agents)
          ▼
   ┌─ THE ORGANISM LOOP (the senses — the flywheel) ─────────────────────────┐
   │  consumers probe → MisconceptionGraph → confusion=research signal       │
   │  → next_action → DeliveryLoop → source-repair → RKA propagate →         │
   │  → better teaching → more learners ──┐                                  │
   └──────────────────────────────────────┼──────────────────────────────────┘
                                          └──► back into the graph
```

**The goal in one line:** *an autonomous pipeline that pulls untranslated Sanskrit into a
priority-ordered queue, ingests each through R2 → Source → translation → proof → argument → review →
synthesis, and populates every data structure (the registry, the atlas, the products, the organism
loop) as ONE coherent organism — with the priority queue deciding WHAT to ingest, next_action deciding
WHAT to work on, and the human gate deciding WHAT becomes canonical.*

---

## THE PIECES (what already exists — the OG atlas machinery)

### 1. THE PRIORITY QUEUE (what to ingest — exists, real)
- **`pipeline/translation_targets.py`** — the master priority registry:
  ```python
  "kramasadbhava":    {"priority": 10, "tier": "1", "status": "TRANSLATE", "tradition": "Kālīkrama"},
  "mahanayaprakasha": {"priority": 11, "tier": "1", "status": "TRANSLATE", "tradition": "Krama"},
  "kubjikamata":      {"priority": 20, "tier": "1", "status": "INGEST",    "tradition": "Kubjikā Kaula"},
  ```
  Priority-ordered by the dialect-genealogy (Krama packet first → lexicon compounds each hop).
- **`pipeline/agent3_queue.py`** — the autonomous driver: `process_next()` picks the next work,
  `--registry`/`--sivaqueue` show the queue, priority-ordered.
- **`pipeline/acquire_sivaqueue_targets.py`** — GRETIL download with verified matches (Kauṇḍinya,
  Kiraṇatantra, Sārdhatriśatikālottara, etc.).
- **The sivaqueue** — 100+ untranslated targets with period/tradition/companion context.

### 2. THE TRANSFORMATION SPINE (what happens to each doc — agentgraph's kernels + mine)
- Tokenization (`vidyut_l0`) → T1 (word gloss) → Close → Reading → Commentary → TranslationProof →
  Argument → Crux → Synthesis. Each a proven kernel (agentgraph) wired into the real pipeline (me).

### 3. THE EPISTEMIC GATE (what becomes canonical)
- review (herdr) + scholar_review (citecheck) + integrity_gate + evidence_ledger + verification_ensemble.
- **next_action** decides what the organism works on next (deterministic, not LLM-guess).

### 4. THE READ PLANE + PRODUCTS (what's served)
- Context bundles → Astro/JSON-LD (humans) · MCP (agents) · the 16 products.

### 5. THE ORGANISM LOOP (the flywheel — the growth)
- consumers probe → MisconceptionGraph → confusion=research signal → source-repair → RKA propagate →
  better teaching. **The closing edge (`misconception.py` repair cascade) is the biggest unbuilt gap.**

---

## THE HONEST GAPS (what blocks the full autonomous organism)

| Gap | Which side | What it is |
|---|---|---|
| **The corpus-wide run** | AGENTPATALA | the priority queue exists, but only ONE claim has been run end-to-end; the full queue → full organism run is the real test |
| **The 3 needs-build products** | AGENTPATALA | Commentary, live Tokenization, Essay projection |
| **`misconception.py` repair cascade** | AGENTGRAPH | the flywheel's closing edge (the organism loop isn't closed) |
| **Live TranslationProof auditors** (xCOMET/MQM) | AGENTGRAPH | the full proof product |
| **Signed attestation** (gap E) | AGENTPATALA | before public authority/marketplace |
| **BKT/FSRS pedagogy policy** | AGENTGRAPH or AGENTPATALA | `next_interaction()` is a weak heuristic |

---

## THE SHARED GOAL (the north star — what BOTH sides build toward)

> **A fully autonomous organism:** a priority-ordered queue of untranslated Sanskrit docs is ingested
> (R2 → Source → translation → proof → argument → synthesis), gated by the epistemic immune system,
> served as products, and closed into a self-improving loop where learner confusion repairs the source —
> **all as ONE coherent system where the priority queue decides what to ingest, next_action decides what
> to work on, and the human gate decides what becomes canonical.**

**The test of the goal:** run the ENTIRE priority queue (or a real batch) end-to-end — every doc through
the full spine, populating the registry, the atlas, the products, and the organism loop — and watch a
source mutation propagate correctly. That's the corpus-wide graduation. **That is what makes it a real
organism, not a pile of kernels.**

---

## THE DIVISION (how we get there)

- **AGENTGRAPH** builds the missing kernels (misconception.py, the live auditors, the BKT/FSRS policy).
- **AGENTPATALA** wires the existing queue + kernels into the real pipeline, runs the corpus-wide
  graduation, and ships the products.

**The priority-queue → full-organism run is agentpatala's headline task.** The queue, the spine, the
gate, the read plane all exist — the work is connecting them end-to-end on real data and closing the
organism loop.

---

*This is the shared goal. The OG atlas machinery (the priority queue, the sivaqueue, the autonomous
driver) is real and sophisticated — the question is feeding it through the whole organism. Both sides
build toward that: agentgraph the missing kernels, agentpatala the corpus-wide autonomous run that makes
it one coherent living system.*

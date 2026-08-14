# migration/v2 — the Pāṭala v2 coherent-system spec

> ## 🔴 ARCHIVED / SUPERSEDED
> **This is the v2 design blueprint (proposed/speculative). It is SUPERSEDED by `migration/v3/` — the
> current, proven organism. Read `v3/README.md` first. This folder is kept for history/context only.**


*The canonical blueprint for a clean, clear, agent-usable Pāṭala. The scholarship pipeline stays; the
names get clear, the layers get codified, and every store derives from one graph.*

---

## THE HIERARCHY — how migration/v2 is organised

There are **four concentric layers** of the v2 package. Read them in this order — each unlocks the next.

```text
LEVEL 0  WHY we exist            migration/README.md  +  strategy/
LEVEL 1  WHAT the system IS      PATALA-V2-SPEC.md    (the architecture)
LEVEL 2  WHAT exists / maps to   LAYERS.yaml · LAYER-MAPPING.md · MODULES.md
LEVEL 3  CURRENT → VISION        CURRENT-TO-VISION.md (the synthesis + build order)
LEVEL 4  HOW to build            GROUND-UP-PLAN.md
LEVEL 5  The great prose         goated/  (read when you want the depth)
```

---

## HOW A NEW AGENT SHOULD FIRST READ IT (the exact order)

**Read these in order. Skipping one means you miss the context it unlocks.**

### Step 0 — orientation: `migration/README.md` then `strategy/README.md`
- `migration/README.md` — what the whole `migration/` folder is for.
- `strategy/README.md` — the two sub-docs it contains.

### Step 1 — the WHY (strategy): `strategy/STRATEGIC-DOSSIER.md`
- The thesis, ecosystem position, economics, partnerships. **This narrows the scope** — it tells you
  what Pāṭala is and is NOT, which decides everything downstream.
- Then `strategy/PRODUCTS.md` (the 16-product catalog) + `strategy/PRODUCTS-VISIONS.md` (implemented vs
  visionary, each product ↔ its vision).
- **Do this first:** you can't judge the architecture until you know what Pāṭala is for.

### Step 2 — the architecture: `PATALA-V2-SPEC.md`
- The rename map, the kernel, the transformation registry, the stores, the execution model, the 3
  planes, the build sequence. This is the *shape* of v2.

### Step 3 — the ground truth: `LAYERS.yaml` + `LAYER-MAPPING.md` + `MODULES.md` + `EXTERNAL-EVIDENCE.md`
- `LAYERS.yaml` — the machine contract (12 layers, 12 transformations) — the spine.
- `LAYER-MAPPING.md` — every layer → name · mechanism (real files) · process · needs · relations ·
  vision · checkpoint.
- `MODULES.md` — every reusable module tagged `[REUSE]`/`[PARTIAL]`/`[GOLD-IPVV]`/`[NEW]` + the full
  lifecycle + the `[NEW]` gaps list.
- `EXTERNAL-EVIDENCE.md` — every layer grounded in external literature + GitHub repos (what to pinch vs
  own; the moat list). **This is what makes migration the FINAL version** — no design is invented in a vacuum.
- `EXTERNAL-REPOS.md` — the COMPLETE external repository map (every repo → layer/product · status),
  incl. the deep translation subsystem (fojin, MITRA, Mitrasamgraha, ByT5, COMET) and the "don't build" boundary.
- **Read these when you need to DO something** — they point at the actual machinery + the external support.

### Step 4 — the synthesis: `CURRENT-TO-VISION.md`
- For every mechanism: current state → vision state · why · how · integration · gap. **The build order
  emerges from the gaps here.** This is the honest "what's real vs what v2 will be."

### Step 5 — the plan: `GROUND-UP-PLAN.md`
- The literal bottom-up build (thesis → scope → harvest → transform → products). The refinery model.

### Step 6 — the depth (optional): `goated/README.md`
- The curated best standalone documents (philosophy-engine set, doctrine, IPVV/prima-materia, global
  architecture, Hermes, strategy, vision). Read when you want the full intellectual depth.

---

## THE FILE MAP (quick reference)

| File | Level | What it is | Read when |
|---|---|---|---|
| `strategy/STRATEGIC-DOSSIER.md` | 1 | thesis · ecosystem · economics · partnerships · go-to-market | orienting (what Pāṭala IS) |
| `strategy/PRODUCTS.md` | 1 | the 16-product catalog (artifact + checkpoint + layer + vision) | productizing |
| `strategy/PRODUCTS-VISIONS.md` | 1 | implemented vs visionary + every vision → product | knowing what's real |
| `PATALA-V2-SPEC.md` | 2 | the architecture (rename, kernel, registry, stores, 3 planes) | the shape of v2 |
| `LAYERS.yaml` | 3 | the machine contract (12 layers, 12 transformations) | the spine |
| `LAYER-MAPPING.md` | 3 | every layer → mechanism/process/vision/checkpoint | navigating a layer |
| `MODULES.md` | 3 | every module tagged + lifecycle + [NEW] gaps | what to reuse / build |
| `CURRENT-TO-VISION.md` | 4 | current → vision · why · how · gap; build order | deciding what's next |
| `EXTERNAL-EVIDENCE.md` | 3 | every layer grounded in external literature + GitHub repos (what to pinch vs own); the moat list; the complete clone/pinch list | validating a layer's design |
| `EXTERNAL-REPOS.md` | 3 | the COMPLETE external repository map (every repo → layer/product · what to pinch · status) — incl. the deep translation subsystem (fojin, MITRA, Mitrasamgraha, ByT5, COMET) and the "don't build" boundary | finding what's already solved |
| `GROUND-UP-PLAN.md` | 4 | the bottom-up build (harvest → refine → products) | the plan |
| `CONVERGENCE-OCHEMA.md` | 4 | the convergence map: Pāṭala ↔ the Ochema Workstation (.meta) — the render engine, writer, publish layer, and source organiser are ALREADY BUILT (DO NOT REBUILD); Pāṭala owns the epistemic gate | the convergence |
| `GEMS.md` | 5 | the distilled insights per layer (the "aha" layer) — each gem: the insight · why · detailed note | thinking |
| `renderr.md` | 5 | the Renderio insight (imported from R2) — the Pāṭala → Library → Renderio three-way split + the 2026 video frontier | media layer |
| `goated/README.md` | 5 | the best standalone prose (curated index) | depth |

---

## The core idea (one line)

> One event-sourced kernel + one derivation graph + clear names + compiled projections. Docs and the
> site become projections of state, not separate truths.

## The rename (code → clear)

- `T1` → `DraftTranslation` · `L0` → `Tokenization` · `ARGMAP` → `ArgumentOutline`
- `L2` → `Translation` · `L200` → `TranslationProof` · `C1` → `Commentary`
- `THEME` → `Theme` · `EDUCATION` → `Lesson` (SYNTHESIS/ARGUMENT/ESSAY keep their names)

Micro-stages `T1→R1→T2→R2→T3→T3.1→C1` unify onto the same vocabulary:
`DraftTranslation → DraftReview → AlternativeTranslation → Adjudication → FinalTranslation →
FinalProof → Commentary`.

## Why it matters

- **Clear names** → an agent reads the name and knows what it does + where it sits. No lookup.
- **One codified spec** → replaces the 19 hand-maintained "Layer 3 is PARTIAL" docs with a generated
  projection. Status can't drift (it's derived from the live registry).
- **One graph** → the derivation DAG is simultaneously correctness, staleness, scheduler, and retrieval.
  That's the biggest lever.

## Next concrete step (recommended)

1. Read `CURRENT-TO-VISION.md` for the build order that falls out of the gaps.
2. The single highest-value next build: **the L200 + C1 gold ingest** (63+63 golds → registry with
   derivation edges) — it makes the TranslationProof moat real and unblocks Synthesis/Essay/Lesson.
   Follow the proven `ingest_ipvv_argmap_golds.py` pattern.
3. Do NOT implement the kernel / projection-compiler until the gold is real.

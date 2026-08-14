# THE GLOBAL VISION → CHUNKS → LAYERS MAP (deterministic, top-down)

*2026-08-14. THE way the whole vision decomposes. Read from the top down: **ONE global vision → a fixed
set of CHUNKS → each chunk lands deterministically on ONE Layer → and the Layer (via `NAVIGATION.md`) is
where you find the implementation, tools, docs, and live state.** No "2 agents" — progress is tracked
PER LAYER in the layer page's "current state" slot.*

> **The direction:** this file goes **vision-first** (top-down). `NAVIGATION.md` goes **implementation-first**
> (bottom-up). They meet at the LAYER — the deterministic anchor where a vision chunk becomes buildable and
> its state is tracked. `handover/STATE.yaml` is the live tracker; each layer page renders its own live state.

---

## THE ONE GLOBAL VISION

> **Pāṭala is a computable scholarly tradition: one evidence graph from Sanskrit source to scholarship to
> understanding, where every claim resolves to its source, and machines propose while scholars certify.**

That is the single vision. Everything else is a chunk of it.

---

## THE CHUNKS (each is a distinct part of the one vision)

The vision decomposes into **8 distinct chunks** (the categories). Each chunk is deterministic: it builds
ONE Layer.

```
GLOBAL VISION
   └─ CHUNK 1  Foundations      ──►  Layer 00  Governance
   └─ CHUNK 2  The Corpus       ──►  Layer 01  Ingestion
   └─ CHUNK 3  The Atlas        ──►  Layer 02  Atlas
   └─ CHUNK 4  The Factory      ──►  Layer 03  Factory
   └─ CHUNK 5  The Epistemic    ──►  Layer 05  Research (MOAT)
   └─ CHUNK 6  The Scholars     ──►  Layer 08  Human Authority
   └─ CHUNK 7  The Organism     ──►  Layer 09  Organism
   └─ CHUNK 8  The Surfaces     ──►  Layer 10  Surfaces
   └─ CHUNK 9  The Economics    ──►  Layer 11  Org & Economics
   └─ CHUNK 10 The Live System  ──►  Layer 12  Live System
```

---

## THE DETERMINISTIC CHUNK → LAYER MAP

| Chunk | The vision chunk | Lands on Layer | What the Layer is | Progress tracked where |
|---|---|---|---|---|
| **1 Foundations** | the one-vision map, the anti-theatre rule | **00 Governance** | the constitution + operating axioms | `00-governance.md` live state |
| **2 The Corpus** | sources → canonical objects (Śiva corpus, ingestion) | **01 Ingestion** | the intake engine + adapters | `01-ingestion.md` live state |
| **3 The Atlas** | the research graph, identity, manuscripts | **02 Atlas** | the canonical graph + storage | `02-atlas.md` live state |
| **4 The Factory** | the compiler SOURCE→C1 | **03 Factory** | the DAG + workers + registry | `03-factory.md` live state |
| **5 The Epistemic** | propositions→arguments→cruxes→synthesis→essay/education | **05 Research** | the epistemic core (the moat) | `05-research.md` live state |
| **6 The Scholars** | review, workbench, attestation | **08 Human Authority** | review / adjudication / supersession | `08-human-authority.md` live state |
| **7 The Organism** | the human-understanding graph, media, adaptive learning | **09 Organism** | the Q moat variable | `09-organism.md` live state |
| **8 The Surfaces** | the sites, APIs, MCP, products | **10 Surfaces** | the read surfaces | `10-surfaces.md` live state |
| **9 The Economics** | scholar credit, market, partnerships | **11 Org & Economics** | the human + economic layer | `11-org-economics.md` live state |
| **10 The Live System** | how agents/state/docs stay in sync | **12 Live System** | the orchestration + projection | `12-live-system.md` live state |

*(Layers 04 Evidence and 06 Commentarial, 07 Verification are cross-cutting substrates, not standalone
chunks — they serve every chunk.)*

---

## THE DETERMINISTIC FLOW (how a vision chunk becomes buildable)

```text
VISION CHUNK            LAYER              NAVIGATION              PROGRESS
   (this map)      docs/layers/NN-*.md   resolves impl/tools      layer page "current state"
       └─►   └─►            └─►  live state via handover/STATE.yaml (flow.py)
```

An agent does this:
```text
1. Pick a VISION CHUNK (1-10) from this map.
2. GO TO its Layer page (docs/layers/NN-*.md) — that is its deterministic home.
3. NAVIGATION.md resolves the implementation + tools + docs for that layer.
4. READ the layer's "current state" slot — that's the live progress.
5. ADVANCE the work → update the layer's state (via STATE.yaml / flow.py).
```

**The honesty rule:** a layer's state is only advanced when its gate is genuinely met (gold + blind eval +
human adjudication), per the anti-theatre doctrine.

---

## THE MACHINE-RESOLVABLE FORM (VISION-CHUNKS.json)

```json
{
  "global_vision": "computable scholarly tradition: one evidence graph, every claim resolves, machines propose scholars certify",
  "chunks": [
    {"chunk":1, "name":"Foundations",  "layer":"00", "doc":"docs/layers/00-governance.md"},
    {"chunk":2, "name":"The Corpus",   "layer":"01", "doc":"docs/layers/01-ingestion.md"},
    {"chunk":3, "name":"The Atlas",    "layer":"02", "doc":"docs/layers/02-atlas.md"},
    {"chunk":4, "name":"The Factory",  "layer":"03", "doc":"docs/layers/03-factory.md"},
    {"chunk":5, "name":"The Epistemic","layer":"05", "doc":"docs/layers/05-research.md"},
    {"chunk":6, "name":"The Scholars", "layer":"08", "doc":"docs/layers/08-human-authority.md"},
    {"chunk":7, "name":"The Organism", "layer":"09", "doc":"docs/layers/09-organism.md"},
    {"chunk":8, "name":"The Surfaces", "layer":"10", "doc":"docs/layers/10-surfaces.md"},
    {"chunk":9, "name":"The Economics","layer":"11", "doc":"docs/layers/11-org-economics.md"},
    {"chunk":10,"name":"The Live System","layer":"12","doc":"docs/layers/12-live-system.md"}
  ],
  "deterministic": "each chunk builds exactly ONE layer; progress tracked per-layer via STATE.yaml"
}
```

---

## HOW IT MEETS NAVIGATION (the two directions, one anchor)

```text
TOP-DOWN (this file):      GLOBAL VISION → 10 CHUNKS → each → ONE LAYER
BOTTOM-UP (NAVIGATION.md): any file/tool → resolve → ONE LAYER → its impl/docs/state
                              ↓  both meet at the LAYER  ↓
                    docs/layers/NN-*.md  =  the deterministic anchor
```

The vision is chunked top-down into layers; navigation resolves bottom-up back to layers. They agree at
the layer page — the single place where "what this vision chunk needs" and "what this layer implements"
are the same thing. Progress is tracked per-layer, deterministically, in `handover/STATE.yaml`.

---

*This supersedes the earlier "2-agent / CP-checkpoint" framing. The vision decomposes into layers, not
agents; agents execute work within a layer, and progress is a layer property. See `docs/vision/REVIEWS.md`
for every vision doc's role, and `NAVIGATION.md` to resolve any layer to its implementation.*

# WHAT TO BUILD — THE FULL INGESTION + STATE MACHINE (filling ip-graph's gaps)

*2026-08-14 · status: BUILD DIRECTIVE for agentgraph + agentpatala · the precise "what to build and why"
for the pieces ip-graph is missing, using what OG patala already has. This is the shared-build spec for
the full autonomous ingestion — from external sources (R2) through the per-work factory state machine to
the compiled graph the site serves.*

---

## THE GAP (what ip-graph is missing vs what OG patala has)

| Concern | OG patala HAS | ip-graph LACKS | Why it matters |
|---|---|---|---|
| External-source harvest (PANDiT/GRETIL/SARIT/MSS) | ✅ `ingestion/adapters/*.py` → R2 | ❌ (its corpus is Doyle/science) | the real Sanskrit input |
| Bibliography (254 works) | ✅ `atlas-bibliography.json` (Postgres) | ❌ | the identity graph |
| Translation-state ledger (which works have T1/T3) | ✅ `corpus_state.py` → `translation-state-ledger.json` (111 works) | ❌ | per-work autonomy |
| Per-work factory state machine | ✅ `next_valid_action(work)` | ❌ | the control plane |
| The real translated corpus | ✅ 71 jsonl + 11 T3 finals | ❌ | the scholarly state |
| The modern kernels + read plane | ❌ (legacy factory) | ✅ 37 kernels + Astro site | the machinery |

**The thesis:** ip-graph has the MODERN MACHINERY; OG patala has the REAL DATA PIPELINE. The shared build
wires them together.

---

## WHAT TO BUILD (in order, with why)

### 1. THE FULL INGESTION — external sources → SOURCE objects

**What:** wire the real harvest adapters (PANDiT/GRETIL/SARIT/MSS, all in `ingestion/adapters/`) into the
factory's SOURCE intake, so real untranslated Sanskrit flows from R2 → object_registry.

**Why:** ip-graph's `ingestion_organism` is the loop design, but it has no real Sanskrit input. OG patala's
adapters are the real harvest machinery. They must be wired together.

**Build:**
- R2 (the external buckets: patala, sourcematerial, atlas-sources) → the adapters (`pandit.py`, `gretil.py`,
  `sarit.py`) → rights-gated (CC BY-NC-SA for PANDiT) → content-addressed SOURCE objects in `object_registry`.
- `ingestion_organism` calls the real adapters instead of a hand-fed `SanskritDoc`.

### 2. THE BIBLIOGRAPHY ↔ SOURCE IDENTITY LINK

**What:** make the 254 bibliography works resolve to their SOURCE objects. The bibliography's `id`
(e.g. `malinivijayottara`) maps to the registry's SOURCE objects via the `bibliographic_id` (already in
the state ledger).

**Why:** this is the "OpenAlex for Sanskrit" core — the thesis's central value. Without it, the bibliography
is isolated from the factory.

**Build:** the identity resolver: `bibliographic_id` ↔ SOURCE objects ↔ the graph. Every SOURCE object
carries its bibliographic_id; the bibliography carries its factory state.

### 3. THE PER-WORK FACTORY STATE MACHINE (the autonomous control plane)

**What:** OG patala's `corpus_state.py` — `next_valid_action(work)` — tracks each of 111 works through its
translation lifecycle (LEGACY_T1_PRESENT → MODERNIZE_L0 → ... → COMPLETE). This is the autonomous factory
state machine.

**Why:** ip-graph's `next_action.py` is a priority *scheduler* (WHAT to work on); OG patala's
`corpus_state.py` is the per-work *state machine* (WHAT transition is valid next). Both are needed:
`next_action` picks the work, `next_valid_action` picks the transition.

**Build:** wire `corpus_state.next_valid_action()` into `ingestion_organism`'s loop — so each work advances
through its legal transitions autonomously, gated by the review + integrity kernels.

### 4. THE COMPILE BRIDGE — canonical objects → ip-graph's graph → the site

**What:** the factory's committed objects flow into ip-graph's `graph.json`/`concepts.jsonl` that the Astro
site serves.

**Why:** right now the factory writes to OG's `object_registry`, but ip-graph's site reads `graph.json`.
They're disconnected. The bridge makes the factory output visible on the site.

**Build:** extend `build_stk_graph.py` to ALL works — a compiler that takes the real ledger objects →
ip-graph's graph format → their `build-static-site.py` → the site.

---

## THE ONE-LINE ARCHITECTURE

> **R2 (external tools: PANDiT/GRETIL/SARIT) → object_registry (SOURCE, the factory's truth) → the per-work
> state machine (next_valid_action, autonomous) → ip-graph's graph.json (the compiled projection) → Astro
> site (the read plane)** — with the bibliography as the identity layer (254 works ↔ their sources ↔ their
> factory state), and Hermes as the execution kernel throughout.

---

## THE BUILD DIVISION

| Build | Who |
|---|---|
| Wire the R2 adapters → SOURCE (real harvest) | agentgraph (source_registry) + agentpatala (adapters exist) |
| The bibliography ↔ SOURCE identity link | agentpatala (bibliography + registry are OG) |
| The per-work state machine (corpus_state → the organism) | agentpatala (has corpus_state) + agentgraph (next_action) |
| The compile bridge (ledger → graph.json → site) | both (agentgraph's build-static-site + agentpatala's data) |

---

## WHY THIS ORDER

1. **Ingestion first** — no point compiling a graph if no real Sanskrit flows in.
2. **Identity link second** — the bibliography is the spine the whole graph hangs on.
3. **State machine third** — autonomy needs the per-work transitions, not just the scheduler.
4. **Compile bridge fourth** — only once the data flows do we render it on the site.

*This is the shared-build directive. ip-graph brings the modern kernels + read plane; OG patala brings the
real Sanskrit harvest, the bibliography, the translation-state, and the per-work factory state machine. The
build wires them into ONE autonomous organism.*

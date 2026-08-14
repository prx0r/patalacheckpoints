# PĀṬALA V3 — THE STRUCTURE REMAKE (brainstorm: AGENTS · layers · docs · live updates · agentic system)

*2026-08-14 · status: BRAINSTORM (not yet implemented) · how to remake the Pāṭala structure around the
ACTUAL final build. The current AGENTS.md / NAVIGATION / layer pages / agent system were written when v1
was the reality. Now we have v3 (proven kernels + production organism + complete thesis). This doc is the
design for the remake — and it contains the FULL THESIS.*
*The key shift: the old structure organized around the DAG (SOURCE→…→C1→…→Lesson). The v3 structure
organizes around the ORGANISM (the verified epistemic OS) — the SAME layers, but as organs of one
system, with the proven machinery as the substrate.*

---

## PART 1 — THE FULL THESIS (the foundation everything is built on)

> **Pāṭala is a proof-carrying scholarly compiler for the Sanskrit intellectual record.** It harvests raw
> tantric/Sanskrit material from the fragmented ecosystem (PANDiT, Muktabodha, IFP, NGMCP, GRETIL, SARIT,
> manuscripts), refines it layer by layer into evidence-backed scholarly objects, gates them by
> deterministic review + human adjudication, and projects them into products for scholars, readers, and
> machines — every output retaining a machine-traversable proof path back to its source and review history.

**Position:** *"OpenAlex for Sanskrit"* — not an archive, library, or translation publisher, but the
**connective / reconciliation / identity layer** that resolves the fragmented ecosystem onto one canonical
ID, preserving every custodian as the authoritative source.

**The moat:** NOT the data (commoditized) and NOT the AI (commoditized) — the **verified, provenance-
preserving scholarly substrate**: the TranslationProof vector, the review-gated claims, the human-
correction corpus, the derivation graph. Everything increasingly powerful AI must *trust*.

**The three truths:**
1. **Pāṭala decides what can responsibly be said.** (the epistemic gate)
2. **The Library decides what is worth communicating.** (the production organism)
3. **Renderio decides how it should be seen.** (the media layer)

**The three laws:**
```text
TRUTH     Nothing becomes true because an agent says so.   (the epistemic gate)
COMPILE   Nothing recomputes unless its dependencies changed. (the staleness DAG)
READ      Nothing computes at request time if bytes could already exist. (the read plane)
```

**The anti-theatre rule (the immune system):** nothing is real without gold + blind eval + metric +
human adjudication. The graduation test is its enforcement.

---

## PART 2 — THE NEW STRUCTURE (the remake)

The current structure (AGENTS.md → NAVIGATION → layers → docs → live updates) is right in SHAPE but
wrong in GROUNDING: it describes a v1 system. The remake keeps the shape, re-grounds it in v3.

### 2.1 THE NEW AGENTS.md (the governing file, re-grounded)

**The key change:** the old A0-A7 agent architecture (governance → philosophy → corpus → translation →
review → synthesis → publication → scholar) was a DAG-shaped organization. The v3 remake organizes by
the ORGANISM'S five systems. The agents become the nervous-system workers, not the architecture.

```text
                    AGENT 0  (the nervous system — governance/routing/infra)
                       │
          ┌────────────┼────────────┬────────────┬────────────┐
          ▼            ▼            ▼            ▼            ▼
        AGENT 1     AGENT 2      AGENT 3      AGENT 4      AGENT 5
       SATELLITE   FACTORY      REASONER     REVIEWER     PRODUCER
       (identity/  (refine:     (argument/   (the gate:   (.meta:
       atlas/      the spine    crux/        anti-        essay→render
       harvest)    + staleness) synthesis)   groupthink)  →publish)
```

- **A0 Nervous System** — governance, routing, the doctrine. (was A0)
- **A1 Satellite** — harvest + identity (adapters → R2 → SOURCE; the Atlas). (was A1+the atlas)
- **A2 Factory** — the refine process (Source→Commentary via the transformation registry + staleness).
  (was A2+A3 merged — translation IS part of the factory)
- **A3 Reasoner** — argument, crux, synthesis. (was A5)
- **A4 Reviewer** — the gate (anti-groupthink panel, CiteCheck, human publication). (was A4)
- **A5 Producer** — the production organism (.meta: essay→render→publish→sites). (was A6+A7)

**The shift:** agents are WORKERS in the organism's systems, not the organizing structure. The structure
is the 5 organ-systems (nervous/skeleton/digestive/reproductive/sensory); agents fill roles within them.

### 2.2 THE NEW LAYER PAGES (the layers leading to the docs)

The old layer pages (00-governance → 12-live-system) become the **organ pages** — same layers, but each
renders its LIVE state from the proven machinery, not from hand-written status.

**The new layer structure (13 pages, re-grounded):**
```text
00  GOVERNANCE        the doctrine + the thesis (the immune system)
01  SATELLITE/INGEST  harvest + identity (was 01-ingestion + 02-atlas)
02  ATLAS/IDENTITY    the authority graph (merged into the identity foundation)
03  FACTORY           the refine process + transformation registry (was 03)
04  EVIDENCE          the contracts + external tools (was 04)
05  SPINE             Source→TranslationProof→Commentary (was 05 research)
06  ARGUMENT          the reasoner (was 06 commentarial)
07  VERIFICATION      the eval plane + the 5 golds (was 07)
08  SCHOLAR           review + attestation (was 08 human-authority)
09  ORGANISM          the consumer loop (was 09)
10  SURFACES          the products (was 10)
11  ECONOMICS         the org (was 11)
12  LIVE SYSTEM       the orchestration (was 12)
```

**Each page renders** from `docs_state.py` + the proven kernels: status is DERIVED (PROVEN /
PROVEN-MECHANISM / NEEDS-BUILD), the mechanism is named (the lib/ kernel + its test), the external tool
is listed, the traceability resolves.

### 2.3 THE NEW DOCS TREE (the layers leading to the docs)

The docs become **projections of state** (the v2 principle, now real):
```text
migration/v3/  ← THE BLUEPRINT (the organism, mechanisms, products, structures, traceability)
  ├─ PATALA-V3-ORGANISM.md    the organism (the 5 systems)
  ├─ V3-BUILD-SPEC.md         the exact build (stack, tools, STEP 0-8)
  ├─ LAYERS.yaml              the proven layer contract
  ├─ PRODUCTS.md              the 16 products (13 proven)
  ├─ MECHANISMS.md            the 5 load-bearing mechanisms
  ├─ STRUCTURES.md            the definitive structures
  ├─ PATALA-NATIVE-MACHINERY.md  the Patala domain code
  ├─ LEGACY-GEMS.md           the genius ideas from the old docs
  └─ TRACEABILITY.md          every reference → full path
```

**The live docs** (generated, not hand-written):
```text
CURRENT_STATE.md   ← rendered from docs_state.py + the live registry
NAVIGATION.md      ← the resolver (re-grounded to v3)
AGENTS.md          ← the governing file (re-grounded to the organism)
layer pages        ← rendered from LAYERS.yaml + the live registry
```

**The rule:** status is a PROJECTION (rendered from the registry/kernels), never a hand-written claim.

### 2.4 THE LIVE UPDATES (how the state stays current)

The live-update system (from the v2/lab):
- **The ledger** (ObjectEvent append-only) is the truth source.
- **The reducer** projects ledger → current state → Postgres.
- **`docs_state.py`** renders the state → the docs (CURRENT_STATE, layer pages).
- **Staleness** flags what changed → what needs regenerating.
- **The projection compiler** renders the read plane (HTML/JSON/Context Bundles).

**The live-update loop:**
```text
ObjectEvent (ledger) → reducer → Postgres → docs_state → CURRENT_STATE.md + layer pages
        ↑                                                     │
        └──────── consumer/scholar action ◄── site ◄── projection compiler
```

### 2.5 THE AGENTIC SYSTEM (Hermes as the nervous system)

- **Hermes** is the execution runtime (kanban, profiles, skills, MCP). Pāṭala decides; Hermes runs.
- **The `patala_*` MCP verbs** let agents drive Pāṭala: `patala_next_action` · `patala_get_work_state` ·
  `patala_propose_translation` (PROPOSE, never ACCEPT).
- **Task ≠ Run ≠ Event** — a task's run history is gold (Run 1 failed → Run 2 candidate → …).
- **The human publication gate** — agents propose, humans accept. Enforced at the verb level.

---

## PART 3 — HOW WE DO THE REMAKE (the build order)

### STEP 1 — Lock the thesis (this doc, PART 1)
Put the full thesis at the top of AGENTS.md. It's the filter everything follows.

### STEP 2 — Re-ground AGENTS.md (PART 2.1)
Replace the A0-A7 DAG-organization with the 5-organ-system agent structure. Agents become workers.

### STEP 3 — Re-ground NAVIGATION + the layer pages (PART 2.2)
The 13 layer pages render from LAYERS.yaml + the live registry. Status is derived, not hand-written.

### STEP 4 — Wire the live updates (PART 2.4)
Ledger → reducer → Postgres → docs_state → generated docs. Kill hand-maintained status.

### STEP 5 — Wire the agentic system (PART 2.5)
The `patala_*` MCP verbs + Hermes profiles + the human gate.

### STEP 6 — The graduation test
One IPVV claim through the whole stack — this is what makes the whole structure REAL, not just designed.

---

## PART 4 — THE ONE-LINE CARRY-FORWARD

> **Remake the Pāṭala structure around the organism: AGENTS.md re-grounds to the 5 organ-systems (agents
> become workers, not the architecture); the 13 layer pages render from the proven LAYERS.yaml + the live
> registry; the docs become projections of state; the live-update loop runs ledger→reducer→Postgres→docs;
> Hermes executes via the patala_* verbs behind the human gate — all anchored by the full thesis and made
> real by the graduation test.**

---

*This is the v3 structure-remake brainstorm, with the full thesis. The shape of the current structure
(AGENTS → NAVIGATION → layers → docs → live updates → agentic) is right; the GROUNDING was v1. The remake
re-grounds it in v3: the organism (5 systems), the proven kernels, the production organism, and the
complete thesis. The graduation test is what makes the rebuilt structure real rather than designed.*

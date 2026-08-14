# THE LAYER-BY-LAYER RECONCILIATION — built vs. borrowed vs. agentic

*2026-08-14. For EVERY layer: what Pāṭala has ALREADY built (Pāṭala-native), what the GitHub/external
ecosystem offers to borrow, and what remains to be built for the agentic system (Layer 12). The honest
answer to "have we already built this ourselves?" — for the epistemic core, **yes, we largely have.***

> **The one-line finding:** our epistemic core (Layers 02-08) is largely BUILT and Pāṭala-native — the
> external repos we researched mostly re-invent what we already have. **The real new work is the
> orchestration layer (Layer 12): Hermes profiles, the projection/staleness engines, the `patala_*`
> capability verbs, run/attempt/lease, and `patala_next_action()` triage.**

---

## THE RECONCILIATION (layer by layer)

| Layer | Pāṭala BUILT (native) | External/GitHub to borrow | Remaining AGENTIC work |
|---|---|---|---|
| **00 Governance** | `AGENTS.md`, `AGENTS-DOCTRINE.md`, `theatre_check.py`, `contracts/CANONICAL-DAG.yaml` | Hermes `/goal` + quality gates (deterministic "done") | add the operating axioms + coding-agent contract to AGENTS.md |
| **01 Ingestion** | `ingestion/` (SourceAsserter, AtlasWriter, SnapshotStore, 8 adapters), R2 Bronze | Docling (+MCP), GROBID, Zotero Translation Server, S2ORC doc2json (normalization) | — (built) |
| **02 Atlas** | Postgres 22-table schema, resolver, API, crosswalk, deterministic UUID | OpenAlex/Crossref (identity) | — (built) |
| **03 Factory** | workers (t1-l200-c1), `object_registry` (versioned + event ledger), scheduler, DAG | Hermes kanban/cron/worktree (execution) | wire the live `factory_loop` + the 3 Hermes profiles |
| **04 Evidence** | contracts (external_record, derived_scholarly_object, source_evidence_profile), 69 tools documented | (already documented in `external-tools.md`) | — (built) |
| **05 Research (MOAT)** | propositions/arguments/cruxes/synthesis, essay/education compilers, golds | DSPy (optimize extraction vs gold), AIF/xAIF adapters | ARGUMENT/SYNTHESIS real workers (declared but empty) |
| **06 Commentarial** | design only (`06-commentarial-graph.md`) | **Vouch** (review-gate — we have this), SocraticKG (QA-extraction), Docling (substrate), instagraph/seventeen-centuries (KG candidates) | the paper→ScholarContributionPacket compiler |
| **07 Verification** | eval plane (Inspect, NAT, golds), the 10 self-tests | RARR/RefChecker/GraphCheck (claim checking) | — (built) |
| **08 Human Authority** | **`review_engine.py` (ReviewEvent ledger + impact_report), `contracts_human_authority.py`** | Vouch, INCEpTION (gold lab), Recogito (annotation) | scholar workbench UI |
| **09 Organism** | design only (`09-organism.md`) | Graphiti (temporal graph), pyBKT/Dialogue-KT (learner), adaptive-kg (interfaces), DeepTutor (memory) | the human-understanding graph + learner model |
| **10 Surfaces** | `app/` (Next.js), `mcp/`, `openpatala/`, Astro | Mirador 4 (manuscripts), Remotion/OpenMontage (media), Postiz (distribution) | the media organism (13) |
| **11 Org/Economics** | `AGENTS.md`, partnership/access docs | ORCID/CRediT, Postiz Agent | — (documented) |
| **12 LIVE SYSTEM** | **Tier-1 truth (object_registry, corpus_state, review_engine, event ledger)** | Hermes (kanban/goals/hooks), Agetor (Task≠Run), Beads Viewer (triage), mcp_agent_mail (leases) | **THE 7 PIECES** (projection, staleness, MCP verbs, run/attempt/lease, triage, profiles, coding-agent contract) |

---

## THE HONEST GAP — what we actually need to build vs. what's done

### ✅ ALREADY BUILT (Pāṭala-native — do NOT re-borrow)
- ReviewEvent ledger + impact propagation (`review_engine.py`) — **the Vouch equivalent, done better**
- Versioned objects + immutable versions + event ledger (`object_registry.py`)
- Epistemic contracts (all of `source-evidence/schema/`)
- The 62 external tools documented + the eval plane

### ⚠️ PARTIALLY BUILT (needs wiring, not greenfield)
- ARGUMENT/SYNTHESIS workers (declared in DAG, 0 objects)
- THEME/ESSAY/EDUCATION reachable via the live factory loop
- The 3 Hermes profiles (only `patala` exists)
- STATE.yaml → projection (currently hand-maintained)

### ❌ THE REAL AGENTIC BUILD (Layer 12, Pieces 1-7)
1. Projection engine (`docs_state` → docs/JSON/API/scholar views)
2. Staleness/provenance engine (deterministic CURRENT/STALE/UNKNOWN)
3. Capability MCP (`patala_*` domain verbs)
4. Task≠Run≠Attempt + leases
5. Observer/triage (`patala_next_action()`)
6. The 3 Hermes profiles + kanban board + skill pack
7. Coding-agent lane contract (AGENTS.md)

---

## THE RECONCILIATION RULE

> **For each layer: (1) if Pāṭala already built it natively, use it — don't re-borrow. (2) If an external
> repo does it AND we haven't, borrow the pattern but keep the Pāṭala-native semantics. (3) The epistemic
> core is ours; the orchestration is Hermes; the rest is organs.**

**The strongest confirmation:** the external reviews (coordinate, 15-plane) proposed borrowing Vouch,
Agetor, Beads Viewer — but `review_engine.py`, `object_registry.py`, and the event ledger are the
Pāṭala-native versions of exactly those. **We validated our design by finding that the ecosystem re-invents
what we already built.**

---

## WHAT TO DO NEXT (the reconciled plan)

1. **Stop researching the epistemic core** — it's built. Don't re-borrow Vouch/Agetor/Beads for Layers 02-08.
2. **Build Layer 12 Pieces 1-2** (projection engine + staleness engine) — the genuinely new, unbuilt pieces.
3. **Wire the partially-built** (ARGUMENT/SYNTHESIS workers, THEME/ESSAY/EDUCATION loop, 3 Hermes profiles).
4. **Use the external repos only where Pāṭala has NOT built it:** media (Remotion/OpenMontage),
   learner model (pyBKT/adaptive-kg), temporal graph (Graphiti), manuscripts (Mirador).

# AGENT 2 — SESSION HANDOVER (2026-08-13, late session — context preserved)

*Emergency handover written under context-pressure. This captures the FULL current state of Agent 2
(the Autonomous Translation Factory / corpus compiler) so a fresh session can continue immediately.
Both autonomous systems are RUNNING right now; do not kill them. Read the READ-FIRST list below.*

---

## 0. RIGHT NOW (the live systems — do not touch)

| System | pid | What it does |
|---|---|---|
| **live RAW→EN runner** | `362890` | translates the RAW_SANSKRIT queue → English (auto_translate_raw.py) |
| **factory loop** | `647686` | advances all works through canonical SOURCE→C1 (factory_loop.sh → DAG scheduler) |

Both are watchdog-protected (cron every 5 min). To check: `bash pipeline/start_overnight.sh status`.
Everything is committed + pushed to `origin/agent2` (0 ahead/behind). Latest: `f1a9e60`.

---

## 1. READ FIRST (the clean index)

- **`handover/agent-2-integration/README.md`** — the single lane index (READ-FIRST docs, overnight pack, build records)
- **`docs/FACTORY.md`** — the canonical factory reference (stack, pipeline, state systems, overnight, catalog)
- **`handover/agent-2-integration/CURRENT-STATE.md`** — current operational state + honest limitations
- **`docs/agent3potential.md`** — the Agent-3 case + the external peer-review that found the 3 bugs
- **`docs/HERMES-ORCHESTRATION-REVIEW.md`** — how the built factory maps to the Hermes orchestration plan
- **`handover/hermes/HERMES-AGENT3-FACTORY-COORDINATOR.md`** — the Agent-3-as-factory-coordinator design (R2)

---

## 2. WHAT'S DONE (this + prior sessions)

### Era A — Factory Completion (DONE)
All 6 canonical layers (T1/L0/ARGMAP/L2/L200/C1) AUTONOMOUSLY_PRODUCIBLE + **verified against the REAL
IPVV exemplars** (the `test_*_ipvv.py` suite).

### Era B — Corpus Compiler (DONE)
- **A2-8/9** DAG scheduler (all eligible jobs, free-draining L0) · **A2-10** rate limiting + size-aware
  timeout · **A2-11** durable append-only failure/retry queue (upsert + retry cap) ·
  **A2-12** dashboard · **A2-13** bulk certificate + overnight loop + catalog.

### Era C — Rebuild Engine (STARTED)
- **A2-14/15/16** supersession propagation + targeted regeneration (`factory_rebuild.py`).

### A2-ARCH-HARDEN (JUST DONE this session — the peer-review fixes)
1. ✅ **ONE canonical DAG manifest** — `contracts/CANONICAL-DAG.yaml` is the single source of truth.
   `object_registry.PREREQS` loads from it; the scheduler + rebuild derive from it (no independent
   maps). **Correct multi-parent gating**: `ARGMAP: [SOURCE, L0]`, `L2: [L0, ARGMAP]`. L2 no longer
   produced without L0+ARGMAP.
2. ✅ **Honest registry naming** — `VERSIONED_REGISTRY` (it rewrites on save), NOT append-only.
3. ✅ **Append-only hash-chained ObjectEvent ledger** — `object-events.jsonl`: every
   OBJECT_CREATED/STATUS_CHANGED/SUPERSEDED event is hash-chained; `verify_event_chain()` proves no
   silent rewrite. Current state is a projection.

### The overnight pack (usable)
`pipeline/start_overnight.sh start|status|stop` + `pipeline/OVERNIGHT.md` (runbook) +
`docs/SOURCE-PROCESS-OVERNIGHT.md` (full code trace).

---

## 3. TESTS — 19/19 PASS (deterministic)

```
test_workers · test_t1 · test_autonomy · test_l0 · test_l1_l2 · test_corpus_state · test_l0_align ·
test_review_engine · test_autonomous · test_scholarly_oracle · test_argmap · test_failure_queue ·
test_factory_status · test_factory_scheduler · test_rate_limit · test_factory_rebuild ·
test_factory_certificate · test_catalog · test_object_events
```
Plus the IPVV-exemplar suite (`test_*_ipvv.py`) + `prove_l0_equivalence`.

---

## 4. NEXT WORK (the roadmap)

1. **The `patala_*` MCP capability layer** (the biggest gap to Hermes orchestration) — expose
   `patala_next_action`, `patala_get_work_state`, `patala_propose_translation` as verbs reading/writing
   the registry+ledger. See `docs/HERMES-ORCHESTRATION-REVIEW.md` §2.1 + `handover/hermes/DEV-PLAN.md` Phase 1.3.
2. **Create the 3 Hermes profiles** (patala-producer / patala-verifier / patala-coordinator) + external
   skill dir (see `HERMES-AGENT3-FACTORY-COORDINATOR.md`).
3. **Run the factory via Hermes kanban/cron** (Hermes supervisor; our loop = producer worker).
4. **Then Era C continuation**: A2-18 DependencyImpactReport + A2-19 ReviewBundle.
5. **Later**: anchor release roots to Rekor (Sigstore) + the event-sourced registry as projection.

**Remaining peer-review items (A2-ARCH-HARDEN):** derive current state as a projection of the event
ledger (step 9), and the FactoryRunCertificate referencing the event range/root hash (step 11).

---

## 5. KEY FILES MAP (the state)

| Concern | Path |
|---|---|
| Canonical DAG (single source of truth) | `contracts/CANONICAL-DAG.yaml` |
| Versioned registry + ObjectEvent ledger | `pipeline/object_registry.py` |
| DAG scheduler | `pipeline/factory_scheduler.py` |
| Per-layer production + failure queue + audit | `pipeline/factory_batch.py` |
| Rebuild engine | `pipeline/factory_rebuild.py` |
| Dashboard | `pipeline/factory_status.py` |
| Bulk certificate | `pipeline/factory_certificate.py` |
| Unified catalog (per-work × per-layer) | `pipeline/catalog.py` |
| Overnight launcher | `pipeline/start_overnight.sh` + `factory_loop.sh` |
| Factory reference | `docs/FACTORY.md` |
| Canonical stack (locked) | `handover/agent-2-integration/CANONICAL-LAYER-STACK.md` |

---

## 6. HONEST CAVEATS

- **Semantic correctness is Agent 1's lane** (AlignScore/NLI). Agent 2 proves shape + provenance + safe
  unattended production + integrity (event chain).
- **Overnight rate is bounded by the shared model API** (T1 is model-bound; the live runner + factory
  share one API). Raise `FACTORY_MODEL_CALLS` to go faster at the live runner's expense.
- **Pre-existing data cruft** (orphan MODE_B L0 without T1 parent, ~781) is surfaced by the certificate
  and superseded as T1 is built — the factory is consistent; the data is being cleaned via supersession.
- **The state is fully committed + pushed.** Nothing is lost. Both systems are live and protected.

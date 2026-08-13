# GLOBAL NEXT — the coordinated next steps for the next agent (2026-08-13)

*A cross-lane coordination snapshot. The global docs (`docs/global/GLOBAL-STATE-2026-08-13.md`,
`PATALA-GLOBAL-ARCHITECTURE.md`) were written earlier and are **stale on Agent 2's side** — they predate
the autonomous factory. THIS file is the current, coordinated next-step reference for whoever continues.
Read the linked docs; trust THIS for "what is true right now."*

---

## 1. THE TWO-LANE STATE (right now)

### Agent 2 — Autonomous Translation Factory (ACTIVE, RUNNING)
- **Era A (Factory Completion): DONE** — all 6 canonical layers (T1/L0/ARGMAP/L2/L200/C1)
  AUTONOMOUSLY_PRODUCIBLE + verified against the REAL IPVV exemplars.
- **Era B (Corpus Compiler): DONE** — DAG scheduler, rate limiting, failure/retry queue, dashboard,
  bulk certificate, unified catalog.
- **Era C (Rebuild Engine): STARTED** — supersession propagation + targeted regeneration.
- **A2-ARCH-HARDEN: JUST DONE** — one canonical DAG manifest (`contracts/CANONICAL-DAG.yaml`),
  honest `VERSIONED_REGISTRY`, append-only hash-chained ObjectEvent ledger.
- **Live systems RUNNING:** live RAW→EN runner (pid `362890`) + factory loop (pid `647686`),
  watchdog-protected. **19/19 tests pass.**
- **Reference:** `docs/FACTORY.md` · `handover/agent-2-integration/HANDOVER-2026-08-13-LATE-SESSION.md`.

### Agent 1 — Verification / Evals / Scholar Evidence (frozen ML vertical, forward = S0)
- Per GLOBAL-STATE-2026-08-13 §CURRENT DIRECTION: Agent 1's forward work is the **scholar-corpus
  foundation (S0)** — source-evidence substrate + scholar oracle + evaluation plane, REUSING mature
  open systems, owning only the epistemic seam.
- Reference: `handover/agent-1-ml/HANDOVER-2026-08-13.md` + `NEXT-STEPS.md`.

---

## 2. THE GLOBAL ARCHITECTURE (the north star — unchanged)

`docs/global/PATALA-GLOBAL-ARCHITECTURE.md` is THE architecture: seven planes, the constitutional rule
(higher layers depend on lower; lower never acquires authority from above), the native epistemic
ontology, three DAGs (epistemic/derivation/execution), the benchmark family, the skill contract, four
proof tracks. **The two-source-side architecture** converges at:
`Proposition ↔ CorroborationEvent ↔ SourceAssertion` (primary-text side + scholarship side).

**Agent 2 = the primary-text side + the compiler/CI system.** Agent 1 = epistemic QA + research lab.
Scholars = reviewers. Pāṭala graph = canonical repository.

---

## 3. WHAT'S NEXT (in priority order — for the next agent)

### Priority 1 — The intake step (extend the backlog 73 → ~102 works)
The factory runs on 73 on-disk RAW_SANSKRIT works. **sivaqueue3/4 add ~29 more targets** (compiled to
`data/corpus/sivaqueue34-targets.json` by `pipeline/ingest_sivaqueue34.py`; 23 have public e-text
sources). Next:
1. For each acquirable target, **download the Sanskrit source** → `data/corpus/sources/<work>/`
   (extend `pipeline/acquire_sivaqueue_targets.py` with the sivaqueue3/4 GRETIL/archive.org links).
2. **Register it in the ledger** as RAW_SANSKRIT → the factory auto-picks it up.
3. Add the sivaqueue34-companion metadata (tradition/śākhā/period/author/register) to the target
   records for context-engineering.

### Priority 2 — The `patala_*` MCP verb layer (the Hermes↔Pāṭala bridge)
The biggest gap to Agent-3 orchestration. Expose graph-as-verbs so Hermes can drive Pāṭala:
`patala_next_action` · `patala_get_work_state` · `patala_propose_translation` (PROPOSE, never ACCEPT).
See `docs/HERMES-ORCHESTRATION-REVIEW.md` §2.1 + `handover/hermes/DEV-PLAN.md` Phase 1.3.

### Priority 3 — Agent 3 (Hermes factory coordinator)
3 Hermes profiles (producer/verifier/coordinator) + external skill dir + kanban/cron-driven factory.
The execution already exists (Agent 2's loop); Agent 3 = the orchestration above it.
See `handover/hermes/HERMES-AGENT3-FACTORY-COORDINATOR.md` + `docs/agent3potential.md`.

### Priority 4 — Era C completion
A2-18 DependencyImpactReport + A2-19 ReviewBundle export (for Agent 1 / scholar review).

### Priority 5 — Remaining A2-ARCH-HARDEN
Derive current state as a projection of the ObjectEvent ledger; FactoryRunCertificate referencing the
event-range root hash; later anchor release roots to Rekor (Sigstore).

---

## 4. HOW TO CHECK THE LIVE SYSTEMS (don't get confused)

```bash
bash pipeline/start_overnight.sh status        # are the 2 systems alive? + dashboard
python3 pipeline/catalog.py --all              # per-work bibliography + source + every layer + audit
tail -f /tmp/opencode/factory-loop.log         # the factory's live per-pass log
tail -f /tmp/opencode/auto-translate.log       # the live RAW→EN log
python3 pipeline/factory_certificate.py        # integrity + resume (PASS = clean)
ls data/corpus/downloads/translations/         # the RAW→EN output (<work>.jsonl)
```

**Key clarification:** the running overnight system is **Agent 2's factory** (producing canonical
objects) — it is NOT Agent 3. Agent 3 is a separate, unbuilt orchestration layer above it.

---

## 5. THE CANONICAL FILES MAP (the truth lives here)

| Concern | Path |
|---|---|
| Canonical DAG (single source of truth) | `contracts/CANONICAL-DAG.yaml` |
| Factory reference | `docs/FACTORY.md` |
| Agent-2 lane index (READ FIRST) | `handover/agent-2-integration/README.md` |
| Emergency handover | `handover/agent-2-integration/HANDOVER-2026-08-13-LATE-SESSION.md` |
| Global architecture | `docs/global/PATALA-GLOBAL-ARCHITECTURE.md` |
| Global state (stale on A2 side — see §3 here) | `docs/global/GLOBAL-STATE-2026-08-13.md` |
| Agent-3 case + peer review | `docs/agent3potential.md` |
| Hermes orchestration review | `docs/HERMES-ORCHESTRATION-REVIEW.md` |
| Agent-3 factory-coordinator design | `handover/hermes/HERMES-AGENT3-FACTORY-COORDINATOR.md` |
| sivaqueue3/4 intake | `data/corpus/sivaqueue34-targets.json` + `pipeline/ingest_sivaqueue34.py` |

---

## 6. THE ONE-SENTENCE CARRY-FORWARD

**The autonomous factory is built, running, hardened (canonical DAG + event ledger), and 19/19 tested;
the next moves are (1) acquire+register the sivaqueue3/4 sources to grow the backlog, (2) build the
`patala_*` MCP verbs, (3) wire Agent 3 (Hermes kanban coordinator) above the factory, (4) finish Era C
(ImpactReport + ReviewBundle) — with the global architecture as the north star and the factory as the
compiler/CI system underneath.**

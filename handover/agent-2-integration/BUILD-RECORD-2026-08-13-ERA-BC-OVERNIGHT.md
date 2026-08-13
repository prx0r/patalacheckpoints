# AGENT 2 — BUILD RECORD 2026-08-13 (Era B/C: the corpus compiler + overnight pack)

*Companion to `BUILD-RECORD-2026-08-13-VERTICAL-WORKERS.md` and `BUILD-RECORD-2026-08-13-LAYER-TESTS.md`.
This records the Era B (Corpus Compiler) + Era C (Rebuild Engine) work + the usable overnight pack —
the phase where Agent 2 stopped being a *worker builder* and became the **operating system for the
corpus** (schedule · execute · retry · resume · version · invalidate · rebuild · report).*

---

## 1. THE SHIFT (per the directive)

Agent 2's milestone is no longer "can individual workers run?" (that's done — Era A). It is:

> **Can the corpus compiler continuously advance a heterogeneous backlog, isolate failures, resume
> safely, and maintain correct dependency state without intervention?**

So the work moved from tuning individual layers to building the **corpus-level operating loop**, and
deliberately did NOT special-case the troublesome bhavopahara work — its retryable timeout is treated as
*useful evidence* that failure isolation works, not a bug to fix first.

## 2. ERA B — CORPUS COMPILER (built this session)

| A2 | Deliverable | File | Status |
|---|---|---|---|
| **A2-8/9** | DAG-based backlog scheduler + multi-work execution | `factory_scheduler.py` | ✅ DONE — enumerates ALL eligible (object,layer) jobs across the graph (not T1-only), ranks, executes within budget. Verified live (spandakarika T1). |
| **A2-13a** | DAG scheduling | `factory_scheduler.py` | ✅ rewritten — finds all eligible jobs, dependency-eligibility from the registry |
| **A2-13b** | free-draining deterministic layers | `factory_scheduler.py` | ✅ L0 runs immediately, never consumes the model budget |
| **A2-10** | resource/rate limiting | `factory_scheduler.py` + `test_rate_limit` | ✅ per-pass model-call budget + inter-batch throttle (coexists with the live runner) |
| **A2-10b** | size-aware timeout/backoff | `t1_worker.py` | ✅ T1 timeout scales with token count (base + 0.5s/token, bounded 600s) |
| **A2-11** | durable failure/retry queue | `factory_batch.py` | ✅ failures recorded, isolated, neighbors never blocked |
| **A2-11b** | preserve retry history (append-only) | `factory_batch.py` | ✅ a failure record stays; on success marked RESOLVED (never deleted) — audit survives for reliability metrics |
| **A2-12** | corpus progress dashboard | `factory_status.py` | ✅ per-work operational view (SOURCE/T1/.../C1 + stale/retryable) |
| **A2-13** | bulk certificate | `factory_certificate.py` | ✅ machine-readable: passes, jobs by layer, model_calls, integrity (duplicates/bad_parents/conflicts), resume_test |

## 3. ERA C — REBUILD ENGINE (started)

| A2 | Deliverable | File | Status |
|---|---|---|---|
| **A2-14/15/16** | supersession propagation + targeted regeneration | `factory_rebuild.py` | ✅ correcting one upstream (e.g. T1:v2) supersedes its downstream (L0/ARGMAP/L2/L200/C1) and regenerates ONLY those — compiler semantics. |
| **critical fix** | `object_registry.current()` | `object_registry.py` | ✅ now returns None when ALL versions are superseded (was: returned the superseded version). Without this, the rebuild engine couldn't detect invalidation. Core to the whole supersession story. |

## 4. THE OVERNIGHT PACK (the usable deliverable)

| File | What it is |
|---|---|
| `pipeline/start_overnight.sh` | ONE-COMMAND launcher: `start` (both systems + watchdogs) · `status` · `stop`. Idempotent. |
| `pipeline/OVERNIGHT.md` | the runbook: canonical-file map, how to start/status/stop, tuning env, morning checklist, honest expectations. |
| `pipeline/factory_loop.sh` | the overnight repeat-loop driver (DAG scheduler per pass, certificate at exit). |
| `pipeline/factory_loop_watchdog.sh` | cron watchdog (every 5 min) that restarts the loop if it dies. |

**To run overnight:** `bash pipeline/start_overnight.sh start` — both the live RAW→EN runner and the
factory loop run, watchdog-protected, rate-limited, idempotent.

## 5. TESTS (all PASS)

`test_workers · test_t1 · test_autonomy · test_l0 · test_l1_l2 · test_corpus_state · test_l0_align ·
test_review_engine · test_autonomous · test_scholarly_oracle · test_argmap · test_failure_queue ·
test_factory_status · test_factory_scheduler · test_rate_limit · test_factory_rebuild ·
test_factory_certificate` + the IPVV-exemplar suite (`test_*_ipvv.py`). **16 deterministic suites + the
IPVV suite all PASS.**

## 6. HONEST LIMITATIONS / NOTES

1. **Semantic correctness is Agent 1's lane** (AlignScore/NLI). Agent 2 proves shape + provenance +
   safe unattended production.
2. **Overnight rate is bounded by the shared model API** — T1 is model-bound; a conservative budget
   advances a few passages/pass. Raising `FACTORY_MODEL_CALLS` speeds the factory at the live runner's
   expense.
3. **Pre-existing data cruft** is surfaced by the certificate (11 duplicate current versions, 781 orphan
   MODE_B L0 with no T1 parent) — from earlier experimentation; superseded as T1 is built. The factory
   is consistent; the data is being cleaned via supersession.
4. **The two running systems** (live runner pid 362890 + factory loop) were both live at session end,
   watchdog-protected.

## 7. CARRY-FORWARD (next)

- **Era C continuation**: A2-18 DependencyImpactReport (mechanical: changed object → descendants
  invalidated → rebuilt) + A2-19 ReviewBundle export (SOURCE/T1/L0/ARGMAP/L2/L200/C1 + dependencies +
  versions + OPEN items) for Agent 1 / the scholar review. Do NOT make Agent 2 infer epistemic
  consequences — report exact dependency consequences; let Agent 1 enrich them.
- **Document discipline**: update `live/agent2.md` (concise) + DEV-PLAN (milestone-level only), not all
  four large docs after every small change. Runtime registries/certificates are authoritative.

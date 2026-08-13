# AGENT 2 — ERA A FACTORY STATUS + PRODUCTION REFERENCE (2026-08-13)

*Production-grade reference for the autonomous SOURCE→C1 corpus compiler (Era A). This records the
operational status of each canonical layer — what is AUTONOMOUSLY_PRODUCIBLE, how it is verified
against the REAL IPVV exemplars, and the guarantees (crash/resume, zero duplicates, provenance). The
registry is authoritative; this doc explains the architecture.*

---

## 1. THE CANONICAL STACK + PRODUCTION STATUS

| Layer | Worker | Validator | Status | Verified against (real IPVV exemplar) |
|---|---|---|---|---|
| SOURCE | `factory_batch._register_source` | registry (input_hash) | ✅ AUTONOMOUSLY_PRODUCIBLE | raw source |
| **T1** | `t1_worker.py` | canonical shape + source binding + fail-closed + abstention | ✅ **AUTONOMOUSLY_PRODUCIBLE** | `02_t1/chunkV2-O` (PASS: glosses match gold) |
| **L0** | `raw_l0.py` + `l0_worker.py` | `validate_l0_spec` (P0 lossless + schema + abstention) | ✅ **AUTONOMOUSLY_PRODUCIBLE** | `l0/chunkV2-O` (PASS: token coverage) |
| **ARGMAP** | `argument_map_worker.py` | 4-section shape + provenance + fail-closed | ✅ **AUTONOMOUSLY_PRODUCIBLE** | `pilot_V2O_ARGUMENT_MAP.md` (PASS: 6/8 claims) |
| **L2** | `l1_l2_translate.py` (L1L2) | L2 semantic-fidelity (content ⊆ L1+supplies) + provenance | ✅ **AUTONOMOUSLY_PRODUCIBLE** | `pilot_V2O_L2_read.md` (PASS: faithful prose) |
| **L200** | `l200_worker.py` (constrained compiler) | Task-2 fidelity (8-section, MT/IA split, derivation map) | ✅ **AUTONOMOUSLY_PRODUCIBLE** | `l200/V2O-saptamo-vimarsa.md` (PASS: MT taxonomy) |
| **C1** | `c1_worker.py` | C1-SPEC §17 (passage-local, no essay drift) | ✅ **AUTONOMOUSLY_PRODUCIBLE** | `c1/read/c1_V2O-orderless-support.md` (PASS: content + structure) |

**Semantic quality is Agent 1's SEPARATE axis** (Inspect/Pāṭala-Evals). Agent 2's gate per layer is
PRODUCTION: canonical shape + provenance + safe unattended + fail-closed → MACHINE_PROPOSED.

---

## 2. HOW EACH LAYER IS VERIFIED (the IPVV test suite — all against the real previous files)

```
pipeline/test_t1_ipvv.py      T1 vs 02_t1/chunkV2-O            PASS
pipeline/test_l0_ipvv.py      L0 vs l0/chunkV2-O               PASS (deterministic contract)
pipeline/test_argmap_ipvv.py  ARGMAP vs pilot_V2O_ARGUMENT_MAP  PASS
pipeline/test_l2_ipvv.py      L2 vs pilot_V2O_L2_read          PASS
pipeline/test_l200_ipvv.py    L200 vs l200/V2O-saptamo-vimarsa  PASS
pipeline/test_c1_ipvv.py      C1 vs c1/read/c1_V2O-orderless   PASS (deterministic stub; live under API contention)
```

**Deterministic unit suite (all PASS):**
```
test_workers · test_t1 · test_autonomy · test_l0 · test_l1_l2 · test_corpus_state (11/0)
test_l0_align (26/0) · test_review_engine (23/0) · test_autonomous · test_scholarly_oracle · test_argmap
prove_vertical (whole-chain L0→C1, fail-closed) · prove_l0_equivalence (vs exemplars)
```

---

## 3. THE AUTONOMOUS GUARANTEES (the production contract)

| Guarantee | Mechanism | Status |
|---|---|---|
| **Crash/resume** | `object_registry` immutable/versioned; each layer is committed independently | ✅ tested |
| **Zero duplicate commits** | `is_committed` idempotency by `(object_id, input_hash)` | ✅ tested |
| **Provenance** | every object carries `input_hash` + upstream version refs; child resolves to committed parent | ✅ tested |
| **Fail-closed** | model failure / bad JSON → GENERATION_FAILED, never a partial commit | ✅ tested |
| **Isolation** | one failed passage/layer doesn't block neighbors (bounded batches) | ✅ tested |
| **Staleness/supersession** | `supersede()` marks current stale; downstream recomputed | ✅ tested (CP3.5) |
| **SOURCE→C1 whole-chain** | `factory_batch.py` registers SOURCE, advances each layer | ✅ wired; model steps slow under API contention |

---

## 4. THE WHOLE-FACTORY COMMAND (the user experience)

```bash
# register + advance a work through the full canonical stack, one layer at a time:
python3 pipeline/factory_batch.py --work <work_id> --count <n> --layers T1,ARGMAP,L0,L2,L200,C1
```
The controller + registry advance from the correct frontier; workers are implementation details.

---

## 5. HONEST LIMITATIONS (what is NOT yet true)

1. **Semantic correctness is NOT validated** — that is Agent 1's evals lane (AlignScore/NLI, the
   T1-NAT / L200-DEV gates). Agent 2 proves shape + provenance + safe unattended production.
2. **Whole-work unattended run on a fresh work is slow under the live runner's API contention** — the
   batch advances correctly but model calls queue. A per-passage timeout/retry scheduler (Era B,
   A2-8..A2-13) is the next milestone for corpus-scale.
3. **L2/C1 live model calls intermittently GENERATION_FAILED under contention** — fail-closed works
   correctly (no partial commit); the deterministic logic is verified.
4. **ESSAY/EDUCATION/THEME** have workers but are NOT yet Era-A targets (they wait until Agent 1
   freezes their contracts).

---

## 6. NEXT (Era B — corpus compiler, per docs/agent2nextdev.md)

- A2-8 backlog scheduler · A2-9 multi-work execution · A2-10 resource/rate limiting
- A2-11 durable failure/retry queues · A2-12 corpus progress dashboard · A2-13 unattended bulk translation
- Then Era C: the living rebuild engine (supersession propagation, targeted regeneration, ImpactReport).

*This is the Era A reference. The canonical layer order + file types: `handover/agent-2-integration/
CANONICAL-LAYER-STACK.md`. The full roadmap: `docs/agent2nextdev.md`.*

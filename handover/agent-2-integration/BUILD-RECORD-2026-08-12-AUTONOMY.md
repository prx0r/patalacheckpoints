# BUILD RECORD — autonomous translation factory (2026-08-12)

*The complete record of what Agent 2 built toward the autonomous translation factory (the canonical
`SOURCE → L0/L1 → L2 → L200 → C1` pipeline), including the L0/L200 certificates, the live benchmarks,
and the scholar-oracle proof (handed to the evidence lane). Companion to `docs/BUILD_NOTES_AUTONOMY.md`,
`docs/BUILD_NOTES_S0_1.md`, `handover/agent-2-integration/PROBLEMS-AUTONOMOUS-TRANSLATION.md`.*

---

## The architecture (target, frozen)
`handover/hermes/hermespatalalayers.md` + `hermespatala-architecture-review.md`:
ONE deterministic controller + ONE scheduler (cron heartbeat) + one skill per layer; registries = truth;
layers = typed compiler passes; eligibility derived from registry; immutable supersession; certificates
before unattended scale. **Hermes manages work. Pāṭala manages knowledge.**

---

## Files built this session

### Generic autonomy core
| file | what |
|---|---|
| `pipeline/object_registry.py` | generic per-layer immutable registry (three-state ladder, input-hash idempotency, supersession, cascading stale) |
| `pipeline/autonomy.py` | the deterministic controller: flock, eligibility predicates, bounded batches, dispatch layer handler, validate, COMMIT/REJECT, run reports |
| `pipeline/l0_worker.py` | L0 layer handler: real RAW-L0 (Vidyut) + batch gloss + validate_l0_spec + commit |
| `pipeline/l200_worker.py` | L200 audit compiler: comparative L1→L2 MT/IA proposal (proposal_status COMPLETE/GENERATION_FAILED) + Task-2 validator |
| `skills/autonomous-layer/` | canonical layer skills re-mapped to `L0/L1/L2/L200/C1/THEME/ESSAY/EDUCATION` (removed the retired T1–T3.1) |

### Batch / reliability (the earlier L0 hardening)
| file | what |
|---|---|
| `pipeline/batch_translate.py` | ONE `hermes -z` call → L0 glosses + close translations for a whole batch (max context, no token cap, passage_id+sha binding) |
| `pipeline/agentic_gloss.py` | batch propose + self-challenge (many verses per call, 600s timeout) |
| `pipeline/model.py` | no token cap (max_tokens unenforced); fail-fast 120s default + bounded retry; process-group kill (F3) |
| `pipeline/auto_run.py` | ledger-driven RAW-L0 loop with registry-derived idempotent skip (F1) + SOURCE_BLOCKED (F7) |
| `pipeline/night_supervisor.py` / `night_review.py` | unattended all-night worker (flock) + reviewable run log |

### Certificates + benchmarks
| file | what |
|---|---|
| `pipeline/certificate_l0.py` | L0 A–H certificate → `factory-certificates/L0-v1/` (deterministic floor certified; gloss 7/7 semantic; hermes nondeterminism = the real risk) |
| `pipeline/certificate_l200.py` | L200-v1 validator-torture certificate (10 phenomena, dims A–L, adversarial mutations, invalidation) → `factory-certificates/L200-v1/` |
| `pipeline/benchmark_l200_live.py` | LIVE L200 semantic benchmark (real model vs typed references: MT/IA precision+recall, laundering, false-certainty, gen-failure) |

### Scholar-oracle proof (handed to the evidence lane — NOT continued by Agent 2)
| file | what |
|---|---|
| `pipeline/scholarly_oracle.py` | witness → publication → span → SourceAssertion → CorroborationEvent (DIRECT/PARTIAL); S0.3 render |
| `pipeline/test_scholarly_oracle.py` | the 10 S0.1 tests |

### Tests
`test_autonomy.py` (16/16) · `test_workers.py` (11/11) · `test_autonomous.py` (7/7) ·
`test_scholarly_oracle.py` (10/10).

---

## Results

### L0 certificate (cross-work, kramasadbhāva)
A lossless 2/2 · B binding 2/2 · C gloss 7/7 semantic · F source-blocked 1 · G replay 0 · H cross-work.
Deterministic floor certified; the real risk is **hermes gloss nondeterminism** (empty returns → fail-closed).

### L200-v1 certificate
10/10 phenomenon fixtures + 14/14 dims (A–L) pass. Proves: empty-success (J) commits vs
GENERATION_FAILED (I) blocks; laundering flagged; source-layer required+attributed; open-item honesty;
replay; mutation/invalidation (upstream change → prior L200 superseded).

### L200 LIVE semantic benchmark (real model, iterated)
| metric | v1 | after iterate |
|---|---|---|
| MT precision | 0.926 | **0.95** |
| MT recall | 0.667 | **0.70** |
| IA precision | 0.333 | **0.80** |
| IA recall | 1.0 | 1.0 |
| generation failure | 0.1 | **0.0** |
| laundering / false-certainty | 1 / 1 | 1 / 1 |

Iteration (conservative prompt: precision over coverage, abstain on paraphrase) fixed the IA
over-production. Remaining weak spot: **MT recall 0.70** (required MTs missed on F1/F2/F5) + 1
laundering/false-certainty case. **Do NOT scale L200 until MT recall + laundering are bounded.**

---

## Honest status
- The **deterministic floor + validator + certificate architecture is certified**.
- The **live L200 MT/IA proposer is functional but not yet certified**: IA precision fixed (0.80),
  MT recall (0.70) and 1 laundering case remain above the conservative threshold.
- **L0: not scaled** (hermes gloss nondeterminism must be bounded first).
- **L200: not scaled** (MT recall/laundering gate).
- **C1: not yet built** (next, after L200 freezes).
- **Full unattended SOURCE→L0/L1→L2→L200→C1: not yet proven.**
- **Scholar-oracle (S0.1)**: proof exists; handed to the evidence lane, NOT continued by Agent 2.

---

## Next (Agent 2, in order)
1. Bounded real IPVV batch (10–20 chunks): real L1+L2 → live L200 → certified validator.
2. Iterate L200 until MT recall + laundering clear the threshold; then freeze L200 v1 + wire into the controller.
3. C1 autonomous production (skill + validator + adversarial tests + certificate + canary).
4. Prove the unattended vertical SOURCE→L0/L1→L2→L200→C1 (crash/resume, idempotency, stale invalidation, fail-closed).
5. Then the larger IPVV production factory.

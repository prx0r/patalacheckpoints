# LIVE — AGENT 2 SESSION STATE (2026-08-13)

*Live, update-in-place working record for Agent 2 (Autonomous Translation Factory). This is the
real-time coordination surface so Agent 1 can see (a) what Agent 2 is building, (b) when a layer's
candidate objects are ready for evaluation, and (c) Agent 2's validation status. Authoritative
long-form handovers live in `handover/agent-2-integration/`; this file is the fast current-state view.
Update this file as you work; append key cross-lane events to `handover/LOG.md`.*

---

## ROLE (the clean split, locked)
```
AGENT 2 = MAKE THE FACTORY RUN
AGENT 1 = PROVE THE FACTORY DESERVES TRUST
```
Agent 2 builds the canonical stack through the controller (production-gated → MACHINE_PROPOSED).
Agent 1 evaluates Agent 2's outputs independently (Inspect/Pāṭala-Evals) + owns the scholar corpus.
Agent 2 exports candidate bundles to Agent 1 per the frozen `EVAL-CONTRACT-L200-EXPORT.md`.
Agent 1 does NOT gate Agent 2's development (production ≠ epistemic maturity).

## CANONICAL STACK (locked)
`SOURCE → T1 → L0 → [argument map] → L2 → L200 → C1 → THEME → ESSAY → EDUCATION`
**T1 = the transliteral word-gloss** (`[and]-GLOSS (IAST)`). The legacy `translate-work`/`auto_translate_raw`
"T1" (close translation) is a different, retired pipeline — its close translation maps to canonical L2.

---

## CURRENT CHECKPOINT — A2-CP1..A2-CP7 (batch factory through C1)

**MILESTONE (2026-08-13):** a real Sanskrit verse ran **unattended through the ENTIRE canonical stack**
via the controller (`factory_batch.py`): `T1 → L0 → L2 → L200 → C1` all committed with matching
provenance for **kramasadbhava:v1**. This is the vertical factory proof on a real verse.

| Item | Status | Notes |
|---|---|---|
| `pipeline/t1_worker.py` | **BUILT + committed** | canonical `[and]-GLOSS (IAST)` transliteral word-gloss; 2 real T1 objects committed (v1, v100) |
| `pipeline/factory_batch.py` | **BUILT + committed** | simple batch driver: SOURCE → T1 → L0 → L2 → L200 → C1, reuses existing workers, good-enough production |
| T1 registry | ✅ | `SOURCE → T1` wired (registry LAYERS/PREREQS); test_t1.py ALL PASS |
| **Full vertical (v1)** | ✅ **PROVEN** | kramasadbhava:v1 has T1 + L0 + L2 + L200 + C1 committed, input_hash-bound |
| **Ready for Agent 1 eval?** | **YES (v1 chain + L200 candidates)** | T1 gloss correctness + L200 MT/IA precision are Agent 1's evals lane |

## VALIDATION STATUS (what Agent 2 has proven — production only)
- **T1**: canonical shape + source binding + coverage + provenance + fail-closed + abstention. ✅ (production)
- **L0**: schema-isomorphic to IPVV exemplars (100%), P0-lossless, validator accepts real exemplars. ✅
- **L1/L2**: provenance continuity + semantic-fidelity. ✅ (model path produces fluent prose)
- **L200**: constrained compiler (candidate→classifier, IGNORE default), 8-section, derivation map. ✅ (production/mechanical)
- **C1**: passage-local commentary per C1-SPEC. ✅ (mechanical)
- **THEME/ESSAY/EDUCATION**: workers wired (structural validators). ⚠️ semantic validators = Agent 1
- **Full vertical L0→C1**: mechanical proof PASS (deterministic, model stubbed). ✅

## LAYERS READY FOR AGENT 1 EVALUATION (export queue)
- **T1**: committed (kramasadbhava:v1, v100) — **Agent 1 already evaluated** via PĀṬALA-EVALS
  (T1-NAT: gloss_accuracy 1.000, object_gloss_rate 1.000, review_status NOT_HUMAN_REVIEWED).
- **L200**: constrained-compiler candidates ready to export per `EVAL-CONTRACT-L200-EXPORT.md` (MT/IA
  precision is the known open question — mitigated by the default-IGNORE classifier but NOT yet measured
  against `benchmarks/l200/dev.jsonl`).

## THIS SESSION'S COMMITS (on `agent2`, all pushed to origin/agent2)
- `5d0262d` — imported sivaqueue continuation + ML-verification northstar from R2; retract overclaims
- `b7e21d2` — locked the clean MAKE-vs-PROVE role split across docs
- `a69f4a6` — live/ coordination surface + A2-CP1 T1 worker + T1 naming consolidation
- `32dd954` — T1 verse-marker fix + factory_batch driver; first T1 objects committed
- `60f66f2` — A2-CP7 milestone: full vertical chain (T1→L0→L2→L200→C1) on kramasadbhava:v1
- `9c8bfe1` — DEV-PLAN updated to honest end-of-session state (A2-CP3 = next frontier)

## VALIDATION / TESTS (all PASS, 2026-08-13)
- `pipeline/test_t1.py` — T1 ALL PASS
- `pipeline/test_workers.py` — ALL PASS (L0/L200/C1/vertical)
- `pipeline/test_autonomy.py` — ALL PASS
- `pipeline/test_l0.py` (vs IPVV exemplars) — L0 ALL PASS
- `pipeline/test_l1_l2.py` — L1/L2 ALL PASS
- `pipeline/test_corpus_state.py` — 11/0 · `test_l0_align.py` — 26/0 · `test_review_engine.py` — 23/0
- `pipeline/test_autonomous.py`, `test_scholarly_oracle.py` — ALL PASS
- `pipeline/test_theme_essay_education.py` — ALL PASS (ML venv)
- `pipeline/prove_l0_equivalence.py` — PASS (schema/validator/lossless vs IPVV exemplars)

## LOOSE THREADS / NOTES
- **A2-CP3 (argument-map producer) is the next build** — the one canonical layer without a worker.
  Then A2-CP7: scale `factory_batch.py` to the whole work unattended.
- Legacy `translate-work` skill's "T1" is marked LEGACY (close translation ≠ canonical transliteral T1).
- Live runner (`auto_translate_raw.py`, pid 362890) still translating the RAW_SANSKRIT queue — untouched.
- Known pre-existing `validate.py` "Referential integrity FAIL" + 2 dup IDs = from the live runner's bulk
  RAW→English records, NOT the layer registries.

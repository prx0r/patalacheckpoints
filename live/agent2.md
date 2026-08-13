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

## CURRENT CHECKPOINT — A2-CP1: SOURCE → T1 (the transliteral word-gloss producer)

| Item | Status | Notes |
|---|---|---|
| `pipeline/t1_worker.py` | **BUILT** | segments raw Sanskrit (Vidyut → IAST surfaces), glosses each token into canonical `[and]-GLOSS (IAST)`, deterministic production gate |
| `object_registry.py` | **BUILT** | T1 added to LAYERS + PREREQS (`SOURCE → T1 → L0`) |
| `autonomy.py` | **BUILT** | T1 handler wired |
| `pipeline/test_t1.py` | **ALL PASS** | canonical shape, source binding, coverage, provenance, fail-closed, honest abstention |
| Live model run | ✅ verified | real verse → `[and]-GLOSS (IAST)`, validator PASS |
| **Ready for Agent 1 eval?** | **NOT YET** | T1 objects not yet committed to the registry on a real batch; semantic eval (gloss correctness vs gold) is Agent 1's lane |

## VALIDATION STATUS (what Agent 2 has proven — production only)
- **T1**: canonical shape + source binding + coverage + provenance + fail-closed + abstention. ✅ (production)
- **L0**: schema-isomorphic to IPVV exemplars (100%), P0-lossless, validator accepts real exemplars. ✅
- **L1/L2**: provenance continuity + semantic-fidelity. ✅ (model path produces fluent prose)
- **L200**: constrained compiler (candidate→classifier, IGNORE default), 8-section, derivation map. ✅ (production/mechanical)
- **C1**: passage-local commentary per C1-SPEC. ✅ (mechanical)
- **THEME/ESSAY/EDUCATION**: workers wired (structural validators). ⚠️ semantic validators = Agent 1
- **Full vertical L0→C1**: mechanical proof PASS (deterministic, model stubbed). ✅

## LAYERS READY FOR AGENT 1 EVALUATION (export queue)
- **L200**: constrained-compiler candidates ready to export per `EVAL-CONTRACT-L200-EXPORT.md` (MT/IA
  precision is the known open question — the ~0.20 MT-precision issue is mitigated by the default-IGNORE
  classifier but NOT yet measured by Agent 1 against `benchmarks/l200/dev.jsonl`).
- **T1**: not yet (will announce when committed on a real batch).

## THIS SESSION'S COMMITS (on `agent2`)
- `5d0262d` — imported sivaqueue continuation + ML-verification northstar from R2; retract overclaims
- `b7e21d2` — locked the clean MAKE-vs-PROVE role split across docs
- (pending) T1 worker + naming consolidation — uncommitted, to commit next

## LOOSE THREADS / NOTES
- Legacy `translate-work` skill's "T1" is marked LEGACY (close translation ≠ canonical transliteral T1).
- Live runner (`auto_translate_raw.py`, pid tracked separately) still translating the RAW_SANSKRIT queue — untouched.
- Next: commit T1 worker; then produce T1 objects on a real committed batch → announce to Agent 1.

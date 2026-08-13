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

## CURRENT CHECKPOINT — ERA A FACTORY COMPLETION (SOURCE→C1, all layers IPVV-verified)

**All six canonical layers are AUTONOMOUSLY_PRODUCIBLE and verified against the REAL IPVV exemplars:**

| Layer | Status | Verified vs (real IPVV file) |
|---|---|---|
| T1 | ✅ | `02_t1/chunkV2-O` (glosses match gold) |
| L0 | ✅ | `l0/chunkV2-O` (token coverage + P0 lossless) |
| ARGMAP | ✅ | `pilot_V2O_ARGUMENT_MAP.md` (6/8 gold claims) |
| L2 | ✅ | `pilot_V2O_L2_read.md` (faithful prose) |
| L200 | ✅ | `l200/V2O-saptamo-vimarsa.md` (MT taxonomy) |
| C1 | ✅ | `c1/read/c1_V2O-orderless-support.md` (content + structure) |

Production reference: `handover/agent-2-integration/CURRENT-STATE.md`. Roadmap: `docs/agent2nextdev.md`.

## VALIDATION / TESTS (all PASS, 2026-08-13)
- IPVV-exemplar suite: `test_t1_ipvv` · `test_l0_ipvv` · `test_argmap_ipvv` · `test_l2_ipvv` ·
  `test_l200_ipvv` · `test_c1_ipvv` — all verify against the previous existing IPVV files.
- Deterministic unit suite: `test_workers` · `test_t1` · `test_autonomy` · `test_l0` · `test_l1_l2` ·
  `test_corpus_state` (11/0) · `test_l0_align` (26/0) · `test_review_engine` (23/0) · `test_autonomous` ·
  `test_scholarly_oracle` · `test_argmap` + `prove_vertical` + `prove_l0_equivalence`.

## THIS SESSION'S COMMITS (on `agent2`)
- `db7b13f` T1 over-segmentation fix + T1-IPVV test
- `160bbe1` ARGMAP-IPVV test
- `affc86e` L2-IPVV test
- `622cabd` L200-IPVV test
- `9a5ae6e` C1-IPVV test + length-ceiling fix
- `f3d1a46` agent2nextdev roadmap
- `596d03e` test_autonomy canonical L2 dependency
- `22a5120` factory_batch SOURCE registration
- `24d177b` Era A CURRENT-STATE.md (production reference)

## READY FOR AGENT 1 EVALUATION
- T1 objects (v1, v100, v11) — T1-NAT evaluated by Agent 1 (gloss_accuracy 1.000)
- Full vertical chains + the IPVV-verified test suite
- L200 candidates per `EVAL-CONTRACT-L200-EXPORT.md`

## LOOSE THREADS / NOTES
- **Era B (corpus compiler)** is next: backlog scheduler, multi-work, rate limiting, failure/retry
  queues, progress dashboard, unattended bulk translation. The fresh-work run is slow under the live
  runner's API contention — a per-passage timeout/retry scheduler is the key Era B build.
- Semantic correctness = Agent 1's evals lane (AlignScore/NLI), NOT Agent 2's.
- Live runner (auto_translate_raw.py, pid 362890) still translating — untouched.

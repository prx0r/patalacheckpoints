# AGENT 2 (CORPUS COMPILER + INTEGRITY) — CHECKPOINTS & GOALS

*2026-08-12. The Agent-2 leading doc. **Agent 2's identity broadened from "the L0 agent" to the CORPUS
COMPILER + INTEGRITY LAYER** — it maintains the canonical machine-readable corpus state that Agent 3
(translation factory) safely operates on, and the review/dependency engine that turns a scholar's
correction into an executable graph mutation. Read `AGENTS.md` + `AGENTS-DOCTRINE.md` +
`handover/CHECKPOINTS.md` first.*

---

## THE LANE (what Agent 2 owns)

```
CP1 PHILOLOGICAL PROOF   →   CORPUS STATE   →   REVIEW/EXECUTABLE-CORRECTIONS
```

**Agent 2's questions:**
- *Is this reading licensed by the source?* (the L0 floor)
- *What do we have, where is it, what state is it in, and can every artifact resolve?* (corpus state)
- *How does a scholar's judgment become an executable graph mutation?* (the review engine)
- *How does every layer of the canonical stack become a deterministic, validated autonomous flow?* (the factory)

**The clean division (per the agent architecture):** Agent 2 = corpus compiler + integrity + state truth +
**the autonomous factory** (wraps each layer in a controller handler + layer-specific validator, reusing
Agent 1's higher-layer algorithms). Agent 1 = the higher-layer *algorithms* (theme/argument/essay/semantic
alignment). The join is the registry: Agent 2 produces the deterministic validated objects; Agent 1's
machinery is the *proposal engine* Agent 2 reuses.

**Does NOT:** generate T1/L2/C1 independently (that's the factory, which Agent 2 builds but which honors
Agent 1's algorithms), promote machine output to accepted scholarship, do argument extraction / themes /
synthesis *as scholarship* (Agent 1).

**HARD RULE — work LAYER BY LAYER, each against its canonical spec + source files.** Perfect L0 (or
T1/L1/R1) → commit → L1/L2 → commit → L200 → commit → C1 → commit → THEME → ESSAY → EDUCATION. Do not build
a layer whose upstream is not committed; do not skip ahead to a higher layer because its algorithm already
exists. Each layer's worker produces its canonical file shape (`translations/_stack/ipvv/specs/*`, the
L200 8-section spec, the C1-SPEC, the `pilot_*_ARGUMENT_MAP.md` argument maps) and is gated by a
layer-specific deterministic validator.

---

## GOAL 1 — THE PHILOLOGICAL PROOF FLOOR (CP1, substantially DONE)

**Where you are (the source floor is real and frozen):**
- **P0 — COMPLETE IPVV 63/63 LOSSLESS, FROZEN.** V2/V3 35/35 (103,917 tokens, 0 unknown) + **V1 legacy
  28/28** via `pipeline/extract_l0_v1.py` (`verify_l0.py` UNCHANGED). Honest caveat: 63/63 proves
  two-format robustness, NOT cross-work generalization (that waits for a second work).
- **P2 CALIBRATED + FROZEN witness (P-011).** Vidyut×Heritage ensemble: control 84–85%, conflict-resolve
  72%, true double-conflict ~9%.
- **P3 ranker REJECTED (P-012).** ranker.py 0.76 < embedding 0.81, 0 abstention.
- **P4 alignment FROZEN witness (P-013).** L0↔L2 term-anchor: 0.93 recall / 0.89 precision / 1.0 abstain
  + independent Vidyut witness 0.81. Frozen per the adequacy doctrine.

**Remaining CP1 items (non-blocking / deferred):**
- P2 human blind review (160 cases) → VALIDATED_AGAINST_HUMAN_GOLD — logged, non-blocking.
- P5 syntax — deferred (adequacy doctrine).
- Cross-work L0 generalization — demonstrated only when a second real work is ingested.

---

## GOAL 2 — THE CORPUS STATE MACHINE (Agent 2's core object, BUILT)

The control plane Agent 3 consumes:

```
pipeline/corpus_state.py  →  per-work state from ACTUAL disk truth:
                              source availability + format (AND_GLOSS / RAW_SANSKRIT)
                              translation stage (T1/L2/C1) · L0 status · proof · review
                              NEXT_VALID_ACTION(work) + eligible_for_agent3
data/corpus/downloads/translation-state-ledger.json   (45 works)
GET /api/corpus/state                                  (served read-only)
```

**Status:** ✅ BUILT + served. The transition contract (MISSING_SOURCE→ACQUIRE, RAW_SANSKRIT→BUILD_L0_
SOURCE_MODE [blocked], L0_VERIFIED→GENERATE_TRANSLATION, etc.) is the Agent-3 control plane.

---

## GOAL 3 — THE EXECUTABLE-CORRECTIONS REVIEW ENGINE (the moat, PHASE 3A BUILT)

The thing to obsess over: a scholar's judgment is an **immutable, provenance-carrying graph mutation**,
not prose.

```
ReviewEvent (append-only) → Review ledger → deterministic reducer → Current scholarly state
   → dependency traversal → ImpactReport (exactly what a correction changes)
```

**Status:** ✅ **Phase 3A BUILT + PROVEN** (`pipeline/review_engine.py`, 15/15 tests). The vertical loop
over ARG-002 (G2-TC2 v1→v2 REVISE): v1 retained, ReviewEvent resolves, v2 created, G2-INF1/G2-CONC
→ NEED_REVIEW, ARG-004 untouched (isolation), reducer idempotent. Doctrine holds: ACCEPT ≠ truth,
REJECT ≠ delete, REVISE ≠ overwrite.

**The five concepts are real:** `ReviewEvent` · `ObjectVersion` · `DependencyEdge` (GROUNDS /
USES_AS_PREMISE / USES_AS_WARRANT / ORGANIZES) · `DerivedState` · `ImpactReport`.

---

## THE CONCRETE SEQUENCE (where we're headed — updated 2026-08-13)

> **NEW NORTHSTAR:** Agent 1 solved the *algorithms* of the higher layers (theme clustering, argument,
> essay, semantic alignment). Agent 2 wraps each in the **autonomous controller flow** — deterministic,
> provenance-bound, layer-specific-validated — until the whole canonical stack is a **single autonomous
> pipeline**. **THE CANONICAL LAYER STACK IS LOCKED: see `CANONICAL-LAYER-STACK.md`** (verified against
> the actual IPVV files). **Work LAYER BY LAYER**, each layer against its canonical spec + source files
> (`translations/_stack/ipvv/specs/*`, the L200 8-section spec, the C1-SPEC, the argument maps). The order:
> `SOURCE → T1 → L0 → [argument map] → L2 → L200 → C1 → THEME → ESSAY → EDUCATION`. T1 = transliteral
> word-gloss; L0 = structured token records from T1; argument map = lateral guide; L2 = readable prose.

```
CP1 floor ✅ (63/63)  →  corpus state ✅ (ledger)  →  review engine ✅ (Phase 3A+3D)
   ↓
✅ 2026-08-13 (Era A): FACTORY COMPLETION — all six canonical layers (T1/L0/ARGMAP/L2/L200/C1) are
   AUTONOMOUSLY_PRODUCIBLE, each with a controller handler + layer-specific validator, and each
   VERIFIED against the REAL IPVV exemplars (the test_*_ipvv.py suite). See
   `handover/agent-2-integration/CURRENT-STATE.md`.
   ↓
✅ 2026-08-13 (Era B): CORPUS COMPILER — durable failure/retry queue (A2-11), progress dashboard
   (A2-12), backlog scheduler + multi-work execution (A2-8/9), resource/rate limiting (A2-10) all DONE.
   Unattended bulk translation (A2-13) running across all registered works.
   ↓
🔴 NEXT (Era B frontier): let the unattended bulk run advance the whole corpus through SOURCE→C1;
   then Era C (living rebuild engine: supersession propagation, dependency invalidation, targeted
   regeneration, ImpactReport integration).
   ↓
NOTE: semantic correctness is Agent 1's evals lane (Inspect/Pāṭala-Evals — the T1-NAT / L200-DEV
gates). Agent 2's gate per layer is PRODUCTION (canonical shape + provenance + safe unattended).
   ↓
PRIORITY (Era C, after bulk): autonomous end-to-end vertical proof on a real corpus subset with the
   supersession/regeneration engine (correct one upstream object → rebuild only its affected downstream).
   ↓
PHASE 3E  tiny Scholar Workbench review screen   (deferred until a real reviewer is ready)
PHASE 3F  Hermes A4 scheduling                   (LAST)
```

**The threshold before "set it loose" — the factory certificate:** P0 coverage 100% · 0 bad spans ·
segmentation/lemma/morphology measured · literal gloss human-rated · **false certainty below threshold**
(the most important metric — the P3 ranker failed on 100% false certainty) · abstention precision measured ·
cost + review minutes + hard failure rate known. **Agent 3 optimizes review burden, not just token cost.**

**DO NOT add more primitives unless a real run forces them.**

**Do NOT:** build a generic ingestion framework · rebuild review workflow infra (OpenReview/Hypothesis/
Crossref exist) · let Hermes determine what Pāṭala knows · promote machine output without a scoped policy.

---

## THE SHARED BOUNDARY (the lanes converge on Ref IDs)

Agent 2 certifies the floor + state; Agent 1 derives upward; Agent 3 produces drafts. The join is
contractual: `Passage ID · PhilologicalProof ID · C1 ID · TranslationDecision ID · ReviewEvent ID` —
never fuzzy.

---

## THE GUARDRAILS (Agent 2 specific)

- Reviews are **immutable**; supersession preserves history, never erases it (≠ Hermes checkpoints).
- No agent tool can **accept/promote**; only PROPOSE/RECORD; promotion is scoped human policy.
- **Hermes hooks trigger recomputation; Pāṭala's dependency engine determines it.**
- Every proof dimension carries an honest status; no collapsed confidence number.
- `extraction_coverage: OPEN` ≠ `lexical_sense: OPEN` — never conflate.
- Keep the frozen P0 extractor; only fix reproducible loss bugs.
- Update `CLAIMS.md` + the handover honestly as each phase crosses its gate.

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

**The clean division (per the agent architecture):** Agent 2 = corpus compiler + integrity + state truth.
Agent 3 = translation factory (consumes NEXT_VALID_ACTION). Agent 1 = philosophical intelligence.

**Does NOT:** generate translations (Agent 3), write C1 / choose interpretive readings (Agent 1), promote
machine output to accepted scholarship, do argument extraction / themes / synthesis (Agent 1).

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

## THE CONCRETE SEQUENCE (where we're headed — updated)

```
CP1 floor ✅ (63/63)  →  corpus state ✅ (ledger)  →  review engine ✅ (Phase 3A)
   ↓
PHASE 3B  typed dependency propagation        (the 4 edge types — partially proven in 3A)
PHASE 3C  ImpactReport                         (✅ done in 3A)
PHASE 3D  MCP review tools                     (✅ BUILT: patala_get_review_state · patala_propose_review ·
          patala_submit_review · patala_get_impact · patala_simulate_review; the executable constitution)
PHASE 3E  tiny Scholar Workbench review screen
PHASE 3F  Hermes A4 scheduling                (LAST — Hermes orchestrates, it doesn't define semantics)
   ↓
(cross-lane) Agent 3 translation factory on kanban+cron  →  (later) BYOA over mcp.patala.org
```

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

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
> pipeline**. **Work LAYER BY LAYER**, each layer against its canonical spec + source files
> (`translations/_stack/ipvv/specs/*`, the L200 8-section spec, the C1-SPEC, the argument maps). Perfect
> L0 → commit → L1/L2 → commit → L200 → commit → C1 → commit → THEME → ESSAY → EDUCATION.

```
CP1 floor ✅ (63/63)  →  corpus state ✅ (ledger)  →  review engine ✅ (Phase 3A+3D)
   ↓
✅ 2026-08-13: FULL STACK WIRED — every layer (L0/L1/L2/L200/C1/THEME/ESSAY/EDUCATION) has a
   controller handler producing its canonical file shape + a layer-specific deterministic validator.
   The singular autonomous pipeline is now RUNNABLE end-to-end through autonomy.py.
   ↓
🔴 CP1 (the foundation proof): a MACHINE-LEARNING-VERIFIED L0 (or T1/L1/R1) READING
   Run the semantic-equivalence harness (docs/ML-L0-SEMANTIC-EQUIVALENCE-PROPOSAL.md) against the IPVV
   exemplar gold; prove our RAW-L0 is schema-isomorphic + validator-equivalent + P0-lossless +
   semantically-equivalent to the exemplar gloss (the ML part). Emit the mechanical proof. This becomes
   the reusable eval substrate for every downstream layer's own proof.
   ↓
PRIORITY (after CP1): autonomous end-to-end vertical proof on a real corpus subset —
   RAW SANSKRIT → SOURCE → L0 → L1 → L2 → L200 → C1 → THEME → ESSAY → EDUCATION, all through the
   controller, fail-closed, idempotent, provenance-bound.
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

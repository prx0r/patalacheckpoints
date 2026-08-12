# Agent 2 — INTEGRATION/CONTENT LANE INDEX

*The one living pointer for Agent 2's current state — done / in-progress / next. Update this as you
work. Append-only history lives under this folder; this file is the single "what is true right now"
source for the integration lane.*

> **LEADING CHECKPOINT DOC: `handover/CHECKPOINTS.md`** (the shared 5-checkpoint plan + 7 canonical
> contracts) + **`handover/agent-2-integration/CHECKPOINTS-INTEGRATION.md`** (this lane's goal:
> CP1 PhilologicalProof). Read those before the current-state below.

---

## THE FULL PROJECT MAP (what this lane sits inside — don't mistake the slice for the whole)

```
SOURCE (M00020/21/22 + Torella IPK)
  ↓  L0/L1  token-level + controlled translation     (l0/, l0_v1/ — the P0/P2/P3/P4 floor I certify)
  ↓  L2     real book prose                         (pilot/pilot_*_L2_read.md)
  ↓  L200   how each reading was derived (8-section audit, 63 files)  ← the audit link
  ↓  C1     what each passage means                 (c1/read/ + c1/source/)
  ↓  THEMES → PARALLELS → ESSAYS → EDUCATION
```
**Parallel translation stack (T1/T2/T3):** `01_t1` (28ch) + `02_t1` (35ch) = T1; `03_t2`, `05_t3` = T2/T3;
`02_r1`, `04_r2` = reviewer passes. Skills map these to checkpoints (translate-* → CP1).
**Product layer (the deliverable my floor feeds):** 34 API routes + 21 MCP tools — the deterministic
substrate (`resolve`, `hub`, `spines`, `themes`, 4 `verify_*`, `recommend`). Docs: `docs/api/`, `docs/openapi.yaml`, `mcp/`.
**Skills:** 7 (`assemble-stack`/`translate-passage`/`translate-work`/`validate-passage` → CP1;
`push-text` → CP4; `write-commentary` → CP3; `use-api` → CP2/CP9).
**Learning:** `docs/LEARNING_STRATEGY.md` (knowledge packets, research-once/distill-repeatedly).
**Honest completeness:** "35/35" = the V2/V3 published corpus, NOT all 63 chunks. 28 V1 legacy chunks
(`01_t1`) are `MIGRATION_PENDING`, 0/28, and are **this lane's known unfinished piece**.

---

## Lane

- **Role:** **CORPUS COMPILER + INTEGRITY LAYER** (not just "the L0 agent") — maintains the canonical
  machine-readable corpus state that Agent 3 (translation factory) safely operates on.
- **Owns:** `data/corpus/`, `app/`, `lib/`, `pipeline/` (incl. `verify_l0.py`, `corpus_state.py`),
  `translations/_stack/ipvv/specs/` + process notes.
- **Questions:** "What do we have, where is it, what state is it in, and can every artifact resolve?"
- **Does NOT:** generate translations (Agent 3), write C1 / choose interpretive readings (Agent 3/1),
  promote machine output to accepted scholarship, do argument extraction / themes / synthesis (Agent 1).
- **Rule:** "AI proposes ≠ Pāṭala asserts." Agent 2 is the build system / state truth; Agent 3 is the
  worker producing candidate artifacts; Agent 1 is the philosophical intelligence.
- **Do NOT:** build ML models or claim results; over-engineer the reader; wander into essay logic.

---

## Current state (2026-08-12)

### Done (the CP1 proof ladder, top to bottom)
- **Corpus published** — 49 IPVV passages as lazy-JSON (`data/published/ipvv/`), single source of
  truth via `getPublishedTranslation()` for both `/read` and `/api/resolve`.
- **Deterministic substrate** — C1 wired, c1_source derived (63), themes exposed, hub + spines + journey
  + analyst + recommend exposed.
- **Verification floor** — `lib/verify.ts` + `lib/citation.ts` + `/api/resolve`.
- **P0 FROZEN + VERIFIED — COMPLETE IPVV 63/63** — **V2/V3 35/35** (103,917 tokens, 0 unknown chars,
  0 bad spans, deterministic, independently re-verified) **+ V1 legacy 28/28** (NEW, 2026-08-12, via
  `pipeline/extract_l0_v1.py`, 91,714 tokens, `verify_l0.py` unchanged). The full flagship corpus now
  bottoms out in an auditable source span. Honest caveat: 63/63 proves two-format robustness, NOT
  cross-work generalization. Full record: `docs/BUILD_NOTES_L0_P0.md`.
- **P2 CALIBRATED + FROZEN as witness** (CLAIM **P-011**) — Vidyut×Heritage ensemble: control
  agreement 84–85%, Vidyut CONFLICT resolution 72%, true double-conflict ~9%, double-unanalyzed
  0.2%. Genuinely-blind 160-case review built but **unfilled** (non-blocking path to
  VALIDATED_AGAINST_HUMAN_GOLD). Full record: `docs/P2-ENSEMBLE.md` + `docs/P2_REVIEW_PROTOCOL.md`.
- **P3 lexical gold v0 + baselines; ranker REJECTED** (CLAIM **P-012**) — ranker.py top1=0.76 vs
  embedding baseline 0.81, 0 abstention, 100% false-certainty. NOT promoted to P3 witness. Gold =
  `docs/p3_lexical_gold_v0.json` (21 fixtures), eval = `docs/p3_lexical_eval_report.json`.
- **P4 alignment — FROZEN SUPPORTED_MACHINE_WITNESS** (P-013) — the meaningful **L0↔L2 term-anchor**
  task. Deterministic aligner: recall 0.93 / precision 0.89 / abstention 1.0 (35 passages / 105
  anchors). Independent Vidyut witness: 0.81 analyzed-only agreement. **Proposes/resolves likely
  anchor↔lemma links; does NOT prove semantic equivalence or replace human philology.** Frozen per the
  adequacy doctrine — do NOT keep tuning; revisit only on downstream failure. P4's uncertainty is
  metadata, not a blocker. Spec: `docs/P4_ALIGNMENT_SPEC.md`. Code: `pipeline/l0_align.py` +
  `pipeline/test_l0_align.py` (26/26 pass).

### In progress / next (in order — CP1: PhilologicalProof)
1. **P2 blind review** (160 cases) → VALIDATED_AGAINST_HUMAN_GOLD (P-011 promotion) — non-blocking.
2. **Deterministic related-rail** — `/api/recommend` + `recommend_related` MCP.
3. **Context alignment** — wire GRETIL IPK+Vṛtti+IPV into `/api/context`.
4. **Comparative matrix** — `comparative.ts` + seed.
5. **Argument truth-packet** — `pt:argument:` + `/verify-argument` (coordinates with Agent 1 CP4).
6. **PARALLELS** — typed cross-text witnesses.
7. **L200 → graph annotations** — keep the MT/IA split.
8. **Schema-version pin** — `data/published/ipvv/version.json`.
9. **Cross-work ingestion demo** (later) — ingest a second real work's T1 to demonstrate/confirm the
   L0 adapter generalizes (do NOT build a generic ingestion framework now).
10. **Autonomous-run supervisor** (deferred) — `pipeline/auto_run.py`: batch T1→L2→C1 per passage via
    existing run.py/skills, auto validate-passage+verify after each, stamp provenance (origin=machine,
    MACHINE_PROPOSED, never auto-accepted), stop on validation failure, batch report. Enables
    "translate while I sleep." Build AFTER git/vision formalization is committed.

Full thread list: `WHAT_NEXT_PATALA.md`.

---

## Open threads (flagged)
- The 6 downloaded IPV/IPK sources are NOT yet registered as hub/resources.
- IPVV 1.5.11 exemplar vs the 49-passage chunk store — keep 49 canonical, 1.5.11 as exemplar.
- Recommended related-rail spec not yet written as the product spec.

---

## Protocol
- Log every data-carrying handoff to `handover/LOG.md` with a schema snippet; bump the version pin on
  shape changes; keep provenance (never overwrite originals). Join with Agent ML on `Ref` IDs, never fuzzy.

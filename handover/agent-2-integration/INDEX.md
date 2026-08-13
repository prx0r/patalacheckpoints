# Agent 2 — INTEGRATION/CONTENT LANE INDEX

*The one living pointer for Agent 2's current state — done / in-progress / next. Update this as you
work. Append-only history lives under this folder; this file is the single "what is true right now"
source for the integration lane.*

> **GUIDING MISSION (READ FIRST): `handover/agent-2-integration/MISSION-AUTONOMOUS-FACTORY.md`** — the
> canonical long-horizon mission: CP0–CP10 ladder, checkpoint doctrine (NOT_BUILT→BUILT→VALIDATED→
> AUTONOMOUSLY_PROVEN), hard gates, anti-drift rules. Each checkpoint = a working system property, not a
> file. Work the ladder until terminal CP9 (full unattended SOURCE→C1) or a genuine blocker.
> **RAW→ENGLISH TRANSLATION (THE ACTUAL DELIVERABLE): Hermes (`hermes -z` via `pipeline/model.py::chat`)
> translates raw Sanskrit → English, driving the queue. Driver = `pipeline/auto_translate_raw.py` +
> `pipeline/batch_translate.py`. See `PROGRESS-AUTONOMOUS-2026-08-12.md` §"RAW → ENGLISH TRANSLATION VIA
> HERMES". Output = `data/corpus/downloads/translations/<work>.jsonl`, MACHINE_PROPOSED, idempotent by
> source_sha256. Run detached (`setsid nohup`), never foreground model calls.**
> **LEADING CHECKPOINT DOC: `handover/CHECKPOINTS.md`** (the shared 5-checkpoint plan + 7 canonical
> contracts) + **`handover/agent-2-integration/CHECKPOINTS-INTEGRATION.md`** (this lane's goal:
> CP1 PhilologicalProof). Read those before the current-state below.
> **DEV PLAN: `handover/agent-2-integration/DEV-PLAN.md`** — this lane's canonical execution plan (honest
> state + the RAW-L0 priority sequence + build order + guardrails). Read it before building.
> **SESSION HANDOVER: `handover/agent-2-integration/SESSION-2026-08-12.md`** — the complete record of this
> session's work + the honest current state + the highest-value next work. Read it first.
> **AUTONOMY BUILD RECORD: `handover/agent-2-integration/BUILD-RECORD-2026-08-12-AUTONOMY.md`** — the full
> inventory + results of the autonomous translation factory build (controller, registry, certificates,
> live L200 benchmark). **Read this for the current autonomous-factory state.**
> **VERTICAL WORKERS (2026-08-13): `handover/agent-2-integration/BUILD-RECORD-2026-08-13-VERTICAL-WORKERS.md`**
> — the canonical stack L0→L1→L2→L200→C1 now has per-layer workers each producing its canonical file shape
> + a layer-specific validator; L200 rewritten as the constrained compiler (default IGNORE); C1 wired
> (was a stub); THEME/ESSAY/EDUCATION wired to the Hermes-skill worker. Proof: `pipeline/prove_vertical.py`
> (3 real kramasadbhava L0 → L1→L2→L200→C1, fail-closed, ALL PASS). The live `auto_translate_raw.py` runner
> is untouched.
> **CURRENT STATE (READ FIRST): `handover/agent-2-integration/SESSION-2026-08-13.md`** — **WE GOT IT RUNNING**:
> the autonomous translation factory is live. Hermes (`hermes -z`) translates the full 73-work RAW_SANSKRIT
> queue to MACHINE_PROPOSED English, unattended + watchdog-survivable. Driver =
> `pipeline/auto_translate_raw.py`, engine = `pipeline/batch_translate.py` → `model.chat` → `hermes -z`.
> Watchdog = `pipeline/watchdog_auto_translate.sh` (cron every 5 min, PATH-fixed). Progress:
> `/tmp/opencode/auto-translate.log` + `data/corpus/downloads/translations/`. The 3 unblocking fixes:
> (1) gloss off the L0 commit gate, (2) generative stage = Hermes not a stub, (3) watchdog PATH bug.
> **CURRENT STATE (READ FIRST): `handover/agent-2-integration/PROGRESS-AUTONOMOUS-2026-08-12.md`** — what is
> VERIFIED / CLOSE-unverified / STILL-NEEDED + the file map + the agent-1 scholarly-oracle handover
> location + the background-run working practice.
>
> **THE CANONICAL LAYER STACK (the authoritative layer definitions — NOT in app/api or mcp, they live on
> the mount `…/sanskritree/translations/_stack/ipvv/`):**
> - `sourcetranslationprompt.md` (R2 original; `/tmp/opencode/sourcetranslationprompt.md`) → `c1/C1-SPEC.md` (imported) — the full `L2 → L200 → C1 → THEME → ESSAY → EDUCATION` stack + the C1 spec.
> - `c1andmore.md` — the universal stack + the 4 human zoom questions.
> - `l200/README-L200-SPEC.md` — the frozen 8-section L200 audit spec (derivation map, MT/IA taxonomy, typed crossrefs, review state).
> - `IPVV-KNOWLEDGE-CORE.md`, `HANDOVER-IPVV-LAYERS-2026-08-12.md`, `c1context.md`, `README.md`.
> The pipeline CODE is `pipeline/` (patala repo); these are the layer DEFINITIONS the autonomy layer-skills
> (`skills/autonomous-layer/`) must map onto: **L0 → L2 → L200 → C1 → THEME → ESSAY**.

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
**Honest completeness:** the IPVV flagship is **63/63 L0 lossless** (V2/V3 35/35 + V1 legacy 28/28).
Cross-work generalization to other Śaiva works is NOT yet demonstrated — the raw-Sanskrit source-L0
mode (kramasadbhava etc.) remains a known seam. See `CHECKPOINTS-INTEGRATION.md`.

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
- **Corpus state machine (the Agent-3 control plane)** — `pipeline/corpus_state.py` computes per-work
  state from ACTUAL disk truth (source format, translation stage, L0 status, proof, review) + the
  transition contract `NEXT_VALID_ACTION(work)` + `eligible_for_agent3`. Served via
  `GET /api/corpus/state`. Ledger: `data/corpus/downloads/translation-state-ledger.json` (45 works).
  Test: `pipeline/test_corpus_state.py` (11/11 pass).
- **Executable-corrections review engine (Phase 3A — THE MOAT)** — `pipeline/review_engine.py`: a
  scholar's judgment is an immutable, provenance-carrying graph mutation (append-only ReviewEvent →
  deterministic reducer → DerivedState → ImpactReport), NOT prose. Vertical loop proven over ARG-002
  (G2-TC2 v1→v2): v1 retained, G2-INF1/G2-CONC → NEED_REVIEW, ARG-004 untouched, idempotent. Doctrine
  holds: ACCEPT≠truth, REJECT≠delete, REVISE≠overwrite. Test: `pipeline/test_review_engine.py` (15/15).

### In progress / next (in order — the updated plan)
1. **🔴 AGENT 3 TRANSLATION FACTORY — THE PRIORITY.** The closed-loop factory: A2 `NEXT_VALID_ACTION`
   → A3 production (Hermes kanban + cron + `model.py`, T1→L2→C1) → MACHINE_PROPOSED artifacts → A2
   validate + state update → review/correction (the Phase-3 engine). Milestone: one legacy work through
   the full factory, producing L0-linked translation/C1 proposals with provenance, then one output
   through the review protocol. Measure cost / failure / review burden.
2. **Phase 3E tiny Workbench screen** — deferred until a real reviewer is ready; minimal only.
3. **Phase 3F Hermes A4 scheduling** — LAST, after the human workflow is proven.
4. **P2 blind review** (160 cases) → VALIDATED_AGAINST_HUMAN_GOLD (P-011 promotion) — non-blocking.
5. **Cross-work L0 generalization** (later) — ingest a second real work to demonstrate the adapter generalizes.
6. **Schema-version pin** — `data/published/ipvv/version.json`.

Full thread list: `WHAT_NEXT_PATALA.md`. Canonical plan: `CHECKPOINTS-INTEGRATION.md`.
**Priority re-anchor:** autonomous translation is the headline; the review-engine work is the validation
substrate, not the goal. See `SESSION-PROGRESS-AUTONOMOUS-TRANSLATION.md`.

---

## Open threads (flagged)
- The 6 downloaded IPV/IPK sources are NOT yet registered as hub/resources.
- IPVV 1.5.11 exemplar vs the 49-passage chunk store — keep 49 canonical, 1.5.11 as exemplar.
- Recommended related-rail spec not yet written as the product spec.

---

## Protocol
- Log every data-carrying handoff to `handover/LOG.md` with a schema snippet; bump the version pin on
  shape changes; keep provenance (never overwrite originals). Join with Agent ML on `Ref` IDs, never fuzzy.

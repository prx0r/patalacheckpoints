# ONBOARDING — one place for complete context, then specialize

*2026-08-12. This folder organizes the EXISTING docs (no content rewritten — every entry points to
the original file) into a single staged read that gives a new agent complete context, then routes them
to their lane. Read top to bottom; then follow the specialization gate for your track.*

> **FIRST, the one rule (auto-loaded, non-negotiable):** `../AGENTS.md`
> Every Pāṭala agent reads this before any build. Nothing is "real" because code exists — only
> independent gold + blind eval + metric + human adjudication makes it real.

> **AND the live agent system:** `../handover/SYSTEM.md` — the agnostic template (`agent0`) → live
> instances (`agent1`/`agent2`), with tracked progress in `../handover/STATE.yaml` via
> `python3 ../handover/flow.py status`. Know your instance's live checkpoints before you start.

---

## STAGE 0 — THE GATE (read before ANY build)

| # | Doc | Why |
|---|---|---|
| 0 | `../AGENTS.md` | THE ONE RULE + the enforcement gate (auto-loaded; read first) |
| 0b | `../machinelearning/AGENTS-DOCTRINE.md` | the master doctrine: 3 categories, 9-field contract, epistemic labels, banned words, abstention, human adjudication |
| 0c | `../machinelearning/theatre_check.py` | run `python3 machinelearning/theatre_check.py --status` — the honest component status |
| 0d | `../machinelearning/CLAIMS.md` | the project's own audit ledger (P-001…P-008) — check before claiming anything works |

## STAGE 1 — THE VISION (what we're building)

| # | Doc | Why |
|---|---|---|
| 1 | `../VISION_AND_NAVIGATION.md` | THE vision + 8-step logical progression + navigation across the 3 homes |
| 1b | `../docs/global/GLOBAL-STATE-2026-08-13.md` | **READ THE TIMESTAMPED GLOBAL CHECKPOINT EARLY** — the current-state orientation snapshot (big picture, discipline, architecture, the CURRENT DIRECTION: scholar-corpus foundation S0 + scholar oracle + evaluation plane). Stale by design — a snapshot, later docs supersede it. |
| 1c | `../docs/vision/INDEX.md` | the full vision arc (Vision 01–13) + foundational strategy + the vision→borrowed-tools map |
| 1d | `../machinelearning/dualagentvision.md` | the master derivation graph + the two-agent split + CP0–CP12 checkpoint ladder |
| 1e | `../machinelearning/dualagentvision-ADAPTED.md` | the vision mapped onto our ACTUAL infra (per-checkpoint real state) |
| 1f | `../source-evidence/docs/` (reuse-first + INTEGRATION-SPEC + tools/) | **the current direction**: the source-evidence substrate (S0) + the scholar-corpus corroboration oracle + the reuse-first doctrine (borrow tools, build only the epistemic graph) |

> **If you are Agent 1, read `../handover/agent-1-ml/HANDOVER-2026-08-13.md`** (the full current handover) after this stage — the ML vertical is frozen + peer-review-clean; the forward work is the scholar-corpus foundation (S0), starting with the Inspect AI prototype.

## STAGE 2 — THE MAP (where everything lives)

| # | Doc | Why |
|---|---|---|
| 2 | `../docs/INDEX.md` | the canonical flat docs index (ONE source of truth per concern) |
| 2b | `../handover/README.md` | the coordination folder for both lanes + the rules that stop status rot |
| 2c | `../docs/README.md` | the machine-first doc home (pipeline → API → MCP → site) |
| 2d | `../machinelearning/README.md` | the ML lane's doc home |

## STAGE 3 — THE FULL SYSTEM (the scholarly factory, how it works)

| # | Doc | Why |
|---|---|---|
| 3 | `THE_COMPANION.md` (sanskritree `_stack/ipvv/specs/`) | the full-system onboarding: the whole scholarly factory |
| 3b | `../docs/PHASE1_IPVV_CORPUS_PROCESS_NOTES.md` | how the flagship IPVV corpus was built |
| 3c | `../docs/SCHOLARLY_GRAPH.md` | the durable data model (objects / annotations / events) |
| 3d | `../docs/TRANSLATION_PROTOCOL.md` | the translation as versioned, passage-linked claims |

---

## THE SPECIALIZATION GATE (after Stages 0–3, choose your track)

```
You are an AGENT. The shared context (Stages 0–3) is complete. Now specialize:

AGENT L0 — VERTICAL TRUTH          AGENT ML — HORIZONTAL/UPWARD
"is this reading licensed by        "does this higher representation
 the source?"                       legitimately derive from the
                                     objects beneath it?"
  → machinelearning/SPEC_L0_PROOF.md   → machinelearning/AGENT1-HANDOVER.md
  → machinelearning/SPEC_L0_STANDARDIZATION.md  → machinelearning/MLUSEINPATALA.md
  → handover/agent-2-integration/INDEX.md       → handover/agent-1-ml/INDEX.md
  → docs/BUILD_NOTES_L0_P0.md                    → machinelearning/DEVPLAN.md
  → docs/BUILD_NOTES_L0_P2.md
  → docs/L0_REVIEW_OLDSANSKRITREE_ENGINE.md

JOIN ON (the contractual boundary — never fuzzy):
  Passage ID · TranslationDecision ID · PhilologicalProof ID · C1 ID
```

---

## THE L0 LANE, in full (current state + working notes)

| Doc | What |
|---|---|
| `machinelearning/SPEC_L0_STANDARDIZATION.md` | the verifiable-substrate spec (schema + invariants) |
| `machinelearning/SPEC_L0_PROOF.md` | the proof-carrying philological-translation spec (P0–P7 + infra survey) |
| `pipeline/verify_l0.py` | the P0 proof harness (source coverage, lossless) |
| `pipeline/verify_l0_p2.py` | the Vidyut P2 morphology witness |
| `docs/BUILD_NOTES_L0_P0.md` | build record: coordinate fix, tokenizer repairs, 35/35 V2/V3 lossless |
| `docs/BUILD_NOTES_L0_P2.md` | build record: Vidyut P2 result + proof-semantics separation |
| `docs/L0_REVIEW_OLDSANSKRITREE_ENGINE.md` | reusable pieces from the old translation engine |
| `docs/l0_reviewed_exceptions.json` | the reviewed-exception classification (V2/V3 P0) |
| `translations/_stack/ipvv/specs/l0_schema.json` | the L0 record contract |
| `translations/_stack/ipvv/specs/l0_coverage.json` | the lossless/coverage taxonomy |
| `translations/_stack/ipvv/specs/SPEC_L0_L1.md` | the L0→L1 factory spec |

## THE ML LANE, in full (current state + working notes)

| Doc | What |
|---|---|
| `machinelearning/AGENT1-HANDOVER.md` | the ML lane handover |
| `machinelearning/MLUSEINPATALA.md` | the frozen ML strategy |
| `machinelearning/DEVPLAN.md` | the ML dev plan |
| `machinelearning/BENCHMARK_HANDOVER.md` | the benchmark seed |
| `machinelearning/COMPONENT-CONTRACTS.md` | the anti-theatre 9-field contract per component |
| `machinelearning/CLAIMS.md` | the audit ledger (both lanes maintain) |

---

## THE CROSS-LANE LOG

- `../handover/LOG.md` — every handoff (what · why · file · date · direction · schema). Read the last
  entries before starting; append yours when you finish.

---

*This folder is the single on-ramp. It organizes existing docs only — nothing here is a new authority;
each entry is the canonical original. If a link breaks, fix the link, not the underlying doc.*

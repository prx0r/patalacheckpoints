# AGENT 2 — CONTEXT-ENGINEERING HANDOVER REVIEW (2026-08-12)

*Dated with the other handovers. This records the full-context onboarding of the next Agent 2 — the
context-engineering pass that turned a fresh agent into a master of the lane — plus the staleness fixes
and the new canonical dev plan made in the same session. It is the review of what was learned + what was
changed, for the next agent.*

---

## 1. THE ONE-LINE STATE

**The next Agent 2 passed the mandatory 27-doc context gate (27/27, PASS), read the full pipeline it
owns + the hermes northstar + the production doctrine, verified the live infra is real (63/63 L0,
RAW-L0 core, 12 eligible works, 21 targets, 39 leads, 4 committed Kramasadbhāva L0 versions), then
fixed the shared-doc staleness and produced a canonical DEV-PLAN + this dated handover.**

---

## 2. WHAT THE FRESH AGENT READ (the context-engineering pass)

### The enforced context gate — `handover/context_gate.py --begin agent2` → confirm all 27 in order
1. **Identity + operating rule:** `AGENTS.md`, `handover/SYSTEM.md`, `AGENTS-DOCTRINE.md` (the 3
   categories, 9-field contract, banned words, abstention, adequacy doctrine, git discipline).
2. **The ledger:** `CLAIMS.md` (P-001 L0 63/63 SUPPORTED · P-011 P2 witness · P-012 ranker REJECTED ·
   P-013 P4 frozen · P-014 vertical serialization).
3. **The vision (highest level first):** `VISION_AND_NAVIGATION.md`, `docs/vision/CORE-BIBLE.md`,
   `docs/vision/INDEX.md`, `dualagentvision.md` + `-ADAPTED.md`.
4. **The map:** `docs/INDEX.md`, `handover/README.md`, `docs/README.md`.
5. **Execution + contracts:** `handover/CHECKPOINTS.md`, `COMPONENT-CONTRACTS.md`.
6. **The scholarly system:** `docs/PHASE1_IPVV_CORPUS_PROCESS_NOTES.md`, `docs/SCHOLARLY_GRAPH.md`,
   `docs/TRANSLATION_PROTOCOL.md`.
7. **The lane (ending at the latest handover):** `ORIENTATION.md`, `CHECKPOINTS-INTEGRATION.md`,
   `verify_l0.py`, `verify_l0_p2.py`, `BUILD_NOTES_L0_P0.md`, `BUILD_NOTES_L0_P2.md`, `P2-ENSEMBLE.md`,
   `P2_REVIEW_PROTOCOL.md`, `P3_EDITORIAL_REVIEW.md`, `INDEX.md`.

### The full system surface (beyond the gate)
- The **site/API/MCP**: `docs/api/README.md` (34 routes), `docs/openapi.yaml`, `docs/api/mcp.md` (21+
  tools), `app/api/`, `data/atlas/`, `mcp/index.mjs`.
- The **pipeline it owns**: `raw_l0.py`, `agent3_batch.py`, `agent3_queue.py`, `l0_registry.py`,
  `translation_targets.py`, `corpus_state.py`, `review_engine.py`, `build_corpus_targets_db.py`.
- The **hermes execution layer**: `AUTOTRANSLATE-NORTHSTAR.md` (the immediate objective),
  `TRANSLATION-APPROACH-AND-VALIDATION.md` (production doctrine), `CANONICAL.md`.

### The verified live state (the gates passed)
```
context_gate --status agent2   → CONTEXT GATE: PASS (27/27)
check_staleness.py             → SYSTEM CLEAN (0 failures)
flow.py status                 → state_version 21; agent2 CP1 PARTIAL (RAW-L0 factory core built)
agent3_queue.py --list         → 12 eligible RAW-L0 works (kramasadbhava first)
agent3_queue.py --registry     → 21 prioritized targets
agent3_queue.py --leads        → 39 tracked leads
l0_registry.py                 → kramasadbhava v1–v4 immutable, committed
```

---

## 3. WHAT THE MASTER AGENT NOW KNOWS (the carry-forward knowledge)

- **Role:** corpus compiler + integrity layer. Lane `SOURCE → L0 → corpus state → RAW-L0 factory →
  versioned L0 → review`. Owns `data/corpus/`, `app/`, `lib/`, `pipeline/`, `handover/agent-2-integration/`.
  Does NOT touch `benchmarks/v0/` or `machinelearning/research/patala_ml/` (Agent 1).
- **The doctrine's hard lines:** nothing is real because code exists; validation is the gate; a wrong
  translation is worse than none; L0 immutable/versioned; proof dimensions separate (never a collapsed
  confidence); `extraction_coverage: OPEN ≠ lexical_sense: OPEN`; IDs resolve on `Ref` only, never fuzzy.
- **The immediate priority:** wire the **gloss/model transport** for `literal_gloss` (the top gap), then
  the **Sanskrit-only replay benchmark** (the Pāṭala-Evals embryo), then **ingest primary texts**, then
  **Kramasadbhāva first cross-work run**. Hermes is unreliable on this box; the deterministic core works
  without it.

---

## 4. THE STALENESS FIXED THIS SESSION (shared docs, Agent 2's own + shared coordination)

| Doc | What was stale | Fix |
|---|---|---|
| `docs/README.md` | §strategy corpus-side pointed to `../../sanskritree/corpus/targets/`; the goldmine was consolidated into `docs/corpus/` | repointed to the consolidated `docs/corpus/` home + the targets DB |
| `handover/README.md` | Agent 2 lane described as "integration/content" (legacy) | → **corpus compiler + integrity** (formerly L0 agent), with the current `owns` |
| `VISION_AND_NAVIGATION.md` §4 | Agent 2 "INTEGRATION/CONTENT owns hub/PUSHING/..." (legacy framing) | → **corpus compiler + integrity owns data/corpus/app/lib/pipeline + source→L0→proof + RAW-L0 factory + state machine** |
| `VISION_AND_NAVIGATION.md` §5 checklist | "ML vs integration" | → "ML/research vs corpus-compiler + integrity" |
| `machinelearning/DUAL_AGENT_TRACK.md` | **missing** (archived; live path referenced by INDEX/handover/VISION) | recreated at the live path with the current 3-role split (A1 ML · A2 corpus compiler + integrity · A3 translation factory), concise, linking the archived deep version |
| `docs/INDEX.md` | (left as-is — it correctly pointed to the live paths, now restored) | — |

**Nothing was touched in Agent 1's lane** (`benchmarks/v0/`, `machinelearning/research/patala_ml/`,
`handover/agent-1-ml/`).

---

## 5. THE NEW CANONICAL DEV-PLAN

`handover/agent-2-integration/DEV-PLAN.md` — the lane's single authoritative execution plan: the honest
state (63/63 L0, P2/P4 witnesses, RAW-L0 core, review engine), the 4-step priority sequence (gloss
transport → replay → ingest → Kramasadbhāva), the Builds 1–6 order, the factory certificate (false
certainty = the killer metric), the queue usage, the goldmine pointer, and the guardrails. Linked from the
lane `INDEX.md`.

---

## 6. OPEN / NOT DONE (honestly)

- **Nothing in Agent 1's lane** was touched (per the guardrail).
- `docs/INDEX.md` + `handover/README.md` still list `docs/vision/INDEX.md`'s lens folders and other docs
  that were verified present; no further churn needed.
- The **gloss/model transport** (the top build gap) is documented, not built this session — it needs a
  decision on the transport (Hermes vs a direct model call) which is a build, not a doc fix.

---

## 7. THE ONE-SENTENCE CARRY-FORWARD

**The next Agent 2 holds the full context (27/27 gate PASS), the fixed shared docs, a new canonical
DEV-PLAN, and this dated handover; the immediate work is the gloss/model transport → the Sanskrit-only
replay → Kramasadbhāva first — holding the doctrine's hard line that validation is the gate, a wrong
translation is worse than none, and L0 stays immutable/versioned.**

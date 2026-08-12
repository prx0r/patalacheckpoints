# AGENT 2 — SESSION PROGRESS + THE AUTONOMOUS-TRANSLATION RE-ANCHOR

*2026-08-12. What Agent 2 actually built this session, and the honest re-anchor: **autonomous translation
is the priority**; the peer-review/executable-corrections work is a real, tested substrate but it is
DOWNSTREAM of the translation floor, not the headline. This doc records both so we don't lose track.*

---

## PART A — WHAT WAS BUILT (this session, all tested + committed on `agent2`)

### A1. The IPVV source floor is COMPLETE — 63/63 lossless, frozen
- **V2/V3 35/35** (103,917 tokens, 0 unknown) — was already done.
- **V1 legacy 28/28** (NEW) — `pipeline/extract_l0_v1.py` turns the legacy prose format into canonical L0
  records; `verify_l0.py` passes **UNCHANGED**. This closes the "35/35 vs 63" gap.
- Honest caveat: proves two-format robustness, NOT cross-work generalization.

### A2. The corpus state machine — the Agent-3 control plane
- `pipeline/corpus_state.py` computes per-work state from ACTUAL disk truth: source availability + format
  (AND_GLOSS / RAW_SANSKRIT), translation stage, L0 status, proof, review — plus the transition contract
  `NEXT_VALID_ACTION(work)` and `eligible_for_agent3`.
- Served read-only via `GET /api/corpus/state`. Ledger: 45 works. (11/11 tests)

### A3. The executable-corrections review engine — Phase 3A (the moat)
- `pipeline/review_engine.py`: a scholar's judgment is an immutable, provenance-carrying **graph mutation**,
  not prose. Append-only `ReviewEvent` → deterministic reducer → `DerivedState` → `ImpactReport`.
- Vertical loop proven over ARG-002 (G2-TC2 v1→v2 REVISE): v1 retained, G2-INF1/G2-CONC → NEED_REVIEW,
  ARG-004 untouched, idempotent. Doctrine holds: ACCEPT≠truth, REJECT≠delete, REVISE≠overwrite. (15/15 tests)

### A4. The Hermes execution-kernel docs (vision + infra layer)
`handover/hermes/` (CANONICAL, DEV-PLAN, PATALA-SETUP, PEER-REVIEW, BACKEND-MODEL) + the Vision×Hermes map
(`docs/vision/functionality/hermes-execution.md`). The corrected thesis: **Hermes is Pāṭala's replaceable
execution kernel, NOT its epistemic backend.**

---

## PART B — THE HONEST PRIORITY CHECK

**The headline goal is AUTONOMOUS TRANSLATION**: "translate while I sleep." Everything above serves it
in this dependency order:

```
source floor (63/63)   ← the hard, foundational unlock      ✅ DONE
     ↓
corpus state machine   ← Agent 3's control plane            ✅ DONE
     ↓
Agent 3 translation factory (kanban + cron)                 ← THE ACTUAL GOAL — NOT YET BUILT
     ↓
review engine          ← what validates Agent 3's output    ✅ DONE (Phase 3A)
     ↓
peer review / workbench ← the scholar-facing product        ← downstream (later)
```

**The gap:** the **Agent 3 translation factory** — the thing that actually translates while you sleep — is
still not built. It's the missing link between the corpus state machine (which says what to do) and the
actual translation work.

**The honest assessment of the peer-review work:** it's real and tested, and the review engine is genuinely
the right substrate for validating Agent 3's machine-proposed drafts (auto-validate after each translation,
per the original auto_run.py design). But **I let it pull focus from the translation factory itself.** The
review engine does NOT need to be finished (3D/3E/3F) before Agent 3 can translate — Agent 3 just needs the
corpus state machine + a way to run translations + a validation gate.

---

## PART C — THE PATH TO AUTONOMOUS TRANSLATION (the priority)

The Agent 3 translation factory, in the minimal shape that "translates while I sleep":

```
Agent 2 ledger (/api/corpus/state) → NEXT_VALID_ACTION (e.g. "GENERATE_TRANSLATION" for an eligible work)
     ↓
Hermes kanban task (claimed by patala profile) + cron (the sleep-time scheduler)
     ↓
pipeline/model.py (already shells to hermes) → T1 → L2 → C1   ← the translation pass
     ↓
auto-validate: verify_l0 / validate-passage / (the review engine as a gate)
     ↓
stamp MACHINE_PROPOSED provenance → write back to the ledger → next eligible task
```

**The minimal blockers to clear (in order):**
1. **Seed the patala profile + project** (hermes profile/project create) — the runtime env.
2. **Pick the first eligible target** — the ledger already shows kramasadbhava etc. are RAW_SANSKRIT-blocked;
   so the first translation target needs an AND_GLOSS/legacy work that's L0-able, OR the raw-Sanskrit L0 mode.
3. **Build the one translation job** — a kanban task + cron that runs one eligible work through `model.py`.
4. **Auto-validate after each** — the review engine (already built) as the gate, fail-closed.

---

## PART D — WHAT TO KEEP vs. DEFER (for the coordinator)

**Keep / prioritize:**
- ✅ Source floor (63/63) — the foundation.
- ✅ Corpus state machine — the control plane; it's what makes autonomous translation *safe* (fail-closed).
- ⬜ **Agent 3 translation factory — THE PRIORITY.** Build it next.
- ✅ Review engine (Phase 3A) — reusable as the validation gate; don't expand it now (adequacy doctrine).

**Defer (downstream, do NOT pull focus):**
- Phase 3D/3E/3F (MCP review tools, Workbench screen, Hermes A4 scheduling).
- BYOA / mcp.patala.org / the corrections dataset.
- Cross-work L0 generalization (until a second real work is actually being translated).

---

## THE ONE-SENTENCE CARRY-FORWARD

**Autonomous translation is the priority; the source floor (63/63) and corpus state machine are done and
are exactly what make it safe; the next build is the Agent 3 translation factory (kanban + cron +
`model.py` + auto-validate) — and the review engine built this session is the validation gate for it,
not a distraction to keep building.**

---

## UPDATE (2026-08-12, later) — Phase 3D done; priority resets to Agent 3 factory

**Phase 3D is complete** (`0ca6173`): the review layer crossed from architecture into a usable protocol
surface. The core invariant is now enforceable outside the repo:
```
machine → propose (patala_propose_review, origin=MACHINE, status=PROPOSED, NO state change)
authorized scholar → review (patala_submit_review, actor_kind + scope)
Pāṭala → compute consequences (the deterministic reducer + ImpactReport)
```
Plus `patala_get_review_state` + `patala_simulate_review` (zero-write counterfactual). 23/23 tests.

**Priority RESET — the headline is the Agent 3 translation factory.** The review layer gives the factory
the validation gate it was missing. The first real closed-loop Pāṭala factory:
```
A2 source + corpus state → NEXT_VALID_ACTION
A3 translation production → MACHINE_PROPOSED artifacts
A2 validation + state update
A4/Phase3 review proposals + corrections → executable downstream impact
```

**The concrete next milestone:**
> Take one legacy work through the full autonomous factory on Hermes, producing modern L0-linked
> translation/C1 proposals with provenance, then pass one output through the new review protocol.

**That proves:** source → autonomous production → validated machine proposal → review → executable
correction.

**Priority order (per the coordinator):**
```
1. Agent 3 factory calibration run
2. one genuine untranslated target
3. measure cost / failure / review burden
4. tiny 3E screen when a real reviewer is ready
5. Hermes A4 scheduling after the human workflow is proven
```

**Do NOT add more primitives** unless a real factory/review run forces them — the risk is now architecture
drift. 3E stays minimal (object · evidence · current state · proposal/review controls · impact preview ·
submit) — no dashboards/profiles/queues/social/reviewer-discovery.

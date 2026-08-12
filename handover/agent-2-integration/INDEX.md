# Agent 2 — INTEGRATION/CONTENT LANE INDEX

*The one living pointer for Agent 2's current state — done / in-progress / next. Update this as you
work. Append-only history lives under this folder; this file is the single "what is true right now"
source for the integration lane.*

> **LEADING CHECKPOINT DOC: `handover/CHECKPOINTS.md`** (the shared 5-checkpoint plan + 7 canonical
> contracts) + **`handover/agent-2-integration/CHECKPOINTS-INTEGRATION.md`** (this lane's goal:
> CP1 PhilologicalProof). Read those before the current-state below.

---

## Lane

- **Role:** integration + scholarly content + docs + Sanskrit substrate (the L0 philological floor).
- **Owns:** `data/`, `app/`, `lib/`, `pipeline/`, the reader/API/MCP, the factory,
  `translations/_stack/ipvv/specs/` + process notes.
- **Rule:** "AI proposes ≠ Pāṭala asserts." Expose scholarly structure as addressable data (schema
  snippets), keep the L200/C1 discipline, preserve provenance.
- **Do NOT:** build ML models or claim results (that's Agent 1); over-engineer the reader before the
  data/API is complete; wander into essay logic.

---

## Current state (2026-08-12)

### Done
- **Corpus published** — 49 IPVV passages as lazy-JSON (`data/published/ipvv/`), single source of
  truth via `getPublishedTranslation()` for both `/read` and `/api/resolve`.
- **Deterministic substrate** — C1 wired, c1_source derived (63), themes exposed, hub + spines + journey
  + analyst + recommend exposed.
- **Verification floor** — `lib/verify.ts` + `lib/citation.ts` + `/api/resolve`.
- **P0 FROZEN + VERIFIED** — V2/V3 **35/35 PASS** (103,917 tokens, 0 unknown chars, 0 bad spans,
  deterministic, independently re-verified). This is CP1's foundation. V1 (28 chunks) is a separate
  legacy format, `MIGRATION_PENDING`. Full record: `docs/BUILD_NOTES_L0_P0.md`.

### In progress / next (in order — CP1: PhilologicalProof)
1. **Heritage ensemble → P2 disagreement analysis** — run Heritage over all Vidyut CONFLICT + UNANALYZED
   + a stratified control (~500 CONFIRMED, ~500 AMBIGUOUS_SUPPORTED) → Vidyut×Heritage confusion matrix.
2. **Lexical gold** (~50–100 fixtures incl. NO-UNIQUE-SENSE abstain) → ranker benchmark (baselines:
   most-common gloss / local L0 gloss / embedding) before ranker.py becomes a witness.
3. **Alignment gold** (held-out from manually checked L0 pairs) → alignment benchmark.
4. **Deterministic related-rail** — `/api/recommend` + `recommend_related` MCP.
5. **Context alignment** — wire GRETIL IPK+Vṛtti+IPV into `/api/context`.
6. **Comparative matrix** — `comparative.ts` + seed.
7. **Argument truth-packet** — `pt:argument:` + `/verify-argument` (coordinates with Agent 1 CP4).
8. **PARALLELS** — typed cross-text witnesses.
9. **L200 → graph annotations** — keep the MT/IA split.
10. **Schema-version pin** — `data/published/ipvv/version.json`.

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

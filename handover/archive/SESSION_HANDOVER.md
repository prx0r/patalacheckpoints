# SESSION HANDOVER — docs created this session + recommended next work

*2026-08-12. Everything I created this session, where it lives, and the recommended next
work (L0 standardization). A new agent should read this, then `VISION_AND_NAVIGATION.md` +
`docs/INDEX.md`, then pick up the recommended task.*

---

## 1. THE SESSION'S DELIVERABLES (in order of creation)

### Vision & navigation (the map for any agent)
- **`VISION_AND_NAVIGATION.md`** (repo root) — the one entry point: vision, 8-step logical
  progression, navigation across the 3 homes, the 2-track split, review checklist.

### The scholarly/integration layer
- **`machinelearning/COMPOUNDING_RESEARCH_SYSTEM.md`** — the source-as-hub model + the
  PUSHING→argument→essay→learning compounding loop.
- **`machinelearning/SPEC_LOGICAL_ARGUMENTS_GOLD.md`** — logical arguments as the gold (the
  truth-packet pipeline).
- **`machinelearning/SPEC_ARGUMENT_TRUTH_PACKET.md`** — the light argument-as-translation model
  (strength-graded PROVED→SPECULATIVE).
- **`data/corpus/hub.ts` + `/api/hub` + `get_work_hub` MCP** — the source hub (every work tracks
  its essays/arguments/pushing/learning).
- **`data/corpus/canonical-spines.ts` + `/api/spines` + `get_school_spine` MCP** — the per-school
  reading path.
- **`data/corpus/themes.ts` + `/api/themes` + `get_themes` MCP** — deterministic theme proposals.

### The PUSHING method (research-library)
- **`pushing/PUSHING_GUIDE.md`** — the formal method.
- **`pushing/AUTONOMOUS_PUSHING_AGENT_SPEC.md`** — the self-contained "create a pushing file"
  instruction (question-context first, loop to repeats).
- **`pushing/QUESTIONNAIRE_REAL_DNA.md`** — the real question DNA from the Q1–Q25 + Logicvids.
- **`pushing/SPEC_COMPARATIVE_PUSHING.md` + `DESIGN_LAYERED_COMPARATIVE_QUESTIONNAIRE.md`** — the
  agnostic core + tradition modules comparative matrix.
- **`pushing/_source/`** — the consolidated Logicvid source files.

### The verification floor (deterministic services, live)
- **`lib/verify.ts` + `/api/verify/{quote,claim-structure,trace-dependency,counterevidence}` + 4 MCP**
  — the deterministic floor ("AI proposes ≠ Pāṭala asserts" as machine access).
- **`lib/citation.ts` + `/api/resolve` + `resolve_ref` MCP** — the citation backbone (immutable ids).

### The education layer (vision + built primitives)
- **`machinelearning/EDUCATION_VISION.md`** — the graph-native teaching engine vision.
- **`machinelearning/geometric.md`** — mechanisms borrowed from the HXRMXS/TPN engine.
- **`data/corpus/journey.ts` + `/api/journey` + `get_journey` MCP** — the graph-owned guided path.
- **`data/corpus/analyst.ts` + `/api/analyst` + MCP** — the metacognitive `my_thoughts` layer.
- **`data/corpus/recommend.ts` + `/api/recommend` + `recommend_related` MCP** — the related-text rail.

### System growth + the Library
- **`machinelearning/SYSTEM_GROWTH_AND_HERMES.md`** — the growth loop + Hermes infra decision.
- **`machinelearning/PATALA_AS_LIBRARY_ENGINE.md`** — Pāṭala as the engine for the `.meta/` Library
  (4 wings as register-projections).
- **`machinelearning/WHAT_NEXT_PATALA.md`** — the open threads + priorities.

### Context engineering (the 2-track agent system)
- **`machinelearning/CONTEXT_ENGINEERING.md`** — shared context → two lanes (ML vs integration).
- **`machinelearning/DUAL_AGENT_TRACK.md`** — the two-lane split + handoff protocol.

### API/docs refresh (clean, current)
- **`docs/openapi.yaml`** — added 8 missing routes (resolve, spines, themes, hub, 4×verify) + fixed
  a YAML bug; now 34 paths.
- **`docs/api/README.md`** + **`docs/api/mcp.md`** — updated to all 35 routes / 21+ MCP tools.
- **`docs/INDEX.md`** — the canonical map (all the above linked).
- **`docs/PHASE1_IPVV_CORPUS_PROCESS_NOTES.md`** — the corpus build + the Phase-0/2 substrate.

---

## 2. THE RECOMMENDED NEXT WORK — L0 STANDARDIZATION (make it fully verifiable)

**Why this is next:** the whole stack (C1, themes, hub, journey, verify, essays) rests on L0 — the
token-level literal substrate. If L0 isn't *provably correct and complete*, everything above it is
built on sand. Currently: L0 exists (35 files) but there is **no verification tool beyond the
extractor**, no round-trip proof, no schema contract. The user wants "a standardised system that no
one can argue with."

### The L0 standardization spec (what to build)

**Goal:** make L0 a verifiable, standardised substrate with a formal contract + automated proofs.

1. **The L0 schema contract** (`l0_schema.json` or a spec):
   - every record must have `id, chunk_id, line_id, lemma_iast, literal_gloss, raw_fragment,
     char_start, char_end, source_text, quoted, status`.
   - **invariants:** no missing lemma where a gloss exists · no overlapping char spans · `status` ∈
     {PARSED, AMBIGUOUS, FAILED} · every `raw_fragment` reconstructs from the immutable T1.

2. **The round-trip verifier** (`verify_l0.py`):
   - parse each L0 file back into text → must equal the immutable T1 chunk (byte-identical modulo
     whitespace).
   - per-chunk: PARSED + AMBIGUOUS + FAILED = total tokens; the reconstructed text matches the T1.
   - this is the "no one can argue" proof: L0 is a faithful, complete, lossless tokenization.

3. **The schema validator** (`validate_l0.py`):
   - every record satisfies the contract; no orphaned/duplicate/overlapping spans; the IAST lemmas
     are well-formed (IAST diacritics, no script mixing).

4. **The cross-layer check** (L0 → the rest):
   - every C1 `verse_commentary` and every published passage's source span resolves to an L0 line
     range (the provenance spine is provable top-to-bottom).

5. **The CI gate:** `verify_l0` + `validate_l0` run in tests; a chunk that fails round-trip blocks
   the build. This is the "standardised system" — deterministic, automated, auditable.

### Why it compounds
A verifiable L0 makes every higher layer defensible: the C1, the themes, the hub, the journey, the
essays, and the ML agent's retrieval all resolve to *proven* tokens. It's the foundation the "no one
can argue with" standard rests on.

---

## 3. OTHER OPEN THREADS (for after L0)

From `WHAT_NEXT_PATALA.md`: context-alignment (wire the downloaded GRETIL IPV/IPK into `/api/context`),
the comparative matrix seed (`/api/comparative`), the argument truth-packet + `/verify-argument`,
L200→graph annotations, PARALLELS.

From `PATALA_AS_LIBRARY_ENGINE.md`: the provenance-backed catalog, the 4-wings-as-registers.

From `geometric.md` / `EDUCATION_VISION.md`: the edge-weights/pathway-vectors, the audio generator,
the feedback loop.

---

## 4. HOW TO START (for the next agent)

1. Read `VISION_AND_NAVIGATION.md`, then `docs/INDEX.md`, then `THE_COMPANION.md` (sanskritree).
2. **Start the L0 standardization** — the recommended next work (§2): the full spec is in
   `machinelearning/SPEC_L0_STANDARDIZATION.md`. Write the schema contract + the round-trip
   verifier + the validator + the CI gate, and prove the current 35 L0 files pass (or fix what
   doesn't).
3. Log any handoff in `machinelearning/HANDOFF-LOG.md`.

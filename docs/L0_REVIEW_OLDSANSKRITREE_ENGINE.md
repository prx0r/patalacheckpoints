# L0 REVIEW — the old sanskritree translation engine: reusable pieces

*2026-08-12. Agent L0. Reviewed the pre-DeepSeek translation engine at
`/mnt/HC_Volume_106427611/sanskritree/src/sanskritree/` + its `proof_engine/` for anything reusable for
the L0 philological-proof floor (P0–P4). The engine was built before we realised a frontier LLM beats a
hand-built translator; its *formal/philological scaffolding* is still valuable for L0's deterministic
proof layers.*

## Verdict (honest)
The **LLM-translation pipeline is not reusable** (superseded). But three formal/philological modules
are genuinely reusable for L0 — they encode exactly the proof/alignment/lexical contracts L0 needs and
we have NOT yet rebuilt them.

## Reusable for L0

### 1. ⭐ `philology/` — the analysis witness (matches L0 P2, already aligned)
- `analysis_lattice.py` — `Analysis(engine, lemma, features, confidence, detail)` + token lattice.
  **This IS the P2 witness shape** (`verify_l0_p2.py` does the same). Confirms our approach.
- `adapters.py` — Vidyut (chedaka+kosha) + Heritage ensemble, `KNOWN_ENGINES`, honest "unavailable →
  gap not parse" discipline. **Directly reusable** for the L0 P2/P3 ensemble.

### 2. ⭐ `alignment/` + `translation/alignments.py` — the P4 alignment contract (NOT built in L0 yet)
- `alignment/spans.py` — typed alignment relations: `one_to_one | one_to_many | many_to_one |
  many_to_many | implicit | expanded | omitted | commentarial | uncertain`.
- `translation/alignments.py` — `record_alignment(source_span → english_span, relation, confidence)`
  + **`alignment_coverage_report()`** (coverage %, relation counts). This is the P4 Sanskrit↔English
  alignment model + its proof (coverage) — reusable as the L0 `alignment` proof dimension.

### 3. ⭐ `evidence/ranker.py` — the P3 lexical-sense module (the `lexical_sense` dimension we froze at UNCHECKED)
- `rank_senses(lemma, context_lemmas, work_id)` — tradition-proximity + technical-term ranking,
  multi-tier (DB senses → glossary → generic), dedup, top-3.
- `TECHNICAL_TERMS_KS` — an **SLP1-keyed technical glossary** (spanda, kSobha, svatantrya, paSu,
  pASa, dIkzA, ...) with doctrinal glosses. This is exactly what resolves L0's `lexical_sense: OPEN`.
- `TRADITION_PROXIMITY` — tradition-distance weighting for sense selection.
- This is the natural P3 implementation: for a L0 lemma, run `rank_senses` → `lexical_sense: SUPPORTED`
  (a ranked sense) vs `OPEN` (no confident sense).

### 4. `proof_engine/failure_taxonomy.py` — the disagreement-queue pattern
- Failure types with **implied recovery actions** (`COMPILE_ERROR → re-formalize`, `UNPROVABLE → log
  axioms`, `TIMEOUT → split`, `MISSING_PRIMITIVE → candidate`).
- Maps to the L0 P2 disagreement queue: each of CONFIRMED/AMBIGUOUS_SUPPORTED/CONFLICT/UNANALYZED/
  TOOL_ERROR implies a next action, not just a count. Reusable as the queue's action design.

## NOT reusable (superseded / out of scope for L0)
- `proof_engine/` Lean/Nyāya formalization (the `sanskrit_pipeline.py` is a stub; Lean is demoted per
  the cross-layer review — L0 is deterministic philology, not theorem proving).
- `inference/factor_graph.py` + `semantics/` (the LLM-assisted scoring/interpretation layer — belongs
  to the ML lane's higher layers, not the L0 floor).
- `translation/candidates.py`, `realization.py` (the blind-run LLM translation workflow).
- `evaluation/`, `review/` (translation QA, superseded by the ML lane).

## Recommended adoptions for L0 (in priority order)
1. **P3 lexical-sense** — reuse `evidence/ranker.py` + `TECHNICAL_TERMS_KS` to resolve
   `lexical_sense: UNCHECKED → SUPPORTED/OPEN` for the parsed lemmas. Highest leverage (unfreezes a
   frozen dimension).
2. **P4 alignment** — reuse the typed alignment relation model + `alignment_coverage_report()` as the
   L0 `alignment` proof dimension (needs the L0↔L2 span pairs).
3. **Disagreement-queue actions** — adopt the failure-taxonomy pattern for the P2 queue.

**Action taken:** recorded this review; the P3 lexical-sense adoption (ranker) is the recommended next
build for the L0 lane after P0 coverage is green. No code moved into the live L0 pipeline yet (P0 drive
first, per the vision's ordering).

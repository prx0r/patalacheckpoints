# AGENT 2 — VERTICAL LAYER WORKERS (L200 constrained compiler + C1 + THEME/ESSAY wiring)

*2026-08-13. Agent 2, canonical-stack mission. Extends the autonomous factory from `RAW→t1` into the
full registry-driven vertical **L0 → L1 → L2 → L200 → C1**, with per-layer workers each producing the
canonical file shape for that layer and each gated by a **layer-specific validator**. Nothing here touches
the live `auto_translate_raw.py` runner (it continues translating the RAW_SANSKRIT queue unattended).*

---

## 1. What was built (per-layer workers + layer-specific validators)

| Layer | File / handler | What it produces (canonical shape) | Layer-specific validation |
|---|---|---|---|
| **L0** | `pipeline/l0_worker.py` (pre-existing) | canonical L0 records (IPVV schema) | `validate_l0_spec`: P0 span-proof + schema + abstraction-honesty; **gloss is NOT a commit gate** (L0-A floor) |
| **L1** | `pipeline/l1_l2_worker.py` | controlled reading (segments + L0 provenance) | **L1 semantic-fidelity**: surfaces must exist in committed L0 (no doctrinal supplement); provenance resolves |
| **L2** | `pipeline/l1_l2_worker.py` | readable prose + refs | **L2 semantic-fidelity**: content(L2) ⊆ content(L1)+declared_supplies (lemma-overlap guard); provenance resolves |
| **L1L2** | `pipeline/l1_l2_translate.py` (pre-existing) | model L1+L2 translations | F4 binding: passage_id+hash echo, reject misbind/duplicate |
| **L200** | `pipeline/l200_worker.py` (**REWRITTEN**) | 8-section audit per `l200/README-L200-SPEC.md` | **Task-2 fidelity**: 8 sections present; MT typed; derivation-map covers L2; model-failure≠empty-success |
| **C1** | `pipeline/c1_worker.py` (**NEW**) | passage-local commentary per `C1-SPEC` (SUMMARY/FUNCTION/KEY TERMS/EXPLANATION/BOUNDARY/RELATED) | **C1 quality gate** (§17): all sections present; explains not paraphrases; concise ceiling; no modern-comparison/essays-as-evidence lexicon |
| **THEME/ESSAY/EDUCATION** | `pipeline/generative_worker.py` (**now wired into controller**) | model proposes via the canonical layer skill | deterministic structural validator (object_id + input_hash + non-empty output) |

## 2. The two real fixes (the stack previously terminated at L200/C1 as stubs)

1. **L200 input-binding gap.** The old `l200_generator` read `b.get("_l2")`, but the controller's
   `find_eligible` never attached `_l2` — so every real L200 proposal was built from empty L2 text
   (empty derivation map, empty refs). **Now** the generator resolves the committed L2 object from the
   registry (`_committed_l2`), so it always has real L2 text + L1 ground + hashes.
2. **CP4 constrained compiler.** The old `_propose_mt_ia` asked the model open-endedly for MT/IA.
   **Now** `_generate_candidates` deterministically produces bounded alignment units (L2 sentence ↔ L1
   ground) and `_classify_candidates` has the model **classify each candidate** into the frozen
   taxonomy with **IGNORE as the default prior** (MT / SUPPLIED / REFERENT_SUPPLY / STRUCTURAL_CONNECTIVE
   / LEXICAL / GRAMMATICAL / INTERPRETIVE_ASSERTION / OPEN / IGNORE). Model failure →
   `GENERATION_FAILED`, never an empty successful audit.

## 3. C1 worker (the capstone layer — was not wired)

`c1_worker.py::make_c1_handlers` consumes the committed **L2 + L200** (reasons through L200's MT/IA/OPEN,
per C1-SPEC §3), runs one Hermes call producing the structured C1, and gates commit with the C1-SPEC §17
deterministic validator. It is now in `autonomy.py` `LAYER_HANDLERS["C1"]`.

## 4. Proof (deterministic, real committed L0, model stubbed)

`pipeline/prove_vertical.py` drives **3 real committed kramasadbhava L0 objects** through
`L1→L2→L200→C1` via the controller:

```
input: 3 committed L0 objects
L1 committed=3 failed=0
L2 committed=3 failed=0
L200 committed=3 failed=0
C1 committed=3 failed=0
  kramasadbhava:v1: {L0 True, L1 True, L2 True, L200 True, C1 True}
fail-closed (bogus upstream): committed=0 (must be 0)
VERTICAL PROOF PASS
```

Provenance binds: C1 payload carries `_l200_version: l200-kramasadbhava:v1-v1` → L200's `0_identification`
carries `l2_version` → L2 carries `l1_version` → L1 carries `l0_version`. Each layer resolves its committed
upstream; a bogus upstream commits nothing (fail-closed).

## 5. Tests

- `test_workers.py` — extended with L200 constrained-compiler + C1 worker tests → **ALL PASS**
- `test_autonomy.py` — **ALL PASS**

## 6. Honest caveats (the truth)

1. **Semantic correctness still not validated against human gold.** This proves *provenance, shape,
   fail-closed behavior, and layer-specific mechanical gates* — NOT that L200 MT precision (the known
   ~0.20 problem) or C1 quality is scholar-correct. The constrained classifier reduces the 
   over-production failure mode by construction (default IGNORE) but must be measured against
   `benchmarks/l200/dev.jsonl` before the DEV gate (MISSION CP5) closes.
2. **The vertical proof stubs the generative L200/C1 model calls.** The live-model L200/C1 path is wired
   and available (the controller calls the real worker), but has not yet been proven end-to-end against
   real model output on a batch.
3. **THEME/ESSAY/EDUCATION** are wired to the Hermes-skill worker with a *structural* validator only;
   their canonical semantic validators (theme coverage, essay proof-carrying) are the next real gap.

## 7. Next moves (in mission order)

1. Measure the constrained L200 classifier against `benchmarks/l200/dev.jsonl` (CP5 DEV gate).
2. Run the **live-model** L200+C1 path unattended on a real kramasadbhava batch (background, tail the log).
3. Build the real **THEME** worker (evidence-backed synthesis across committed C1s) per `LAYER_MATRIX.md`.
4. Move toward MISSION CP9 (full unattended vertical) once L200 DEV + C1 canaries hold.

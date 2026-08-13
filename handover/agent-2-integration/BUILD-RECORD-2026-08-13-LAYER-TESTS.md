# AGENT 2 — VERTICAL LAYER WORKERS + IPVV-STACK TESTS (2026-08-13)

*Companion to `BUILD-RECORD-2026-08-13-VERTICAL-WORKERS.md`. This record adds: the layer-by-layer test
results against the REAL IPVV exemplars, the confirmation that our layer registry maps to the canonical
IPVV stack (NOT the T1/R1/T2 pipeline), and the current loose threads. The live `auto_translate_raw.py`
runner is untouched throughout.*

---

## 0. CONFIRMATION — the layer stack is the IPVV canonical stack

We are NOT on the T1/R1/T2/T3 pipeline naming for the autonomous layers. The canonical IPVV layer stack
(`translations/_stack/ipvv/README.md`, `c1andmore.md`, `hermespatalalayers.md`) is:

```
SOURCE → L0/L1 → L2 READ → L200 AUDIT → C1 COMMENTARY → THEMES → PARALLELS → ESSAYS → EDUCATION
```

`pipeline/object_registry.LAYERS` already matches this exactly:
`['SOURCE','L0','L1L2','L1','L2','L200','C1','THEME','ARGUMENT','SYNTHESIS','ESSAY','EDUCATION']`.
The workers are wired to these layer names. L200's derivation map now binds the **argument-map segment +
L0 range + source range** per the IPVV L200-SPEC §2 (L2 ¶ → argument-map segment → L0 range → source
range), not an empty placeholder.

## 1. LAYER TESTS vs the REAL IPVV exemplars

Each layer's worker was tested against the actual hand-authored canonical files on the mount
(`/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv/`).

### L0 — PASS (`pipeline/test_l0.py`)
- **Validator accepts the real canonical IPVV exemplars** (`chunkV2-A/B/C*.l0.jsonl`, ~7,500 records):
  schema + abstraction-honesty **100%** (schema_ok = n for all 3). Our validator is aligned with the
  shipped canonical data.
- **RAW-L0 (MODE_B, deterministic, no model)** on real verses: schema-conformant + **P0 lossless**
  (0 unknown chars, 0 bad spans).
- **Controller L0 handler commits + gates** correctly (3/3).
- *Harness note:* the P0 span-proof applies only to MODE_B raw-Sanskrit L0 (source_text = Sanskrit). The
  MODE_A exemplars store English gloss prose in source_text, so P0 does not apply there — schema +
  abstention is the correct gate, and it passes.

### L1 / L2 — PASS (`pipeline/test_l1_l2.py`)
- **L1 (controlled):** every controlled-segment surface verified to exist in the committed L0 records
  (no doctrinal supplement); provenance resolves to committed L0. Deterministic scaffold PASS.
- **L2 (readable):** content(L2) ⊆ content(L1)+declared_supplies (lemma-overlap guard); provenance
  resolves to L1. Deterministic scaffold PASS.
- **Live model path (L1L2 worker `l1_l2_translate.py`):** real verse → produced fluent close (L1) +
  readable (L2), validator PASS. This is the path that produces the *perfect readable file type* (the
  deterministic scaffold is the content-faithful floor, not fluent prose).
- Topical agreement vs the canonical kramasadbhava 1.8 translation confirmed (homage/goddess/kālī/
  supreme/bliss).

### L200 — constrained compiler (test in background as of this writing)
`pipeline/test_l200_v2o.py` feeds the REAL hand-authored V2-O L1 + L2 into the constrained classifier
and compares MT/IA against the canonical `l200/V2O-saptamo-vimarsa.md`. Derivation map now binds
argmap/L0/source ranges. Result logged to `/tmp/opencode/test-l200.log`.

### C1 — worker built + validator-gated (live model test next)
`pipeline/c1_worker.py` consumes L2 + L200, emits the C1-SPEC structure (SUMMARY/FUNCTION/KEY TERMS/
EXPLANATION/BOUNDARY/RELATED), gated by the C1-SPEC §17 deterministic validator. Wired into the
controller. Live comparison vs `c1/read/c1_V2O-orderless-support.md` is the next test.

## 2. FILES CREATED / MODIFIED (this session)

| File | Kind | What it does |
|---|---|---|
| `pipeline/l200_worker.py` | modified | constrained compiler (deterministic candidate generation → model classifies, IGNORE default); resolves committed L2 from registry; derivation map binds argmap+L0+source (IPVV §2) |
| `pipeline/c1_worker.py` | new | C1 commentary worker (make_c1_handlers); consumes L200 MT/IA/OPEN; C1-SPEC §17 validator |
| `pipeline/l1_l2_worker.py` | modified | L1/L2 validators hardened to semantic-fidelity (content-subset + provenance) |
| `pipeline/autonomy.py` | modified | wired C1 worker + THEME/ESSAY/EDUCATION Hermes-skill worker into LAYER_HANDLERS |
| `pipeline/generative_worker.py` | (used) | Hermes-runs-layer-skill worker, now wired into the controller |
| `pipeline/prove_vertical.py` | new | deterministic vertical proof: committed L0 → L1→L2→L200→C1, fail-closed |
| `pipeline/test_l0.py` | new | L0 layer test vs IPVV exemplars |
| `pipeline/test_l1_l2.py` | new | L1/L2 layer test |
| `pipeline/test_l200_v2o.py` | new | L200 constrained-compiler test vs V2-O exemplar |
| `pipeline/compare_ipvv_exemplars.py` | new | multi-layer comparison harness (superseded by the per-layer test files) |
| `pipeline/test_workers.py` | modified | extended with L200 + C1 worker tests |
| `handover/agent-2-integration/STALLS-PITFALLS.md` | modified | added the background-tests practice (one layer at a time, detached, log-file progress) |

## 3. HOW IT WORKS (the per-layer autonomous flow)

```
committed L0  ──L1──>  controlled reading (segments + L0 provenance)
    │                     [L1 validator: surfaces ∈ L0, provenance resolves]
    ▼
L2 READ  ──(L1L2 model path or deterministic scaffold)──>  readable prose + refs
    │                     [L2 validator: content(L2) ⊆ content(L1)+supplies, provenance]
    ▼
L200 AUDIT  ──>  deterministic 8-section scaffold + constrained classifier (MT/IA/OPEN, IGNORE default)
    │                     [L200 validator: Task-2 fidelity, 8 sections, derivation map]
    ▼
C1 COMMENTARY  ──>  passage-local commentary (SUMMARY/FUNCTION/KEY TERMS/EXPLANATION/BOUNDARY)
                     [C1 validator: C1-SPEC §17 — explains, concise, no modern-comparison/essays]
```

Each layer: deterministic controller (`autonomy.py::tick`) → find_eligible from registry DAG → bounded
batch → layer generator (model or deterministic) → **layer-specific validator** → commit / fail-closed.
The model never self-validates; every layer has a distinct validator.

## 4. CURRENT LOOSE THREADS

1. **L200 live-model result vs V2-O exemplar** — in flight (`/tmp/opencode/test-l200.log`); confirm the
   constrained classifier recalls the canonical MT types (LEXICAL/STRUCTURAL_CONNECTIVE/SUPPLIED) on real
   input before the CP5 DEV gate closes.
2. **C1 live-model comparison** vs `c1/read/c1_V2O-orderless-support.md` — not yet run (next).
3. **L200 semantic quality** (the known MT-precision ~0.20 problem): the constrained classifier reduces
   over-production by construction (default IGNORE), but must be **measured against
   `benchmarks/l200/dev.jsonl`** (MISSION CP5) before claiming the DEV gate.
4. **THEME/ESSAY/EDUCATION** validators are structural-only (object_id + hash + non-empty). Their
   canonical semantic validators (theme membership evidence, essay proof-carrying) are the next real gap.
5. **THEME worker itself** is not built (only the generic Hermes-skill handler is wired). Per
   `LAYER_MATRIX.md`, THEME should be evidence-backed synthesis across committed C1s.
6. **Unpushed commit(s)** on `agent2` (`5d48617` + the derivation-map fix) — not yet pushed to origin.
7. **compare_ipvv_exemplars.py** is superseded by the per-layer test files (test_l0/test_l1_l2/
   test_l200_v2o/test_c1); can be removed or kept as a cross-layer sanity harness.

## 5. CARRY-FORWARD

L0, L1, L2 are tested and passing against the real IPVV exemplars + registry truth. L200's compiler is
rewritten to the IPVV shape and under live test; C1 is built and gated, pending its live exemplar
comparison. Next: finish the L200/C1 live tests, then measure L200 against the DEV benchmark (CP5), then
build the real THEME worker (CP8+).

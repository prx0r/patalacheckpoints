# Experiment — Kramasadbhāva 1.8 (kramasadbhava-1.8-v1)

*2026-08-10. The first real vertical slice: the full audited translation stack
(T1→R1→T2→R2→T3→T3.1) run on one verse with the actual model. Pipeline version
`translation-pipeline-v1.0`, model `deepseek-v4-flash`, base source
`pt:src:kramasadbhava:dyczkowski-ed`.*

## Experiment config

```
experiment_id      kramasadbhava-1.8-v1
pipeline_version   translation-pipeline-v1.0
model              deepseek-v4-flash
base_source        pt:src:kramasadbhava:dyczkowski-ed
passage            tantra:text:kramasadbhava:1.8
date               2026-08-10
flow               T1 → R1 → T2 → R2 → T3 → T3.1
```

Sanskrit: `ooṃ namaste devadeveśi mahākāli namo'stu te | namo'stu paramānande nirānande namo'stu te`

## What ran

The durable state machine (load → transition → run → audit → persist → reload)
drove the verse through all six stages. **All six stage payloads were persisted**
to `translations/_stack/kramasadbhava/passages/1.8.json`, `pipeline_stage=T3.1`,
`editorial_status=proposed` (correct — no machine stage claimed review).

## Results by stage

| Stage | Output | Verdict |
|---|---|---|
| **T1** | close: "oṃ, salutation to you, O Queen of Gods, O Mahākālī... Homage be to you, O Supreme Bliss, O Non-Bliss..." | ✅ real content |
| **R1** | `cruxes: []`, `detail: ""` | ❌ **empty** — model returned nothing |
| **T2** | `close_translation: ""` | ❌ **empty** |
| **R2** | `decisions: []`, `chosen: ""` | ❌ **empty** |
| **T3** | "oṃ. Homage to you, O queen of gods, O Mahākālī: homage to you... O supreme bliss; homage to you, O blissless one." | ✅ real content |
| **T3.1** | "oṃ. Homage to you, O queen of the gods, O Mahākālī — homage to you... O supreme bliss; homage to you, O blissless one." | ✅ real content |

## The core empirical finding

**`deepseek-v4-flash` returns EMPTY output on the complex, strict-JSON stage prompts
(R1/T2/R2) — the same failure we first hit on T1.** The verbose house system prompt
+ multi-field JSON schema makes the model emit nothing.

- Short prompts / lean JSON → the model works (T1, T3, T3.1 succeeded).
- Long system prompt + full-schema JSON → empty (T1 initially; R1/T2/R2 now).

Two fixes were applied during the run and are committed:
1. **`max_tokens` 2000 → 4000** (the T1 JSON was being truncated to nothing).
2. **T1 uses a LEAN strict-JSON schema** (`close_translation`/`reader_draft`/`flags`);
   the extended fields default in the pipeline. This fixed T1.

But **R1/T2/R2 still use the long house prompts + full schema and still return empty.**
The same lean-schema treatment is needed for R1/T2/R2 — OR the house style rules must
be moved out of the strict-JSON system prompt (the style can be applied to the prose,
while the JSON structure stays minimal).

## Why this is not an architecture failure

The state machine behaved correctly:
- T1 v1 empty → `RETRY` → T1 v2 valid (the retry path worked).
- R1/T2/R2 empty → the strict-JSON check *should* have raised `StageOutputError`,
  but the log shows `ok=True` — **a bug**: the empty-parse path produced an empty
  object (`{...}.get("x","")`) that passed, rather than raising. This is a pipeline
  bug to fix: an empty/missing required field in a strict stage must be INVALID, not
  silently accepted.

## The bugs to fix (next pass)

1. **R1/T2/R2 empty-output**: same model-interface fix as T1 — lean the JSON schema
   and/or shorten the system prompt. This is the #1 blocker.
2. **Empty strict output is accepted**: `_payload_from_json` defaults missing fields
   to `""`/`[]`; for strict stages, a missing required field should mark the stage
   INVALID (so RETRY engages), not produce an empty-but-"valid" stage. The
   `stage_T2(close="")` / `stage_R2(chosen="")` path must fail.
3. **C1**: not yet run (the run stopped at T3.1). Needs the same lean-JSON treatment.

## What to review with ChatGPT

Ask ChatGPT to review **the persisted `1.8.json` + this report + the R1/T2/R2 prompt
handling**, specifically:
- How to make `deepseek-v4-flash` (and models in general) reliably emit the R1/T2/R2
  structured JSON without returning empty — lean-schema, prompt-splitting, or a
  two-call (prose-then-structure) approach?
- Whether the "empty strict output must be INVALID, not silently accepted" rule is
  right, and how to enforce it cleanly (per-field presence checks).
- Whether the two-fix pattern (max_tokens + lean schema) generalizes to R1/T2/R2/C1.

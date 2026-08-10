# Blocker Report — Kramasadbhāva 1.8, pipeline fix status (requesting help)

*2026-08-10. I've implemented the stage-contract fix from the last review and verified it
with a deterministic mock. The code is correct. I'm now blocked by the **model backend
degrading**, and I need detailed advice on the model-interface layer.*

---

## What I fixed (all verified with a mock, no full run)

Following your review, I:
1. **Added `pipeline/contracts.py`** — a stage-contract layer separating FORMAT
   (parseable JSON) from CONTRACT (did the model produce the required data).
   `validate_stage_contract()` requires substantive fields:
   - `T1`: close_translation, reader_draft
   - `R1`: assessment, cruxes (array, may be `[]` if the verse is constrained)
   - `T2`: translation, decisions, constrained
   - `R2`: translation, decisions, hard_core
   - `T3`: resolved
   `{}` / empty output → INVALID (no more silent acceptance).
2. **`_make_payload` now normalizes lean→canonical BEFORE the contract check**, then
   constructs the payload. `_payload_from_json` no longer defaults required fields.
3. **Simplified the R1/T2/R2 prompts to lean model contracts** — short stage-specific
   system prompts (no big STYLE+EVIDENCE blob), lean JSON in the user message, and
   **removed commentary-generation from R2** (that's C1's job now).
4. Kept `max_tokens=4000` as a ceiling; the substantive fix is the lean contract.

**Verified end-to-end with a deterministic mock:** an empty `{}` R1 is correctly
rejected (`R1 contract not met`) and the next call retries to a valid R1; the flow
then runs T1→R1→T2→R2→T3→T3.1→COMPLETE. `{}` no longer silently becomes a "valid"
stage.

---

## The blocker — the model backend is degrading

The opencode-go `deepseek-v4-flash` account is now returning **slow, empty, or
non-compliant** responses inconsistently:

- A trivial `Reply READY` call took 13s and returned "It looks like your message...".
- The same R1 prompt sometimes returns valid JSON (1220 chars), sometimes empty (0 chars).
- 4 sequential calls hung past a 90s timeout.

This is **not** our code (verified with the mock). It looks like **rate-limiting /
throttling** on the opencode-go workspace, not a deterministic prompt failure.

**I need your advice on two things:**

### 1. Model-interface reliability (the real remaining problem)
Even when the backend isn't degraded, the model is *sometimes* empty/non-compliant on
the lean JSON prompts. Options I'm weighing:
- **(a) Lean-schema only** (current): short sys + lean JSON. Reduces but doesn't
  eliminate empties.
- **(b) Two-call: prose-then-structure** — the reviewer warned against this for
  R1/T2/R2 (cost, distortion, provenance), but recommended it for C1. Is there a
  middle ground?
- **(c) A JSON-mode / response-format API param** — does opencode-go / the underlying
  OpenAI-compatible endpoint support a native `response_format={"type":"json_object"}`
  or `json_schema` mode that would force strict JSON and avoid empties? If so, what's
  the exact invocation? This feels like the cleanest fix but I don't know the endpoint's
  capabilities.
- **(d) Retry-with-backoff + a "health probe"** — before each stage, confirm the
  backend responds; if degraded, pause/backoff rather than wasting calls on empties.

Please advise the most robust approach and, if (c), give me the exact request shape /
parameter to add to `pipeline/model.py`'s `chat()`.

### 2. Should I build a response-validation test harness?
A small CI-like harness that, given a stage + a sample passage, calls the model N times
and reports: empty-rate, valid-JSON rate, contract-pass rate, latency. This would let us
measure whether a fix (lean schema, response_format, backoff) actually helps. Worth
building, or is it premature given the backend is the bottleneck?

---

## Files for review (all pushed, commit `b90ef45`)

1. **`pipeline/contracts.py`** — the stage-contract layer (new).
2. **`pipeline/state_machine.py`** — `_make_payload` (normalize→contract→construct),
   the FORMAT-vs-CONTENT distinction.
3. **`pipeline/prompts.py`** — the lean R1/T2/R2 system + user prompts.
4. **`pipeline/model.py`** — `chat()`/`chat_json()`/`parse_json()`/`StageOutputError`.
5. **`experiments/kramasadbhava-1.8-v1.md`** — the original experiment report.

Repo: **https://github.com/prx0r/patala** (branch `main`, commit `b90ef45`).

## The exact question for you
> What is the most robust way to make a degraded/unreliable OpenAI-compatible backend
> (opencode-go, `deepseek-v4-flash`) reliably produce small strict-JSON responses for
> the R1/T2/R2/T3 stages — native `response_format` if available, retry-with-backoff,
> health-probe, or something else? And should I build a response-reliability harness to
> measure it? Please give concrete code/recommendations I can drop in.

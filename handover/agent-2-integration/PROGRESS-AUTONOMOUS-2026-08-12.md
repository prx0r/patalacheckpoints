# AGENT 2 — AUTONOMOUS FACTORY PROGRESS (2026-08-12)

*The single current-state map for the autonomous translation factory (`SOURCE→L0/L1→L2→L200→C1`).
Three columns: what is VERIFIED, what is CLOSE-but-unverified, what is STILL NEEDED. Plus the full file
map and the agent-1 / evidence-lane handover location.*

---

## 1. VERIFIED (real, tested)

| capability | evidence |
|---|---|
| **Autonomous RAW-L0 runs** | controller tick drove real RAW-L0 (Vidyut + gloss + validate + commit) on kramasadbhāva: **11/12 passages committed**, 59 glossed records, 1 fail-closed (OCR verse) |
| L0 deterministic floor | certificate A/B/F/G/H: lossless 2/2, binding 2/2, source-blocked, no dupes, cross-work |
| Generic autonomy controller | `pipeline/autonomy.py` + `object_registry.py`: eligibility DAG, flock, idempotency (registry-derived), supersession, run reports — tested 16/16 |
| L200 validator certificate | 10 phenomena + 14 dims (A–L) + adversarial mutations + invalidation — PASS (deterministic core) |
| ModelAdapter boundary | `pipeline/model_adapter.py`: DirectModelAdapter (**~1.4–2.1s** vs hermes 8–48s) + HermesAdapter + strict batch (ID+hash binding, fail-closed) |
| Tests | `test_autonomy` 16/16 · `test_workers` 11/11 · `test_autonomous` 7/7 · `test_scholarly_oracle` 10/10 |

## 2. CLOSE — implemented, but the live-model quality/reliability gap is NOT yet bounded

| capability | gap |
|---|---|
| **Autonomous RAW-L0 gloss reliability** | the gloss model call was nondeterministic (hermes empty-return → fail-closed). The Direct adapter (~2s, structured) is wired and should close it, but a full unattended batch was **not yet proven** end-to-end after wiring (run produced no output / timed out — needs a background re-run) |
| **L200 live semantic quality** | instance-level benchmark: MT precision 0.20, 8 FP (model over-produces). IA precision 0.33, open precision 0.14. Over-production not yet fixed (needs candidate→classifier + L0 evidence) |
| L200 benchmark semantics | fixed (instance-level, micro) — the honest numbers above; DEV set is contaminated (used for prompt iteration); **TEST set not yet built** |

## 3. STILL NEEDED (the path to autonomous RAW-L0 v1, in order)

1. **Close the RAW-L0 gloss reliability gap with the Direct adapter** — run a real unattended batch in the background, confirm the nondeterminism is bounded.
2. **Autonomous RAW-L0 v1 proof** — leave a bounded corpus to the controller unattended; all committed objects correctly bound + validator-passing; malformed/model-failed/source-corrupt never silently commit; reruns don't duplicate.
3. Freeze autonomous RAW-L0 v1.
4. Then resume **L200**: candidate→classifier redesign (deterministic L1↔L2/L0 candidates → model classifies, default IGNORE), L0 evidence into L200 input, IA as a separate pass.
5. L200-TEST-v1 (15–20 real IPVV, independently typed) → blind run once.
6. **C1** autonomous production.
7. Unattended `SOURCE→L0/L1→L2→L200→C1` vertical proof.

## 4. FILE MAP

| area | files |
|---|---|
| controller | `pipeline/autonomy.py` · `object_registry.py` |
| L0 workers | `l0_worker.py` · `raw_l0.py` · `batch_translate.py` · `agentic_gloss.py` · `auto_run.py` |
| L200 worker | `l200_worker.py` |
| model boundary | `model_adapter.py` (Direct/Hermes + strict batch) · `model.py` |
| certificates | `certificate_l0.py` → `factory-certificates/L0-v1/` · `certificate_l200.py` → `factory-certificates/L200-v1/` |
| benchmarks | `benchmark_l200_live.py` → `benchmarks/l200/{dev.jsonl,report-dev.md}` |
| skills | `skills/autonomous-layer/` (L0/L1/L2/L200/C1/THEME/ESSAY/EDUCATION + controller) |
| tests | `test_autonomy.py` · `test_workers.py` · `test_autonomous.py` |

## 5. AGENT-1 / EVIDENCE-LANE HANDOVER (the scholarly-oracle proof — NOT Agent 2's lane)

A working **scholarly-oracle vertical** (one proposition → SourceAssertion → CorroborationEvent, DIRECT +
PARTIAL) was built as a proof and is **handed to the evidence lane**. Agent 2 does NOT continue it.
**Find it here:**
- `pipeline/scholarly_oracle.py` (the vertical) + `pipeline/test_scholarly_oracle.py` (10/10)
- `docs/BUILD_NOTES_S0_1.md` (the proof writeup)
- `handover/LOG.md` (the handover entry)

## 6. WORKING-PRACTICE NOTE (from the coordinator's review)

**Run long model calls in the BACKGROUND** (nohup / async / a separate worker), never blocking the
session. A hermes/direct call can take 8–48s or hang; running it in the foreground stalls all other work.
The controller/supervisor (`autonomy.py` tick, `auto_run.py`) already run unattended; any manual
adapter/canary invocation should be backgrounded and the log tailed, not awaited inline.

---

## UPDATE (2026-08-13) — THE RAW-L0 BLOCKER IS CLOSED (checkpoint CP1/CP2)

### The validator fix (the exact blocker, now resolved)
`validate_l0_spec.py` no longer requires a `literal_gloss` on `AMBIGUOUS` records. An empty-gloss
`AMBIGUOUS` is now a **valid honest abstention** (deterministic Layer A commits; the gloss is best-effort
Layer B enrichment — an enrichment failure never erases Layer A). `PARSED` STILL strictly requires both
lemma AND gloss (no fabricated certainty). Regression-tested (F10).

### Three reliability bugs fixed (all in the gloss path)
1. **`l0_worker.py` passed `"L0"` as the work_id** to the gloss term-packet lookup → the sivaqueue
   term-context was never applied. Now derives the real work_id from the passage object_id (F11).
2. **`agentic_gloss.run_batch` let an empty/malformed challenge response ERASE the propose-pass glosses**
   (challenged returned `{idx:{token:""}}` which overwrote proposed). Now falls back to proposed (F).
3. **Gloss nondeterminism** — propose/challenge occasionally return all-empty. Added `_gloss_call_with_retry`
   (bounded retry, only accept empty when every attempt is empty — honest fail, never fabricated).

### Verified (fast, deterministic, no model)
- **CP1 on a real verse:** `aśarīrāḥ śarīrasthāḥ kālyārādhanatatparāḥ` → 3 canonical L0 (PARSED, correct
  glosses) → `validate_l0_spec` **PASS** (schema 3/3, abstention 3/3, gloss 3/3, P0 true, 0 unknown).
- **Whole-work deterministic floor:** kramasadbhāva **97/100 P0-PASS** (lossless, 0 unknown), 509 canonical
  records, 350 parsed / 159 honest AMBIGUOUS; the 3 fails are all genuine lacuna/OCR verses that
  fail-closed (e.g. `* * * * * * *(?)`). This is the certified floor, no model required.
- Tests: `test_autonomous.py` ALL PASS (incl. new F10/F11 regressions).

### In flight (CP2 — autonomous RAW→L0 v1, driven by the real controller)
`pipeline/prove_raw_l0.py` (detached) drives `autonomy.tick` for kramasadbhāva through the Direct model
adapter, committing validator-passing canonical L0 to the durable registry, writing
`factory-certificates/L0-v1/raw-l0-v1.json` + `data/corpus/registries/l0-registry.jsonl`. Gloss layer is
slow (real model calls, retries), so this takes a few minutes — checked back later, not babysat.

---


## UPDATE (2026-08-12, end of session) — autonomous RAW-L0: the precise blocker

### What works (verified)
- **Deterministic floor**: Vidyut lemma/morphology + P0 lossless (0 unknown) — verified on raw kramasadbhāva.
- **Autonomous controller + registry**: `autonomy.py` tick + `object_registry.py` — idempotency, flock,
  supersession, run reports — tested (16/16).
- **DirectModelAdapter** (~1.4–2.1s trivial; ~10s/passage on real gloss) — faster than hermes but **also
  hangs/times out on the real gloss prompt sometimes**.
- **Proof harness**: `pipeline/proof_autonomous_l0.py` (2-in-a-row, ledger advance) — runs without
  hanging (bounded 60s timeout + retry + ok-check wired in), but currently reports FAIL (0 committed).

### The EXACT blocker (why 0 commits)
`pipeline/validate_l0_spec.py` **requires even AMBIGUOUS records to carry a `literal_gloss`** (line ~106:
"AMBIGUOUS record has empty literal_gloss (IPVV L0 always glosses)"). So when the model cannot gloss a
token, the honest-abstention path (empty gloss → AMBIGUOUS) still fails the whole verse. The deterministic
floor is rejected.

**To make raw-L0 WORK (commit the deterministic floor when the model abstains):** relax the validator so an
**AMBIGUOUS record with an empty gloss is a valid honest abstention** (do not require gloss on AMBIGUOUS).
This is the doctrine's "miss + OPEN tolerated, never fabricated" — the deterministic floor commits, the
gloss is best-effort/OPEN.

### Also documented
- `STALLS-PITFALLS.md` — why the shell kept wedging (foreground model calls; `&` background jobs the
  shell waits on; stuck workers hogging the API) + the working rule.
- The gloss is wired to the adapter (Direct) with 60s bounded timeout + retry + ok-check (fail-closed,
  never hangs). Both backends (hermes/direct) are nondeterministic on the real gloss prompt — the
  reliability gap is NOT yet closed.

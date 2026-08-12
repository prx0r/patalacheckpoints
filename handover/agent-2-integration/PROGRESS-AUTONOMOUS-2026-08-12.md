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

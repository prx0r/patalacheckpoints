# PROBLEMS — AUTONOMOUS TRANSLATION FACTORY (2026-08-12)

*Red-team of the unattended "translate while I sleep" loop. This is the honest problem ledger for the
autonomous A3 factory: what's built, what actually works, and every real defect found — so a human can
advise on direction. Companion: `AUTOTRANSLATE-NORTHSTAR.md`, `SESSION-PROGRESS-AUTONOMOUS-TRANSLATION.md`.*

---

## 0. The good news (what actually works, verified this session)

- **One `hermes -z` call produces MANY translations** — `pipeline/batch_translate.py` returned L0 glosses +
  close translations for 3–4 kramasadbhāva verses in ONE call, with school-correct senses
  (vimarśa→"reflexive awareness" per Pratyabhijñā/Krama policy). No max-token cap (max_tokens is
  unenforced → bounded only by context).
- **`auto_run.py` commits real L0 through hermes** — kramasadbhāva v1/v3/v4 committed (P0 lossless,
  0 unknown), with honest fail-closed rejection of illegible verses.
- **The deterministic core (Vidyut + P0 proof + `validate_l0_spec`) runs locally, no API.**
- **Hermes-as-agent setup exists**: `patala` profile, `patala-translate` skill, `hermes cron`
  (`patala-autotranslate`, every 30m) — but the cron was paused.

---

## 1. CRITICAL — the loop is NOT idempotent (re-running duplicates)

`pipeline/auto_run.py::run_work`:
```python
verses = split_verses(raw)[:max_verses]   # SAME first N verses every run
```
- **No per-verse "already done" check.** Every run re-glosses verses `0..max_verses` and re-commits them.
- A work of N>max_verses verses is **never advanced past verse max_verses** — it redoes the same batch forever.
- `eligible_works()` returns **all** RAW_SANSKRIT works regardless of completion — a work never leaves the queue.
- `update_ledger()` writes per-run `{completed: n, total: max_verses}` — **not cumulative, not per-verse**, so
  there's no resume-from-where-it-left-off.
- `commit_l0()` dedups only **byte-identical** record-SHAs; glosses are **model-nondeterministic**, so the same
  verse re-glossed usually yields a different SHA → a **new version every run** (churn). Evidence: kramasadbhava
  already has v1–v4 from overlapping verse windows.

**Consequence:** left for hours then re-run = wasted hermes calls (re-glossing), version churn, and never a
completed work. Crash/restart is not resumable.

## 2. hermes -z reliability (the runtime the factory depends on)

- Intermittent **hangs** — a call can block for minutes. Mitigated this session (600s batch timeout + one
  bounded retry), but a persistent hang still stalls a batch ~10 min before the retry+second timeout.
- **Orphaned subprocesses on kill** — killing the supervisor left a hung `hermes -z` running (PID orphan),
  doing nothing; had to be killed manually. The supervisor must clean up its child processes.
- Non-JSON model output → empty glosses (honest but low commit rate).

## 3. Deterministic-core gaps (block P0, not the model)

- **Avagraha `'`** is an unknown char for the tokenizer → `cidgagana` fails P0 (e.g. `dantyāsyo'yaṃ`). The
  sandhi apostrophe isn't handled → those works can never commit.
- **OCR / source noise** (e.g. kramasadbhāva `* * * * * * * *(?)`) → unknown chars → honest FAIL. Needs
  source cleaning.

## 4. Double-run / coordination risk

- Only **one** worker should run at a time. The hermes cron (agent) + the nohup `auto_run` worker would both
  process the same ledger. The cron is paused, but there's no lock guarding against both running.

## 5. The factory certificate is NOT yet met (the gate before "set it loose")

Per `AUTOTRANSLATE-NORTHSTAR.md`: before trusting unattended output, we need the **Sanskrit-only replay
benchmark** vs IPVV gold showing **false-certainty below threshold** + human review of failure clusters +
Kramasadbhāva cross-work. The benchmark scaffold (`pipeline/benchmark_l0_replay.py`) runs but the full
IPVV raw↔gold alignment is not done. **Until then, the loop's output quality is unmeasured.**

---

## 6. Open questions — ADVICE REQUESTED

1. **Idempotency design** — the clean fix is per-verse completion tracking (read committed `passage_id`s from
   the l0 registry → start at the next uncommitted verse; skip done; advance). Should progress live in the
   ledger (`l0.progress` as a set of committed passage_ids) or be derived by scanning `l0-version-registry.json`
   for committed record ids? (Ledger = state truth; registry = immutable versions. I lean derived-from-registry
   to avoid two sources of truth.)
2. **Verse window** — batch the whole work in one pass (max context, but a 100-verse call risks the model
   degrading/truncating) vs. bounded batches (e.g. 8–16 verses/call) with resume? The user wants "as many as
   possible in one call" — what's the safe batch size given hermes can hang and output quality drops with size?
3. **hermes reliability** — is a retry-with-backoff + orphan-cleanup (kill child on timeout) enough, or should
   the supervisor run `hermes -z` calls in a subprocess it can hard-kill? Should we move off `hermes -z` to a
   direct model call (OpenCode Go) for the generative layer, keeping hermes only for the cron-agent?
4. **Avagraha + OCR** — fix the tokenizer to treat `'` as a non-losing boundary char (P0-preserving), and
   add a source-cleaning pass for OCR noise? Or flag these works as needs-manual-source?
5. **Cron vs nohup worker** — for the all-night run, which is the driver: the hermes **agent** (patala-translate
   skill, cron) or the deterministic `auto_run` loop? The user wants "hermes as the agent, not a py script" —
   but the agent path is untested and hermes is flaky. What's the pragmatic split?

---

*Status: worker stopped (not safe to leave churning). Nothing here is claimed working beyond what §0 shows.*

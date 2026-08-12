# STALLS / PITFALLS — why commands hang (2026-08-12)

*The recurring reason my shell keeps timing out / wedging, and the rule that fixes it. READ BEFORE running
any model call or background job.*

## The three things that keep stalling

### 1. Running `hermes -z` (or a large Direct call) in the FOREGROUND
`model.chat` / `complete_json` on a big prompt takes **8–48s** and can **hang**. When I run it in the
foreground shell, the whole tool command blocks for up to the shell timeout (120s) or longer.
- **Symptom:** a command that should return in 2s runs 120s then times out; "no output".
- **Fix:** never run a model call in the foreground for more than ~2 small passages. Use a **background
  detached** runner for any real batch, or keep foreground tests to ≤2 passages.

### 2. Launching a background job with `&` in the tool's persistent shell
When I do `nohup python3 ... &`, it becomes a **job of the persistent shell**. The next command that
touches it (`kill`, `pgrep`, `pkill`) makes the shell **wait on that job** → the shell wedges for 120s.
- **Symptom:** `kill`/`pgrep`/`pkill` on the background PID times out.
- **Fix:** if a background worker is needed, launch it with **`setsid` + `nohup` + `disown`** so it is fully
  detached and NOT a shell job; and **never `kill`/`pgrep` it from the same shell** — use a detached kill.

### 3. A stuck background worker hogging the model API
A wedged `run_autonomous_l0` (or any worker) keeps calling the Direct API. While it runs, **even fast
foreground Direct calls hang** (they compete for the same API), so my proof script times out too.
- **Symptom:** even a 2-passage Direct gloss hangs.
- **Fix:** kill stuck workers OUT-OF-BAND before any new model work. Do not start new runs while one is
  stuck.

## The working rule (adopt this)

```text
1. NEVER run hermes/direct in the foreground for more than ~2 small passages.
2. NEVER launch a model worker with `&` in the tool shell (it becomes a wedging job).
   If a background run is truly needed: setsid + nohup + disown, and manage it via a separate
   detached command, not pgrep/pkill from the same shell.
3. Before any model run, confirm no stuck worker is alive (out-of-band), else the Direct API is saturated.
4. For "autonomous/unattended" runs, use the controller tick (`autonomy.py`) which is designed to run
   unattended — not a manual foreground invocation.
```

## Current known stuck processes (as of 2026-08-12)
- `run_autonomous_l0` workers (2) left from a 24-passage background run — they are wedged and hog the
  Direct API. They must be killed out-of-band (the tool shell wedges on them) before any new model work.

## Where this lives
This rule is also recorded in `handover/agent-2-integration/PROGRESS-AUTONOMOUS-2026-08-12.md` §6
(working practice). The autonomous factory controller itself (`autonomy.py`, `auto_run.py`) is designed to
run unattended without blocking — the stalling is a MY-TESTING practice issue, not a factory defect.

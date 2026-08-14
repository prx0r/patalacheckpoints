# THE WORKING TRANSLATION FACTORY — infrastructure + runbook

*2026-08-13 (late). This is the ACTUAL working state: how the autonomous factory produces canonical T1
glosses from raw Sanskrit, and exactly how it was run. Read this if you need to restart or extend it.
Supersedes earlier "AGENTIC-TRANSLATION.md" notes where they conflict. Verified live: 50-verse batches,
one work at a time, real `[and]-GLOSS (IAST)` output committing to the registry.*

---

## THE ONE-THING-THAT-FIXED-EVERYTHING

> **Hermes is an agent with file access. Give it a FILE PATH, not the content.**
> Every prior failure traced to passing the Sanskrit/content into the prompt as a **command-line
> argument**: it either blew the 2MB OS `ARG_MAX` (`[Errno 7] Argument list too long`) or returned
> empty/invalid because the model was "blind" to the repo. Writing the batch to a file and prompting
> hermes to **read that file** removed both problems at once.

---

## THE PIPELINE (what actually runs)

```
factory_loop.sh                    ← detached, nohup, repeat loop
   └─ factory_scheduler.py         ← one work at a time, parallel model calls
        └─ factory_batch.py        ← _run_generator (parallel) + _commit_proposals (serial)
             └─ t1_worker.py       ← the T1 layer
                  ├─ _write_batch_file()  → data/corpus/downloads/t1-batches/<work>-<ts>.jsonl (50 verses)
                  ├─ _build_file_prompt() → SMALL prompt: file path + T1 format + term senses
                  └─ chat_agentic()       → hermes chat -Q -q ... (agentic, reads the file, returns glosses)
```

### The four pieces that make it work
1. **`model.py::chat_agentic`** — agentic hermes call: `hermes chat -Q -q "<small prompt>" --yolo
   --max-turns 8`. `-Q` = clean programmatic output; agentic = file tools so it can read the batch file.
   (NOT `-z`, which is blind with no file access.)
2. **`t1_worker.py` file-based batch** — writes up to `T1_MAX_BYTES` (3MB default, ≈50 verses) of a work
   to a JSONL file, then prompts hermes with only the file path. No content in argv → no ARG_MAX.
3. **`factory_scheduler.py` one-work-at-a-time** — processes the highest-priority work's eligible jobs
   fully before the next (target-priority order, e.g. kramasadbhava p10 → mahanayaprakasha p11 → …).
4. **`factory_scheduler.py` parallel model calls** (`FACTORY_PARALLEL`, default 4) — runs the slow
   generator (model call) for several chunks concurrently, then **commits serially** (avoids registry
   write races: `_run_generator` in a `ThreadPoolExecutor`, `_commit_proposals` serial).

### The T1 output format (canonical)
```
[and]-GLOSS (IAST)     e.g.  [and]-abiding in preservation (sthitisthaṃ)
```
Stored per-verse as `{tokens:[{surface, iast, gloss, status, form:[and]-GLOSS (IAST)}]}` in the
`data/corpus/registries/t1-registry.jsonl`, status `MACHINE_PROPOSED`.

---

## HOW IT WAS RUN (exact commands)

```bash
# 1) clean the stale failure backlog (from the old big-batch bug) so the loop doesn't waste calls:
#    (back up then clear)
cp data/corpus/downloads/factory-failure-queue.jsonl /tmp/failure-queue.backup.jsonl
: > data/corpus/downloads/factory-failure-queue.jsonl

# 2) kill any old loop/scheduler
ps -eo pid,cmd | grep -E 'factory_loop|factory_scheduler' | grep -v grep | awk '{print $1}' | xargs -r kill -9

# 3) launch the overnight factory (DETACHED, nohup, survives session end)
( setsid nohup env PATALA_T1_MAX_BYTES=3000000 FACTORY_MODEL_CALLS=10 FACTORY_PARALLEL=4 \
    bash -c 'cd /root/projects/patala && exec bash pipeline/factory_loop.sh' \
    > /tmp/opencode/factory-night.log 2>&1 < /dev/null & )
```

## Tuning knobs
| Env | Default | Meaning |
|---|---|---|
| `PATALA_T1_MAX_BYTES` | 3000000 | max **file** size per T1 call (~50 verses); raise for bigger batches |
| `FACTORY_PARALLEL` | 4 | concurrent model calls per pass |
| `FACTORY_MODEL_CALLS` | 6 | model-call budget per scheduler pass |
| `FACTORY_THROTTLE` | 2 | seconds between committed chunks |
| `FACTORY_SLEEP` | 30 | seconds between passes |

## Monitoring
```bash
tail -f /tmp/opencode/factory-night.log            # loop/scheduler output
tail -f data/corpus/downloads/t1-stream.jsonl      # per-verse T1 results as they land
tail -f data/corpus/downloads/factory-audit.jsonl  # every commit/reject/retry
python3 pipeline/factory_status.py --all           # the corpus dashboard
ls data/corpus/downloads/t1-batches/               # batch files hermes is reading
rg 'kramasadbhava' data/corpus/registries/t1-registry.jsonl | wc -l   # T1 committed for a work
```

## How it chooses the next work / knows when done
- **Next work:** ranked by `pipeline/translation_targets.py` priority (lower = higher). One work is
  advanced fully, then the next.
- **What's eligible:** a passage is a job for a layer when its **upstream** layer is committed but this
  layer isn't (from `object_registry`, never guessed). DAG order: SOURCE→T1→ARGMAP→L0→L2→L200→C1.
- **Done:** a work is complete when it has 0 eligible jobs; the whole factory when eligible = 0 across
  all works.

## The commits that made it work
- `0c83f11` — T1 batch via FILE prompt (hermes reads the file; no ARG_MAX; ~50 verses/call)
- `9f5aec6` — parallel model calls (`FACTORY_PARALLEL`) with serial commits
- `6117018` — one-work-at-a-time scheduler
- `fa6033b` — T1 via agentic `chat_agentic` (not blind `-z`) + robust batch JSON parse

## Honest limits
- **T1 semantic quality is Agent 1's evals lane** (this is the production/shape gate → MACHINE_PROPOSED).
- Rate is bounded by the shared model API; larger `FACTORY_PARALLEL`/`PATALA_T1_MAX_BYTES` trade speed
  against the live runner.
- Genuinely-unanalyzable verses are honest `OPEN`/`GENERATION_FAILED`, capped at 3 retry attempts.

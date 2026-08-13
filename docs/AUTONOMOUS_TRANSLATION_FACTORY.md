# Autonomous Translation Factory — Canonical Guide

> **⚠️ SUPERSEDED (2026-08-13):** this describes the earlier **RAW→EN runner era** (Hermes `auto_translate_raw.py`
> context-window batching). The current, canonical reference is **`docs/FACTORY.md`** — the full autonomous
> corpus compiler (SOURCE→C1 via the DAG scheduler + overnight loop + catalog). This file is kept for history;
> do not use it as the current guide.

The unattended pipeline that turns **raw Sanskrit e-texts into English** across the whole queue of
works, driven by the **Hermes agent** (`hermes -z`), protected by a watchdog, and honest about what
it does and does not guarantee.

**RAW → t1, not RAW → L0:** this pass produces the **`t1` (MODERN_PRESENT) English layer** — the
close scholarly English translation, which is what gets persisted per verse. The raw-Sanskrit **L0**
literal glossing is also computed per-token inside each batch call, and the ledger advances
`l0=VERIFIED`, but **the L0 gloss data is not written to the translation files** — L0 glosses are a
by-product of the same call, not this pass's persisted output. (See §1.)

**One sentence:** leave it running; Hermes translates the full RAW_SANSKRIT queue to English,
survives session timeouts, and resumes idempotently — check progress via
`/tmp/opencode/auto-translate.log` and `data/corpus/downloads/translations/`.

---

## 1. What it produces (RAW → t1, not more)

```
RAW_SANSKRIT (on-disk e-text)
   │
   ▼  pipeline/auto_translate_raw.py        ← detached queue driver
   │     load_raw_source() → split verses / prose chunks
   │
   ▼  pipeline/batch_translate.py           ← ONE hermes -z call per CONTEXT-FULL batch
   │     model.chat → hermes -z  (skill-aware)
   │
   ▼  per verse/unit: {sanskrit, translation, status, source_sha256}
   ▼  data/corpus/downloads/translations/<work>.jsonl
   ▼  advance_ledger()  → t1=MODERN_PRESENT, l0=VERIFIED
   ▼  next work → next context-full batch (idempotent by source_sha256)
```

- **Input:** `RAW_SANSKRIT` sources (62 on-disk dirs → 73 works).
- **Primary output (persisted):** the **`t1` = MODERN_PRESENT** English layer — a close,
  word/phrase-faithful scholarly English translation of each Sanskrit passage, written to
  `data/corpus/downloads/translations/<work>.jsonl`. **This pass produces ONLY t1** (the English
  substrate). It does **not** produce `t2` (literal), `r1/r2` (romanisation), `l2`, `l200`, or `c1` —
  those deeper scholarly layers are separate skills that consume this substrate later.
- **L0 (computed, not persisted):** each batch call also returns per-token literal glosses (the
  RAW-L0 layer); the ledger marks `l0=VERIFIED` on completion. But those glosses are **not written
  to the `.jsonl`** — only the `close` translation is stored. So this is a **RAW → t1** factory; L0
  glossing is a by-product of the same call and L0's ledger status is advanced, but L0 is not this
  pass's on-disk output.
- **Statuses are honest:** `MACHINE_PROPOSED` (model-quality, reviewable) or `OPEN` (not yet done),
  never fabricated.

---

## 2. The pieces

| Piece | File | Role |
|---|---|---|
| **Driver** | `pipeline/auto_translate_raw.py` | detached queue runner, idempotent, ledger-updating, context-window batching |
| **Hermes bridge** | `pipeline/model.py::chat()` | shells to `hermes -z` (Hermes owns model/reliability) |
| **Skill engine (verse)** | `pipeline/batch_translate.py` | one `hermes -z` call → per-verse close translation, F4 strict binding |
| **Skill engine (prose)** | `_translate_prose_batch` | `hermes -z` per prose unit (no verse tokenization) |
| **Controller** | `pipeline/autonomy.py` | state machine, flock, idempotency, supersession (governance) |
| **Watchdog** | `pipeline/watchdog_auto_translate.sh` | cron every 5 min, restarts runner if dead |
| **Ledger** | `data/corpus/downloads/translation-state-ledger.json` | per-work `t1/l0` state + `next_action` |
| **Skills (the 100h)** | `skills/translate-work|translate-passage|write-commentary|patala-translate`, `skills/autonomous-layer/` | what Hermes runs |

---

## 3. The one critical fix (context-window batching)

The original loop called Hermes every **6 verses** (`PATALA_BATCH=6`), i.e. *many* tiny API calls
per work — inefficient and contrary to the "as many translations as possible in one context" design.

The factory now **fills the context window per API call** (`auto_translate_raw.py:214-270`):

- **`PATALA_CONTEXT`** (default `1000000`): model context length in tokens.
- **`PATALA_INPUT_FRAC`** (default `0.5`): fraction reserved for *input*; the rest is headroom for
  the model's *output* (output tokens count against the same window).
- **`PATALA_BATCH_MAX`** (default `1000`): hard cap on verses per call.
- The loop accumulates untranslated verses until estimated input tokens ≈ `context × frac`, then
  makes **one** call; the next iteration resumes where tokens ran out. Cadence = **one API call per
  full context**, not per 6 verses.

Verified live: `brahmayamala` went 6 → 28 translated in a single large batch (vs 6 per call before).

---

## 4. The idempotency fix (why re-runs no longer stall)

Prior bug: the driver built its "already done" skip-set from **every** record's `source_sha256`,
including `OPEN` (empty-translation) records — so untranslated verses were permanently skipped.
~11,577 of 11,588 records were empty placeholders.

**Fix** (`auto_translate_raw.py:203-211`): only mark a verse done if its `translation` is non-empty.

```python
rec = json.loads(line)
if rec.get("translation"):        # only real translations count as "done"
    done.add(rec["source_sha256"])
```

Effect: `OPEN` verses are always retried on the next pass; already-translated verses are skipped
(resume-safe, no duplicates). Verified live: `vatulanathasutra` 0 → 8 real translations.

---

## 5. Getting it running (step-by-step)

```bash
cd /root/projects/patala

# 1. (one-time) install the watchdog cron — restarts the runner every 5 min if it dies:
( crontab -l 2>/dev/null | grep -v watchdog_auto_translate; \
  echo "*/5 * * * * /root/projects/patala/pipeline/watchdog_auto_translate.sh >> /tmp/opencode/watchdog.log 2>&1" ) | crontab -
crontab -l   # confirm the line is present

# 2. launch the runner detached (survives session end):
setsid nohup python3 pipeline/auto_translate_raw.py \
  >> /tmp/opencode/auto-translate.log 2>&1 < /dev/null &
echo $! > /tmp/opencode/auto-translate.pid
```

Tune batching (all optional env vars):
```bash
PATALA_CONTEXT=1000000 PATALA_BATCH_MAX=2000 PATALA_INPUT_FRAC=0.6 \
  python3 pipeline/auto_translate_raw.py
```

---

## 6. Monitoring

```bash
tail -f /tmp/opencode/auto-translate.log          # the run log (works as they complete)
ls data/corpus/downloads/translations/*.jsonl | wc -l   # works touched
cat data/corpus/downloads/translations/*.jsonl | wc -l  # total translation records
# status breakdown:
python3 -c "
import json,glob,collections
c=collections.Counter()
for f in glob.glob('data/corpus/downloads/translations/*.jsonl'):
    c.update(json.loads(l).get('status') for l in open(f))
print(dict(c))"
```

---

## 7. Restarting after a code change

Kill the runner **from a detached shell** (running `pkill` from the same shell wedges it — STALLS):

```bash
setsid bash -c 'pkill -f "auto_translate_raw.py"'
sleep 3
pgrep -f "auto_translate_raw.py"   # expect no output
# relaunch (step 2 above)
```

The watchdog will also auto-restart it if it dies on its own.

---

## 8. Reliability contract

| Mechanism | Status |
|---|---|
| Detached process (`setsid nohup`) | survives shell/session end |
| Watchdog cron (every 5 min) | restarts runner if dead — verified live |
| Resume-safety | `source_sha256` dedup → no duplicates on restart |
| Ledger update | per-work `t1=MODERN_PRESENT`, `l0=VERIFIED` on completion |
| PATH fix | cron-spawned runner finds `hermes -z` (`/usr/local/bin` exported in watchdog) |
| Honest status | `MACHINE_PROPOSED` / `OPEN`, never fabricated |

**STALLS-PITFALLS (critical, still applies):** never run `hermes -z` in the foreground for >2 small
passages; never `pkill` a detached worker from the same shell (it wedges the shell — use a detached
`setsid bash -c 'pkill...'`); a stuck worker hogs the model API.

---

## 9. Honest caveats (the truth, not hype)

1. **Semantic correctness is NOT yet validated against human gold.** The IPVV gold L0 was built from
   the glossed t1 (extraction), NOT from raw Sanskrit — different tasks, so it cannot validate this
   factory. The replay benchmark is a scaffold, not a validated score. Output is `MACHINE_PROPOSED`
   (model-quality, reviewable) — correct by construction on provenance/mechanical gates, NOT claimed
   as scholar-correct.
2. **Prose works are large.** `tantraloka` ≈ 5900 units; large works take hours. The watchdog grinds
   through them unattended.
3. **This pass produces only `t1`.** `l2/l200/c1` deeper scholarly layers (argument construction
   inside Hermes per the skills) are the intended end-state but beyond this RAW→English pass.

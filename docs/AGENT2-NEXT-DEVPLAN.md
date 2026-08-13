# AGENT 2 — FULL DEV PLAN (for the next agent — begin work immediately)

> **SUPERSEDED for the next cycle.** The sivaqueue intake (below) is done. The new plan is
> `docs/AGENT2-ATLAS-FOUNDATION-PLAN.md` — do the **Atlas foundation (B) properly first** (Postgres DB +
> R2 asset store + bibliography→Atlas migration + OpenAlex-grammar API), then one vertical.

*2026-08-13. The complete execution plan for the next Agent-2 session: acquire all sivaqueue sources →
ensure they're in the factory queue → verify the live factory → link to the bibliography → polish the
whole factory. Grounded in the VERIFIED current state (every number checked against the live files).*

---

## 0. THE CURRENT STATE (verified, so you know what's real)

| Item | Value |
|---|---|
| **Live factory loop** | RUNNING (pid `647686`), producing SOURCE→C1 objects |
| **Live RAW→EN runner** | RUNNING (pid `362890`) |
| **Tests** | 19/19 PASS (deterministic) + IPVV-exemplar suite |
| **Works in the factory queue** (RAW_SANSKRIT, on-disk, translatable) | **73** |
| **sivaqueue works acquired** (in `sivaqueue-acquired.json`) | **44** |
| **acquired AND registered in the factory queue** | **35** |
| **sivaqueue3/4 targets compiled** (to `sivaqueue34-targets.json`) | **29** (23 have public e-text hints) |
| **Canonical DAG** | hardened — `contracts/CANONICAL-DAG.yaml` (single source of truth) |
| **Append-only event ledger** | `object-events.jsonl` (hash-chained) |
| **All committed + pushed** | `origin/agent2` (0 ahead/behind, latest `0062196`) |

**The core finding: the acquisition→queue link is PARTIAL.** 35 of 44 acquired works are in the
factory queue. **~9 acquired works + the 29 sivaqueue3/4 targets are NOT yet in the queue** — those are
the intake gap you'll close.

---

## 1. THE GOAL (what "done" looks like)

1. Every sivaqueue work that has an acquirable source is **downloaded → on-disk → registered RAW_SANSKRIT**
   in the ledger → the factory auto-picks it up.
2. Every work's bibliography record is **linked** (title, tradition, period, translation_status, source
   links) via the atlas (`data/atlas/`).
3. The factory is **verified healthy** (both systems, the catalog, the certificate).
4. The factory is **polished** (clean docs, no stale files, clear monitoring).

---

## 2. THE BUILD SEQUENCE (do these in order)

### STEP 1 — Verify the live factory is healthy (10 min, read-only)
```bash
bash pipeline/start_overnight.sh status        # both systems alive? + dashboard
python3 pipeline/catalog.py --all              # per-work bibliography + source + layers + audit
python3 pipeline/factory_certificate.py        # integrity + resume (PASS = clean)
tail -5 /tmp/opencode/factory-loop.log         # recent pass outcome
```
**Gate:** confirm both systems running + the factory is committing (not just alive). If the factory
loop died, the cron watchdog restarts it within 5 min; if not, `bash pipeline/start_overnight.sh start`.

### STEP 2 — Complete the sivaqueue acquisition (the main work)
**2a. Find the gap:** which acquired works are NOT in the factory queue?
```python
import json
ledger = json.load(open('data/corpus/downloads/translation-state-ledger.json'))['works']
acquired = json.load(open('data/corpus/sivaqueue-acquired.json'))['acquired']
raw = {k for k,w in ledger.items() if w.get('source',{}).get('available') and w['source'].get('format')=='RAW_SANSKRIT'}
missing = [k for k in acquired if k not in raw]
print(len(missing), missing)   # ~9 works to register
```

**2b. Register the acquired-but-unregistered works** in the ledger as RAW_SANSKRIT (point
`source_ref` at the on-disk `data/corpus/sources/<work>/<work>.txt`). Reuse the pattern in
`pipeline/acquire_sivaqueue_targets.py` / `pipeline/corpus_state.py`.

**2c. Acquire the sivaqueue3/4 targets** (the 29 compiled in `data/corpus/sivaqueue34-targets.json`):
- For the **23 with public e-text hints** (GRETIL / archive.org / vedicheritage / titus): download the
  Sanskrit source → `data/corpus/sources/<work>/<work>.txt`, then register as RAW_SANSKRIT.
- Extend `pipeline/acquire_sivaqueue_targets.py` (or add a new `acquire_sivaqueue34.py`) with the
  verified GRETIL/archive.org links from `sivaqueue34-targets.json`.
- The **6 needing manual acquisition** (scans/editions): record them in the access-manifest as
  `on_disk=false, needs_manual=true` — do NOT block the factory on them.

**2d. Add the sivaqueue34-companion metadata** (tradition/śākhā/period/author/register) to the target
records for context-engineering (this feeds the term-context packet).

**Gate:** `python3 pipeline/ingest_sivaqueue34.py` (re-run) shows the targets; the ledger's RAW_SANSKRIT
count grows from 73 toward ~100+; the factory auto-picks up new works on the next pass.

### STEP 3 — Link everything to the bibliography
The atlas (`data/atlas/`) is the bibliography. `sivaqueueSeed.ts` already maps sivaqueue1/2. For the
newly-acquired works:
- **3a.** For each new work, ensure there's a `BibliographyRecord` in `data/atlas/` (title, traditions,
  period, translationStatus, textSources, translations). Extend `sivaqueueSeed.ts` (or add the
  sivaqueue3/4 works).
- **3b.** Link the ledger → atlas: the ledger's `bibliographic_id` field (set by `corpus_state.py`
  from `data/atlas/*.ts`). Ensure the new works get a `bibliographic_id` so the catalog shows their
  bibliography.
- **3c.** Verify via `python3 pipeline/catalog.py --work <new_work>` → shows bibliography + source +
  layers.

**Gate:** every work in the factory queue has a `bibliographic_id` resolving to an atlas record, and
the catalog shows title/tradition/status for it.

### STEP 4 — Polish the whole factory (cleanliness)
- **4a.** Run the full test suite: `for t in pipeline/test_*.py; do python3 $t; done` — all 19 PASS.
- **4b.** Clean stale files: mark any obsolete scripts (e.g. `factory_run.py` is already marked
  OBSOLETE). Do NOT delete — mark + document.
- **4c.** Update `docs/FACTORY.md` + `CURRENT-STATE.md` + `live/agent2.md` with the new intake counts.
- **4d.** Re-run `factory_certificate.py` to confirm the factory is still integrity-clean after the
  intake (0 duplicates, resume PASS).

---

## 3. THE CANONICAL FILE MAP (where everything is)

| Concern | Path |
|---|---|
| Canonical DAG (single source of truth) | `contracts/CANONICAL-DAG.yaml` |
| Factory reference | `docs/FACTORY.md` |
| Intake (sivaqueue3/4 compile) | `pipeline/ingest_sivaqueue34.py` → `data/corpus/sivaqueue34-targets.json` |
| Acquisition (sivaqueue1/2) | `pipeline/acquire_sivaqueue_targets.py` + `pipeline/sivaqueue_targets.py` |
| Acquisition state | `data/corpus/sivaqueue-acquired.json` (44) · `sivaqueue-access-manifest.json` |
| Bibliography atlas | `data/atlas/` (bibliographySeed.ts, audited.ts, sivaqueueSeed.ts) |
| Factory queue (ledger) | `data/corpus/downloads/translation-state-ledger.json` (73 RAW_SANSKRIT) |
| Corpus catalog | `pipeline/catalog.py` |
| Overnight launcher | `pipeline/start_overnight.sh` + `OVERNIGHT.md` |
| Next-step reference | `docs/global/GLOBAL-NEXT-2026-08-13.md` |
| Agent-2 handover | `handover/agent-2-integration/HANDOVER-2026-08-13-LATE-SESSION.md` |

---

## 4. GUARDRAILS (do not violate)

1. **Do NOT kill the live factory/runner** — they're producing. Check status, don't restart unless dead.
2. **Do NOT touch `benchmarks/v0/` or `machinelearning/research/patala_ml/`** (Agent 1's lane).
3. **A wrong translation is worse than none** — the validator gates; don't weaken it to increase
   throughput.
4. **Registry is versioned** (not in-place edits); the append-only event ledger is the integrity trail.
5. **Registration must be honest** — only register a work as RAW_SANSKRIT if the on-disk source is
   actually a Sanskrit e-text (not a scan/PDF that needs OCR).
6. **Do NOT declare the architecture frozen** — the peer-review hardening is the standard.

---

## 5. THE ONE-SENTENCE CARRY-FORWARD

**The factory is built, running, and 19/19 tested; the next session's job is the INTAKE — register the
~9 acquired-but-unqueued works, acquire + register the 29 sivaqueue3/4 targets (23 via public e-texts),
link every work to the bibliography atlas, verify the live factory, and polish the docs — so the
autonomous backlog grows from 73 to ~100+ works and everything is auditably linked.**

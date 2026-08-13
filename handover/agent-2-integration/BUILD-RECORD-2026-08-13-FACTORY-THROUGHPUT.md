# AGENT 2 — FACTORY THROUGHPUT + INTEGRITY + PRIORITIZED QUEUE (build record)

*2026-08-13 (late session). Agent 2, canonical-stack mission. This session's work on the autonomous
factory: integrity fixes (the L0-ahead-of-T1 dependency violation), the prioritized next-best-target
queue, duplicate-work cleanup, and the batch/session throughput work — plus the two global strategy docs
(partnerships + access). Nothing here claims a semantic-quality result; it is production-machinery
hardening + throughput per the anti-theatre rule (AGENTS.md).*

---

## 1. The integrity fix (the big one)

**Problem:** `factory_batch.py` had `l0_inputs or srcs` and `l2_inputs or srcs` fallbacks that committed
L0/L2 from **raw SOURCE verses without a committed T1/L0 parent**. This was the source of the **773
bad-parent-hash integrity violations** (L0 ran ahead of its interpretive T1 floor).

**Fix:** fail-closed per the canonical DAG (`contracts/CANONICAL-DAG.yaml`). If the upstream layer isn't
committed, the layer is skipped with an explicit message — never fabricated from SOURCE.
- `pipeline/factory_batch.py`: L0 requires T1; L2 requires L0. Removed both `or srcs` fallbacks.

**Effect:** no new orphan L0s. The historical orphaned records remain (a data-migration item, not a
code fix).

---

## 2. The prioritized next-best-target queue

**Problem:** the scheduler ranked model jobs round-robin **alphabetically** across works — it didn't
spend budget on the highest-value targets.

**Fix:** `pipeline/factory_scheduler.py` now ranks works by **translation-target priority** (from
`pipeline/translation_targets.py`, lower = first), within which it round-robins so no single work
monopolizes:
```
p10 KRAMA_PACKET  kramasadbhava      p20 TIER1  kubjikamata
p11 KRAMA_PACKET  mahanayaprakasha   p21 TIER1  svacchandatantra
p12 KRAMA_PACKET  kalikulapancasatika ...
```
Unknown works (not in the target registry) sort last (priority 100). Added `--queue` for a read-only
preview of the ordering.

**Verified live:** after restart the scheduler committed T1 to kramasadbhava (p10) first, then
mahanayaprakasha/kubjikamata/svacchandatantra/netratantra — the Krama packet + tier-1 targets.

---

## 3. Duplicate-work cleanup (data integrity)

**Problem:** the same source was registered under underscore and plain-concatenated work ids
(e.g. `aghorasivas_ullekhini_on_ratnatraya` vs `aghorasivasullekhinionratnatraya`), inflating the
"80 works" count and fragmenting the corpus.

**Fix:**
- `pipeline/register_sources.py`: intake now dedups by **content hash across all works**, not just
  object_id (a verse whose content hash exists is never re-registered under a different name).
- Consolidated **9 duplicate work registrations** into canonical (underscore) ids. SOURCE registry
  objects: 14,021 → 13,418 (removed 603 orphaned objects; all verified zero-downstream).
- ObjectEvent chain still verifies `True`.

---

## 4. Minor integrity/ops fixes

- `pipeline/factory_status.py`: stale/version counts were **global** (every work showed the same
  number); now scoped per-work.
- `pipeline/factory_certificate.py`: removed the hardcoded `UPSTREAM` DAG copy; now derives from the
  canonical manifest (`object_registry.PREREQS`). Also fixed ARGMAP's parent (T1 → SOURCE).
- `pipeline/watchdog_auto_translate.sh`: removed deletion of `.autonomy.lock` — that's the autonomy
  **controller's** lock; `auto_translate_raw.py` uses no lock (its safety is source_sha256 dedup).
  Deleting it could unlatch the controller mid-run.

---

## 5. Throughput work: batching then persistent-session streaming

**Context:** the factory T1 path was calling the model **once per verse** (~36 verses/hour), while the
live RAW→EN runner fills the context (up to 1000 verses/call). Two sub-rounds this session:

### 5a. Batched T1 (`t1_worker.py`)
Rewrote `t1_generator` to pack a whole batch (all verses + Vidyut tokens) into **one prompt**, bind each
verse's gloss to its own `object_id`, and write a per-verse **stream log** (`t1-stream.jsonl`) as each
verse is produced. Added `_parse_batch` + `_build_batch_prompt`. All T1 tests pass.

### 5b. Persistent-session streaming (`t1_session.py`) — the "long context + document as it goes" design
**The tension:** long context is essential for correct glossing, but ONE giant call is a single point
of failure (10+ min, one timeout → everything lost, no partial output, no observability).

**Key discovery:** Hermes persists sessions (SQLite) and `--resume SESSION` continues them **with
accumulated context** (verified: a fact told in one resumed call is recalled in the next).

**Design (`pipeline/t1_session.py`, new):**
1. Open **ONE session per work**, seeded with the work's context packet (term-senses, school/period,
   translation neighbourhood, companion guides) — the long context lives here.
2. Feed verse-**chunks** via `--resume <session>` — each call adds verses while Hermes retains prior
   context (it "documents as it goes").
3. **Commit + stream-log each chunk immediately** — a failed chunk loses only that chunk (retryable),
   never the whole text.

**Integration:** `t1_worker.py` gained `t1_generator_session` (grouped by work, driven through the
session) + `make_t1_handlers()` env switch (`PATALA_T1_SESSION=1` to use sessions, default batched).
`model.py` `_hermes_call`/`chat` gained a `session` param (passes `--resume`).

**Note:** session streaming was implemented but the live test produced no output and was **aborted
before verification** — it is wired but **NOT yet proven live**; treat as EXPERIMENTAL_INFRASTRUCTURE
until a successful end-to-end run. The batched path remains the proven default.

---

## 6. Global strategy docs (partnerships + access)

Two new global docs, registered in `docs/global/README.md`, `docs/INDEX.md`, and the context chain
(`handover/CONTEXT-CHAIN.yaml`), confirmed through the context gate (34/34):
- `docs/global/globalpartnerships.md` — Pāṭala as the **integration/identity layer** over the fragmented
  Sanskrit ecosystem ("OpenAlex for Sanskrit"): 4 partner classes, identity/crosswalk principle
  (`PATA-W-…` survives external change), versioned-Assertion provenance, 11 adapters to integrate first.
- `docs/global/globalaccess.md` — the **access/rights/ecosystem model**: open-reference,
  controlled-corpus; 4 access layers (L0 identity → L3 core), asymmetric openness, the identifier as
  the highest-value product, institution/scholar attribution, AI-extraction protection, the social
  contract, and the crawler/access policy.

Also marked `docs/corpus/markguidance.md` and `docs/corpus/canonical_reference_map.md` as
**GUIDANCE/REFERENCE** (scholarly-content references, not global strategy), and updated
`docs/positioningpartners.md` to cross-link the new global doc.

---

## 7. Test status (this session)

| Suite | Result |
|---|---|
| `test_factory_scheduler` | ALL PASS |
| `test_factory_rebuild` | ALL PASS |
| `test_factory_certificate` | ALL PASS |
| `test_factory_status` | ALL PASS |
| `test_failure_queue` | ALL PASS |
| `test_object_events` | ALL PASS |
| `test_autonomy` | ALL PASS |
| `test_t1` + `test_t1_ipvv` | ALL PASS |
| ObjectEvent chain (`verify_event_chain`) | True |

---

## 8. Honest gaps / not done

- The **session-streaming path is not yet proven live** (test aborted before verification) — the
  batched path is the proven default. `PATALA_T1_SESSION=1` is the switch.
- The **historical orphaned L0s** (773 bad-parent-hash violations) remain; fixing them requires a data
  migration (supersede/rebuild), not the fail-closed code fix.
- **Live runner semantic yield** (RAW→EN mostly OPEN/empty, ~3.8% non-empty) is a pre-existing issue,
  untouched this session.
- Committed files excluded the **live registry data** (source/t1/object-events JSONL) because the running
  factory writes them concurrently — those are a separate data commit when the factory pauses.

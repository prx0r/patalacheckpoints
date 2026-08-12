# PHASE 1 — PROCESS NOTES (IPVV corpus build, agnostic & reproducible)

*2026-08-12. How the IPVV canonical passage corpus was built, so any agent can reproduce or extend
it for ANY work. The method is text-agnostic: it reads the structure already implicit in the layered
translation stack and turns it into a machine-readable passage corpus — it does NOT invent a new
segmentation.*

---

## 1. The Phase-1 goal

Every passage must:
1. have an immutable passage ID;
2. resolve to its Sanskrit source;
3. carry its published L2 translation;
4. link back to L0/T1 provenance;
5. appear in the READ view;
6. pass zero-loss validation.

## 2. The structure reused (the source of truth)

The hierarchy (from `translations/_stack/ipvv/README.md` + the L200 files):
```
work → volume (M00020/21/22) → vimarśa/adhikāra → kārikā → canonical passage
```
The canonical passage unit is the **chunk** (the L200 file's unit), linked to:
- **source range** (`M0002x lines N–M`) — present in every L200 file's IDENTIFICATION;
- **L0 records** (`l0/<chunk>.l0.jsonl`);
- **L2 read** (`pilot/pilot_<CHUNK>_L2_read.md` — the published prose);
- the **T1 chunk** (`02_t1/` or `01_t1/`).

The chunk→source-range map is the authoritative segmentation. It is already in the L200 files; we
parse it, we do not re-segment.

## 3. The tool

`/root/projects/patala/pipeline/phase1_ipvv_corpus.py`

```
python3 pipeline/phase1_ipvv_corpus.py --base /mnt/.../sanskritree --out /tmp/ipvv_phase1
```

What it does (agnostic):
1. **Parse L200 files** → per chunk: `{vol, source_start, source_end, section, l0, argmap, l2}`.
   - source range regex: `M0002[012] lines (\d+)[–-]?(\d+)?`
   - chunks without an explicit end get it from the next chunk's start (same vol).
2. **Resolve source text** — read the source vol's line range (`Volume {1,2,3}-M0002x-IAST.txt`).
3. **Attach L2 prose** — derive the L2 read path from the chunk name:
   `chunkV2-A-... → pilot_V2A_L2_read.md`; special case V3-B → `pilot_V3B_full_L2.md`.
4. **Attach L0 path** — `l0/<chunk>.l0.jsonl` (or `l0_v1/` for V1).
5. **Emit** `ipvv_passages.jsonl` (one record per passage) + `ipvv_ingest_report.json`.

## 4. The hard-stop discipline

Phase 1 FAILS if:
- source text disappears during segmentation;
- L2 text is orphaned (a chunk with no L2 read);
- duplicate passage IDs exist;
- source locators cannot resolve;
- any chunk is silently skipped;
- paragraph ordering changes;
- unresolved mappings are auto-guessed.

Unresolved items are emitted explicitly with `status: NEEDS_MAPPING` — never "best-effort" attached.

## 5. The result (2026-08-12)

| metric | value |
|---|---|
| chunks parsed | 52 |
| passages total | 52 |
| passages OK (source + L2 + L0 + provenance) | **49** |
| passages NEEDS_MAPPING | 3 (legacy V1 small chunks: `01_t1/upoddhata-mangala`, `01_t1/k1.1-kathamcit`, `01_t1/purvapaksa-opening` — no L2 read) |
| l2_orphaned | 0 |
| no_source | 0 |
| duplicate ids | 0 |
| provenance_resolves | True |
| zero_loss | **False** (honestly reflects the 3 NEEDS_MAPPING) |

Artifacts (in `--out`, e.g. `/tmp/ipvv_phase1/`):
- `ipvv_passages.jsonl` — canonical source/passage records (id, work_id, chunk, vol, source start/end/text, l0, l2, l2_text, section, status).
- `ipvv_ingest_report.json` — counts + zero-loss + unresolved + provenance failures.

## 6. To reproduce for ANOTHER work

If the work has the same layered stack (token-T1 + L200 with source ranges + pilot L2 reads):
1. Point `--base` at that work's repo root.
2. Adjust `chunk_l2_path` if the L2 naming differs.
3. Set the `work_id` (currently hardcoded to IPVV — parameterize if needed).
4. Run; read `ipvv_ingest_report.json`; resolve the `NEEDS_MAPPING` items.

The principle: **read the structure already implicit in the layered stack; emit it as machine
records; validate zero-loss + provenance; flag the unresolved, never guess them.**

## 7. NOT done in Phase 1 (deliberately)

- **No C1/L200 ingestion** — that is a later phase. Phase 1 proves the corpus mapping (Sanskrit ↔
  passage ↔ L2 ↔ provenance) is sound first.
- **No new platform features** — no new frontend, no new segmentation, no silent resolution.

---

## 8. Phase-1 PUBLICATION (lazy-JSON — done 2026-08-12)

The 49 OK passages are published as **lazy JSON assets** (NOT bundled TS):

- **Store:** `data/published/ipvv/` — `index.json` (structural only) + one `.json` per passage. Total **2.3MB**.
- **Loader:** `data/corpus/published.ts` rewritten as a lightweight registry — metadata/index only, lazy-loads from disk server-side. No `~90MB` payloads in the bundle.
- **Single source of truth:** `getPublishedTranslation(id)` is the ONE loader used by BOTH `/read` (via `/api/passages/:id/translation`) and `/api/resolve`. Reader and resolver consume the same canonical object; `ipvvResolveImmutable()` is the shared immutable-id authority.
- **Invariants hold:** bad locators → explicit `undefined` (→404), never silent fallback; source spans + L0/L2 provenance + ordering preserved; duplicate ids 0.
- **Build sane:** `.next/static` = **1.3MB** (the earlier ~90MB bundled-TS caused OOM). The orphaned 168MB generated `.ts` units were converted to `.json` and archived (`data/corpus/units/_archive_generated/`) so tsc ignores them — provenance preserved, not deleted.

**Reproduce:**
```
python3 pipeline/emit_published_json.py --in <phase1>/ipvv_passages.jsonl --out data/published/ipvv
npx tsx tests/ipvv_published.test.ts     # V1/V2/V3 + bad locator + immutable-id resolve
npm run build
```

**Tests:** `tests/ipvv_published.test.ts` — 21 checks, ALL PASS (V1, V2, V3 load; bad locator → undefined; immutable-ID resolve returns the same passage).

---

## 9. Phase 0 + Phase 2 (the deterministic substrate — done 2026-08-12)

After Phase-1 publication, the deterministic content + verification floor was built so the ML master
has a complete machine-queryable substrate.

### Phase 0A — C1 wired into the published objects
- `pipeline/attach_c1.py` attaches the 63 C1 read/ renderings into the 49 published passage JSONs.
- Shape: `c1.verse_commentary[]` (one entry per covering C1) — the exact shape the reader's
  Commentary toggle renders (`pub.c1.verse_commentary`). **V1 chunks bundle multiple sub-C1s**
  (e.g. chunkH → V1H + V1-upoddhata-k6-k8): 17 passages have >1 C1, 72 total entries.
- `shapeIpvv` (published.ts) maps the store's c1 into the reader shape; `getPublishedTranslation`
  still serves /read + /api/resolve the SAME object.

### Phase 0B — c1/source structured records completed
- `pipeline/gen_c1_source.py` mechanically derives the missing 53 c1/source/ records from the read/
  renderings (SUMMARY ≈ body, KEY TERMS from Terms:, RELATED from See also). Now 63 total
  (10 hand-authored + 53 derived). Deterministic, no model call.

### Phase 0C — deterministic THEMES exposed
- `data/corpus/themes.ts` derives MACHINE_PROPOSED themes from shared technical lemmas across C1s
  (the structured signal the pilot identified). `get_themes` MCP tool + `/api/themes`.

### Phase 2 — the deterministic verification floor (EXPOSE services)
- `lib/verify.ts` + `/api/verify/{quote,claim-structure,trace-dependency,counterevidence}` —
  deterministic, over existing data, never silent-fallback. The ML master's INFER services build
  ABOVE these. 4 MCP tools added (verify_quote, verify_claim_structure, trace_dependency,
  find_counterevidence).

### Benchmark seed handover
- `machinelearning/BENCHMARK_HANDOVER.md` documents the existing fixtures (gold.ts, qa_v1_gold 34,
  stall-log 60) so the ML master builds Benchmark v0 from real data.

**Reproduce:**
```
python3 pipeline/attach_c1.py --store data/published/ipvv --c1 <sanskritree>/c1 --write
python3 pipeline/gen_c1_source.py --c1 <sanskritree>/c1 --write
npx tsx tests/ipvv_published.test.ts
npm run build
```

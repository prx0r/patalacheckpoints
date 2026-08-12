# IPVV STACK — Structure & Pāṭala Integration (ground-truth audit)

*2026-08-12. An intimate, verified review of the actual IPVV translation stack and how it maps onto the
current Pāṭala integration. This re-grounds the ML plan (`MLUSEINPATALA.md`) in the real data — the
structures the models would learn over and the exact wiring gaps. Every number was checked against the
live files, not recalled.*

---

## 1. The IPVV stack (the source of all Pāṭala content) — verified

```
00_source/  base texts (Torella IPK + M00020-22)
01_t1/      02_t1/     hyper-literal T1 chunks — the IMMUTABLE substrate (35 chunks)
02_r1/      03_t2/     adversarial reviews / opposing readings
04_r2/      05_t3/     adjudications / final resolved
06_c1/      c1/        commentary (see §2)
l0/ l0_v1/            token-level literal records (L0)
l200/ l200_legacy/     cross-layer audit (66 files; 63 audits + spec/ledger/review)
pilot/                  L2 reads + argument maps (108 files)
specs/                  the specs (THEMES, C1, provenance, patalaml, ...)
```

### The derivation chain (each layer derives from the one below, provenance preserved)
```
SANSKRIT (M00022 + Torella)
  ↓ L0   token + IAST + gloss  (l0/*.jsonl — verified: V2-O has 3444 tokens, 3310 PARSED, 134 AMBIGUOUS, 0 FAILED)
  ↓ L1   controlled Sanskrit-close
  ↓ L2   READ prose (pilot/pilot_*_L2_read.md)
  ↓ L200 cross-layer audit (how L2 was derived)   → l200/<chunk>.md
  ↓ C1   passage commentary (what it means)       → c1/read/ + c1/source/
  ↓ THEMES / ESSAYS / EDUCATION
```

### The four files a single passage touches (verified on V2-O)
| File | Role | Verified content |
|---|---|---|
| `02_t1/chunkV2-O-saptamo-vimarsa.md` | immutable T1 | the maṅgala + kārikā 1 (pratibhā) + anvaya-vyatireka plan |
| `l0/chunkV2-O-saptamo-vimarsa.l0.jsonl` | L0 tokens | 3444 records; e.g. `L14:T4 evam → "thus"` |
| `pilot/pilot_V2O_ARGUMENT_MAP.md` | the argument | the plan, kārikā 1, the 14-verse structure, OPEN items |
| `pilot/pilot_V2O_L2_read.md` | L2 prose | 3 ¶ (support; 14-verse plan; the pratibhā), fidelity note |
| `l200/V2O-saptamo-vimarsa.md` | the audit | 8 sections; 6 MT decisions; 3 IA; typed crossrefs; editor-reviewed |
| `c1/read/c1_V2O-orderless-support.md` | C1 | the continuous commentary (pratibhā, order-less knower) |

### The C1 layer (verified: 63 read renderings)
- **63 read/** continuous renderings (100–450 words each; `c1_<id>-<topic>.md`)
- **10 source/** structured records (SUMMARY/FUNCTION/KEY TERMS/LOCAL CONTEXT/EXPLANATION/BOUNDARY/RELATED)
- **63 distinct passage-ids**: V1A–N (27 C1s, fine-grained: upoddhata/k1.x/purvapaksa splits), V2A–S, V3A–P

### The L200 layer (verified: 63 audits, all `editor-reviewed`)
The frozen 8-section schema: IDENTIFICATION / PUBLISHED READING / DERIVATION MAP /
MATERIAL TRANSLATION DECISIONS / INTERPRETIVE ASSERTIONS / SOURCE LAYER / CROSS-REFERENCES (typed) /
OPEN / REVIEW STATE. `l200_validate.py` → **ALL CHECKS PASS**.

---

## 2. The current Pāṭala integration (verified 2026-08-12)

The architecture has evolved this session into a **lazy JSON store** (no more bundling ~90MB of
spans into the client):

```
data/published/ipvv/
  index.json            structural only: work, passages[id, immutable_id, locator, order, file, vol]
  pt-passage-<slug>.json   one per OK passage (the canonical phase-1 record) — 49 records
```

- `data/corpus/published.ts` — the single loader `getPublishedTranslation(id)` reads the index lazily
  and shapes each record into the `PublishedTranslation` the reader + `/api/resolve` BOTH consume.
  **Same canonical object for reader and resolver** — the invariant.
- `shapeIpvv()` (published.ts:102) turns a lazy record into a PublishedTranslation:
  one coarse source span + L2 prose target + provenance, **decisions: [], evidence: [], NO c1**.
- The 35 V2/V3 generated units were **archived** to `data/corpus/units/_archive_generated/` (JSON) —
  no longer imported into published.ts.
- `pipeline/emit_published_json.py` — emits index.json + one JSON per OK passage from
  `ipvv_passages.jsonl` (the phase-1 canonical records).
- New: `pipeline/emit_published_json.py`, `tests/ipvv_published.test.ts`, `docs/GAPS.md`,
  `machinelearning/`.

### Verified numbers
- **49 published passages** (data/published/ipvv/, indexed)
- **49 with `l2_text`** (the L2 READ prose)
- **35/49 match a C1 read** by chunk-id normalization (V2/V3 all match; the 14 unmatched are the V1
  chunks — because C1 splits each V1 chunk into finer upoddhata/purvapaksa/k1.x sub-commentaries)
- **0 of 49 carry `c1`, `l200`, or `decisions` in the emitted JSON** (verified: keys are only
  id/work_id/chunk/vol/source/l0/argmap/l2/l2_text/section/status/immutable_id)

---

## 3. The wiring gap — C1 was NOT in the published objects (now RESOLVED, 2026-08-12)

**This was the single most important integration finding, and it has been fixed.**

**The reader has a Commentary toggle (`pub.c1.verse_commentary`), fully implemented and styled.**
The 1.5.11 hand-authored unit demonstrates it (`c1: { body, verse_commentary: [{locator, commentary}] }`).
Previously the **49 emitted IPVV passages had NO `c1` field** — the Commentary toggle showed the
placeholder for every IPVV passage except 1.5.11.

**RESOLVED (2026-08-12):** `pipeline/attach_c1.py` now attaches the 63 C1 read/ renderings into the
49 published passage JSONs as `c1.verse_commentary[]` — the exact shape the reader renders. Verified:
`shapeIpvv` (published.ts) maps the store's c1 into `verse_commentary[]`; the reader renders it; the
1.5.11 hand-authored unit still works; all tests pass; build clean.

### Why the 14 V1 chunks "don't match" a single C1 (and why that's fine)
The C1 layer is **finer-grained** than the T1 chunk: a V1 chunk splits into multiple C1s (e.g.
`chunkH-k1.8-caitanyamajada-pratibimba.md` ↔ C1s `V1-upoddhata-k6-k8-caitanyamajada`, etc.). The reader's
`verse_commentary[]` array is exactly the right shape to hold **multiple C1s per passage** — so a chunk
can bundle several C1 commentary blocks, each with its own locator. The wiring is: one chunk →
`c1.verse_commentary = [ each covering C1 ]`.

### The wiring spec (what to build)
For each published passage record, attach the covering C1s:
```
c1: {
  body: "<the passage's L2-first-sentence as a one-line summary>",
  verse_commentary: [
    { locator: "V2-O · kārikā 1", commentary: "<c1/read/c1_V2O-orderless-support.md body>" },
    ...   // one per covering C1, mapped chunk→C1-id
  ],
  claim_links: [...],   // optional: map C1 claims → target spans
}
```
Plus optionally the L200 audit + decisions:
```
l200: { ...the audit sections... }   // for the AUDIT view / /api/resolve
decisions: [...]                     // derived from MT decisions
evidence: [...]                      // from IA + scholarship
```

### This is the prerequisite for the ML work
Per `MLUSEINPATALA.md` Phase 0A: **you cannot learn over C1s the reader/API doesn't expose.** Wiring the
63 C1s into the 49 published objects (via `verse_commentary[]`) is the precondition for:
- the C1 retrieval layer (Phase 3/4 — embedding the C1s),
- the THEMES layer (which clusters C1s — the pilot proved the mechanism on exactly these),
- the THEMES pilot run against the benchmark + `/api/themes` + MCP tool (Phase 0B — after the benchmark),
- the claim-verification + vertical-fidelity work (Phase 5 — C1→Theme→Guide conservation).

---

## 4. How the ML plan applies to the ACTUAL structures (grounded)

| ML plan item | The real structure it operates on | Status |
|---|---|---|
| **C1 retrieval** | `c1/read/*.md` bodies (63) → embed per-passage | content exists; **now in the published objects** (verse_commentary[]) |
| **THEMES discovery** | the C1 set + `See also` edges + KEY TERMS (the pilot's exact inputs) | mechanism proven; **deterministic proposals exposed** (`/api/themes`) |
| **Multi-resolution retrieval** | span (L0) → passage (l2_text) → C1 → theme → work | the ladder exists as files; **passage + C1 served** |
| **Claim extraction** | C1/essay prose → atomic claims | none yet |
| **verify-claim** | assertions + evidence roles | primitives exist; **4 verify services shipped** |
| **Vertical fidelity** | L2→C1→Theme→Guide conservation | none yet; C1 content ready |

**Progress (2026-08-12):** Phase 0A done — the 63 C1s are wired into the 49 published objects
(`c1.verse_commentary[]`, V1 multi-C1), the 53 `c1/source/` records are complete (63 total), THEMES
are exposed (`/api/themes` + `get_themes` MCP), and the 4 deterministic verify services are shipped
(`/api/verify/*`). The substrate the retrieval/verification/learning phases need is now in place on
real data.

---

## 5. Key files (for the next agent)

| Path | Role |
|---|---|
| `/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv/` | the IPVV stack (source of all content) |
| `.../c1/read/` (63) · `.../c1/source/` (10) · `.../l200/` (63 audits) · `.../pilot/` (L2 + maps) | the layers |
| `/root/projects/patala/data/corpus/published.ts` | the single loader (`getPublishedTranslation`, `shapeIpvv`, `listUnitPassages`) |
| `/root/projects/patala/data/published/ipvv/index.json` + `pt-passage-*.json` | the lazy store (49) |
| `/root/projects/patala/pipeline/emit_published_json.py` | the emitter |
| `/root/projects/patala/app/read/[work]/[locator]/page.tsx` | the reader (Commentary toggle at line ~239) |
| `/root/projects/patala/data/corpus/units/isvarapratyabhijnavivrtivimarsini-1.5.11-published.ts` | the hand-authored C1 exemplar (`c1.verse_commentary`) |

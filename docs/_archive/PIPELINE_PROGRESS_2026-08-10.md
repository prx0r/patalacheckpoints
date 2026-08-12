# Pāṭala — Pipeline + Stack Progress (2026-08-10)

*The translation pipeline and the per-work stacked artifact. Complements
`PROGRESS_2026-08-10.md` (the API/hub work) and `translations/STATUS.md` (the corpus).*

---

## 1. What this work built

### A. The automated translation pipeline (`pipeline/`)
The structured, audited flow `T1 → R1 → T2 → R2 → T3 → T3.1 → C1`, aligned to
`corpus/targets/translation_flow_spec.md` + the house policies.

| File | What it is |
|---|---|
| `schema.py` | the passage-record data structure + stage constructors + lineage |
| `audit.py` | validates a record at every stage (schema + epistemic honesty) |
| `prompts.py` | the house prompts injected into the model per stage |
| `model.py` | the opencode-go model client |
| `run.py` | the orchestrator |
| `exemplars.py` | **2 gold exemplars** built by hand from real on-disk material |
| `exemplars_cli.py` | dump / audit / export the gold exemplars |
| `from_t1.py` | build a record from an existing on-disk T1 file (no model) |
| `gold_from_t1.py` | batch-generate gold records from on-disk T1s (23 produced) |
| `gold_records/` | 23 gold passage records from real Kramasadbhāva T1 verses |

### B. The FoJin-style validation/tracking layer (`pipeline/validate.py`)
- Crawls every corpus passage + every gold record.
- **Referential integrity**: unique ids, work resolves, source present.
- **Epistemic invariants**: no machine-output-as-reviewed, stage ordering, T3-needs-R2, [X] honesty.
- **Per-passage tracking state**: `valid / needs_review / invalid`.
- **Conformance report** (`--report`), now wired into `tests/api_suite.py` (74/74 passing).

### C. The per-work stacked artifact (`pipeline/stack.py` + `docs/STACKED_ARTIFACT_SPEC.md`)
The spec the project was missing: one directory per work, each stage as a floor,
each floor both content and audit, and a machine-readable `AUDIT.md`.

```
translations/_stack/{work_id}/
  00_source/   01_t1.md  02_r1.md  03_t2.md
  04_r2.md  05_t3.md  06_t3_1.md  07_c1.md  AUDIT.md
```

- **13 canonical works assembled** from the flat corpus (mapped to bibliography ids).
- **sivasutra** is the fullest: 7 floors (T1/R1/T2/R2/T3/C1 + source).
- The stack **wraps** the flat corpus (pointers, not moves); no file is overwritten.
- `AUDIT.md` per work carries floors state + passage validity + integrity.

### D. A real bug fixed (the validation layer proved its worth)
The kramasadbhava corpus had **7 duplicate/wrong passage ids**: the raw segmenter
treated paṭala **colophons** (`dvitīyaḥ paṭalaḥ ||2/2 ||`) as verse boundaries.
Fixed `scripts/segment-kramasadbhava.mjs` to exclude colophons → **563 clean passages,
0 duplicates**.

## 2. Current numbers

```
Corpus passages       4,395   unique 4,395   dups 0   valid 563   needs_review 3,832
Gold records             23   all needs_review (T1-only — honest: missing time-place-context)
Stacked works            13   sivasutra fullest (7 floors)
tests/api_suite         74/74 passing (incl. corpus integrity + epistemic gates)
```

## 3. What's next

- **Wire the pipeline → API/MCP** (serve the validated records through `/api/passages`).
- **Anchor-loading** at R1/R2 (the anchor-as-referee rule from the flow spec).
- **Term-proposal promotion** from records → `terms.json`.
- **Alias mapping** for flat-filename ↔ canonical-id differences (e.g. `kubjika` → `kubjikamata`).
- Run a full work through the pipeline (model) to the `07_c1.md` commentary, then wire C1 → essays/videos.

## 4. Large generated data (not committed)
`data/manuscripts.json` (5.5MB, OCHS source) and `data/corpus/passages/kubjikamata.jsonl`
(1.5MB) are gitignored — regenerate via `scripts/convert-ochs.py` and `scripts/segment-t1.mjs`.

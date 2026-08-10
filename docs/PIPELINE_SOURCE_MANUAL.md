# Pāṭala Translation Pipeline — Source Code Manual

*2026-08-10. The deep-dive reference for the translation pipeline + the per-work
stacked artifact. For a peer reviewer or a future developer: how the code is
organized, how the data flows, how each module works, and how to run it. Companion
to `docs/STACKED_ARTIFACT_SPEC.md` (the what/why) and `docs/api/` (the API).*

---

## 1. The two codebases

| Codebase | Path | Role |
|---|---|---|
| **Pāṭala hub** | `/root/projects/patala` | the pipeline, the API, the passage corpus, the bibliography, the docs |
| **Sanskrit corpus** | `/root/projects/sanskritree` (= `/mnt/.../sanskritree`) | the raw Sanskrit, the flat translation files, the dossiers, the anchors |

The pipeline lives in `patala/pipeline/` and reads the corpus from
`sanskritree/translations/`. The two are linked by stable `work_id` + passage ids.

---

## 2. The pipeline modules (`patala/pipeline/`)

| Module | Responsibility |
|---|---|
| `schema.py` | the passage-record data structure, stage constructors, lineage |
| `audit.py` | validates a record at every stage (schema + epistemic honesty) |
| `prompts.py` | the house prompts injected into the model per stage |
| `model.py` | the opencode-go model client |
| `run.py` | the orchestrator (calls the model, stores + audits each stage) |
| `exemplars.py` | 2 hand-built gold exemplars from real on-disk material |
| `exemplars_cli.py` | dump / audit / export the gold exemplars |
| `from_t1.py` | build a record from an existing on-disk T1 file (no model) |
| `gold_from_t1.py` | batch-generate gold records from on-disk T1s |
| `stack.py` | assembles the per-work stacked artifact + writes `AUDIT.md` |
| `validate.py` | the FoJin-style per-passage validation/tracking + conformance report |
| `gold_records/` | 23 generated gold passage records (Kramasadbhāva 1.x) |

---

## 3. The data structure (`schema.py`)

One record per verse. See `docs/TRANSLATION_SCHEMA.md` for the full field notes.

```json
{
  "passage_id": "tantra:text:kramasadbhava:1.8",
  "work_id": "kramasadbhava",
  "location": { "chapter": 1, "verse": 8 },
  "source": { "source_edition": "...", "source_file": "...", "source_text": "..." },
  "stages": { "T1": {...}, "R1": {...}, "T2": {...}, "R2": {...}, "T3": {...}, "T3.1": {...}, "C1": {...} },
  "audit": { "T1": [...findings...], ... },
  "lineage": [ { "stage": "T1", "created_by": "...", "derived_from": null }, ... ],
  "policy": { "translation_contract": "1.0.0", "style_guide": "1.0.0", "schema": "1.0.0" },
  "review_status": "C1"
}
```

### The stages (constructors in `schema.py`)
- `stage_T1(close, reader_draft, flags, notes, lexical_decisions, grammatical_notes, parallels, time_place_context)` — the working translation + evidence + required header.
- `stage_R1(detail, verdicts, cruxes, anchor_quote, source)` — the adversarial critique: maps genuine CRUXES (id/type/assumption/rivals/evidence-needed) + verdicts + commentary stubs.
- `stage_T2(close, strategy)` — the strongest materially-different defensible rival (SEES T1+R1; difference budget; no manufactured disagreement).
- `stage_R2(chosen, reasoning, hard_core, divergence, readability, school_context, commentary, equal_alternates, rejected, is_open, decisions)` — the adjudication BY DECISION (CONSTRAINED/PREFERRED/OPEN/RECONSTRUCTED).
- `stage_T3(resolved, open_flags, editorial_notes)` — the current resolved scholarly candidate.
- `stage_T31(reading)` — the reader's edition (derived from T3).
- `stage_C1(interpretation, challenges)` — the commentary; may CHALLENGE T3 (→ RevisionProposal → T3 v2) but never mutates it.

`set_stage(record, payload, created_by, derived_from)` appends a VERSION (never overwrites)
and updates `pipeline_stage` + `origin`. `set_review(record, review)` records a scoped
ReviewEvent and is the ONLY thing that promotes `editorial_status`. `get_stage(record, stage)`
reads the current version; `record["versions"][stage]` holds all versions.

**Three independent dimensions (never conflated):**
```
pipeline_stage    where in the flow (T1 → ... → C1)   — set by set_stage
origin            who produced it (machine / human)   — set by set_stage
editorial_status  proposed / reviewed / accepted / disputed — set ONLY by set_review
```
So `pipeline_stage = R2, origin = machine, editorial_status = proposed` is honest.

---

## 4. The audit (`audit.py`)

Two jobs:
1. **Schema validity** — well-formed ids/locations/enums; stage ordering (contiguous
   T1→…→C1); T3 requires a prior R2.
2. **Epistemic honesty** — no empty close/resolved/reading; `[X]`/typed flags valid
   (`TXT GRAM LEX DOCT WIT SUP X`); [X] not laundered; machine output never presented
   as reviewed.

Findings are `{level: error|warn, stage, code, message}`. `audit_ok()` = no errors.

---

## 5. The validation/tracking layer (`validate.py`)

- `load_corpus()` — reads `data/corpus/passages/*.jsonl` (the API corpus).
- `load_gold_records()` — reads `pipeline/gold_records/*.json`.
- `validate_record(r)` — normalizes either shape, runs `audit_record`, returns
  `{status, errors, warnings, stages, review_status}`. Status ∈ `valid | needs_review | invalid | pending`.
- `referential_integrity(records)` — dup ids, missing work, missing source, dangling.
- `run_corpus_audit()` — validates + tracks everything.
- `conformance_report()` — the machine-verifiable summary (`--report`).

```
valid        no errors, no warnings
needs_review  warnings only (flag for human)
invalid      error-level findings
```

---

## 6. The stack builder (`stack.py`)

Assembles `translations/_stack/{work_id}/` from the flat corpus (wraps, doesn't move):

```
00_source/   01_t1.md  02_r1.md  03_t2.md  04_r2.md  05_t3.md  06_t3_1.md  07_c1.md  AUDIT.md
```

- `detect_works()` — the canonical ids (from `data/atlas/*.ts`) ∩ files present.
- `find_floor_files(work_id)` — matches flat filenames to floors (`p2_{w}`→R1,
  `t3_{w}`→T3, `c1_{w}`→C1, ...).
- `assemble(work_id)` — creates the dir + floor pointers.
- `write_audit(work_id)` — writes `AUDIT.md` (floors state + passage validity).
- CLI: `python3 -m pipeline.stack <work>` · `--list` · `--all`.

---

## 7. The prompts (`prompts.py`)

Each stage has a `sys_*` system prompt encoding the house policy
(STYLE_GUIDE + EVIDENCE_POLICY + the stage's job) and a `user_prompt(stage, record)`
builder that assembles the current record's relevant floors. The model follows the
process; the pipeline stores + audits the result.

---

## 8. How to run

```bash
# gold exemplars (no model)
python3 pipeline/exemplars_cli.py --audit
python3 pipeline/gold_from_t1.py --all-kramasadbhava

# validation + conformance (no model)
python3 pipeline/validate.py --report

# assemble the stack (no model)
python3 -m pipeline.stack --all

# run the full flow on one verse (needs OPENCODE_GO_API_KEY)
export OPENCODE_GO_API_KEY=<key>
python3 pipeline/run.py <source.txt> <work_id> \
  --edition "..." --verse 49 --stages T1,R1,T2,R2,T3,T3.1,C1 --out out.json
```

---

## 9. The invariants (locked)

1. Stable IDs never depend on mutable wording.
2. Work ≠ witness ≠ digital representation ≠ canonical passage.
3. Annotations are independent from the base text and independently addressable.
4. Machine output always enters as a proposal, never authority.
5. Every meaningful scholarly judgment can carry evidence and review history.
6. Translation prose and interpretive decisions have independent version histories.
7. Convenient API bundles are projections over normalized scholarly data, not the
   canonical data model.

*(These come from the peer review of the pipeline against FoJin/Bilara/BDRC/SARIT/
OpenPecha/84000 — recorded in `docs/PEER_REVIEW_REDTEAM.md`.)*

---

## 10. Known gaps (honest)

- **Storage is currently the blob** (per-passage `stages` dict); the "normalize on
  write / bundle on read" refactor (invariant 7) is the next data-model step.
- **Anchor-loading** at R1/R2 not yet wired (the anchor-as-referee rule).
- **Term-proposal promotion** → `terms.json` not yet wired.
- **Alias mapping** for flat-filename ↔ canonical-id (e.g. `kubjika` → `kubjikamata`).
- **T3.1-in-one-call** batching; R1/R2/C1 must stay independent (adversarial).

# Pāṭala — Handover (2026-08-10)

*The single entry point for the next agent. Supersedes `HANDOVER_SITE.md` and
`HANDOVER_MCP_API.md` (both earlier and now partially outdated). Covers the whole
system: the two codebases, what's built, how to navigate, how to run it, and what's next.*

---

## 1. What Pāṭala is

Pāṭala (repo: **https://github.com/prx0r/patala**, local `/root/projects/patala`) is the
**Tantra Hub** — the authority, provenance, relationship, expert-validation and workflow
layer for tantric textual heritage. It sits *between* manuscript repositories (OCHS,
Muktabodha, GRETIL) and the people/AI that use them.

The mission: **make the textual landscape of Tantra navigable.** Two halves:

1. **The translation pipeline + corpus** (the content) — produces structured, audited
   translations T1→T3.1 + commentary (C1) for each work.
2. **The hub + API/MCP** (the infrastructure) — serves the bibliography, the passage
   corpus, the evidence bundles, the terms, and the audit chain.

**Core invariant:** *machines propose, humans review.* "AI proposes ≠ Pāṭala asserts."
Every translation-status claim is "No complete English translation located", never
"Untranslated."

---

## 2. The two codebases

| Codebase | Path | Role |
|---|---|---|
| **Pāṭala hub** | `/root/projects/patala` (git repo) | the pipeline, the API, the passage corpus, the bibliography, the docs |
| **Sanskrit corpus** | `/root/projects/sanskritree` (= `/mnt/HC_Volume_106427611/sanskritree`) | the raw Sanskrit, the flat translation files, the dossiers, the anchors |

The pipeline reads the corpus from `sanskritree/translations/`. They are linked by
stable `work_id` and passage ids. (Note: the MCP's `TANTRA_CORPUS` default points at
`/mnt/HC_Volume_106427611/sanskritree/translations` — same path via symlink.)

---

## 3. What's built (validated)

### The translation pipeline (`pipeline/`)
The structured, audited flow `T1 → R1 → T2 → R2 → T3 → T3.1 → C1`:
- `schema.py` — the passage-record data structure + stage constructors + lineage
- `audit.py` — validates a record at every stage (schema + epistemic honesty)
- `prompts.py` — the house prompts injected into the model per stage
- `model.py` — the opencode-go model client
- `run.py` — the orchestrator
- `exemplars.py` + `gold_records/` — **25 gold passage records** built from real on-disk material
- `validate.py` — the FoJin-style per-passage validation/tracking + conformance report
- `stack.py` — assembles the **per-work stacked artifact** (13 works), each with `AUDIT.md`

### The API (19 routes, all live + tested)
`/api` · `/api/health` · `/api/stats` · `/api/texts`(+`/:id`,`/translations`) ·
`/api/works`(+`/:id`,`/manuscripts`) · `/api/passages/:id` · `/api/context/passages/:id` ·
`/api/search/passages` · `/api/manuscripts` · `/api/relations/:work_id` · `/api/terms`(+senses,+occurrences) ·
`/api/term-proposals` · `/api/assertions` · `/api/crosswalks` · `/api/concordance` ·
`POST /api/resolve/work`.

The **MCP** (`mcp/index.mjs`) mirrors it: 12 read-only tools (`get_work`,
`get_source_passage`, `get_passage_context`, `get_term_senses`, `get_manuscripts`,
`search_passages`, `concordance`, ...). Connects to Hermes (config in
`~/.hermes/config.yaml` → `tantrakosa` server → `http://localhost:3000`).

### The corpus
- **4,395** segmented verse passages (7 works: kubjikamata 2437, kulasara 711,
  kramasadbhava 563, cidgaganacandrikā 312, timirodghatana 231, maharthamanjari 74,
  tararahasya 67). Referential integrity clean (0 duplicates).
- **1,542** OCHS manuscript witnesses resolved to 18 works.
- **15** accepted term senses (kula, krama, śakti, ...) + 1 proposal.

### The tests
- `tests/api_suite.py` — **74 checks** (contract, referential integrity, epistemic
  invariants, provenance, golden resolver cases, error handling, OpenAPI conformance,
  corpus integrity). `npm test`. All passing.
- `tests/gold/manifest.json` — the tracked passage manifest.
- `examples/` — 7 executable doc examples (`bash examples/run_all.sh`).

---

## 4. How to navigate (the docs map)

Start at **`docs/README.md`** — the documentation home with the full tree and the
7 locked invariants.

| Doc | What it is |
|---|---|
| `docs/STACKED_ARTIFACT_SPEC.md` | the per-work stacked artifact (the what/why) |
| `docs/PIPELINE_SOURCE_MANUAL.md` | the source-code manual (the how) |
| `docs/PEER_REVIEW_REDTEAM.md` | the red-team response (4 changes + 7 invariants) |
| `docs/api/README.md` + `recipes/` + `concepts/` | the API docs (quickstart, 6 recipes, concepts) |
| `docs/NORTHSTAR.md` | the master strategy |
| `docs/nextdev.md` | the 6 formal primitives |
| `docs/endgame1..5year.md` | the vision specs |
| `docs/PROGRESS_2026-08-10.md` + `PIPELINE_PROGRESS_2026-08-10.md` | the progress records |
| `docs/CHECKPOINTS.md` | the validated milestones |

The skills (`skills/`): `translate-passage`, `validate-passage`, `assemble-stack`,
`use-api` — how to interact with the system.

---

## 5. How to run

```bash
cd /root/projects/patala
npm run dev            # the API (localhost:3000)
npm run build          # the verification (must stay clean)
npm test               # the 74-check suite (needs the API up)

# pipeline (no model)
python3 pipeline/exemplars_cli.py --audit
python3 pipeline/validate.py --report
python3 -m pipeline.stack --all

# pipeline (with the model — needs OPENCODE_GO_API_KEY)
python3 pipeline/run.py <source.txt> <work_id> --verse N --out out.json
```

---

## 6. The 7 locked invariants

1. Stable IDs never depend on mutable wording.
2. Work ≠ witness ≠ digital representation ≠ canonical passage.
3. Annotations are independent from the base text and independently addressable.
4. Machine output always enters as a proposal, never authority.
5. Every meaningful scholarly judgment can carry evidence and review history.
6. Translation prose and interpretive decisions have independent version histories.
7. Convenient API bundles are projections over normalized scholarly data, not the
   canonical data model.

---

## 7. What's next (priority order)

1. **The normalize-on-write refactor** (invariant 7). Storage is currently the
   per-passage blob (`stages` dict); split into independent addressable annotations
   (translation / lexical decision / grammar / review / evidence) so decisions have
   independent version histories and can be reused. This is the biggest data-model step.
2. **Wire the pipeline → API/MCP** — serve the validated pipeline records through
   `/api/passages` so the stacked artifact feeds the site.
3. **Anchor-loading** at R1/R2 (the anchor-as-referee rule from the flow spec).
4. **Term-proposal promotion** from pipeline records → `terms.json`.
5. **Alias mapping** for flat-filename ↔ canonical-id (e.g. `kubjika` → `kubjikamata`).
6. **Run one full work** through the pipeline to `07_c1.md`, then wire C1 → essays/videos.

## 8. Honest caveats

- **Not deployed** — the API runs locally only (Cloudflare token issue). `npm run build` is the check.
- The **dev server caches the passage corpus** at first load; restart it after adding passages.
- **Large generated data is gitignored**: `data/manuscripts.json` (5.5MB) and
  `data/corpus/passages/kubjikamata.jsonl` (1.5MB). Regenerate via `scripts/convert-ochs.py`
  and `scripts/segment-t1.mjs`.
- The **MCP model calls are slow** (~60s/turn on deepseek-v4-flash) — fine for one
  verse, slow for a whole chapter. Batching generation up to T3.1 is planned.
- `globals.css` isn't imported in `layout.tsx` (site skin) — cosmetic, known.

# Pāṭala — Process Notes & Current Progress

*2026-08-10. How we work, what's built, where we are, and what's next. The companion to `CHECKPOINTS.md` (the validated milestones) and `DEV_PLAN.md` (the plan).*

---

## The way we work (the process)

- **Build → expose in the API → test → checkpoint.** Every milestone is a target that is *functioning, validated, and integrated into the API*. Nothing is "done" until the API can serve it.
- **The API/MCP is the product.** The site is a render of the API; the MCP is a scholarly evidence engine. "No endpoint, no feature" — anything we build becomes a route + an MCP tool, or it isn't built yet.
- **The API/MCP is loose, not rigid.** It grows as we build useful things, not a frozen pre-spec. Don't overengineer.
- **Bibliography first; corpus manifest before translation tools; the contract before the content.** Provenance is non-negotiable: every record carries a tier / statusChecked / custodian.
- **Resolve, don't duplicate.** We don't own every leaf (manuscripts, archives, texts); we connect them, preserving each source's provenance and custodianship (OCHS, GRETIL, Muktabodha...).
- **The model is the translator; the MCP is the evidence.** The contract (`TRANSLATION_SKILL.md` → `STYLE_GUIDE` / `EVIDENCE_POLICY` / `TRANSLATION_SCHEMA` / `REVIEW_PROTOCOL`) defines how to translate; the MCP supplies evidence.

---

## What's built (validated)

### The stack
```
docs/              19+ specs, endgames (1–5), policies, handovers
data/atlas/        bibliography schema + 69 works (11 audited Trika + 58 school seed)
data/corpus/       works registry · relations · passage loader · manuscripts
data/corpus/passages/  4,016 verse passages (5 works)
data/manuscripts.json   1,542 OCHS manuscript witness records
data/terms.json    accepted term ledger (15 lemmas) · term_proposals.jsonl
app/api/           9 endpoints
mcp/index.mjs      MCP server, 9 tools
scripts/           segmenters (T1 markdown, Kramasadbhāva), OCHS converter
```

### The 9 API endpoints
`/api/texts` (+ `/:id`, `/:id/translations`) · `/api/works` (+ `/:id`, `/:id/manuscripts`) · `/api/relations/:work_id` · `/api/passages/:id` · `/api/search/passages` · `/api/manuscripts`

### The 9 MCP tools
`get_work` · `get_source_passage` · `search_passages` · `get_related_works` · `get_term_senses` · `search_surface_occurrences` · `get_working_translations` · `get_manuscripts` · `get_existing_translations`

### The integrated object (the payoff)
A single `/api/works/:id` (+ sub-routes) now returns: **manuscript witnesses (OCHS) + editions + translation status + our working translations + passages + relations + term senses + rights** — the object the positioning doc says nobody provides.

### The contract (source of truth, separated)
`TRANSLATION_SKILL.md` (compiled instruction + 8 core rules) → `STYLE_GUIDE.md` (voice) / `EVIDENCE_POLICY.md` (reasoning) / `TRANSLATION_SCHEMA.md` (data shape) / `REVIEW_PROTOCOL.md` (workflow). The T0→T3.1 pipeline, typed flags, per-dimension assessment, decision ids, version lineage, term proposals (never auto-accepted).

---

## Checkpoints (validated milestones)

| # | Milestone | Status |
|---|---|---|
| 1 | AI-readable bibliography served by the API | ✅ |
| 2 | Full-depth bibliography for all schools (69 works) | ✅ |
| 3 | Corpus manifest: works registry + relations + passage layer | ✅ |
| 4 | Translation contract + MCP v1 + proof chapter | ✅ |
| 5 | Our own T1 corpus ingested (4,016 passages) + working-translation API | ✅ |
| 6 | OCHS manuscript witnesses ingested & resolved (1,542 records, 18 works) | ✅ |

Full detail in `CHECKPOINTS.md`.

---

## Known gaps / honest caveats

- **The MCP has never been wired into a real client session** to run a full translation end-to-end. The tools work (validated via stdio test), the contract exists, but no model has yet translated a passage through the loop with the skill injected.
- **Passage corpus = 5 works.** Many translated T2/T3s and several untranslated sources (Devīpañcaśataka, Kramastotra, Mahānayaprakāśa) are not yet segmented.
- **58 seed records are `verified:false`** (full-depth shape, not gold-audited).
- **OCHS images are not tagged/bulk-downloadable** → link out later (IIIF), don't ingest.
- **Terms.json is hand-authored**; the translation-driven proposal loop exists but hasn't run at scale.

---

## Next steps (candidates, priority order)

1. **Run the closed-loop translation** — wire hermes/opencode to the patala MCP and translate Kramasadbhāva paṭala 1 with the skill injected. The milestone that proves the MCP produces a full translation; reveals where model/API/schema fail.
2. **Corpus density done smartly** — segment the untranslated sources (Devīpañcaśataka, Kramastotra, Mahānayaprakāśa) and/or the T2/T3s.
3. **`/api/occurrences`** — term co-occurrence in context (cheap over the 4k-passage corpus).
4. **Rights/licensing doc + API surface** — open-to-humanity / commercial-to-machines (endgame4/5).

---

## Process reminders

- Run `npm run build` as the verification check; smoke-test new endpoints live.
- MCP: keep it a thin read-only evidence layer; the model stays the translator.
- Data is king; components/routes are dumb renderers of the API.
- Preserve provenance and custodianship on every external source.
- Don't overengineer; each checkpoint should be a small, validated step.

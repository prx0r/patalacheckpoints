# Pāṭala Documentation — Home

*2026-08-10. The entry point to all Pāṭala documentation: the pipeline, the API,
the corpus, the stacked artifact, and the skills. Everything is machine-first:
the API is the product, the MCP is the agent layer, the pipeline produces the
content, and the site renders it.*

## The system, in one view

```
 RAW SANSKRIT                    THE PIPELINE                     THE HUB
 (sanskritree)                   (patala/pipeline)                (patala app/api)
                                                                      │
 sources/ ──► T1 → R1 → T2 → R2 ──► T3 → T3.1 → C1 ──► passages ──► /api/passages
 anchors/     (working  (review)  (alt)   (synthesis)  (reader)  (commentary) │
 dossiers/     translation)                                  AUDIT.md        ├─ /api/works
                                                                             ├─ /api/terms
 flat T1s ──► stacked artifact (_stack/{work}) ──► validation (validate.py) ──► /api/concordance
                                                                             └─ MCP (12 tools)
```

---

## The documentation tree

### The pipeline (translation)
- [`STACKED_ARTIFACT_SPEC.md`](STACKED_ARTIFACT_SPEC.md) — the per-work stacked artifact (the what/why).
- [`PIPELINE_SOURCE_MANUAL.md`](PIPELINE_SOURCE_MANUAL.md) — the source-code manual (the how).
- [`PEER_REVIEW_REDTEAM.md`](PEER_REVIEW_REDTEAM.md) — the red-team response (the 4 changes + 7 invariants).
- [`TRANSLATION_SKILL.md`](TRANSLATION_SKILL.md) · [`STYLE_GUIDE.md`](STYLE_GUIDE.md) · [`EVIDENCE_POLICY.md`](EVIDENCE_POLICY.md) · [`TRANSLATION_SCHEMA.md`](TRANSLATION_SCHEMA.md) · [`REVIEW_PROTOCOL.md`](REVIEW_PROTOCOL.md) — the house contract.
- [`TRANSLATION_PROTOCOL.md`](TRANSLATION_PROTOCOL.md) · [`TRANSLATION_SKILL_SPEC.md`](TRANSLATION_SKILL_SPEC.md) — the fuller vision + buildable slice.

### The API
- [`api/README.md`](api/README.md) — 5-minute quickstart + endpoint index.
- [`api/recipes/`](api/recipes/) — 6 research recipes.
- [`api/concepts/`](api/concepts/) — the epistemic model, work-vs-witness-passage, assertions/proposals, rights.
- [`api/mcp.md`](api/mcp.md) — the MCP setup + tool mapping.
- [`openapi.yaml`](openapi.yaml) — the executable contract.

### The data model (the durable foundation)
- [`SCHOLARLY_GRAPH.md`](SCHOLARLY_GRAPH.md) — the canonical object/annotation model (Work/Witness/Passage/SourceSpan/Person/Term/Sense/Resource + assertions). The schema that must survive years.

### The corpus & status
- [`PROGRESS_2026-08-10.md`](PROGRESS_2026-08-10.md) — the API/hub progress.
- [`PIPELINE_PROGRESS_2026-08-10.md`](PIPELINE_PROGRESS_2026-08-10.md) — the pipeline/stack progress.
- [`CHECKPOINTS.md`](CHECKPOINTS.md) · [`PROCESS_NOTES.md`](PROCESS_NOTES.md) · [`DEV_PLAN.md`](DEV_PLAN.md) — the milestones/plan.
- [`CHANGELOG.md`](CHANGELOG.md) — API / data / scholarly changes.

### The strategy
- [`NORTHSTAR.md`](NORTHSTAR.md) · [`nextdev.md`](nextdev.md) · [`endgame1..5year.md`](endgame2.md) — the vision.
- [`../PROCESS_NOTES.md`](../PROCESS_NOTES.md) · [`../HANDOVER.md`](../HANDOVER.md) — current state + handover.

### The strategy — corpus-side (in `sanskritree/corpus/targets/`)
These are the authoritative strategic/analytic docs (they live in the source repo):
- [`canonical_reference_map.md`](../../sanskritree/corpus/targets/canonical_reference_map.md) — the historical map + glossary dossiers (the atlas source of truth)
- [`markguidance.md`](../../sanskritree/corpus/targets/markguidance.md) — the Recognition Enquiry (Pratyabhijñā)
- [`leapfrog_map.md`](../../sanskritree/corpus/targets/leapfrog_map.md) + [`leapfrog_guide.md`](../../sanskritree/corpus/targets/leapfrog_guide.md) — the corpus-ladder strategy
- [`translation_flow_spec.md`](../../sanskritree/corpus/targets/translation_flow_spec.md) — the T1→C1 flow spec
- [`targetacquired.md`](../../sanskritree/corpus/targets/targetacquired.md) + [`translation_status_audit.md`](../../sanskritree/corpus/targets/translation_status_audit.md) — the acquisitions + translation-status registers

### The skills (how to interact)
- `skills/translate-work/SKILL.md` (the T1→T3.1 state-machine workflow)
- `skills/write-commentary/SKILL.md` (the C1 capstone)
- `skills/translate-passage/SKILL.md` · `skills/validate-passage/SKILL.md` · `skills/assemble-stack/SKILL.md` · `skills/use-api/SKILL.md`

---

## The invariants (locked)

1. Stable IDs never depend on mutable wording.
2. Work ≠ witness ≠ digital representation ≠ canonical passage.
3. Annotations are independent from the base text and independently addressable.
4. Machine output always enters as a proposal, never authority.
5. Every meaningful scholarly judgment can carry evidence and review history.
6. Translation prose and interpretive decisions have independent version histories.
7. Convenient API bundles are projections over normalized scholarly data, not the
   canonical data model.

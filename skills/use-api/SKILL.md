---
name: use-api
description: "Interact with the Pāṭala API: find works, read passages, pull evidence bundles, trace manuscripts, explore terminology, resolve titles, build an AI research agent. Use when asked to query the corpus through the API or MCP."
version: 1.0.0
author: Pāṭala
metadata:
  hermes:
    tags: [api, mcp, patala, tantra, retrieval, research]
    related_skills: [translate-passage, validate-passage]
    checkpoint: CP2/CP9 (retrieval + the API/MCP surface)
---

# Use the Pāṭala API / MCP

## When to use
- Asked to find a work, read a passage, get evidence, or build a research agent.
- The API is at `http://localhost:3000/api` (run `npm run dev`). The MCP mirrors it.

## The epistemic rules (never break)
1. Resolve identities before assuming aliases.
2. Prefer accepted assertions over proposals.
3. Never report `machine_proposed` as established fact.
4. Preserve uncertainty; don't launder `[X]`.
5. Cite the source/provenance the API returns.
6. Distinguish Pāṭala metadata from upstream source material (OCHS, GRETIL, Muktabodha).
7. Do not infer permissions from public accessibility.

## The common operations
```bash
# find a work
curl "http://localhost:3000/api/works?tradition=Krama"
# read a passage
curl "http://localhost:3000/api/passages/tantra:text:kramasadbhava:1.2"
# the evidence bundle
curl "http://localhost:3000/api/context/passages/tantra:text:kramasadbhava:1.9"
# accepted term senses
curl "http://localhost:3000/api/terms/kula/senses"
# resolve an uncertain title (machine proposal only)
curl -X POST http://localhost:3000/api/resolve/work -H "Content-Type: application/json" -d '{"title":"Amṛteśatantram"}'
```

## Full docs
See `docs/api/README.md` (5-min quickstart), `docs/api/recipes/` (6 recipes), and
`examples/` (7 executable examples — run `bash examples/run_all.sh`).

## Invariants
- The resolver returns `machine_proposed`, never `accepted`.
- Substring search is honest (`lemmatized: false`).
- Every response carries provenance.

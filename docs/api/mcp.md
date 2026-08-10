# MCP — setup & tool mapping

The MCP server is the **agent convenience layer** over the same API. It mirrors the HTTP routes one-to-one — same operation, different transport. This is deliberate:

> **API = protocol-neutral data layer. MCP = agent convenience layer.**

## Setup

```bash
# the MCP server reads the live API (default http://localhost:3000)
cd /root/projects/patala/mcp
npm install
# run it as a stdio MCP server (connect via ChatGPT / Claude / opencode / hermes)
node index.mjs
```

Env:
- `TANTRA_API_BASE` — default `http://localhost:3000` (the Next dev server must be running)
- `TANTRA_CORPUS` — default `/mnt/HC_Volume_106427611/sanskritree/translations` (our T1/T2/T3 files)
- `TANTRA_CORPUS_ROOT` — default `/mnt/HC_Volume_106427611/sanskritree` (for the concordance)

Hermes is already configured: `~/.hermes/config.yaml` has a `tantrakosa` MCP server pointing at `patala/mcp/index.mjs` + `TANTRA_API_BASE: http://localhost:3000`. Verify with `hermes mcp test tantrakosa`.

## Tool mapping (12 tools = the API surface)

| MCP tool | HTTP equivalent | Purpose |
|---|---|---|
| `get_work` | `GET /api/works/{id}` | work metadata + status |
| `get_source_passage` | `GET /api/passages/{id}` | the Sanskrit of one verse |
| `get_passage_context` | `GET /api/context/passages/{id}` | the evidence bundle |
| `search_passages` | `GET /api/search/passages` | substring search |
| `get_related_works` | `GET /api/relations/{work_id}` | typed edges for ranking |
| `get_term_senses` | `GET /api/terms/{lemma}/senses` | accepted senses |
| `find_term_occurrences` | `GET /api/terms/{lemma}/occurrences` | surface occurrences (substring) |
| `get_term_history` | `GET /api/terms/{lemma}/history` | the diachronic sense-trajectory |
| `search_surface_occurrences` | `GET /api/search/passages` | substring, honest about method |
| `get_working_translations` | `GET /api/texts/{id}/translations` | our T1s (provisional) |
| `get_manuscripts` | `GET /api/manuscripts` | OCHS witnesses |
| `get_existing_translations` | reads `TANTRA_CORPUS` files | our T1/T2/T3 files on disk |
| `concordance` | `GET /api/concordance` | raw-corpus tracking (~500 texts) |

## Agent usage principles

The MCP returns **evidence, not a magic answer**. The model stays the translator; the MCP is the scholarly evidence engine. Same rules as the [AI research agent](recipes/ai-research-agent.md):

- `search_surface_occurrences` / `find_term_occurrences` are **substring**, `lemmatized: false` — do not treat hits as lemma evidence.
- `get_term_senses` returns **accepted** senses; proposals live separately and are never auto-accepted.
- `get_working_translations` / `get_existing_translations` are provisional, for calibration — never copy verbatim.
- Every result should be cited back to its work/passage/edition with the provenance the API returned.

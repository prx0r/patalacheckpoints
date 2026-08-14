# THE INTERFACES INDEX — everything an agent can actually call

*2026-08-14. The catalog of Pāṭala's **real, callable interfaces** — the Hermes skills, the HTTP API
routes, and the MCP tools an agent (or human) can invoke. This is the "what can I actually call?"
reference — the executable surface of Pāṭala, complementing `DATA-ASSETS-INDEX.md` (the data) and
`GOLD-EVIDENCE-INDEX.md` (the verified results).*

> **The principle:** the architecture docs describe machinery and vision. THIS is the live interface
> surface — what a caller can invoke right now.

---

## 1. THE HERMES SKILL PACK — `skills/` (19 skills, the procedural layer)

The canonical source of truth for the Hermes skills (synced 1:1 to `~/.hermes/profiles/patala/skills/`).

**Top-level skills (9):**
| Skill | What it does |
|---|---|
| `translate-passage` | the full T1→R1→T2→R2→T3→T3.1→C1 passage flow |
| `translate-work` | a whole work's translation |
| `patala-translate` | the autonomous A3 translation-agent loop (ledger→context→batch→validate→stamp→commit) |
| `raw-l0` | the RAW-L0 source floor |
| `assemble-stack` | assembling the layered stack |
| `validate-passage` | passage validation |
| `write-commentary` | C1 commentary generation |
| `use-api` | API/MCP interaction (curl against `/api`) |
| `push-text` | pushing text downstream |

**The nested autonomous-layer bundle (`autonomous-layer/patala-autonomous-layer-skills/skills/`, 10):**
| Skill | Layer |
|---|---|
| `patala-l0` · `patala-l1` · `patala-l2` · `patala-l200` · `patala-c1` · `patala-theme` · `patala-essay` · `patala-education` | the per-layer autonomous skills |
| `patala-autonomy-controller` · `patala-layer-auditor` | the controller + auditor |

---

## 2. THE HTTP API — `app/api/` (43 real routes)

**Read / resolve:**
`/api/resolve` · `/api/resolve/work` · `/api/context/passages/{id}` · `/api/passages/{id}` ·
`/api/passages/{id}/translation` · `/api/search/passages` · `/api/works` · `/api/works/{id}` ·
`/api/works/{id}/manuscripts` · `/api/texts` · `/api/texts/{id}` · `/api/texts/{id}/translations` ·
`/api/texts/kramasadbhava/decisions` · `/api/spines` · `/api/crosswalks`

**Terms / lexicon:**
`/api/terms` · `/api/terms/{lemma}/senses` · `/api/terms/{lemma}/occurrences` · `/api/terms/{lemma}/history` ·
`/api/term-proposals`

**Verify / review:**
`/api/verify/claim-structure` · `/api/verify/counterevidence` · `/api/verify/quote` ·
`/api/verify/trace-dependency` · `/api/assertions` · `/api/decisions/{id}`

**Corpus / factory:**
`/api/corpus/state` · `/api/factory/status` · `/api/factory/quality` · `/api/hub` · `/api/themes` ·
`/api/education` · `/api/manuscripts` · `/api/relations/{work_id}` · `/api/concordance`

**Discovery / product:**
`/api/analyst` · `/api/journey` · `/api/recommend` · `/api/history/timeline` · `/api/resources` ·
`/api/stats` · `/api/health`

---

## 3. THE MCP SERVER — `mcp/index.mjs` (the agent tool surface)

The MCP server exposes the HTTP API + review-engine tools as native agent tool calls. It covers the
corpus (resolve, verify, themes, recommend, terms) + the review engine. See `docs/api/mcp.md`.

---

## 4. THE RUNNABLE EXAMPLES — `examples/` (the "executable truth")

`01-find-work` · `02-resolve-title` · `03-read-passage` · `04-passage-context` · `05-manuscript-witnesses` ·
`06-term-ledger` · `07-agent-research-flow` + `run_all.sh` (the harness that runs all 7 against the live
API). These are the documented, runnable proof the API works (`docs/api/README.md` calls them
"executable truth").

---

## 5. HOW AN AGENT USES THIS

```text
"what can I actually call?"  →  this index
  → the Hermes skills (19)      →  the procedural layer (translate/validate/commentate)
  → the API routes (43)         →  the HTTP surface (resolve/verify/terms/corpus)
  → the MCP tools               →  the agent tool surface
  → the examples (7)            →  the runnable proof
```

**The anti-theatre note:** unlike the DESIGN layers (06, 09, 11), these interfaces are REAL and callable
right now. Run `examples/run_all.sh` to verify the API is up; read a `SKILL.md` to see the procedural
doctrine; call `/api/health` to confirm.

---

*This is the interfaces index. It completes the "what actually exists" trilogy:
`GOLD-EVIDENCE-INDEX.md` (results) · `DATA-ASSETS-INDEX.md` (data) · `INTERFACES-INDEX.md` (callable surface).*

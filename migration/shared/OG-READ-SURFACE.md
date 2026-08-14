# THE OG READ SURFACE — useful docs + runnable examples (the "what can I actually call?" reference)

*2026-08-14 · status: REFERENCE · the OG Next.js site, MCP server, API routes, and runnable examples are
genuinely USEFUL — they're the "executable truth" of Pāṭala's read surface. Even though they read static
`@/data` today (see `BUILD-SITE-LIVE-DATA.md` for the live-wiring), they are working, documented examples
of how the read plane works. This is the reference for what exists to call/consume.*

---

## THE REAL, CALLABLE SURFACE (verified)

| Surface | Count | What it is | Where |
|---|---|---|---|
| **Hermes skills** | 19 | the procedural layer (translate, validate, assemble, commentate) | `skills/` (synced to `~/.hermes/profiles/patala/skills/`) |
| **API routes** | 43 | the HTTP surface (works, texts, passages, resolve, search, verify, themes, education, timeline, terms) | `app/api/*/route.ts` |
| **MCP tools** | 29 | the agent-callable surface (get_work, resolve_ref, search_passages, verify_*, patala_* review tools) | `mcp/index.mjs` |
| **Runnable examples** | 7 | the "executable truth" — real flows that curl the API | `examples/` |

## THE 7 RUNNABLE EXAMPLES (the executable truth)
| Example | What it demonstrates |
|---|---|
| `01-find-work.py` | find a work |
| `02-resolve-title.py` | resolve a title |
| `03-read-passage.py` | read a passage |
| `04-passage-context.py` | passage context |
| `05-manuscript-witnesses.py` | manuscript witnesses |
| `06-term-ledger.py` | the term ledger |
| `07-agent-research-flow.py` | the agent research flow |
| `run_all.sh` | curl all the API endpoints (the smoke test) |

## THE "OTHER STUFF" (the timeline + lemma — real, curated)
- **Timeline**: `app/api/history/timeline/route.ts` → `data/atlas/historyTimeline.json` (23 schools, the
  Śiva-before-Abhinava chronology)
- **Lemma-through-time**: `app/api/terms/[lemma]/history/route.ts` → the diachronic sense-trajectory
  (curated, reviewable, addressable — NOT mechanical)
- **The MCP tools**: `get_history_timeline`, `get_term_senses`, `get_term_history`, `concordance`

## THE DOCUMENTED SURFACE (the "what can I actually call?" catalog)
- **`docs/process/INTERFACES-INDEX.md`** — THE canonical catalog of every callable interface (skills,
  API routes, MCP tools, examples). Read this to know what's callable.
- **`docs/process/05-app-api-sites.md`** — the read surfaces design (one graph, disposable projections).
- **`docs/process/DATA-ASSETS-INDEX.md`** — the data the surfaces serve.

---

## WHAT THIS MEANS (the useful framing)

The OG site + MCP + examples are **not dead weight** — they're:
1. **Working examples** of how the read plane is supposed to work (the executable truth).
2. **A documented surface** (INTERFACES-INDEX) the other agent can call to test/consume.
3. **The read-surface reference** for the live-wiring build (`BUILD-SITE-LIVE-DATA.md`).

When we wire them to the live factory (the four-truths fix), these examples become the **tests** — run
`examples/run_all.sh` against the live data to prove a new translation reaches the site.

## THE TEST (prove the surface is real)

```bash
# the examples are runnable (start the API, then run them)
cd /root/projects/patala/examples
./run_all.sh http://localhost:3000   # the smoke test of the API surface
# the INTERFACES-INDEX documents everything
grep -n "43\|29\|19\|7" docs/process/INTERFACES-INDEX.md | head
```

**Pass when:** a new agent reads INTERFACES-INDEX to know what's callable, runs the examples to see the
surface work, and (after the live-wiring) uses them as the tests that prove the factory → site connection.

# USING PĀṬALA — the scholar's guide

*2026-08-15. How a scholar actually uses Pāṭala. Read this, then `./start.sh` to open it. This is the
human-facing guide: how to read texts, find cruxes, review scholarship, and attest. Everything below is
real and runnable.*

---

## 0. Open Pāṭala (one command)

```bash
cd /root/patalacheckpoints
./start.sh          # opens the scholar-facing app at http://localhost:3000
./start.sh status   # confirm it's up
```

Once up, open `http://localhost:3000` in a browser. You'll see the Tantra Hub — works, concepts,
bibliography, history, and (new) the **Review** screen.

---

## 1. What a scholar can do

### Read the corpus
- `http://localhost:3000/` — the hub (69 works).
- `http://localhost:3000/texts/{work}` — one work's record (editions, translations, manuscripts).
- `http://localhost:3000/read/{work}/{locator}` — read a passage with its translation + commentary.
- `http://localhost:3000/bibliography` — the 69-work bibliography.

### Find what's interesting (the tension finder)
```bash
# the vision's /find-interesting-tension — where interpretations diverge (where papers come from)
cd /root/patalacheckpoints
PYTHONPATH=pipeline python3 pipeline/products/tension_finder/engine.py 0 10
```
Returns contradictions, cruxes, doctrinal shifts, live-issues — 67 tensions across 5 kinds.

### Find the crux between two positions
```bash
PYTHONPATH=pipeline python3 pipeline/products/crux/engine.py \
  ARG:pt:passage:ipvv:chunkA-svatyandya.md ARG:pt:passage:ipvv:chunkB-eligibility-gita.md
```

### Review an object (the human-authority surface)
1. Open `http://localhost:3000/review`.
2. Paste an object id (e.g. `V2-L-sastho-vimarsa-smrti-apohana:c1`).
3. See its epistemic state + downstream impact.
4. Choose a decision (`ACCEPT / ACCEPT_WITH_QUALIFICATION / DISPUTE / PROPOSE_ALTERNATIVE / ABSTAIN / OUT_OF_SCOPE`) and record a rationale.

Or via the API:
```bash
curl "http://localhost:3000/api/scholar?verb=object&target_ref=V2-L-sastho-vimarsa-smrti-apohana:c1"
curl "http://localhost:3000/api/scholar?verb=impact&target_ref=V2-L-sastho-vimarsa-smrti-apohana:c1"
```

### Check a translation's proof (the moat)
```bash
PYTHONPATH=pipeline python3 pipeline/products/translation_proof/engine.py \
  "pt:passage:ipvv:chunkD-memory-pramana.md"
```
Returns a 10-dimension audit vector + a publication gate (BLOCKED on any failing dimension — no fake "94%").

### Track your contributions (the scholar profile)
```bash
PYTHONPATH=pipeline python3 pipeline/products/scholar_profile/engine.py leaderboard
```

---

## 2. The honest "what's the epistemic state"

Every object carries an **epistemic ceiling** + a 4-axis authority vector
(`generation · evidence · review · publication`). The ladder:
`MACHINE_PROPOSED → ENGINEERING_VALIDATED → SCHOLARLY_CORROBORATED → INDEPENDENT_REVIEWED → ADJUDICATED`.

- A **machine** may propose; only an **authorized scholar** promotes.
- `authority(projection) ≤ authority(parent)` — a review never raises an object above its evidence.
- **Banned words**: you'll never see "PROVED/TRUTH/CORRECT" — Pāṭala says "SUPPORTED BY / PASSED CHECK X /
  MACHINE-PROPOSED / REVIEWED BY."

---

## 3. The AI interface

Pāṭala exposes **55 MCP tools** (works, passages, crux, review, attestation, terminology...) that a
scholar's AI assistant can call. To register it with your AI:

```bash
hermes mcp add patala --command node --args "/root/patalacheckpoints/mcp/index.mjs"
# (answer Y to enable the 55 tools)
```

Once registered, your AI can ask "find the crux between these two passages" or "what needs review first"
and it will call the real engine.

---

## 4. What's honest vs. what's the boundary

- **Real + usable now:** the corpus (69 works, 2189 passages), the tension finder, crux, review screen,
  translation proof, terminology/timeline, the scholar API.
- **Needs a GPU box (adopted, not built):** OCR (kraken/eScriptorium). Manuscript routing + quality
  labelling work on CPU; the actual text extraction runs on a GPU.
- **Needs the other machine's data:** the full 254-work corpus + some golds live on the other repo.

---

*This is the scholar's guide. Start with `./start.sh`, open the hub, find a crux, review an object. The
engine is real; the last mile (launch + docs + review screen) is now in place.*

---

## 5. Per-product: human + agent usage

Every product is usable by a **human** (via a page or CLI) AND by an **agent** (via Hermes MCP,
`mcp__patala__<tool>`). This is the full matrix.

### Explore products (human: /tools pages · agent: MCP)

| Product | Human | Agent (Hermes MCP) |
|---|---|---|
| **tension_finder** | `/tools/tensions` | `patala_tension_finder` |
| **crux** | `/tools/crux` | `patala_crux` |
| **terminology** | `/tools/terminology` | `patala_terminology` |
| **timeline** | `/tools/timeline` | `patala_timeline` |
| **passage** | `/read/{work}/{locator}` | `patala_passage` |
| **translation_proof** | `translation_proof/engine.py` | `patala_translation_proof` |
| **research_packet** | `research_packet/engine.py "question"` | `patala_research_packet` |
| **evidence_independence** | `evidence_independence/engine.py live` | `patala_evidence` |

### Scholar workflow products (human: /review, /queue, /scholars · agent: MCP)

| Product | Human | Agent (Hermes MCP) |
|---|---|---|
| **review** | `/review` | `patala_scholar_object` / `patala_scholar_panel` |
| **review_queue** | `/queue` | `patala_review_queue` |
| **scholar_profile** | `/scholars` | `patala_scholar_profile` |
| **scholar_identity** | (register via CLI) | `patala_scholar_identity` |
| **review_policy** | `review_policy/engine.py` | `patala_review_policy` |
| **scholar_publication** | (published JSON-LD) | `patala_scholar_publication` |
| **scholar_vertical** | (full run via CLI) | `patala_scholar_vertical` |
| **passage_workbench** | (record disagreement via CLI) | `patala_passage_workbench` |

### Manuscript products (human: CLI · agent: MCP)

| Product | Human | Agent (Hermes MCP) |
|---|---|---|
| **manuscript_routing** | `manuscript_routing/engine.py demo` | `patala_manuscript_routing` |
| **manuscript_ingest** | `manuscript_ingest/engine.py demo` | `patala_manuscript_ingest` |

### Eval (human: CLI · agent: MCP)

| Product | Human | Agent (Hermes MCP) |
|---|---|---|
| **benchmark** | `benchmark/engine.py` | `patala_benchmark` |

### The Hermes reduction layer (agents gate + commit product derivations)

```bash
# a Hermes worker (or a human) gates a product's derivation and commits it to the canonical store
PYTHONPATH=pipeline python3 pipeline/product_reducer.py reduce claim      # derive + validate 49 claims
PYTHONPATH=pipeline python3 pipeline/product_reducer.py commit claim '<proposal-json>'  # gate + commit
```
Agent-side: `mcp__patala__patala_reduce` (verb=reduce/validate/commit, product=claim/crux/evidence/tension).

---

*Every product is now usable by a human (page or CLI) and by an agent (Hermes MCP). Start with
`./start.sh`, open the hub, and ask your AI to "find the crux" — it will call the real engine.*

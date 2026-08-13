# Pāṭala API — Documentation

> **Open research API for tantric textual data, provenance and evidence.**

Pāṭala is the **authority, provenance, relationship, expert-validation and workflow layer** for tantric textual heritage. It sits *between* manuscript repositories (OCHS, Muktabodha, GRETIL) and the people/AI systems that use them. The API exposes what exists, where it came from, what has been translated, how texts relate, and what is verified — so agents and scholars retrieve *evidence*, not hallucinated guesses.

**Machine-first.** The API is the product; the MCP is an agent convenience layer over it; the website is a render of it.

---

## The epistemic model (read first)

Four layers keep Pāṭala honest:

```
SOURCE      what upstream material says
PROPOSAL    what a machine/human suggests (never auto-accepted)
ASSERTION   a structured, reviewable claim
REVIEW      a recorded judgment (who / what / decision / why / when)
ACCEPTED    Pāṭala's current editorial position
```

**Rules that never break:**

```
Proposal ≠ assertion.
Assertion ≠ consensus.
Accepted ≠ certain.
Machine score ≠ scholarly confidence.
```

The resolver returns `status: "machine_proposed"` — **never** `accepted`. Only a human review event promotes a proposal. Term proposals (`/api/term-proposals`) never appear in the accepted ledger (`/api/terms`).

Public phrasing is deliberately careful: **"No complete English translation located"**, never "Untranslated."

---

## 5-minute quickstart

The API is at `http://localhost:3000/api`. It returns JSON. No auth key needed.

### 1. Find a work

```bash
curl http://localhost:3000/api/works?tradition=Krama
```

### 2. Read a passage

```bash
curl http://localhost:3000/api/passages/tantra:text:kramasadbhava:1.2
```

### 3. Get its research context (the evidence bundle)

```bash
curl http://localhost:3000/api/context/passages/tantra:text:kramasadbhava:1.9
```

That's the whole philosophy: **find a thing → read it → pull its evidence.** Everything else is a refinement of these three.

---

## Endpoint index

| Endpoint | Purpose |
|---|---|
| `GET /api` | Discoverability: endpoint groups + principles |
| `GET /api/health` | Operational status + dataset version |
| `GET /api/stats` | Corpus credibility signals (raw counts) |
| `GET /api/corpus/state` | **The translation-state ledger** — per-work source/translation/L0/proof/review state + NEXT_VALID_ACTION + agent3 eligibility (the corpus control plane; Agent 2's core object) |
| `GET /api/factory/quality` | **The live translation-ready signal** — per-work CLEAN / READY / PRIORITY fingerprint (on-disk Sanskrit usable? in ledger + queue? copyright-aware translation value?). `?work=<id>` for one, no param for all, `?priority=HIGH\|MEDIUM\|LOW` to filter. Powered by `pipeline/source_ready.py` |
| `GET /api/factory/status` | **Factory run state** — per-layer object counts in the canonical registry + the A-H/A-L certificates (how far SOURCE→C1 production has gone) |
| `GET /api/texts` | The bibliography (the "WHAT EXISTS?" spine) |
| `GET /api/resources` | The external-resource federation register (typed + tradition-tagged) |
| `GET /api/texts/{id}` | One full bibliography record |
| `GET /api/texts/{id}/translations` | Our working (T1) translations |
| `GET /api/works` | The work registry |
| `GET /api/works/{id}` | One work's metadata |
| `GET /api/works/{id}/manuscripts` | A work's OCHS manuscript witnesses |
| `GET /api/passages/{id}` | One verse-anchored passage |
| `GET /api/context/passages/{id}` | The deterministic evidence bundle |
| `GET /api/search/passages` | Substring search over the corpus |
| `GET /api/manuscripts` | The OCHS manuscript layer |
| `GET /api/relations/{work_id}` | Typed/confidence/evidence edges |
| `GET /api/terms` | The accepted term ledger |
| `GET /api/terms/{lemma}/senses` | Accepted senses for a lemma |
| `GET /api/terms/{lemma}/occurrences` | Surface occurrences (substring) |
| `GET /api/term-proposals` | Machine/human proposals |
| `GET /api/assertions` | Contested claims as objects |
| `GET /api/crosswalks` | Our↔external object mappings |
| `GET /api/concordance` | Raw-corpus word tracking (~500 texts) |
| `POST /api/resolve/work` | Candidate work identity (machine proposal) |

**Full machine-readable contract:** `docs/openapi.yaml` (OpenAPI 3.0.3).

---

## The translation-ready signal (`/api/factory/quality`)

The factory computes a granular per-work quality fingerprint — the same one used to route texts
through the pipeline. Every work is scored on three axes:

| Field | Meaning |
|---|---|
| `clean` | Is the on-disk Sanskrit actually usable? (IAST/Devanagari density, size; not an OCR-mess or English-only file) |
| `ready` | Is it registered? (in the ledger as RAW_SANSKRIT **and** has committed SOURCE objects the factory can process) |
| `priority` | Copyright-aware translation value — **HIGH** (no English, or English under copyright → translate your own to publish) / **MEDIUM** (public-domain English exists) / **LOW** (unclear — verify) |
| `english` | The atlas translation coverage (`none` / `partial` / `complete`) |
| `next_action` | The ledger's next valid transition (e.g. `BUILD_L0_SOURCE_MODE`) |

```bash
# one work
curl http://localhost:3000/api/factory/quality?work=tantraloka
# everything, highest value first
curl "http://localhost:3000/api/factory/quality?priority=HIGH"
```

The rationale behind `priority`: an existing **copyrighted** English translation (e.g. Dyczkowski's
Tantrāloka) cannot be republished on your site — so a Pāṭala-native translation is the high-value
target, even though "complete English exists." Public-domain English (Keith, Ganguli, Whitney) can be
linked instead, so those are MEDIUM. This is what decides where the factory spends its budget.

---

## Stable identifiers

Every object has a stable, resolvable identity:

```
tantra:text:kramasadbhava
tantra:text:kramasadbhava:1.2      (a passage)
pt:ms:ochs_000_000_002_amrtesatantram
```

Most `{id}` routes accept **either** the bare id (`kramasadbhava`) **or** the full urn (`tantra:text:kramasadbhava`). Passages use `{work}:{chapter}.{verse}`. Never let a URL fragment be the canonical identity.

---

## Guides (research recipes)

- [Find a work](recipes/find-a-work.md)
- [Resolve an uncertain title](recipes/resolve-a-title.md)
- [Read a passage + its evidence bundle](recipes/read-a-passage.md)
- [Trace manuscript witnesses](recipes/manuscript-witnesses.md)
- [Explore terminology](recipes/terminology.md)
- [Build an AI research agent](recipes/ai-research-agent.md)

## Concepts

- [The epistemic model](concepts/epistemic-model.md)
- [Work vs witness vs passage](concepts/work-witness-passage.md)
- [Assertions and proposals](concepts/assertions-proposals.md)
- [Rights](concepts/rights.md)

## MCP

- [MCP setup & tool mapping](mcp.md)

## Executable examples

Each recipe has a runnable example (curl-equivalent Python) under `examples/`. These are **executable truth** — if a documented fixture stops resolving, the example fails.

```bash
bash examples/run_all.sh      # requires the API up (npm run dev)
```

| # | Example | Recipe |
|---|---|---|
| 01 | [`examples/01-find-work`](../../examples/01-find-work) | Find a work |
| 02 | [`examples/02-resolve-title`](../../examples/02-resolve-title) | Resolve an uncertain title |
| 03 | [`examples/03-read-passage`](../../examples/03-read-passage) | Read a passage |
| 04 | [`examples/04-passage-context`](../../examples/04-passage-context) | Evidence bundle |
| 05 | [`examples/05-manuscript-witnesses`](../../examples/05-manuscript-witnesses) | Manuscript witnesses |
| 06 | [`examples/06-term-ledger`](../../examples/06-term-ledger) | Explore terminology |
| 07 | [`examples/07-agent-research-flow`](../../examples/07-agent-research-flow) | AI research agent |

## Versioning

- **API version:** `1.0` (in every response `provenance.api_version`, and `/api/health`).
- **Dataset revision:** `2026-08-10` (in `/api/health.dataset_revision`). Each dataset build is citable: *"Query performed against Pāṭala dataset 2026-08-10."*
- **Changelog:** `docs/CHANGELOG.md` records API + data + scholarly changes separately.

---

## What to note

- **`verified:false`** = metadata has the full schema but hasn't received the gold audit yet (the seed records). It's not "wrong"; it's *not yet audited*.
- **`accepted`** (term sense) = current editorial state, not universal scholarly consensus.
- **`machine_proposed`** = generated by an automated process; not a scholarly assertion.
- **Substring search is honest.** `/api/terms/{lemma}/occurrences` and `/api/search/passages` do *substring* matching, not morphological/lemma retrieval (`lemmatized: false`). Sanskrit inflects — `śakti / śaktiḥ / śaktim` are not interchangeable for a raw concordance.

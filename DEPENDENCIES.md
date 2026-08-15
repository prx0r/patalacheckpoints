# PĀṬALA PRODUCTS — dependencies (everything needed to run the 25 engines)

*2026-08-15. The complete dependency list for the 25 product engines + the MCP server + the UI. A
fresh checkout needs exactly these. All deps verified present on this box.*

---

## 1. Python (system 3.14 — mostly stdlib)

The 25 product engines are **nearly stdlib-only**. Only two external packages:

| Package | Used by | Version (verified) |
|---|---|---|
| **networkx** | `research_packet` (PathRAG flow) | 3.6.1 |
| **cryptography** | `scholar_review` attestation (Ed25519), `scholar_identity` | 46.0.5 |

Install: `pip install networkx cryptography`

> The rest is stdlib: `hashlib, json, re, sys, pathlib, dataclasses, datetime, collections,
> tempfile, subprocess`.

## 2. Node (MCP server)

| Package | Used by | Version |
|---|---|---|
| **@modelcontextprotocol/sdk** | `mcp/index.mjs` (the 61-tool server) | ^1.30.0 |

Install (in `mcp/`): `npm install`

## 3. Internal modules (must ship WITH the products — not pip-installable)

These are Pāṭala's own modules the engines import. They are in the repo, not external.

| Module | Path | Used by |
|---|---|---|
| `review_engine` | `pipeline/review_engine.py` | `scholar_review`, `review_workbench`, `scholar_vertical` |
| `object_registry` | `pipeline/object_registry.py` | `product_reducer` (the Hermes reduction layer) |
| `opencitations` | `source-evidence/production/adapters/opencitations.py` | `evidence_independence` |
| `ipvv` (shared loader) | `pipeline/products/_shared/ipvv.py` | ALL products read real IPVV passages |
| `closed_vocabulary` | `pipeline/products/_shared/closed_vocabulary.py` | `argument`, `claim` |
| `canonical_id` | `pipeline/products/_shared/canonical_id.py` | `research_packet` |

## 4. Data files (the real substrate the products read)

| File | Used by | Present? |
|---|---|---|
| `data/published/ipvv/pt-passage-*.json` (49) | all products (claims, crux, argument...) | ✅ 49 |
| `data/corpus/trajectories.json` | `terminology` | ✅ |
| `data/atlas/historyTimeline.json` | `timeline` | ✅ |
| `data/corpus/registries/*-registry.jsonl` (21) | `evidence_independence`, `product_reducer` | ✅ 21 |
| `data/scholar/{reviews,attestations}.jsonl` | `scholar_profile`, `scholar_publication` | ✅ (empty until used) |

## 5. The gold source (independent ground truth, for `gold_check.py`)

| File | Used by | Where |
|---|---|---|
| `raw-material/c1/*.md`, `raw-material/argmap/*.md` | `gold_check.py` (anti-theatre) | smellycock repo |

## 6. Runtime tools

- **Python 3.14** (`/usr/bin/python3`)
- **Node 20.20.2** (for the MCP server)
- **Hermes** (to call the MCP tools as `mcp__patala__<tool>`) — optional, for the agent interface
- **Next.js** (the UI) — `node_modules` in the patalacheckpoints app (run `npm install`)

---

## Quick verify (run this to confirm deps are ready)

```bash
python3 -c "import networkx, cryptography; print('py deps OK')"
cd mcp && npm ls @modelcontextprotocol/sdk 2>/dev/null
python3 -c "import sys; sys.path.insert(0,'pipeline'); import review_engine, object_registry; print('internal OK')"
```

---

*This is the complete dependency contract. All verified present on this box; a fresh checkout needs
`pip install networkx cryptography` + `npm install` in `mcp/`.*

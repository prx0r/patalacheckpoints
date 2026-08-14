# HANDOVER — THE CURRENT STATE (read this first)

*2026-08-14. The canonical, stable top-level handover for any next agent. It gives the complete current
state: what Pāṭala is, the layer assignment (ACTIVE/ARCHIVED), how to use the existing assets, the
canonical indexes, and the priority list. **This file is the STABLE entry point.** Session-by-session
history is in `handover/sessions/` (timestamped session notes).*

> **The orientation:** Pāṭala = a small epistemic kernel + compiler, made frontier by proof-carrying
> objects, industry-aligned adapters, the Scholar Attestation Vertical, and the Q-moat organism. The real
> proof is the IPVV build + the 5 golds + the certificates. Everything else is active machinery, borrowed
> substrate, or archived history.

---

## 1. THE AGENT SYSTEM (where agent0 is, how it's explained)

- **`AGENTS.md`** — the governing rules (agent stack A0-A7, operating axioms, Hermes). READ FIRST.
- **`handover/AGENTS.yaml`** — the registry (agent0 = template, agent1/2 = live instances).
- **`handover/STATE.yaml` + `flow.py`** — the live checkpoint state machine.
- **`handover/agent0-coordinator/`** — the A0-A8 architecture vision.
- **The key shift:** progress is tracked **PER-LAYER** (`docs_state.py` + `VISION-CHUNKS.json`), not per-agent.

## 2. THE LAYER ASSIGNMENT (ACTIVE / ARCHIVED / how to use)

| Layer | Status | How to use |
|---|---|---|
| 00 Governance | ACTIVE | `AGENTS.md`, the anti-theatre gate |
| 01 Ingestion | ACTIVE | `DATA-ASSETS-INDEX.md`, corpus targets |
| 02 Atlas | ACTIVE/PARTIAL | add CTS + Stencila (`FRONTIER-MAP.md`) |
| 03 Factory | ACTIVE/PARTIAL | SYNTHESIS/ESSAY/EDUCATION = 0, to build |
| 04 Evidence | ACTIVE | `INTERFACES-INDEX.md` + `EVALS-BENCHMARKS-INDEX.md` |
| 05 Research | ACTIVE/PARTIAL | the moat; upper layers to build |
| 06 Commentarial | DESIGN | the paper→packet compiler is the frontier |
| 07 Verification | ACTIVE | `EVALS-BENCHMARKS-INDEX.md` |
| 08 Human Authority | ACTIVE/PARTIAL | the Scholar Attestation Vertical is the priority |
| 09 Organism | DESIGN | Engram substrate identified |
| 10 Surfaces | ACTIVE/PARTIAL | `INTERFACES-INDEX.md` |
| 11 Economics | DESIGN | the partnership docs |
| 12 Live System | ACTIVE/PARTIAL | the 7 pieces to build |

## 3. THE EXISTING TRANSLATION ASSET (how to make it useful)

- **71 RAW-EN works** (patala `downloads/translations/`) = the LIVE factory input → `register_sources.py`
  commits them as SOURCE → they advance through the DAG.
- **141 old-batch T1 + 11 T3 finals** (sibling `sanskritree/` repo) = ARCHIVED format, converted by `import_sanskritree.py`
  (provenance `sanskritree-import`).
- **IPVV gold layers** (63 L200 audits, 63 C1, 63 T1 golds — all in the sibling `sanskritree/translations/_stack/ipvv/`) = the primary scholarly evidence (`IPVV-BUILD.md`).

## 4. THE CANONICAL INDEXES (the "what exists" reference)

| Index | Documents |
|---|---|
| `docs/process/GOLD-EVIDENCE-INDEX.md` | what's proven (gold/certificates/proofs) |
| `docs/process/DATA-ASSETS-INDEX.md` | the real data (targets/registries/bibliography) |
| `docs/process/INTERFACES-INDEX.md` | what's callable (skills/API/MCP/examples) |
| `docs/process/EVALS-BENCHMARKS-INDEX.md` | how it's tested (NAT/golds/review) |
| `docs/process/IPVV-BUILD.md` | the full IPVV build |
| `docs/process/FRONTIER-MAP.md` | every layer's best-version + build path |
| `docs/process/RECONCILIATION.md` + `INDUSTRY-ALIGNMENT.md` | built-vs-borrowed + the standards map |
| `NAVIGATION.md` | resolve anything → layer/impl/docs/run/Hermes |

## 5. WHAT TO CONTINUE (the priority list)

1. **Layer 12 Pieces 1-4** (projection + staleness + MCP verbs) — makes everything non-theatre.
2. **Layer 12 Piece 5 — the Scholar Attestation Vertical** — the frontier differentiator.
3. **Enable SYNTHESIS/ESSAY/EDUCATION** in the factory (currently 0 objects).
4. **Make the 71 RAW-EN works useful** — ensure registered as SOURCE and advancing through the DAG.
5. **Adopt CTS + Stencila** (Layer 02/04) — identity interop + schema-drift fix.
6. **Add `cts_urn`** to passage/work identity.
7. **Design the `TranslationProof` schema** (Layer 03) — the novel translation moat.

## 6. THE HONEST STATE (one screen)

```
REAL + TESTED:  SOURCE→T1→L0→L200, 5 golds, Nyāya gate, certificates, NAT tests, 43 API routes, 19 skills
DATA:           corpus targets, 32k SOURCE objects, 254 works, 71 translated works
DESIGN (not built): Commentarial (06), Organism (09), Economics (11), SYNTHESIS/ESSAY/EDUCATION (0)
ARCHIVED:       the old freestyle pipeline (converted), the ai/ research, devpaths log
SCHEMA DIVERGENCE (flagged, not fixed): ReviewEvent/Authority/Proposition (SCHEMA-AUDIT.json)
```

## 7. THE SESSION ARCHIVE

Session-by-session history is in **`handover/sessions/`** (timestamped session notes). The most recent is
`2026-08-14-two-sided-build-and-reorg.md` (the two-sided build with agentgraph + the doc reorg). Read the
session note for the full rationale; this file is the stable current-state.

---

*This is the stable top-level handover. For the full session history, see `handover/sessions/`. For the
deep "what exists" picture, use the canonical indexes in §4.*

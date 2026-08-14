# HANDOVER — NEXT AGENT START HERE (the complete state, assigned, active/archived, and what to do)

*2026-08-14. The top-level handover for any next agent. It assigns every part of Pāṭala to its LAYER,
marks it ACTIVE or ARCHIVED, explains how it should be USED, and lists the concrete continuation tasks.
Read this first; then use the canonical indexes it links to.*

> **The orientation:** Pāṭala = a small epistemic kernel + compiler, made frontier by proof-carrying
> objects, industry-aligned adapters, the Scholar Attestation Vertical, and the Q-moat organism. The
> real proof is the IPVV build + the 5 golds + the certificates. Everything else is either active
> machinery, borrowed substrate, or archived history.

---

## 0. THE AGENT SYSTEM (where is agent0, and how is it explained now?)

**The agent architecture is `AGENTS.md` §1 (the governing file) + `handover/agent0-coordinator/`:**

| Asset | What it is | Status |
|---|---|---|
| `AGENTS.md` | the governing rules — the agent stack (A0 governance → A1 philosophy · A2 corpus · A3 factory → A4 review · A5 synthesis · A6 projection · A7 scholar network), the operating axioms, Hermes wiring | ACTIVE (read first) |
| `handover/AGENTS.yaml` | the agent registry — **agent0 = the template**, agent1/agent2 = live instances | ACTIVE |
| `handover/STATE.yaml` + `flow.py` | the live agent checkpoint state machine | ACTIVE (update via `flow.py`) |
| `handover/agent0-coordinator/AGENT-ARCHITECTURE-VISION.md` | the mature A0-A8 architecture vision | ACTIVE (the design) |

**How it's explained now:** `AGENTS.md` is the canonical explanation (the stack + the "Pāṭala decides
what matters, Hermes decides how" boundary). The vision→checkpoint map is in `VISION-CHECKPOINT-MAP.md`
(layers, not agents). **The key shift since the early build: progress is tracked PER-LAYER (via
`docs_state.py`), not per-agent** — see `VISION-CHUNKS.json`.

---

## 1. THE LAYER ASSIGNMENT — what's ACTIVE, what's ARCHIVED, how to use it

| Layer | What's real | Status | How to use |
|---|---|---|---|
| **00 Governance** | doctrine, DAG, operating axioms | ACTIVE | read `AGENTS.md`; the anti-theatre gate |
| **01 Ingestion** | SourceAsserter, 8 adapters, R2 Bronze, 71 RAW-EN works | ACTIVE | see `DATA-ASSETS-INDEX.md`; the corpus targets |
| **02 Atlas** | 22-table Postgres, 254 works, resolver, API | ACTIVE/PARTIAL | add CTS + Stencila (see `FRONTIER-MAP.md`) |
| **03 Factory** | SOURCE→C1 real (32k), 71 translated works, L200 proof | ACTIVE/PARTIAL | SYNTHESIS/ESSAY/EDUCATION = 0, to build |
| **04 Evidence** | contracts, 69 tools, eval plane | ACTIVE | see `INTERFACES-INDEX.md` + `EVALS-BENCHMARKS-INDEX.md` |
| **05 Research** | argument/crux/synthesis compilers, 5 golds | ACTIVE/PARTIAL | the moat; upper layers to build |
| **06 Commentarial** | DESIGN only | ARCHIVED-as-design | the paper→packet compiler is the frontier (see `FRONTIER-MAP.md`) |
| **07 Verification** | NAT tests, certificates, eval plane | ACTIVE | see `EVALS-BENCHMARKS-INDEX.md` |
| **08 Human Authority** | ReviewEvent + review_engine | ACTIVE/PARTIAL | the Scholar Attestation Vertical is the priority |
| **09 Organism** | DESIGN only | ARCHIVED-as-design | Engram substrate identified (see `FRONTIER-MAP.md`) |
| **10 Surfaces** | app/ + MCP + 43 API routes | ACTIVE/PARTIAL | see `INTERFACES-INDEX.md` |
| **11 Economics** | strategy only | ARCHIVED-as-design | see the partnership docs |
| **12 Live System** | Tier-1 truth real | ACTIVE/PARTIAL | the 7 pieces to build |

---

## 2. THE EXISTING TRANSLATION ASSET (the big untapped gold)

**The question "how do we make the old translations useful?" — the answer:**

| Asset | Location | Count | Status | How to make useful |
|---|---|---|---|---|
| **RAW-EN works** (the live runner's output) | `data/corpus/downloads/translations/*.jsonl` | **71** | ACTIVE | these ARE in the factory queue — `register_sources.py` commits them as SOURCE → they advance through the DAG |
| **Old-batch T1 files** (the freestyle prose, 8-layer pipeline) | `sanskritree/translations/01_t1_working/` | **141** | ARCHIVED (old format) | **converted** by `import_sanskritree.py` → canonical T1 objects (provenance `sanskritree-import`) |
| **Old-batch T3 finals** | `sanskritree/translations/05_t3_final/` | **11** | ARCHIVED | imported as T3 (the adjudicated view) |
| **Old R1/T2/R2/C1** | `sanskritree/translations/{02_r1,03_t2,04_r2,06_c1}/` | — | ARCHIVED | provenance only — do NOT re-ingest; the modern L0/L200/C1 replaces them |
| **IPVV gold layers** (L200 audits, C1, T1 golds) | `translations/_stack/ipvv/` | 63+ | ACTIVE (GOLD) | see `IPVV-BUILD.md` — the primary-scholarly evidence |

**The rule:** the OLD freestyle pipeline (T1→R1→T2→R2→T3→C1) is **superseded** by the modern layered
stack (SOURCE→T1→L0→L200→C1). The old files are NOT wasted — they're converted to canonical objects by
`import_sanskritree.py` (T1) and used as provenance. The RAW-EN works (71) are the LIVE factory input.

---

## 3. THE CANONICAL INDEXES (the "what exists" reference — all ACTIVE)

| Index | What it documents | Use for |
|---|---|---|
| `docs/process/NAVIGATION.md` | resolve anything → layer/impl/docs/run | the master index |
| `docs/process/GOLD-EVIDENCE-INDEX.md` | what's proven (gold/certificates/proofs) | "what's real" |
| `docs/process/DATA-ASSETS-INDEX.md` | the real data (targets/registries/bibliography) | "what data" |
| `docs/process/INTERFACES-INDEX.md` | what's callable (skills/API/MCP/examples) | "what can I call" |
| `docs/process/EVALS-BENCHMARKS-INDEX.md` | how it's tested (NAT/golds/review) | "how is it tested" |
| `docs/process/IPVV-BUILD.md` | the full IPVV build | the scholarly proof |
| `docs/process/FRONTIER-MAP.md` | every layer's best-version + build path | what to build next |
| `docs/process/RECONCILIATION.md` | built vs borrowed vs agentic | what's ours vs external |

---

## 4. WHAT TO CONTINUE (the next agent's priority list)

1. **Layer 12 Pieces 1-4** (projection + staleness + MCP verbs) — makes everything non-theatre.
2. **Layer 12 Piece 5 — the Scholar Attestation Vertical** — the frontier differentiator.
3. **Enable SYNTHESIS/ESSAY/EDUCATION** in the factory (currently 0 objects) — the declared-but-empty upper layers.
4. **Make the 71 RAW-EN works useful** — ensure they're all registered as SOURCE and advancing through the DAG.
5. **Adopt CTS + Stencila** (Layer 02/04) — identity interop + schema-drift fix.
6. **Add `cts_urn`** to passage/work identity (cheap, high value).
7. **Design the `TranslationProof` schema** (Layer 03) — the novel translation moat.

---

## 5. THE HONEST STATE (one screen)

```
REAL + TESTED:  SOURCE→T1→L0→L200 (IPVV + 71 works), 5 golds, the Nyāya gate, the certificates,
                the NAT tests, the eval plane, 43 API routes, 19 skills, 69 external tools
DATA:           corpus targets (21 RAW-L0 + 100 sivaqueue + 39 leads), 32k SOURCE objects, 254 works
DESIGN (not built): Commentarial (06), Organism (09), Economics (11), SYNTHESIS/ESSAY/EDUCATION (0)
ARCHIVED:       the old freestyle pipeline (converted to canonical), the ai/ research, devpaths log
```

---

*This is the top-level handover. Read the layer-assignment (§1), the translation-asset answer (§2), the
index map (§3), and the priority list (§4). Then go deep via the canonical indexes.*

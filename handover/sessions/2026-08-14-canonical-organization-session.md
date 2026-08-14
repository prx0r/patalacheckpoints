# SESSION NOTE — 2026-08-14 — canonical organization + Hermes integration + the "what exists" documentation

*Timestamped session record. This is the COMPLETE record of what was accomplished this session, so any
future agent can see exactly what changed, what was discovered, and what was fixed. Read the canonical
`HANDOVER.md` (root) for the current state; this is the history + rationale.*

---

## 1. WHAT THIS SESSION ACCOMPLISHED (the arc)

This session transformed Pāṭala from a **messy, fragmented doc + schema landscape** into a **canonical,
machine-verifiable, agent-readable architecture** — and used a real Hermes agent as a probe to verify it.
The arc:

1. **Consolidated 5 redundant map files → 2** (govern = AGENTS.md, navigate = NAVIGATION.md)
2. **Built machine-verifiable manifests** (directory, vision, docs) with runnable validators
3. **Used Hermes as a probe** → found the recurring model-config bug and FIXED it
4. **Documented the "what exists" layer** (gold, data, interfaces, evals) that was under-surfaced
5. **Mapped the whole thing to formal industry standards** and the frontier best-version
6. **Created the top-level handover** + this session archive

---

## 2. THE ORGANIZATION (the canonical structure)

### 2.1 The map consolidation (5 → 2 files)
Before: 5 overlapping maps (SPINE, globalglobal, SITE-WIDE, NAVIGATION, VISION_AND_NAVIGATION).
After: **2 distinct-purpose files**
- **`AGENTS.md`** = *govern* (rules, doctrine, axioms, Hermes, agent stack)
- **`NAVIGATION.md`** = *navigate* (resolve anything → layer/impl/docs/run/Hermes)
The redundant ones were folded into NAVIGATION as redirects.

### 2.2 The three machine-verifiable manifests (all with runnable validators)
| Manifest | Validator | What it enforces |
|---|---|---|
| `DIRECTORY-MANIFEST.json` | `check_directory_manifest.py` | every top-level folder → role/layer/class (33 folders) |
| `docs/vision/VISION-MANIFEST.json` | `docs/vision/check_manifest.py` | every vision doc → one role/name/file (33 docs) |
| `docs/DOCS-AUDIT.json` | `docs/check_docs_audit.py` | every loose docs/ file → CANONICAL/ARCHIVE/PART_OF (58 files) |

Plus `FEATURE-MODULES.md` (feature → code) and `SCHEMA-AUDIT.json` (the diverged code definitions).

### 2.3 The layer architecture (13 layers, deterministic)
`VISION-CHUNKS.json` — one global vision → 10 chunks → each lands on ONE layer. Progress tracked per-layer
via `docs_state.py` (derived from `object_registry`), not per-agent.

---

## 3. THE HERMES INTEGRATION (the real fix)

### 3.1 The recurring model-config bug — FIXED
**The bug:** `pipeline/model.py` set only `HERMES_MODEL` env, but this Hermes version doesn't read it →
every factory model call failed with "HTTP 401: Model not supported" / "Provider 'deepseek' ... no API key".
**The fix:** `_hermes_call` + `chat_agentic` now pass `-m deepseek-v4-flash --provider opencode-go` explicitly.
**Verified:** `chat()` returns real output; `chat_agentic()` runs. Marked FIXED in `INFRA-INVENTORY.md`.

### 3.2 Hermes as an architecture probe (the proof it's navigable)
Ran a real Hermes agent against the repo:
- **Education test:** Hermes found the vision, ran `docs_state.py`, found the code, and gave an honest
  answer (vision = graph-native tutoring; reality = orphaned compiler + LLM distiller + 0 objects).
- **Navigation test:** Hermes resolved 5/5 questions (NAVIGATION, DIRECTORY-MANIFEST, CATEGORIES, honest
  state, factory scripts).
- **Discoverability friction found + fixed:** Hermes couldn't find `education_compiler.py` by filename →
  built `FEATURE-MODULES.md` so feature→code resolves directly.

### 3.3 The factory→Hermes migration (still on the table, deliberately incremental)
Specced thoroughly (DEV-PLAN 5 phases, the profiles, the MCP verbs, the kanban) but NOT executed. **The
decision this session: build the `patala_*` MCP verbs as the boundary ON TOP of the working factory, not a
big-bang refactor.** The factory works (32k SOURCE, 71 works, L0/L200 certified) — don't rip it out.

---

## 4. THE "WHAT EXISTS" DOCUMENTATION (the under-surfaced gold)

Built 4 canonical indexes documenting the real assets that the architecture docs missed:
| Index | What it documents |
|---|---|
| `GOLD-EVIDENCE-INDEX.md` | what's proven (5 golds, frozen golds, certificates, proofs, domain golds) |
| `DATA-ASSETS-INDEX.md` | the real data (corpus targets, 32k registries, bibliography, site data) |
| `INTERFACES-INDEX.md` | what's callable (19 Hermes skills, 43 API routes, MCP, 7 examples) |
| `EVALS-BENCHMARKS-INDEX.md` | how it's tested (frozen golds, NAT suites, review packets) |
| `IPVV-BUILD.md` | the complete IPVV build (the scholarly proof) |

Plus `FRONTIER-MAP.md` (every layer's best-version + build path), `INDUSTRY-ALIGNMENT.md` (our stack →
formal standards: T1→IGT, L0→TEI+CTS, L200→TranslationProof-NOVEL), `RECONCILIATION.md`.

**The key discovery:** our translation layer `L200`/`TranslationProof` is **genuinely frontier** — no
formal standard covers proof-carrying translation. The layers around it (T1→IGT, L0→TEI, publish→RO-Crate)
should be adapters.

---

## 5. THE IMPORTS (from the sanskritree R2 bucket)

| File | Placed in | What it added |
|---|---|---|
| `commentarialgraph` | `docs/process/06-commentarial-graph.md` | the secondary-scholarship → commentarial-graph layer |
| `externalpaper` | `06-commentarial-graph.md` + manifest | the paper→ScholarContributionPacket compiler |
| `coordinate` | `docs/layers/12-live-system.md` + `docs-cache/` | the peer review (7 pieces, 5 states, the triage) |
| `patalagithubs` | `githubclones.md` §J | the full-stack "adapters around a kernel" map |
| `patalatranslate` | `githubclones.md` §K + Layer 03 + external-tools | the translation subsystem (proof-carrying, benchmarks) |
| `agenticideas` | `docs-cache/` + Layer 12 | the peer review (Scholar Attestation Vertical is the priority) |
| `patalaorganism` (5 files) | `docs/vision/organism/` + `09-organism.md` | the human-understanding graph / Q moat |
| `githubclones`, `agenticideas` | `docs-cache/` + registry | the agentic-stack + KG-tool reviews |

---

## 6. THE HONEST STATE (the anti-theatre verification)

```
REAL + TESTED:  SOURCE→T1→L0→L200, 5 golds, Nyāya gate, certificates, NAT tests, 43 API routes, 19 skills
DATA:           corpus targets, 32k SOURCE objects, 254 works, 71 translated works
DESIGN (not built): Commentarial (06), Organism (09), Economics (11), SYNTHESIS/ESSAY/EDUCATION (0)
ARCHIVED:       the old freestyle pipeline (converted), the ai/ research, devpaths log
SCHEMA DIVERGENCE (flagged, not fixed): ReviewEvent/Authority/Proposition in 3-4 places (SCHEMA-AUDIT.json)
```

All 3 validators pass. A live Hermes agent independently verified the architecture is navigable.

---

## 7. WHAT TO CONTINUE (the priority list for the next agent)

1. **Layer 12 Pieces 1-4** (projection + staleness + MCP verbs) — makes everything non-theatre.
2. **Layer 12 Piece 5 — the Scholar Attestation Vertical** — the frontier differentiator.
3. **Enable SYNTHESIS/ESSAY/EDUCATION** in the factory (currently 0 objects).
4. **Make the 71 RAW-EN works useful** — ensure registered as SOURCE and advancing through the DAG.
5. **Adopt CTS + Stencila** (Layer 02/04) — identity interop + schema-drift fix.
6. **Add `cts_urn`** to passage/work identity (cheap, high value).
7. **Design the `TranslationProof` schema** (Layer 03) — the novel translation moat.

---

*This is the session record. The canonical current-state is `HANDOVER.md` (root). Prior session notes are
in this `handover/sessions/` folder.*

# ENDGAME BUILD — SESSION BUILD RECORD (2026-08-13, the full run)

*Consolidated build record of the 2026-08-13 endgame session — 57 commits from the empirical-
qualification plan through the reconciliation-engine layer. Companion to `INFRA-INVENTORY.md`
(what exists) + `BUILD-NOTES-PROGRESS.md` (strategy/pilot). This is the WHAT-WAS-BUILT log.*

---

## Phase 1 — empirical qualification (devpath13, A1-CONTINUE-v2)

The directive: QUALIFY the system, do not expand the ontology. Force the existing stack through real data.

| Commit | Deliverable |
|---|---|
| `893c9f6` | **P0 ATLAS-NAT-NATURAL-v1** — 51 frozen natural source-resolution cases, non-circular evidence-derived evaluator (SYSTEM_FALSE_AUTHORITY_PROMOTION_RATE=0.216 fixture, detection recall/precision 1.0). |
| `c5d5bfe` | **P1 cross-lane Atlas audit** — found + fixed the publication-gate-not-rights-aware bug (SEVERE), factory gate, single-ladder vocab. |
| `417d2fa` | **P2 close G3A** — ARGMAP NAT on real committed map + 51 IPVV exemplars; NAT-gated proposition derivation (load-bearing ARGMAP failure → NOT_ELIGIBLE). |
| `9db998e` | **P3 IPVV-VERTICAL-001** — froze the source dossier (Pratyabhijñā recognition vs Buddhist adhyavasāya). |
| `06a71d8` | **P6 crux stress-test** — extended crux engine: redundant support (P1-OR-P2), defeaters, alternative routes; verified on the real argument. |
| `2179bd9` | **P7 SYNTHESIS-NAT-NATURAL** — real synthesis preserves the debate (RIVAL_AS_CONSENSUS=0, OPEN_AS_RESOLVED=0). |
| `39194b5`+`c2d7931` | **P8 whole-essay audit** — found + recorded `EF-ESSAY-2026-0001` (load-bearing boundary/rival sentences untraceable). |
| `4fbf753` | **P9 education validation** — 8 interactions, epistemic+pedagogical audit. |
| `124088a` | **P11 whole-chain correction** — REVISE propagates NEED_REVIEW through the chain. |
| `643d7a2` | **P16 PATALA-VERTICAL-1 certificate** — 12/13 nodes, essay traceability honestly OPEN. |

## Phase 2 — the essay repair loop

| Commit | Deliverable |
|---|---|
| `32adfb0` | **ESSAY v2 supersession** — resolved `EF-ESSAY-2026-0001` (S012 boundary traceable, S013 rival demoted, whole-essay GLOBAL_TRACEABILITY). 13/13. |

## Phase 3 — education IR + downstream consumers

| Commit | Deliverable |
|---|---|
| `bc97ad7` | **Education IR** — LearningClaim/Skill/Interaction/MasteryEvidence + interaction compiler (graph-neighbor distractors). |
| `0c7a31e` | Compiled the real VERTICAL-1 argument through the IR. |
| `db8e313` | **Annotation bridge** (INCEpTION/Recogito-style W3C-Web-Annotation export/import). |
| `ffceb10` | **Era C A2-18** — DependencyImpactReport over real production objects. |

## Phase 4 — the decisive bottleneck experiment (IPVV-ARGREC-PILOT-001)

| Commit | Deliverable |
|---|---|
| `9c16373` | **Registry concurrency** — atomic writes + single-writer lock (permanent torn-write fix). |
| `397ca25` | **Pilot freeze** — 5-unit bounded experiment + ArgumentContext layer (T1 units vs ARGMAP context windows, segmentation provenance). |
| `9d43a26`+`9f686c3`+`303c6ef` | Pilot T1/ARGMAP — **used REAL existing V2L T1/L0/C1** (corrected the false need to generate T1), no gold leakage. |
| `ec11368` | **Real recovery result** — the machine independently recovered the V2L argument (objection/reply/crux, UNSUPPORTED_BRIDGE_RATE=0). |

## Phase 5 — the infrastructure audit (DO NOT REBUILD)

| Commit | Deliverable |
|---|---|
| `9057f96` | **INFRA-INVENTORY.md** — WHAT EXISTS / WHERE / DON'T REBUILD (the compass was there all along). |
| `d38c569` | Wired the inventory into all canonical entry points. |
| `0dd950d` | **Security** — untracked 9 in-copyright scholar PDFs from the public repo. |

## Phase 6 — the six real-gap tooling items (P0–P5)

| Commit | Deliverable |
|---|---|
| `dc2c1eb` | **P0 semantic recovery matcher** — 2-stage (embedding align + structured judge, polarity-guard). |
| `3b89f8b` | **P2 OpenCitations** — citation graph → independence + SOURCE_ECHO. |
| `91bbdbe` | **P3 ORCID/ROR** — name-variant→Person, institution→ROR (identity ≠ correctness). |
| `51a0aae` | **P4 scholar-graph eval** — SourceAssertion+CorroborationEvent suffices; quality measurable. |
| `9c71a44` | **P5 Atlas QA audit** — authority-inflation/completeness/rights over 254 records. |
| `aa813f4` | **HERMES-CALLING** — the correct way to call Hermes (agentic `hermes chat`, not blind `-z`). |

## Phase 7 — the reconciliation-engine layer (the ecosystem reframe)

| Commit | Deliverable |
|---|---|
| `52d0c64` | **P4 MANUSCRIPT-RESOLUTION-GOLD** — 10 frozen cases, FALSE_MERGE_RATE primary. |
| `4f44581` | **P3 entity reconciliation engine** — typed CandidateMatch (EXACT/PROBABLE/POSSIBLE/CONFLICT/UNRESOLVED). |
| `1481c57` | **P3↔P4 loop** — engine vs gold: FALSE_MERGE_RATE=0, abstains 30%. |
| `ea67d1a` | **P2 ExternalRecord + adapter framework** — raw-immutable record + ReconciliationAdapter contract. |
| `0126511` | **Text fingerprints** — incipit/explicit/ngram/MinHash + candidate_rank. |
| `c897b26` | Recorded the reconciliation layer in the inventory. |

## Phase 8 — the Pāṭala THESIS (the global README)

| Commit | Deliverable |
|---|---|
| `b5e8a8b` | **The Pāṭala Thesis** (`docs/global/README.md`) — what Pāṭala is (authority graph + reconciliation engine), is not, the one contribution, the integration posture (borrow 26 tools, own the evidence seam), the authority ladder, the products, the honest proven state. Wired into `docs/INDEX.md`. + `SESSION-BUILD-RECORD-2026-08-13.md`. |

## Phase 9 — ATLAS-100 (the main project now)

| Commit | Deliverable |
|---|---|
| `c1d822b` | **#1 Hermes fix** — added agentic `chat_agentic()` (correct `hermes chat`, not blind `-z`); semantic judge uses it. |
| `954f439` | **#2 Atlas backfill** — `atlas_backfill.py` parses the rich `audited.ts` (node) → 11 provenance-carrying candidates (every field has value/source/derivation/authority_state). |
| `07815a2` | **#3/#5 ATLAS-10 + quality scorecard** — per-dimension PASS/OPEN/FAIL + completeness vector. |
| `d154a1f` | **#4 Scholarship side** — real Ratié/Torella → IPVV proposition corroboration (publication/span/relation/independence). |
| `ebce504` | **#6/#7 Agent-1 QA + 50-IPVV recovery batch** — 0 authority-inflation on backfill; semantic scorer over 50 golds. |
| `d0ea3c7` | **#9 INCEpTION gold** — 20-passage real annotation project (8 layers, W3C-Web-Annotation) ready for human gold. |
| `27bdaaf` | **#10 Adapter coverage** — measured: modern-paper adapters (Crossref/OpenAlex/OpenCitations) ~0% coverage for Sanskrit tantric works; name-normalization 5/5. The local scholar corpus + fingerprints are the real path. |
| `fa6033b` | **Factory T1 via agentic hermes** — switched the T1 batch to `chat_agentic` (file access) not blind `-z` + robust batch JSON parse. |

## Phase 10 — FULL PROJECT AUDIT (5 parallel subsystems)

| Commit | Deliverable |
|---|---|
| `PROJECT-AUDIT.md` | The consolidated read-only audit of all 5 subsystems (factory, ML/research, source-evidence/external-tools, Atlas, app/API/MCP/data). Core is healthy + green; real findings: unwired high layers, IPVV passage-id mismatch, thin-vs-rich Atlas, stale schema duplicate, live-registry debt, L1/L1L2 duplication, hard-coded paths. |
| audit-fix pass | Deleted the stale `schema/schema/` duplicate; `atlas_persist_rich.py` wrote the rich scholarship graph to Postgres (3 editions/8 etexts/6 scholarly_work/9 related); added `/api/education` + refreshed the `/api` index; env-config'd machine paths; added THEME to scheduler (later reverted per P4). |

## Phase 11 — CANONICAL-GRAPH-1 (make one graph genuinely canonical; no new features)

| Commit | Deliverable |
|---|---|
| `6dcb5d3` | **P0 PassageIdentity crosswalk** — IPVV id reconciliation: published (`pt:passage:ipvv:chunk*.md`) + segmented (`tantra:text:...:V2-A:<slug>`) ids now resolve to ONE canonical via the V-tag. 49/49 + 231/231 resolve (invariant holds); published-only V1 chunks resolve honestly to themselves. |
| `12bb100` | **P1 REGISTRY-FORENSICS-v1** — read-only classifier (no mutation): 789 bad parents = 723 MISSING_HISTORICAL_OBJECT (orphaned L0), 66 MISSING_PARENT, 119 WRONG_HASH_COMPUTATION conflicts, 521 duplicates, 6 legacy placeholders. Fix-by-class recorded. |
| `da6b31e` | **P2 L2 canonicalization / L1 retirement** — L2 is the ONE canonical contract; L1L2 = producer impl emitting L2-shaped; L1 = RETIRED. Decision doc, no factory change. |
| `738e66c` | **P4 on-demand projections** — reverted THEME from LAYER_ORDER (lateral index, not epistemic parent); THEME/ESSAY/EDUCATION stay on-demand, not automatic. |
| `1f6bfa0` | **P7 TEST-HYGIENE** — cleared the 2 stale ML tests (evidence-aware essay validator aligned to unprefixed refs + NOT_AUDITED-when-incomplete; vertical generates deterministic proof fixture). ML suite 39/39. |
| `EF-ARGMAP-2026-0001` | **P6** — froze the real V3M unsupported-inference live defect as an EvaluationFinding. |
| `8d7de32` | **P3 real ARGUMENT + SYNTHESIS workers** — replaced the generic_generator stub: ARGUMENT derives propositions+cruxes from eligible ARGMAP (hard gate: ARGMAP eligible + traceable + no unsupported bridge, else DEPENDENCY_BLOCKED); SYNTHESIS builds ArgumentSynthesis from Arguments+Cruxes (never resolves open disputes). Wired into LAYER_HANDLERS. |
| factory-T1 | Parallel factory commits (0c83f11/d0d0334/8070e5c/8f6b921): T1 batch via file prompts + persistent per-work hermes sessions — reliable 50-verse batches. |

---

## Session totals

- **~76 commits**, all pushed to `origin/agent2`.
- Built: 5 NAT/bench evaluators + 6 external-tool adapters + the reconciliation-engine layer (ExternalRecord/EntityResolution/ManuscriptGold/Fingerprints) + the IPVV pilot (real argument recovery proven) + the ATLAS-100 pipeline (backfill/scorecard/scholarship/QA/INCEpTION) + the Pāṭala Thesis + the full project audit + CANONICAL-GRAPH-1 (passage identity, registry forensics, L2 canonicalization, on-demand projections, ARGUMENT/SYNTHESIS workers, test hygiene).
- Fixed: registry concurrency, the resolver publication-gate inflation bug, the essay traceability gap, the Hermes `-z`-vs-agentic bug, the stale schema duplicate, the thin-vs-rich Atlas gap (rich graph → Postgres).
- Security: removed 9 in-copyright PDFs from the public repo.

## Open review items (carried forward)

1. ~~Hermes model-config~~ — FIXED (`chat_agentic`, agentic path).
2. Atlas bibliography thin — the ATLAS-10 backfill pipeline now fills it from `audited.ts` (ongoing: scale to ATLAS-100).
3. Repo history rewrite (owner decision, destructive).

## CANONICAL-GRAPH-1 exit-criteria status (P8 in progress)

- [x] all IPVV passage aliases resolve canonically (P0: 49/49 + 231/231)
- [x] registry bad-parent hashes classified (P1, read-only; repair deferred — no factory mutation)
- [x] one canonical L2 production path (P2 decision)
- [x] ARGUMENT real worker (P3)
- [x] SYNTHESIS real worker (P3)
- [x] no generic fallback for epistemic layers (P3)
- [x] V3M real inference defect frozen (P6, EF-ARGMAP-2026-0001)
- [ ] one real IPVV passage traverses Source→…→C1→Proposition→Argument→Crux→Synthesis (P8 — whole_chain_proof script in progress)
- [ ] same object accessible through API/MCP (P8 — the PassageIdentity crosswalk enables it; the API route wiring is next)
- [ ] exact upstream + downstream trace works (P8)

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

---

## Session totals

- **57 commits**, all pushed to `origin/agent2`.
- Built: 5 NAT/bench evaluators + 6 external-tool adapters + the reconciliation-engine layer (ExternalRecord/EntityResolution/ManuscriptGold/Fingerprints) + the IPVV pilot (real argument recovery proven).
- Fixed: registry concurrency, the resolver publication-gate inflation bug, the essay traceability gap.
- Security: removed 9 in-copyright PDFs from the public repo.

## Open review items (carried forward)

1. Hermes model-config (default works; overrides 401 — see `HERMES-CALLING`).
2. Atlas bibliography thin (254 recs, 1/8 fields) — the ATLAS-100 backfill target.
3. Repo history rewrite (owner decision, destructive).

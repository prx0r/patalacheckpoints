# PĀṬALA — THE HANDOFF QUEUE (the shared integration truth)

*2026-08-14 · status: LIVE · the reconciled truth of every kernel between the two sides.
- **AGENTGRAPH** (ip-graph) builds the frontier kernels + proves the mechanism.
- **AGENTPATALA** (patala) wires them into the real system, tests on real IPVV/gold/Hermes, ships products.
- This file is updated by both: AGENTGRAPH when a kernel is proven/built, AGENTPATALA when it's integrated.*

**Status legend:**
- `BUILT` = agentgraph: real-data validator passes (their BUILT-BY-LAYER ✅)
- `MECH` = agentgraph: mechanism-only (synthetic, honestly flagged)
- `INTEGRATED` = agentpatala: wired into real Pāṭala + tested on real data/Hermes
- `NOT-BUILT` = the gap

---

## THE RECONCILED PICTURE (agentgraph's 37 kernels → agentpatala's integration)

### L00 Core — ✅ agentgraph fully built
| Kernel | agentgraph | agentpatala integration |
|---|---|---|
| `epistemic.py` | ✅ BUILT | **INTEGRATED** — tested honest ceiling on fresh IPVV |
| `schema.py` | ✅ BUILT | ⚠️ blocked by the schema.py collision (run in separate processes) |
| `certificate.py` | ✅ BUILT | FRONTIER (expansion E1, marketplace) |

### L01 Source/Provenance — ✅ agentgraph fully built
| Kernel | agentgraph | agentpatala |
|---|---|---|
| `source_registry.py` | ✅ BUILT | FRONTIER — needs real corpus integration |
| `fts_search.py` | ✅ BUILT | FRONTIER |

### L03 Factory/Translation — ✅ agentgraph fully built (the moat)
| Kernel | agentgraph | agentpatala |
|---|---|---|
| `translation.py` | ✅ BUILT | **INTEGRATED** — 11-dim vector + gate tested |
| `translation_variant.py` | ✅ BUILT | FRONTIER — needs real verse via Hermes (three-version) |
| `vidyut_l0.py` | ✅ BUILT | FRONTIER — needs real IPVV L0 commit |
| `staleness.py` | ✅ BUILT | **INTEGRATED** — diamond-DAG precision tested |
| `discovery.py` | ✅ BUILT | FRONTIER (expansion E3, what-if) |

### L04 Argument/Crux — ✅ agentgraph fully built
| Kernel | agentgraph | agentpatala |
|---|---|---|
| `review.py` | ✅ BUILT | **INTEGRATED** — machine-can't-promote tested |
| `essay_ingest.py` | ✅ BUILT | **INTEGRATED** — mines claims on real IPVV |

### L05 Review/Gate/Evolution — ✅ agentgraph fully built (+1 mech)
| Kernel | agentgraph | agentpatala |
|---|---|---|
| `scholar_review.py` | ✅ BUILT | **INTEGRATED** — adversarial panel BLOCKED with dissent tested |
| `integrity_gate.py` | ✅ BUILT | FRONTIER |
| `open_ended_evolve.py` | ✅ BUILT | FRONTIER |
| `skill_graph.py` | ✅ BUILT | FRONTIER |
| `evolve.py` | ⚠️ MECH | FRONTIER — needs real arguments |

### L06 Retrieval/Compiler — ✅ agentgraph fully built
| Kernel | agentgraph | agentpatala |
|---|---|---|
| `query.py` | ✅ BUILT | **INTEGRATED** — passage query tested |
| `retrieval.py` | ✅ BUILT | INTEGRATED (mechanism) — PathRAG/HippoRAG run + rank |
| `context_compiler.py` | ✅ BUILT | FRONTIER |
| `alignment_flywheel.py` | ✅ BUILT | FRONTIER |
| `evidence_ledger.py` | ✅ BUILT | FRONTIER |

### L07 Surfaces/SEO/Audit — ✅ agentgraph fully built
| Kernel | agentgraph | agentpatala |
|---|---|---|
| `seo.py` | ✅ BUILT | FRONTIER |
| `bundle_router.py` | ✅ BUILT | FRONTIER |
| `verification_ensemble.py` | ✅ BUILT | FRONTIER |
| `structure_recall.py` | ✅ BUILT | FRONTIER |

### L08 Scholar/Self-proving — ✅ agentgraph fully built
| Kernel | agentgraph | agentpatala |
|---|---|---|
| `system_provenance.py` | ✅ BUILT | FRONTIER (expansion E5, self-proving) |

### L09 Organism/Education — ⚠️ the genuinely partial layer
| Kernel | agentgraph | agentpatala |
|---|---|---|
| `education.py` | ⚠️ MECH | **INTEGRATED** (mechanism) — LearningClaim + wrong-answer→neighbor tested |
| `pedagogy.py` | ⚠️ MECH | **INTEGRATED** — mastery reducer tested |
| `organism.py` | ⚠️ MECH | INTEGRATED (mechanism) |
| `organism_loop.py` | ⚠️ MECH | INTEGRATED (mechanism) |
| `agent_delivery.py` | ⚠️ MECH | INTEGRATED — task+budget tested (gap E: signed auth) |
| `self_healing.py` | ✅ BUILT | FRONTIER |
| `next_action.py` | ✅ BUILT | FRONTIER |

### L10 Read/Compare — ✅ agentgraph fully built
| Kernel | agentgraph | agentpatala |
|---|---|---|
| `lightrag_compare.py` | ✅ BUILT | FRONTIER |
| `cognee_compare.py` | ✅ BUILT | FRONTIER |

### Cross-layer
| Kernel | agentgraph | agentpatala |
|---|---|---|
| `patala_product.py` | ✅ BUILT | **INTEGRATED** — 18/18 on real V2-A |

---

## THE NOT-BUILT GAPS (what's waiting)

| Gap | Which side | Why |
|---|---|---|
| `misconception.py` repair cascade | **AGENTGRAPH** (new kernel) | the flywheel's closing edge (misconception→source-repair) |
| Corpus-wide IPVV graduation | **AGENTPATALA** | only ONE claim proven end-to-end, not a full pass |
| Commentary + live Tokenization + Essay projection | **AGENTPATALA** (wire + test) | the 3 v3 needs-build products |
| Live TranslationProof auditors (xCOMET/MQM) | AGENTGRAPH (integrate) | the full proof product |
| Signed attestation (gap E) | AGENTPATALA (wire C2PA/ORCID) | before public marketplace |
| The Scholar Workbench UI (vision-07) | AGENTPATALA | the human surface |
| Context paging (gap A) | AGENTGRAPH or AGENTPATALA | the retrieval gap |

---

## THE PROMOTION RULE (the gate)

> A kernel is `INTEGRATED` only when **AGENTPATALA** has run it on **REAL Pāṭala data** (real IPVV/gold
> through the real Hermes path) and it works. AGENTGRAPH proves the mechanism; AGENTPATALA makes it real.
> That's the promotion from their ✅ to my INTEGRATED.

**Current: 10 kernels INTEGRATED by agentpatala, 27 at frontier (theirs, built but not yet wired into
real Pāṭala).** The frontier→integrated promotion is the ongoing work.

---

*Both sides update this file. AGENTGRAPH: mark built/proven. AGENTPATALA: mark INTEGRATED + add the proof.
This is the single coordination truth between the two repos building one Pāṭala.*

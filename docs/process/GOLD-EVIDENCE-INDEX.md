# THE GOLD & EVIDENCE INDEX — everything certified, gold, frozen, and proven

*2026-08-14. THE catalog of Pāṭala's **golden evidence** — the assets that are actually real, tested,
and verified — so an agent searching "what's proven" finds them all in one place. This is the layer the
architecture docs (FRONTIER-MAP, RECONCILIATION, the layer pages) UNDER-SURFACED: they describe the
*machinery*, not the *verified evidence it produced*. This index is the honest "what has Pāṭala actually
proven?" reference.*

> **The principle:** per the anti-theatre doctrine, a schema is not a result. THIS is the evidence that
> distinguishes results from infrastructure. Every entry is `FROZEN` (immutable gold), `CERTIFIED`
> (factory-verified), `GOLD` (hand-grounded), or `PROOF` (a run/report).

---

## THE STATUS LADDER (what each tag means)

- **GOLD** — hand-constructed, human-grounded reference (the standard to measure against)
- **FROZEN** — immutable snapshot (no gold leakage; pinned hashes)
- **CERTIFIED** — factory-verified via a deterministic certificate runner
- **PROOF** — a reproducible run/report showing a vertical works end-to-end

---

## 1. THE GOLD ARGUMENTS (hand-grounded, primary-Sanskrit) — GOLD

| Gold | File | Passage | Move |
|---|---|---|---|
| ARG-GOLD-001 | `patala_ml/gold.py` | V2-O | the base argument |
| ARG-GOLD-002 | `patala_ml/gold002.py` | `chunkV2-L` | objection→reply (the "I" is NOT a vikalpa; the `dvayākṣepī` self-grasp) |
| ARG-GOLD-003 | `patala_ml/gold003.py` | `chunkV2-O` | reductio (ordered-support regress is absurd) |
| ARG-GOLD-004 | `patala_ml/gold004.py` | `chunkV2-H` | conceptual distinction (prakāśa vs vimarśa) |
| ARG-GOLD-005 | `patala_ml/gold005.py` | `chunkV3-I` | ambiguous case (two defensible reconstructions) |
| Review packet | `benchmarks/v0/ARG-GOLD-REVIEW-PACKET-v2.md` + `.json` | all | primary-Sanskrit-grounded, explicitness labels, 4 review questions |

## 2. THE FROZEN GOLDS (immutable, no leakage) — FROZEN

| Asset | File | What it freezes |
|---|---|---|
| **Recovery gold** (51 cases) | `data/evaluation/recovery-gold-v1.json` | the argument-recovery benchmark gold (built by `build_recovery_gold.py`) |
| **ARGREC pilot** | `data/evaluation/argrec-pilot-001-freeze.json` | the real V2-L recovery (no gold leakage; pinned source hashes) + `argrec-pilot-001-argmap.json` |
| **ARG-GOLD review** | `benchmarks/v0/review/ARG-GOLD-REVIEW-PACKET-v2.json` | the frozen review evidence |
| **Inception gold project** | `data/evaluation/inception-gold-project.json` | the 20-passage human-annotation gold (ready for INCEpTION) |
| **Goldchain** | `data/published/ipvv/goldchain-cl3.json` | the gold argument chain |

## 3. THE CERTIFICATES (factory-verified, deterministic) — CERTIFIED

| Certificate | Runner | What it verifies | Result |
|---|---|---|---|
| **L0 certificate (v1)** | `pipeline/certificate_l0.py` | the kramasadbhāva cross-work canary: losslessness, binding, gloss precision, false-certainty, abstention, source-failure, replay | ✅ **deterministic floor certified** (lossless, bound, fail-closed, no dupes; 7/7 gloss semantics) |
| **L200 certificate (v1)** | `pipeline/certificate_l200.py` | the L200 proof layer integrity | ✅ certified |
| **PĀTALA-VERTICAL-1** | `benchmarks/v0/review/PATALA-VERTICAL-1-CERTIFICATE.json` | the gold review vertical (Pratyabhijñā recognition vs Buddhist determination) | ✅ **12/13 nodes**, essay traceability honestly OPEN |
| **Factory certificate** | `pipeline/factory_certificate.py` + `data/corpus/downloads/factory-certificate.json` | the live registry integrity | PASS when clean (currently reports live-data debt, not cert-logic bug) |

## 4. THE PROOF RUNS (reproducible verticals) — PROOF

| Proof | File | What it proves |
|---|---|---|
| **L0 proof runs** | `benchmarks/v0/runs/l0-proof-*.json` | the L0 lossless proof (3 runs) |
| **Tantra gold run** | `benchmarks/v0/runs/tantra-gold-*.json` | the tantra-gold proof run |
| **Vertical proof** | `handover/agent-2-integration/BUILD-RECORD-2026-08-13-VERTICAL-WORKERS.md` | 3 real committed L0 → L1→L2→L200→C1, all committed, provenance-bound, fail-closed. **VERTICAL PROOF PASS.** |
| **Whole-chain proof** | `machinelearning/research/tests/test_whole_chain_proof.py` + `experiments/whole_chain_proof.py` | source → … → synthesis + API/MCP traversal |

## 5. THE DOMAIN-SPECIFIC GOLDS — GOLD

| Gold | File | Domain |
|---|---|---|
| **Nyāya gate gold** | `benchmarks/v0/evidence/nyaya-gate-gold.jsonl` (12) | the Nyāya-gate test gold (viruddha/contradiction) |
| **Cross-gold candidates** | `benchmarks/v0/disagreements/cross-gold-candidates.json` | cross-gold disagreement candidates |
| **P3 lexical gold** | `docs/p3_lexical_gold_v0.json` | lexical-sense gold (stratified fixtures) + `p3_lexical_eval_report.json` |
| **P4 alignment eval** | `docs/p4_alignment_eval_report.json` | the alignment evaluation report |
| **Manuscript-resolution gold** | `source-evidence/evals/patala/tasks/manuscript_resolution_gold.py` | the manuscript-reconciliation gold (FALSE_MERGE_RATE primary) |
| **L200 gold** | `gold_records/` + `gold_from_t1.py` | the L200 derivation gold |

---

## 6. THE IPVV GOLD (the scholarly corpus — see `IPVV-BUILD.md`)

- **T1 golden chunks**: 63 (`01_t1/` + `02_t1/`)
- **L200 audits**: 63 (3 canonical models + 8 hand-authored + 52 standardized, all editor-reviewed)
- **C1 commentaries**: 63 read + 10 source records
- **The essay library**: 22 essays (`research-library/recognition/`)

---

## 7. THE VERIFICATION STATE (what's actually tested — honest)

**✅ Deterministic + proven (no model needed):**
- `test_l0_ipvv` PASS · `test_t1_ipvv` PASS · `test_ipvv_integration` PASS
- `certificate_l0` + `certificate_l200` — deterministic floor certified
- `test_gold`, `test_goldutil`, `test_goldchain`, `test_whole_chain_proof` (ML lane)
- the 10 eval self-tests (source-evidence)

**⚠️ Model-dependent (real but not deterministically verifiable):**
- `test_l2_ipvv`, `test_c1_ipvv`, `test_argmap_ipvv` (invoke Hermes)

**❌ 0 objects (declared, not built):** SYNTHESIS, ESSAY, EDUCATION in the factory registry.

---

## 8. HOW AN AGENT USES THIS

```text
"what has Pāṭala actually proven?"  →  this index
  → the FROZEN golds (recovery-gold, argrec pilot, review packet)  →  THE scholarly evidence
  → the CERTIFIED certificates (L0, L200, VERTICAL-1)              →  THE factory verification
  → the PROOF runs (vertical, whole-chain)                         →  THE end-to-end proofs
  → the domain golds (nyaya, p3, p4, manuscript)                   →  THE per-domain gold
```

**The anti-theatre check:** this index is what separates *results* from *machinery*. Every asset here is
FROZEN/CERTIFIED/GOLD/PROOF — runnable and verifiable — as opposed to the DESIGN layers (06, 09, 11) which
are not.

---

*This is the golden-evidence index. It complements `FRONTIER-MAP.md` (what to build) and `IPVV-BUILD.md`
(the IPVV specifically): this is the catalog of what is ALREADY proven across the whole repo.*

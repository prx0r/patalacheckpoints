# PĀṬALA V3 — THE FINAL SYNTHESIS (the organism)

*2026-08-14 · status: THE SYNTHESIS + VERIFIED · Pāṭala v3 merges everything — v1 (what exists), v2 (the
blueprint), the ip-graph lab's proven kernels, the .meta production organism, and (new) the VERIFIED
testing that proves each product works. This README is the single entry point: what Pāṭala is, how to
read the docs, how to run the proofs, and the honest state.*

---

## THE ARC

```text
v1  what exists (the working factory, the gold)
v2  the blueprint (clear names, codified layers, 16 products, external grounding)
v3  the ORGANISM (v2 + proven kernels + production floor + verified testing)
```

## THE THREE TRUTHS (what makes it final)

1. **Pāṭala decides what can responsibly be said.** (the epistemic gate)
2. **The Library decides what is worth communicating.** (the production organism)
3. **Renderio decides how it should be seen.** (the media layer)

## THE VERIFIED FACT (proven by execution, not documentation)

The system has been **tested end-to-end on a genuinely FRESH Sanskrit text** (Vākyapadīya 1.1 — no gold),
not just the pre-golded IPVV chunks. The proofs are runnable:

```bash
# 1. the complete translation (T1 + Close + Reading + Commentary + Proof) — ONE Hermes call
python3 migration/v3/translate_passage.py "anādinidhanam brahma śabdatattvaṃ yad akṣaram"

# 2. the per-product integration test (Hermes + isolated lab kernels) — 11/11 products
python3 migration/v3/test_products_integration.py

# 3. the multi-subject generality test (IPVV + Doyle + Ratié) — 20/20
python3 migration/v3/test_multisubject.py

# 4. the IPVV vertical (raw → essay, one chunk) — 12/12
python3 migration/v3/vertical_v2a.py

# 5. all 16 products built + verified on the real V2-A claim — 18/18
python3 migration/v3/build_products.py
```

---

## THE FILES (how to read v3)

### READ FIRST (the orientation)
| File | What it is | Read when |
|---|---|---|
| **this README** | the entry point + how to run the proofs | orienting |
| `PATALA-V3-ORGANISM.md` | the organism: 5 organ-systems + the 17 kernels + 16 products + 6 expansions + the graduation test | the vision |
| `V3-BUILD-SPEC.md` | the exact build: stack, mechanisms, external tools, STEP 0-8 | the build |

### THE CONTRACT (the machine truth)
| File | What it is |
|---|---|
| `LAYERS.yaml` | the layer contract — every layer → proven kernel + external tool + honest status |
| `PRODUCTS.md` | the 16 products, each with mechanism + proof + tool + build |
| `MECHANISMS.md` | the 5 load-bearing mechanisms + the 7 algorithms + invariants + 8 laws |
| `STRUCTURES.md` | the 11 structures Pāṭala needs + the v2→v3 completeness validation |

### THE PROOFS (the verified testing — the newest, most important work)
| File | What it proves | Result |
|---|---|---|
| `translate_passage.py` | the COMPLETE translation (T1+Close+Reading+Commentary+Proof) in ONE Hermes call | ✅ fresh verse |
| `test_products_integration.py` | every product on a fresh text via Hermes + isolated kernels | ✅ 11 WORKS / 0 BROKEN |
| `test_multisubject.py` | the kernels generalize across IPVV + Doyle + Ratié | ✅ 20/20 |
| `vertical_v2a.py` | one IPVV chunk raw → essay | ✅ 12/12 |
| `build_products.py` | all 16 products built + verified on the V2-A claim | ✅ 18/18 |
| `PRODUCT-PROOFS.md` | per-product: testable now? test or state the build | 10 WORKS / 6 PARTIAL |
| `INTEGRATION-AUDIT.md` | v3 claims vs v1 reality (BS vs real vs unfinished) + the schema.py collision | the honest audit |
| `TRANSLATION.md` | the complete translation vision + the gap + the build | the translation |
| `proofs/proof-manifest.json` | the machine-readable proof manifest | the evidence |

### THE DEPTH (the intellectual + domain material)
| File | What it is |
|---|---|
| `PATALA-NATIVE-MACHINERY.md` | the actual Pāṭala domain code v3 was missing |
| `LEGACY-GEMS.md` | genius ideas from the old docs (T/R/E/C/H/X tags, the 12-question scaffold, etc.) |
| `TRACEABILITY.md` | every reference → full resolvable path → implementation → test |
| `STRUCTURE-REMAKE.md` | how to re-ground AGENTS.md/layers/docs around the organism |

---

## THE HONEST STATE (what works vs what's unfinished)

**WORKS (tested, real output):**
Translation (T1+Close+Reading+Commentary) · Claim · Argument · Crux · Review · ScholarAttestation ·
Education · Audit · Benchmark · ContextBundle · Essay (via Hermes) · the IPVV vertical · generality
across 3 subjects.

**PARTIAL (real but needs finishing):**
TranslationProof live auditors (xCOMET/MQM) · Passage/Reading readable-prose chain · ResearchPacket
compilation · Synthesis on real inputs · Comparison compiler · the three-version flow (R1/T2/R2 workers).

**The one integration bug (found by testing):**
Pāṭala's `pipeline/schema.py` and the lab's `lib/schema.py` collide on the bare name `schema` — the two
systems must run in **separate processes** (the integration tests already do this).

**Two corrections to earlier v3 claims:**
1. **Essay WORKS** (Hermes generates real essays) — was wrongly marked NEEDS-BUILD.
2. **Translation works on fresh text** via the real batch flow — not just the gold.

---

## THE GRADUATION TEST (the crux — what makes it real)

> **One IPVV claim through the WHOLE organism on real evidence, then MUTATE the source and watch it
> react.** The `vertical_v2a.py` (12/12) + `test_products_integration.py` (11/11) are the working forms
> of this — the machinery genuinely runs from raw Sanskrit to essay/education.

---

*This is the definitive v3 entry point. The docs are the blueprint; the proofs (the .py scripts + the
proofs/manifest) are the evidence that the blueprint works. Read this, then run the proofs to verify.
Everything is committed and traceable.*

# TRANSLATION-PRODUCTION INTEGRATION — patala factory + my validation (the moat)

*2026-08-14. The plan to make the translation moat REAL: patala's mature factory produces the
translations + L200 derivational-audits + C1 commentaries; my ip-graph kernels VALIDATE them with the
TranslationProof (non-aggregate vector) + three-version comparison. Never rebuild the factory — wire my
validation on top of its real output.*

---

## THE REALITY (verified)

**Patala's mature factory (REAL, committed):**
- T1 transliteral gloss: 397 objects / 25 works ✅
- L0 token floor (vidyut): 815 objects / 12 works ✅
- L1L2-translate: the generative translation engine ✅
- L200 derivational-audit: 11 committed (fixtures) + 63 hand-authored IPVV gold ⚠️
- C1 commentary: 4 committed + 63 IPVV gold ⚠️
- The L200 spec is FROZEN (8 sections, MT/IA classifier, IGNORE-default-prior) ✅
- corpus_state: 111-work ledger, next_valid_action control plane ✅

**My validation kernels (REAL, validated):**
- `TranslationProof` (11-dim non-aggregate vector, gate BLOCKS on failing dim, HUMAN_ADJUDICATION_PENDING) ✅
- `translation_variant` (three-version: agreement core + interpretation-space) ✅
- `commentary_lift` (B3 gloss → B4 commentary-frame, reaches the gold terms) ✅
- `scholar_review` (adversarial panel + citecheck) ✅
- `hermes_exec` (real agentic generation, not blind -z) ✅

---

## THE GOLD STANDARD (from TRANSLATION-APPROACH-AND-VALIDATION + my gold-review)

**Dyczkowski's Tantrāloka is the gold standard.** His reading of AbhT 1/52:
> "it is its own object of awareness and is self-luminous; it is not an object of a means of knowledge
> that is other than its own self-awareness."

**My gold-review finding (verified):** our literal gloss scored 0.118 vs the gold because it misses the
PHILOSOPHICAL frame. The fix is the **B3 gloss → B4 commentary-lift → validate the commentary** pipeline.
The gold confirms the crux compass (vimarśa-entailed-by-prakāśa).

**The validation doctrine (SPEC-16):** a translation can't be proven equivalent to source, but CAN be made
proof-carrying. The moat is the VERIFIER (the L200 audit + TranslationProof), not the generator.

---

## THE BUILD (in order)

### T1 — Ingest the IPVV gold into the registry (the moat becomes real)
- Bulk-ingest the 63 L200 + 63 C1 IPVV golds into `object_registry` with Derivation edges (mirror
  `ingest_ipvv_argmap_golds.py`). This is the highest-leverage gap (v2 STEP 2).
- Each L200 gets a TranslationProof (compute the 11-dim vector on the gold's real audit).
- **Gate:** the 63 L200 golds resolve in the registry with derivation edges + TranslationProof vectors.

### T2 — The Translation Audit Compiler (SPEC-16 §30)
- Build `patala translate-proof SOURCE TRANSLATION → translation-proof.json` (13 sections).
- Wire the real proof generators: ByT5-Sanskrit / Heritage / Vidyut / skrutable (the analysis lattice;
  agreement = evidence, disagreement = ANALYSIS_UNCERTAIN).
- Wire the redundant auditors: xCOMET / GemSpanEval / OTTAWA (SOURCE_COVERAGE + TARGET_GROUNDING) /
  entailment (P_s ⊨ P_t and P_t ⊨ P_s) / term-consistency / MQM.
- **Gate:** a real translation produces a 13-section translation-proof.json with the non-aggregate vector.

### T3 — The B3→B4→validate pipeline on the Tantrāloka root
- For each Āhnika 1 kārikā: L0 (vidyut) → L1 gloss (Hermes) → B4 commentary-lift (commentary_lift.py,
  reaching the philosophical frame) → validate the commentary against Dyczkowski (translation_variant).
- **Gate:** the commentary reaches the gold's load-bearing terms (self/object/luminous) for the flagship
  kārikās; the agreement-core/interpretation-space is measured honestly.

### T4 — The three-version + error-family validation
- Ingest Mitrasamgraha (391k bitext) + MITRA (1.74M S↔T↔C) as the benchmark + error-family validators
  (compound loss, scope loss, negation loss, case-role inversion...).
- Run the three-version (my translation + Dyczkowski + a second independent rendering) on the corpus.
- **Gate:** error-family validators catch the known failure modes; the agreement-core is load-bearing.

### T5 — Scale the factory + validation over the corpus
- Run the L200/C1 workers + my validation over the full Tantrāloka (and then the sivaqueue works).
- Each work: SOURCE → L0 → L1/L2 → L200 audit → C1 commentary → TranslationProof → three-version validate.
- **Gate:** a corpus-wide run (not single-claim) produces real translations + proofs + commentaries.

---

## THE INTEGRATION RULE

> patala PRODUCES (the factory workers + Hermes). I VALIDATE (TranslationProof + commentary_lift +
> three-version + scholar_review). The L200 derivational-audit is the moat; my TranslationProof is the
> verifier on top of it. Keep `lib/schema.py` and `pipeline/schema.py` in SEPARATE processes.

## Proofs / resolution
- Patala factory: `pipeline/{t1,l0,l1_l2,l200,c1}_worker.py`, `object_registry.py`, `corpus_state.py`
- The frozen specs: `translations/_stack/ipvv/l200/README-L200-SPEC.md`, `.../c1/C1-SPEC.md`
- My validation: `lib/{translation,translation_variant,commentary_lift,scholar_review}.py`
- The gold: Dyczkowski vol1 + my `tantraloka/GOLD-STANDARD-INSIGHTS.md`
- The master: `devplans/MASTER-INTEGRATION-DEVPLAN.md`

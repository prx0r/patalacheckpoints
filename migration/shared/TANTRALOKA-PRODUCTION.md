# TANTRALOKA FULL-CORPUS PRODUCTION — the Mona Lisa at scale

*2026-08-14. The plan to produce the FULL Tantrāloka translation corpus — all 5,860 kārikās (or the
333-Āhnika-1 flagship first) — through the integrated organism: patala's factory + my validation + my read
plane, autonomously. This is the deliverable that makes the whole system real.*

---

## THE REALITY (verified)

- **Ingested:** 5,860 Tantrāloka kārikās (SOURCE), 333 in Āhnika 1.
- **The 7-stage suite passes (7/7):** ingest → atlas → translation → argument → fullstack → validation →
  factory, all auto-derived (no hand-fed theatre).
- **The real generation path works:** `run-tantraloka-autonomous.py` (8/8) — next_action schedules,
  real Hermes generates AbhT 1/52, proof computed on real output.
- **The gold-standard insight:** our literal gloss (0.118 vs Dyczkowski) needs the B4 commentary-lift to
  reach the philosophical frame; validated 5/5.
- **The mature factory:** patala's L0/L1/L2/L200/C1 workers + registry (real).

---

## THE GOAL

**Produce the full Āhnika 1 translation corpus** (333 kārikās): each kārikā gets SOURCE → L0 (vidyut) →
L1 gloss (Hermes) → L2 reading → L200 derivational-audit → C1 commentary → my TranslationProof → validated
against Dyczkowski. Autonomously, logged, compute-on-write.

---

## THE BUILD (in order)

### X1 — The corpus runner (scale the autonomous runner over Āhnika 1)
- Extend `run-tantraloka-autonomous.py` from ONE kārikā to the full 333 of Āhnika 1, driven by
  `next_action` + `factory_pool` (parallel), each kārikā through the chain.
- Each kārikā: real Hermes generation (agentic) → TranslationProof (real output) → integrity gate.
- Log every kārikā (PASS/FAIL/timing) to `tantraloka/corpus/`.
- **Gate:** N kārikās produced real translations + proofs (machine + human logs).

### X2 — The B3→B4 commentary-lift at corpus scale
- For each kārikā: literal gloss (B3) → B4 commentary-lift (reaches the philosophical frame) grounded in
  the pushing crux.
- **Gate:** the commentaries reach the gold's load-bearing terms for the flagship kārikās.

### X3 — Validate the corpus against Dyczkowski (the payoff)
- For each kārikā, three-version compare (my gloss + my commentary + Dyczkowski's real text).
- Measure agreement-core (technical terms) + interpretation-space (where we diverge = the original
  commentary).
- **Gate:** the corpus validates: agreement on the load-bearing core, divergence on the cruxes the pushing
  sessions flagged.

### X4 — Feed the products (essay + education + site)
- The validated corpus → essay (reactive, sentence-sourced) → education (LearningClaims + wrong-answer→
  neighbor) → compile to the site (compute-on-write).
- **Gate:** a Tantrāloka section on the site shows the corpus: translations + proofs + commentaries +
  essays + education, all from the real compiled artifacts.

### X5 — The iteration log (document the autonomous build)
- Every corpus run logged to `tantraloka/logs/` + `tantraloka/iterations/`; the AUTONOMOUS-ITERATION-LOG
  records findings + fixes.
- **Gate:** the full build is documented, failures recorded, no stage skipped.

---

## THE INTEGRATION RULE

> The corpus is produced by patala's factory + my real Hermes generation, VALIDATED by my TranslationProof
> + commentary-lift + three-version, SERVED by my read plane. Autonomously, logged, compute-on-write. The
> 333-Āhnika-1 corpus is the deliverable; the full 5,860-kārikā corpus is the scale-up.

## Proofs / resolution
- The runner: `scripts/run-tantraloka-autonomous.py` (8/8)
- The harness: `tantraloka/run-all.py` (7/7)
- The insight + fix: `tantraloka/GOLD-STANDARD-INSIGHTS.md` + `lib/commentary_lift.py`
- The factory: patala `pipeline/` (t1/l0/l1_l2/l200/c1 workers, object_registry)
- The master: `devplans/MASTER-INTEGRATION-DEVPLAN.md`

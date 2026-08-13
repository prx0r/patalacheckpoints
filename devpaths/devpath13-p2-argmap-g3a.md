# DEVPATH 13 · P2 — CLOSE G3A ON REAL ARGMAP (blind NAT)

**Status: ✅ CLOSED (2026-08-13)**
**Directive:** A1-CONTINUE-v2 P2 — "close G3A on REAL ARGMAP. Do not use gold arguments as the main validation."

---

## What was verified

Agent 1's ARGMAP NAT verifier (`argmap_eval.py`, built in devpath1) runs on **real committed ARGMAP**:

| Input | Objects | Result |
|---|---|---|
| `argmap-registry.jsonl` (Agent 2 factory committed map) | 1 (`kramasadbhava:v1`) | **PASS** (shape + structural NAT) |
| IPVV gold exemplars (real) | 51 maps / 459 samples | shape_pass_rate=1.0, mutation_recall=1.0 |
| Coverage (IPVV pratibhā/āśraya/maheśvara) | present: support/āśraya/maheśvara/pratibhā/flashing/order-less/powers; missing: freedom | PASS |

The ARGMAP-NAT-IPVV task (`argmap_ipvv_eval.py`) covers the **recognition/reflexivity/self-awareness
material** that is the VERTICAL-1 (P3) seed — pratibhā, āśraya, maheśvara are the Abhinavagupta
recognition-doctrine terms.

## The G3A hard rule (added)

`proposition_layer.build_proposition_layer(...)` now takes `argmap_nat_ok`:

> A load-bearing ARGMAP failure makes downstream proposition production **NOT_ELIGIBLE**.

Verified (added to `tests/test_proposition_layer.py`):
```
argmap_nat_ok=None   -> argmap route NOT_ELIGIBLE (counts.argmap == 0)
argmap_nat_ok=False  -> argmap route NOT_ELIGIBLE (load-bearing failure)
argmap_nat_ok=True   -> argmap route ELIGIBLE (counts.argmap >= 1)
```

This is the P2 hard rule from the directive: "load-bearing ARGMAP failure → downstream proposition
production NOT_ELIGIBLE". It closes devpath3 for real.

## Honest status

- The one real committed factory ARGMAP (`kramasadbhava:v1`) is **MACHINE_PROPOSED / NOT_HUMAN_REVIEWED**;
  its NAT PASS is an engineering-validity result, not a scholar-correctness result.
- The IPVV-exemplar eval (shape 1.0 / mutation recall 1.0) is a verifier-competence result on real
  material, not a claim of generator accuracy.
- G3A gate is now enforced in code (eligible → only when NAT passed).

## Deliverables
- `machinelearning/research/patala_ml/proposition_layer.py` — G3A eligibility gate on ARGMAP NAT
- `machinelearning/research/tests/test_proposition_layer.py` — G3A hard-rule tests (all pass)
- ARGMAP NAT run: shape_pass_rate=1.0 on the real committed map (recorded)

**Hand-off:** the real factory ARGMAP batch can now flow into propositions the moment Agent 2 emits
more maps; each is individually NAT-gated.

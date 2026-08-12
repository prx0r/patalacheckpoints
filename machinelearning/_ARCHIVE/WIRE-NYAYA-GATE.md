# WIRING THE NYĀYA GATE INTO PĀṬALA — full justification

*2026-08-12. The best use of the truth-engine's Nyāya gate: implement Pāṭala's **`/verify-claim-semantic`** —
the deterministic gate that decides whether a claim is *logically admissible* (not merely resolvable).
This doc justifies WHY the gate, HOW it wires in, and why it beats every alternative.*

---

## 1. The current state — the exact gap

Pāṭala's verify floor (`lib/verify.ts`) has FOUR functions:

| Function | What it checks | What it does NOT check |
|---|---|---|
| `verifyQuote` | a quote is a verbatim substring | — |
| `verifyClaimStructure` | the claim's passage RESOLVES (has source + L2 + C1) | whether the claim is *sound* |
| `traceDependency` | the derivation DAG backward walk | — |
| `findCounterevidence` | curated contradicts/qualifies edges | discovered counterevidence |

**The gap:** `verifyClaimStructure` answers *"does the passage the claim cites exist and have content?"*
It does NOT answer *"is this claim logically admissible?"* A claim can pass structure while being:
- a **fallacy** (savyabhicara: "meditation always produces nondual awareness")
- **overbroad** (badhita: "consciousness has no neural correlates")
- **unfalsifiable** (no tarka falsifier)
- **counter-balanced** (satpratipaksa: an equally strong counter-claim exists)

The Nyāya gate answers exactly these. **This is the semantic verification the vision's Phase 6 demands.**

---

## 2. The best use: implement `verify-claim-semantic`

The gate becomes Pāṭala's **claim-admissibility gate** — the enforcement of the vision's core rule:

```
DETERMINISTIC_FACT | MACHINE_PROPOSED | HUMAN_REVIEWED | ACCEPTED   — never blur them.
```

Specifically, the gate decides **`can_update_posterior`**: whether a claim is even *allowed* to move
evidence (the Bayesian strength). This closes the loop: `verifyClaimStructure` (does it resolve) →
`verifyClaimSemantic` (is it admissible) → `can_update_posterior` (may it move evidence).

**The wiring (my `argument.py` already has the `gate` slot — this FILLS it with the real engine):**

```
claim
  ↓ pramāṇa assignment      (pratyakṣa | anumāna | upamāna | śabda)
  ↓ tradition scoping
  ↓ 5 hetvābhāsa checks     (savyabhicara / viruddha / asiddha / satpratipaksa / badhita)
  ↓ tarka falsifier check   (every claim needs a falsifier)
  ↓ gate outcome            (accepted / accepted_with_penalty / needs_review / hollow / refuted)
  ↓ can_update_posterior    (deterministic; caps the Bayesian LBF)
```

---

## 3. WHY the gate (vs the alternatives)

### 3a. Why not just trust `verifyClaimStructure`?
Because structure ≠ soundness. A claim citing a real passage can still be a logical fallacy. The gate is
what separates "this claim references evidence" from "this claim is *licensed by* that evidence." The
whole Pāṭala honesty principle (`AI proposes ≠ Pāṭala asserts`) requires the second.

### 3b. Why not a hand-rolled "quality score"?
A numeric quality score is exactly the **BS we removed** (the fake B-STRUCT result). The Nyāya gate is
**categorical and deterministic**: it returns *which fallacy* was committed, with *reasoning* — not a
mysterious 0.87. It's the difference between "a reviewer's verdict with reasons" and "a number."

### 3c. Why this specific gate (vs the 680-LOC alternatives)?
The truth-engine has multiple pieces; the gate is the right one because:
- **It's the enforcement layer** — it decides admissibility, which is exactly Phase 6.
- **It's deterministic** — no model judgment, no calibration needed (unlike the Bayesian engine, which
  needs calibrated likelihoods). The gate is defensible *now*, not after data collection.
- **It produces the reviewable output** — hetvābhāsa failures + falsifier status + `can_update_posterior`,
  which maps onto the vision's review states.

### 3d. Why NOT the full Bayesian engine?
Per `TRUTHENGINE_TO_PATALA_MAPPING.md`: the F1–F8/D1–D5/B1–B6 ontology is metaphysics-specific and does
NOT fit Pāṭala's philological/argumentative claims. The gate is **domain-appropriate** (pramāṇas +
hetvābhāsas are the natural evidence-taxonomy for scholarship); the propagation ontology is not. **Reuse
the gate, reject the ontology.**

---

## 4. The concrete integration (what I'll build)

```
pipeline/  →  a Python port of the gate's validate()/gate_claim() logic
lib/verify.ts  →  add verifyClaimSemantic(claim, ref) → { admissible, pramana, hetvabhasa_failures[], falsifier, can_update_posterior }
app/api/verify/claim-semantic/route.ts  →  the endpoint
mcp/index.mjs  →  verify_claim_semantic tool
```

**The deterministic checks (from `TRUTHCHANGES6` + the 680-LOC gate):**
1. **pramāṇa assignment** — what kind of evidence is this? (replaces ad-hoc "evidence dimension")
2. **hetvābhāsa** — the 5 fallacies, each with a clear criterion
3. **tarka falsifier** — does the claim have a disproof-condition? (no falsifier → weak)
4. **outcome + can_update_posterior** — admissible, or flagged for review

**And the bonus:** `satpratipaksa` (counter-balanced) **IS** `discover_counterevidence` — the gate
detects when an equally-strong counter-claim exists, which is the vision's Phase-6 counterevidence tool,
for free.

---

## 5. Where it sits in the vision

| Vision phase | What the gate provides |
|---|---|
| **Phase 6 — semantic verification** | `verify-claim-semantic` (the gate) + `discover-counterevidence` (satpratipaksa) |
| **Phase 8 — workbench** | "attack this interpretation" = run the gate as the structured critic |
| **Phase 9 — adversarial review** | hetvābhāsa + nigrahasthāna defeat-tracking = the peer-review critic |
| **CP4 — argument layer** | fills `argument.py`'s `gate` slot with the real engine |

---

## 6. The honest caveats

- **The gate is deterministic but the hetvābhāsa *detection* is partly heuristic** (it relies on the
  claim's fields: vyāpti, falsifier, peer-claims). It is sound *given* well-formed input; it does not
  invent the input.
- **It needs a pramāṇa field on Pāṭala's claims** (currently absent) — the first concrete change.
- **It does NOT replace the Bayesian strength** — it *gates* it. `can_update_posterior` decides whether
  the (separate, honest) Bayesian primitive may run.

---

## 7. The bottom line

The best use of the Nyāya gate is **`verify-claim-semantic`**: the deterministic claim-admissibility gate
that decides whether a claim is logically admissible (pramāṇa + hetvābhāsa + falsifier) and whether it may
move evidence (`can_update_posterior`). It beats the alternatives because it is (a) deterministic and
defensible *now*, (b) domain-appropriate (the pramāṇas/hetvābhāsas are the natural scholarship evidence
taxonomy), (c) categorical-with-reasons (not a BS number), and (d) it delivers `discover_counterevidence`
(satpratipaksa) for free. It fills the honest gap — `argument.py`'s empty `gate` slot — with the real,
battle-tested engine, and it is exactly the vision's Phase-6 verification.

# NYAYA GATE — FROZEN CANDIDATE v1 (measured, paused)

*2026-08-12. The Nyāya gate is FROZEN as a measured candidate. Do NOT hack viruddha in now — it needs
a real argument graph, which is the next build. This records the exact result, including the bug/fix that
is part of the research record.*

---

## THE FROZEN RESULT

```
NYAYA_GATE_CANDIDATE_v1
Gold:      12 author-created fixtures (benchmarks/v0/evidence/nyaya-gate-gold.jsonl)
Measured:  defect recall 4/5 · clean FP 0/5 · abstention 1/2
Status:    BENCHMARKED_PRELIMINARY
           NOT_INDEPENDENTLY_VALIDATED
           NOT_SEMANTIC_VERIFIER
```

### The exact result (final)
```
defect-detection (positives, n=5): 4/5 = 0.80
false-positive   (negatives, n=5): 0/5 = 0.00
abstention       (borderline, n=2): 1/2 = 0.50
```
Reproduce: `python3 machinelearning/research/experiments/eval_gate_gold.py`

### The bug/fix (part of the research record)
The FIRST run was `defect 0.20 / FP 0.00 / abstain 0.50` (only satpratipaksa detected). The fix added
real detectors for asiddha/savyabhicara/viruddha/badhita. Then a SECOND regression: fixing the
savyabhicara false-positive (a *valid* "invariably" claim with vyāpti 0.9 was being flagged) dropped
detection to 0.60, then the correct rule (universal claim is a defect UNLESS backed by vyāpti ≥ 0.8)
recovered to 0.80 with FP 0.00.

The pre-fix savyabhicara result: the false-positive (SAVYABHICARA-002, should be CLEAN, got flagged) is
documented in the git history. That bug/fix is retained.

---

## THE BOUNDARY THE RESULT EXPOSES (why we pause)

The 4/5 result is genuinely useful — it maps the boundary:

| Defect | Type | Current gate |
|---|---|---|
| **asiddha** | structural/local | ✅ sometimes detects |
| **savyabhicara** | structural/local | ✅ sometimes detects |
| **satpratipaksa** | structural/local | ✅ sometimes detects |
| **badhita** | structural/local | ✅ sometimes detects |
| **viruddha** | **CONTEXT-DEPENDENT** | ❌ requires knowing what the text establishes |

**viruddha requires a real argument graph** — knowing the IPVV argues the OPPOSITE of "memory proves the
self is constructed" (it argues memory proves a persistent self, V2-P). Keyword rules cannot do this.
Do NOT hack it in — that would recreate the theater failure with a fancier heuristic.

---

## THE COMMIT / FIXTURE VERSION (lineage)

- **Fixture version:** `benchmarks/v0/evidence/nyaya-gate-gold.jsonl` (12 fixtures, SINGLE_REVIEWED)
- **Implementation:** `machinelearning/research/patala_ml/nyayagate.py`
- **Eval:** `machinelearning/research/experiments/eval_gate_gold.py`
- **Git commit:** the commit that added these (see git log — "Nyāya gate: gold fixtures + blind eval")

---

## DO NOT (the guardrails)

- Do NOT hack viruddha into the gate.
- Do NOT rush DOUBLE_REVIEWED on the 12 fixtures before broadening them — a second reviewer is worth it
  only once the fixture design is worth reviewing (target 30–50 fixtures incl. clear pos/neg/near-miss/
  ambiguous/insufficient-context/abstain-correct).
- Do NOT promote to `verify-claim-semantic`. It is `NOT_SEMANTIC_VERIFIER`.

---

## WHAT AGENT ML DOES NEXT (the actual prerequisite viruddha exposed)

Build **Argument Gold v0 properly** — the real argument graphs that viruddha would need to reason over.
Then viruddha becomes a proper graph operation (retrieve accepted propositions → does H support ¬S? →
VIRUDDHA_CANDIDATE → semantic layer decides), not a keyword hack. See `CHECKPOINTS-ML.md` CP4.

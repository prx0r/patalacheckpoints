# HONEST AUDIT — OUR OWN STRUCTURES (the no-BS version)

*2026-08-12. The same brutal standard applied to the Lean work, now applied to EVERYTHING we built.
The recurring failure mode: **structurally-elegant-but-hollow** — well-typed containers, tested schemas,
and impressive-looking statuses, with no real content underneath. This is the honest inventory.*

---

## 1. The recurring failure mode (name it, so we stop it)

We keep building objects that are **schema-valid but substantively empty**, then reporting them as if
they contain scholarship. Three specific instances, same pattern:
1. **B-STRUCT "won"** — circular (premises were C1 titles). Retired.
2. **`strength.py`** — called "the truth-engine Bayesian scorer," actually a toy (weights hand-chosen). Relabeled.
3. **The gold-chain certificate** — STILL hardcoded `EDITOR_APPROVED` (below). Not yet fixed.

The pattern: *a well-tested container is presented as a real result.* The tests prove the schema; they
don't prove scholarship.

---

## 2. The gold-chain certificate is STILL theater (verified just now)

`experiments/build_goldchain.py` lines 99–132 hardcode:
```
L200  → status="EDITOR_APPROVED"
C1    → status="EDITOR_APPROVED"
THEME → status="EDITOR_APPROVED"
ARGUMENT → status="EDITOR_APPROVED"
ESSAYCLAIM → "EDITOR_APPROVED" if EVIDENCED else "SUPPORTED"
```
**No editor approved anything.** This is the same lie the cleanup claimed to remove. We fixed the
*certificate computation* (proof_level logic) but the *builder that feeds it* still fabricates the
statuses. **The gold-chain certificate is not an audit of real review; it's a hardcoded label.**

**This must be fixed before anything is shown as credible.** The honest value: the L0 proof layer IS real
(the OPEN cruxes propagate genuinely). Everything above `L0` in the gold chain is fabricated labels.

---

## 3. The honest inventory (what's real vs. hollow)

### GENUINELY REAL & USEFUL
| Asset | Why real |
|---|---|
| **`benchmarks/v0/`** | frozen, split-policy, per-metric, ARG-GOLD-001. It MEASURES. Most valuable thing we have. |
| **The Nyāya gate** (truth-engine, 680 LOC) | deterministic claim validation (hetvābhāsa/falsifier/pramāṇa). Best asset, unwired. |
| **`verify_l0.py`** (other agent) | honest — it surfaced real bugs. Genuine. |
| **L0 proof layer in the gold chain** | the OPEN cruxes propagate genuinely (V2-L: 2726 unknown chars). Real. |

### STRUCTURALLY-ELEGANT-BUT-HOLLOW (the honest list)
| Asset | LOC | Why hollow |
|---|---|---|
| `strength.py` | 170 | Bayesian toy; weights hand-chosen, uncalibrated. Math right, not useful. |
| `argument.py` | 185 | typed container; `gate` slot empty; "premises" were relabeled source-candidates. No real argument content. |
| `goldchain.py` + builder | 92+ | certificate's `EDITOR_APPROVED` is HARDCODED. Fabricated statuses. |
| `essaygen/essayplan/essayverify/essay/essaysentence` | ~440 | the synthesis layer. User said essays are "just the endpoint." Scope creep. |
| `aifgraph.py` | 148 | structurally sound, no real propositions in it. |
| `c1metrics.py` | 106 | heuristic with unvalidated thresholds (32/63 failed on tuning). |
| `builders.py` + comparison | 123+ | retired as CIRCULAR. |
| `cluster.py` | 194 | real graph topology — but "themes" are machine proposals, not accepted scholarship. |

---

## 4. The brutal takeaway

**We have exactly ONE truly valuable, honest asset we built: the benchmark.** And two real ones from
elsewhere: the Nyāya gate (unwired) and the L0 proofs. Everything else we built this session is either:
- a hollow container presented as a result, OR
- scope creep (the essay layer), OR
- a retired circular result.

**The honest priority is now clear and tiny:**
1. **Fix the gold-chain hardcoded statuses** (or stop showing the certificate as credible).
2. **Wire the Nyāya gate** as `verify-claim-semantic` — the one real claim-validation asset.
3. **Stop building more layers.** Every future build must pass the checkpoint-test: name the checkpoint,
   the object, the benchmark/proof. If it can't, don't build it.

---

## 5. The permanent principle (say it plainly)

> **A tested schema is not a result. A typed container is not an argument. A hardcoded status is not an
> audit. The benchmark is the only thing that turns a container into a result — and even then, only for
> what it actually measures.**

We keep building containers and calling them scholarship. The benchmark exists precisely to catch this —
but we haven't routed our own work through it, and the gold-chain certificate is still fabricating its
top layers. Fix that before adding anything.

# HONESTY CLEANUP — what was invalid, what is real, what it establishes

*2026-08-12. The recovery step. Schema-valid ≠ source-grounded. This records which previous results are
INVALID, which artifacts are real, and what each layer actually establishes — so we never again mistake
structural validity for epistemic validity.*

---

## 1. INVALIDATED RESULTS (retired — do not cite)

| Result | Why invalid |
|---|---|
| **"B-STRUCT wins" (argument-builder comparison)** | CIRCULAR. B-STRUCT's "premises" are the C1 titles/terms, and the ground-truth argument cites the same C1 passages → gt_overlap measures passage-ID overlap, not argumentative content. |
| **"coverage is a real metric, Spearman +0.94"** | Inherits the circularity: coverage = how many member-C1 titles appear in premises, trivially high for a builder that uses member titles as premises. INVALID_METRIC. |
| **The 4-builder comparison (compare_arguments.py)** | Marked INVALID_EXPERIMENT / CIRCULAR_METRIC. The comparison tested passage-reference overlap, not reasoning. |

**Status: the builder comparison is retired.** It did not compare argument quality; it compared
passage-title overlap against a ground truth that shared the same titles.

---

## 2. RELABELED (the honest names)

**The old "premises" were NOT premises.** They were passage labels + key-term lists. They are now:

```
argument_source_candidates   (or passage_evidence_candidates)
```
They are **references to where an argument might be found**, NOT the argument's propositions.
They are NOT called premises until they are actual propositions.

---

## 3. FIXED — fabricated passage IDs

The builders emitted `pt:passage:ipvv:V2L-nonconstructed-I` — a format that does NOT match the real
store (`pt:passage:ipvv:chunkV2-L-...`). These did not resolve.

**Fix (`cleanup.py`):**
- `load_real_passage_ids()` — reads the real store index.
- `resolve_token()` — resolves via EXACT normalized match only; **no fuzzy best-guess** (a
  wrong-but-confident match is worse than an honest UNRESOLVED). Single-letter V1 keys excluded to
  avoid collisions.
- Unresolvable tokens → `UNRESOLVED`, never silently mapped to a wrong passage.

---

## 4. REMOVED — hardcoded EDITOR_APPROVED

The gold chain set `INTERPRETATION / ESSAY_CLAIM: EDITOR_APPROVED` as a hardcoded string. No editor
approved anything. **All generated statuses now default to `MACHINE_PROPOSED`.** Editorial status only
changes through a real review event (the adjudicate.py loop).

The gold-chain certificate now distinguishes:
```
REAL              (L0 proofs, actual source)
MACHINE_PROPOSED  (generated, un-reviewed)
UNRESOLVED        (passage not resolvable)
EDITOR_APPROVED   (only after a real human sign-off)
```

---

## 5. WHAT IS ACTUALLY REAL vs NOT YET REAL

**REAL (genuine):**
- L0 proof machinery (`verify_l0.py` — the P0 harness is honest; it surfaces real bugs)
- C1 corpus (49 passages, 63 C1s, real content)
- graph/community proposals (real graph topology on real C1s)
- the schemas (Claim-v3, AIF, EssayPlan — structurally sound)
- the AIF representation + EssayPlan representation

**NOT YET REAL (was presented as real):**
- argument extraction (no real propositions extracted from C1 prose)
- argument evaluation (the comparison was circular)
- semantic verification (the "verifier" is regex against a hardcoded list, not semantics)
- editorial adjudication (nothing actually reviewed)

---

## 6. THE ENGINEERING PRINCIPLE (now permanent)

```
Schema-valid ≠ source-grounded.
Source-grounded ≠ interpretively justified.
Interpretively justified ≠ logically valid.
Logically valid ≠ historically true.
```

And: **every test suite must declare which layer it establishes** — SCHEMA / RESOLUTION / GROUNDING /
DERIVATION / EDITORIAL / FORMAL — and never report them together as "N tests = scholarship verified."

---

## 7. THE RECOVERY PATH

(a) Honesty cleanup — DONE (this doc + `cleanup.py`).
(b) **Argument Gold v0** — one real, hand-reconstructed argument from a real C1/passage (V2-O),
    with actual propositional premises, conclusion, qualification, explicit/implicit status,
    inference relation, and exact resolvable source support. That hand-adjudicated object becomes the
    first benchmark for automatic extraction. One genuinely correct ArgumentPacket > 1,000 shells.

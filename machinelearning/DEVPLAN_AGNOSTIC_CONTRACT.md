# DEV PLAN — IPVV as the gold standard → the agnostic contract → future texts

*2026-08-12. The plan for how Pāṭala handles ANY future text. The idea: **the IPVV is the canonical
gold standard** — it is the one text we drive through every layer end-to-end and validate. From its
working pipeline we **extract the agnostic contract** (the reusable schemas + validators + specs that
don't depend on Śaiva content). Then any new text follows that frozen contract. The IPVV is the
reference; the contract is the reusable artifact.*

---

## 0. The core insight

Two things are produced when we finish the IPVV:
1. **The IPVV edition itself** (the content — 49 passages, 63 C1s, themes, arguments).
2. **The AGNOSTIC CONTRACT** — the schemas, validators, and specs that make the *process* reproducible
   for any text. This is the transferable asset.

The IPVV is where we *learn* what the contract must be. Once frozen, future texts are validated against
it — so the IPVV is the gold standard that proves the contract works.

```
IPVV (gold standard) ──► working pipeline ──► AGNOSTIC CONTRACT (frozen)
                                                   │
                          Tantrāloka · Spanda · Kubjikā ──► follow the contract
```

---

## 1. What IPVV already proves (the validated layers)

| Layer | IPVV evidence | Generalized? |
|---|---|---|
| SOURCE | Torella IPK + M00020-22, license-tagged | ✅ `SPEC_SOURCE` (agnostic) |
| L0 | 3444-token records, round-trip validated | ✅ `SPEC_L0_L1` |
| L2 | 49 READ passages, fidelity notes | ✅ `SPEC_L2` |
| L200 | 66 audits, 8-section, MT/IA split | ✅ `README-L200-SPEC` |
| C1 | 63 renderings + 10 structured records | ⚠️ spec exists, metrics not yet machine |
| THEME/CLUSTER | 9 V2/V3 clusters (clean) + V1 flagged | ⚠️ my clusterer, not yet a general spec |
| ARGUMENT | 3 LOGICAL-ARGUMENT files | ❌ no schema yet |

**The IPVV proves the bottom layers work agnostically.** The gaps (C1 machine metrics, argument schema)
are exactly what must be frozen before the contract is complete.

---

## 2. The dev plan — three phases

### PHASE A — Finish IPVV as the gold standard (prove the top layers)

Drive the IPVV through the remaining top layers, each validated, so we KNOW the contract works:

| Step | Build | Validated by |
|---|---|---|
| A1 | **C1 machine metrics** (score the 63 IPVV C1s) | all 63 score above thresholds |
| A2 | **Theme-adjudicate** the 9 clusters → accepted IPVV themes | editor accepts/merges/splits |
| A3 | **ArgumentProposal schema + validator** on IPVV (from the 3 LOGICAL-ARGUMENT files + C1s) | resolvable + downward-chain + circularity-guard |
| A4 | **Provenance 4-level contract** on one IPVV essay | RESOLVES/AUTHENTIC/RELEVANT/SUPPORTS typed |

**Phase A produces:** a fully-validated IPVV + a first-draft agnostic contract (the schemas/validators
proven on IPVV).

### PHASE B — Freeze the AGNOSTIC CONTRACT (generalize the IPVV work)

Extract the reusable, content-independent pieces from Phase A into the frozen contract:

| Contract piece | From IPVV | Agnostic form |
|---|---|---|
| **Layer schemas** | the passage record, C1 record, argument record | typed JSON schemas (no Śaiva terms) |
| **Cross-layer validator** | `validate_layers.py` | validates ANY passage through all layers |
| **C1 metrics** | the 10-checkbox → scored metrics | works for any commentary |
| **Cluster spec** | the V2/V3-vs-V1 finding | the general "cluster thematic vs editorial-block" rule |
| **Argument validator** | resolvability/downward-chain/circularity-guard | works for any argument |
| **The PUSHING DNA** | `QUESTIONNAIRE_REAL_DNA.md` (agnostic shapes) | already tradition-neutral |
| **The specs** | `SPEC_L0_L1/L2/SOURCE/...` | already agnostic |

**Phase B produces:** `contracts/` — a directory of frozen schemas + validators + the spec index, all
content-independent. A new text must pass these to be "published."

### PHASE C — Apply the contract to future texts (the replication)

New texts follow the frozen contract mechanically:

```
NEW TEXT (Tantrāloka / Spanda / Kubjikā / ...)
  → validate SOURCE (witness, license, spans)
  → validate L0 (tokens round-trip)
  → validate L2 (propositions traceable)
  → validate L200 (MT/IA split)
  → validate C1 (machine metrics pass)
  → CLUSTER (the agnostic clusterer)
  → THEME-adjudicate
  → ARGUMENT (validate resolvable + gated)
  → provenance-carrying essay
```
Each step is validated by the SAME contract that IPVV proved — no ad-hoc decisions, no re-inventing.

---

## 3. The deliverable — `contracts/` (the reusable asset)

The whole point: a self-contained `contracts/` directory (or `machinelearning/contracts/`) that any
future text runs against:

```
contracts/
  schemas/          passage.schema.json · c1.schema.json · argument.schema.json · provenance.schema.json
  validators/       validate_layers.py · c1metrics.py · validate_argument.py
  metrics/          the thresholds (novelty, boundary, resolvability, ...)
  specs/            the agnostic SPEC_* index (which spec applies at which layer)
  README.md         "how to onboard a new text" — the one-page contract
```

A new text is "done" when it passes every validator in `contracts/`. The IPVV is the reference case
that proves the thresholds are right.

---

## 4. The priority order (what to build first)

| # | Build | Effort | Unblocks |
|---|---|---|---|
| **1** | **C1 machine metrics** (score the 63 IPVV C1s — proves the C1 contract) | medium | the C1 layer is validated agnostically |
| **2** | **ArgumentProposal schema + validator** (from IPVV's LOGICAL-ARGUMENT files) | medium | the argument layer is validated |
| **3** | **`validate_layers.py`** (cross-layer, per-passage pass/fail) | medium | the meta-contract |
| **4** | **`contracts/` directory** (freeze schemas + validators + spec index) | medium | future-text onboarding |
| **5** | **Onboard a 2nd text** (Tantrāloka or Spandakārikā) through the contract | large | proves the contract generalizes |

**The critical path:** #1 (C1 metrics) and #2 (argument schema) first — they close the two validation
gaps. Then #3/#4 freeze them. Then #5 proves it generalizes.

---

## 5. The "any text" guarantee (what this actually achieves)

Once the contract is frozen:
- **A new text is validated identically to the IPVV** — the IPVV is the gold standard the thresholds
  were calibrated on.
- **Nothing is silently unvalidated** — every layer's output is a typed object that must pass its
  validator.
- **The ML consumes guaranteed shapes** — the argument/cluster/provenance loaders never guess; the
  contract guarantees the fields.
- **The validation IS the supervision** — the scored C1, resolvable arguments, typed provenance are
  exactly the training data the ML learns over.

So the IPVV does double duty: it's the **reference edition** (the content) AND the **calibration corpus**
for the agnostic contract (the process). Future texts inherit both.

---

## 6. Bottom line

Use the IPVV as the **gold standard** — drive it through every layer, validated. From what works on it,
**freeze the agnostic contract** (schemas + validators + specs, content-independent) into a `contracts/`
directory. Then any future text follows that frozen contract mechanically, validated identically to the
IPVV, and the validation doubles as the ML supervision substrate. The immediate builds: **C1 machine
metrics** (#1) and **ArgumentProposal schema + validator** (#2) — these close the two gaps that keep the
contract from being complete, and they're proven on the IPVV before being frozen.

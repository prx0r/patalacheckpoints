# FULL AUDIT — THE TRUTH-ENGINE DOC SET (what's there, what's reusable, what's missing)

*2026-08-12. A complete inventory of the truth-engine's `docs/active/` set (22 docs), read in full, with
what each contains, what is reusable for Pāṭala, and what is missing. This answers "are we missing
anything important" and prevents re-inventing existing machinery.*

---

## 1. The canonical locations (dedup)

- **Runtime code:** `/root/projects/.meta/misc/truth-engine/` (canonical) = `/root/projects/clean/` (mirror)
- **Docs:** `/root/projects/.meta/misc/truth-engine/docs-active/` = `/root/projects/clean/docs/active/`
- **The FATHERFUCKER/ subdirs are stale copies** — ignore them.

---

## 2. THE 22 DOCS — the full inventory (all read)

### A. The DESIGN core (what the engine IS)

| Doc | What it contains | Reusable for Pāṭala |
|---|---|---|
| **`TRUTHMAP-PURPOSE.md`** | the two layers: (1) Sanskritree formal-proof, (2) truth-map evidence tracking | the 2-layer mental model; "the boundary between formalizable and not is itself a finding" |
| **`TRUTHMAP-REDESIGN.md`** | the D1–D5 discrimination cascade + B1–B6 branches + EIG question selection | the *eliminative-question* method (maps to Pāṭala's questionnaire); the ontology (F1–F8/D/B) does NOT fit Pāṭala |
| **`TRUTHMAP-PROGRESS.md`** | the codebase status + doc quality ratings | confirms what's built; the "don't trust docs, check code" warning |
| **`TRUTHMAP-ARGUMENT-FABRIC.md`** | the argument-fabric graph (source→claim→gate→argument→crux→candidate→state-of-play) | **the AIF-style graph — directly relevant to Pāṭala's ARGUMENT layer** |

### B. The Nyāya framework (the BEST asset — the user is right)

| Doc | What it contains | Reusable |
|---|---|---|
| **`TRUTHCHANGES6.md`** | **THE Nyāya spec**: 4 pramāṇas, vyāpti, 5 hetvābhāsas, nigrahasthāna (22 defeat-points), tarka falsifier generation, the 5-member syllogism | **the definitive gate design — this is what `/verify/claim-semantic` should implement** |
| **`TRUTH-TEST.md`** | the test protocol: known-truth + adversarial tests, gate validation, dimension tracking, end-to-end | **the test template for the gate + propagation** |
| `truthchanges5.md` | (refutation-led provenance) | the "numbers are summaries, not verdicts" principle |
| `TRUTHCHANGES8.md` | (further changes) | partial |
| `TRUTHCHANGES.md` | (the original changes) | superseded by 5/6/8 |

### C. The objects (RO / EO — the data model)

| Doc | What it contains | Reusable |
|---|---|---|
| **`RO-v2.md`** | the **Research Object** spec: themed passage extraction, per-passage pramāṇa + hetvābhāsa_check + falsifier, versioning, validation rules (R01–R10) | **the RO = Pāṭala's themed-passage object; the gate integration is exactly what Pāṭala's argument layer needs** |
| **`EO-v2.md`** | the **Essay Object** spec: the 5-member syllogism + candidates with live/weakened/defeated status | **the mature form of Pāṭala's ArgumentProposal + EssayPlan** |
| `ENQUIRY-PIPELINE.md` | the 4-pass orchestration: sweep → contentions → gate → ingest → probe → propagate → essay-seed | **the end-to-end pipeline design — maps to Pāṭala's phases** |

### D. The audits / reviews (what was wrong)

| Doc | What it contains |
|---|---|
| **`truthreview.md`** | the lead-agent audit: 3 state layers (runtime/argument/editorial), the "make argument state primary" principle, the required build queue |
| **`truthadvanced.md`** | the deeper audit: the Claim v3 schema (posterior_targets vs argument_targets), the P0 ingestion pipeline |
| `HANDOVER-SESSION-2026-07-26.md` | the architecture decisions (5 layers, refutation-led, not a Bayesian oracle) |

### E. The meta / planning

| Doc | What it contains |
|---|---|
| `TRUTHPLAN.md`, `ROADMAP.md`, `SCALE-PLAN.md` | the plans (stale — pieces now exist) |
| `ONBOARDING.md`, `REF.md`, `VISION.md` | the reading order + reference (stale) |
| `TRUTHMAP-PRODUCTION-HARDENING.md` | the production hardening |

---

## 3. THE KEY FINDING — what we have that Pāṭala HASN'T wired

The single most important asset is the **Nyāya gate** (`scripts/nyaya-truthmap-gate.py`, 680 LOC) +
its design (`TRUTHCHANGES6.md`) + its tests (`TRUTH-TEST.md`). **Pāṭala has NOT wired it.**

My `argument.py` has a `gate: Optional[dict]` field — but it's a **slot**. Nothing calls the real gate.
The docs reference it; no code runs it. This is the gap.

**What the gate provides (from `TRUTHCHANGES6` + the 680-LOC code):**
- **4 pramāṇas** (pratyakṣa/anumāna/upamāna/śabda) → the correct evidence taxonomy
- **5 hetvābhāsas** (savyabhicara/viruddha/asiddha/satpratipaksa/badhita) → the fallacy detector
- **tarka falsifier generation** (prasaṅga/arthāpatti) → every claim needs a falsifier
- **gate outcomes** that cap the Bayesian LBF (accepted / accepted_with_penalty / needs_review / hollow / refuted)
- **satpratipaksa** = the counter-balanced-claim detector = literally `discover_counterevidence`

---

## 4. WHERE THIS FITS THE DUAL-AGENT VISION (the natural links)

| Vision phase | The truth-engine asset | Pāṭala use |
|---|---|---|
| **Phase 6 — semantic verification** | the Nyāya gate (hetvābhāsa + falsifier) | **`/verify/claim-semantic`** — the deterministic gate deciding `can_update_posterior` |
| **Phase 6 — counterevidence** | `satpratipaksa` (counter-balanced) + `badhita` (overtidden) | **`/discover-counterevidence`** |
| **Phase 8 — workbench** | "attack this interpretation" | the gate IS the structured critic |
| **Phase 9 — adversarial review** | nigrahasthāna defeat-tracking | the adversarial peer-review critic |
| **Phase 4 — argument gold** | the 5-member syllogism (EO) | the gold argument structure |
| **CP4 — argument layer** | `RO-v2` + the gate | the RO → gate → claim ingestion path |

---

## 5. WHAT'S MISSING (the honest gaps)

1. **The Nyāya gate is unwired in Pāṭala.** `argument.py.gate` is an empty slot. This is the #1 gap.
2. **The claim schema is fragmented.** Pāṭala has Claim-v3 (mine) + RO-v2/EO-v2 (truth-engine) — not unified.
3. **No pramāṇa field** on Pāṭala's claims (the 4-type evidence taxonomy is absent).
4. **No falsifier-required enforcement** in Pāṭala (the gate's tarka step).
5. **No `discover_counterevidence`** (satpratipaksa exists in the gate, not wired).
6. **The propagation engine's ontology (F1–F8/D1–D5/B1–B6) does NOT fit Pāṭala** — per
   `TRUTHENGINE_TO_PATALA_MAPPING.md`, do NOT port it; reuse the mechanisms, reject the ontology.

---

## 6. THE RECOMMENDATION (the honest next move)

The user is right: the Nyāya gate is the best asset. The highest-value, honest integration is:

**Wire the real Nyāya gate as `/verify/claim-semantic`** — port `nyaya-truthmap-gate.py`'s hetvābhāsa +
falsifier + pramāṇa logic onto Pāṭala's claims, so:
1. a claim's `gate` field is **filled by the real engine**, not an empty slot
2. `can_update_posterior` is enforced (the "never blur MACHINE_PROPOSED/ACCEPTED" rule, made real)
3. `satpratipaksa` becomes `discover_counterevidence`
4. the pramāṇa taxonomy + falsifier-required become the claim contract

This fits the vision's Phase 6, uses the best existing machinery, and replaces the honest gap (an empty
gate slot) with the real enforcement. It is my lane (the derivation/verification layer).

---

## 7. BOTTOM LINE

The truth-engine doc set is a **mature, battle-tested design** — and the Nyāya gate is the best piece.
We've now read all 22 docs and know exactly what's reusable. The honest gap is that Pāṭala has the gate's
*container* (the `gate` field) but not its *engine*. Wiring the real gate is the clear, high-value move
that fits the vision and uses the best asset we have.

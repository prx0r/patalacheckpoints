# ML ↔ PĀṬALA ALIGNMENT — every ML artifact maps onto existing types + the truth engine

*2026-08-12. The rule going forward: **nothing the ML lane builds may invent parallel notions.** Every
ML artifact must map onto (a) the existing Pāṭala types (`translation.ts`, `primitives.ts`, `lib/verify.ts`)
and (b) the truth-engine's Bayesian scoring. This doc is the alignment contract — it shows each ML concept
and the existing type/notion it uses, so the data stays auditable and in-system.*

---

## 0. The three existing notion-systems (the ground truth everything maps to)

**1. Pāṭala's evidence types** (`data/corpus/translation.ts`):
```
EvidenceVerification = verified | locator_unverified | quote_unverified | resource_missing
EvidenceRole         = supports | contradicts | defines | dates | identifies | quotes | parallel | commentary
EvidenceUse          = { evidence_id, role, note }
```

**2. Pāṭala's epistemic primitives** (`data/corpus/primitives.ts`):
```
EpistemicState = machine_proposed | human_proposed | checked | expert_reviewed
               | editorially_accepted | disputed | rejected
Certainty      = certain | probable | possible | uncertain
Origin         = machine | editor | scholar | institution
```

**3. The deterministic verify floor** (`lib/verify.ts`):
```
verifyQuote · verifyClaimStructure · traceDependency · findCounterevidence
```

**4. The truth-engine Bayesian scoring** (`truthengine-propagation.py`):
```
weighted_lbf = w_rel × w_map × w_dep × w_aux × log_bayes_factor
w_dep        = 1 / (1 + alpha·n_prior)     ← paradigm-dependence discount
log_odds update:  posterior += weighted_lbf
```

---

## 1. The alignment table (every ML concept → the Pāṭala/truth-engine notion)

| ML concept (my work) | Maps to (existing) | How |
|---|---|---|
| **provenance 4-level** (RESOLVES/AUTHENTIC/RELEVANT/SUPPORTS) | `EvidenceVerification` | RESOLVES→`verified`; AUTHENTIC→`quote_unverified` cleared by verifyQuote; RELEVANT/SUPPORTS→`EvidenceRole` |
| **provenance relation** (ENTAILS/SUPPORTS/QUALIFIES/CONTRADICTS) | `EvidenceRole` | map onto supports/contradicts (+ qualifies) — no new enum |
| **claim strength** (WELL_SUPPORTED/PLAUSIBLE/...) | `Certainty` + truth-engine Bayes | strength = Bayesian posterior mapped to `certain/probable/possible/uncertain` |
| **claim status** (MACHINE_PROPOSED/REVIEWED/...) | `EpistemicState` | MACHINE_PROPOSED→`machine_proposed`; REVIEWED→`checked`; ACCEPTED→`editorially_accepted` |
| **ArgumentProposal** | `TranslationDecision` shape | mirrors it: source_span_ids + evidence + status + review |
| **Argument evidence** | `EvidenceUse` | {evidence_id, role, note} — the exact type |
| **C1 metrics** | `EvidenceVerification`-style | each metric's pass/fail is a verification state |
| **Bayesian claim scorer** | truth-engine `weighted_lbf` | port `truthengine-propagation.py` as the derived scorer |

**The rule:** if an ML artifact introduces a concept that has no mapping in the table above, it's either
(a) a genuinely new notion (rare — flag it), or (b) a re-invention (reject it and use the existing type).

---

## 2. The Bayesian claim-strength mapping (the key alignment)

The truth engine gives a **derived number**; Pāṭala has `Certainty` as a **label**. The bridge:

```
truth-engine posterior (0..1)  →  Pāṭala Certainty  →  Pāṭala claim-strength
  0.85+  →  certain           →  FORMALLY_VALID_GIVEN_ENCODING (Lean) or WELL_SUPPORTED
  0.65-0.85  →  probable       →  WELL_SUPPORTED / PLAUSIBLE
  0.45-0.65  →  possible       →  PLAUSIBLE
  < 0.45  →  uncertain         →  SPECULATIVE
```

**This is the auditable strength:** a claim's `WELL_SUPPORTED` is NOT a hand-label — it's the Bayesian
posterior (weighted_lbf over its premises) mapped to `Certainty`. The essay cites the number's origin:
`weighted_lbf = w_rel(0.9) × w_map(0.8) × w_dep(0.66) × w_aux(0.7) × lbf(1.2)` → posterior 0.72 →
`probable` → `WELL_SUPPORTED`. **Fully auditable, fully Bayesian, fully in-system.**

---

## 3. The C1 metrics → auditable alignment

My C1 machine metrics (novelty, localness, no_anachronism, boundary, hedge, term_quality) each produce a
**verification state**, not just a number:

```
metric → { score, threshold, pass }
  pass  → the C1 is "verified" for that dimension (maps to EvidenceVerification: verified)
  fail  → flagged (maps to: quote_unverified / resource_missing — needs human review)
```
So the C1 metrics double as **the C1's auditable verification record** — consistent with how Pāṭala
verifies decisions/evidence. A C1 that passes all metrics is `checked` (EpistemicState); a human review
can promote it to `expert_reviewed`.

---

## 4. The ArgumentProposal → Pāṭala Decision shape

The `ArgumentProposal` (from the corrected review) mirrors `TranslationDecision` so it reuses the same
audit machinery:

| ArgumentProposal field | TranslationDecision field |
|---|---|
| `claim` | `claim` |
| `source.passage_id` + `immutable_id` | `source_span_ids` |
| `evidence_chain` (L1/L2/C1/IA) | `evidence` (EvidenceUse[]) |
| `inference.scheme` | `method` (DerivationMethod) |
| `status` (MACHINE_PROPOSED...) | `status` (DecisionStatus) + `editorial_status` (EpistemicState) |
| `strength` (derived) | `certainty` (Certainty) |

So an argument is **auditable exactly like a translation decision** — a resolvable path, evidence roles,
review state, derived certainty. No new audit machinery needed.

---

## 5. What this guarantees (the "usable and auditable" requirement)

1. **Usable:** every ML artifact uses the existing `EvidenceVerification`, `EvidenceRole`, `Certainty`,
   `EpistemicState`, `EvidenceUse` types — so the API/MCP and the reader can consume it without new
   code.
2. **Auditable:** every artifact carries a resolvable path (passage → `/api/resolve` → Sanskrit), a
   verification state, and a Bayesian-derived strength whose inputs (the weights) are recorded.
3. **Aligned:** nothing re-invents Pāṭala's notions; the argument mirrors `TranslationDecision`, the
   strength maps `Certainty`, the status maps `EpistemicState`.
4. **Truth-engine-integrated:** the Bayesian scorer is a *port* of `truthengine-propagation.py`, not a
   new system — the `weighted_lbf` formula IS the strength source.

---

## 6. The rule for building going forward (enforce this)

> **Before any ML artifact is "done," it must have a row in the §1 alignment table.** If it doesn't map
> onto an existing Pāṭala type (EvidenceVerification/EvidenceRole/Certainty/EpistemicState/EvidenceUse)
> or a truth-engine notion (weighted_lbf/posterior), either reuse the existing type or explicitly flag
> it as a new notion for review. No parallel systems, no invented enums where one exists.

---

## 7. The immediate application (my in-flight work, aligned)

- **C1 metrics** → each metric is an `EvidenceVerification`-style state; a passing C1 is `checked`.
- **Claim strength** → Bayesian posterior mapped to `Certainty`, NOT a hand-label.
- **ArgumentProposal** → mirrors `TranslationDecision` + uses `EvidenceUse`.
- **Provenance 4-level** → maps onto `EvidenceVerification` + `EvidenceRole` (no new enum).
- **ClusterProposal** → the membership strengths + edge evidence become `EvidenceUse[]` on the argument
  it feeds.

Everything I build from here maps onto this table. That's the alignment that makes the ML data usable,
auditable, and in-system — with the truth engine's Bayesian scoring as the strength source.

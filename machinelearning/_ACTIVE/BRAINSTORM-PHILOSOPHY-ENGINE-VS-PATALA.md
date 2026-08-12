# BRAINSTORM — the Philosophy-Engine reviews vs. Pāṭala's current implementation

*2026-08-12. High-level synthesis of two imported architecture reviews (from the sanskritree R2 bucket)
against what we have actually built. Not a spec — a brainstorm: where our implementation already aligns,
where the reviews would upgrade it, and what the honest next move is given our frozen gate + gold +
anti-theatre doctrine.*

**Sources imported:**
- `PHILOSOPHY-ENGINE-ARCHITECTURE-REVIEW.md` — the "one abstraction layer too shallow" critique + the
  13-object ontology + the `Sπ(G)` profile-relative evaluation + crux-as-outcome-sensitivity.
- `PHILOSOPHY-ENGINE-INFRASTRUCTURE-REVIEW.md` — the "delegate to existing infra (py-aspic/xAIF/oAMF),
  Pāṭala owns the IR" correction + the 12-object + EvaluationProfile + the build order.

---

## 0. THE HEADLINE

**Both reviews are remarkably close to what we already designed — they largely VALIDATE our
DebateFrame/SemanticAlignment direction, then push it one level deeper.** Our `SEMANTIC-COMMENSURABILITY.md`
already contains the review's central insight ("alignment before contradiction", argument-under-a-frame).
The reviews add: (1) **Commitment** (who asserts vs. quotes vs. attributes-to-opponent), (2) **strict vs
defeasible** inference as a separate dimension, (3) **Attack vs Defeat** as separate objects, (4)
**EvaluationProfile-relative** outcomes, and (5) **Crux as outcome-sensitivity** (a graph problem, not an
authored label). The second review is a strong **"don't reimplement the wheel"** discipline that matches
our own anti-theatre + don't-build-the-essay-layer guardrails.

---

## 1. WHERE WE ALREADY AGREE (the reviews validate our design)

| Review idea | Our existing implementation | Verdict |
|---|---|---|
| **alignment before contradiction** | `SEMANTIC-COMMENSURABILITY.md` (the 3 relation types, the decision ladder) | ✅ already core |
| **argument-under-a-frame** | `DebateFrame` (already in `gold002.py`) | ✅ already built |
| **semantic alignment as first-class** | `SemanticAlignment` (in `gold002.py`, `CHECKPOINTS.md` #8) | ✅ already built |
| **valid ≠ sound ≠ justified ≠ historically attributed ≠ true** | the whole doctrine (`AGENTS-DOCTRINE.md`, the 5 claims) | ✅ already gospel |
| **UNDERDETERMINED is a first-class outcome** | the gate's `needs_review`/abstain + `abstention` metrics | ✅ aligned |
| **don't collapse argument_strength into one number** | `strength.py` (explicitly uncalibrated, ordinal, `audit_trace`) | ✅ aligned |
| **global knowledge base must be non-explosive** | `aifgraph.py` (conflict nodes, not explosion) | ✅ aligned |
| **don't build the whole essay/argument stack** | the guardrails (CP4 gold first) | ✅ aligned |

**The second review's central architectural boundary is exactly our own:** *"Pāṭala owns the
philosophical intermediate representation + provenance layer; delegate standard argumentation computation
to existing infra."* We have been building the IR (gold + DebateFrame + SemanticAlignment + aifgraph) and
have NOT been reimplementing ASPIC+/Dung semantics. Good.

---

## 2. WHERE THE REVIEWS WOULD UPGRADE US (the genuinely new ideas)

These are the real additions — things we do not yet have. Ranked by leverage:

### 2a. `Commitment` (who asserts vs. quotes vs. attributes) — HIGHEST value
Our gold has an `OBJECTION` kind and a `Defeater` type, but not a first-class "this is attributed to the
**opponent**, not to Abhinavagupta." This is the exact historical-philosophy error the review flags:
> turning "the opponent might say X" into "Abhinavagupta's position is X."

Our corpus is full of this — the C1 digest shows the Buddhist pūrvapakṣa throughout (V1-F, V1-upoddhata-*,
V3-I). **A `Commitment` object (ASSERTS/DENIES/PRESUPPOSES/ASSUMES_FOR_ARGUMENT/ATTRIBUTES_TO_OPPONENT/
QUOTES/RECONSTRUCTED) would directly improve ARG-003 (the reductio — where Abhinava *assumes* the Buddhist
view for the reductio) and ARG-005 (the ambiguous V3-I — where two readings differ on who commits to what).**

### 2b. `Attack` vs `Defeat` (the objection exists ≠ the objection succeeds)
Our `Defeater` conflates these. The review: store the attack as data; whether it **defeats** is derived
under an EvaluationProfile. This is a cleaner ontology AND a natural place for the Nyāya gate to plug in
later (the gate decides whether an attack defeats, per regime).

### 2c. strict vs defeasible as a separate dimension
Our `scheme` enum (TRANSCENDENTAL/REDUCTIO/etc.) mixes "what kind of reasoning" with "how strong." The
review separates them. We have a `Defeater` concept but not a clean STRICT/DEFEASIBLE flag per inference.
**Cheap to add to the gold schema; clarifies ARG-001 (transcendental = defeasible) vs a hypothetical
formal step (strict).**

### 2d. `EvaluationProfile` (outcomes are relative to a regime)
Our `DebateFrame` + `SemanticAlignment` set up the frame, but the review's `Sπ(G)` — *the same argument
graph evaluated under Śaiva vs Buddhist vs shared-debate regimes gives different outcomes* — is the 
cross-tradition payoff. This is the natural evolution of our gate's `tradition` field into a first-class
profile. **Not urgent for CP4, but the destination for viruddha-as-graph-op.**

### 2e. `Crux` as outcome-sensitivity (the graph problem, not an authored label)
The review's sharpest insight: a crux is "a minimal set of disputed dependencies whose change alters the
evaluated status of q." This turns "what's the real disagreement" into a **computable graph problem** with
crux-centrality. **This is CP4-adjacent future work** — it needs the argument DAGs first, which is exactly
what the gold is building toward.

---

## 3. WHERE THE REVIEWS WOULD SIMPLIFY / RESTRAIN US

The second review is a strong **anti-scope-creep** document that matches our guardrails:
- **Do NOT adopt py-aspic/xAIF as Pāṭala's persistent schema** — use them as evaluators/adapters.
- **Do NOT reimplement computational argumentation** — delegate to py-aspic (ASPIC+), ALIAS (Dung), xAIF (interchange).
- **`EvaluationState` is derived, not canonical data** — persist the profile, not the result.
- **`Warrant` folds into `InferenceRule`** (don't need two objects).
- **No quantitative scores as primary epistemology** (don't adopt ACAL/QBAF scoring).

All of these match our anti-theatre doctrine. The reviews **reaffirm our decision not to build a bespoke
Bayesian/argumentation engine before the gold exists** — which is exactly the guardrail our `AGENTS-DOCTRINE`
and `CHECKPOINTS-ML.md` already enforce.

---

## 4. THE HONEST GAP (where the reviews outrun us — and why that's OK)

The reviews describe the **finished** philosophy engine: profile-relative evaluation, crux extraction,
counterfactual intervention, Scholar Workbench graph UI. **We do not have the substrate for any of that
yet.** The reviews themselves acknowledge the build order:
> PHASE 0: finish the IPVV scholarly substrate. PHASE 1: implement the 12-object IR (no clever AI).
> PHASE 2: manually encode 5–10 disputes.

**Our CP4 Argument Gold IS Phase 2.** We are exactly where the review says to be. The gap is not a
failure — it's the correct sequencing. What the reviews would add to our *immediate* gold work is modest:
**a `Commitment`-style field** (who asserts each node) and **an `Attack` vs `Defeat` split** in the gold
shape. Everything else (EpistemicRegime, EvaluationProfile, Crux, the py-aspic/xAIF adapters) is
correctly LATER than the gold.

---

## 5. RECOMMENDED NEXT MOVES (brainstorm — not yet a commitment)

1. **Adopt `Commitment` into the gold schema now** — the cheapest, highest-value upgrade. Add a
   `commitment` (or `speaker`/`force`) field to each gold node: ASSERTS / ATTRIBUTES_TO_OPPONENT /
   ASSUMES_FOR_ARGUMENT / CONCEDES / QUOTES. This fixes the pūrvapakṣa-attribution problem the whole
   corpus is vulnerable to, and directly strengthens ARG-003 (reductio) and ARG-005 (ambiguous).
2. **Split `Defeater` into `Attack` (data) + `Defeat` (derived)** in the gold shape — cleaner, and the
   Nyāya gate becomes the future "decides whether an attack defeats" layer.
3. **Add a `strictness` (STRICT/DEFEASIBLE) flag** to gold inferences — cheap, clarifies ARG-001.
4. **Park** EpistemicRegime, EvaluationProfile, Crux-as-outcome-sensitivity, and the py-aspic/xAIF/ALIAS
   adapters as **the documented future of CP4/CP5** — NOT now. They need the argument DAGs that the gold
   (5 real arguments) is building toward.
5. **Keep the anti-theatre boundary:** when we DO reach the profile-relative evaluation, use py-aspic as
   the evaluator (don't reimplement ASPIC+), persist profiles not states, and never report a quantitative
   score as truth.

---

## 6. THE ONE-SENTENCE CARRY-FORWARD

**Both reviews validate our DebateFrame/SemanticAlignment direction and correctly sequence the work: our
CP4 Argument Gold is their Phase 2, so the immediate upgrade is to add `Commitment` (who asserts vs
attributes-to-opponent) and split `Attack`/`Defeat` into the gold shape — while parking the
profile-relative evaluation, crux extraction, and py-aspic/xAIF adapters as the documented future, to be
built only once the gold's argument DAGs exist. This keeps us on the anti-theatre path: build the gold
first, then delegate standard argumentation to existing infra, then compute the genuinely Pāṭala-specific
layer (commitment, alignment, regimes, cruxes) on top.**

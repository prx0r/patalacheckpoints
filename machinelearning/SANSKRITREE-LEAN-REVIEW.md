# SANSKRITREE LEAN / FORMAL-PROOF — review (what's useful for Pāṭala)

*2026-08-12. Review of the Sanskritree formal-proof work (THESIS.md, proofenginge.md, proof_engine/,
FORMALISATION_SCHEMA.md). The honest question: what here is genuinely usable for Pāṭala, and what is
aspirational?*

---

## 1. The thesis (THESIS.md) — the vision, and its honest status

**The idea is excellent and directly Pāṭala-relevant:** a "truth compressor" that maps Sanskrit
philosophical claims to Lean 4 types, outputting `PROVED / OUTSIDE_FORMAL / HOLLOW`. Three commitments
that align perfectly with Pāṭala's honesty principle:
- "The goal is **honesty, not proofs**" — HOLLOW and OUTSIDE_FORMAL are correct results.
- "The boundary between what can and cannot be formalized is itself a finding."
- "We do not bias toward provability" — no `sorry`, gaps are explicit.

**Its architecture** (the hybrid oracle):
```
Lean 4 = formal oracle (proves; no sorry)
Human  = semantic oracle (faithfulness to source)
LLM    = decomposition oracle (sayability, template, decompose — NEVER proof)
```

**The status (honest):** this is a **real implemented pipeline** (`proof_engine/` has 18 modules —
algorithm.py, lean_checker.py, fol_lean_bridge.py, decomposition.py, phase1_dharmakirti.py,
phase1_nyaya.py, bnf.py, ground_truth.py, validation.py, registry.py, db.py). It targets **Dharmakīrti
PV III** + **Nyāya** first; the planned bootstrap is **Tarkasaṃgraha** (padārtha). The Lean checker has
a **real Pantograph** path with a `FALLBACK_KNOWN` table when Lean is unavailable.

---

## 2. What's genuinely useful for Pāṭala (the reusable pieces)

### 2a. The `fol_lean_bridge.py` (125 LOC) — the Navya-Nyāya → Lean mapping
This is the most directly reusable piece. It maps the NN operators to Lean types:
```
abheda      → a = b                (identity)
vyapti      → ∀ x, Hetu x → Sadhya x   (universal concomitance)
sambandha   → the relation
avacchedaka → the limitor
```
**Why it matters for Pāṭala:** Pāṭala's argument layer uses the SAME Nyāya concepts (vyāpti, the 5-member
syllogism, hetvābhāsa). This bridge gives the formal encoding for the *strictly-formalizable subset* of
Pāṭala's arguments — exactly the "FORMALLY_VALID_GIVEN_ENCODING" verdict the external review wanted,
instead of a vague "PROVED."

### 2b. The `bnf.py` / NNExpr grammar (the gate)
The Navya-Nyāya expression grammar (`TID_N[Trad]`, `vyapti(a,b)`, `abheda`, etc.) — validates LLM
formalization output before it reaches Lean. This is the "the model can't fabricate a parse" guard.

### 2c. The tradition-scoped term registry (the key design)
**"Same IAST, different tradition → different formal node."** `pramāṇa` in Nyāya ≠ `pramāṇa` in
Dharmakīrti. This is EXACTLY Pāṭala's attributed-contexts requirement (the reviewer's "Abhinavagupta
asserts X ≠ Ratié interprets X as Z" — epistemic worlds). The term registry is a concrete implementation
of that.

### 2d. The Kāṇḍa system (from Pāṇini) — the epistemic-layering
```
Kāṇḍa 1 (siddha)   axioms/definitions, globally visible, no proof
Kāṇḍa 2 (vidhi)    derivations, must prove or decompose
Kāṇḍa 3 (asiddha)  FDE/circular/abhāva, hidden, human promotion for bridges
```
This maps cleanly onto Pāṭala's review-state ladder (DETERMINISTIC_FACT / MACHINE_PROPOSED /
HUMAN_REVIEWED / ACCEPTED). The Kāṇḍa system is a formal version of "some things are axioms, some are
derived, some need human adjudication."

### 2e. `lean_checker.py` — the real proof-checking path
A working `pantograph_check` (Lean4 REPL) + `lake env lean` + the `FALLBACK_KNOWN` table. This is the
actual "prove it in Lean" machinery — the thing Pāṭala's `FORMALLY_VALID_GIVEN_ENCODING` verdict would
use.

---

## 3. What is aspirational (NOT yet usable, be honest)

- **The full cross-tradition graph** (centre nodes, bridges, divergence nodes) — the vision, not built.
- **The "formal structure of consciousness = formal structure of physics" experiment** (Phase 3) — a
  research goal, not an artifact.
- **PROVED for most claims** — the reality is that Lean proves *definitions* (Dharmakīrti's pratyakṣa as
  Kāṇḍa-1 stipulation) but **structural/philosophical claims remain UNPROVED** until the Lean foundation
  expands. THESIS says this honestly.
- **Nāgārjuna's catuskoṭi FDE layer** — planned, not built.

---

## 4. How this fits Pāṭala (the natural integration)

The external review's correction was: **Lean is an optional analytical instrument for a strict subset —
`FORMALLY_VALID_GIVEN_ENCODING`, not the spine.** The Sanskritree proof engine is precisely that
instrument, already built. So:

| Pāṭala need | Sanskritree asset | Use |
|---|---|---|
| `FORMALLY_VALID_GIVEN_ENCODING` verdict | `lean_checker.py` + `fol_lean_bridge.py` | the "prove" step for strictly-formalizable subarguments |
| argument inference-scheme formalization | `fol_lean_bridge.py` (vyāpti→∀, abheda→=) | encode Pāṭala's argument schemes in Lean |
| attributed contexts / no false mergers | the tradition-scoped term registry | the epistemic-worlds requirement |
| review-state ladder | the Kāṇḍa system | axioms vs derivations vs human-promotion |
| no hallucinated formalization | `bnf.py` NNExpr grammar | validate LLM formalization before Lean |

---

## 5. The honest caveat (from the external review, reinforced here)

**Lean proves the formal claim, NOT that the formal claim faithfully encodes the Sanskrit.** The
Sanskritree thesis itself says the human is the "semantic oracle." So Pāṭala should use this engine ONLY
for the `FORMALLY_VALID_GIVEN_ENCODING` verdict on a strict subset — never as the whole truth engine. The
Kāṇḍa-1-vs-2 distinction (axioms vs derivations) is exactly the boundary where human judgment must sit.

---

## 6. The bottom line

There **is** cool, genuinely-reusable stuff in the Lean area — but it's a **formalization instrument for
a strict subset**, not a replacement for Pāṭala's verification or evidence machinery:

1. **`fol_lean_bridge.py`** + **`lean_checker.py`** = the real `FORMALLY_VALID_GIVEN_ENCODING` engine.
2. **The tradition-scoped term registry** = a concrete implementation of Pāṭala's attributed-contexts.
3. **The Kāṇḍa system** = a formal version of Pāṭala's review-state ladder.
4. **`bnf.py` NNExpr grammar** = the no-fabricated-formalization guard.

These slot into Pāṭala's ARGUMENT → VERIFICATION layer as the *strict-formal subset* the external review
described — **complementing** the Nyāya gate (semantic verification) and the Bayesian primitive (evidence
strength), not replacing them. The full cross-tradition formal graph is the vision, not yet a usable
artifact.

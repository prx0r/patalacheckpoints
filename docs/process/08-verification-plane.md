# 08 — THE VERIFICATION PLANE (external methods test Pāṭala; they never define Pāṭala truth)

*Part of `docs/process/README.md`. This is the **two-plane architecture**: a PRODUCTION COMPILER (the
factory + epistemic core) and a VERIFICATION PLANE (Inspect + atomic verifiers + metamorphic tests +
calibrated abstention) that tests every object from OUTSIDE the graph. The ruling principle: **external
ML methods test Pāṭala; they do not get to define Pāṭala truth.***

Raw research: `source-evidence/docs/tools/docs-cache/layertools-research.md` +
`layertoolsintegration-research.md`.

---

## 1. The two-plane architecture

```text
PRODUCTION COMPILER
SOURCE → T1 → L0 → ARGMAP → L2 → L200 → C1 → THEME → ESSAY → EDUCATION
   │ every object
   ▼
VERIFICATION PLANE  (Inspect AI)
   ├─ deterministic contract scorer
   ├─ semantic scorer (AlignScore / NLI cheap witness)
   ├─ RefChecker-style atomic claim verification
   ├─ FActScore atomic-factual precision
   ├─ metamorphic tests (perturbation/crux)
   ├─ calibrated abstention (conformal)
   └─ certificate emitter
```

## 2. The reusable verification stack (compose, don't invent)

```text
STRUCTURE          StructEval (methodology only)
ATOMIC DECOMP      RefChecker / FActScore
SOURCE↔OUTPUT      AlignScore / NLI
ABSTENTION         conformal prediction / CIC
MUTATION           metamorphic testing (native)
ORCHESTRATION      Inspect AI (the runtime)
```

License notes (from the research):
- **Inspect AI** — MIT, integrate directly (already INTEGRATED).
- **RefChecker** — Apache-2.0 but archived (Apr 2026): pin/fork behind your own interface.
- **FActScore** — MIT: reuse methodology; register Pāṭala objects as the trusted source (not Wikipedia).
- **AlignScore** — MIT: optional local semantic witness.
- **GlossLM** — Apache-2.0 weights: benchmark T1 against the IGT glossing paradigm.
- **StructEval** — Apache-2.0: borrow methodology, not runtime.
- **ByT5-Sanskrit** — weights downloadable but license unclear: don't treat as redistribution-cleared.
- **conformal / metamorphic** — research methods: implement natively.

## 3. The generalized atomic-support evaluator (the core equation)

```
License(O) = supported_upstream_atomic_claims / substantive_atomic_claims_in_output
```
Shared by **L2-License, C1-License, Essay-License, Education-License** — one evaluator, each layer's
explicit permitted dependency set:
```text
source → T1 → L0 → ARGMAP → L200 → C1 → THEME → SYNTHESIS
```

## 4. The cheap→expensive verification ladder

```text
claim
  ↓ deterministic checks
  ↓ AlignScore/NLI cheap verifier
  ↓ obvious PASS/FAIL → record
  ↓ borderline → LLM critic
  ↓ critic uncertain → OPEN / human
```

## 5. RefChecker-style decomposition (per layer)

```text
L2 sentence → atomic semantic units → each licensed by SOURCE+T1+ARGMAP → ENTAILED/UNSUPPORTED/CONTRADICTED
C1 sentence → atomic claims → L200/source support
Essay sentence → atomic claims → theme/synthesis support
Education claim → essay support
```

## 6. T1 as Interlinear Glossed Text (the right benchmark, not BLEU)

```text
T1 benchmark = segmentation F1 + token↔gloss alignment + gloss accuracy + lexical-sense accuracy
             + morphology contribution + abstention
```
Learned linguistic witness stack: `Vidyut/Heritage (deterministic) → ByT5-Sanskrit (learned) → LLM T1
agent (semantic)`. Disagreement is useful (2/3 consensus = strong; all-disagree = OPEN).

## 7. Metamorphic testing (native)

Use the existing perturbation/crux machinery: invariant-preserving perturbations of inputs must not
change the object's valid conclusions. This is the mutation suite the epistemic core already partially
has (see `07-ml-epistemic-core.md` / agent1atlas NAT tests).

---

## 8. How it links

```
FACTORY (03) + EPISTEMIC CORE (07)  → produce objects (MACHINE_PROPOSED)
VERIFICATION PLANE (this layer)     → tests them from outside (Inspect + atomic verifiers)
REVIEW (04 human authority)         → human adjudication
CERTIFICATE                         → engineering-validated state
```
The verification plane is the benchmark family's home (TantraFact / ArgumentBench / TranslationBench /
CorroborationBench / PāṭalaQA) — all in `source-evidence/evals/`.

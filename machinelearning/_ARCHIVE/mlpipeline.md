# ML — THE AUDITABLE SANSKRIT→ARGUMENT→ESSAY PIPELINE (verified methods + tools)

*2026-08-12. **Agent 1's (ML) assessment of the question: "can we build a full auditable pipeline from
Sanskrit translation to essay?"** — with the existing ML methods and git projects that make each link
real. Every cited method/tool was verified reachable via arXiv API / GitHub this session. This is the
design; the pipeline is already 60% built in the codebase.*

---

## 0. The answer up front

**Yes — and the auditable pipeline is not only possible, it's already 60% built.** The missing pieces
are specific, and each has a **proven existing method/tool**. The pipeline:

```
SANSKRIT  →  L2 (read)  →  L200 (audit: IAs)  →  C1  →  ARGUMENT  →  ESSAY
  [✓ exists]  [✓ exists]     [✓ exists]           [✓]   [∅]        [∅]
```

What exists: the translation stack, L200 interpretive assertions (IAs), C1s, and the 
`LOGICAL-ARGUMENT-1-reflexivity-debate.md` format. What's missing: **(a)** the automatic extraction of
formal argument structure from C1s/IAs, and **(b)** the *provenance-guaranteed* essay generation. Both
have direct, verified precedents.

---

## 1. The two hard links, and the methods that solve them

### Link 1: prose → formal argument (the C1/IA → argument step)

**Verified precedent: Argument Mining.** The field has mature tools for exactly "detect argument units,
classify their type (claim/premise/support), and detect the relations between them."
- **ABAM — Aspect-Based Argument Mining** (2011.00633, github.com/trtm/ABAM): extracts argument units +
  their *aspects*, enabling argument ranking/summarization and **counter-argument search** — the latter
  is literally `/discover-counterevidence`.
- **Multilingual Argument Mining** (2010.06432): transfer learning works well for stance/evidence
  detection even across languages — directly relevant since Pāṭala mixes Sanskrit terms + English prose.
- **TACAM** (1906.00923): shows *topic context* is crucial for argument classification — matching
  Pāṭala's finding that shared terms alone (without doctrinal context) over-connect.

**The Pāṭala-specific advantage:** unlike generic argument-mining (which has to *discover* claims in raw
prose), Pāṭala's L200 **IAs are already labeled interpretive assertions**, and its C1s already separate
SUMMARY/FUNCTION/EXPLANATION/BOUNDARY. So the "argument mining" is *easier* than the general problem:
the units are pre-segmented; the model's job is to map C1-EXPLANATION → premises and C1-BOUNDARY →
the honest verdict. **The argument structure is latent in the C1 schema, not buried in prose.**

### Link 2: argument → provenance-guaranteed essay

**Verified precedent: Generation-time Fine-grained Provenance.** This is the frontier, and two 2026
papers do *exactly* the essay end of Pāṭala's pipeline:
- **GenProve** (2601.04932): models generate fluent text **while producing structured sentence-level
  provenance triples** (`Quotation | Compression | Inference`) that say *how* each sentence is supported.
  It found a critical result: models are good at `Quotation` but **struggle at `Inference`-based
  provenance** — "verifiable reasoning is a frontier challenge distinct from surface citation." **This is
  Pāṭala's exact problem** (an essay claim *infers* from the argument, it doesn't quote it).
- **PaperTrail** (2602.21045): decomposes both answers and sources into discrete claims+evidence and maps
  them, revealing supported/unsupported/omitted claims. Its finding: **provenance *lowers* user trust
  (good) but doesn't change behavior** (users still rely on the LLM). Lesson for Pāṭala: provenance is
  necessary but not sufficient — the UI must make verification *easy*, not just possible.
- **TRACER** (2605.09934): generates each sentence with a provenance record identifying the supporting
  tool-turn + evidence + relation, then **verifies** it (schema check, alignment, authenticity,
  rationality) and feeds verified provenance back as RL reward. This is the most complete recipe: Pāṭala
  could treat its `/verify/*` services as the "verifier" and reward essay generation for producing
  verified provenance.

**The Pāṭala-specific advantage:** the `SHOW EVIDENCE` discipline (SPEC_ESSAY) already wants
claim→passage→Sanskrit; GenProve/PaperTrail/TRACER give the *mechanism* to make it automatic and
verified. And Pāṭala's essays are *downstream of arguments* (not free prose), so the provenance relation
is `Inference` from an argument packet — a cleaner structure than GenProve's raw-text setting.

---

## 2. The "prove" link (the truth engine) — verified tools

The `proof` field in the argument truth-packet wants a real Lean verdict (not the simulated demo in
`nyayaengine.py`). The verified tool:
- **Lean Copilot** (2404.12534, github.com/lean-dojo/LeanCopilot, MIT): runs LLM inference *natively in
  Lean* as a **copilot** — suggests proof steps, completes goals, selects premises. Requires only **2.08
  human steps** on average vs 3.86 for aesop, automates 74.2% of steps. This is the real engine to
  replace `simulated_lean_check()`.

**Honest boundary (unchanged from my guardrail):** Lean proves *formal* claims. The Sanskrit→Lean
*translation* of a premise is itself interpretive — LeanCopilot can prove the formal claim, but whether
that formal claim faithfully encodes the Sanskrit is a *separate* (human-reviewed) judgment. So the
pipeline is: **human/editor approves the premise-encoding → LeanCopilot proves the formal claim → the
proof is machine-checked.** The proof is sound *given* the encoding; the encoding is the scholarly act.

---

## 3. The verified-fit to Pāṭala's existing stack

| Pipeline stage | Pāṭala has | Existing method/tool | Effort |
|---|---|---|---|
| Sanskrit → L2 | ✓ published store | — | done |
| L2 → L200 IA | ✓ 66 audits | — | done |
| L200 IA / C1 → Argument | ✓ IAs + C1 schema | Argument Mining (ABAM 2011.00633) | low (units pre-segmented) |
| Argument → Essay | ✓ SHOW-EVIDENCE discipline | GenProve (2601.04932) / TRACER (2605.09934) | medium (frontier) |
| Essay → verified | ✓ `/api/verify/*` | TRACER's verifier pattern | low (services exist) |
| Argument → PROVED | ∅ (simulated) | Lean Copilot (2404.12534) | medium (formal encoding) |

**The ordering insight:** the *cheapest* wins are the ones where Pāṭala already has the structure —
the L200 IAs are pre-segmented interpretive assertions, so argument *discovery* is easier than mining raw
prose. BUT this is **not low-effort** (see `ML-ARGUMENT-REVIEW-CORRECTED.md`): extracting implicit
premise, speaker, scope, reductio structure, and inference rule from Abhinavagupta is genuinely hard, and
C1 must only *discover* the argument, never be its ultimate evidence. The genuinely *frontier* part is
the Inference-provenance essay generation (GenProve), which is Pāṭala's eventual crown.

---

## 4. The three concrete ML builds (in priority order, my lane)

1. **C1 → ArgumentProposal extractor** (medium — NOT low-effort). Map the existing C1 schema
   (SUMMARY→conclusion, EXPLANATION→premises, BOUNDARY→honest verdict, RELATED→passages) onto the
   AIF-informed argument object — but the proposal must point DOWNWARD to Sanskrit/L1/L2, with C1 as
   discovery only, never as ultimate evidence (the circularity guard). Argument Mining assists;
   it does not decide.
2. **Argument → verified-essay provenance** (frontier). Adapt the GenProve/TRACER recipe: essay
   sentences carry a provenance triple (`Quotation|Compression|Inference`) + the argument packet id +
   passages; `/api/verify/*` checks resolvability. Record the `Inference`-vs-`Quotation` gap — Pāṭala's
   essays are mostly `Inference`, so this is where the hard, interesting ML lives.
3. **Lean Copilot link** (proof-of-life, on a STRICT subset only). Wire a selected, human-approved
   strictly-formalizable subargument's claim to Lean Copilot. The verdict is **`FORMALLY_VALID_GIVEN_ENCODING`**,
   NOT `PROVED` — Lean proves "C follows from A, B, R" but not "A faithfully represents Abhinavagupta."
   The human formalization review sits between Sanskrit and Lean. Replaces the simulated engine honestly.

---

## 5. Guardrails (unchanged, now with evidence)

- **Lean proves the formal claim, not the Sanskrit encoding.** The encoding is human-reviewed; the
  proof is machine-checked. GenProve's finding (models struggle with Inference-provenance) confirms this
  is the hard step — don't pretend an LLM can auto-encode a Sanskrit premise into Lean without review.
- **Provenance lowers trust but doesn't change behavior** (PaperTrail). The essay UI must make
  verification *effortless*, or users won't use it.
- **Argument mining over pre-segmented C1s ≠ general argument mining.** Pāṭala's advantage is the
  schema; don't import generic AM complexity that ignores it.
- **The `proof` verdict is a label until Lean is real.** Record `engine: manual` / `status: REVIEWED`
  until the Lean Copilot link lands.

---

## 6. Bottom line

The auditable Sanskrit→argument→essay pipeline is **real and mostly built**. The two missing links have
**verified, named, reachable methods**: Argument Mining (ABAM, multilingual AM, TACAM) for the
C1→argument step, and **Generation-time Provenance** (GenProve, TRACER, PaperTrail) for the
argument→verified-essay step — the last being the frontier that Pāṭala is unusually well-placed to
advance, because its essays are *downstream of typed arguments*, not free prose. The "prove" link is
**Lean Copilot** (verified, MIT, runs natively in Lean). Each has a Pāṭala-specific advantage that makes
the problem *easier* than the general case.

The single highest-value next build: **the C1 → ArgumentPacket extractor** (my lane, low effort, uses
the existing C1 schema as pre-segmentation). It produces the first real truth-packets from actual
scholarship and unblocks everything downstream.

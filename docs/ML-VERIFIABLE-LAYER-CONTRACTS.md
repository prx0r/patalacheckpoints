# ML-VERIFIABLE LAYER CONTRACTS — when a layer is "done correctly" (BRAINSTORM 2026-08-13)

*The goal: for each layer of the canonical stack, define a **machine-verifiable contract** — a set of
deterministic checks (and where meaning is involved, an ML-verified semantic check) that prove the layer
output is correct. These contracts become the **validation gates** in the autonomous factory AND the
**acceptance criteria** in the skills. This is the brainstorm: for each layer, what makes it "done"?

Grounded in the existing validators (`pipeline/*_worker.py`) + the IPVV specs (`translations/_stack/ipvv/specs/`)
+ the locked canonical stack (`handover/agent-2-integration/CANONICAL-LAYER-STACK.md`).*

---

## 0. THE PRINCIPLE

A layer is **DONE-CORRECT** when every one of its contract checks passes AND its ML-verified semantic
check (where meaning matters) passes against the exemplar gold. Two tiers:

- **Tier A — DETERMINISTIC (machine-provable, no model):** structural, provenance, schema, losslessness.
  These are un-cheatable — they are the floor.
- **Tier B — ML-VERIFIED (semantic, benchmarked):** the *meaning* matches the exemplar gold to a
  measured degree. These are MACHINE_PROPOSED until human-adjudicated; they are how we know a layer is
  semantically right, not just well-formed.

**The rule:** a layer may be *BUILT* (Tier A) immediately, but is only *VALIDATED* (per MISSION doctrine)
when Tier B is measured against a hidden gold with an honest metric.

---

## 1. SOURCE

- **Tier A (deterministic):**
  - source text present, resolvable `source_id` (`pt:src:*`), edition/format recorded
  - raw bytes readable; character accounting complete (0 unknown chars under the agreed charset)
  - `source_sha256` stable across re-reads
- **Tier B (ML/semantic):** n/a — source is the ground; nothing to compare against yet.
- **Skill gate:** "I have acquired and verified a lossless, provenance-bound source."
- **Done-correct when:** Tier A passes; registry has an immutable SOURCE object.

## 2. T1 (transliteral word-gloss — THE FLOOR)

This is the first interpretive layer. The exemplar is `01_t1/`, `02_t1/` (the `[and]-GLOSS (IAST)` form).

- **Tier A (deterministic):**
  - token grammar valid: every token is `[and]-GLOSS (IAST)` | `[and]-"GLOSS (IAST)"` | bare connective
  - every IAST token maps to a source span (provenance to SOURCE)
  - every Sanskrit token in the source appears in the T1 gloss (coverage / recall of the passage)
  - no invented gloss: each gloss traces to a real Sanskrit token (no free-floating English)
  - source lossless: T1 reconstructs the source's Sanskrit token set (round-trip)
- **Tier B (ML-verified semantic):**
  - **gloss-correctness**: does each English gloss *mean* the token correctly? (word-sense disambiguation)
    → benchmark: our gloss vs the IPVV T1/L0 exemplar gloss, embedding/translation-similarity per token
  - **abstention-honesty**: an unclear token is left OPEN, never fabricate a confident gloss
- **Skill gate:** "I produced a transliteral gloss where every Sanskrit token is glossed and traceable."
- **Done-correct when:** Tier A (grammar + coverage + lossless) AND Tier B (gloss similarity vs gold above
  threshold, false-certainty below threshold).
- **ML contract metric (proposed):** per-token gloss similarity (embedding) vs exemplar; abstention rate;
  false-certainty rate; token-coverage recall.

## 3. L0 (structured token records FROM T1)

The exemplar is `l0/*.l0.jsonl`, `l0_v1/*.l0.jsonl`; the spec is `SPEC_L0_L1.md` + `l0_schema.json`.

- **Tier A (deterministic):**
  - schema conformant (17 fields, correct enums) — **already proven** (`validate_l0_spec`)
  - P0 lossless (source exactly reconstructible, 0 unknown chars) — **already proven**
  - pure derivation: L0 is a lossless transform of T1 (every L0 record ↔ a T1 token) — no added content
  - provenance: each record's `raw_fragment` re-checks against the T1 chunk
- **Tier B (ML-verified semantic):**
  - **gloss-vs-exemplar**: our `literal_gloss` vs the IPVV exemplar gloss for the same token
    (embedding similarity; abstention on mismatch)
  - **lemma correctness**: our `lemma_iast` vs the exemplar's lemma (string/stem/compound agreement)
  - this is the **semantic-equivalence harness** (`docs/ML-L0-SEMANTIC-EQUIVALENCE-PROPOSAL.md`)
- **Skill gate:** "I produced structured L0 records that are a lossless derivation of T1 and semantically
  equivalent to the exemplar gold."
- **Done-correct when:** Tier A (schema + P0 + derivation) AND Tier B (gloss + lemma similarity vs gold).
- **ML contract metric (proposed):** schema-iso (bool), P0-lossless (bool), per-token gloss/lemma
  similarity, abstention, false-certainty, coverage.

## 4. ARGUMENT MAP (lateral guide)

The exemplar is `pilot/*_ARGUMENT_MAP.md`.

- **Tier A (deterministic):**
  - the argument map names the passage's move (what is at issue), the plan/verse-scheme, and OPEN items
  - every segment it references resolves to a source span / kārikā
  - consistent with the L0 token set (the terms it cites exist in L0)
- **Tier B (ML-verified semantic):**
  - **move-identification**: does the map's statement of the passage's argument match the exemplar's
    argument map? (semantic similarity of the "what is at issue" vs the exemplar)
  - **faithfulness**: the map does not invent an argument the source doesn't license (no unsupported
    reconstruction)
- **Skill gate:** "I understood the passage's argument structure before writing prose, and it matches the
  source."
- **Done-correct when:** Tier A (resolvable + consistent) AND Tier B (move-identification vs exemplar).

## 5. L2 (readable whole-passage prose)

The exemplar is `pilot/*_L2_read.md`; the spec is `SPEC_L2.md`.

- **Tier A (deterministic):**
  - derived from committed L0/L1 + the argument map (not independent prose)
  - content(L2) ⊆ content(L0/L1) + declared_supplies (no unsupported additions) — the semantic-fidelity
    guard already in `l1_l2_worker.py`
  - every sentence maps to L1/L0 refs; provenance resolves
- **Tier B (ML-verified semantic):**
  - **readability-vs-exemplar**: is our readable prose *equivalent in meaning* to the IPVV L2 read?
    (translation-similarity / entailment of the passage's propositions)
  - **fidelity**: every proposition in our L2 is licensed by the source (no paraphrased-away content,
    no added claim) — paraphrase-detection / claim-preservation
  - **argument-map alignment**: our L2 follows the argument map's structure (the same moves in the same
    order)
- **Skill gate:** "I produced readable prose that is faithful to the transliteral layer and follows the
  argument map, and it matches the exemplar read."
- **Done-correct when:** Tier A (fidelity + provenance) AND Tier B (meaning-equivalence + fidelity vs
  exemplar).
- **ML contract metric (proposed):** claim-preservation recall, unsupported-addition precision,
  proposition-equivalence (NLI/translation-similarity), structure-alignment.

## 6. L200 (the audit)

The exemplar is `l200/README-L200-SPEC.md` + the 3 canonical models (V2-O, V3-B, V3-C).

- **Tier A (deterministic):** — already partly implemented in `l200_worker.py`
  - 8 sections present + well-formed (identification, published reading, derivation map, MT, IA,
    source-layer, crossrefs, open, review state)
  - derivation map covers every L2 paragraph (L2 ¶ → argmap → L0 range → source range)
  - MT/IA strictly separated (a translation decision is not an interpretive assertion; a paraphrase is
    not a MT) — the frozen decision-type taxonomy
  - crossrefs typed; open items carry status; review state present
  - model-failure ≠ empty-success (fail-closed on GENERATION_FAILED)
- **Tier B (ML-verified semantic):**
  - **MT-correctness**: are the Material Translation Decisions genuinely material + correctly typed?
    (vs the canonical MT tables)
  - **IA-grounding**: do the Interpretive Assertions trace to the source, and are they distinguished from
    translation?
  - **derivation-map accuracy**: the L0/source ranges actually point at the cited content
- **Skill gate:** "I produced the audit of how this reading was derived, with MT/IA strictly separated
  and the derivation map traceable."
- **Done-correct when:** Tier A (8-section + MT/IA discipline) AND Tier B (MT/IA classification accuracy
  vs canonical exemplars — the CP5 DEV-gate benchmark).
- **ML contract metric (proposed):** MT-precision/recall, IA-precision, FALSE_POSITIVE_MT,
  category-laundering rate, derivation-map range-precision (all vs `benchmarks/l200/dev.jsonl`).

## 7. C1 (commentary)

The exemplar is `c1/C1-SPEC.md` + `c1/read/*.md` + `c1/source/*.md`.

- **Tier A (deterministic):** — implemented in `c1_worker.py`
  - all structured sections present (SUMMARY/FUNCTION/KEY TERMS/EXPLANATION/BOUNDARY/RELATED)
  - explains not paraphrases (length floor); concise (length ceiling)
  - no modern-comparison / essays-as-evidence lexicon
  - passage-local (no unsupported strengthening)
- **Tier B (ML-verified semantic):**
  - **commentary-vs-exemplar**: does our C1 capture the same passage-meaning as the IPVV C1 read?
    (semantic similarity of the SUMMARY/EXPLANATION)
  - **no-essay-drift**: the C1 stays local (no modern comparison, no grand synthesis) — classifier on the
    C1 text
  - **boundary-honesty**: the BOUNDARY/OPEN states genuine limits, matching what the source licenses
- **Skill gate:** "I produced a passage-local commentary that a reader could place under the translation,
  matching the exemplar's meaning without drifting into essay."
- **Done-correct when:** Tier A (structure + scope) AND Tier B (meaning vs exemplar + no-drift).
- **ML contract metric (proposed):** commentary-equivalence (similarity vs gold), essay-drift rate,
  boundary-honesty.

## 8. THEME

The exemplar is `SPEC_THEME.md` + `SPEC_THEME_CLUSTERING.md`.

- **Tier A (deterministic):** — implemented in `theme_worker.py`
  - every member_C1 resolves to a committed C1; members carry strength+role
  - overlapping member_of allowed; status MACHINE_PROPOSED; THEME BOUNDARY present
- **Tier B (ML-verified semantic):**
  - **theme-validity**: is the theme a genuine evidence-backed synthesis (not a keyword/cluster)?
    → compare the theme's member_C1s + recurring claims against the exemplar theme lists
    (e.g. Memory & Recognition = V2-A, V2-C, V2-L, V2-O, V2-S)
  - **no-synthesis-inflation**: the theme's claims all trace to member C1s (no claim the C1s don't ground)
  - **clustering-quality**: does the hybrid graph (terms + see-also + argument sequence) recover the
    exemplar's theme groupings? (overlap/Jaccard vs the hand theme map)
- **Skill gate:** "I produced an evidence-backed theme whose members resolve and whose recurring claims are
  grounded in those C1s."
- **Done-correct when:** Tier A (structure + resolution) AND Tier B (theme-validity + clustering-recovery
  vs the exemplar theme map).
- **ML contract metric (proposed):** theme-membership Jaccard vs gold, claim-grounding precision,
  synthesis-inflation rate.

## 9. ESSAY

The exemplar is `SPEC_ESSAY.md` + the research-library essays.

- **Tier A (deterministic):** — implemented in `essay_worker.py`
  - derived from ≥1 THEME (not forced); every sentence maps to ≥1 claim
  - SentenceEvidenceAudit passes (no certainty inflation, no boundary erasure, no orphan sentences)
- **Tier B (ML-verified semantic):**
  - **claim-licensing**: every essay sentence's meaning is licensed by its cited claims (entailment /
    paraphrase-check) — the SentenceEvidenceAudit is partly deterministic; the semantic half needs an
    entailment model
  - **evidence-resolution**: SHOW-EVIDENCE links resolve (passage → Sanskrit → decision)
  - **no-citation-as-authority**: where it cites other translations, they are adversarial witnesses, not
    authority
- **Skill gate:** "I produced proof-carrying prose where every sentence is licensed by the theme's claims
  and the evidence resolves."
- **Done-correct when:** Tier A (structure + SentenceEvidenceAudit) AND Tier B (claim-licensing +
  evidence-resolution).
- **ML contract metric (proposed):** claim-licensing entailment score, orphan-sentence rate,
  evidence-resolution rate, certainty-inflation rate.

## 10. EDUCATION

The exemplar is `SPEC_EDUCATION.md` + the concept primers.

- **Tier A (deterministic):** — implemented in `education_worker.py`
  - derived from a committed ESSAY; concise (distills, not re-runs); no overreach lexicon; links up to
    essay and down to passage
- **Tier B (ML-verified semantic):**
  - **distillation-fidelity**: the explainer is *simpler but not false* — a specialist would not object
    as false, only as simplified (paraphrase/entailment vs the essay, checking nothing is distorted)
  - **no-overreach**: the explainer does not assert beyond the essay's license (same overreach check as
    the essay, at the pedagogic surface)
- **Skill gate:** "I distilled the essay so a non-specialist understands it, without distorting or
  overreaching the evidence."
- **Done-correct when:** Tier A (structure + scope) AND Tier B (distillation-fidelity vs the essay).
- **ML contract metric (proposed):** distillation-fidelity (simplified-but-faithful), overreach rate.

---

## 11. HOW THIS BECOMES THE AUTONOMOUS GATE

Each worker already runs its **Tier A** validator at commit. The **Tier B** contract is the next layer:
it is a `benchmarks/<layer>-contract/` with a hidden gold (the IPVV exemplars) + a scorer that the worker
(or a reviewer) runs. Flow:

```
worker produces layer object
  → Tier A validator (deterministic) gates commit       [already wired]
  → Tier B scorer (ML) compares vs the exemplar gold      [to build, per layer]
      → metrics recorded as a BenchmarkRun
      → if Tier B above threshold → layer VALIDATED (MACHINE_PROPOSED-verified)
      → else → REVIEW_REQUIRED / REJECT
```

**This is how the skills state "done" honestly:** a skill claims DONE only when both Tier A and Tier B
pass against the hidden gold. The exemplars are the gold; the benchmark is the gate; the metrics are the
proof. This is the CP1 (ML-verified L0) foundation scaled to every layer.

---

## 12. PROPOSED BUILD ORDER (checkpoint-oriented)

1. **CP1 — L0/T1 ML contract** (the foundation): the semantic-equivalence harness vs the L0/T1 exemplars
   (gloss + lemma similarity, abstention, false-certainty). Build `benchmarks/l0-contract/`.
2. **L200 contract** (the highest-value audit): the CP5 DEV gate — `benchmarks/l200/dev.jsonl` + MT/IA
   precision/recall + laundering rate.
3. **L2 contract**: claim-preservation + unsupported-addition vs `pilot/*_L2_read.md`.
4. **C1 contract**: commentary-equivalence + no-drift vs `c1/read/*.md`.
5. **THEME contract**: clustering-recovery + claim-grounding vs the exemplar theme map.
6. **ESSAY + EDUCATION contracts**: claim-licensing + distillation-fidelity.

Each is a hidden-gold benchmark with an honest metric — the exact mechanism the doctrine demands
("no model works unless there is a BenchmarkRun demonstrating it").

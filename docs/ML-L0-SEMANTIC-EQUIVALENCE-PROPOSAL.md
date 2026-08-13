# SPEC PROPOSAL — ML Semantic-Equivalence Harness for L0 (RAW-Sanskrit → IPVV-Exemplar)

*2026-08-13 · Agent 2 (integration/L0 lane) · status: PROPOSAL (for external-agent review + web research)
· governing doctrine: `machinelearning/_ACTIVE/MLUSEINPATALA.md` (FROZEN — no ML idea enters unless it names
the benchmark it improves and the baseline it must beat). This proposal is written so an external agent
with web access can validate the method choices and add current best-practice citations.*

> **⚠️ SUPERSEDED FRAMING (corrected 2026-08-13, per `docs/ml/MACHINE-PROOF-CONTRACTS.md` §3 + §20):**
> this proposal was written under the **MODE_B RAW→L0** conception (raw Sanskrit creates the gloss).
> The **locked canonical stack** (`handover/agent-2-integration/CANONICAL-LAYER-STACK.md`) says instead:
> **T1 creates the gloss (the transliteral word-gloss); L0 structurally encodes T1** (`t1_extract.py → l0`).
> Therefore **most of the semantic-equivalence work described here belongs on T1, not L0.** L0 becomes
> a **deterministic round-trip contract** (T1→L0→T1 lossless), not an ML task. The correct home for the
> gloss-semantics / false-certainty / technical-sense / abstention benchmark is
> **`docs/ML-VERIFIABLE-LAYER-CONTRACTS.md` §2 (T1)** + the T1-eval scaffold in `docs/ml/LAYER-TOOLS-SURVEY.md`
> (IGT/GlossLM + ByT5-Sanskrit + metamorphic mutations + Inspect). Keep this doc for the historical
> MODE_B→T1 reconciliation (raw works like kramasadbhava still need a T1 producer), but do NOT build a
> separate L0 semantic scorer — that would duplicate/confuse authority (machineproof §7: "Do not run
> another semantic model over L0 and pretend this independently verifies T1").

---

## 0. TL;DR (one paragraph)

We want our deterministic RAW-L0 worker (raw Sanskrit → token+lemma+gloss) to be **provably
semantically-equivalent** to the human-built IPVV L0 exemplars — but the two are different tasks
(MODE_A extraction-from-English-gloss vs MODE_B creation-from-raw-Sanskrit), so we **cannot** assert
byte-identical output. We have already proven **schema isomorphism + validator-equivalence +
determinism + P0-losslessness** (`pipeline/prove_l0_equivalence.py`, all PASS). The proposal is the
**next stage**: build a **live semantic-equivalence harness** that runs our L0 against the IPVV
exemplars, scores how close the two readings are in *meaning*, iterates our segmentation/lemmatization/
gloss toward that gold (machine-learning style), and emits a mechanical proof. This becomes the
reusable training/eval substrate for our own ML tooling on future works.

## 1. The honest problem (why we cannot just "compare identical")

Verified against the live files on the mount (`translations/_stack/ipvv/`):

| | IPVV exemplar (`l0/chunkV2-C*.l0.jsonl`, MODE_A) | our worker (`raw_l0.py`, MODE_B) |
|---|---|---|
| input | already-glossed English T1 chunk | raw Sanskrit verse |
| `raw_fragment` | English gloss (`"'s knowledge of the other's\ncognition"`) | IAST token (`"śarīrasthāḥ"`) |
| `source_text` | English chunk prose | the Sanskrit verse |
| `lemma_iast` | Sanskrit lemma where recoverable | Vidyut lemma |
| task | extraction | creation |

So "identical" is **false by construction**. What is genuinely equivalent and machine-checkable:
1. **Schema** — same 17-field record, same `status`/`line_kind` enums. **PROVEN** (100%).
2. **Validator** — both pass `validate_l0_spec` (schema + abstraction-honesty). **PROVEN**.
3. **Losslessness** — our MODE_B source is exactly reconstructible from spans (P0), 0 unknown chars.
   **PROVEN**.
4. **Semantics** — does our Sanskrit token/lemma/gloss *mean* the same as the exemplar's gloss? **NOT
   YET MEASURED.** This is the open question the harness must answer.

> Note: the mount's `l0_v1/` files are ALSO English-extraction (not raw-Sanskrit gold). Only 6 of 63
> exemplar files carry Sanskrit lemmas (`chunkV2-O`, `chunkV3-B`, etc.) — a small but real raw-anchored
> gold seed.

## 2. The target shape (what "semantically equivalent" means, measured)

A per-token **alignment score** between our RAW-L0 output and the exemplar's lemma+gloss for the same
passage, aggregated to per-passage and per-work scores, with **abstention** (the harness may say
"cannot judge" rather than fabricate a score). This mirrors the existing internal precedent exactly:

- **P2 ensemble** (`docs/P2-ENSEMBLE.md`): Vidyut×Heritage morphology with honest status labels
  (SUPPORTED_BY_ENSEMBLE / SUPPORTED_BY_SINGLE_WITNESS / CONFLICTING / UNANALYZED) and benchmark rates
  (control-agreement 85%, conflict-resolution 72%). **Reuse this status taxonomy and confusion-matrix
  style.**
- **P3 lexical gold** (`docs/P3_EDITORIAL_REVIEW.md`): 0/21 promoted because the proposed sense was
  judged *from the translation that already embodies it* (circularity). **Avoid this exact circularity**:
  our Sanskrit token must be judged against the exemplar gloss using INDEPENDENT signal, not a gloss we
  generated from the same text.
- **semantic_alignment.py** (`machinelearning/research/patala_ml/semantic_alignment.py`): already
  implements `align(A,B)` in three spaces (sanskrit/l2/c1) with 6 labels + abstention + per-space
  cosine. **This is the scaffold** — it already embodies the "neural similarity NOMINATES, never asserts,
  a scholarly relation" rule.

## 3. Proposed method stack (what to benchmark, in order)

Frozen rule: **never let a neural similarity score become a scholarly relation by itself.** The harness
emits MACHINE_PROPOSED equivalence scores; Pāṭala's explicit graph + human review adjudicates.

**Stage 1 — lexical/anchor baseline (deterministic, CPU, mandatory baseline to beat):**
- For each raw-Sanskrit token, match our `lemma_iast` against the exemplar record's Sanskrit lemma
  (where present) and the embedded Sanskrit term in the exemplar's parenthetical gloss.
- Score exact / stem-equivalent / compound-split / no-match (reuse P2's relation classes).
- Baseline = our RAW-L0 self-consistency + the P0 lossless floor.

**Stage 2 — cross-lingual semantic alignment (dense, CPU-small):**
- Use `semantic_alignment.align` in the `sanskrit` + `l2` + `c1` spaces.
- Candidate encoders (all in `machinelearning/research/RESOURCES.md §2`): `all-MiniLM-L6-v2`
  (fastest), `paraphrase-multilingual-mpnet-base-v2` (multilingual Skt coverage), `intfloat/
  multilingual-e5-large` (stronger), and the Skt-aware `ByT5-Sanskrit` (arXiv 2409.13920 — byte-level
  Skt LM, SOTA segmentation/lemmatization/morphosyntactic tagging) as the strongest reference.
- The empirical question: **which representation space catches false-similarity vs true equivalence**
  for Skt technical terms (śakti, kula, krama, vimarśa).

**Stage 3 — iteration / fine-tune toward gold (the "ML" part):**
- Treat the 6 raw-anchored exemplar files as a small gold seed; the 57 English-extraction files as
  weak supervision (lemma side only).
- Options to benchmark (need external validation of current SOTA):
  - **ByT5-Sanskrit** fine-tune on Sanskrit word-segmentation/lemmatization (arXiv 2409.13920) — the
    strongest published route for our exact tokenization task.
  - Instruction-tuned LLM vs task-specific Seq2Seq on Sanskrit parsing (arXiv 2511.08145 — "Still Not
    There": domain fine-tuned ByT5 beats instruction LLMs on Sanskrit poetry→prose; relevant to whether
    we fine-tune or prompt).
  - Energy-based segmentation (arXiv 1809.01446 — "Free as in Free Word Order").
  - "Sanskrit Segmentation Revisited" + "Building a Word Segmenter for Sanskrit Overnight" (classical
    segmenters to compare the deterministic Vidyut floor against).
- Gate: any model only enters if it beats the Stage-1 lexical baseline on a **fixed held-out split**
  (per MLUSEINPATALA.md — never tune on the set you evaluate on).

## 4. Output contract (the mechanical proof)

Per passage, a JSON record (mirrors P2's per-record capture + the AUTONOMY_CONTRACT run report):
```
{
  "passage_id": "...", "work_id": "...",
  "tokens": [
     {"surface": "...", "lemma": "...", "gloss": "...",
      "exemplar_lemma": "...", "exemplar_gloss": "...",
      "equivalence": "EXACT | STEM_EQUIVALENT | COMPOUND_SPLIT | CONFLICT | UNANALYZED | ABSTAIN",
      "alignment": {"sanskrit": 0.0, "l2": 0.0, "c1": 0.0}}
  ],
  "aggregate": {"precision": 0.0, "recall": 0.0, "abstention_rate": 0.0,
                "false_certainty": 0.0, "n_exact": 0, "n_conflict": 0},
  "method": {"encoder": "...", "prompt_hash": "...", "worker_sha": "..."},
  "status": "MACHINE_PROPOSED"
}
```
**Gate (mirrors P2/P3 honesty):** no EQUIVALENCE label may be claimed from a similarity score alone;
the harness reports MACHINE_PROPOSED + abstention; human review of the CONFLICT/ABSTAIN cells is the
route to an ADJUDICATED gold.

## 5. What the external agent should research/validate (with web access)

1. **Sanskrit word-segmentation + lemmatization SOTA in 2026** — confirm ByT5-Sanskrit (2409.13920)
   is still the strongest published byte-level Skt model, or identify newer (Skt-T5, Vedas corpus
   models, Dharmamitra etc.).
2. **Cross-lingual dense alignment for Skt↔English technical terminology** — does multilingual-e5 or
   a Skt-aware model handle terms like *vimarśa* / *śakti* better than all-MiniLM? Is there a better
   model (e.g. BGE-M3, LaBSE, text-embedding-3 multilingual)?
3. **Fine-tune vs instruction-tune for our task** — is the 2511.08145 finding (fine-tuned ByT5 beats
   instructed LLMs on Skt) still current, and does it apply to tokenization/lemmatization or only to
   poetry→prose?
4. **Whether a held-out eval split should be passage-level or work-level** to avoid leakage
   (P3's circularity lesson).
5. **Cost/CPU feasibility** of the recommended model in our CPU-only research lane
   (`machinelearning/research/requirements.txt`).

## 6. Success criteria (what closes this proposal)

- A `benchmarks/l0-semantic-equivalence/` with a frozen split + the run harness
  (`pipeline/benchmark_l0_semantic.py`).
- A deterministic lexical baseline (Stage 1) with honest P/R/abstention on the raw-anchored seed.
- At least one model/representation that **beats** the baseline on the held-out split, with the
  comparison reproducible.
- A mechanical proof object (per §4) that future works' RAW-L0 can be scored against the IPVV gold the
  same way — the substrate for our own ML tooling.

## 7. Guardrails (from MLUSEINPATALA.md + doctrine)

- No ML output becomes established scholarship without human review; everything is MACHINE_PROPOSED.
- Neural similarity NOMINATES, the Pāṭala graph + human adjudication ASSERTS.
- Never tune on the held-out split; a wrong reading is worse than abstention.
- Reuse P2/P3/semantic_alignment internal precedents — do not rebuild parallel machinery.
- Do not treat the mount exemplars' content as raw-Sanskrit gold; only 6 files are raw-anchored.

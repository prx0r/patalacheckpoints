# SPEC — THE RIGID DATA CONTRACT (schema + validation metrics per layer)

*2026-08-12. To make Pāṭala work for ANY text and be ML-ready, every layer needs a **machine-enforced
schema + precise validation metrics** — not just "general format instructions." The bottom layers (L0,
T1→C1) already have this; the ML layers (argument, cluster, provenance) do NOT. This spec defines the
contract for all layers, so a new text is validated identically and the ML consumes guaranteed shapes.*

> **The principle:** a layer is only "done" when (1) its output matches a typed schema, and (2) it passes
> deterministic validation metrics. A doc describing the format is not enough — the validator is the
> contract.

---

## 0. The layer-by-layer contract (the whole spine)

| Layer | Schema (typed) | Validation metrics | Status |
|---|---|---|---|
| **SOURCE** | witness record | source_id resolves · license tagged · span→passage 1:1 | ✅ (SPEC_SOURCE) |
| **L0** | token record | PARSED+AMBIGUOUS+FAILED = round-trip count · every lemma has gloss | ✅ deterministic |
| **L2** | passage prose | every proposition → L0 range · term-ledger consistent | ✅ (Task-1/2) |
| **L200** | 8-section audit | derivation map covers all L2 ¶ · MT/IA separated · typed crossrefs | ✅ (validate.py) |
| **C1** | structured record + read | **machine metrics (below)** | ⚠️ part-human |
| **THEME/CLUSTER** | ClusterProposal | coherence · overlap · edge-evidence · determinism | ✅ (my cluster) |
| **ARGUMENT** | ArgumentProposal | **schema + gates (below)** | ❌ no schema |
| **PROVENANCE** | claim→evidence | RESOLVES/AUTHENTIC/RELEVANT/SUPPORTS | ❌ no schema |

The **bottom is rigid, the top is not.** The fix is to extend the existing `schema.py`/`contracts.py`
pattern to the ML layers.

---

## 1. C1 — turn the human checklist into machine metrics

The C1-SPEC has 10 human checkboxes. Make them *measurable*:

| Checkbox | Machine metric |
|---|---|
| "explains, not paraphrases" | **novel-word ratio** = (new words in C1 not in L2) / total — a paraphrase repeats; an explanation adds |
| "stays local" | **local-referent score** = % of cross-references that are nearby passages (RELATED, not global) |
| "no modern comparison" | **anachronism detect** = presence of banned-term list (self-model, predictive processing, Ñāṇavīra...) |
| "distinguishes established vs stronger" | **boundary presence** = the BOUNDARY field is non-empty + has hedging words (does not, not by itself) |
| "terms contextually precise" | **term-ledger match** = each KEY TERM resolves in the ledger with a sense |
| "uncertainties visible" | **hedge ratio** = count of uncertainty markers (possibly, may, not certain) per word |

These turn C1 validation from subjective to a **scored, thresholded, reproducible metric**. A C1 passes
if it meets each threshold. This is what the ML (Vertical Fidelity, argument extraction) needs — a
guaranteed C1 shape.

---

## 2. THEME / CLUSTER — the metrics already exist

My clusterer emits: `size, coherence, members_overlapping, member_c1_ids, edge_evidence` + validates
determinism. **This is the rigid contract for the cluster layer.** Add one metric:
- **structural floor** — every member_c1_id resolves to a real passage (via `/api/resolve`); every
  membership has edge_evidence (no orphan membership).

---

## 3. ARGUMENT — the new rigid schema (the AIF-informed ArgumentProposal)

The most important missing schema. From the external review + truth-engine, a typed ArgumentProposal:

```json
{
  "argument_id": "pt:argument:ipvv:V2O-orderless-support:ARG-001",
  "claim": { "text": "...", "explicitness": "EXPLICIT|IMPLICIT", "speaker": "ABHINAVAGUPTA",
             "role": "CONCLUSION|PREMISE|OBJECTION|REPLY" },
  "inference": { "scheme": "TRANSCENDENTAL|REDUCTIO|ANALOGY|ENTAILMENT|PRESUPPOSITION",
                 "inference_id": "ARG-INF-001" },
  "source": { "sanskrit_span": "...", "passage_id": "pt:passage:ipvv:...", "immutable_id": "..." },
  "evidence_chain": { "L1_support": "...", "L2_rendering": "...", "C1_discovery": "...",   // C1 DISCOVERS, never proves
                      "L200_IA": "IA-001" },
  "status": "MACHINE_PROPOSED",
  "strength": null   // derived later: FORMALLY_VALID_GIVEN_ENCODING|REVIEWED|WELL_SUPPORTED|PLAUSIBLE|SPECULATIVE
}
```

**Validation metrics for ARGUMENT:**
| Metric | What it checks | Deterministic? |
|---|---|---|
| **resolvability** | `source.passage_id` + `immutable_id` resolve via `/api/resolve` | ✅ |
| **downward-chain** | every claim's evidence_chain has a Sanskrit span (C1 is discovery, not evidence) | ✅ |
| **circularity-guard** | no claim's evidence is ONLY a C1 (must point to L0/Sanskrit) | ✅ |
| **speaker-scope** | `speaker` is a valid actor; `claim` doesn't assert what the speaker didn't | ⚠️ semantic |
| **explicitness** | IMPLICIT claims flagged for human review (the hard case) | ✅ flag |
| **gate** | passes the Nyāya hetvābhāsa + falsifier checks | ✅ (truth-engine gate) |

---

## 4. PROVENANCE — the 4-level contract

Every essay/claim→evidence link must be typed at one of four levels (the external review's correction):
```json
{ "claim_id": "...", "evidence_id": "...", "passage_id": "...",
  "level": "RESOLVES|AUTHENTIC|RELEVANT|SUPPORTS",
  "relation": "ENTAILS|SUPPORTS|QUALIFIES|CONTRADICTS|INSUFFICIENT",
  "verified_by": "verify-service-id", "status": "machine|human" }
```
**Validation:** RESOLVES + AUTHENTIC are deterministic (`/verify/quote` + `/verify/claim-structure`);
RELEVANT + SUPPORTS are semantic → model-proposed, human-reviewable. The contract enforces *which
level is claimed* so an essay can't silently upgrade RESOLVES to SUPPORTS.

---

## 5. The meta-contract — a cross-layer validator

A single `validate_layers.py` that walks a passage through every layer and reports, per layer:
```
PASSAGE V2-O
  SOURCE:     ✓ span resolves
  L0:         ✓ 3444 tokens round-trip
  L2:         ✓ 3 ¶ traceable
  L200:       ✓ 6 MT / 3 IA, typed crossrefs
  C1:         ✗ anachronism: "predictive processing" present   ← catches the leak
  CLUSTER:    ✓ CL-3 member, coherence 3.5
  ARGUMENT:   (none yet)   ← the gap
```
This is the **"highly precise exact validation metrics"** the user asked for — one command that tells
you, for any text, exactly which layers pass and which fail, so nothing is silently unvalidated.

---

## 6. Why this makes it "work for any text"

Once the contract is a validator (not a doc):
1. A new text (Tantrāloka, Spandakārikā) is **validated identically** — no ad-hoc checking.
2. **ML consumes guaranteed shapes** — the argument/cluster/provenance loaders don't guess; the
   validator guarantees the fields.
3. **The validation IS the ML training signal** — the C1 metrics, the argument resolvability, the
   provenance levels are exactly the supervision data the ML learns over.
4. **Every transformation is measured** (the external review's methodology): you validate C1→proposition
   precision, proposition→role F1, etc., because each layer's output is a known typed object.

---

## 7. What to build (the immediate queue)

| # | Build | Effort |
|---|---|---|
| **1** | **`schema_layers.py`** — the typed schemas for C1-metrics, ArgumentProposal, Provenance (extend the existing `schema.py` pattern) | medium |
| **2** | **`validate_layers.py`** — the cross-layer validator (one command per passage, per-layer pass/fail) | medium |
| **3** | **C1 machine metrics** — turn the 10 human checkboxes into scored metrics | medium |
| **4** | **Argument validator** — resolvability + downward-chain + circularity-guard + explicitness-flag | medium |
| **5** | **Provenance 4-level contract** — the typed claim→evidence record | low |

This is the **rigid foundation** that makes the whole pipeline reproducible for any text and
ML-ready. Without it, the docs describe the format but nothing *guarantees* it.

---

## 8. Bottom line

The user is right: **general format specs are not enough.** The pipeline becomes "for any text" only
when each layer has (1) a typed schema and (2) deterministic validation metrics — and the ML layers
(C1 metrics, ArgumentProposal, provenance levels) are the ones missing them today. The build is to
extend the existing `schema.py`/`contracts.py` pattern upward: a cross-layer validator + per-layer
metrics that turn every transformation into a measured, guaranteed-shape step. That's both the
reproducibility contract AND the ML supervision substrate.

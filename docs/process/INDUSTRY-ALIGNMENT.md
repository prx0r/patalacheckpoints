# THE INDUSTRY-ALIGNMENT MAP (our homegrown stack → formal standards)

*2026-08-14. The honest mapping of Pāṭala's homegrown scholarly stack onto **formal/industry standards**.
The goal: our mechanisms are conceptually right but not "frontier-legible." This map makes each layer
legible as industry-aligned, and flags which layers are genuinely NOVEL (the moat) vs. which should be
plain adapters to existing standards.*

> **The principle (matches `source_evidence_profile.py`):** compose existing standards, don't invent
> ontologies. Pāṭala adds only the fine-grained epistemic kernel on top. Adapters outward, kernel inward.

---

## THE TRANSLATION STACK → STANDARD (the layer the user asked about)

| Our layer | What it actually does | Maps to the formal standard | Adapter or Novel? |
|---|---|---|---|
| **SOURCE / WITNESS** | the text + its physical witness | **CTS URN** (citable passage identity) + **TEI** (critical apparatus, `listWit`/`rdg`) | ADAPTER — use CTS semantics + SARIT TEI |
| **T1** (working translation + gloss + evidence) | careful word-level reading anchored to source | **IGT (Interlinear Glossed Text)** — the literal standard for word-gloss + alignment | ADAPTER — benchmark via GlossLM, output IGT-compatible |
| **L0** (structured tokens from T1) | token/morphology/lemma floor | **TEI feature structures** + **Text-Fabric text-position primitive** (stable token identity) | ADAPTER — Vidyut is the deterministic kernel |
| **L2** (readable prose) | the readable translation | **XLIFF** (translation-memory interchange) if interop needed; else free | OPTIONAL adapter |
| **L200** (proof: how the reading was derived) | material translation decisions + interpretive assertions + derivation map | **NO STANDARD — this is the `TranslationProof` object, genuinely novel** | **NOVEL (the moat)** |
| **T1/T2/R2/T3** (rival readings + adjudication) | strongest-rival + adjudication of decisions | **MQM** (Multidimensional Quality Metrics error taxonomy) + **TeamTat** blind-adjudication pattern | ADAPTER — MQM as the error vocabulary |
| **C1** (passage interpretation) | passage-local meaning | **xAIF** (argumentation interchange) + **nanopub** (claim+evidence) | ADAPTER outward |

**The key finding: `L200` (proof-carrying translation) is genuinely FRONTIER.** No formal standard covers
"what Sanskrit was read, how parsed, which target spans realize which source obligations, what couldn't
be verified, what alternatives exist." That's the moat — the `patalatranslate` review's core idea. The
layers *around* it (T1→IGT, L0→TEI+CTS, adjudication→MQM, publish→RO-Crate) should be plain adapters.

---

## THE FULL STACK → STANDARD (beyond translation)

| Pāṭala layer | Maps to standard |
|---|---|
| 01 Ingestion (OCR) | Kraken (ALTO/PageXML), CTS identity |
| 02 Atlas (identity/provenance) | CTS URN, PROV-O, knowledgeProvenance, nanopub |
| 03 Factory (compiler) | the DAG = a build-pipeline; XLIFF for TM interop |
| 04 Evidence (contracts) | **FaBiO / PROV-O / W3C Web Annotation / CiTO / RO-Crate** (already aligned in `source_evidence_profile.py`) |
| 05 Research (argument/crux) | **xAIF / oAMF** (argument interchange) — adapt outward, native stays richer |
| 07 Verification | **Inspect AI** (runtime) + MQM (error vocab) + SciFact/FEVER (claim-check patterns) |
| 08 Human Authority (review) | **OpenReview / COAR Notify** + TeamTat blind-adjudication + CRediT/ORCID |
| 10 Surfaces | DTS (text API), IIIF (manuscripts), RO-Crate (export) |
| 12 Live System | Hermes (execution) + C2PA (Stencila signed provenance) |

---

## THE "WHAT'S NOVEL vs. WHAT'S AN ADAPTER" VERDICT

**NOVEL (the moat — no standard covers these, keep them native):**
- **`L200` / `TranslationProof`** — proof-carrying translation (source obligations → target spans, unverified, alternatives, checks)
- **The epistemic kernel** — proposition identity + argument reconstruction + semantic-strength ceilings + crux propagation
- **The review-gated promotion** — `ReviewEvent` → adjudication → graph mutation with provenance
- **The learner model over verified structure** (Engram-style, but from the epistemic graph)

**ADAPTER (reuse existing standards, don't build):**
- T1 gloss → IGT · L0 tokens → TEI+CTS · passage identity → CTS · OCR → Kraken · schema → Stencila ·
  provenance → PROV-O/nanopub · publish → RO-Crate/C2PA · adjudication → MQM/TeamTat · argument interop → xAIF

---

## THE ONE-LINE STRATEGIC POSITION

> Pāṭala's layer names are homegrown, but the concepts are portable. **The `L200`/`TranslationProof` layer
> and the epistemic kernel are genuinely frontier (the moat); everything around them should become
> adapters to formal standards** (IGT, TEI, CTS, MQM, xAIF, RO-Crate, C2PA). Make the stack *legible* by
> publishing this map, then *align* by wrapping each adapter.

---

## NEXT ACTION (recommended)

1. **Publish this map** (done — this doc) so the homegrown stack is industry-legible.
2. **Adopt the error vocabulary:** map MQM error types onto our L200/T1 validators.
3. **Add `cts_urn`** to `external_ids` on passage/work (cheap, high interop value).
4. **Align T1 output to IGT** (so GlossLM + the IGT benchmark can evaluate it).
5. **Design the `TranslationProof` schema** as a first-class object (the novel moat) — start from
   `docs-cache/patalatranslate.md` §26.

# AI DOCS — TAKEAWAYS (the actionable distill)

*2026-08-12. What the `ai/` deep-research + AI-vision docs actually mean for Pāṭala, distilled to what an
agent should act on. Source docs: `ai/VISION.md`, `ai/argumentation-ir-frameworks-survey.md` (Deep Research 10),
`ai/argumentation-ir-exec-summary.md` (Deep Research 11), reconciled with `machinelearning/_ACTIVE/ARGUMENT-IR-VISION.md`
and `PATALA-ENGINE-ROADMAP-12MO.md`. The doctrine still governs: **nothing is real without gold + blind eval + metric +
human adjudication.**

---

## 1. The one thesis (from `ai/VISION.md`)

> **AI is commoditizing translation, prose, and RAG. Pāṭala's moat is the verified, provenance-preserving scholarly
> substrate — not better AI.** Pāṭala should become the canonical machine-verifiable research layer for Indian
> philosophical texts: canonical IDs + provenance + gold/benchmark evaluation + human-correction/error corpus +
> evidence-and-argument graph. Every stronger model makes Pāṭala *more* useful, because intelligence gets cheaper
> while the verified substrate stays scarce.

Implications that matter to **Agent 1 (CP4)**:
- The **gold benchmark is a moat and the measurement instrument** — IPVV as a hard AI-philology benchmark
  (PĀṬALA-IPVV), not just a translation corpus. This is *why* ARG-001..005 must be real, hand-grounded, blind-evaluable.
- **"AI proposes ≠ Pāṭala asserts"** is the architecture, not a slogan: every generated object enters as
  `PROPOSED`, promoted only by evidence validation + human review.

## 2. The tool split (from Deep Research 10)

**Delegate computation, own the IR + provenance.** Do NOT reimplement argumentation engines:
- **py-aspic** — ASPIC+ structured reasoning (compile `InferenceRule`/`InferenceApplication` → `pyaspic.Rule`).
- **xAIF / oAMF** — interchange + mining pipelines (export/import the IR graph as xAIF JSON).
- **ALIAS** — Dung semantics / abstract acceptability (collapse IR → AF, compute extensions).
- **ArgLLM / AKG** — LLM argument construction + undercut detection (design reference only).
- **Epistemic Argumentation Frameworks** — multi-regime evaluation (Śaiva vs Buddhist) is a known concept, no
  off-the-shelf tool; custom labeling needed (LATER, CP5).

**The four real gaps (where Pāṭala must build):**
1. **SemanticAlignment** — word-sense disambiguation (open; no tool).
2. **Commitment** — who said what, and with what force (no NLP solution; custom parsing/curation).
3. **Epistemic regimes** — tradition-relative evaluation (novel; no tool).
4. **Crux extraction** — minimal pivotal premises (minimal-hitting-set, potentially NP-hard; novel).

## 3. The roadmap / build order (from Deep Research 11)

Gold-first, exactly the current CP4 discipline:
```
Phase 0  Gold-annotate 5–10 IPVV debates → force the IR schema (propositions, frames, commitments)
Phase 1  Prototype engine: py-aspic adapters; Commitment extraction; Nyāya gate on annotated cases; crux study
Phase 2  Integrate in an oAMF pipeline; evaluate end-to-end on the gold; Beta
```
Go/No-Go (Month ~8): inferred argument states match expert judgment on **>80%** of gold cases (incl. cruxes),
with no core gap → community rollout; else revisit alignment/commitment.

## 4. What this means for the two agents RIGHT NOW

**Agent 1 (CP4, the live build):** the deep-research validates the current plan exactly — build ARG-003 (reductio) /
004 (conceptual-distinction) / 005 (ambiguous) **with the IR shape already in the gold**: `Commitment` (who asserts vs
attributes-to-opponent), derivational `Proposition` (`derived_from`), `ResearchQuestion`, Attack/Defeat split, and
three-level `SemanticAlignment` (LEXICAL/CONCEPTUAL/PROPOSITIONAL) for ARG-005. Do NOT build py-aspic/xAIF adapters yet —
that is Phase 1, after the gold. Do NOT design EpistemicRegime/EvaluationProfile/Crux empty — the gold forces them.

**Agent 2 (CP1, the source floor):** the AI vision reinforces that the L0 proof floor (P0 35/35, P2 calibrated witness)
is the bottom of the provenance stack every later moat resolves to. Keep `PhilologicalProof` honest — it is the
`grounding`/`derived_from` floor the IR propositions resolve to.

## 5. The honest position

These `ai/` docs are **new and not yet wired into the docs system** (not in `docs/INDEX`, `docs/vision/INDEX`,
`handover/CONTEXT-CHAIN.yaml`, or `onboarding/README.md`). They are directional research that *confirms* the existing
CP4 gold-first plan; they do not change the immediate build. The survey/report files carry a caveat (from git
`bebf96b`): the referenced tools are small/immature (1–18 GitHub stars) — "mature" in the report is optimistic;
treat them as prototypes to evaluate, not turnkey.

---

## The one-sentence carry-forward

**AI commoditizes generation; Pāṭala owns the verified substrate — so the immediate mission is unchanged and more
justified: build real Argument Gold (ARG-001..005) with the IR shape, route everything through the frozen benchmark,
and defer all argumentation-engine adapters (py-aspic/xAIF/oAMF/ALIAS) to Phase 1 until the gold forces the ontology.**

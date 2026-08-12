# PĀṬALA PRODUCT PORTFOLIO — aligned by user base (the cohesive product map)

*2026-08-12. The consolidation that aligns every vision doc to a concrete **user base / product surface**.
Reads the whole vision (Vision 01–12 + the endgames + the lens folders) and organizes it as **who buys/uses
what**, completing Vision 12 (Multi-Surface Platform). For each surface: the products, the vision docs they
come from, and the concrete feature. This is the product catalog — the "what do we actually build for whom".*

---

## THE ALIGNMENT (every vision → a surface)

| Surface | User | Products | Sources |
|---|---|---|---|
| **CONSUMER** | learners, practitioners, general readers | Tantra Hub · reader · atlas graph · learning/courses · media (shorts/video/AI-teacher) | V01/02, V09, `LEARNING_STRATEGY.md`, `EDUCATION_VISION.md` |
| **SCHOLAR** | Sanskritists, philosophers, digital-humanities researchers | **Pāṭala Review** · Scholar Workbench · research compiler · translation QA · benchmark/rating | V06, V07, V08 |
| **CONTRIBUTOR** | manuscript holders, editors, translators | acquisition pipeline · manuscript upload · translation memory · critical editions | V11, `endgame1.md` |
| **DEVELOPER** | external agents, researchers building tools | Pāṭala API · MCP (`mcp.patala.org`) · OAuth · BYOA · executable-corrections protocol | V12, `apideas.md`, `hermes-execution.md` |
| **REVIEWER** | editorial board, specialist adjudicators | review queue · adjudication · promotion policy · review credit (ORCID/Crossref) | V06, V08, `PEER-REVIEW.md` |

**The rule (Vision 12):** one scholarly core, five permission-scoped surfaces. The products below are
projections of the SAME graph + MCP + review engine.

---

## SCHOLAR-FACING PRODUCTS (the full catalog — including new brainstorm)

These are the scholar products, grouped by the job they do for a scholar.

### A. Translation quality (the biggest new opportunity — rating, correcting, benchmarking)
The scholar's #1 pain is translation uncertainty. Pāṭala can offer, all on top of the 63/63 L0 floor:

1. **Translation Rating / Audit** — a scholar pastes their translation of a Sanskrit span; Pāṭala returns a
   structured assessment: source-integrity PASS/FAIL, morphology analyses, alignment (which English maps to
   which Sanskrit), term-policy consistency, parallels, external readings, and **flags** (omission,
   overtranslation, polarity shift, referent issue, term-sense drift). *This is Vision 06 §1, now
   operational via `verify_l0` + `l0_align` + the review engine.*
2. **Adversarial Translation Review** — "attack this reading." Pāṭala generates the strongest rival parse
   and returns objections (referent, term-sense, scope). *Vision 06 §2 — the `/adversarial-translation-review` product.*
3. **Translation Comparison** — same Sanskrit, translations A/B/C → agreement/divergence + why it matters
   (`/compare-readings`). *Vision 06 §10.*
4. **Term Audit** — "audit my use of *śakti* across this translation" → 63 occurrences, rendering
   distribution, unexplained drift. *Vision 06 §11.*
5. **A Sanskrit translation BENCHMARK** — the moat asset: PĀṬALA-IPVV, a curated set of difficult passages
   with expert gold (segmentation, translation, speaker attribution, argument role, term sense, ambiguity).
   This **rates** a scholar's translation against gold AND **measures AI competence** in Sanskrit philosophy.
   *From `visionai`/`historicalsiva` + the manifest — makes Pāṭala the place where Sanskrit-AI competence is measured.*

### B. Review & the research compiler (Vision 06 — the mega-product)
6. **Pāṭala Review** — a scholar uploads a draft article/chapter/thesis → machine pre-review →
   claim extraction → citation resolution → argument graph → source-grounding audit → Reviewer-2 attack →
   impact/crux analysis. Returns "17 claims, 11 grounded, 2 unsupported, 1 load-bearing issue." Every
   criticism resolves to corpus objects.
7. **The Research Compiler** — raw scholarly input → warnings/errors/unresolved-references/dependency-graph
   → an AUDITABLE RESEARCH OBJECT (like a compiler, not an AI reviewer). *Vision 06 §15.*
8. **Thesis stress test** — "in early Krama, kālī primarily functions as X" → supporting/qualifying/
   counterexample passages + chronological/scope problems (`/stress-test-thesis`). *Vision 06 §8.*
9. **Impact analysis** — "what depends on this reading?" → the executable-corrections ImpactReport
   (already built in Phase 3A/3D). *Vision 06 §13.*
10. **Philological proof certificate** — a machine-readable certificate ("these 11 proof obligations were
    checked"), citable in papers. *Vision 06 §3.*

### C. The Scholar Workbench (Vision 07 — structured inquiry)
11. **Explore mode** — the scholar works in the research graph: test alternatives, map arguments, collect
    tensions, build themes, stress-test a thesis. The essay is one output.
12. **The review screen** (Phase 3E, minimal) — object · evidence · current state · proposal/review
    controls · impact preview · submit. The entry point to the executable-corrections loop.
13. **The AI research copilot** — a constrained profile that queries the MCP, compares readings, launches
    blind critics, constructs alternatives — but cannot accept/promote.

### D. Scholar economics (Vision 08 — makes it sustainable)
14. **Scholarly bounties** — tightly scoped, paid adjudication (not "review our corpus for free").
15. **Durable credit** — ORCID/CRediT/DOI: "I reviewed 63 Pratyabhijñā propositions for Pāṭala" becomes a
    citable scholarly service.
16. **Microgrants / commissions** — for neglected texts (Kubjikā microgrant, early-career fellowship).

---

## CONSUMER-FACING PRODUCTS (educational — the current site)

17. **Tantra Hub / Reader** (V02) — bibliography, reader, translation-workshop, commentary, media.
18. **The atlas graph** — the traditions/texts/concepts rendered as a navigable graph (the current homepage).
19. **Learning / courses** (V09 + `LEARNING_STRATEGY.md`) — knowledge packets → quizzes/courses; the
    graph-native teaching engine (`EDUCATION_VISION.md`).
20. **Media layer** (V09) — the scholarly core rendered as shorts/video/essays/AI-teacher, reproduced
    across traditions (Tantra → Yogic → Vedānta → Greek).

---

## DEVELOPER-FACING (already real — the protocol surface)

21. **Pāṭala API** (34 routes) — stable primitives.
22. **Pāṭala MCP** (21 tools + 5 review tools) — `mcp.patala.org`, OAuth scopes, BYOA.
23. **The executable-corrections protocol** — machine→propose, authorized-scholar→review, Pāṭala→compute.
    The start of "Pāṭala as a scholarly protocol rather than a repo."

---

## CONTRIBUTOR-FACING (V11 — the corpus growth surface)

24. **Manuscript upload / acquisition** — upload a scan/transcription → metadata/rights → Agent 2's corpus
    inventory → the translation factory.
25. **Critical editions** — fork a reading → Pāṭala calculates dependencies, term-policy changes, proof
    obligations ("GitHub PRs for philology"). *Vision 06 §17.*

---

## REVIEWER-FACING (A4 — the adjudication surface)

26. **The review queue** — graph-aware ranking of objects needing judgment (impact/uncertainty/centrality).
27. **Adjudication + promotion policy** — the strongest boundary; only editors/adjudicators promote.
28. **Review credit** — Crossref `isReviewOf` + ORCID reviewer credit (the interop stack).

---

## THE PRODUCT-LED BUILD SEQUENCE (relative to the autonomous-translation priority)

```
NOW (built)     L0 floor 63/63 · corpus state · review engine (3A+3D) · MCP (21+5) · API
NEXT (priority) Agent 3 translation factory → produces the machine-proposed drafts
THEN            Scholar product #1: Translation Audit/Rating (uses what's built, no new infra)
                + the minimal 3E review screen
THEN            PĀṬALA-IPVV benchmark (the rating moat — measures scholar translation vs gold + AI)
LATER           Pāṭala Review mega-product, Workbench, media, contributor, reviewer surfaces
```

**The logic:** the translation factory produces the raw machine-proposed material; the **Translation Audit
(#1) + benchmark (#5)** are the first scholar products because they're *directly* enabled by the 63/63 floor
+ P4 alignment + review engine we already built — no new infrastructure, just the product layer.

---

## THE ONE-SENTENCE CARRY-FORWARD

**Pāṭala's products align to five user bases (consumer/scholar/contributor/developer/reviewer) as
permission-scoped projections of one scholarly core; the scholar catalog is rich — translation
audit/rating, adversarial review, comparison, term audit, a Sanskrit-translation benchmark, the research
compiler, the workbench, bounties and durable credit — and the first two to build after the Agent 3 factory
are the Translation Audit and the PĀṬALA-IPVV benchmark, because the 63/63 floor + P4 alignment + review
engine already make them possible without new infrastructure.**

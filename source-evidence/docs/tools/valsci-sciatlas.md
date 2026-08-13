# Valsci + SciAtlas — external baselines / retrieval providers (later)

**What Pāṭala borrows:** two *competitor/compare* systems, NOT build-on:
- **Valsci** — automated scientific claim verification (literature retrieval + structured evidence reports,
  OpenAI-compatible models, batch claim checking). **Do not build on it** (its bibliometric credibility scoring
  doesn't align with Pāṭala), but run it as an **external competitor baseline** on the same claims for
  CorroborationBench.
- **SciAtlas** — graph-aware scholarly retrieval over papers/authors/institutions/venues/citations/topics, with a
  reusable machine-readable artifact client. **Not a backend**, but a possible **external research retrieval
  provider / baseline** for the modern-science side — a way to ask *does explicit Pāṭala epistemics improve on a
  good graph-aware retrieval system?*

**Licenses:** open (check each repo).

## How Pāṭala consumes them
Baselines in the benchmark matrix:
```
BM25  vs  PaperQA2  vs  Valsci  vs  SciAtlas  vs  generic RAG  vs  Pāṭala
```
If Pāṭala's explicit attribution/scope/defeater machinery matters, the epistemic-fidelity metrics
(attribution/scope preservation) should show it even if raw answer accuracy is comparable.

**Priority: LATER (baselines).**

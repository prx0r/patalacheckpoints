# AlignScore — cheap semantic entailment witness

**What Pāṭala borrows:** a general information-alignment function (trained on ~4.7M examples across NLI,
QA, paraphrase, fact-verification, retrieval, semantic-similarity, summarization; tested on 22 factual
consistency datasets). A cheap semantic entailment layer so we don't need an LLM critic for every claim.

**License:** MIT. Repo: `yizhongw/AlignScore`.

## The cheap→expensive ladder (08-verification-plane.md)
```text
claim → deterministic checks → AlignScore/NLI cheap verifier
  → obvious PASS/FAIL → record
  → borderline → LLM critic
  → critic uncertain → OPEN / human
```

## How Pāṭala consumes it
**PLANNED.** Optional local semantic witness in the verification plane — routes most claims through the
cheap path, escalating only borderline cases.

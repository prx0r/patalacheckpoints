# RefChecker — atomic claim decomposition + fidelity

**What Pāṭala borrows:** decomposes model output into fine-grained knowledge triplets and checks each
against reference material, with localization back into reference snippets. Granularity beats
whole-response/sentence/sub-sentence checking for hallucination detection.

**License:** Apache-2.0 (archived Apr 2026 — pin/fork behind your own interface). Repo:
`amazon-science/RefChecker`.

## The architecture (modular: extractor + checker + aggregation independently replaceable)
```text
generated text → claim extractor → claim triplets → checker vs reference → Entailment/Neutral/Contradiction → aggregate
```

## How Pāṭala consumes it
**PLANNED.** The atomic-support evaluator shared by L2-License / C1-License / Essay-License /
Education-License (`08-verification-plane.md`). Reference = Pāṭala upstream objects, not Wikipedia.

## Doctrine
Check atomic claims, not the whole answer. Support LLM/NLI/AlignScore checkers.

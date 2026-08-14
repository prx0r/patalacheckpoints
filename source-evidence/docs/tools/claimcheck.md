# CLAIMCHECK — claim-targeted critique (scholar-review objections)

**What Pāṭala borrows:** links review weaknesses to the paper claims they dispute, annotating critique
type, validity and objectivity. Note: human experts still beat LLMs on important claim-centric review
tasks.

**License:** research. Ref: `arxiv.org/abs/2503.21717`.

## How Pāṭala consumes it
**PLANNED.** Pāṭala Review generates structured critiques, not "this paper is flawed":
```text
Critique: { target_claim, type, objection, source_support, alternative_reading, confidence, status: MACHINE_PROPOSED }
```

## Doctrine
A machine review is a structured, target-specific critique proposal — never a vague verdict.

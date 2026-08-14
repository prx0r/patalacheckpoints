# GraphCheck — graph-vs-graph relational drift detection

**What Pāṭala borrows:** fact-checking long-form text by extracting graph representations from both the
claims and the source, so RELATIONAL errors are detected (not just sentence-local noun errors).

**License:** research. Repo: `Yingjian-Chen/GraphCheck`.

## How Pāṭala consumes it
**PLANNED.** Long-form outputs (e.g. a 20-minute documentary script): compare the SCRIPT GRAPH against
the CANONICAL GRAPH → detect relationship drift (A-implies-B vs A-qualifies-B), not just hallucinated
nouns (`08-verification-plane.md`).

## Doctrine
Check relationship-level fidelity, not just token-level.

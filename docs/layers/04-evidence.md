# LAYER 04 — EVIDENCE (the contracts + adapters + evals)

*Part of the `globalglobal.md` spine. The scholarly-evidence substrate holding the graph together.*

## 1. What it is
The typed contracts, external adapters, and evaluation plane that every layer obeys. The
"source-evidence" directory — the reuse-first boundary where borrowed tools pour into Pāṭala-native
objects.

## 2. Purpose
Own the epistemic seam: Pāṭala borrows commodity tools but owns the semantics of evidence,
interpretation, argument, and review. Provides the canonical typed shapes (ExternalRecord,
DerivedScholarlyObject, ReviewEvent, SourceAssertion) and tests the graph from outside.

## 3. External tools used
GROBID (PDF parse) · Docling · Crossref · OpenAlex · OpenCitations · identity crosswalks (ORCID/ROR/VIAF) ·
Inspect AI (benchmark runtime). See `docs/process/external-tools.md`.

## 4. Data
- Contracts: `source-evidence/schema/` (external_record, derived_scholarly_object, source_evidence_profile,
  contracts_human_authority, text_fingerprint).
- Evals: `source-evidence/evals/` (Inspect tasks, NAT tests, golds).
- Tool registry: `source-evidence/docs/tools/MANIFEST.json` (69 tools + status).

## 5. Processes
```
Pāṭala-owned: resolve identity → SourceAssertion → CorroborationEvent → epistemic objects
Borrowed: document parse (GROBID/Docling) → metadata (Crossref/OpenAlex) → benchmark (Inspect)
```
Doctrine: authority(projection) ≤ authority(parent); content(projection) ⊆ content(parent) ∪ grounded
additions.

## 6. Implementations
- `source-evidence/schema/external_record.py` — `ExternalRecord`, `ReconciliationAdapter`.
- `source-evidence/schema/derived_scholarly_object.py` — the universal envelope + `derive_ceiling`.
- `source-evidence/schema/contracts_human_authority.py` — ReviewEvent/Proposal/Adjudication/Promotion.
- `source-evidence/schema/source_evidence_profile.py` — SourceAssertion/CorroborationEvent builders.
- `source-evidence/production/adapters/` — the external adapters.
- `source-evidence/evals/` — the benchmark plane.
- `source-evidence/docs/tools/` — the tool registry + per-tool docs.
- Tests: the 10 eval self-tests.

## 7. Docs
- `docs/process/external-tools.md` — the status board (69 tools, 6 adapter contracts).
- `docs/process/08-verification-plane.md` — the test-from-outside layer.
- `docs/process/githubclones.md` — researcher repos to raid.
- `docs/global/globalpartnerships.md` — the integration/identity strategy.

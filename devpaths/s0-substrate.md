# S0 — SOURCE-EVIDENCE SUBSTRATE COMMIT (the scholar external-tools layer)

**Status: ✅ CLOSED (2026-08-13)**
**Commit:** S0 substrate (source-evidence/ + 6-finding bundle) on local agent2

---

## Objective

Commit the S0 scholar-corpus substrate — the scholarship/external-tools side of the convergence
(per `source-evidence/docs/tool-integration.md` S0.0–S0.4 + the globalplan Phase 5). This was 100%
untracked on the local agent2 tree and is the substrate every external-tool + Atlas-NAT build writes
against.

## What was committed (56 files)

- `source-evidence/schema/` — DerivedScholarlyObject envelope, source_evidence_profile,
  contracts_human_authority (the 4 human objects).
- `source-evidence/production/` — core, build_corpus, extract/ingest, crux, and the external-tool
  adapters (GROBID, metadata_resolver, scholar_document).
- `source-evidence/evals/` — Inspect NAT harnesses (arglaundry, l200) + EVAL-CONTRACT + nat scaffold.
- `source-evidence/docs/` — scholar-layer schema-stack, evaluation-and-ids, tool-integration*,
  reuse-first-stack, INTEGRATION-SPEC.
- `data/evaluation/findings/` — the 6-finding G2 bundle.

## Excluded (per SPEC)

Scraped `docs/tools/docs-cache/` · nested `schema/schema/` dup · generated `production/store/` ·
`pilot-out/` · `__pycache__`.

## Verification

- schema imports OK
- `test_core.py` (object chain + dedup + independence) PASS
- `test_parser_invariance.py` (2/2 held) PASS

## Git-hygiene note

The first staging attempt swept in hundreds of unrelated untracked files (data/corpus, machinelearning,
pipeline, app, handover). This was reset and redone with **explicit paths**, verifying each exclude
group = 0 staged. The final commit is exactly 56 S0 files, 9294 insertions.

## Boundary / next

- This is the scholarship/evidence substrate. The external-tool **pilot** (Zotero → GROBID →
  Crossref/OpenAlex → resolver → SourceAssertion) and the **Atlas NAT** (source-reconciliation
  evaluation, Phase 5) build on this — those are the next S0 steps.
- The `schema/` files + `evals/patala/` (devpath1) + `typed_scholarly_object.py` (devpath7) were
  already tracked; this commit adds the rest.

> **ARCHIVED / SUPERSEDED** — kept for history only. Do NOT follow as current. See `docs/INDEX.md` + `docs/DOCS-AUDIT.json` for the canonical doc for this concern.

# BUILD NOTES — S0.1 scholarly-oracle vertical (2026-08-12)

## What was built
`pipeline/scholarly_oracle.py` — the first complete Pāṭala evidence object: a proposition that points
independently DOWNWARD to both primary textual evidence and exact published scholarly evidence.

Chain: PROPOSITION → PDF → external adapter → Witness → Publication → Span → SourceAssertion →
CorroborationEvent → DIRECT_SUPPORT/PARTIAL_SUPPORT.

- **External adapter** (noncanonical extraction witness): pymupdf now; **GROBID is the target** (same
  interface: tool/version/input_sha/output_sha/timestamp). The adapter id is never Pāṭala identity.
- **Publication resolver**: metadata witness (Crossref/OpenAlex/Zotero are adapters; local stub now).
- **Witness**: `pt:witness:` (source_ref, file_hash, mime, derivation, availability, rights).
- **Span**: human locator (p./§) + machine locator (quote, offsets, prefix/suffix, text hash).
- **SourceAssertion**: `pt:assertion:` (commitment ASSERTS/DENIES/ATTRIBUTES_TO/QUOTES/EDITOR_RECONSTRUCTS,
  proposition_text, generation_status MACHINE_PROPOSED, evidence_status SPAN_BOUND).
- **CorroborationEvent**: `pt:corroboration:` (target_proposition_ref, source_assertion_ref,
  relation DIRECT_SUPPORT/PARTIAL_SUPPORT/..., scope/semantic alignment, independence, defeaters).

## The first vertical (real)
- **Proposition** (IPVV/recognition): "In Utpaladeva's Īśvarapratyabhijñā, liberation is the recognition
  that one's own identity (ātman) is Śiva, and consciousness is the unity of manifestation (prakāśa) and
  self-cognition (vimarśa)."
- **Scholar A — Sanderson, Śaivism and the Tantric Traditions** (§Recognition): **DIRECT_SUPPORT**
  (witness = `shaivism_tantric_traditions_angkor.pdf`, real located span with offsets).
- **Scholar B — Brill's Encyclopedia of Hinduism vol.1**: **PARTIAL_SUPPORT** (scope OVERLAPS_CLAIM +
  1 defeater) — proves the DIRECT/PARTIAL distinction.

## S0.3 (the thin substrate serving the visions)
`render_s0_3()` renders the SAME corroboration object through bibliography / scholar-assistant /
argument-view / site-citation / education-citation — same `pt:corroboration` + `pt:assertion` IDs everywhere.

## Tests — 10/10 PASS (`test_scholarly_oracle.py`)
rename PDF (IDs stable) · delete PDF (metadata survives) · same PDF twice (no 2nd publication) ·
GROBID rerun (versionable) · wrong attribution rejected · QUOTES ≠ DIRECT_SUPPORT · scope-strengthening
flagged · offline ingest · quote changed → hash mismatch · assertion superseded → corroboration stale.

## Honest scope
- GROBID is the target adapter; pymupdf is the current fallback (the interface is GROBID-compatible).
- The publication resolver is a local stub; live Crossref/OpenAlex/Zotero are adapters to add.
- The vertical is ONE proposition; bulk ingestion (10+ PDFs) is NOT done — the 10 tests + DIRECT/PARTIAL
  distinction are proven before scaling.

## Next
SourceAssertion/CorroborationEvent registries feed CorroborationBench + TantraFact + Scholar Assistant.
Live L200 canary (5 IPVV chunks) runs in parallel (experiment, non-blocking).

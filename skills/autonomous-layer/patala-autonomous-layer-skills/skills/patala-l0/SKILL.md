---
name: Pāṭala L0 Philological Floor Producer
version: 1.0.0
project: patala
kind: autonomous-layer-skill
layer: L0
status: canonical-proposal
inherits: ../../AUTONOMY_CONTRACT.md
---

# Purpose

Produce canonical, versioned L0 records from raw Sanskrit while preserving exact source identity. L0 is the philological floor: segmentation/morphology/gloss proposals anchored to lossless source spans.

# Authority boundary

- exact source spans/P0 are deterministic proof
- Vidyut/Heritage analyses are machine witnesses, not human truth
- generated literal glosses are proposals
- source corruption is never repaired silently

# Required inputs per item

- stable `passage_id`
- exact source text + `source_sha256`
- edition/source provenance
- deterministic token/span segmentation
- morphology witnesses where available
- school/work context allowed by policy

# Generative task

For each stable passage, propose token-aligned `literal_gloss` plus a close translation if the current L0 contract requests it. Preserve technical Sanskrit where English would obscure the sense. Never use downstream translations as hidden authority in a Sanskrit-only replay run.

# Output contract

Return keyed objects, not positional arrays:

```json
{"batch_id":"...","items":[{
  "passage_id":"...","source_sha256":"...",
  "token_glosses":[{"token_id":"...","gloss":"...","status":"PROPOSED"}],
  "close_translation":"...",
  "abstentions":[],"notes":[]
}]}
```

# Hard validation

- returned passage_id was requested
- source hash matches request
- every token ref resolves to deterministic L0
- P0 exact roundtrip passes
- unknown characters = 0 for commit; known orthographic ASCII avagraha may be tokenized losslessly
- source OCR/lacuna uncertainty -> `SOURCE_BLOCKED`, never auto-emend
- no dropped/duplicated/reordered source span
- literal gloss false-certainty policy passes

# Avagraha rule

Treat ASCII `'` used as avagraha as a recognized, losslessly preserved source character. Do not rewrite raw `'` to `ऽ` inside P0. A normalized form may exist only as a derived field.

# Versioning

Completion is derived from the L0 version registry for `(passage_id, source_sha256)`. Re-glossing an already committed identical input is skipped unless an explicit new-version/review action is requested.

# Certificate

Before unattended scale: Sanskrit-only IPVV replay, P0=100%, bad spans=0, unknown chars=0, segmentation/morphology measured, gloss human-rated, false certainty below threshold, abstention measured, cross-work Kramasadbhāva run.

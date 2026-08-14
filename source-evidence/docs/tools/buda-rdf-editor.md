# BDRC RDF editor — SHACL-driven scholar edit forms

**What Pāṭala borrows:** BDRC's open web-based RDF editor driven by SHACL (React) — turning semantic
schemas into safe scholarly editing interfaces. Plus `jena-stable-turtle` (deterministic Turtle
serialization to reduce Git diff noise).

**License:** varies. Repos: `buda-base/rdf-document-editor`, `buda-base/jena-stable-turtle`.

## Why it matters (study, not embed)
Pāṭala schema → generated scholar forms → edit Person/Work/Witness/Relation → schema validation.

**Steal the deterministic-serialization principle:** canonical exports should be deterministic — same
graph → same ordering → meaningful Git diffs. Apply everywhere.

## How Pāṭala consumes it
**PLANNED.** Study how schemas → safe scholarly edit forms. Apply deterministic serialization to
canonical exports.

## Doctrine
Don't embed their editor; steal the schema→form generation + deterministic serialization principles.

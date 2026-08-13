# RO-Crate — portable corpus / benchmark packaging

**What Pāṭala borrows:** packaging files + resources + JSON-LD metadata (people, organizations, software,
provenance, licensing, relationships) into a portable **Research Object Crate** for export/archive/interchange —
**NOT Pāṭala's database**. Emit RO-Crates for the corpus, benchmark releases, and (later) TantraFact/Benchmark
crates.

**License:** Apache-2.0 (spec + Python library `rocrate`). No server — it's a packaging format + library.

## API / usage (no remote API)
- Python library: `pip install rocrate`, then `rocrate.RoCrate()`, `crate.add_workflow()`,
  `crate.add_workflow_run()`, `crate.write()` (creates `ro-crate-metadata.json` + the file tree).
- Structure:
  ```
  my-corpus/
    ro-crate-metadata.json   (the JSON-LD metadata graph)
    files/                   (contained resources)
  ```
- `@id: ./` is the root Dataset; every file/resource is a node in `@graph` with `conformsTo` the RO-Crate
  profile; external (non-redistributable) resources are referenced by URI without bundling.
- RO-Crate 1.3 is extensible with additional linked-data vocabularies (FaBiO/PROV/Web Annotation) rather than
  demanding one giant ontology — exactly the profile-composition we want.

## Rate limiting / etiquette
None — it's local packaging. The etiquette is about *what you put in the crate*: record fixity (sha256),
software versions (`conformsTo` + the exact tool version), licenses, and provenance so a released crate is
self-describing and reproducible.

## How Pāṭala consumes it
```
Emit: Pāṭala IPVV Research Corpus v1 / Sanderson Corpus Index / Argument Benchmark v1 / TantraFact v1
   as RO-Crates containing the benchmark objects + gold refs + source ids + licenses + eval scripts.
```
Use as export/interchange; keep the canonical epistemic graph native (the earlier RO-Crate pilot in
`source-evidence/ro_crate.py`).

# I3 — the source resolver slice

*2026-08-13. The Agent 2 side of the Agent 1 Atlas NAT contract: resolve a work's identity + edition +
etext provenance against external authorities and record **per-dimension** AuthorityEvidence in the
Atlas Postgres.*

## The contract (mirrors ARGMAP NAT)

```text
Agent 2 resolver  →  SourceResolutionCandidate  →  Agent 1 Atlas NAT  →  SourceResolutionFinding[]
```

The resolver **proposes**; Agent 1 **evaluates**. The resolver never says "THIS IS DEFINITELY THE
TANTRĀLOKA" — it returns candidates + evidence + open dimensions. Agent 1 decides trust.

## Multidimensional authority (the Agent 1 requirement)

Authority is **per-dimension**, never a single `verified=true` or a lone `authority_state:
EDITION_VERIFIED` string:

```json
{
  "authority": {
    "WORK_IDENTITY":    {"relation": "MULTI_SOURCE_MATCHED", "source_scheme": "ATLAS_CROSSWALK"},
    "AUTHOR_IDENTITY":  {"relation": "UNSUPPORTED",          "source_scheme": "NONE"},
    "EDITION_IDENTITY": {"relation": "DISCOVERED",           "source_scheme": "ARCHIVE_ORG"},
    "ETEXT_DERIVATION": {"relation": "OPEN",                 "source_scheme": "UNRESOLVED"},
    "WITNESS_LINKAGE":  {"relation": "OPEN",                 "source_scheme": "UNRESOLVED"},
    "DATE_PRECISION":   {"relation": "OPEN",                 "source_scheme": "UNRESOLVED"},
    "RIGHTS":           {"relation": "OPEN",                 "source_scheme": "UNRESOLVED"}
  }
}
```

Unresolved dimensions stay **OPEN / UNSUPPORTED** — no provenance theatre. Convenience gates are
**explicit predicates** derived from the vector:

```text
factory_eligible        WORK_IDENTITY is CATALOG_MATCHED / MULTI_SOURCE_MATCHED
publication_eligible    EDITION_IDENTITY is MULTI_SOURCE_MATCHED / COPY_INSPECTED / EDITION_VERIFIED
scholar_review_eligible WORK_IDENTITY MULTI_SOURCE_MATCHED or EDITION_VERIFIED+
```

## The authority ladder (shared vocabulary)

```
DISCOVERED → CATALOG_MATCHED → MULTI_SOURCE_MATCHED → COPY_INSPECTED
→ EDITION_VERIFIED → TEXT_DERIVATION_VERIFIED → SCHOLAR_CONFIRMED
```

## Run

```bash
python3 python/patala_core/atlas/resolver.py --work matangaparamesvara            # resolve (network)
python3 python/patala_core/atlas/resolver.py --work matangaparamesvara --no-net   # offline (crosswalk only)
python3 python/patala_core/atlas/resolver.py --work matangaparamesvara --persist  # write authority_evidence rows
```

## Adapters (reuse-first, per the authority stack)

- **archive.org** (`_archive_search`) — edition/translation candidate discovery
- **ATLAS_CROSSWALK** — the migrated legacy→uuid identity (WORK_IDENTITY baseline)
- **GRETIL / NCC / NMM / NGMCP / SARIT / Muktabodha + library catalogs** — future adapters (I3b)

Each adapter produces evidence, never automatic truth. Source-independence matters: multiple catalogues
echoing the same upstream record is NOT independent corroboration (Agent 1's `SOURCE_ECHO` concern).

## Files

| File | Role |
|---|---|
| `resolver.py` | `resolve_work()` → SourceResolutionCandidate · `persist_evidence()` → Atlas |
| `test_resolver.py` | multidimensional-authority + honesty tests (ALL PASS) |

## The exit gate (met)

The resolver produces the exact candidate shape Agent 1's Atlas NAT consumes — multidimensional,
honest, gate-predicated — and can persist per-dimension evidence to the Atlas. Tests ALL PASS.

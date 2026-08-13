# VISION 15 — THE PĀṬALA ATLAS (the Sanskrit Research Graph) — "OpenAlex for Sanskrit"

*2026-08-13. The strategic upgrade: promote the bibliography from "supporting metadata for the factory"
into **the authoritative research graph that the factory is downstream of**. The Atlas is the base-layer
product — the identity/provenance layer for the Śaiva tradition first, then Vedic, then Pāli/Tibetan/Greek/
Latin/Arabic. This is not a new project — it formalizes the substrate already built (bibliography, source_ready
signal, catalog, registries, factory hooks).*

---

## 1. THE ONE-LINE FRAMING

> **Pāṭala Atlas = "OpenAlex for Sanskrit"** — the canonical authority + bibliography + manuscript + edition
> research graph. Its killer difference from OpenAlex: OpenAlex models modern scholarly works/authors/
> institutions/citations; the Atlas models **textual transmission** — the real, provable lineage from a
> physical manuscript to the text the factory translates.

And the layering that makes it a product, not just data:

```text
ATLAS     what exists + where + which version/witness?
    ↓
FACTORY   what can we derive from it?
    ↓
EPISTEMIC CORE   what is actually supported?
```

---

## 2. THE BASE GRAPH (the object model)

```text
PĀṬALA ATLAS / SANSKRIT RESEARCH GRAPH

Work
Author
Edition
Manuscript Witness
Digital Surrogate
Transcription
E-text
Translation
Scholarship
Institution
Identifier
Rights
Relationship
```

The **textual transmission** spine — this is what OpenAlex cannot do:

```text
WORK
  ↓ has edition
EDITION
  ↓ constituted from
MANUSCRIPT WITNESSES
  ↓ represented by
DIGITAL SURROGATES
  ↓ transcribed as
TRANSCRIPTIONS
  ↓ normalized/published as
E-TEXTS
  ↓ selected as
PĀṬALA SOURCE
  ↓ then the factory
SOURCE → translation → proposition → argument → review → essay → education
```

---

## 3. THE IDENTITY RULE (do not collapse identity)

This is the single most important discipline, and it is exactly the "no fake `verified=true`" lesson.

**Keep these distinct — never merge them:**

```text
Tantrāloka                  = WORK
Kaul edition                = EDITION
specific manuscript         = WITNESS
Bodleian scan               = SURROGATE
GRETIL file                 = E-TEXT
Pāṭala-selected text basis  = SOURCE
```

Each record carries **authority evidence** (an attestation about which catalogs/authorities matched,
with confidence), not a single collapsed boolean.

---

## 4. RECONCILIATION ACROSS THE AUTHORITY STACK

There is **no one Sanskrit API**. The Atlas reconciles a touched work across the sources we trust, in
parallel, with the reconciliation pattern (candidate → authority → confidence → auto/review/unresolved):

```text
WORK IDENTITY        NCC (New Catalogus Catalogorum)
MANUSCRIPT WITNESSES NMM / Pandulipi Patala (India), NGMCP (Nepal)
E-TEXTS              GRETIL · SARIT · Muktabodha
SURROGATES/IIIF      Bodleian · OCHS
PRINTED EDITIONS     Google Books · HathiTrust · LoC · WorldCat
MODERN SCHOLARSHIP   Crossref · OpenAlex (this is where OpenAlex IS used — for the scholarship layer)
AUTHORS              ORCID
INSTITUTIONS         ROR
```

---

## 5. LAZY, RECONCILIATION-DRIVEN (never bulk-ingest)

Exactly as the bibliography strategy already says — do **not** ingest every Sanskrit record on earth.
When a text enters the genealogy / factory / research path:

```text
touch work
→ resolve aliases
→ query Sanskrit authorities      (NCC, NMM, NGMCP)
→ query manuscript catalogs
→ query editions                  (Google Books / HathiTrust / LoC / WorldCat)
→ query digital repositories      (SARIT / GRETIL / Muktabodha / IIIF)
→ cache candidate graph
→ human confirm ambiguous matches
→ promote
```

Manageable. No dump.

---

## 6. THE API (already the shape of what we built)

```text
GET /works/tantraloka
GET /works/tantraloka/editions
GET /works/tantraloka/manuscripts
GET /works/tantraloka/etexts
GET /works/tantraloka/translations
GET /works/tantraloka/scholarship
GET /works/tantraloka/relationships

GET /resolve?title=tantraloka
GET /search?author=abhinavagupta
GET /witnesses?repository=bodleian
GET /timeline?tradition=krama
```

Then MCP verbs for agents:

```text
resolve_work
find_editions
find_manuscripts
find_translations
find_scholarship
trace_textual_lineage
compare_editions
```

This alone is already a real product for researchers and AI agents.

---

## 7. WHY THIS IS ALREADY PARTLY BUILT (it's a formalization, not a rewrite)

Agent 2 has accidentally built the substrate:

| Atlas piece | Existing |
|---|---|
| Bibliography | `data/atlas/` (254 records, school/period/translations) |
| Quality signal | `source_ready.py` (CLEAN/READY/PRIORITY) |
| Catalog | `pipeline/catalog.py` + `/api/factory/quality` |
| Registries (versioned) | `data/corpus/registries/` |
| Verification v1 | `verify_editions.py` (attestations, authority ladder) |
| Factory hooks | factory loop + auto-intake |

The upgrade is **framing + the identity distinction + the reconciliation stack** — not new code from
scratch.

---

## 8. INSTITUTIONAL INTEGRATION (the partnership moat)

The Atlas makes institutional collaboration trivial because it is **upstream nodes**, not adoption of the
translation system:

> A manuscript project gives you IIIF manifests or catalog records. They don't need to adopt Pāṭala's
> translation system. They become upstream nodes in the graph, and Pāṭala adds downstream value.

```text
OCHS / Bodleian owns: images, cataloguing, HTR ground truth, manuscript expertise
PĀṬALA adds:          source reconciliation, translation audit, argument/evidence graph,
                      dependency analysis, scholar review, education/media projections
```

Complementary, not competing.

---

## 9. GENERALIZABILITY (language-independent base graph)

The base graph is highly generalizable:

```text
Sanskrit → Pāli → Tibetan → Greek → Latin → Arabic
```

because `Work / Edition / Witness / Surrogate / Transcription / Scholarship` is **language-independent**.
Only the text-processing compiler changes. (This is the same claim as the GlossLM / universal-kernel
argument — the Atlas is the universal identity layer, the compiler is the per-language layer.)

---

## 10. THE THREE-LAYER STRATEGIC POSITION

> **The Atlas = the identity/provenance layer. The Factory = the transformation layer. The Epistemic Core =
> the trust/reasoning layer.**

```text
ATLAS      what exists + where + which version/witness?
    ↓
FACTORY    what can we derive from it?
    ↓
EPISTEMIC CORE   what is actually supported?
```

This is the meaningful strategic upgrade: the current bibliography stops being "supporting metadata for
the factory" and becomes **the authoritative research graph that the factory is downstream of.**

---

## 11. IMPLEMENTATION ORDER (depth before width)

```text
E0  Formalize the Atlas object model (Work/Edition/Witness/Surrogate/Transcription/E-text/Source distinct)
E1  Finish the identity distinction in the atlas (separate Work/edition/source fields; authority evidence, not verified=true)
E2  Wire verify_editions.py into source_ready (source_ready depends on resolution, not just clean-on-disk)
E3  The read API over the Atlas (works/editions/manuscripts/etexts/translations/scholarship/relationships)
E4  The reconciliation stack adapters (NCC/NMM/NGMCP/SARIT/GRETIL/Muktabodha + Google Books/HathiTrust/LoC/WorldCat + IIIF)
E5  The MCP verbs (resolve_work, find_editions, trace_textual_lineage, …)
E6  Source_ready upgrade: clean AND work_identity_resolved AND edition_identity AND rights_ok AND provenance_ok
E7  Institutional ingest (IIIF manifests, catalog records as upstream nodes)
```

**Do NOT build the whole reconciliation stack at once.** Prove the Atlas model + API on the existing
corpus (E0–E3), then add adapters (E4) and MCP (E5) as sources are touched.

---

## 12. THE CARRY-FORWARD

> **Pāṭala Atlas = "OpenAlex for Sanskrit": the canonical authority + bibliography + manuscript + edition
> research graph, modeling textual transmission (Work→Edition→Witness→Surrogate→Transcription→E-text→Source),
> reconciled lazily across NCC/NMM/NGMCP/GRETIL/SARIT/Muktabodha + library catalogs + IIIF, exposing the
> identity/provenance layer that the Factory (transformation) and Epistemic Core (trust) are downstream of.
> Mostly already built as the bibliography + quality signal + catalog + registries — the upgrade is the
> identity distinction, the reconciliation stack, and the read API.**

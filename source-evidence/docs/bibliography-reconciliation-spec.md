# Bibliography Reconciliation Spec — Pāṭala's current bibliography × external tool (Zotero)

*2026-08-13. How Pāṭala's existing `BibliographyRecord` layout (which is kept UNCHANGED as the canonical identity
+ epistemic layer) reconciles with Zotero as the external bibliographic-management/citation backend. This is a
spec for review — not a build. The reconciliation is **additive**: a crosswalk on top of the current layout,
never a replacement of it.*

---

## 0. Principle (the split, not a swap)

```
Pāṭala BibliographyRecord (canonical identity + epistemic gate)   ← stays as-is, the source of truth for site/API
        ↕  crosswalk (additive)
Zotero item (management + citation formatting + sync)  ↔  DOI  ↔  OpenAlex  ↔  OpenCitations
```

- **Pāṭala owns:** identity (`pt:src:*`), the epistemic fields (`verified`, `state`, `tier`, `translationStatus`,
  `statusLabel`, `statusChecked`, `statusEvidence`), the scholar-facing structure (`translations[]`, `textSources[]`,
  `manuscripts[]`, `rights` enum, `notes`).
- **Zotero owns:** bibliographic CRUD, attachments, versioning, `since=` incremental sync, formatted citations
  (CSL/citeproc), BibTeX/RIS/TEI export.
- **No external provider owns identity.** Replacing Zotero/OpenAlex later must not invalidate Pāṭala IDs or
  epistemic fields.

---

## 1. Additive field (the only change to the layout)

Add ONE optional field to `BibliographyRecord` (backward-compatible — absent = no external link):

```ts
export interface BibliographyCrosswalks {
  zotero?: { library_id: string; item_key: string };
  doi?: string;
  openalex?: string;        // OpenAlex work id (W...)
  opencitations?: string;   // OpenCitations id
  // metadata witnesses are preserved as received (never silently merged)
  witness?: { source: "zotero" | "openalex" | "crossref" | "opencitations";
              title?: string; year?: number; doi?: string; }[];
}
```
Added to `BibliographyRecord` as optional `crosswalks?: BibliographyCrosswalks;`. Everything else in the current
layout is untouched.

---

## 2. The reconciliation contract (field-by-field)

| Pāṭala `BibliographyRecord` field | Source of truth | Zotero role |
|---|---|---|
| `id` (`pt:src:*`) | **Pāṭala** (canonical) | referenced via crosswalk (`zotero.item_key`) |
| `work`, `traditions`, `period` | **Pāṭala** | never overwritten by Zotero |
| `verified`, `state`, `tier` | **Pāṭala** (epistemic gate) | Zotero has no equivalent; stays native |
| `translations[]` (language/coverage/type/complete) | **Pāṭala** (curated) | Zotero may hold a copy but Pāṭala's is authoritative |
| `textSources[]` (edition/etext/scan + tier) | **Pāṭala** | Zotero attachments ↔ `textSources` via crosswalk |
| `translationStatus`/`statusLabel`/`statusChecked` | **Pāṭala** | not in Zotero; stays native |
| `rights` (enum) | **Pāṭala** (curated) | Zotero/Crossref may *suggest*; Pāṭala's enum is authoritative |
| `scholarship[]` | **Pāṭala** | Zotero items can back these |
| title/author/year/venue/DOI | **Zotero + OpenAlex + Crossref** (metadata witnesses) | Zotero is the primary manager; enrichment proposes |
| formatted citation | **Zotero/CSL** | Pāṭala delegates, never writes its own citation engine |

**Rule: external metadata is a WITNESS, not an authority.** Zotero/OpenAlex/Crossref may *propose* metadata; the
canonical decision (what the site/API serves) is Pāṭala's, and must be **deterministic**. On disagreement
(e.g. GROBID title = A, OpenAlex title = A', Crossref = A), preserve each as a `witness[]` entry and let Pāṭala's
record keep its decision — **never silent majority-vote.**

---

## 3. Sync flow (bidirectional, `since=` based)

```
ZOTERO → PĀṬALA   (pull): Zotero `since=` incremental → Pāṭala resolver upserts the crosswalk + attachments;
                     Pāṭala-native fields are NEVER overwritten; new/changed metadata lands in `witness[]`.
PĀṬALA → ZOTERO   (push): a Pāṭala edit (e.g. a new translation or a verified flip) mirrors the bibliographic
                     fields to the Zotero item; the epistemic fields stay Pāṭala-only.
```

## 4. Merge / disagreement rules (the critical part)

1. **Never overwrite Pāṭala-native fields** (`verified`, `state`, `tier`, `translations`, `statusLabel`, `rights`
   enum) from an external source — audited records (e.g. the Trika-10, `verified:true`) are immutable against
   external metadata.
2. **Preserve witnesses:** each external provider's value is kept as a `witness[]` entry; the canonical decision is
   Pāṭala's and deterministic.
3. **External enrichment is optional:** if OpenAlex/Crossref/Zotero is UNAVAILABLE (429/timeout/offline), local
   source identity still succeeds; enrichment = `PENDING`/`UNKNOWN`. Never require an external call for basic
   identity.
4. **Zotero is replaceable:** a future bibliography tool must be able to replace Zotero without touching Pāṭala's
   `pt:*` IDs or epistemic fields (the acceptance criterion).

## 5. Acceptance criteria

- `resolve(pt:src:...)` returns the same canonical record regardless of which external tool is up.
- A Pāṭala edit never loses its epistemic fields to Zotero.
- The audited (`verified:true`) records are never mutated by external metadata.
- `rights: "unknown"` still allows metadata/citation/private scholarly analysis, but does not imply redistribution
  permission.
- Removing/renaming a source file breaks no reference (the hard-stop criterion 6).

## 6. Status

**Spec for review — no build.** Implementation, if approved, is the `adapters/zotero.py` + `resolver.py` +
`crosswalk` from `tool-integration.md`, with the LIVE/RECORDED/UNAVAILABLE testing rule. Your current bibliography
layout is preserved verbatim; only the optional `crosswalks` field is added.

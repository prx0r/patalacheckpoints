# Concepts — Work vs witness vs passage

Pāṭala ruthlessly separates the *abstract intellectual object* from its *concrete manifestations* and from *addressable text*. This is the BDRC/SARIT discipline, adapted.

```
WORK         the abstract intellectual object (e.g. "Kubjikāmatatantra")
   │
   ├─ WITNESS / SOURCE     a concrete manifestation (a manuscript, an edition, an e-text)
   │     │
   │     └─ DIGITAL SURROGATE   a scan/image representation (IIIF, not hosted by us)
   │
   └─ PASSAGE        one addressable unit of text (tantra:text:kubjikamata:3.14)
```

## The three objects

| Object | Endpoint | Example | What it is |
|---|---|---|---|
| **Work** | `/api/works/{id}` | `kramasadbhava` | the abstract intellectual object |
| **Manuscript / witness** | `/api/manuscripts` | `pt:ms:ochs_...` | a concrete manifestation (custodian OCHS) |
| **Passage** | `/api/passages/{id}` | `tantra:text:kramasadbhava:1.2` | one addressable verse/segment |

## Why keep them separate

- A **work** is one thing with many witnesses (a critical edition, a manuscript, a GRETIL e-text) that may disagree at a locus.
- A **passage** belongs to a work and carries a *location* (`{chapter, verse}`) and a *source_edition* — it is addressed by a stable id, never by its URL.
- A **manuscript** is a *witness of a work*, and Pāṭala resolves OCHS records to works via curated crosswalks — but the manuscript data stays owned by OCHS.

Root and commentary are also separate records (e.g. `paratrisika` root vs `paratrisikavivarana`), so coverage and status never blur across layers.

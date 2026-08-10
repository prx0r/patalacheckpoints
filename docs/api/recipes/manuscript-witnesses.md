# Recipe — Trace manuscript witnesses

Determine which manuscripts witness a work, and where they live. The manuscript layer comes from **OCHS** (custodian), CC BY-NC-SA 4.0 — Pāṭala resolves OCHS records against its own work-authority graph but never claims ownership.

## 1. Get a work's witnesses

```bash
curl "http://localhost:3000/api/works/netratantra/manuscripts"
```

```json
{
  "work_id": "netratantra",
  "count": 5,
  "manuscripts": [
    {
      "id": "pt:ms:ochs_000_000_002_amrtesatantram",
      "ochs_slug": "ochs_000_000_002_amrtesatantram",
      "custodian": "OCHS",
      "licence": "CC-BY-NC-SA-4.0",
      "source_url": "https://ochs-database.netlify.app/manuscripts/ochs_000_000_002_amrtesatantram/",
      "photos": true,
      "text": true,
      "title": "Amṛteśatantram",
      "catalogueIds": "...",
      "script": "...",
      "dateOriginal": "..."
    }
  ]
}
```

Each record preserves its source URL and licence. Link out for images; don't ingest them.

## 2. Search all manuscripts

```bash
curl "http://localhost:3000/api/manuscripts?q=netra"
curl "http://localhost:3000/api/manuscripts"                       # all 1,542
curl "http://localhost:3000/api/manuscripts?work_id=kubjikamata"   # one work's
```

## 3. Trace provenance of a passage (the chain)

For any passage, walk the evidence chain back to a source:

```
passage → work → source edition → upstream repository
```

`GET /api/context/passages/:id` returns the `work` with its `source_editions` and `rights`, and the OCHS `manuscripts` with their `source_url`. That chain is how a claim terminates in a real, citable source.

---

**MCP:** `get_manuscripts({ work_id })` / `get_manuscripts({ q })`.

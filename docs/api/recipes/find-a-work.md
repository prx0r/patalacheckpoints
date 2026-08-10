# Recipe — Find a work

How to discover what works exist and drill into one.

## 1. List works by tradition

```bash
curl "http://localhost:3000/api/works?tradition=Krama"
```

`tradition` accepts a label (`Krama`) or id (`krama`). Response:

```json
{
  "count": 11,
  "works": [
    {
      "id": "kramasadbhava",
      "urn": "tantra:text:kramasadbhava",
      "title": "Kramasadbhāva",
      "traditions": [{ "id": "krama", "label": "Krama", "certainty": "medium" }],
      "translation_status": "partial",
      "verified": false,
      "working_translations": 570,
      "manuscripts": 0
    }
  ]
}
```

Filter by translation status and audit state too:

```bash
curl "http://localhost:3000/api/works?tradition=Krama&status=none"
curl "http://localhost:3000/api/works?verified=true"
```

## 2. Get the full bibliography for a text (the "WHAT EXISTS?" record)

The bibliography (`/api/texts`) is the spine — what exists, what's translated, what scholarship exists.

```bash
curl "http://localhost:3000/api/texts/kubjikamata"
```

```bash
# which Krama texts lack a complete English translation? (a question an agent can now answer)
curl "http://localhost:3000/api/texts?tradition=Krama&status=none"
```

## 3. Get one work's full metadata

```bash
curl "http://localhost:3000/api/works/tantra:text:kramasadbhava"
```

Accepts the bare id or the urn.

---

**MCP:** the same operations are `get_work({ id })` and `search_passages` / the `/api/texts` list. See [MCP mapping](mcp.md).

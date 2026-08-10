# Recipe — Read a passage + its evidence bundle

The passage is the fundamental addressable scholarly unit. Every translation, note, variant and citation hangs off a stable passage id.

## 1. Read a passage

```bash
curl "http://localhost:3000/api/passages/tantra:text:kramasadbhava:1.2"
# or the bare form
curl "http://localhost:3000/api/passages/kramasadbhava:1.2"
```

Response:

```json
{
  "data": {
    "id": "tantra:text:kramasadbhava:1.2",
    "work_id": "kramasadbhava",
    "location": { "chapter": 1, "verse": 2 },
    "sanskrit": "tasmiṃ cakre mahāghore ... * * * * * * * *(?)",
    "source_edition": "Dyczkowski ed., Muktabodha (MS 1-76 Saivatantra 144; NGMPP A 209/23)"
  },
  "provenance": { "api_version": "1.0" }
}
```

The `* * * * (?)` marks are the source manuscript's corrupt/lacunose loci — preserved, not silently repaired.

## 2. Get the evidence bundle (the important one)

`GET /api/context/passages/:id` is a **deterministic evidence packet** — it assembles everything about a passage with **no generated interpretation**:

```bash
curl "http://localhost:3000/api/context/passages/tantra:text:kramasadbhava:1.9"
```

Response keys:

```
passage          the Sanskrit + edition
work             the parent work's metadata + rights
manuscripts      OCHS manuscript witnesses
neighboring      previous / next passages (resolve)
tracked_terms    accepted senses for core technical lemmas
related_works    typed relations (for context ranking)
translations     note about our working T1s
provenance       source note
```

Example:

```json
{
  "passage": { "id": "tantra:text:kramasadbhava:1.9", "sanskrit": "namo nitye tvanitye ca ..." },
  "work": { "id": "kramasadbhava", "title": "Kramasadbhāva", "translation_status": "partial" },
  "neighboring": {
    "previous": { "id": "tantra:text:kramasadbhava:1.8" },
    "next": { "id": "tantra:text:kramasadbhava:1.10" }
  },
  "tracked_terms": [ { "lemma": "kula", "senses": ["lineage / family", "body / power / totality"] } ]
}
```

**Why this matters:** it's the packet a translator or an LLM needs to *ground* a rendering — the same-text usage, the witnesses, the neighboring context, the term policy — without hallucinating. It contains evidence, not answers.

## 3. Our working translations for a work

```bash
curl "http://localhost:3000/api/texts/kubjikamata/translations"
```

Returns verse-anchored passages with our T1 `close_translation`, staged as `T1`, with a **"NOT peer reviewed; provisional"** provenance note. Use for comparison and calibration — never copy verbatim.

## 4. Search the corpus

```bash
curl "http://localhost:3000/api/search/passages?q=khecar&work_id=kubjikamata"
```

This is **substring** search over Sanskrit + working translation + id. `limit` defaults to 50.

---

**MCP:** `get_source_passage({ passage_id })`, `get_passage_context({ passage_id })`, `get_working_translations({ work_id })`, `search_passages({ q })`.

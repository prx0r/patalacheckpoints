# The Corpus Manifest — text registry + passage API

*The foundational artifact: what texts do we have, what are they, where do they sit historically, and how do we retrieve exact passages? Build this BEFORE the translation MCP. You already have the raw ingredient (hundreds of Sanskrit texts); what's needed is a catalogue that makes those files computable.*

## Minimum architecture

```text
WORK
  ↓
EDITION / SOURCE
  ↓
PASSAGES
  ↓
TOKENS / LEMMAS
```

## Work metadata

```json
{
  "id": "tantrasadbhava",
  "title": "Tantrasadbhāva",
  "authors": [],
  "traditions": ["Bhairava", "Trika-related"],
  "date": { "not_before": 900, "not_after": 1000, "certainty": "approximate" },
  "region": ["Kashmir"],
  "genres": ["tantra"],
  "languages": ["sa"],
  "source_editions": ["muktabodha:M..."],
  "translation_status": "partial"
}
```

## Passage

```json
{
  "id": "pt:tantrasadbhava:3.14",
  "work_id": "tantrasadbhava",
  "location": { "chapter": 3, "verse": 14 },
  "sanskrit": "...",
  "source_edition": "...",
  "tokens": []
}
```

## MCP queries it enables

```text
search_texts(traditions=["Krama"], date_from=850, date_to=1050)
search_passages(lemma="kula", work_ids=[...])
read_passage("pt:kramasadbhava:4.17")
```

## Key metadata fields

stable `work_id` · title + alternate titles · author/attribution · traditions (array) · approximate date range + certainty · region · genre · parent/related texts · source edition · manuscript witnesses · translation status · passage segmentation.

## Relationship edges from the start

```json
{
  "source": "tantrasadbhava",
  "target": "malinivijayottara",
  "relation": "textually_related",
  "certainty": "high",
  "evidence": []
}
```

Retrieval ranking: 1. same work · 2. direct textual relative · 3. same author · 4. same tradition · 5. adjacent tradition · 6. same date range · 7. wider tantric corpus.

## The first API (extremely small)

```http
GET /works
GET /works/{id}
GET /passages/{id}
GET /search/passages
GET /search/works
GET /relations/{work_id}
```

```http
GET /works?tradition=krama
GET /works?author=abhinavagupta
GET /works?date_from=900&date_to=1050
GET /search/passages?lemma=vimarsa
GET /search/passages?q=śakticakra
```

## MCP tools (simple first)

```text
list_texts
get_text
read_passage
search_corpus
find_term
get_related_texts
```

Then the clever stuff (after): `find_historical_usage` · `find_parallels` · `get_translation_context` · `audit_translation`.

## Build order

```text
1. normalize corpus files
2. create work registry
3. assign metadata
4. segment every text
5. assign stable passage IDs
6. expose passage/search API
7. add MCP
8. add lemma/morphology indexing
9. add translation workflow
10. add historical/contextual retrieval
```

## Don't wait for perfect metadata

Give uncertain metadata explicit confidence:

```json
{
  "date": { "not_before": 950, "not_after": 1050, "certainty": "low", "sources": [] }
}
```

```json
"traditions": [
  { "id": "trika", "relationship": "reception", "certainty": "high" },
  { "id": "vidyapitha", "relationship": "textual_origin", "certainty": "medium" }
]
```

Better than forcing historically messy texts into a rigid folder taxonomy.

## The artifact

```text
corpus/
  works.json
  relations.json
  texts/
    tantrasadbhava.jsonl
    kubjikamata.jsonl
    kramasadbhava.jsonl
    tantraloka.jsonl
```

with each `.jsonl` containing addressable passages. Once that exists, ChatGPT through MCP can navigate the corpus intelligently instead of doing glorified full-text grep.

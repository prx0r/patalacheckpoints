# Concepts — Rights

Pāṭala tracks **operational permissions**, not just a license string. For every resource it can answer independently what you may do with it. **`unknown` is a valid and honest answer.**

## The permission matrix

| Permission | Question |
|---|---|
| `public_display` | may it be shown? |
| `download` | may it be downloaded? |
| `redistribution` | may it be redistributed? |
| `api_fulltext` | may full text be served through the API? |
| `index_search` | may it be indexed/searched? |
| `embed` | may it be embedded? |
| `rag` | may it be used in RAG? |
| `embeddings` | may embeddings be created? |
| `model_training` | may it be used for model training? |
| `evaluation` | may it be used for evaluation? |
| `commercial_feed` | may it be commercially licensed as a feed? |

Each can be `yes | no | unknown | conditional`.

## The cardinal rule

> **Never infer permissions from public accessibility.**

"Publicly accessible" ≠ "commercial ML training allowed." Most manuscript sources are owned by custodians (OCHS, Muktabodha, GRETIL, IFP). Our own working translations are ours; upstream material retains its own rights. `rights` on a work (`/api/works/{id}`) records this and, where unresolved, stays `unknown` rather than assuming open.

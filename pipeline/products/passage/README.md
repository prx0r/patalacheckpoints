# passage — Passage / Reading (#3)

A **standalone** philology-facing primitive: a canonical Passage object + a deterministic KG2Code-style
query engine over the real IPVV passage graph. Borrows the proven `KnowledgeQuery` pattern from
fuck-off's `lib/query.py`, re-expressed against PĀṬALA's real passages.

## What it provides
- **canonical Passage** — source Sanskrit + L2 + C1 + immutable_id + work
- **resolve / neighbors / path / evidence** — deterministic graph queries (no embeddings, CPU-only)
- **human-friendly resolution** — "chunkD" → the full canonical passage

## Run
```bash
cd /root/patalacheckpoints
PYTHONPATH=pipeline python3 pipeline/products/passage/test.py          # 6/6 proof
PYTHONPATH=pipeline python3 pipeline/products/passage/engine.py "chunkD" get
PYTHONPATH=pipeline python3 pipeline/products/passage/engine.py "chunkD" neighbors
```

## Engine API
```python
from products.passage.engine import make_query
q = make_query()
p = q.get("chunkD")            # canonical passage
nb = q.neighbors("chunkD")     # same-work neighbors
paths = q.path("chunkA", "chunkD", max_hops=4)
ev = q.evidence("chunkD")      # evidence state
```

## Honest limits
- Adjacency = same-work + shared-term links (lexical, not semantic embedding).
- The full L2 readable-prose chain (L0→L1→L2 registry) is upstream; this reads the committed IPVV.

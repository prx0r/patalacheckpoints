# S2ORC — modern-science structured corpus (later)

**What Pāṭala borrows:** a large general-purpose structured scientific literature corpus (AllenAI). It will not
help Sanskrit humanities, but when Pāṭala expands into **consciousness science / neuroscience / Friston / Seth /
Solms / Levin / active inference**, there's no reason to PDF-ingest that literature at the same scale manually.

**License:** research corpus; distributed via Semantic Scholar API/bulk data.

## Usage
Bulk data / Semantic Scholar API. Keep the split:
```
Sanskrit/humanities:  our curated corpus (GROBID/Docling pipeline)
modern science:       S2ORC / Semantic Scholar substrate
   → normalize BOTH into Pāṭala SourceAssertion
```

## How Pāṭala consumes it
Feeds the modern-science side of the scholar oracle (and baselines) later — same `SourceSpan → SourceAssertion →
CorroborationEvent` seam. No need now.

**Priority: LATER.**

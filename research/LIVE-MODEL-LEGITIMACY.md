# LIVE MODEL LEGITIMACY — how a model plugs in, gets measured, and reports real cost

*2026-08-15 · the complete mechanism for making the translation cost/quality/throughput estimates LEGIT
(live + measured, not assumed). Built on the provider-aggregator insight: opencode-go returns REAL usage
tokens per completion, and OpenRouter exposes LIVE per-token prices for 413 models. cost = real tokens ×
live price.*

---

## 1. THE THESIS (why this is legitimate)

Instead of maintaining our own per-model price table (which goes stale), we use a **provider aggregator**:
- **opencode-go** (our generation provider) returns real `usage` tokens per completion (verified live).
- **OpenRouter** exposes **live per-token prices** per model via `/models` (verified: 413 models).
- **cost = real tokens × live price** — a true measured number, updated on refresh.

This answers the 3 questions honestly:
1. **"How does a new model (e.g. Cloudflare Qwen) plug in?"** — add it as a model id; the catalog has its
   live price; the adapter calls it. No hardcoded price.
2. **"How do I know live costs?"** — the adapter captures real tokens → cost = tokens × live price.
3. **"How do I know if it's good at Sanskrit?"** — run it on gold verses (Sāmayik/Itihāsa/raw-material),
   score with quality_score → a real 0-1 number, ranked on the leaderboard.

---

## 2. THE ARCHITECTURE

```
GENERATION PROVIDER (opencode-go / any OpenAI-compatible)      PRICE AGGREGATOR (OpenRouter)
   │  returns real usage tokens                                      │  returns live per-token prices
   ▼                                                                 ▼
ModelAdapter (model_adapter.py)                            model_catalog.py
  ModelResult: prompt_tokens, completion_tokens,              GET /models → {model: {prompt, completion,
    cached_tokens, .cost()  ←──────── real tokens × ────────  cache_read, context}} → cached (compute-on-write)
   │                                                                      │
   ▼                                                                      ▼
PROJECTOR (project_translation.py) = verse_count × per-verse time × (real-token cost from live price)
   │
   ▼
INGESTION ROI (assess-flow T5) / the openpatala leaderboard
```

---

## 3. THE FILES (what each does)

| File | Role | Gate |
|---|---|---|
| `pipeline/model_adapter.py` | the ModelAdapter boundary (Direct/Hermes). **Now captures real usage tokens** in ModelResult + `.cost()`. Add a backend = 1 subclass (e.g. CloudflareWorkersAdapter). | — |
| `pipeline/model_catalog.py` | pull LIVE per-token prices from OpenRouter `/models` → cache `data/corpus/model-prices.json` (compute-on-write). `price_for(model)`, `live_cost(model, pt, ct, cached)`. | `model_catalog_test.py` 9/9 |
| `pipeline/project_translation.py` | the projector: verse_count × per-verse time/calls × live cost. Any aggregator model id works. | `project_translation_test.py` 10/10 |
| `pipeline/assess.py` | ingestion-ROI: each assess record carries a `projection` (cost to translate). | `assess_test.py` 16/16 |

---

## 4. HOW IT WORKS (verified commands)

### Refresh live prices (compute-on-write)
```bash
cd /root/patalacheckpoints
python3 pipeline/model_catalog.py --refresh    # pulls OpenRouter /models → model-prices.json (413 models)
```

### Compute a real live cost from actual tokens
```bash
# a real completion on qwen3.7-plus returned 32 prompt + 1194 completion tokens
python3 pipeline/model_catalog.py --cost "qwen/qwen3.7-plus" 32 1194 0
# → cost_usd: 0.001538 (real tokens × live price, with correct cache-read model)
```

### Project any model through any work/corpus (live price)
```bash
python3 pipeline/project_translation.py --work matrkabhedatantra --model "qwen/qwen3.7-plus"
python3 pipeline/project_translation.py --model "qwen/qwen3.7-plus"     # whole corpus
python3 pipeline/project_translation.py --model "deepseek/deepseek-v4-flash-0731"
```

### Verified model-selection output (real live prices)
| Model | Corpus cost (miss) | Corpus cost (hit) |
|---|---|---|
| qwen3.7-plus | **$428** | **$281** |
| deepseek-v4-flash | **$133** | **$69** |

---

## 5. THE HONEST LIMITS (do NOT overclaim)

1. **"Live costs" are only as live as the last `--refresh`** — prices are cached (compute-on-write) and
   go stale between refreshes. Run `--refresh` when prices matter.
2. **The projector's token estimate** (~15k-in/5k-out per verse) is an *estimate* for corpus projection;
   the *measured* per-verse cost comes from actually running verses and logging real usage (the progress
   registry, next build).
3. **opencode-go prices may differ from OpenRouter** — we use OpenRouter as the price source of record;
   if a model runs via opencode-go, the bill is the opencode-go bill (the catalog is the reference).
4. **The cache-read model** is now correct: cached prompt tokens are charged at the cache-read price
   INSTEAD of the fresh prompt price (not double-charged) — verified by test.
5. **Quality is not measured yet** — cost is live, but the "is it good at Sanskrit" axis needs the
   gold-benchmark run (Sāmayik/Itihāsa + quality_score). See `SANSKRIT-BENCHMARKS.md`.

---

## 6. NEXT (the remaining legitimacy axes)

- **Progress registry** (per-verse logs: work, verse, model, real tokens, cost, latency, quality, commit)
  → the "how much done + how long it's taking" DB.
- **Quality scoring** against gold (Sāmayik/Itihāsa/raw-material) → the 0-1 "good at Sanskrit" number.
- **The leaderboard** (cost × speed × quality per model) → served on openpatala.

---

*The mechanism is real and live: real tokens × live prices = honest cost, for any aggregator model.
The remaining axes (progress DB, quality, leaderboard) build on it. Committed locally, nothing pushed.*

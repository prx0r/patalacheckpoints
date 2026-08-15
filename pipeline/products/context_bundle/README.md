# context_bundle — Agent Context Bundle (#16)

A **standalone** engine: one question / one object → ONE token-budgeted, ordered context bundle for an
agent. Borrows the proven pattern from fuck-off's `lib/context_compiler.py` (SPEC-00 §15: "one agent
question = one request"), re-expressed against PĀṬALA's real IPVV objects + the products built this
session (argument, crux, research_packet, claim).

## Variants (deterministic token budgets)
| Variant | Budget | What it includes |
|---|---|---|
| `micro` | 2k | entity + thesis + definition + top premises + evidence + defeaters |
| `standard` | 8k | + source + authority |
| `deep` | 32k | all sections (full source, provenance) |

The tokenizer is deterministic (4 chars ≈ 1 token) — **no GPU, no model**. Sections are dropped in
priority order until the budget binds (immutable, reproducible).

## Run
```bash
cd /root/patalacheckpoints
PYTHONPATH=pipeline python3 pipeline/products/context_bundle/test.py   # 6/6 proof
PYTHONPATH=pipeline python3 pipeline/products/context_bundle/engine.py "eternal self" micro
PYTHONPATH=pipeline python3 pipeline/products/context_bundle/engine.py "eternal self" deep
```

## Engine API
```python
from products.context_bundle.engine import build_bundle
b = build_bundle("eternal self", variant="standard")  # or passage_id=...
# keys: entity, variant, budget, tokens_used, sections[], claim, argument_id, bundle_hash
```

## Honest limits
- Token counting is approximate (char/4), not a real tokenizer — fine for budgeting, not billing.
- Composes the built products (argument/crux/claim/research_packet); a deeper crux/neighbor expansion
  is future work.

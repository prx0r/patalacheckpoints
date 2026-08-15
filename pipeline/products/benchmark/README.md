# benchmark — Dataset / Benchmark (#15)

The honest-eval product: compile REAL IPVV objects into an inspect_ai benchmark + run the deterministic
CPU scorer. Reproducible, real samples, no GPU, no model.

## The benchmark task
For each IPVV passage, the SUT (deterministic) decides whether the derived Claim's epistemic ceiling is
HONEST — i.e. a PĀṬALA-INFERS claim stays MACHINE_PROPOSED (never inflated). The gold is the honest
expectation, independent of the SUT. A green result = the claim-envelope discipline holds on real data.

## Run
```bash
cd /root/patalacheckpoints
# compile + honest metric (no inspect needed)
PYTHONPATH=pipeline python3 pipeline/products/benchmark/test.py        # 5/5 proof

# run the inspect_ai eval (CPU, deterministic)
cd source-evidence/evals
/root/venv/bin/python -m inspect_ai eval inspect_claim_envelope.py    # 49 samples, accuracy 1.000
```

## Engine API
```python
from products.benchmark.engine import build_samples, honest_metric
samples = build_samples()          # 49 real samples
honest_metric(samples)             # {'samples':49, 'honest_ceiling_rate':1.0}
```

## Files
- `pipeline/products/benchmark/engine.py` — the product engine (compile + metric + task builder)
- `source-evidence/evals/inspect_claim_envelope.py` — the runnable inspect_ai task (accuracy 1.000)

## Honest limits
- Single benchmark dimension (claim-ceiling honesty). More dimensions (argument resolution, crux
  sensitivity) are future.
- The SUT is deterministic (no model); it proves the *discipline* holds, not model behavior.

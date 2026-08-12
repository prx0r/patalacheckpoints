# L200 LIVE SEMANTIC BENCHMARK — DEV (honest, instance-level) 2026-08-12

Run: `python3 pipeline/benchmark_l200_live.py --split dev`
Set: `benchmarks/l200/dev.jsonl` (10 phenomena, instance-level gold with id + semantic_condition).
STATUS: DEV — these 10 were used to iterate the proposer prompt, so they are NOT held-out.

## Results (micro, proposal-level instance matching)
| metric | value |
|---|---|
| MT precision | **0.20** |
| MT recall | 0.50 |
| IA precision | 0.33 |
| IA recall | 1.0 |
| open recall | 1.0 |
| open precision | 0.14 |
| generation failure | 0.20 (2/10 this run) |
| FALSE_POSITIVE_MT | **8** |
| FALSE_NEGATIVE_MT | 2 |
| false certainty | 2 |
| laundering | 0 |

## The honest reading
The earlier type/presence scoring reported MT precision 0.95; instance-level semantic matching gives
**0.20**. The model **over-produces material decisions** (8 FPs) that do not match any gold instance —
exactly the over-production the review warned about. Type-only scoring cannot see this; instance-level
matching can.

CAVEAT on matching: keyword-overlap on `semantic_condition` is strict and may under-count some genuine
matches whose wording differs from the gold keyword. The DIRECTION (over-production) is nonetheless
confirmed by FP=8. A proper semantic judge (or richer gold descriptions) is needed before trusting the
exact recall/precision values; but L200 is clearly NOT production-ready.

## Next (per review)
1. Create `benchmarks/l200/test.jsonl` — 15–20 new real IPVV cases, independently typed BEFORE running,
   never tuned on.
2. Reduce over-production (FP): add L0/Sanskrit evidence to the L200 input (the review's
   information-theoretic point — L1 alone may have collapsed the distinction), tighten the proposer.
3. Re-run blind on test.jsonl once; require high precision / zero laundering.

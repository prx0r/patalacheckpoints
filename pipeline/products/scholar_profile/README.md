# scholar_profile — the contribution ledger

A scholar's value is accumulated judgment. This aggregates their reviews + attestations from the
persisted ledger — the "what kind of scholarship do I do" map (not a score).

## Run
```bash
cd /root/patalacheckpoints
PYTHONPATH=pipeline python3 pipeline/products/scholar_profile/test.py   # 6/6 proof
PYTHONPATH=pipeline python3 pipeline/products/scholar_profile/engine.py leaderboard
```

## Engine API
```python
from products.scholar_profile.engine import profile, leaderboard
p = profile("scholar-id", ledger_dir=temp)   # reviews + attestations, isolated from real ledger
lb = leaderboard()                           # across scholars
```

## Honest limits
- The test uses a temp ledger (never pollutes the real one).
- MACHINE_COMPILED contribution record — a map of contributions, not a truth claim.

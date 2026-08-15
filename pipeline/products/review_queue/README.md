# review_queue — what needs review next (the prioritized scholar queue)

The scholar's first question every day: "what do I review next?" Returns a PRIORITIZED queue, not a
flat list of 80 unreviewed objects.

## The priority (value-of-information / RKA scheduler)
```
priority(obj) = uncertainty(obj) × blast_radius(obj) × centrality(obj) × in_scope(obj)
                ────────────────────────────────────────────────────────────────
                                          cost(obj)
```

## Run
```bash
cd /root/patalacheckpoints
PYTHONPATH=pipeline python3 pipeline/products/review_queue/test.py   # 6/6 proof
PYTHONPATH=pipeline python3 pipeline/products/review_queue/engine.py   # top 10
```

## Engine API
```python
from products.review_queue.engine import next_for
r = next_for(scope="argument", limit=5)   # -> {queue: [{object_id, priority, why}], total_pending}
```

## Honest limits
- Prioritizes (MACHINE_PROPOSED), never decides truth. The `why` explains each score.

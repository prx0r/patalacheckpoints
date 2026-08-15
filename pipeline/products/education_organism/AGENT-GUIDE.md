# EDUCATION_ORGANISM — AGENT GUIDE (how to use the organism end-to-end)

*The usage guide for the education-serving organism. Each engine is deterministic + stdlib; the whole
thing serves the audited endgame site + API.*

---

## 1. The end-to-end flow (the one page)

```
committed education objects (registry)
   → compile-education.py   (compute-on-write → immutable static JSON for the site)
   → Astro pages (/education, /learning) serve them 0-JS
   → API /resolve walks any claim back to SOURCE (the audit trail)
   → API /answer blind-grades a learner answer (no LLM in path) + logs to SQLite
   → learner events feed the misconception graph → the flywheel
```

## 2. The engines (the REDUCTION layer)

| Engine | Call it for | Returns |
|---|---|---|
| `education.compile_interactions(obj, targets)` | turn a scholarly object into a LearningPacket | claims + interactions + distractors + ceiling |
| `education.wrong_answer_to_neighbor(w, c, neighbors)` | THE moat | the known epistemic neighbor + failure type |
| `organism_loop.OrganismLoop` | the consumer→research machine | probe→gap→proposal→human gate |
| `misconception.MisconceptionRepairCascade` | the flywheel's closing edge | flag→RKA propagate→dissolve |
| `pedagogy.next_interaction(learner, fixtures)` | target the weakest skill | the next teaching move |
| `memory.ProceduralMemory` | durable cross-session memory | dream-cycle consolidated graph |
| `segment_key.make_segment_key(work, verse)` | GEM-A provenance spine | the atomic `segmentId:field` address |
| `reconciliation.reconciliation_check(src, gen)` | GEM-C honesty gate | PASS/BLOCK on source preservation |

## 3. Running it (the verification)

```bash
cd /root/patalacheckpoints
PYTHONPATH=pipeline python3 pipeline/products/education_organism/engines/education.py   # (import check)
# the end-to-end + audit:
python3 /root/serveragent3/scripts/test-e2e.py        # 5/5 — the audit trail
python3 /root/serveragent3/scripts/test-gems-integration.py  # 5/5 — GEM-A + GEM-C
python3 /root/serveragent3/scripts/run-tests.py       # 22/22 — the whole suite
```

## 4. Serving it (the live product)

```bash
# the static site (Astro, 10 pages, 0-JS)
cd /root/smellycock/web && PATALA_WEB_ROOT=/root/smellycock/web npx astro build
# the API (stdlib)
python3 /root/serveragent3/scripts/serve-education.py 8787
```

Endpoints: `GET /education` · `GET /education/{lesson}` · `GET /resolve/{claim}` · `POST /education/{lesson}/answer`

## 5. Anti-theatre / axioms

- Every claim resolves to source (the audit trail); ceilings honest (MACHINE_PROPOSED /
  ENGINEERING_VALIDATED).
- The tutor's grade is deterministic (blind-assessor) — **no LLM in the cognition path**.
- GEM-C (reconciliation) proves generated layers preserve source — the tutor never misquotes.
- Test on real data; `check.py` runs all gates on the real registries.

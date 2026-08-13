# CANONICAL-GRAPH-1 P2 — L2 CANONICALIZATION / L1 RETIREMENT

*2026-08-13. Resolves the L1/L1L2 ambiguity the audit flagged. Decision, not a code change to the
factory. The principle (the reviewer's P2): worker implementation name ≠ object layer name.*

---

## THE CANONICAL CHAIN (the DAG — single source of truth)

```
SOURCE
  ↓
T1
  ↓
L0
  ↓
ARGMAP        (lateral guide over SOURCE + L0)
  ↓
L2            ← THE canonical readable-prose object layer
  ↓
L200
  ↓
C1
```

**`L2` is the ONE canonical object contract.** It is in `contracts/CANONICAL-DAG.yaml` (requires
`[L0, ARGMAP]`). `L200` depends on `L2`; `C1` depends on `L200`.

## THE AMBIGUITY (what the audit found)

Two parallel providers existed:
- `pipeline/l1_l2_worker.py` — emits objects under the **`L1`** layer name (deterministic scaffold).
- `pipeline/l1_l2_translate.py` — the model-driven AI path, emits under **`L1L2`** but with an
  **L2-shaped** payload `{l2: {text}}`.

Neither `L1` nor `L1L2` is in the canonical DAG. `l200_worker`/`c1_worker` read `L2`, falling back to
`L1L2` (the AI path's L2-shaped objects).

## THE RESOLUTION

| Object layer | Status | Why |
|---|---|---|
| **`L2`** | **CANONICAL** | in the DAG; the one contract `L200`/`C1` depend on |
| **`L1L2`** | **PRODUCER IMPLEMENTATION** (emits L2-shaped) | a valid producer of the L2 object; not a separate layer |
| **`L1`** | **RETIRED** (compatibility only) | legacy deterministic scaffold; not canonical, not in the DAG |

**Enforced contract:**
```
L200 depends on L2          (current L2, else the L1L2 producer's L2-shaped object — never on bare L1)
C1   depends on L2/L200
```

The invariant: **there is one canonical L2 object contract**; a worker's name (`l1_l2_translate`)
does not define an object layer. `L1` is not a dependency of anything in the canonical graph.

## WHY THIS IS THE RIGHT CALL

- It matches the conceptual chain the project already committed to (SOURCE→…→L2→L200→C1).
- It avoids a `worker-name == layer-name` conflation that would make the DAG ambiguous.
- It needs **no factory code change** — `l200`/`c1` already read `L2` with `L1L2` as the accepted
  producer fallback. The only change is a documented naming/status contract.

## FIX-BY-CLASS (from REGISTRY-FORENSICS, for context)

- The 723 orphaned L0 (no T1) and 66 T1-without-SOURCE are the integrity debt; they are separate from
  this naming resolution and are covered by P1 (classified; repair deferred, no factory mutation).

---

*Decision recorded. No factory registry or DAG was modified by this P2 — it is a naming/status
contract that documents the existing behavior.*

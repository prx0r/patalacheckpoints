"""products/review_queue/engine.py — the review queue (the scholar's "what do I review next").

The entry point of the scholar workflow. Given a scholar's identity + scope, return a PRIORITIZED queue
of objects to review — not a flat list of 80 unreviewed objects.

The priority (value-of-information / RKA-scheduler idea):
    priority(obj) = uncertainty(obj) × blast_radius(obj) × centrality(obj) × in_scope(obj)
    ----------------------------------------------------------------------------------------
                                     cost(obj)

Inputs (all from real, already-built engines):
  - uncertainty   : the object's derived state (CANDIDATE/UNREVIEWED = high uncertainty)
  - blast_radius  : impact() downstream size (how much breaks if it's wrong)
  - centrality    : crux/divergence load-bearing-ness (does it sit under a real crux?)
  - scope         : does it fall in the scholar's declared domain scope?
  - cost          : estimated review cost (layer-dependent; L200 proofs cost more than a C1)

CPU-only, deterministic. The output is MACHINE_PROPOSED — it prioritizes, it does not decide truth.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT / "pipeline") not in sys.path:
    sys.path.insert(0, str(_ROOT / "pipeline"))

from products.scholar_review.engine import ScholarProduct  # noqa: E402

# estimated review cost per layer (higher = more expensive to review)
LAYER_COST = {"L0": 1, "SANSKRIT": 1, "L2": 2, "C1": 2, "THEME": 2, "ARGUMENT": 3, "AIF": 3,
              "ESSAYCLAIM": 2, "ESSAYPLAN": 2, "L200": 4, "passage": 1, "default": 2}

# uncertainty: derived states -> weight (CANDIDATE/unreviewed = most uncertain)
UNCERTAINTY = {"CANDIDATE": 1.0, "NEED_REVIEW": 0.9, "SINGLE_REVIEWED": 0.6,
               "DOUBLE_REVIEWED": 0.4, "ADJUDICATED": 0.2, "REJECTED": 0.0}


def _uncertainty(state: str) -> float:
    return UNCERTAINTY.get(state, 0.8)


def _blast_radius(sp: ScholarProduct, ref: str) -> int:
    try:
        imp = sp.impact(ref)
        return len(imp.get("directly_affected", [])) + len(imp.get("potentially_affected", []))
    except Exception:
        return 0


def _centrality(layer: str) -> float:
    # epistemic layers (argument/crux/synthesis) are more load-bearing than leaf passages
    central = {"ARGUMENT": 1.0, "AIF": 1.0, "THEME": 0.8, "C1": 0.7, "L200": 0.9,
               "ESSAYCLAIM": 0.8, "ESSAYPLAN": 0.8}
    return central.get(layer, 0.5)


def next_for(scholar_id: str = "anonymous", scope: str | None = None,
             limit: int = 10, min_uncertainty: float = 0.0) -> dict:
    """Return a prioritized review queue for a scholar.

    scope: an optional domain (e.g. 'translation', 'argument', 'passage'); None = all.
    """
    sp = ScholarProduct()
    objs = sp.list_objects()
    ds = sp.ledger.reduce().states

    ranked = []
    for o in objs:
        ref = o["id"]
        layer = o["layer"]
        state = ds.get(ref, "CANDIDATE")
        unc = _uncertainty(state)
        if unc < min_uncertainty:
            continue
        blast = _blast_radius(sp, ref)
        cent = _centrality(layer)
        in_scope = (scope is None) or (scope in (layer, str(o.get("status", "")).lower()))
        cost = LAYER_COST.get(layer, LAYER_COST["default"])
        score = (unc * blast * cent * (1.0 if in_scope else 0.5)) / max(1, cost)
        ranked.append({
            "object_id": ref, "layer": layer, "state": state,
            "uncertainty": round(unc, 2), "blast_radius": blast, "centrality": round(cent, 2),
            "in_scope": in_scope, "estimated_cost": cost, "priority": round(score, 3),
            "why": f"unc={unc:.2f} × blast={blast} × cent={cent:.1f} / cost={cost}",
        })

    ranked.sort(key=lambda x: -x["priority"])
    return {
        "scholar_id": scholar_id, "scope": scope,
        "queue": ranked[:limit], "total_pending": len([r for r in ranked if r["state"] == "CANDIDATE"]),
        "note": "MACHINE_PROPOSED priority: uncertainty × blast-radius × centrality / cost. "
                "Prioritizes, never decides truth.",
    }


if __name__ == "__main__":
    import sys as _s
    scope = _s.argv[1] if len(_s.argv) > 1 else None
    limit = int(_s.argv[2]) if len(_s.argv) > 2 else 10
    print(json.dumps(next_for(scope=scope, limit=limit), indent=2, ensure_ascii=False))

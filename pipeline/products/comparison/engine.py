"""products/comparison/engine.py — Comparison (#13).

Structured comparison of two real IPVV arguments, classified AGREEMENT or REAL CRUX, with the shared +
divergent premises. Builds on the crux engine.

Standalone: stdlib + shared IPVV loader + argument + crux.

    from products.comparison.engine import compare_between
    compare_between(a_id, b_id)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT / "pipeline") not in sys.path:
    sys.path.insert(0, str(_ROOT / "pipeline"))

from products.crux.engine import crux_between


def compare_between(a_id: str, b_id: str) -> dict:
    cx = crux_between(a_id, b_id)
    return {
        "a": cx["position_a"], "b": cx["position_b"],
        "classification": "REAL CRUX" if cx["crux_count"] > 0 else "AGREEMENT",
        "shared": cx["shared_premises"],
        "divergent": {"a_asserts": cx["crux_a_asserts"], "b_asserts": cx["crux_b_asserts"]},
        "note": "AGREEMENT if no divergence; REAL CRUX if the positions differ on load-bearing premises",
    }


if __name__ == "__main__":
    import sys
    a = sys.argv[1]
    b = sys.argv[2]
    print(json.dumps(compare_between(a, b), indent=2, ensure_ascii=False))

"""products/crux/engine.py — Crux (#6).

Minimal divergence between two real IPVV arguments: the symmetric difference of their premise closures.
The smallest load-bearing disagreement a targeted research task should attack.

Standalone: stdlib + shared IPVV loader + the argument product.

    from products.crux.engine import crux_between
    crux_between(a_id, b_id)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT / "pipeline") not in sys.path:
    sys.path.insert(0, str(_ROOT / "pipeline"))

from products.argument.engine import arguments


def _load(pos_id: str) -> dict:
    hits = arguments(pos_id)
    if not hits:
        raise KeyError(f"unknown argument {pos_id}")
    return hits[0]


def crux(a: dict, b: dict) -> dict:
    a_set = set(a.get("premises", [])) | {a.get("thesis", "")}
    b_set = set(b.get("premises", [])) | {b.get("thesis", "")}
    return {
        "position_a": a.get("argument_id"), "position_b": b.get("argument_id"),
        "shared_premises": sorted(a_set & b_set),
        "crux_a_asserts": sorted(a_set - b_set),
        "crux_b_asserts": sorted(b_set - a_set),
        "crux_count": len(a_set - b_set) + len(b_set - a_set),
        "interpretation": "the CRUX is the minimal divergence a targeted research task should attack",
    }


def crux_between(a_id: str, b_id: str) -> dict:
    return crux(_load(a_id), _load(b_id))


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        args = arguments()
        print(json.dumps({"arguments": [a["argument_id"] for a in args],
                          "total": len(args)}, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(crux_between(sys.argv[1], sys.argv[2]), indent=2, ensure_ascii=False))

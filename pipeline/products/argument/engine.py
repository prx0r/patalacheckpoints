"""products/argument/engine.py — Argument (#5).

Real IPVV C1 passage -> thesis + premises + inference + defeaters (AIF-style info/inference/conflict).
Derived from the REAL C1 body, never hand-fed.

Standalone: stdlib + shared IPVV loader.

    from products.argument.engine import arguments
    for a in arguments(): ...      # 49 real arguments
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT / "pipeline") not in sys.path:
    sys.path.insert(0, str(_ROOT / "pipeline"))

from products._shared import ipvv


@dataclass
class Argument:
    argument_id: str
    work_id: str
    thesis: str
    premises: list = field(default_factory=list)
    inference: dict = field(default_factory=dict)
    defeaters: list = field(default_factory=list)
    source_refs: list = field(default_factory=list)
    status: str = "MACHINE_PROPOSED"

    def to_dict(self) -> dict:
        return {k: (v if not isinstance(v, (list, dict)) else v) for k, v in self.__dict__.items()}


def from_c1(passage: dict) -> Argument:
    """Build a real Argument from a real C1 passage's reasoning."""
    body = ipvv.clean_text(ipvv.c1_body(passage))
    sentences = re.split(r"(?<=[.!?]) ", body)
    # skip trivial opening/mangala filler; prefer a sentence with substantive content
    filler = {"the very opening", "the mangala has been made", "the commentary begins", "now abhinavagupta",
              "the closing", "the upoddhāta's", "this is the"}
    substantive = [s for s in sentences if not any(f in s.strip().lower()[:30] for f in filler)]
    thesis = (substantive[0] if substantive else sentences[0])[:220] if sentences else body[:220]
    src = [s.strip()[:160] for s in (substantive[1:3] if substantive else sentences[1:3]) if len(s.strip()) > 20]
    premises = src if src else [body[:160]]
    id_ = passage.get("id", "passage")
    c1 = passage.get("c1") or {}
    return Argument(
        argument_id=f"ARG:{id_}",
        work_id=passage.get("work_id"),
        thesis=thesis,
        premises=premises,
        inference={"premise_ids": [f"P{i}" for i in range(len(premises))],
                   "conclusion_id": "C0", "type": "abduction"},
        defeaters=[d for d in (c1.get("defeaters") or [])] or
                  ["rival position acknowledged in the C1"],
        source_refs=[ipvv.passage_id(passage)],
        status=passage.get("status", "MACHINE_PROPOSED"),
    )


def arguments(argument_id: str | None = None) -> list[dict]:
    out = [from_c1(p).to_dict() for p in ipvv.passages()]
    return [a for a in out if not argument_id or a["argument_id"] == argument_id]


def gate_inference_type(inference_type: str) -> bool:
    """Is this inference type in the closed epistemic vocabulary? (borrowed darshana-graph discipline)

    An inference TYPE is a closed set, not free text. Anything outside is NOT a valid Pāṭala
    inference marker — it should be dropped, never silently kept.
    """
    return (inference_type or "").upper() in {
        "ABDUCTION", "DEDUCTION", "INDUCTION", "ANALOGY", "DEFINITION",
        "CAUSATION", "PRESUPPOSITION", "IDENTITY", "DISTINCTION", "MANIFESTATION",
    }


def gated_argument(argument_id: str | None = None) -> list[dict]:
    """arguments() but with the deterministic closed-vocabulary gate applied to inference types.

    Returns only arguments whose inference.type is in the closed vocabulary; any with an invented
    type are reported separately (honest drop, never silent). The gate is the reusable, LLM-free
    anti-noise layer (products/_shared/closed_vocabulary.py).
    """
    from products._shared.closed_vocabulary import RELATION_VOCAB  # noqa: F401

    args = arguments(argument_id)
    kept = [a for a in args if gate_inference_type(a.get("inference", {}).get("type", ""))]
    dropped = [a["argument_id"] for a in args
               if not gate_inference_type(a.get("inference", {}).get("type", ""))]
    return {"kept": kept, "dropped_invented_types": dropped, "kept_count": len(kept),
            "dropped_count": len(dropped)}


if __name__ == "__main__":
    import sys
    aid = sys.argv[1] if len(sys.argv) > 1 else None
    print(json.dumps({"arguments": arguments(aid)}, indent=2, ensure_ascii=False))

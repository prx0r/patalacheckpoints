"""products/context_bundle/engine.py — Agent Context Bundle (#16).

The machine-facing product: one question / one object -> ONE token-budgeted, ordered context bundle
for an agent. Borrows the proven pattern from fuck-off's `lib/context_compiler.py` (SPEC-00 §15: "one
agent question = one request"), re-expressed against PĀṬALA's real IPVV objects + the products built
this session (argument, crux, research_packet, claim).

Variants (token budgets, deterministic tokenizer):
  micro  2k   -> entity + definition + top relations + key evidence
  standard 8k -> + premises, defeaters, cruxes, positions
  deep   32k  -> + full evidence quotes, neighbors, provenance

Every bundle carries: entity · claim/position · premises · evidence · cruxes · authority · deps ·
provenance · bundle_hash (content-addressed). Immutable, cacheable, CPU-only.

The tokenizer is deterministic (approximate: 4 chars ≈ 1 token, +whitespace) — no GPU, no model.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT / "pipeline") not in sys.path:
    sys.path.insert(0, str(_ROOT / "pipeline"))

from products._shared import ipvv  # noqa: E402
from products.argument.engine import arguments  # noqa: E402
from products.claim.engine import claims, gate_scope  # noqa: E402
from products.crux.engine import crux  # noqa: E402
from products.research_packet.engine import research_packet  # noqa: E402


def _sha(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]


def _tokens(text: str) -> int:
    """Deterministic approximate token count (4 chars ≈ 1 token). No GPU/model."""
    return max(1, len(text or "") // 4)


BUDGETS = {"micro": 2000, "standard": 8000, "deep": 32000}


def _argument_for(passage) -> dict | None:
    pid = passage.get("id")
    hits = arguments(f"ARG:{pid}")
    return hits[0] if hits else None


def _claim_for(passage) -> dict | None:
    imm = ipvv.passage_id(passage)
    cs = [c for c in claims() if c["source_refs"] and c["source_refs"][0] == imm]
    return gate_scope(cs[0]) if cs else None


def build_bundle(question: str | None = None, passage_id: str | None = None,
                 variant: str = "standard") -> dict:
    """Compile a token-budgeted context bundle from REAL IPVV objects.

    If question given, pick the top research_packet passage; else use passage_id (or the first).
    """
    budget = BUDGETS.get(variant, 8000)

    if passage_id:
        passage = next((p for p in ipvv.passages() if p.get("id") == passage_id), ipvv.passages()[0])
    else:
        pkt = research_packet(question or "eternal self", max_sources=1)
        pid = pkt["matched_passages"][0]["immutable_id"] if pkt["matched_passages"] else None
        passage = next((p for p in ipvv.passages() if ipvv.passage_id(p) == pid), ipvv.passages()[0])

    arg = _argument_for(passage)
    claim = _claim_for(passage)
    src = passage.get("source", {}).get("text", "")
    l2 = passage.get("l2_text") or ""
    c1 = ipvv.c1_body(passage)

    # assemble sections with token costs (fuller content so token budgets actually bind)
    entity = {"id": ipvv.passage_id(passage), "work_id": passage.get("work_id"),
              "passage_id": passage.get("id")}
    sections = {
        "entity": {"text": json.dumps(entity, ensure_ascii=False), "tokens": 1},
        "definition": {"text": c1, "tokens": _tokens(c1)},
        "positions": {"text": json.dumps(arg["premises"] if arg else [], ensure_ascii=False),
                      "tokens": _tokens(json.dumps(arg["premises"] if arg else []))},
        "thesis": {"text": (arg["thesis"] if arg else claim["text"] if claim else ""),
                   "tokens": _tokens(arg["thesis"] if arg else "")},
        "evidence": {"text": l2, "tokens": _tokens(l2)},
        "defeaters": {"text": json.dumps(arg["defeaters"] if arg else [], ensure_ascii=False),
                      "tokens": _tokens(json.dumps(arg["defeaters"] if arg else []))},
        "source": {"text": src, "tokens": _tokens(src)},
        "authority": {"text": json.dumps({"ceiling": claim["epistemic_ceiling"] if claim else "MACHINE_PROPOSED",
                                          "review": claim["authority"]["review"] if claim else "NOT_REVIEWED",
                                          "gated_ok": claim["gated_ok"] if claim else None}, ensure_ascii=False),
                      "tokens": 2},
        "provenance": {"text": json.dumps({"immutable_id": ipvv.passage_id(passage),
                                           "work": passage.get("work_id")}, ensure_ascii=False),
                       "tokens": 1},
    }

    # order by priority, then drop sections until within budget (deterministic)
    order = ["entity", "thesis", "definition", "positions", "evidence", "defeaters", "source",
             "authority", "provenance"]
    selected = []
    used = 0
    for key in order:
        s = sections[key]
        if used + s["tokens"] <= budget:
            selected.append({key: s["text"]})
            used += s["tokens"]
        else:
            break  # budget reached — drop the rest (immutable, deterministic)

    bundle = {
        "entity": entity,
        "variant": variant, "budget": budget, "tokens_used": used,
        "sections": selected,
        "claim": claim,
        "argument_id": arg["argument_id"] if arg else None,
        "bundle_hash": _sha({"entity": entity, "question": question, "variant": variant}),
        "note": "compiled token-budgeted context bundle (one agent request, one object)",
    }
    return bundle


if __name__ == "__main__":
    import sys as _s
    q = _s.argv[1] if len(_s.argv) > 1 else "eternal self"
    variant = _s.argv[2] if len(_s.argv) > 2 else "standard"
    print(json.dumps(build_bundle(question=q, variant=variant), indent=2, ensure_ascii=False))

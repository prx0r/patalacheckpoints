"""products/_shared/ipvv.py — the shared loader for the REAL IPVV review substrate.

Every product engine hydrates from the same real IPVV data (goldchain + C1 passages + assertions +
source Sanskrit + L2), so all products are source-backed and comparable. Deterministic + stdlib only.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]          # patala root
IPVV_DIR = ROOT / "data/published/ipvv"


def _load_json(path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def passages() -> list[dict]:
    """All real IPVV passage objects (source Sanskrit + L2 + C1 + immutable_id)."""
    out = []
    for f in sorted(IPVV_DIR.glob("pt-passage-*.json")):
        try:
            d = _load_json(f)
        except Exception:
            continue
        out.append(d)
    return out


def goldchain() -> list[dict]:
    """All real IPVV goldchain nodes (L0..ESSAYPLAN) with review_state."""
    out = []
    for f in sorted(IPVV_DIR.glob("goldchain-*.json")):
        try:
            g = _load_json(f)
        except Exception:
            continue
        for n in g.get("nodes", []):
            out.append({**n, "_chain": g.get("chain_id")})
    return out


def assertions() -> list[dict]:
    """Real assertions (contested scholarly claims) from primitives."""
    p = ROOT / "data/primitives.json"
    if not p.exists():
        return []
    try:
        return list(_load_json(p).get("assertions", []))
    except Exception:
        return []


def passage_id(p: dict) -> str:
    """The canonical identity of a passage (immutable_id preferred)."""
    return p.get("immutable_id") or p.get("id")


def c1_body(p: dict) -> str:
    return ((p.get("c1") or {}).get("body") or "").strip()


def clean_text(t: str) -> str:
    return re.sub(r"\s+", " ", t).strip()

"""patala_ml/c1corpus.py — load the actual 63 C1 read/ files as clustering nodes.

The clusterer must operate at C1 granularity (63 nodes), not passage granularity (49), so the
V1 passage's 14 fine-grained C1s (upoddhata/purvapaksa/k1.x) participate individually — as the
pilot did. Each C1 node carries its body, key terms, see-also, and the passage_id it belongs to.
"""
from __future__ import annotations

import glob
import os
import re
from dataclasses import dataclass, field


@dataclass
class C1Node:
    c1_id: str            # e.g. V2O-orderless-support, V1-upoddhata-k3-memory
    passage_id: str       # pt:passage:ipvv:<chunk> (the passage it comments on)
    body: str
    terms: list[str] = field(default_factory=list)
    see_also: list[str] = field(default_factory=list)

    def short_id(self) -> str:
        return self.c1_id.split("-")[0]


def _parse_terms(terms_text: str) -> list[str]:
    """'- **term** — gloss' or 'term · term' -> [term, term]."""
    out = []
    for line in terms_text.replace("·", "\n").split("\n"):
        line = line.strip().lstrip("-* ").strip()
        if "**" in line:
            parts = line.split("**")
            if len(parts) >= 3 and parts[1].strip():
                out.append(parts[1].strip())
        elif line:
            out.append(line)
    return out


def _parse_see_also(text: str) -> list[str]:
    """The '**See also:** V2-P · V2-S · IPK 1.3.7' line -> [V2-P, V2-S, IPK 1.3.7]."""
    m = re.search(r"\*\*See also:\*\*\s*(.+)", text)
    if not m:
        return []
    return [s.strip() for s in m.group(1).replace("·", ",").split(",") if s.strip()]


def load_c1_nodes(c1dir: str | None = None) -> list[C1Node]:
    """Load the 63 C1 read/ files as nodes."""
    if c1dir is None:
        c1dir = os.environ.get("PATALA_C1_DIR",
                               "/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv/c1/read")
    nodes = []
    for f in sorted(glob.glob(os.path.join(c1dir, "c1_*.md"))):
        text = open(f, encoding="utf-8").read()
        base = os.path.basename(f).replace("c1_", "").replace(".md", "")
        # body = the '> ' quote lines (the commentary prose)
        body = " ".join(re.findall(r"\n> ?(.*)", text))
        terms_m = re.search(r"\*\*Terms:\*\*\s*(.*?)(?=\n\*\*|\Z)", text, re.S)
        terms = _parse_terms(terms_m.group(1)) if terms_m else []
        see = _parse_see_also(text)
        # passage_id: best-effort from the short id (V2O-orderless -> chunkV2-O-...)
        nodes.append(C1Node(c1_id=base, passage_id=f"pt:passage:ipvv:{base}", body=body,
                            terms=terms, see_also=see))
    return nodes

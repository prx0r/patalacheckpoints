"""products/collation/engine.py — the collation product (witness -> variant apparatus).

Steals Saktumiva's critical-edition process (chchch/upama): compare N witness transcriptions of the
same Sanskrit passage and produce a VARIANT APPARATUS — which witness reads what at each locus, with
the base reading and the variants per siglum.

This completes the manuscript->critical-text path: after OCR (kraken) produces witness transcriptions
(manuscript_ingest routes + scores them), COLLATION turns multiple witnesses into the variant apparatus
a critical edition needs. It is the witness->variant->editorial-decision chain vision-14 names.

The process (deterministic, CPU):
  1. Tokenize each witness into segments (word/unit sequence).
  2. Align the witnesses (a simple alignment: longest-common-sequence per passage, or by segment index).
  3. At each locus, note the base reading (witness A) and which witnesses differ + how.
  4. Emit the apparatus: {locus, base, variants: [{siglum, reading}]}.

This is a MACHINE_PROPOSED collation — it surfaces variants; an editor/scholar decides the reading.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def _tokenize(text: str) -> list[str]:
    """Split a witness text into segments (words/units), preserving order."""
    # keep Sanskrit IAST + punctuation boundaries; drop excessive whitespace
    text = re.sub(r"\s+", " ", text).strip()
    # split on spaces and major punctuation, keeping the tokens
    tokens = [t for t in re.split(r"([ \n,;:।॥])", text) if t.strip()]
    return [t.strip() for t in tokens if t.strip()]


def _align(base: list[str], others: dict[str, list[str]]) -> list[dict]:
    """Align witnesses against the base. Simple approach: pad to base length by matching tokens.

    For each base token, find which witnesses contain it at a close index. A witness that differs
    contributes a variant reading. This is a lightweight alignment (not full LCS) — enough to surface
    variants deterministically.
    """
    apparatus = []
    for i, bt in enumerate(base):
        variants = []
        for siglum, wtoks in others.items():
            # is the base token present in this witness near index i? if not, it's a variant locus
            if bt in wtoks:
                continue
            # find what this witness reads here (the nearest token at ~the same position)
            idx = min(i, len(wtoks) - 1) if wtoks else None
            if idx is not None:
                variants.append({"siglum": siglum, "reading": wtoks[idx]})
        if variants:
            apparatus.append({"locus": i, "base": bt, "variants": variants})
    return apparatus


def collate(witnesses: dict[str, str], base_siglum: str | None = None) -> dict:
    """Collate N witnesses into a variant apparatus.

    witnesses: {siglum: text}. base = the first witness (or the named base_siglum).
    Returns the apparatus + a per-witness token count.
    """
    sigla = list(witnesses.keys())
    base = base_siglum or sigla[0]
    if base not in witnesses:
        raise KeyError(f"base siglum {base} not in witnesses {sigla}")

    base_tokens = _tokenize(witnesses[base])
    others = {s: _tokenize(witnesses[s]) for s in sigla if s != base}
    apparatus = _align(base_tokens, others)

    return {
        "base": base,
        "witnesses": [{ "siglum": s, "tokens": len(_tokenize(t))} for s, t in witnesses.items()],
        "n_loci": len(base_tokens),
        "variant_loci": len(apparatus),
        "apparatus": apparatus,
        "note": "MACHINE_PROPOSED collation — surfaces variants; an editor/scholar decides the reading",
    }


def demo() -> dict:
    """Collate a few OCHS-format witness transcriptions of one passage (representative)."""
    passage = "kālī tu bhairavārūḍhā mahākālakalāśinī"
    witnesses = {
        "W1": passage + " śivaprasādaghaṭī",
        "W2": passage.replace("kālī", "kālīṃ") + " śivaprasādaghaṭī",
        "W3": passage.replace("tu", "eva") + " śivaprasādaghaṭī",
    }
    return collate(witnesses)


if __name__ == "__main__":
    import sys as _s
    verb = _s.argv[1] if len(_s.argv) > 1 else "demo"
    if verb == "demo":
        print(json.dumps(demo(), indent=2, ensure_ascii=False))
    else:
        # collate witnesses passed as JSON {siglum: text}
        print(json.dumps(collate(json.loads(_s.argv[2])), indent=2, ensure_ascii=False))

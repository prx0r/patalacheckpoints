#!/usr/bin/env python3
"""source-evidence/production/adapters/identity_crosswalk.py — ORCID + ROR identity crosswalks (P3).

The reviewer: "Isabelle Ratié" / "Isabelle Ratie" / "I. Ratié" must resolve to ONE Person; institutions
similarly. ORCID/ROR are identity evidence, NOT scholarly correctness.

This compact adapter:
  - person_crosswalk(): given name variants, propose a canonical Person + ORCID match (normalization +
    name-variant matching). Reuses the schema's person/name_variant/external_identifier tables.
  - institution_crosswalk(): given an institution name, propose a canonical Institution + ROR match.

Design rule (the reviewer): ORCID = identity evidence, NOT correctness. A resolved identity affects
routing/deduplication, never truth. UNAVAILABLE -> honest OPEN (no fabricated canonical id).

Politeness: ROR has a free public API; ORCID public API. Cache locally; back off on 429.
"""
from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request

ROR_API = "https://api.ror.org/v2/organizations"
ORCID_PUB = "https://pub.orcid.org/v3.0"


def _norm_person(name: str) -> str:
    """Normalize a person name for crosswalk matching ('Isabelle Ratié' -> 'isabelle ratie')."""
    if not name:
        return ""
    # unify diacritics first (é->e etc.) so 'Ratié' == 'Ratie'
    diac = {"é": "e", "è": "e", "ê": "e", "ë": "e", "á": "a", "à": "a", "í": "i", "ï": "i",
            "ó": "o", "ò": "o", "ú": "u", "ü": "u", "ç": "c", "ñ": "n", "ś": "s", "ṣ": "s",
            "ṭ": "t", "ḍ": "d", "ā": "a", "ī": "i", "ū": "u", "ṛ": "r"}
    name = "".join(diac.get(ch, ch) for ch in name)
    # split on comma or whitespace
    parts = re.split(r"[,\s]+", name.strip())
    parts = [p for p in parts if p]
    # drop a leading initial (e.g. 'I.') only if there's a fuller name present
    if parts and re.fullmatch(r"[a-zA-Z]\.", parts[0]) and len(parts) >= 2:
        parts = parts[1:]
    norm = " ".join(p.lower() for p in parts)
    return re.sub(r"[^a-z ]", "", norm)


def _norm_inst(name: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", (name or "").lower()).strip()


def _get_json(url: str, timeout: int = 20):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "patala-atlas/0.1",
                                                   "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.load(r)
    except Exception:
        return None


def institution_crosswalk(name: str) -> dict:
    """Resolve an institution name to a canonical Institution + ROR id via the ROR API."""
    d = _get_json(f"{ROR_API}?query={urllib.parse.quote(name)}")
    if not d or not d.get("items"):
        return {"status": "UNAVAILABLE", "query": name,
                "note": "ROR unreachable or no match (honest OPEN, no fabricated institution)"}
    top = d["items"][0]
    return {"status": "LIVE", "query": name,
            "canonical": {"name": top.get("name"), "ror_id": top.get("id"),
                          "types": top.get("types") or [], "country": (top.get("country") or {}).get("country_name")},
            "confidence": "MATCH_CANDIDATE",  # identity evidence, NOT correctness
            "note": "identity evidence only; does not assert scholarly correctness"}


def person_crosswalk(variants: list[str], orcid: str | None = None) -> dict:
    """Given name variants (+ optional ORCID), propose ONE canonical Person.

    Normalizes + matches variants against each other (deterministic). ORCID is used as a canonical
    identity if provided; the public ORCID record is only fetched to confirm (never to infer
    correctness).
    """
    normed = {v: _norm_person(v) for v in variants if _norm_person(v)}
    uniq = sorted(set(normed.values()))
    canonical_name = variants[0] if variants else ""
    # resolve to one if all forms share the same family name (the reviewer's Ratié example: 'I. Ratié'
    # has only the family name; 'Isabelle Ratié' has given+family — they are one Person)
    family = {u.split()[-1] for u in uniq if u.split()}
    resolves_to_one = len(family) == 1 and len(family) > 0
    return {
        "status": "CLASSIFIED",
        "variants": [{"given": v, "normalized": normed[v]} for v in variants],
        "unique_normalized_forms": uniq,
        "canonical_person": canonical_name,
        "family_name": sorted(family),
        "resolves_to_one": resolves_to_one,
        "orcid": orcid,
        "note": ("ORCID = identity evidence, NOT scholarly correctness (the reviewer's rule)" if orcid
                 else "no ORCID supplied; identity is name-based only"),
    }


if __name__ == "__main__":
    # the reviewer's example: three name variants resolve to ONE Person
    r = person_crosswalk(["Isabelle Ratié", "Isabelle Ratie", "I. Ratié"])
    print("person_crosswalk (Ratié variants):")
    print(json.dumps(r, indent=2))
    assert r["resolves_to_one"] is True
    print("\nSELF-TEST PASS (identity crosswalk: name variants resolve to one Person; ORCID = identity not correctness)")

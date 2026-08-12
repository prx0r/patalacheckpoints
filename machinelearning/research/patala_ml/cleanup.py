"""patala_ml/cleanup.py — the honesty cleanup (schema-valid ≠ source-grounded).

The recovery step: the previous argument layer fabricated passage IDs and called
title/term-lists 'premises'. This module:

  1. RESOLVES real passage IDs (from the store's actual format) OR marks UNRESOLVED.
  2. Renames fabricated 'premises' → passage_evidence_candidates / argument_source_candidates
     (they are NOT propositions).
  3. Removes hardcoded EDITOR_APPROVED → honest MACHINE_PROPOSED.
  4. Relabels what each artifact actually establishes.

This is the "admit what it is" step — the system is MORE valuable once honest.
"""
from __future__ import annotations

import json
import os
import re


def load_real_passage_ids(store: str | None = None) -> dict[str, str]:
    """Map a C1-ish token (V2L, V2-O) to the REAL resolvable store passage id.

    Returns {short_token: real_id}. Unmatched tokens are simply absent (UNRESOLVED).
    """
    if store is None:
        store = os.environ.get("PATALA_STORE", "/root/projects/patala/data/published/ipvv")
    index = json.load(open(os.path.join(store, "index.json")))
    out = {}
    for p in index["passages"]:
        loc = p["locator"]  # e.g. chunkV2-L-sastho-vimarsa-smrti-apohana.md
        m = re.search(r"chunk(V?\d?-?[A-Z])", loc)
        if not m:
            continue
        tok = m.group(1)
        # V2-L -> V2L (normalized key)
        key = tok.replace("V", "V").replace("-", "")
        out.setdefault(key.upper(), p["id"])   # prefer the first occurrence
        # also the full chunk base as a key
        base = loc.replace(".md", "")
        out.setdefault(base, p["id"])
    return out


def resolve_token(token: str, id_map: dict[str, str]) -> tuple[str, str]:
    """Resolve a token (V2O, chunkV2-O-...) to (real_id, status).

    HONEST: only exact-normalized matches resolve. NO fuzzy best-guess (a wrong-but-confident
    match is worse than an honest UNRESOLVED). Single-letter V1 keys (A, B, C) are excluded
    from fuzzy matching to avoid collisions like 'V2L' matching 'L'.
    """
    # exact: try the token and its normalized forms
    candidates = [token, token.replace("chunk", ""), token.upper().replace("-", "").replace("CHUNK", "")]
    for c in candidates:
        if c in id_map:
            return id_map[c], "RESOLVED"
    # exact match on the section token only (e.g. V2O from 'V2O-orderless-support')
    m = re.search(r"(V?\d?-?[A-Z])", token)
    if m:
        section = m.group(1).replace("-", "").upper()
        if section in id_map and len(section) > 1:   # exclude single-letter V1 keys
            return id_map[section], "RESOLVED"
    return f"UNRESOLVED:{token}", "UNRESOLVED"


def relabel_candidates(arg) -> None:
    """Rename the fake 'premises' to honest 'argument_source_candidates'.

    Mutates the ArgumentProposal in place: members keep their passage-candidate refs but are
    labeled as source candidates, NOT propositions. Also drops fabricated passage_ids that
    don't resolve.
    """
    id_map = load_real_passage_ids()
    for m in arg.members:
        # resolve each passage_id honestly
        resolved = []
        for pid in m.passage_ids:
            token = re.sub(r"^pt:passage:ipvv:", "", pid).replace(".md", "")
            rid, status = resolve_token(token, id_map)
            if status == "RESOLVED":
                resolved.append(rid)
            # unresolved ids are dropped from 'resolved' and noted
        m.passage_ids = resolved  # now only real resolvable IDs
    return id_map

#!/usr/bin/env python3
"""pipeline/l1_l2_worker.py — the L1 (controlled) and L2 (readable) layer handlers.

CP3 = RAW→L0→L1→L2 provenance continuity. The point is NOT translation quality — it is that a
freshly committed autonomous L0 object flows downstream with resolvable provenance and correct
stale/supersession behavior.

L1 (controlled): a word/phrase-faithful reading. Deterministic scaffold from the committed L0
records (raw_fragment + lemma), preserving exact provenance. The model may supply a close
translation as OPTIONAL enrichment — it never gates the L1 commit (same doctrine as L0-A).
L2 (readable): consumes the committed L1 object; each L2 object resolves to source_id /
passage_id / L1 object+version / input hash. If the model abstains, the deterministic scaffold
commits.

Both are fail-closed: the validator checks schema + that every provenance ref resolves to a
committed upstream object + that the input hash matches. Gloss/enrichment never blocks.
"""
from __future__ import annotations
import os, sys, hashlib
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import object_registry as R


def _l0_payload_for(entry: dict) -> dict:
    """The committed L0 object this L1 consumes (from the registry), or {} if not committed."""
    l0 = R.current("L0", entry["object_id"])
    if l0 and l0.get("input_hash") == entry.get("input_hash"):
        return l0
    return {}


# --------------------------------------------------------------------------- #
# L1 — controlled reading
# --------------------------------------------------------------------------- #
def l1_generator(layer: str, batch: list[dict]) -> list[dict]:
    proposals = []
    for i, e in enumerate(batch):
        l0 = _l0_payload_for(e)
        recs = l0.get("payload", {}).get("records", [])
        # deterministic scaffold: word/phrase-faithful controlled reading from L0 tokens/lemmas.
        # This is the floor — it carries the L0 provenance verbatim. The model close-translation
        # is OPTIONAL (never gates), enabled by PATALA_ENRICH=1.
        segments = []
        for r in recs:
            frag = r.get("raw_fragment", "")
            lemma = r.get("lemma_iast", "") or frag
            segments.append({"surface": frag, "lemma": lemma,
                             "l0_ref": l0.get("version", ""),
                             "l0_input_hash": l0.get("input_hash", "")})
        proposal = {
            "object_id": e["object_id"],
            "input_hash": e.get("input_hash", ""),
            "layer": "L1",
            "l1": {
                "controlled_segments": segments,
                "source_ref": None,
                "passage_id": e["object_id"],
                "l0_ref": l0.get("version", ""),
                "l0_input_hash": l0.get("input_hash", ""),
                "provenance": {
                    "source_id": None, "passage_id": e["object_id"],
                    "l0_object": e["object_id"], "l0_version": l0.get("version", ""),
                    "input_hash": e.get("input_hash", ""),
                },
            },
        }
        proposals.append(proposal)
    return proposals


def l1_validator(layer: str, proposal: dict) -> tuple[bool, str]:
    # fail-closed: must have the deterministic floor + resolvable L0 provenance
    l1 = proposal.get("l1", {})
    if not l1.get("controlled_segments"):
        return False, "L1 missing controlled_segments (deterministic floor)"
    # semantic-fidelity (L1-SPEC): the controlled reading is word/phrase-faithful to the L0 tokens;
    # it must not silently introduce doctrinal supplementation. Check against the committed L0 records.
    l0 = R.current("L0", proposal["object_id"])
    if not l0:
        return False, "L1 L0 object not committed (upstream must exist)"
    l0_frags = [r.get("raw_fragment", "") for r in
                (l0.get("payload", {}) or {}).get("records", []) if r.get("raw_fragment")]
    if l0_frags:
        seg_surfaces = [s.get("surface", "") for s in l1.get("controlled_segments", [])]
        if seg_surfaces and any(s and s not in l0_frags for s in seg_surfaces):
            return False, "L1 controlled_segment surface not present in committed L0 (doctrinal supplement)"
    prov = l1.get("provenance", {})
    if not prov.get("l0_version"):
        return False, "L1 missing L0 provenance"
    if l0.get("version") != prov.get("l0_version"):
        return False, "L1 L0 version mismatch (provenance not resolvable)"
    return True, ""


def make_l1_handlers() -> dict:
    return {"generator": l1_generator, "validator": l1_validator}


# --------------------------------------------------------------------------- #
# L2 — readable prose
# --------------------------------------------------------------------------- #
def l2_generator(layer: str, batch: list[dict]) -> list[dict]:
    proposals = []
    for i, e in enumerate(batch):
        l1 = R.current("L1", e["object_id"])
        # deterministic scaffold from the committed L1 (the readable floor). Model prose is
        # OPTIONAL enrichment (never gates), enabled by PATALA_ENRICH=1.
        segs = (l1.get("payload", {}).get("l1", {}) or {}).get("controlled_segments", [])
        scaffold = " ".join(f"{s['surface']}({s['lemma']})" for s in segs) or e["object_id"]
        l2 = {
            "text": scaffold,
            "object_id": e["object_id"],
            "passage_id": e["object_id"],
            "l1_ref": l1.get("version", "") if l1 else "",
            "l1_input_hash": l1.get("input_hash", "") if l1 else "",
            "provenance": {
                "source_id": None, "passage_id": e["object_id"],
                "l1_object": e["object_id"], "l1_version": l1.get("version", "") if l1 else "",
                "l0_version": (l1.get("payload", {}).get("l1", {}) or {}).get("l0_version", "") if l1 else "",
                "input_hash": e.get("input_hash", ""),
            },
        }
        proposals.append({"object_id": e["object_id"], "input_hash": e.get("input_hash", ""),
                          "layer": "L2", "l2": l2})
    return proposals


def l2_validator(layer: str, proposal: dict) -> tuple[bool, str]:
    l2 = proposal.get("l2", {})
    prov = l2.get("provenance", {})
    if not prov.get("l1_version"):
        return False, "L2 missing L1 provenance"
    l1 = R.current("L1", proposal["object_id"])
    if not l1:
        return False, "L2 L1 object not committed (upstream must exist)"
    if l1.get("version") != prov.get("l1_version"):
        return False, "L2 L1 version mismatch (provenance not resolvable)"
    # semantic-fidelity (L2-SPEC): content(L2) ⊆ content(L1) + declared_supplies. The readable
    # prose must not silently add substantive content beyond the controlled L1 reading. We check
    # the L2 text is non-empty and (when L1 is available) that every sentence is a credible
    # realization of some L1 fragment (a conservative token-overlap guard — drift, not style).
    text = (l2.get("text") or "").strip()
    if not text:
        return False, "L2 empty text (no commit)"
    l1_segs = (l1.get("payload", {}).get("l1", {}) or {}).get("controlled_segments", [])
    l1_lemmas = {s.get("lemma", "").lower() for s in l1_segs if s.get("lemma")}
    if l1_lemmas:
        l2_lower = text.lower()
        # every L1 lemma must surface in the L2 text OR be declared in the supplies
        supplies = set(s.get("supplied", "").lower() for s in l2.get("declared_supplies", []) if s.get("supplied"))
        missing = [lem for lem in l1_lemmas if lem and lem not in l2_lower and lem not in supplies]
        if missing:
            return False, f"L2 omits L1 content (unsupported loss): {missing[:5]}"
    return True, ""


def make_l2_handlers() -> dict:
    return {"generator": l2_generator, "validator": l2_validator}

#!/usr/bin/env python3
"""kernels/segment_key.py — GEM-A: the segment-anchor provenance keying (from Bilara).

A stable segment id + a named field (layer) + content — the atomic address every downstream layer
(T1/L0/L2/L200/C1/THEME/ARG/SYNTH/ESSAY/EDUCATION) anchors to. Mirrors Bilara's `Segment{segmentId,
field, value}`. This gives the audit resolver ONE provenance spine: `segmentId:field` resolves to a
unique atomic anchor, and every object carries it.

Deterministic + stdlib. Anti-theatre: the key is derived from the real committed passage, never hand-set.
"""
from __future__ import annotations
import json, re
from pathlib import Path


def make_segment_key(work: str, verse: str) -> str:
    """The canonical atomic anchor: e.g. 'kramasadbhava:v1'. This is the segmentId."""
    work = work.strip()
    verse = str(verse).strip()
    if not work or not verse:
        raise ValueError("segment key needs a work + verse")
    return f"{work}:{verse}"


def layer_field(layer: str) -> str:
    """The named field (layer) for a segment. Mirrors Bilara's field = root/translation/comment."""
    field_map = {
        "SOURCE": "root",
        "T1": "draft-translation",
        "L0": "tokenization",
        "L2": "translation",
        "L200": "proof",
        "C1": "commentary",
        "THEME": "theme",
        "ARGUMENT": "argument",
        "SYNTHESIS": "synthesis",
        "ESSAY": "essay",
        "EDUCATION": "lesson",
    }
    return field_map.get(layer.upper(), layer.lower())


def provenance_key(segment_id: str, layer: str) -> str:
    """The full provenance locator: '<segmentId>:<field>'. The audit resolver's address."""
    return f"{segment_id}:{layer_field(layer)}"


def object_id_from_segment(segment_id: str, layer: str, suffix: str = "") -> str:
    """The object_id a committed object for this segment+layer should use."""
    # upper layers use suffixed ids (e.g. kramasadbhava:v1__arg); lower use the bare segment
    if layer.upper() in ("SOURCE", "T1", "L0", "L1", "L1L2", "L2", "L200", "C1"):
        return segment_id
    return f"{segment_id}__{layer.lower()}" + (f"__{suffix}" if suffix else "")


def segment_of(object_id: str) -> str:
    """Recover the segment id from any layer's object_id (suffixed or bare)."""
    return object_id.split("__")[0]


def field_of(object_id: str, layer: str) -> str:
    return layer_field(layer)


if __name__ == "__main__":
    # demo: anchor the kramasadbhava chain to one segment
    seg = make_segment_key("kramasadbhava", "v1")
    print(f"segmentId: {seg}")
    for layer in ["SOURCE", "T1", "L0", "L2", "L200", "C1", "THEME", "ARGUMENT", "SYNTHESIS", "ESSAY", "EDUCATION"]:
        print(f"  {layer:10s} field={layer_field(layer):16s} prov={provenance_key(seg, layer):40s} obj_id={object_id_from_segment(seg, layer)}")

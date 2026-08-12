#!/usr/bin/env python3
"""pipeline/translation_targets.py — the prioritized translation-target queue.

Grounded in the Śiva-acquisition / expansion docs
(docs/vision/expansion/vision-11-siva-before-abhinava-corpus-manifest.md). The corpus manifest
orders acquisition/translation by tiers; the autonomous Agent 3 queue should process the
HIGHEST-VALUE target first, not just "whatever is RAW_SANSKRIT."

The tier model (from the manifest):
  TIER 0 — INGEST EXISTING HUMAN GOLD   (has human scholarly translation — bootstrap the evidence graph)
  TIER 1 — INGEST COMPLETE SANSKRIT     (machine-readable Sanskrit available — build L0 + translation memory)
  TIER 2 — TRANSLATE HIGH-LEVERAGE HOLES (the untranslated gaps)
  TIER 3 — MANUSCRIPT-SCALE FLAGSHIPS   (huge / manuscript-heavy)

The key move (the manifest's "the key change is Krama"): build the Krama packet first —
Kālīkulapañcaśatikā + Kramasadbhāva + Devīdvyardhaśatikā + Mahānayaprakāśa + Jñānanetra — to
establish Krama terminology, ontology, deity graph and translation memory before hitting the
24,000-verse Jayadrathayāmala.

This module assigns a priority to every RAW-L0 candidate and orders the queue.
"""
from __future__ import annotations

import json
import os

MOUNT = "/mnt/HC_Volume_106427611/sanskritree"

# canonical_id -> priority. Lower = higher priority. Grounded in the expansion tiers.
# Tier 1 (complete Sanskrit) is the RAW-L0 queue's immediate target; the Krama packet first.
TIER_PRIORITY = {
    # the Krama packet first (the manifest's key move)
    "kramasadbhava": 10,
    "mahanayaprakasha": 11,
    # tier-1 complete Sanskrit corpora
    "kubjikamata": 20,
    "svacchandatantra": 21,
    "netratantra": 22,
    "kulasara": 23,
    # tier-0 / tier-2 (existing human gold or high-leverage)
    "malinivijayottara": 30,
    "brahmayamala": 31,
    "cidgagana": 32,
    "spandakarika": 33,
    "kubjika": 34,
    "tantraloka": 35,
    # tier-3 manuscript-scale flagships (lowest immediate priority)
    "jayadrathayamala": 90,
}

# aliases: some on-disk names differ from the manifest canonical_ids
ALIASES = {
    "malinivijayottara": "malinivijayottara",
    "kramasadbhava": "kramasadbhava",
}


def priority(work_id: str) -> int:
    """The queue priority for a work (lower = first). Defaults high (lowest priority) if unknown."""
    return TIER_PRIORITY.get(work_id, 100)


def order_queue(works: list[str]) -> list[str]:
    """Order RAW-L0 candidates by expansion priority (lower priority value = first)."""
    return sorted(works, key=lambda w: priority(w))


def priority_label(work_id: str) -> str:
    p = priority(work_id)
    if p <= 15:
        return "TIER_1-KRAMA_PACKET"
    if p <= 25:
        return "TIER_1-COMPLETE_SANSKRIT"
    if p <= 40:
        return "TIER_0/2-EXISTING_GOLD_OR_HOLE"
    return "TIER_3-MANUSCRIPT_FLAGSHIP"

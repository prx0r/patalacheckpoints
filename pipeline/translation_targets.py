#!/usr/bin/env python3
"""pipeline/translation_targets.py — the PRIORITIZED translation-target QUEUE (the huge queue).

Grounded in the Śiva-acquisition / expansion docs
(docs/vision/expansion/vision-11-siva-before-abhinava-corpus-manifest.md) + the download manifest
(data/corpus/downloads/siva-corpus-download-manifest.json). This is the FULL intended corpus —
all works Pāṭala plans to acquire/translate, prioritized by the expansion tiers.

Each target carries:
  priority   (lower = first)
  tier       the expansion tier (0 ingest-gold / 1 complete-Sanskrit / 2 translate-holes / 3 flagships)
  status     INGEST (has/gold) | TRANSLATE (needs L0+translation) | MANUSCRIPT (huge, later)
  source     the download manifest's canonical_id / tradition / date / rights

The queue (agent3_queue.py) processes targets whose source is on disk as RAW_SANSKRIT first; the
full list here is the master registry so new work is always ordered correctly.

The manifest's key move: build the KRAMA PACKET first (kālīkulapañcaśatikā + kramasadbhāva +
devīdvyardhaśatikā + mahānayaprakāśa + jñānanetra) to establish Krama terminology/ontology/deity
graph before the 24,000-verse Jayadrathayāmala.
"""
from __future__ import annotations

# canonical_id -> {priority, tier, status, tradition}
# priority: lower = higher. Grounded in the expansion tiers + the Krama-first key move.
TARGETS = {
    # ── the KRAMA PACKET first (the manifest's key change) ──
    "kramasadbhava":         {"priority": 10, "tier": "1", "status": "TRANSLATE", "tradition": "Kālīkrama"},
    "mahanayaprakasha":      {"priority": 11, "tier": "1", "status": "TRANSLATE", "tradition": "Krama"},
    "kalikulapancasatika":   {"priority": 12, "tier": "1", "status": "TRANSLATE", "tradition": "Kālīkrama"},
    # ── TIER 1: complete Sanskrit corpora ──
    "kubjikamata":           {"priority": 20, "tier": "1", "status": "INGEST", "tradition": "Kubjikā Kaula"},
    "svacchandatantra":      {"priority": 21, "tier": "1", "status": "TRANSLATE", "tradition": "Bhairava"},
    "netratantra":           {"priority": 22, "tier": "1", "status": "TRANSLATE", "tradition": "Bhairava"},
    "kulasara":              {"priority": 23, "tier": "1", "status": "TRANSLATE", "tradition": "early Kaula"},
    "siddhayogesvarimata":   {"priority": 24, "tier": "0", "status": "INGEST", "tradition": "Vidyāpīṭha"},
    # ── TIER 0/2: existing human gold or high-leverage ──
    "malinivijayottara":     {"priority": 30, "tier": "0", "status": "INGEST", "tradition": "Trika"},
    "tantrasadbhava":        {"priority": 31, "tier": "2", "status": "INGEST", "tradition": "Trika"},
    "malinislokavarttika":   {"priority": 32, "tier": "2", "status": "TRANSLATE", "tradition": "Trika (Abhinava)"},
    "sivadrsti":             {"priority": 33, "tier": "0", "status": "INGEST", "tradition": "Pratyabhijñā"},
    "kiranatantra":          {"priority": 34, "tier": "0", "status": "INGEST", "tradition": "Śaiva Siddhānta"},
    "brahmayamala":          {"priority": 35, "tier": "2", "status": "INGEST", "tradition": "Bhairava/Śākta"},
    "cidgagana":             {"priority": 36, "tier": "2", "status": "TRANSLATE", "tradition": "Krama"},
    "spandakarika":          {"priority": 37, "tier": "0", "status": "TRANSLATE", "tradition": "Spanda"},
    "kubjika":               {"priority": 38, "tier": "2", "status": "TRANSLATE", "tradition": "Kubjikā"},
    "tantraloka":            {"priority": 39, "tier": "1", "status": "TRANSLATE", "tradition": "Trika (Abhinava)"},
    # ── TIER 3: manuscript-scale flagships (later) ──
    "jayadrathayamala":      {"priority": 90, "tier": "3", "status": "MANUSCRIPT", "tradition": "Kālīkula"},
    "manthanabhairava":      {"priority": 91, "tier": "3", "status": "MANUSCRIPT", "tradition": "Kaula/Kubjikā"},
    "devyamala":             {"priority": 92, "tier": "3", "status": "MANUSCRIPT", "tradition": "Śākta/Kaula"},
}


def all_targets() -> dict:
    """The full prioritized registry (the huge queue master list)."""
    return dict(sorted(TARGETS.items(), key=lambda kv: kv[1]["priority"]))


def priority(work_id: str) -> int:
    """Queue priority (lower = first). Unknown works = 100 (lowest)."""
    return TARGETS.get(work_id, {}).get("priority", 100)


def tier(work_id: str) -> str:
    return TARGETS.get(work_id, {}).get("tier", "?")


def status(work_id: str) -> str:
    return TARGETS.get(work_id, {}).get("status", "?")


def order_queue(works: list[str]) -> list[str]:
    """Order RAW-L0 candidates by expansion priority (lower priority value = first)."""
    return sorted(works, key=lambda w: priority(w))


def priority_label(work_id: str) -> str:
    p = priority(work_id)
    if p <= 15:
        return "KRAMA_PACKET"
    if p <= 25:
        return "TIER1-COMPLETE_SANSKRIT"
    if p <= 40:
        return "TIER0/2-GOLD_OR_HOLE"
    return "TIER3-MANUSCRIPT_FLAGSHIP"

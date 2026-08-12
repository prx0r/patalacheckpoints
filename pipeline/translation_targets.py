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


# ─────────────────────────────────────────────────────────────────────────────
# LEADS — the full translation-target corpus from the untranslated registers + acquisition board
# (corpus/targets/untranslated.md I, untranslated2.md II, untranslated3.md III, targetacquired.md).
# These are tracked as leads (acquisition/translation candidates). source: vishvasa/Muktabodha/GRETIL
# per the registers. register = which untranslated register listed it. Some overlap the action TARGETS.
# ─────────────────────────────────────────────────────────────────────────────
LEADS = {
    # register I (the 20 highest-value)
    "tantrasadbhava":          {"register": "I", "n": 1, "source": "Muktabodha/Bang", "note": "highest-return untranslated"},
    "devipancasataka":         {"register": "I", "n": 2, "source": "Muktabodha", "note": "Twelve Kālīs; = kalikulapancasatika"},
    "yonigahvaratantra":       {"register": "I", "n": 3, "source": "MS-request", "note": "no public scan"},
    "satsahasrasamhita":       {"register": "I", "n": 4, "source": "Muktabodha", "note": "Kubjikā expansion"},
    "srimatottara":            {"register": "I", "n": 5, "source": "Muktabodha", "note": "Kubjikā expansion"},
    "kularatnoddyota":         {"register": "I", "n": 6, "source": "Muktabodha", "note": "Kaula/Kubjikā bridge"},
    "cincinmatasarasamuccaya": {"register": "I", "n": 7, "source": "LANDED", "note": "best bridge text; on disk"},
    "urmikaularnava":          {"register": "I", "n": 9, "source": "Dyczkowski e-ed", "note": "Abhinava knew it"},
    "kalikulakrama":           {"register": "I", "n": 11, "source": "Muktabodha", "note": "Krama preservation"},
    "kalanalatantra":          {"register": "I", "n": 13, "source": "NGMPP e-text", "note": "Kubjikā-associated"},
    "pingalamata":             {"register": "I", "n": 15, "source": "Muktabodha", "note": "Jayadrathādhikāra"},
    "varahitantra":            {"register": "I", "n": 17, "source": "study-only", "note": "late synthesis"},
    "mahakalasamhita":         {"register": "I", "n": 18, "source": "editions", "note": "huge later Kālī corpus"},
    "kubjika_liturgy":         {"register": "I", "n": 20, "source": "Muktabodha M00547-51", "note": "ritual cluster"},
    # register II (sources behind the famous sources)
    "laghvikamnaya":           {"register": "II", "n": 22, "source": "MS-request", "note": "earlier KMT recension"},
    "kulapancasika":           {"register": "II", "n": 23, "source": "LOCATE", "note": "attributed Matsyendra"},
    "kularatnamala":           {"register": "II", "n": 27, "source": "specialist-hunt", "note": "KMT draws on it"},
    "trisirobhairava":         {"register": "II", "n": 28, "source": "specialist-hunt", "note": "grouped with Trika"},
    "kramavilasastotra":       {"register": "II", "n": 29, "source": "codex-unicus", "note": "Sanderson prints chunk"},
    "kalasamkarsinimata":      {"register": "II", "n": 30, "source": "vishvasa", "note": "Kālasaṃkarṣiṇī material"},
    "kalikarahasya":           {"register": "II", "n": 31, "source": "M00242", "note": ""},
    "mahaguhyakalividhana":    {"register": "II", "n": 32, "source": "M00403/M00516", "note": ""},
    "padyavahini":             {"register": "II", "n": 37, "source": "M00676", "note": ""},
    "kankalamalinitantra":     {"register": "II", "n": 40, "source": "M00026", "note": ""},
    # register III (the next 20, #41-60)
    "yogapithakramodaya":      {"register": "III", "n": 41, "source": "M00281", "note": "earliest recovered Kaula"},
    "nityakaulatantra":        {"register": "III", "n": 42, "source": "wikisource", "note": "pre-10th Tripurā"},
    "svacchandoddyota":        {"register": "III", "n": 45, "source": "M00091", "note": "Kṣemarāja's commentary"},
    "netradyota":              {"register": "III", "n": 47, "source": "OCHS/M00504", "note": "Kṣemarāja 9-22"},
    "tantralokaviveka":        {"register": "III", "n": 49, "source": "vishvasa", "note": "Jayaratha — HUGE, privileged evidence"},
    "nisvasaguhyasutra":       {"register": "III", "n": 50, "source": "vishvasa", "note": "deep historical baseline"},
    "brhatkalottaratantra":    {"register": "III", "n": 51, "source": "NGMPP A43/1", "note": "early Siddhānta"},
    "kalottaragama":           {"register": "III", "n": 52, "source": "M00248/IFP", "note": ""},
    "matangaparamesvara":      {"register": "III", "n": 53, "source": "GRETIL", "note": "Siddhānta control group"},
    "mrgendragama":            {"register": "III", "n": 54, "source": "GRETIL", "note": "Siddhānta control group"},
    "rauravagama":             {"register": "III", "n": 55, "source": "GRETIL", "note": "Siddhānta control group"},
    "vimalavati":              {"register": "III", "n": 56, "source": "NGMPP A186/10", "note": "Siddhānta exegesis"},
    "kaulasutra":              {"register": "III", "n": 58, "source": "hareesh", "note": "64 sūtras, one-shot target"},
    "paratantra":              {"register": "III", "n": 59, "source": "M00062", "note": "screen first"},
    "brahmasandhana":          {"register": "III", "n": 60, "source": "M00262", "note": "BHU MS, screen first"},
}


def all_leads() -> dict:
    """The full tracked leads (registers I-III + acquisition board). ~60 targets."""
    return dict(sorted(LEADS.items(), key=lambda kv: (kv[1]["register"], kv[1]["n"])))


def summary() -> dict:
    """The huge queue: actionable TARGETS + tracked LEADS + tracked pipeline works."""
    from l0_registry import summary as _reg  # noqa: F401  (avoid heavy import in CLI)
    return {
        "actionable_targets": len(TARGETS),
        "tracked_leads": len(LEADS),
        "targets": list(all_targets().keys()),
        "leads": list(all_leads().keys()),
    }

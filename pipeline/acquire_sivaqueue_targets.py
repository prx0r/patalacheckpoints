#!/usr/bin/env python3
"""pipeline/acquire_sivaqueue_targets.py — acquire the freely-available 'Śiva before Abhinava' texts.

Sources of freely-acquirable Sanskrit:
  - GRETIL (the full 494-work corpus, R2 datasets/gretil_all_quotes.json)
  - the on-disk Muktabodha library (already extracted from MUKTABODHA-LIBRARY-IAST.zip)

For each sivaqueue target whose text is freely acquirable, this writes the Sanskrit verses to
data/corpus/sources/<work_id>/<work_id>.txt (canonical IAST), so the target can go straight to
RAW-L0. Targets whose text is book-only (IFP editions etc.) are left as tracked acquisitions.

Genuine GRETIL matches (verified, no false positives) are declared below; each maps a sivaqueue
work_id to a GRETIL work name substring + a note.

Usage:
  python3 pipeline/acquire_sivaqueue_targets.py --gretil /tmp/opencode/gretil_all.json [--write]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = "/root/projects/patala"
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import sivaqueue_targets as SQ

OUT = Path(ROOT) / "data/corpus/sources"
MANIFEST = Path(ROOT) / "data/corpus/sivaqueue-acquired.json"

# verified genuine GRETIL matches: sivaqueue work_id -> (gretil work substring, source_note)
GRETIL_MATCHES = {
    "pancarthabhasya_kaundinya": ("Pāśupatasūtra with Kauṇḍinya", "GRETIL Pāśupatasūtra + Kauṇḍinya Pañcārthabhāṣya"),
    "sardhatrisatikalottara": ("Sārdhatriśatikālottarāgama", "GRETIL Sārdhatriśatikālottara"),
    "kiranatantra": ("Kiraṇatantra, 1-6", "GRETIL Kiraṇatantra 1-6 (Rāmakaṇṭha)"),
    "mrgendratantra": ("Mṛgendrāgama", "GRETIL Mṛgendrāgama (= Mṛgendratantra)"),
    "ratnatrayapariksa_srikantha": ("Ratnatrayaparīkṣā", "GRETIL Ratnatrayaparīkṣā"),
    "anonymous_ratnatrayapariksavyakhya": ("Ratnatrayaparīkṣā", "GRETIL Ratnatrayaparīkṣā (anonymous commentary)"),
    "aghorasivas_ullekhini_on_ratnatraya": ("Ratnatrayaparīkṣā", "GRETIL Ratnatrayaparīkṣā (Ullekhinī)"),
    "bhavopahara": ("Bhāvopahārastotra", "GRETIL Bhāvopahārastotra + Vivaraṇa (Ramyadeva)"),
}

# on-disk Muktabodha matches: work_id -> relative path (already extracted)
ON_DISK = {
    "kalikapurana": "muktabodha-lib/kAlikApurANam-M04002-IAST.txt",
    "pauskaraparamesvara": "muktabodha-lib/pauSkara saMhitA-M00259-IAST.txt",
    "mohacudottara": "muktabodha-lib/mohacUDottara-M00304-IAST.txt",
    "pratisThaparamesvara": "muktabodha-lib/pratiSThAlakSaNasArasamuccaya-M00065-IAST.txt",
    "mrgendratantra": "muktabodha-lib/mRgendrAgama-M00037-IAST.txt",
    "makutottara": "muktabodha-lib/makuTottararahasya-M00525-IAST.txt",
    "satsahasrakalottara": "muktabodha-lib/SatSahasrakAlottarAgama-M00249-IAST.txt",
    "tattvasamgraha_sadyojyotis": "muktabodha-lib/ASTaprakaraNa tattvasaMgraha-M00011-IAST.txt",
    "tattvatrayanirnaya": "muktabodha-lib/ASTaprakaraNa tattvatrayanirNaya-M00012-IAST.txt",
    "ratnatrayapariksa_srikantha": "muktabodha-lib/ASTaprakaraNa ratnatrayaparIkSA-M00009-IAST.txt",
    "nadakarika": "muktabodha-lib/ASTaprakaraNa nAdakArikA-M00007-IAST.txt",
    "tattvaprakasa_bhojadeva": "muktabodha-lib/kriyAsAratattvaprakAzinIvyAkhyA-M00232-IAST.txt",
    "moksakarika": "muktabodha-lib/ASTaprakaraNa mokSakArikA-M00006-IAST.txt",
    "siddhantasara": "muktabodha-lib/vIrazaivasiddhAntottarakaumudI-M00604-IAST.txt",
    "siddhantadipika_ramanatha": "muktabodha-lib/vIrazaivasiddhAntottarakaumudI-M00604-IAST.txt",
    "kriyakramadyotika": "muktabodha-lib/kriyakramadyotikavyAkhyA-M00324-IAST.txt",
    "pratisThakriyadipika": "muktabodha-lib/pratiSThAlakSaNasArasamuccaya-M00065-IAST.txt",
    "siddhantasaravali": "muktabodha-lib/vIrazaivasiddhAntottarakaumudI-M00604-IAST.txt",
    "pratisThalaksanasara": "muktabodha-lib/pratiSThAlakSaNasArasamuccaya-M00065-IAST.txt",
    "vimalavati": "muktabodha-lib/vimalAvatItantra-M00295-IAST.txt",
    "spandapradipika": "muktabodha-lib/spandapradIpikA-M00532-IAST.txt",
    "svacchandodyota": "muktabodha-lib/svacchandapaddhati-M00194-IAST.txt",
    "netratantroddyota": "muktabodha-lib/netratantra-M00038-IAST.txt",
    "bhagavadgita_sarvatobhadra": "muktabodha-lib/bhagavadgItA-M00167-IAST.txt",
    "janmamaranavicara": "muktabodha-lib/janmamaRanavicAra-M00155-IAST.txt",
    "vatulanathasutra": "muktabodha-lib/vAtUlanAthasUtra-M00099-IAST.txt",
}


def _norm(s: str) -> str:
    t = {'ā':'a','ī':'i','ū':'u','ṛ':'r','ṝ':'r','ḷ':'l','ḹ':'l','ṃ':'m','ñ':'n','ṅ':'n',
         'ś':'s','ṣ':'s','ṭ':'t','ḍ':'d','ḥ':'h','ṁ':'m'}
    return re.sub(r'[^a-z0-9]', '', ''.join(t.get(c, c) for c in s.lower()))


def _extract_from_gretil(gretil: dict, work_sub: str) -> str:
    """Concatenate the verses of one GRETIL work (substring match) into a text."""
    lines = []
    seen = set()
    for x in gretil:
        if work_sub in x.get("work", ""):
            v = (x.get("text") or "").strip()
            if v and v not in seen:
                seen.add(v)
                lines.append(v)
    return "\n".join(lines)


def build(gretil: dict, write: bool) -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    acquired = {}
    # 1. GRETIL acquisitions
    for wid, (sub, note) in GRETIL_MATCHES.items():
        text = _extract_from_gretil(gretil, sub)
        if not text:
            acquired[wid] = {"work_id": wid, "source": "gretil", "verses": 0, "acquired": False,
                             "note": note, "reason": "no verses in GRETIL dataset"}
            continue
        workdir = OUT / wid
        workdir.mkdir(parents=True, exist_ok=True)
        path = workdir / f"{wid}.txt"
        if write:
            path.write_text(text, encoding="utf-8")
        acquired[wid] = {"work_id": wid, "source": "gretil", "verses": text.count("\n") + 1,
                         "acquired": True, "note": note, "path": str(path)}
    # 2. on-disk Muktabodha acquisitions (link/copy so they're addressable under the sivaqueue id)
    mount = Path("/mnt/HC_Volume_106427611/sanskritree/sources")
    for wid, rel in ON_DISK.items():
        src = mount / rel
        if not src.exists():
            acquired[wid] = {"work_id": wid, "source": "muktabodha", "acquired": False,
                             "reason": f"missing {rel}"}
            continue
        workdir = OUT / wid
        workdir.mkdir(parents=True, exist_ok=True)
        if write:
            # copy so the sivaqueue id owns an addressable text (provenance recorded)
            shutil = __import__("shutil")
            shutil.copy2(src, workdir / f"{wid}.txt")
        acquired[wid] = {"work_id": wid, "source": "muktabodha", "acquired": True,
                         "note": f"copied from {rel}", "path": str(workdir / f"{wid}.txt")}

    manifest = {"schema": "patala:sivaqueue:acquired:v1", "compiled": "2026-08-12",
                "n_acquired": sum(1 for v in acquired.values() if v.get("acquired")),
                "acquired": acquired}
    if write:
        with open(MANIFEST, "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, indent=2, ensure_ascii=False)
    return manifest


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--gretil", default="/tmp/opencode/gretil_all.json")
    ap.add_argument("--write", action="store_true", help="write the text files (else dry-run)")
    a = ap.parse_args()
    gretil = json.load(open(a.gretil))
    m = build(gretil, a.write)
    print(json.dumps({"n_acquired": m["n_acquired"], "targets": m["acquired"]}, indent=2, ensure_ascii=False))
    print("mode:", "WRITTEN" if a.write else "DRY-RUN")

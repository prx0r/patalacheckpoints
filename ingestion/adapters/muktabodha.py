"""ingestion/adapters/muktabodha.py — the MUKTABODHA ReconciliationAdapter (R2 IAST e-text library).

ALIGNED with ingestion-refinery.md + the GRETIL/SARIT adapter pattern. Muktabodha (Muktabodha
Indological Research Institute) publishes Śaiva/Śākta/Tantra IAST e-texts under CC BY-NC 4.0. The
R2 snapshot is `source/ingestion/MUKTABODHA/snapshots/muktabodha-library-2026-08-14/` (500 IAST .txt).

Each file carries a clean header we parse (never guessed):
    Catalog number: M00008
    Uniform title: ...
    Main title: ...
    Author : ...
    Commentator : ...
    Editor : ...

Design laws (unchanged):
  - MUKTABODHA ids (M00008) are crosswalk identifiers, NEVER canonical identity (PATA-W-... survives).
  - License CC BY-NC 4.0 -> recorded on every object (discovery/index/provenance; partner, don't relicense).
  - A Muktabodha e-text is a TextInstance, not yet a canonical Work (resolve separately).
  - Raw is preserved forever; reconciliation produces new objects.

This is a ReconciliationAdapter subclass (source-evidence/schema/external_record.py) — the contract is
reused, not redefined. It reads the R2/local snapshot files (file ingestion), not the network.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path
from typing import Optional

_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_ROOT / "source-evidence" / "schema"))

from external_record import ExternalRecord, ReconciliationAdapter  # noqa: E402

LICENSE = "CC-BY-NC-4.0"


def _parse_header(text: str) -> dict:
    """Parse the Muktabodha IAST file header into structured fields (never guess)."""
    out = {"catalog_no": "", "uniform_title": "", "main_title": "", "secondary_title": "",
           "author": "", "commentator": "", "editor": "", "description": ""}
    for line in text.splitlines()[:40]:
        line = line.strip()
        low = line.lower()
        if low.startswith("catalog number"):
            out["catalog_no"] = line.split(":", 1)[1].strip() if ":" in line else ""
        elif low.startswith("uniform title"):
            out["uniform_title"] = line.split(":", 1)[1].strip() if ":" in line else ""
        elif low.startswith("main title"):
            out["main_title"] = line.split(":", 1)[1].strip() if ":" in line else ""
        elif low.startswith("secondary title"):
            out["secondary_title"] = line.split(":", 1)[1].strip() if ":" in line else ""
        elif re.match(r"^author\s*:", low):
            out["author"] = line.split(":", 1)[1].strip() if ":" in line else ""
        elif low.startswith("commentator"):
            out["commentator"] = line.split(":", 1)[1].strip() if ":" in line else ""
        elif low.startswith("editor"):
            out["editor"] = line.split(":", 1)[1].strip() if ":" in line else ""
        elif low.startswith("description"):
            out["description"] = line.split(":", 1)[1].strip() if ":" in line else ""
    return out


class MuktabodhaAdapter(ReconciliationAdapter):
    source = "MUKTABODHA"
    license = LICENSE
    access_constraints = "R2 snapshot (500 IAST e-texts); no public API"
    source_authority = "Muktabodha Indological Research Institute"
    update_cadence = "manual snapshot (2026-08-14)"
    entity_types = ["TEXT_INSTANCE", "WORK"]
    rights = "CC-BY-NC-4.0 (non-commercial); discovery/index/provenance; partner, do not relicense"

    def __init__(self, local_dir: Optional[str] = None, snapshot_id: str = "muktabodha-library-2026-08-14"):
        """local_dir: extracted snapshot dir (muktabodha-lib/ holding the .txt files), or None = R2.
        Reads from the local/R2 snapshot files (file ingestion), never the network."""
        self.local_dir = Path(local_dir) if local_dir else None
        self.snapshot_id = snapshot_id

    # ---- ReconciliationAdapter contract ----

    def snapshot(self) -> dict:
        return {"source": self.source, "snapshot_id": self.snapshot_id, "license": self.license,
                "layout": "muktabodha-lib/*.txt (IAST)"}

    def _files(self) -> list[Path]:
        if self.local_dir and self.local_dir.exists():
            d = self.local_dir / "muktabodha-lib" if (self.local_dir / "muktabodha-lib").exists() else self.local_dir
            return sorted(d.glob("*.txt"))
        return []

    def fetch(self, params: dict) -> list[dict]:
        """Read the snapshot files -> {path, catalog_no, text} (raw, never modified)."""
        rows = []
        for p in self._files():
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:  # noqa: BLE001
                continue
            header = _parse_header(text)
            rows.append({"path": str(p), "name": p.name, "text": text, "header": header})
        return rows

    def normalize(self, raw: dict) -> dict:
        h = raw.get("header", {})
        # derive a catalog id from the filename when the header lacks one (e.g. M00008)
        cat = h.get("catalog_no") or (re.search(r"M\d+", raw.get("name", "")).group(0) if re.search(r"M\d+", raw.get("name", "")) else raw.get("name"))
        title = h.get("main_title") or h.get("uniform_title") or raw.get("name")
        author = h.get("author") or h.get("commentator") or ""
        return {
            "external_id": cat,
            "title": title,
            "author_raw": author,
            "incipit": next((l.strip() for l in raw.get("text", "").splitlines() if l.strip() and not l.strip().startswith("#") and ":" not in l[:20]), "")[:160],
            "extra": {"catalog_no": h.get("catalog_no"), "uniform_title": h.get("uniform_title"),
                      "commentator": h.get("commentator"), "editor": h.get("editor"),
                      "license": self.license, "path": raw.get("name"),
                      "design_law": "Muktabodha e-text is a TextInstance, not a canonical Work (resolve separately)"},
        }

    def emit_external_records(self, raws: list[dict]) -> list[ExternalRecord]:
        out = []
        for r in raws:
            n = self.normalize(r)
            if not n["external_id"]:
                continue
            sha = hashlib.sha256(n["incipit"].encode()).hexdigest()[:16]
            out.append(ExternalRecord(
                source=self.source,
                external_id=f"muktabodha:{n['external_id']}",
                title_raw=n["title"],
                author_raw=n["author_raw"],
                incipit_raw=n["incipit"],
                retrieved_at=self.snapshot_id,
                extra={**n["extra"], "incipit_sha": sha, "license": self.license},
            ))
        return out

    def map_identifiers(self, rec: dict) -> dict:
        return {"scheme": "MUKTABODHA", "value": rec.get("external_id", "").replace("muktabodha:", ""),
                "url": f"https://muktabodha.org/catalog/{rec.get('external_id','').replace('muktabodha:','')}"}

    def export_enrichment(self) -> list[dict]:
        return [{"type": "license_firewall", "source": self.source, "license": self.license,
                 "policy": "CC-BY-NC: discovery/index/provenance; partner, do not relicense"}]

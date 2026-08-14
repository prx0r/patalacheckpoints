"""ingestion/adapters/gretil.py — the GRETIL ReconciliationAdapter.

ALIGNED with ingestion-refinery.md §7-§8 + the existing `acquire_sivaqueue34_gretil.py` logic:

  - GRETIL's clean machine-readable e-texts are IAST HTML; we strip to the Sanskrit body and register
    them as a GRETIL ExternalRecord per work (a TextInstance, not yet a Work — §8: GRETIL file != Work).
  - GRETIL now has stable GitHub/TextGrid snapshots; each work carries a git-commit SHA (Bronze).
  - Per-file license: GRETIL material is mostly freely redistributable, but record it per file.

This is a ReconciliationAdapter subclass (source-evidence/schema/external_record.py). It reuses the
HTML-stripping + IAST heuristic from the factory's existing acquire script (kept here so intake is a
single, reuse-first path).
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path
from typing import Optional

_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_ROOT / "source-evidence" / "schema"))
sys.path.insert(0, str(_ROOT / "source-evidence" / "evals" / "patala" / "tasks"))

from external_record import ExternalRecord, ReconciliationAdapter

GRETIL_HOME = "https://gretil.sub.uni-goettingen.de"


def _strip_html(html: str) -> str:
    """Extract the IAST Sanskrit body from a GRETIL HTML page (reused from acquire_sivaqueue34_gretil.py)."""
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "head", "title"]):
            tag.decompose()
        text = soup.get_text("\n")
    except Exception:
        text = re.sub(r"<[^>]+>", "\n", html)
    lines = []
    for line in text.splitlines():
        s = line.strip()
        iast = len(re.findall(r"[āīūṛṝḷḹṃñṅśṣṭḍḥṁ]", s))
        if iast >= 3 and len(re.findall(r"[A-Za-zāīūṛṝḷḹṃñṅśṣṭḍḥ]", s)) > 10:
            lines.append(s)
    return "\n".join(lines)


class GretilAdapter(ReconciliationAdapter):
    source = "GRETIL"
    license = "per-file"
    access_constraints = "public e-texts; stable GitHub mirror"
    source_authority = "GRETIL (gretil.sub.uni-goettingen.de) + INDOLOGY/GRETIL-mirror"
    update_cadence = "per git commit"
    entity_types = ["TEXT_INSTANCE", "WORK", "PUBLICATION"]
    rights = "per-file license; record each file's license, do not assume uniform"

    def __init__(self, targets: Optional[dict] = None, git_commit: str = "snapshot",
                 local_dir: Optional[str] = None):
        """targets: {work_id: (gretil_url, short_title)} — mirrors acquire_sivaqueue34_gretil.TARGETS."""
        self.targets = targets or {}
        self.git_commit = git_commit
        self.local_dir = Path(local_dir) if local_dir else None

    # ---- ReconciliationAdapter contract ----

    def snapshot(self) -> dict:
        return {"source": self.source, "snapshot_id": f"gretil-{self.git_commit}",
                "license": self.license, "git_commit": self.git_commit,
                "n_targets": len(self.targets)}

    def fetch(self, params: dict) -> list[dict]:
        """Download each GRETIL e-text -> {work_id, url, html}. Fails-closed per work."""
        import subprocess

        rows = []
        for wid, (url, title) in self.targets.items():
            html = ""
            raw_path = None
            if self.local_dir:
                raw_path = self.local_dir / wid / f"{wid}.html"
                if raw_path.exists():
                    html = raw_path.read_text(encoding="utf-8", errors="ignore")
            if not html:
                cmd = ["curl", "-sL", "-m", "240", "-A", "Mozilla/5.0 (X11; Linux x86_64)", url]
                try:
                    html = subprocess.run(cmd, capture_output=True).stdout.decode("utf-8", "ignore")
                except Exception:  # noqa: BLE001
                    html = ""
            if not html:
                rows.append({"work_id": wid, "title": title, "url": url, "html": "", "ok": False})
                continue
            rows.append({"work_id": wid, "title": title, "url": url, "html": html, "ok": True})
        return rows

    def normalize(self, raw: dict) -> dict:
        text = _strip_html(raw.get("html", "")) if raw.get("ok") else ""
        return {
            "external_id": raw.get("work_id"),
            "title": raw.get("title", ""),
            "author": "",
            "incipit": text[:120],
            "extra": {"url": raw.get("url"), "text_chars": len(text), "ok": raw.get("ok"),
                      "git_commit": self.git_commit},
        }

    def emit_external_records(self, raws: list[dict]) -> list[ExternalRecord]:
        out = []
        for r in raws:
            n = self.normalize(r)
            sha = hashlib.sha256((n["incipit"] or "").encode()).hexdigest()[:16]
            out.append(ExternalRecord(
                source=self.source,
                external_id=f"gretil:{n['external_id']}",
                title_raw=n["title"],
                author_raw=n["author"],
                incipit_raw=n["incipit"],
                retrieved_at=self.git_commit,
                extra={**n["extra"], "incipit_sha": sha,
                       "design_law": "GRETIL file is a TextInstance, not a canonical Work (resolve separately)"},
            ))
        return out

    def map_identifiers(self, rec: dict) -> dict:
        return {"scheme": "GRETIL", "value": rec.get("external_id", "").replace("gretil:", ""),
                "url": f"{GRETIL_HOME}/cgi-bin/etext.pl"}

    def export_enrichment(self) -> list[dict]:
        return [{"type": "text_instance_resolution",
                 "note": "GRETIL files resolve to canonical Work/Edition via the entity resolver"}]

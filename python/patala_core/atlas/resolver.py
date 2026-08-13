"""patala_core.atlas.resolver — the I3 source resolver slice.

Resolves a work's identity + edition + etext provenance against external authorities and records
PER-DIMENSION AuthorityEvidence in the Atlas Postgres. This is the Agent 2 side of the
Agent 1 Atlas NAT contract:

    Agent 2 resolver → SourceResolutionCandidate → Agent 1 Atlas NAT → SourceResolutionFinding[]

Per Agent 1's directive, authority is MULTIDIMENSIONAL — never a single `verified=true` or a lone
`authority_state: EDITION_VERIFIED` string. We record per-dimension evidence and derive convenience
gates (factory_eligible, publication_eligible, scholar_review_eligible) as explicit predicates.

Authority dimensions (per atlas-database.md / agent1atlas.md):
    WORK_IDENTITY · AUTHOR_IDENTITY · EDITION_IDENTITY · ETEXT_DERIVATION · WITNESS_LINKAGE ·
    DATE_PRECISION · RIGHTS

No automatic authority promotion from fuzzy matching. Results are candidates + evidence + open
dimensions; Agent 1 decides trust.

Run:
    python3 python/patala_core/atlas/resolver.py --work matangaparamesvara
    python3 python/patala_core/atlas/resolver.py --work matangaparamesvara --json
"""
from __future__ import annotations

import json
import re
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import os
ROOT = Path(os.environ.get("PATALA_ROOT", "/root/projects/patala"))

# ── authority ladder (shared vocabulary, per design doc) ─────────────────────────
# Literal producer vocabulary (per peer review — authority inflation fix):
#   an internal crosswalk is INTERNAL_IDENTITY_BOUND, NOT multi-source corroboration;
#   a single external search hit is EXTERNAL_CANDIDATE_FOUND, NOT multi-source;
#   MULTI_SOURCE_MATCHED requires >=2 epistemically independent sources + field agreement.
LADDER = [
    "UNKNOWN", "DISCOVERED", "INTERNAL_IDENTITY_BOUND", "EXTERNAL_CANDIDATE_FOUND",
    "CATALOG_MATCHED", "MULTI_SOURCE_MATCHED", "COPY_INSPECTED",
    "EDITION_VERIFIED", "TEXT_DERIVATION_VERIFIED", "SCHOLAR_CONFIRMED",
]
DIMENSIONS = ["WORK_IDENTITY", "AUTHOR_IDENTITY", "EDITION_IDENTITY",
              "ETEXT_DERIVATION", "WITNESS_LINKAGE", "DATE_PRECISION", "RIGHTS"]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _norm(s: str) -> str:
    t = {'ā':'a','ī':'i','ū':'u','ṛ':'r','ṝ':'r','ḷ':'l','ḹ':'l','ṃ':'m','ṁ':'m',
         'ñ':'n','ṅ':'n','ṇ':'n','ś':'s','ṣ':'s','ṭ':'t','ḍ':'d','ḥ':'h'}
    return re.sub(r'[^a-z0-9 ]', '', ''.join(t.get(c, c) for c in s.lower()))


def _atlas_label(wid: str) -> str:
    from patala_core.atlas.adapter import ATLAS_FILES, ROOT as _R
    for fn in ATLAS_FILES:
        p = _R / "data" / "atlas" / fn
        if not p.exists():
            continue
        txt = p.read_text(encoding="utf-8")
        m = re.search(r'\{\s*"?id"?\s*:\s*"' + re.escape(wid) + r'"\s*,?\s*"?work"?\s*:\s*"([^"]+)"', txt)
        if m:
            return m.group(1)
    return wid


def _legacy_to_uuid(wid: str) -> str:
    """Resolve the Atlas work uuid from the legacy id via the crosswalk; else a deterministic uuid."""
    from patala_core.atlas.adapter import PostgresBackend
    try:
        m = PostgresBackend().legacy_id_map()
        if wid in m:
            return m[wid]
    except Exception:
        pass
    import hashlib
    return str(uuid.UUID(bytes=hashlib.md5(wid.encode()).digest()[:16]))


# ── external authority adapters (reuse the verify_editions logic) ────────────────
def _archive_search(query: str, rows: int = 5, timeout: int = 30) -> dict:
    import subprocess
    q = _norm(query).replace(" ", "+")
    url = (f"https://archive.org/advancedsearch.php?q={q}"
           f"&fl%5B%5D=identifier&fl%5B%5D=title&rows={rows}&output=json")
    try:
        r = subprocess.run(["curl", "-s", "-m", str(timeout), url], capture_output=True, text=True)
        d = json.loads(r.stdout)
        docs = d.get("response", {}).get("docs", [])
        return {"num_found": d.get("response", {}).get("numFound", 0),
                "hits": [{"identifier": x.get("identifier"), "title": str(x.get("title", ""))[:80]} for x in docs]}
    except Exception as e:
        return {"num_found": 0, "hits": [], "error": str(e)[:120]}


def _crosswalk_has(wid: str) -> bool:
    try:
        from patala_core.atlas.adapter import PostgresBackend
        return wid in PostgresBackend().legacy_id_map()
    except Exception:
        return False


def resolve_work(wid: str, net: bool = True) -> dict:
    """Resolve one work into a SourceResolutionCandidate with per-dimension authority evidence."""
    label = _atlas_label(wid) or wid
    query_label = re.split(r'\s*[—–]\s*', label)[0].strip()

    evidence = {}   # dimension -> {relation, source_scheme, payload}
    attestations = []

    # WORK_IDENTITY + EDITION_IDENTITY from archive.org + the crosswalk
    atlas_uuid = _legacy_to_uuid(wid)
    # The internal Pāṭala legacy-id → UUID crosswalk is an INTERNAL mapping, not external
    # corroboration. Only genuine independent-source agreement is MULTI_SOURCE_MATCHED.
    if _crosswalk_has(wid):
        work_relation = "INTERNAL_IDENTITY_BOUND"
    else:
        work_relation = "DISCOVERED"
    evidence["WORK_IDENTITY"] = {
        "relation": work_relation,
        "source_scheme": "ATLAS_CROSSWALK", "payload": {"legacy_id": wid, "atlas_uuid": atlas_uuid},
    }
    evidence["AUTHOR_IDENTITY"] = {"relation": "UNSUPPORTED", "source_scheme": "NONE",
                                   "payload": {"note": "authority from bibliography; not yet reconciled"}}

    if net:
        ed = _archive_search(query_label + " sanskrit")
        tr = _archive_search(query_label + " translation")
        attestations += [
            {"source": "archive.org", "kind": "edition", "num_found": ed.get("num_found", 0), "hits": ed.get("hits", [])},
            {"source": "archive.org", "kind": "translation", "num_found": tr.get("num_found", 0), "hits": tr.get("hits", [])},
        ]
        time.sleep(1)
        # One archive.org query with search hits is an EXTERNAL CANDIDATE, never multi-source.
        # MULTI_SOURCE_MATCHED requires >=2 independent sources + field agreement (checked by
        # Agent 1 Atlas NAT, which also catches SOURCE_ECHO when catalogues copy one record).
        edition_relation = "EXTERNAL_CANDIDATE_FOUND" if ed.get("num_found", 0) > 0 else "DISCOVERED"
        evidence["EDITION_IDENTITY"] = {
            "relation": edition_relation,
            "source_scheme": "ARCHIVE_ORG",
            "payload": {"num_found": ed.get("num_found", 0), "hits": ed.get("hits", [])[:3]},
        }
    else:
        evidence["EDITION_IDENTITY"] = {"relation": "DISCOVERED", "source_scheme": "ATLAS_SEED", "payload": {}}

    # honest OPEN / UNKNOWN for the dimensions we cannot resolve yet
    for dim in ("ETEXT_DERIVATION", "WITNESS_LINKAGE", "DATE_PRECISION", "RIGHTS"):
        evidence.setdefault(dim, {"relation": "OPEN", "source_scheme": "UNRESOLVED", "payload": {}})

    return {
        "type": "SOURCE_RESOLUTION_CANDIDATE",
        "work_id": wid,
        "atlas_uuid": atlas_uuid,
        "label": label,
        "authority": evidence,
        "attestations": attestations,
        "open_dimensions": [d for d in DIMENSIONS if evidence.get(d, {}).get("relation") in ("OPEN", "UNSUPPORTED")],
        "gates": {
            "factory_eligible": _gate(evidence, "factory"),
            "publication_eligible": _gate(evidence, "publication"),
            "scholar_review_eligible": _gate(evidence, "scholar"),
        },
        "note": "Resolution candidate + evidence. Not a claim of scholarly verification; Agent 1 Atlas NAT decides trust.",
    }


def _gate(evidence: dict, kind: str) -> bool:
    """Explicit predicates — never a scalar rank.

    Authority-inflation fix (A1-Q1 + devpath13 P1 audit):
      - INTERNAL_IDENTITY_BOUND (crosswalk) / EXTERNAL_CANDIDATE_FOUND (single hit) are NOT
        publication-grade. Only genuine corroboration qualifies.
      - EVERY gate must be RIGHTS-aware: a candidate with RIGHTS=UNKNOWN or RIGHTS=DISCOVERABLE
        (searchable-only) must NOT open `factory` or `publication`, no matter how strong the
        edition/identity evidence is. This closes the P1 audit finding (resolver opened publication
        on a rights-UNKNOWN candidate).
      - `factory` requires a usable (copy-inspected / verified) edition, not just a high work identity.
    """
    wid = evidence.get("WORK_IDENTITY", {}).get("relation", "DISCOVERED")
    ed = evidence.get("EDITION_IDENTITY", {}).get("relation", "DISCOVERED")
    rights = evidence.get("RIGHTS", {}).get("relation", "UNKNOWN")

    # rights ladder: DISCOVERABLE=searchable-only; processing allowed; redistributable; open license
    rights_usable = rights in ("PROCESSING_ALLOWED", "REDISTRIBUTABLE", "OPEN_LICENSE")
    rights_publishable = rights in ("REDISTRIBUTABLE", "OPEN_LICENSE")

    if kind == "factory":
        # usable as a translation source: a real edition + processing rights (never rights-UNKNOWN)
        return ed in ("MULTI_SOURCE_MATCHED", "COPY_INSPECTED", "EDITION_VERIFIED") and rights_usable
    if kind == "publication":
        # publishable only with redistributable rights AND a genuinely verified/copy-inspected edition
        return rights_publishable and ed in ("COPY_INSPECTED", "EDITION_VERIFIED")
    if kind == "scholar":
        # a positively identified work (for review); scholar review does not require publication rights
        return wid in ("CATALOG_MATCHED", "MULTI_SOURCE_MATCHED") or ed in ("COPY_INSPECTED", "EDITION_VERIFIED")
    return False


def persist_evidence(wid: str, candidate: dict) -> int:
    """Write per-dimension authority_evidence rows to the Atlas Postgres. Returns rows written."""
    from patala_core.atlas.adapter import DEFAULT_DB_URL
    import psycopg2
    url = DEFAULT_DB_URL.replace("postgresql+psycopg2://", "postgresql://", 1)
    conn = psycopg2.connect(url)
    cur = conn.cursor()
    atlas_uuid = candidate["atlas_uuid"]
    n = 0
    for dim, ev in candidate["authority"].items():
        cur.execute(
            """INSERT INTO authority_evidence (id, subject_type, subject_id, dimension, source_scheme, relation, evidence_payload, asserted_at)
               VALUES (gen_random_uuid(),'work',%s,%s,%s,%s,%s, now())""",
            (atlas_uuid, dim, ev.get("source_scheme"), ev.get("relation"), json.dumps(ev.get("payload", {}))),
        )
        n += 1
    conn.commit()
    cur.close(); conn.close()
    return n


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-net", action="store_true")
    ap.add_argument("--persist", action="store_true", help="write authority_evidence rows to the Atlas")
    a = ap.parse_args()

    cand = resolve_work(a.work, net=not a.no_net)
    if a.persist:
        n = persist_evidence(a.work, cand)
        cand["persisted_evidence_rows"] = n
    if a.json:
        print(json.dumps(cand, indent=2, ensure_ascii=False, default=str))
    else:
        print(f"{cand['work_id']} — {cand['label']}")
        for dim, ev in cand["authority"].items():
            print(f"  {dim:22} {ev.get('relation'):20} ({ev.get('source_scheme')})")
        print("  open:", cand["open_dimensions"])
        print("  gates:", cand["gates"])
    return 0


if __name__ == "__main__":
    sys.exit(main())

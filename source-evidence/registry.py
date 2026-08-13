"""registry.py — seed the Publication + Witness registry from the existing structured sources.

The coordinator's principle: most of the generic substrate already exists. The Sanderson manifest
(`data/corpus/sources/sanderson/sanderson_manifest.json`) is already a machine-readable Publication->Witness
index (53 works, structured). The Ratié papers are curated from the scholarship corpus. We do NOT invent a new
ontology — we emit FaBiO-aligned Publications + Witnesses (with PROV provenance fields) from these seeds.
"""
from __future__ import annotations

import json
import os

from schema.source_evidence_profile import biblio_work, witness, sha256_file

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SANDERSON_MANIFEST = os.path.join(ROOT, "data", "corpus", "sources", "sanderson", "sanderson_manifest.json")
SCHOLARSHIP_DIR = "/mnt/HC_Volume_106427611/sanskritree/corpus/ipvv-anchor/scholarship"

# the Ratié papers most relevant to the argument golds (curated; path -> (publication metadata))
RATIE_PAPERS = {
    "Otherness_in_the_Pratyabhijna_Philosophy.pdf": {
        "title": "Otherness in the Pratyabhijñā Philosophy", "year": 2007, "venue": "Journal of Indian Philosophy 35",
    },
    "On_reason_and_scripture_in_the_Pratyabhi.pdf": {
        "title": "On Reason and Scripture in the Pratyabhijñā", "year": 2013,
        "venue": "Scriptural Authority, Reason and Action (ÖAW)",
    },
    "Can_one_prove_that_something_exists_beyo.pdf": {
        "title": "Can One Prove that Something Exists Beyond Consciousness?", "year": None, "venue": None,
    },
}


def sanderson_publications() -> list[dict]:
    """Emit a Publication + Witness per downloaded Sanderson work (FaBiO-aligned)."""
    with open(SANDERSON_MANIFEST, encoding="utf-8") as f:
        m = json.load(f)
    out = []
    for w in m.get("works", []):
        key = w.get("key") or ""
        df = w.get("downloaded_file")
        if not w.get("downloaded") or not df:
            continue
        path = os.path.join(os.path.dirname(SANDERSON_MANIFEST), df)
        if not os.path.exists(path):
            path = os.path.join(os.path.dirname(SANDERSON_MANIFEST), "academia_bundles", "consolidated", df)
            if not os.path.exists(path):
                continue
        pub = biblio_work(
            pub_id=f"pt:publication:sanderson:{key}",
            title=w.get("title", key), authors=["pt:person:alexis-sanderson"],
            year=w.get("year"), venue=None, pub_type=(w.get("type") or "ARTICLE").upper(),
            identifiers={},
        )
        wit = witness(
            witness_id=f"pt:witness:sanderson:{key}:file",
            pub_ref=pub["@id"], local_path=os.path.relpath(path, ROOT),
            sha256=sha256_file(path), format="PDF" if df.endswith(".pdf") else "TXT",
            source_uri=w.get("url"), extraction_status="NOT_EXTRACTED",
        )
        out.append((pub, wit))
    return out


def ratie_publications() -> list[dict]:
    """Emit a Publication + Witness per curated Ratié paper (FaBiO-aligned)."""
    out = []
    for fname, meta in RATIE_PAPERS.items():
        path = os.path.join(SCHOLARSHIP_DIR, fname)
        if not os.path.exists(path):
            continue
        slug = fname.split(".")[0]
        pub = biblio_work(
            pub_id=f"pt:publication:ratie:{slug}",
            title=meta["title"], authors=["pt:person:isabelle-ratie"],
            year=meta["year"], venue=meta["venue"], pub_type="ARTICLE",
        )
        wit = witness(
            witness_id=f"pt:witness:ratie:{slug}:file",
            pub_ref=pub["@id"], local_path=path,
            sha256=sha256_file(path), format="PDF", extraction_status="NOT_EXTRACTED",
        )
        out.append((pub, wit))
    return out


def build_registry() -> list[dict]:
    """All seeded Publications + Witnesses."""
    return sanderson_publications() + ratie_publications()


if __name__ == "__main__":
    pubs = build_registry()
    print(f"seeded {len(pubs)} Publication/Witness pairs")
    for pub, wit in pubs[:8]:
        print(f"  {pub['@id']} -> {os.path.basename(wit['local_path'])} ({wit['sha256'][:12]}…)")

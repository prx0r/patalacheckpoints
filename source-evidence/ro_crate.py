"""ro_crate.py — emit a Research Object Crate (RO-Crate) for a set of source publications.

RO-Crate is used as the PACKAGING / EXPORT / INTERCHANGE format only — NOT Pāṭala's database. The crate JSON-LD
graph carries FaBiO identities, PROV derivations, Web Annotation spans and Pāṭala SourceAssertions, so the same
crate is both a portable research corpus and a machine-resolvable evidence layer.
"""
from __future__ import annotations

import json
import os

from schema.source_evidence_profile import (STANDARD_ALIGNMENT, span, source_assertion, corroboration_event)

PROFILE_URL = "https://w3id.org/ro/crate"
PATALA_PROFILE = "pt:PatalaSourceEvidenceProfile_v0"


def emit_crate(*, pubs_wits: list, spans: list | None = None, assertions: list | None = None,
               corrs: list | None = None, out_dir: str) -> str:
    """Build an RO-Crate metadata graph and write ro-crate-metadata.json to out_dir."""
    os.makedirs(out_dir, exist_ok=True)
    graph = [
        {"@id": "ro-crate-metadata.json", "@type": "CreativeWork",
         "conformsTo": {"@id": PROFILE_URL},
         "about": {"@id": "./"}},
        {"@id": "./", "@type": "Dataset",
         "name": "Pāṭala Scholar Corpus Pilot (source-evidence v0)",
         "description": "FaBiO + PROV-O + Web Annotation + RO-Crate + Pāṭala SourceAssertions",
         "hasPart": [wit["@id"] for _, wit in pubs_wits]},
        {"@id": PATALA_PROFILE, "@type": "Profile",
         "name": "Pāṭala Source Evidence Profile v0",
         "alignment": STANDARD_ALIGNMENT},
    ]
    for pub, wit in pubs_wits:
        graph.append(pub)
        graph.append({**wit, "@type": [w for w in wit["@type"] if w != "fabio:Manifestation"] + ["File"]})
        # PROV derivation: the witness file is part of the publication
        graph.append({"@id": wit["@id"], "prov:specializationOf": pub["@id"]})
    graph.extend(spans or [])
    graph.extend(assertions or [])
    graph.extend(corrs or [])
    crate = {"@context": ["https://w3id.org/ro/crate/1.1/context",
                          {"oa": "http://www.w3.org/ns/oa#", "prov": "http://www.w3.org/ns/prov#",
                           "fabio": "http://purl.org/spar/fabio/", "pt": "https://patala.example/"}],
             "@graph": graph}
    out = os.path.join(out_dir, "ro-crate-metadata.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(crate, f, indent=2)
    return out


def crate_for_pilot(sources: list, spans: list, assertions: list, corrs: list, out_dir: str) -> str:
    return emit_crate(pubs_wits=sources, spans=spans, assertions=assertions, corrs=corrs, out_dir=out_dir)

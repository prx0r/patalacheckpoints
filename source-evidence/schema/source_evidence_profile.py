"""source_evidence_profile.py — Pāṭala Source Evidence Profile v0.

An application profile that COMPOSES existing standards (FaBiO / PROV-O / W3C Web Annotation / CiTO /
RO-Crate / IIIF) and adds a SMALL Pāṭala-native epistemic extension. This is NOT a new ontology — it maps each
Pāṭala object to the external standard that already models it, and keeps native only what none provide
(SourceAssertion, CorroborationEvent, authority/review state, dependency propagation).

External-standard alignment (the frozen schema stack):
  BibliographicWork/Witness  -> FaBiO (Work/Expression/Manifestation/Item)
  provenance / derivation    -> PROV-O (Entity/Activity/Agent)
  SourceSpan                 -> W3C Web Annotation (SpecificResource + selectors)
  publication citations      -> CiTO
  packaging                  -> RO-Crate (export/interchange only, not the DB)
  images/pages/assets        -> IIIF Presentation (compatibility from day one)
  metadata/IDs               -> DataCite / Crossref / OpenAlex (metadata witness, never canonical identity)

Pāṭala-native (the epistemic boundary none of the bibliographic standards provide):
  SourceAssertion · CorroborationEvent · review/authority state · dependency propagation
"""
from __future__ import annotations

import hashlib
import json


# ── the external-standard alignment ─────────────────────────────────────────────
STANDARD_ALIGNMENT = {
    "BibliographicWork": "fabio:Work",
    "Witness": "fabio:Manifestation/Item + PROV-O provenance",
    "SourceSpan": "W3C Web Annotation SpecificResource + selectors",
    "SourceAssertion": "Pāṭala-native (attributed actor commits to a structured proposition at a span)",
    "CorroborationEvent": "Pāṭala-native (proposition <-> SourceAssertion epistemic relation)",
    "CitationRelation": "CiTO",
    "Asset": "IIIF content resource",
    "Package": "RO-Crate",
    "Metadata": "DataCite/Crossref/OpenAlex (metadata witness)",
    "PrimaryTextIdentity": "CTS-compatible (TextGroup -> Work -> Edition/Translation -> Passage); keep pt:* internal",
    "TextAPI": "DTS-compatible (external text retrieval; internal = canonical graph)",
    "ArticleMarkup": "JATS (consume losslessly when available; JATS -> HTML -> born-digital PDF -> OCR PDF)",
    "PersonIdentity": "ORCID (sameAs) on pt:person:; internal id kept for historical actors without ORCID",
    "OrgIdentity": "ROR (sameAs) on pt:org:",
}


def biblio_work(*, pub_id: str, title: str, authors: list[str], year: int | None,
                venue: str | None = None, pub_type: str = "ARTICLE", identifiers: dict | None = None) -> dict:
    """A `pt:BibliographicWork` — the canonical identity (FaBiO-aligned)."""
    return {
        "@id": pub_id,
        "@type": ["fabio:Work", "pt:BibliographicWork"],
        "title": title,
        "author": authors,
        "year": year,
        "venue": venue,
        "publication_type": pub_type,
        "identifiers": identifiers or {},   # DOI/ISBN/OpenAlex — metadata witness, NOT the canonical id
    }


def witness(*, witness_id: str, pub_ref: str, local_path: str, sha256: str,
            format: str = "PDF", source_uri: str | None = None, derives_from: str | None = None,
            extraction_status: str = "NOT_EXTRACTED", rights: dict | None = None) -> dict:
    """A `pt:Witness` — one file of a Publication (FaBiO Manifestation/Item + PROV provenance)."""
    return {
        "@id": witness_id,
        "@type": ["fabio:Manifestation", "pt:Witness"],
        "publication_ref": pub_ref,
        "format": format,
        "sha256": sha256,
        "local_path": local_path,
        "source_uri": source_uri,
        "derives_from": derives_from,
        "extraction_status": extraction_status,
        "rights": rights or {},   # rights_status, license, copyright_holder, allowed_uses, attribution_requirement
    }


def span(*, span_id: str, witness_ref: str, page: int | None = None, section: str | None = None,
         paragraph: int | None = None, char_start: int | None = None, char_end: int | None = None,
         quote: str | None = None, prefix: str | None = None, suffix: str | None = None,
         span_sha256: str | None = None) -> dict:
    """A `pt:Span` — W3C Web Annotation SpecificResource with multiple resilient selectors."""
    selectors = {}
    if page is not None:
        selectors["HumanPageSelector"] = {"@type": "pt:HumanPageSelector", "page": page, "section": section,
                                          "paragraph": paragraph}
    if char_start is not None and char_end is not None:
        selectors["TextPositionSelector"] = {"@type": "oa:TextPositionSelector",
                                             "start": char_start, "end": char_end}
    if quote is not None:
        selectors["TextQuoteSelector"] = {"@type": "oa:TextQuoteSelector", "exact": quote,
                                          "prefix": prefix, "suffix": suffix}
    if span_sha256 is not None:
        selectors["PāṭalaHashSelector"] = {"@type": "pt:HashSelector", "span_sha256": span_sha256}
    return {
        "@id": span_id,
        "@type": ["oa:SpecificResource", "pt:Span"],
        "witness_ref": witness_ref,
        "selectors": selectors,
    }


def source_assertion(*, assertion_id: str, span_ref: str, attributed_to: str, claim: str,
                     assertion_type: str = "INTERPRETIVE", commitment: str = "ASSERTS",
                     extraction_origin: str = "MACHINE_PROPOSED", verification: str = "SPAN_UNVERIFIED",
                     extraction_activity: str | None = None) -> dict:
    """A `pt:SourceAssertion` — the Pāṭala-native epistemic bridge.

    `verification == SPAN_VERIFIED` means "the source really says this, adequately represented" — NOT
    "the assertion is philosophically true." Same Pāṭala discipline.
    """
    return {
        "@id": assertion_id,
        "@type": "pt:SourceAssertion",
        "source_span_ref": span_ref,
        "attributed_to": attributed_to,
        "claim": claim,
        "assertion_type": assertion_type,
        "commitment": commitment,
        "extraction_origin": extraction_origin,       # MACHINE_PROPOSED -> ...
        "verification": verification,                 # SPAN_UNVERIFIED -> SPAN_VERIFIED (not 'true')
        "extraction_activity": extraction_activity,   # PROV Activity (Hermes/model/editor/skill-version)
    }


def corroboration_event(*, corr_id: str, target_ref: str, source_assertion_ref: str, relation: str,
                        scope: str = "PROPOSITION", semantic_relation: str = "CONSERVATIVE_PARAPHRASE",
                        independence: str = "INDEPENDENT_AUTHOR", method: str = "MACHINE_MATCHED_HUMAN_SOURCE",
                        review_state: str = "MACHINE_VERIFIED_MAPPING", defeaters: list | None = None) -> dict:
    """A `pt:CorroborationEvent` — Pāṭala-native proposition <-> SourceAssertion epistemic relation."""
    return {
        "@id": corr_id,
        "@type": "pt:CorroborationEvent",
        "target_ref": target_ref,
        "source_assertion_ref": source_assertion_ref,
        "relation": relation,          # DIRECT_SUPPORT / PARTIAL_SUPPORT / DIRECT_CONTRADICTION /
                                       # ALTERNATIVE_READING / BACKGROUND_ONLY / NON_EQUIVALENT
        "scope": scope,
        "semantic_relation": semantic_relation,
        "independence": independence,  # SAME_AUTHOR / DERIVED_CITATION / INDEPENDENT_AUTHOR / ...
        "method": method,
        "review_state": review_state,
        "defeaters": defeaters or [],
    }


def sha256_file(path: str) -> str:
    """Cryptographic integrity hash of a witness file (a justified Pāṭala extension)."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def _json(obj):  # helper for tests/emitters
    return json.dumps(obj, indent=2, ensure_ascii=False)

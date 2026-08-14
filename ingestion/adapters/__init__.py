"""ingestion/adapters/ — concrete external-source ReconciliationAdapters (the real gap).

ALIGNED: the adapter contract is `source-evidence/schema/external_record.py::ReconciliationAdapter`.
Each adapter below implements that contract for one external source. Add new sources by subclassing
the same contract — never a parallel abstraction.

Integration-first order (globalpartnerships.md): Wikidata · OpenAlex · Crossref · VIAF · ROR ·
C-SALT · GRETIL · SARIT · PANDiT · NGMCP · IIIF. (OpenAlex/Crossref/ROR/ORCID/OpenCitations live in
source-evidence/production/adapters/.)

Design law for ALL: external IDs are crosswalk identifiers (external_identifier), NEVER canonical
identity. Imported facts are authority_evidence/assertions, never canonical fields. Raw preserved.
"""
from .pandit import PanditAdapter  # noqa: F401
from .gretil import GretilAdapter  # noqa: F401
from .wikidata import WikidataAdapter  # noqa: F401
from .viaf import ViafAdapter  # noqa: F401
from .csalt import CSaltAdapter  # noqa: F401
from .sarit import SaritAdapter  # noqa: F401
from .ngmcp import NgmcpAdapter  # noqa: F401
from .iiif import IiifAdapter  # noqa: F401

__all__ = [
    "PanditAdapter", "GretilAdapter", "WikidataAdapter", "ViafAdapter",
    "CSaltAdapter", "SaritAdapter", "NgmcpAdapter", "IiifAdapter",
]

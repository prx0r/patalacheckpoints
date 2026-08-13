"""production/core.py — Pāṭala Scholar Evidence Corpus: production core.

The productionized version of the S0.1 pilot. Turns real on-disk scholarship into a stable,
provenance-bound scholarly evidence layer:

    Publication → Witness → Span → SourceAssertion → Proposition link → Corroboration/Contestation candidate
        → Evidence view → corpus report

This module owns the deterministic object chain + the integrity invariants. It is NOT a UI, NOT a
benchmark harness, NOT an ontology explosion — it is the minimal production root the argument/review
engine consumes.

Schema-debt fixes relative to the pilot (per the mission brief):
  - target_proposition_ref is a canonical `pt:prop:*` ID (with a textual snapshot + hash where possible),
    not a free-form string.
  - independence describes SCHOLARLY lineage (SAME_AUTHOR / DERIVED_CITATION / INDEPENDENT_AUTHOR /
    INDEPENDENT_TEXTUAL_ANALYSIS / PRIMARY_EDITION / UNKNOWN), never MACHINE_SEGREGATED / process provenance.
  - Machine/extraction provenance stays in the assertion's provenance metadata, NOT in scholarly independence.
"""
from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone


# ── stable vocabularies ─────────────────────────────────────────────────────────
# Frozen scholarly-independence vocabulary (does NOT describe machine/process provenance).
INDEPENDENCE = ("SAME_AUTHOR", "DERIVED_CITATION", "INDEPENDENT_AUTHOR",
                "INDEPENDENT_TEXTUAL_ANALYSIS", "PRIMARY_EDITION", "UNKNOWN")
# SAME_PUBLICATION added narrowly (two spans within the same publication, but independent analyses):
# documented in the mission; still a scholarly-lineage term, not a process term.
INDEPENDENCE_ALL = INDEPENDENCE + ("SAME_PUBLICATION",)

# What an author does at a span — conservative, never strengthened by the extractor.
COMMITMENT = ("ASSERTS", "DENIES", "ATTRIBUTES_TO_OTHER", "QUOTES_OTHER",
              "EDITORIAL_RECONSTRUCTION", "UNCLEAR")

# Proposition <- SourceAssertion relation candidate (machine candidate unless adjudicated).
RELATION = ("DIRECT_SUPPORT", "PARTIAL_SUPPORT", "DIRECT_CONTRADICTION", "ALTERNATIVE_READING",
            "BACKGROUND_ONLY", "NON_EQUIVALENT", "UNDERDETERMINED")

# Four orthogonal statuses (never one scalar ladder).
STATUS_KEYS = ("evidence_status", "review_status", "publication_status", "generation_status")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def canonical_json(obj) -> str:
    """Deterministic JSON for hashing: sorted keys, compact, NFKC-normalized strings."""
    def _norm(o):
        if isinstance(o, str):
            import unicodedata
            return unicodedata.normalize("NFKC", o)
        if isinstance(o, list):
            return [_norm(x) for x in o]
        if isinstance(o, dict):
            return {k: _norm(v) for k, v in o.items()}
        return o
    return json.dumps(_norm(obj), sort_keys=True, separators=(",", ":"), ensure_ascii=False)


@dataclass
class Publication:
    """A pt:BibliographicWork — the canonical identity of a scholarly publication."""
    pub_id: str                       # pt:publication:<author>:<slug>
    title: str
    author: str                       # canonical person ref, e.g. pt:person:isabelle-ratie
    author_name: str
    year: int | None = None
    venue: str | None = None
    pub_type: str = "ARTICLE"
    identifiers: dict = field(default_factory=dict)   # DOI/ISBN — metadata witness, not canonical id

    def to_dict(self) -> dict:
        return {"@id": self.pub_id, "@type": ["fabio:Work", "pt:BibliographicWork"],
                "title": self.title, "author": self.author, "author_name": self.author_name,
                "year": self.year, "venue": self.venue, "publication_type": self.pub_type,
                "identifiers": self.identifiers}

    def object_hash(self) -> str:
        return sha256_text(canonical_json(self.to_dict()))

    def content_hash(self) -> str:
        d = self.to_dict()
        d.pop("@id", None)
        return sha256_text(canonical_json(d))


@dataclass
class Witness:
    """A pt:Witness — one immutable file of a Publication (FaBiO Manifestation + PROV)."""
    witness_id: str                   # pt:witness:<pub>:file
    pub_ref: str
    local_path: str
    sha256: str
    format: str = "PDF"
    extraction_status: str = "NOT_EXTRACTED"
    source_uri: str | None = None
    rights: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {"@id": self.witness_id, "@type": ["fabio:Manifestation", "pt:Witness"],
                "publication_ref": self.pub_ref, "format": self.format, "sha256": self.sha256,
                "local_path": self.local_path, "source_uri": self.source_uri,
                "extraction_status": self.extraction_status, "rights": self.rights}

    def object_hash(self) -> str:
        return sha256_text(canonical_json(self.to_dict()))

    def content_hash(self) -> str:
        """Content-only hash for dedup: same as object_hash but WITHOUT the assigned @id.

        Reruns of identical content must collapse to one object regardless of the id assigned
        on each run (the anti-multiple-corroboration invariant).
        """
        d = self.to_dict()
        d.pop("@id", None)
        return sha256_text(canonical_json(d))


@dataclass
class Span:
    """A pt:Span — W3C Web Annotation SpecificResource + resilient selectors."""
    span_id: str                      # pt:span:<pub>:<stable-locator>
    witness_ref: str
    page: int | None = None
    section: str | None = None
    paragraph: int | None = None
    char_start: int | None = None
    char_end: int | None = None
    quote: str | None = None
    prefix: str | None = None
    suffix: str | None = None
    span_sha256: str | None = None

    def to_dict(self) -> dict:
        return {"@id": self.span_id, "@type": ["oa:SpecificResource", "pt:Span"],
                "witness_ref": self.witness_ref,
                "page": self.page, "section": self.section, "paragraph": self.paragraph,
                "char_start": self.char_start, "char_end": self.char_end,
                "quote": self.quote, "prefix": self.prefix, "suffix": self.suffix,
                "span_sha256": self.span_sha256}

    def object_hash(self) -> str:
        return sha256_text(canonical_json(self.to_dict()))

    def content_hash(self) -> str:
        """Content-only hash for dedup: same as object_hash but WITHOUT the assigned @id."""
        d = self.to_dict()
        d.pop("@id", None)
        return sha256_text(canonical_json(d))


@dataclass
class SourceAssertion:
    """A pt:SourceAssertion — the Pāṭala-native epistemic bridge.

    `attributed_to` = the ACTOR the claim is attributed to (the author, or the quoted scholar).
    `commitment`   = what that actor does at the span (ASSERTS/DENIES/...), never strengthened.
    `extraction_origin`/`verification` = machine/extraction provenance, kept OUT of independence.
    """
    assertion_id: str
    span_ref: str
    attributed_to: str
    claim: str
    commitment: str = "ASSERTS"
    assertion_type: str = "INTERPRETIVE"
    extraction_origin: str = "MACHINE_PROPOSED"
    verification: str = "SPAN_UNVERIFIED"
    extraction_activity: str | None = None

    def to_dict(self) -> dict:
        return {"@id": self.assertion_id, "@type": "pt:SourceAssertion",
                "source_span_ref": self.span_ref, "attributed_to": self.attributed_to,
                "claim": self.claim, "commitment": self.commitment,
                "assertion_type": self.assertion_type, "extraction_origin": self.extraction_origin,
                "verification": self.verification, "extraction_activity": self.extraction_activity}

    def object_hash(self) -> str:
        return sha256_text(canonical_json(self.to_dict()))

    def content_hash(self) -> str:
        """Content-only hash for dedup: same as object_hash but WITHOUT the assigned @id."""
        d = self.to_dict()
        d.pop("@id", None)
        return sha256_text(canonical_json(d))


@dataclass
class Proposition:
    """A pt:Prop — a canonical, sourced proposition (10-25 in the first set)."""
    prop_id: str                      # pt:prop:<slug>
    formulation: str
    subject: str | None = None
    scope: str | None = None
    modality: str | None = None
    temporal_scope: str | None = None
    assumptions: str | None = None
    provenance: str = "FROM_SOURCE_EVIDENCE"

    def to_dict(self) -> dict:
        return {"@id": self.prop_id, "@type": "pt:Prop",
                "formulation": self.formulation, "subject": self.subject,
                "scope": self.scope, "modality": self.modality,
                "temporal_scope": self.temporal_scope, "assumptions": self.assumptions,
                "provenance": self.provenance}

    def object_hash(self) -> str:
        return sha256_text(canonical_json(self.to_dict()))

    def content_hash(self) -> str:
        d = self.to_dict()
        d.pop("@id", None)
        return sha256_text(canonical_json(d))


@dataclass
class EvidenceLink:
    """A SourceAssertion → Proposition relation candidate (machine candidate unless adjudicated)."""
    link_id: str
    assertion_ref: str
    prop_ref: str
    relation: str = "UNDERDETERMINED"
    independence: str = "UNKNOWN"
    scope: str = "PROPOSITION"
    review_state: str = "MACHINE_CANDIDATE"
    # the canonical proposition the assertion is offered as evidence for (schema-debt fix)
    target_proposition_ref: str | None = None
    target_proposition_snapshot: str | None = None
    target_proposition_hash: str | None = None

    def to_dict(self) -> dict:
        return {"@id": self.link_id, "@type": "pt:EvidenceLink",
                "assertion_ref": self.assertion_ref, "prop_ref": self.prop_ref,
                "relation": self.relation, "independence": self.independence,
                "scope": self.scope, "review_state": self.review_state,
                "target_proposition_ref": self.target_proposition_ref,
                "target_proposition_snapshot": self.target_proposition_snapshot,
                "target_proposition_hash": self.target_proposition_hash}

    def object_hash(self) -> str:
        return sha256_text(canonical_json(self.to_dict()))

    def content_hash(self) -> str:
        """Content-only hash for dedup: same as object_hash but WITHOUT the assigned @id."""
        d = self.to_dict()
        d.pop("@id", None)
        return sha256_text(canonical_json(d))


class Corpus:
    """In-memory canonical store with deterministic dedup + integrity invariants.

    All objects are stored under their canonical ID; identical content cannot create duplicate
    objects (reruns, re-ingestion, renamed files, duplicate PDFs are deduplicated by content hash).
    """

    def __init__(self) -> None:
        self.publications: dict[str, Publication] = {}
        self.witnesses: dict[str, Witness] = {}
        self.spans: dict[str, Span] = {}
        self.assertions: dict[str, SourceAssertion] = {}
        self.propositions: dict[str, Proposition] = {}
        self.links: dict[str, EvidenceLink] = {}
        self._content_index: dict[str, str] = {}   # object_hash -> id (dedup)
        self.duplicates_rejected = 0
        self.provenance_failures: list[str] = []

    def _dedup(self, kind: str, obj_hash: str, want_id: str) -> str:
        """Return the canonical id for content; reject true duplicates (reruns never double)."""
        key = f"{kind}:{obj_hash}"
        existing = self._content_index.get(key)
        if existing:
            self.duplicates_rejected += 1
            return existing
        self._content_index[key] = want_id
        return want_id

    def add_publication(self, p: Publication) -> str:
        if p.pub_id not in self.publications:
            self.publications[p.pub_id] = p
        return p.pub_id

    def add_witness(self, w: Witness) -> str:
        # duplicate-file guard: two witnesses of the SAME publication with the SAME content
        # (sha256) are ONE witness — a duplicated PDF/rename must not create a second
        # representation whose assertions would look like independent corroboration.
        for wid, existing in self.witnesses.items():
            if existing.pub_ref == w.pub_ref and existing.sha256 == w.sha256:
                self.duplicates_rejected += 1
                return wid
        if w.witness_id not in self.witnesses:
            self.witnesses[w.witness_id] = w
        return w.witness_id

    def add_span(self, s: Span) -> str:
        canonical = self._dedup("span", s.content_hash(), s.span_id)
        if canonical not in self.spans:
            self.spans[canonical] = s
        return canonical

    def add_assertion(self, a: SourceAssertion) -> str:
        canonical = self._dedup("assertion", a.content_hash(), a.assertion_id)
        if canonical not in self.assertions:
            self.assertions[canonical] = a
        return canonical

    def add_proposition(self, p: Proposition) -> str:
        if p.prop_id not in self.propositions:
            self.propositions[p.prop_id] = p
        return p.prop_id

    def add_link(self, l: EvidenceLink) -> str:
        canonical = self._dedup("link", l.content_hash(), l.link_id)
        if canonical not in self.links:
            self.links[canonical] = l
        return canonical

    def link(self, assertion_ref: str, prop_ref: str, relation: str,
             independence: str, snapshot: str, prop_hash: str) -> str:
        link_id = f"pt:link:{len(self.links) + 1}"
        l = EvidenceLink(
            link_id=link_id, assertion_ref=assertion_ref, prop_ref=prop_ref,
            relation=relation, independence=independence,
            target_proposition_ref=prop_ref, target_proposition_snapshot=snapshot,
            target_proposition_hash=prop_hash,
        )
        return self.add_link(l)

    def validate(self) -> list[str]:
        """Integrity check: every ref resolves; independence vocabulary respected; no machine provenance leaked."""
        errors = []
        for s in self.spans.values():
            if s.witness_ref not in self.witnesses:
                errors.append(f"span {s.span_id}: witness_ref {s.witness_ref} unresolved")
        for a in self.assertions.values():
            if a.span_ref not in self.spans:
                errors.append(f"assertion {a.assertion_id}: span_ref {a.span_ref} unresolved")
            if a.commitment not in COMMITMENT:
                errors.append(f"assertion {a.assertion_id}: bad commitment {a.commitment}")
        for l in self.links.values():
            if l.assertion_ref not in self.assertions:
                errors.append(f"link {l.link_id}: assertion_ref unresolved")
            if l.prop_ref not in self.propositions:
                errors.append(f"link {l.link_id}: prop_ref {l.prop_ref} unresolved")
            if l.independence not in INDEPENDENCE_ALL:
                errors.append(f"link {l.link_id}: bad independence {l.independence}")
            if l.relation not in RELATION:
                errors.append(f"link {l.link_id}: bad relation {l.relation}")
            if "MACHINE" in l.independence or "PROCESS" in l.independence:
                errors.append(f"link {l.link_id}: machine/process provenance leaked into independence")
        return errors

    def counts(self) -> dict:
        return {
            "publications": len(self.publications),
            "witnesses": len(self.witnesses),
            "spans": len(self.spans),
            "assertions": len(self.assertions),
            "propositions": len(self.propositions),
            "evidence_links": len(self.links),
            "duplicates_rejected": self.duplicates_rejected,
        }

    def dump(self, out_dir: str) -> str:
        os.makedirs(out_dir, exist_ok=True)
        manifest = {
            "schema_version": "v0.1",
            "generated_at": _now(),
            "counts": self.counts(),
            "provenance": {
                "extraction_origin": "CURATED_HUMAN_READ",
                "adjudicator": {"type": "MACHINE", "agent": "agent1",
                                "model": None, "prompt_hash": None},
                "review_status": "NOT_HUMAN_REVIEWED",
                "notes": ("Assertions are curated from actual source text (SPAN_VERIFIED). "
                          "Evidence links are MACHINE_CANDIDATE, not independently adjudicated. "
                          "None of this is expert gold; review_status stays NOT_HUMAN_REVIEWED "
                          "until independent human/expert adjudication."),
                "provenance_failures": self.provenance_failures,
            },
            "objects": {
                "publications": [p.to_dict() for p in self.publications.values()],
                "witnesses": [w.to_dict() for w in self.witnesses.values()],
                "spans": [s.to_dict() for s in self.spans.values()],
                "assertions": [a.to_dict() for a in self.assertions.values()],
                "propositions": [p.to_dict() for p in self.propositions.values()],
                "evidence_links": [l.to_dict() for l in self.links.values()],
            },
        }
        with open(os.path.join(out_dir, "corpus.json"), "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        return os.path.join(out_dir, "corpus.json")

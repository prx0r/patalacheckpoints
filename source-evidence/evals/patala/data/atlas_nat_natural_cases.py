#!/usr/bin/env python3
"""evals/patala/data/atlas_nat_natural_cases.py — ATLAS-NAT-NATURAL-v1 frozen natural cases.

The peer review's central correction, applied: a natural benchmark is NOT a mutation suite that the
harness was designed to catch. These are REAL historical / source-resolution ambiguities a researcher
actually meets, frozen with their HONEST expected authority state.

CRITICAL DESIGN LAW (A1-CONTINUE-v2 P14/P15, the overfitting fix):

    Each case carries BOTH:
      authority    the relation labels the resolver CLAIMED (what it output)
      evidence     the independent FACTUAL evidence it actually had (sources, inspection, rights)

    The evaluator derives the HONEST CEILING for each dimension from `evidence` — NOT from any
    hand-written label. A false promotion is when the claimed `authority` EXCEEDS what the `evidence`
    factually licenses. This is non-circular: the spec (evidence → honest ceiling) is separate from the
    claimed output (authority), so the evaluator cannot be reverse-engineered from my own labels.

    `expect_promotion` is used ONLY as ground-truth for scoring detection recall/precision. The
    evaluator's verdict itself never reads it.

Design law (from the review):
    UNKNOWN -> OPEN  is cheap (always allowed, never penalized)
    UNKNOWN -> VERIFIED is dangerous (a false promotion)
    internal crosswalk != MULTI_SOURCE_MATCHED
    one archive.org hit != MULTI_SOURCE_MATCHED
"""
from __future__ import annotations

# -- the 8 scored dimensions (A1-CONTINUE-v2 P0) ------------------------------------------------
DIMENSIONS = (
    "WORK_IDENTITY", "AUTHOR_IDENTITY", "EDITION_IDENTITY", "ETEXT_DERIVATION",
    "WITNESS_LINKAGE", "DATE_PRECISION", "RIGHTS", "SOURCE_INDEPENDENCE",
)


def _case(id_, category, authority, evidence, gates=None, expect_promotion=False, note=""):
    return {
        "id": id_, "category": category, "authority": authority,
        "evidence": evidence, "gates": gates or {}, "expect_promotion": expect_promotion,
        "note": note,
    }


# fmt: off
NATURAL_CASES = [
    # ── A. exact, unambiguous work (fully corroborated, all gates open) ─────────────────────────
    _case("nat-001", "EXACT_UNAMBIGUOUS",
          {"WORK_IDENTITY": "MULTI_SOURCE_MATCHED", "AUTHOR_IDENTITY": "MULTI_SOURCE_CONFIRMED",
           "EDITION_IDENTITY": "EDITION_VERIFIED", "ETEXT_DERIVATION": "TRANSCRIPTION_VERIFIED",
           "WITNESS_LINKAGE": "MULTI_WITNESS", "DATE_PRECISION": "c.995", "RIGHTS": "OPEN_LICENSE",
           "SOURCE_INDEPENDENCE": "MULTI_SOURCE"},
          {"independent_sources": 3, "archive_hit": False, "crosswalk": False,
           "catalog_match": True, "edition_inspected": True, "etext_verified": True,
           "witnesses": 4, "rights_granted": "OPEN_LICENSE", "date_exact": True, "echo": False},
          gates={"factory": True, "publication": True, "scholar": True},
          note="LoC + NMM + GRETIL edition statement independently agree; edition inspected; rights open → every gate may open"),

    # ── B. homonymous titles / aliases ──────────────────────────────────────────────────────────
    _case("nat-002", "HOMONYMOUS_TITLE",
          {"WORK_IDENTITY": "EXTERNAL_CANDIDATE_FOUND", "AUTHOR_IDENTITY": "UNKNOWN",
           "EDITION_IDENTITY": "DISCOVERED", "ETEXT_DERIVATION": "OPEN",
           "WITNESS_LINKAGE": "UNRESOLVED", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "UNKNOWN",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 1, "archive_hit": True, "crosswalk": False,
           "catalog_match": False, "edition_inspected": False, "etext_verified": False,
           "witnesses": 0, "rights_granted": "UNKNOWN", "date_exact": False, "echo": False},
          note="two distinct works share the title; one weak archive hit cannot disambiguate → stay open"),

    _case("nat-003", "HOMONYMOUS_TITLE",
          {"WORK_IDENTITY": "CATALOG_MATCHED", "AUTHOR_IDENTITY": "UNKNOWN",
           "EDITION_IDENTITY": "CATALOG_MATCHED", "ETEXT_DERIVATION": "PROBABLE_BASIS",
           "WITNESS_LINKAGE": "UNRESOLVED", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "DISCOVERABLE",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 1, "archive_hit": False, "crosswalk": False,
           "catalog_match": True, "edition_inspected": False, "etext_verified": False,
           "witnesses": 0, "rights_granted": "DISCOVERABLE", "date_exact": False, "echo": False,
           "ambiguous_match": True},
          expect_promotion=True,
          note="FALSE PROMOTION: a single catalogue title-match for a homonymous work is not a confirmed WORK_IDENTITY"),

    _case("nat-004", "ALIAS",
          {"WORK_IDENTITY": "INTERNAL_IDENTITY_BOUND", "AUTHOR_IDENTITY": "CATALOG_SUPPORTED",
           "EDITION_IDENTITY": "DISCOVERED", "ETEXT_DERIVATION": "OPEN",
           "WITNESS_LINKAGE": "UNRESOLVED", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "DISCOVERABLE",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 1, "archive_hit": False, "crosswalk": True,
           "catalog_match": True, "edition_inspected": False, "etext_verified": False,
           "witnesses": 0, "rights_granted": "DISCOVERABLE", "date_exact": False, "echo": False},
          note="same work under an alias; bound only by the internal crosswalk → WORK_IDENTITY=INTERNAL_IDENTITY_BOUND is honest"),

    # ── C. same title / different authors ───────────────────────────────────────────────────────
    _case("nat-005", "SAME_TITLE_DIFF_AUTHOR",
          {"WORK_IDENTITY": "EXTERNAL_CANDIDATE_FOUND", "AUTHOR_IDENTITY": "CATALOG_SUPPORTED",
           "EDITION_IDENTITY": "DISCOVERED", "ETEXT_DERIVATION": "OPEN",
           "WITNESS_LINKAGE": "UNRESOLVED", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "UNKNOWN",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 1, "archive_hit": True, "crosswalk": False,
           "catalog_match": True, "edition_inspected": False, "etext_verified": False,
           "witnesses": 0, "rights_granted": "UNKNOWN", "date_exact": False, "echo": False},
          note="hit could be the other author's text; work identity stays open, one catalogue supports the author"),

    # ── D. anonymous works / disputed authorship ────────────────────────────────────────────────
    _case("nat-006", "ANONYMOUS",
          {"WORK_IDENTITY": "CATALOG_MATCHED", "AUTHOR_IDENTITY": "UNKNOWN",
           "EDITION_IDENTITY": "CATALOG_MATCHED", "ETEXT_DERIVATION": "OPEN",
           "WITNESS_LINKAGE": "UNRESOLVED", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "DISCOVERABLE",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 1, "archive_hit": False, "crosswalk": False,
           "catalog_match": True, "edition_inspected": False, "etext_verified": False,
           "witnesses": 0, "rights_granted": "DISCOVERABLE", "date_exact": False, "echo": False},
          note="traditionally anonymous; author must stay UNKNOWN (never filled in)"),

    _case("nat-007", "DISPUTED_AUTHORSHIP",
          {"WORK_IDENTITY": "CATALOG_MATCHED", "AUTHOR_IDENTITY": "CATALOG_SUPPORTED",
           "EDITION_IDENTITY": "CATALOG_MATCHED", "ETEXT_DERIVATION": "OPEN",
           "WITNESS_LINKAGE": "UNRESOLVED", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "DISCOVERABLE",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 1, "archive_hit": False, "crosswalk": False,
           "catalog_match": True, "edition_inspected": False, "etext_verified": False,
           "witnesses": 0, "rights_granted": "DISCOVERABLE", "date_exact": False, "echo": False},
          note="scholars dispute attribution; one catalogue supports it → CATALOG_SUPPORTED, not MULTI_SOURCE_CONFIRMED"),

    # ── E. approximate dates ────────────────────────────────────────────────────────────────────
    _case("nat-008", "APPROXIMATE_DATE",
          {"WORK_IDENTITY": "MULTI_SOURCE_MATCHED", "AUTHOR_IDENTITY": "MULTI_SOURCE_CONFIRMED",
           "EDITION_IDENTITY": "EDITION_VERIFIED", "ETEXT_DERIVATION": "TRANSCRIPTION_VERIFIED",
           "WITNESS_LINKAGE": "MULTI_WITNESS", "DATE_PRECISION": "10th-11th c.", "RIGHTS": "OPEN_LICENSE",
           "SOURCE_INDEPENDENCE": "MULTI_SOURCE"},
          {"independent_sources": 2, "archive_hit": False, "crosswalk": False,
           "catalog_match": True, "edition_inspected": True, "etext_verified": True,
           "witnesses": 3, "rights_granted": "OPEN_LICENSE", "date_exact": False, "echo": False},
          note="scholars only date to a century-range → date must remain approximate, not rendered c.995"),

    _case("nat-009", "APPROXIMATE_DATE",
          {"WORK_IDENTITY": "CATALOG_MATCHED", "AUTHOR_IDENTITY": "CATALOG_SUPPORTED",
           "EDITION_IDENTITY": "CATALOG_MATCHED", "ETEXT_DERIVATION": "OPEN",
           "WITNESS_LINKAGE": "UNRESOLVED", "DATE_PRECISION": "c.1000 (approx.)", "RIGHTS": "DISCOVERABLE",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 1, "archive_hit": False, "crosswalk": False,
           "catalog_match": True, "edition_inspected": False, "etext_verified": False,
           "witnesses": 0, "rights_granted": "DISCOVERABLE", "date_exact": False, "echo": False},
          note="'c.1000 (approx.)' flagged approximate is honest"),

    # ── F. modern reprints of old editions ──────────────────────────────────────────────────────
    _case("nat-010", "MODERN_REPRINT",
          {"WORK_IDENTITY": "MULTI_SOURCE_MATCHED", "AUTHOR_IDENTITY": "MULTI_SOURCE_CONFIRMED",
           "EDITION_IDENTITY": "EXTERNAL_CANDIDATE_FOUND", "ETEXT_DERIVATION": "PROBABLE_BASIS",
           "WITNESS_LINKAGE": "UNRESOLVED", "DATE_PRECISION": "2012", "RIGHTS": "PROCESSING_ALLOWED",
           "SOURCE_INDEPENDENCE": "MULTI_SOURCE"},
          {"independent_sources": 2, "archive_hit": True, "crosswalk": False,
           "catalog_match": True, "edition_inspected": False, "etext_verified": False,
           "witnesses": 0, "rights_granted": "PROCESSING_ALLOWED", "date_exact": True, "echo": False},
          note="2012 reprint of an 1890 edition; reprint is not the critical edition → edition stays a weak candidate"),

    _case("nat-035", "MODERN_REPRINT",
          {"WORK_IDENTITY": "MULTI_SOURCE_MATCHED", "AUTHOR_IDENTITY": "MULTI_SOURCE_CONFIRMED",
           "EDITION_IDENTITY": "CATALOG_MATCHED", "ETEXT_DERIVATION": "PROBABLE_BASIS",
           "WITNESS_LINKAGE": "UNRESOLVED", "DATE_PRECISION": "1890", "RIGHTS": "PROCESSING_ALLOWED",
           "SOURCE_INDEPENDENCE": "MULTI_SOURCE"},
          {"independent_sources": 2, "archive_hit": False, "crosswalk": False,
           "catalog_match": True, "edition_inspected": False, "etext_verified": False,
           "witnesses": 0, "rights_granted": "PROCESSING_ALLOWED", "date_exact": False, "echo": False},
          expect_promotion=True,
          note="FALSE PROMOTION: catalogue-match of a reprint alone is not EDITION_VERIFIED / a critical edition"),

    # ── G. edition vs e-text confusion ──────────────────────────────────────────────────────────
    _case("nat-011", "EDITION_ETEXT_CONFUSION",
          {"WORK_IDENTITY": "MULTI_SOURCE_MATCHED", "AUTHOR_IDENTITY": "MULTI_SOURCE_CONFIRMED",
           "EDITION_IDENTITY": "CATALOG_MATCHED", "ETEXT_DERIVATION": "TRANSCRIPTION_VERIFIED",
           "WITNESS_LINKAGE": "UNRESOLVED", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "PROCESSING_ALLOWED",
           "SOURCE_INDEPENDENCE": "MULTI_SOURCE"},
          {"independent_sources": 2, "archive_hit": False, "crosswalk": False,
           "catalog_match": True, "edition_inspected": False, "etext_verified": True,
           "witnesses": 0, "rights_granted": "PROCESSING_ALLOWED", "date_exact": False, "echo": False},
          note="e-text transcription verified but edition not inspected → EDITION_IDENTITY=CATALOG_MATCHED honest"),

    _case("nat-031", "EDITION_ETEXT_CONFUSION",
          {"WORK_IDENTITY": "MULTI_SOURCE_MATCHED", "AUTHOR_IDENTITY": "MULTI_SOURCE_CONFIRMED",
           "EDITION_IDENTITY": "EDITION_VERIFIED", "ETEXT_DERIVATION": "TRANSCRIPTION_VERIFIED",
           "WITNESS_LINKAGE": "MULTI_WITNESS", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "PROCESSING_ALLOWED",
           "SOURCE_INDEPENDENCE": "MULTI_SOURCE"},
          {"independent_sources": 2, "archive_hit": False, "crosswalk": False,
           "catalog_match": True, "edition_inspected": False, "etext_verified": True,
           "witnesses": 2, "rights_granted": "PROCESSING_ALLOWED", "date_exact": False, "echo": False},
          expect_promotion=True,
          note="FALSE PROMOTION: EDITION_VERIFIED claimed although the edition was never inspected (only catalogued)"),

    # ── H. GRETIL with unclear printed basis ────────────────────────────────────────────────────
    _case("nat-012", "GRETIL_UNCLEAR_BASIS",
          {"WORK_IDENTITY": "EXTERNAL_CANDIDATE_FOUND", "AUTHOR_IDENTITY": "UNKNOWN",
           "EDITION_IDENTITY": "DISCOVERED", "ETEXT_DERIVATION": "PROBABLE_BASIS",
           "WITNESS_LINKAGE": "UNRESOLVED", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "DISCOVERABLE",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 1, "archive_hit": True, "crosswalk": False,
           "catalog_match": False, "edition_inspected": False, "etext_verified": False,
           "witnesses": 0, "rights_granted": "DISCOVERABLE", "date_exact": False, "echo": False},
          note="GRETIL file states no printed basis → derivation stays PROBABLE_BASIS"),

    _case("nat-032", "GRETIL_UNCLEAR_BASIS",
          {"WORK_IDENTITY": "EXTERNAL_CANDIDATE_FOUND", "AUTHOR_IDENTITY": "UNKNOWN",
           "EDITION_IDENTITY": "DISCOVERED", "ETEXT_DERIVATION": "OPEN",
           "WITNESS_LINKAGE": "UNRESOLVED", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "DISCOVERABLE",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 1, "archive_hit": True, "crosswalk": False,
           "catalog_match": False, "edition_inspected": False, "etext_verified": False,
           "witnesses": 0, "rights_granted": "DISCOVERABLE", "date_exact": False, "echo": False},
          note="GRETIL header names no edition → derivation must stay OPEN"),

    # ── I. SARIT with explicit edition provenance ──────────────────────────────────────────────
    _case("nat-013", "SARIT_EXPLICIT_PROVENANCE",
          {"WORK_IDENTITY": "CATALOG_MATCHED", "AUTHOR_IDENTITY": "CATALOG_SUPPORTED",
           "EDITION_IDENTITY": "CATALOG_MATCHED", "ETEXT_DERIVATION": "TRANSCRIPTION_VERIFIED",
           "WITNESS_LINKAGE": "SINGLE_WITNESS", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "PROCESSING_ALLOWED",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 1, "archive_hit": False, "crosswalk": False,
           "catalog_match": True, "edition_inspected": False, "etext_verified": True,
           "witnesses": 1, "rights_granted": "PROCESSING_ALLOWED", "date_exact": False, "echo": False},
          gates={"factory": True, "publication": False, "scholar": True},
          note="SARIT provenance explicit for derivation + one witness; rights processing-only → publication closed"),

    _case("nat-033", "SARIT_EXPLICIT_PROVENANCE",
          {"WORK_IDENTITY": "CATALOG_MATCHED", "AUTHOR_IDENTITY": "CATALOG_SUPPORTED",
           "EDITION_IDENTITY": "COPY_INSPECTED", "ETEXT_DERIVATION": "TRANSCRIPTION_VERIFIED",
           "WITNESS_LINKAGE": "SINGLE_WITNESS", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "PROCESSING_ALLOWED",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 1, "archive_hit": False, "crosswalk": False,
           "catalog_match": True, "edition_inspected": True, "etext_verified": True,
           "witnesses": 1, "rights_granted": "PROCESSING_ALLOWED", "date_exact": False, "echo": False},
          gates={"factory": True, "publication": False, "scholar": True},
          note="SARIT edition copy-inspected → COPY_INSPECTED honest; rights processing-only → publication closed"),

    # ── J. Muktabodha provenance differences ────────────────────────────────────────────────────
    _case("nat-014", "MUKTABODHA",
          {"WORK_IDENTITY": "CATALOG_MATCHED", "AUTHOR_IDENTITY": "CATALOG_SUPPORTED",
           "EDITION_IDENTITY": "CATALOG_MATCHED", "ETEXT_DERIVATION": "OPEN",
           "WITNESS_LINKAGE": "UNRESOLVED", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "DISCOVERABLE",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 1, "archive_hit": False, "crosswalk": False,
           "catalog_match": True, "edition_inspected": False, "etext_verified": False,
           "witnesses": 0, "rights_granted": "DISCOVERABLE", "date_exact": False, "echo": False},
          note="Muktabodha file has editorial history but unclear transcription basis → derivation open"),

    _case("nat-034", "MUKTABODHA",
          {"WORK_IDENTITY": "EXTERNAL_CANDIDATE_FOUND", "AUTHOR_IDENTITY": "UNKNOWN",
           "EDITION_IDENTITY": "DISCOVERED", "ETEXT_DERIVATION": "PROBABLE_BASIS",
           "WITNESS_LINKAGE": "UNRESOLVED", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "DISCOVERABLE",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 1, "archive_hit": True, "crosswalk": False,
           "catalog_match": False, "edition_inspected": False, "etext_verified": False,
           "witnesses": 0, "rights_granted": "DISCOVERABLE", "date_exact": False, "echo": False},
          note="Muktabodha scan lacks a clear derivation chain → keep PROBABLE_BASIS"),

    # ── K. Archive.org false / weak search hits ────────────────────────────────────────────────
    _case("nat-015", "ARCHIVE_FALSE_HIT",
          {"WORK_IDENTITY": "EXTERNAL_CANDIDATE_FOUND", "AUTHOR_IDENTITY": "UNKNOWN",
           "EDITION_IDENTITY": "DISCOVERED", "ETEXT_DERIVATION": "OPEN",
           "WITNESS_LINKAGE": "UNRESOLVED", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "UNKNOWN",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 1, "archive_hit": True, "crosswalk": False,
           "catalog_match": False, "edition_inspected": False, "etext_verified": False,
           "witnesses": 0, "rights_granted": "UNKNOWN", "date_exact": False, "echo": False},
          gates={"factory": False, "publication": False, "scholar": False},
          note="single loose archive.org search hit → work + edition stay weak; no gate opens"),

    _case("nat-016", "ARCHIVE_FALSE_HIT",
          {"WORK_IDENTITY": "EXTERNAL_CANDIDATE_FOUND", "AUTHOR_IDENTITY": "UNKNOWN",
           "EDITION_IDENTITY": "EXTERNAL_CANDIDATE_FOUND", "ETEXT_DERIVATION": "OPEN",
           "WITNESS_LINKAGE": "UNRESOLVED", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "UNKNOWN",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 1, "archive_hit": True, "crosswalk": False,
           "catalog_match": False, "edition_inspected": False, "etext_verified": False,
           "witnesses": 0, "rights_granted": "UNKNOWN", "date_exact": False, "echo": False},
          gates={"factory": False, "publication": False, "scholar": False},
          note="one archive.org hit must never be EDITION_VERIFIED or open publication"),

    _case("nat-050", "ARCHIVE_FALSE_HIT",
          {"WORK_IDENTITY": "EXTERNAL_CANDIDATE_FOUND", "AUTHOR_IDENTITY": "UNKNOWN",
           "EDITION_IDENTITY": "EXTERNAL_CANDIDATE_FOUND", "ETEXT_DERIVATION": "OPEN",
           "WITNESS_LINKAGE": "UNRESOLVED", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "UNKNOWN",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 1, "archive_hit": True, "crosswalk": False,
           "catalog_match": False, "edition_inspected": False, "etext_verified": False,
           "witnesses": 0, "rights_granted": "UNKNOWN", "date_exact": False, "echo": False},
          gates={"factory": False, "publication": False, "scholar": False},
          note="single archive hit ≠ edition corroboration; no gate opens"),

    # ── L. NMM catalogue uncertainty ───────────────────────────────────────────────────────────
    _case("nat-017", "NMM_UNCERTAINTY",
          {"WORK_IDENTITY": "CATALOG_MATCHED", "AUTHOR_IDENTITY": "UNKNOWN",
           "EDITION_IDENTITY": "DISCOVERED", "ETEXT_DERIVATION": "OPEN",
           "WITNESS_LINKAGE": "UNRESOLVED", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "UNKNOWN",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 1, "archive_hit": False, "crosswalk": False,
           "catalog_match": True, "edition_inspected": False, "etext_verified": False,
           "witnesses": 0, "rights_granted": "UNKNOWN", "date_exact": False, "echo": False},
          note="NMM lists the work but flags authorship uncertain → author stays open"),

    # ── M. NGMCP manuscript matches ────────────────────────────────────────────────────────────
    _case("nat-018", "NGMCP_MANUSCRIPT",
          {"WORK_IDENTITY": "EXTERNAL_CANDIDATE_FOUND", "AUTHOR_IDENTITY": "UNKNOWN",
           "EDITION_IDENTITY": "DISCOVERED", "ETEXT_DERIVATION": "OPEN",
           "WITNESS_LINKAGE": "SINGLE_WITNESS", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "UNKNOWN",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 1, "archive_hit": False, "crosswalk": False,
           "catalog_match": False, "edition_inspected": False, "etext_verified": False,
           "witnesses": 1, "rights_granted": "UNKNOWN", "date_exact": False, "echo": False},
          note="one NGMCP manuscript record → SINGLE_WITNESS, never MULTI_WITNESS"),

    _case("nat-041", "NGMCP_MANUSCRIPT",
          {"WORK_IDENTITY": "EXTERNAL_CANDIDATE_FOUND", "AUTHOR_IDENTITY": "UNKNOWN",
           "EDITION_IDENTITY": "DISCOVERED", "ETEXT_DERIVATION": "OPEN",
           "WITNESS_LINKAGE": "SINGLE_WITNESS", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "UNKNOWN",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 1, "archive_hit": False, "crosswalk": False,
           "catalog_match": False, "edition_inspected": False, "etext_verified": False,
           "witnesses": 1, "rights_granted": "UNKNOWN", "date_exact": False, "echo": False},
          gates={"factory": False, "publication": False},
          note="one NGMCP manuscript → SINGLE_WITNESS, never MULTI_WITNESS; no gate opens"),

    # ── N. catalogues echoing one upstream record (SOURCE_ECHO) ────────────────────────────────
    _case("nat-019", "SOURCE_ECHO",
          {"WORK_IDENTITY": "MULTI_SOURCE_MATCHED", "AUTHOR_IDENTITY": "MULTI_SOURCE_CONFIRMED",
           "EDITION_IDENTITY": "EDITION_VERIFIED", "ETEXT_DERIVATION": "TRANSCRIPTION_VERIFIED",
           "WITNESS_LINKAGE": "MULTI_WITNESS", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "OPEN_LICENSE",
           "SOURCE_INDEPENDENCE": "MULTI_SOURCE"},
          {"independent_sources": 1, "archive_hit": False, "crosswalk": False,
           "catalog_match": True, "edition_inspected": False, "etext_verified": True,
           "witnesses": 2, "rights_granted": "OPEN_LICENSE", "date_exact": False, "echo": True},
          expect_promotion=True,
          note="FALSE PROMOTION: Google Books + WorldCat + LoC all copy one LoC MARC → MULTI_SOURCE_MATCHED is a false promotion"),

    _case("nat-020", "SOURCE_ECHO",
          {"WORK_IDENTITY": "MULTI_SOURCE_MATCHED", "AUTHOR_IDENTITY": "MULTI_SOURCE_CONFIRMED",
           "EDITION_IDENTITY": "COPY_INSPECTED", "ETEXT_DERIVATION": "TRANSCRIPTION_VERIFIED",
           "WITNESS_LINKAGE": "MULTI_WITNESS", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "OPEN_LICENSE",
           "SOURCE_INDEPENDENCE": "MULTI_SOURCE"},
          {"independent_sources": 3, "archive_hit": False, "crosswalk": False,
           "catalog_match": True, "edition_inspected": True, "etext_verified": True,
           "witnesses": 2, "rights_granted": "OPEN_LICENSE", "date_exact": False, "echo": False},
          note="truly independent sources agree → MULTI_SOURCE + MULTI_WITNESS is honest"),

    _case("nat-042", "SOURCE_ECHO",
          {"WORK_IDENTITY": "MULTI_SOURCE_MATCHED", "AUTHOR_IDENTITY": "MULTI_SOURCE_CONFIRMED",
           "EDITION_IDENTITY": "EDITION_VERIFIED", "ETEXT_DERIVATION": "TRANSCRIPTION_VERIFIED",
           "WITNESS_LINKAGE": "MULTI_WITNESS", "DATE_PRECISION": "c.995", "RIGHTS": "OPEN_LICENSE",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 1, "archive_hit": False, "crosswalk": False,
           "catalog_match": True, "edition_inspected": False, "etext_verified": True,
           "witnesses": 2, "rights_granted": "OPEN_LICENSE", "date_exact": False, "echo": True},
          expect_promotion=True,
          note="FALSE PROMOTION: WorldCat + Google + Amazon ingest the same NMM record → not independent corroboration"),

    _case("nat-043", "SOURCE_ECHO",
          {"WORK_IDENTITY": "CATALOG_MATCHED", "AUTHOR_IDENTITY": "CATALOG_SUPPORTED",
           "EDITION_IDENTITY": "CATALOG_MATCHED", "ETEXT_DERIVATION": "OPEN",
           "WITNESS_LINKAGE": "UNRESOLVED", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "DISCOVERABLE",
           "SOURCE_INDEPENDENCE": "MULTI_SOURCE"},
          {"independent_sources": 1, "archive_hit": False, "crosswalk": False,
           "catalog_match": True, "edition_inspected": False, "etext_verified": False,
           "witnesses": 0, "rights_granted": "DISCOVERABLE", "date_exact": False, "echo": True},
          gates={"factory": False, "publication": False},
          expect_promotion=True,
          note="FALSE PROMOTION: two catalogues quoting the same edition preface are not two independent sources"),

    _case("nat-044", "MULTI_SOURCE_HONEST",
          {"WORK_IDENTITY": "MULTI_SOURCE_MATCHED", "AUTHOR_IDENTITY": "MULTI_SOURCE_CONFIRMED",
           "EDITION_IDENTITY": "EDITION_VERIFIED", "ETEXT_DERIVATION": "TRANSCRIPTION_VERIFIED",
           "WITNESS_LINKAGE": "MULTI_WITNESS", "DATE_PRECISION": "c.995", "RIGHTS": "OPEN_LICENSE",
           "SOURCE_INDEPENDENCE": "MULTI_SOURCE"},
          {"independent_sources": 3, "archive_hit": False, "crosswalk": False,
           "catalog_match": True, "edition_inspected": True, "etext_verified": True,
           "witnesses": 3, "rights_granted": "OPEN_LICENSE", "date_exact": True, "echo": False},
          gates={"factory": True, "publication": True, "scholar": True},
          note="LoC + NMM + GRETIL edition statement independently agree; edition inspected → honest MULTI_SOURCE"),

    # ── O. wrong witness links ──────────────────────────────────────────────────────────────────
    _case("nat-021", "WRONG_WITNESS_LINK",
          {"WORK_IDENTITY": "CATALOG_MATCHED", "AUTHOR_IDENTITY": "CATALOG_SUPPORTED",
           "EDITION_IDENTITY": "CATALOG_MATCHED", "ETEXT_DERIVATION": "OPEN",
           "WITNESS_LINKAGE": "MULTI_WITNESS", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "DISCOVERABLE",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 1, "archive_hit": False, "crosswalk": False,
           "catalog_match": True, "edition_inspected": False, "etext_verified": False,
           "witnesses": 1, "rights_granted": "DISCOVERABLE", "date_exact": False, "echo": False},
          expect_promotion=True,
          note="FALSE PROMOTION: witness links point to a different recension; only one real witness confirmed → MULTI_WITNESS unsupported"),

    _case("nat-040", "WRONG_WITNESS_LINK",
          {"WORK_IDENTITY": "CATALOG_MATCHED", "AUTHOR_IDENTITY": "CATALOG_SUPPORTED",
           "EDITION_IDENTITY": "CATALOG_MATCHED", "ETEXT_DERIVATION": "OPEN",
           "WITNESS_LINKAGE": "MULTI_WITNESS", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "DISCOVERABLE",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 1, "archive_hit": False, "crosswalk": False,
           "catalog_match": True, "edition_inspected": False, "etext_verified": False,
           "witnesses": 1, "rights_granted": "DISCOVERABLE", "date_exact": False, "echo": False},
          expect_promotion=True,
          note="FALSE PROMOTION: folios mis-linked to a different text; one real witness → MULTI_WITNESS unsupported"),

    # ── P. rights uncertainty ──────────────────────────────────────────────────────────────────
    _case("nat-022", "RIGHTS_UNCERTAINTY",
          {"WORK_IDENTITY": "MULTI_SOURCE_MATCHED", "AUTHOR_IDENTITY": "MULTI_SOURCE_CONFIRMED",
           "EDITION_IDENTITY": "EDITION_VERIFIED", "ETEXT_DERIVATION": "TRANSCRIPTION_VERIFIED",
           "WITNESS_LINKAGE": "MULTI_WITNESS", "DATE_PRECISION": "c.995", "RIGHTS": "UNKNOWN",
           "SOURCE_INDEPENDENCE": "MULTI_SOURCE"},
          {"independent_sources": 3, "archive_hit": False, "crosswalk": False,
           "catalog_match": True, "edition_inspected": True, "etext_verified": True,
           "witnesses": 3, "rights_granted": "UNKNOWN", "date_exact": True, "echo": False},
          gates={"factory": False, "publication": False},
          note="rights unknown → publication + factory stay closed even though identity is solid"),

    _case("nat-023", "RIGHTS_DISCOVERABLE_ONLY",
          {"WORK_IDENTITY": "MULTI_SOURCE_MATCHED", "AUTHOR_IDENTITY": "MULTI_SOURCE_CONFIRMED",
           "EDITION_IDENTITY": "EDITION_VERIFIED", "ETEXT_DERIVATION": "TRANSCRIPTION_VERIFIED",
           "WITNESS_LINKAGE": "MULTI_WITNESS", "DATE_PRECISION": "c.995", "RIGHTS": "DISCOVERABLE",
           "SOURCE_INDEPENDENCE": "MULTI_SOURCE"},
          {"independent_sources": 3, "archive_hit": False, "crosswalk": False,
           "catalog_match": True, "edition_inspected": True, "etext_verified": True,
           "witnesses": 3, "rights_granted": "DISCOVERABLE", "date_exact": True, "echo": False},
          gates={"factory": False, "publication": False},
          note="DISCOVERABLE (searchable) is not PROCESSING_ALLOWED → publication + factory closed"),

    _case("nat-038", "RIGHTS_DISCOVERABLE_ONLY",
          {"WORK_IDENTITY": "MULTI_SOURCE_MATCHED", "AUTHOR_IDENTITY": "MULTI_SOURCE_CONFIRMED",
           "EDITION_IDENTITY": "EDITION_VERIFIED", "ETEXT_DERIVATION": "TRANSCRIPTION_VERIFIED",
           "WITNESS_LINKAGE": "MULTI_WITNESS", "DATE_PRECISION": "c.995", "RIGHTS": "REDISTRIBUTABLE",
           "SOURCE_INDEPENDENCE": "MULTI_SOURCE"},
          {"independent_sources": 3, "archive_hit": False, "crosswalk": False,
           "catalog_match": True, "edition_inspected": True, "etext_verified": True,
           "witnesses": 3, "rights_granted": "DISCOVERABLE", "date_exact": True, "echo": False},
          gates={"factory": False, "publication": False},
          expect_promotion=True,
          note="FALSE PROMOTION: REDISTRIBUTABLE claimed when the source grants only DISCOVERABLE"),

    _case("nat-039", "RIGHTS_PROCESSING",
          {"WORK_IDENTITY": "MULTI_SOURCE_MATCHED", "AUTHOR_IDENTITY": "MULTI_SOURCE_CONFIRMED",
           "EDITION_IDENTITY": "EDITION_VERIFIED", "ETEXT_DERIVATION": "TRANSCRIPTION_VERIFIED",
           "WITNESS_LINKAGE": "MULTI_WITNESS", "DATE_PRECISION": "c.995", "RIGHTS": "PROCESSING_ALLOWED",
           "SOURCE_INDEPENDENCE": "MULTI_SOURCE"},
          {"independent_sources": 3, "archive_hit": False, "crosswalk": False,
           "catalog_match": True, "edition_inspected": True, "etext_verified": True,
           "witnesses": 3, "rights_granted": "PROCESSING_ALLOWED", "date_exact": True, "echo": False},
          gates={"factory": True, "publication": False},
          note="PROCESSING_ALLOWED → factory yes, publication no"),

    # ── Q. internal crosswalk (the regression the review found) ────────────────────────────────
    _case("nat-024", "INTERNAL_CROSSWALK",
          {"WORK_IDENTITY": "INTERNAL_IDENTITY_BOUND", "AUTHOR_IDENTITY": "UNKNOWN",
           "EDITION_IDENTITY": "DISCOVERED", "ETEXT_DERIVATION": "OPEN",
           "WITNESS_LINKAGE": "UNRESOLVED", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "UNKNOWN",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 0, "archive_hit": False, "crosswalk": True,
           "catalog_match": False, "edition_inspected": False, "etext_verified": False,
           "witnesses": 0, "rights_granted": "UNKNOWN", "date_exact": False, "echo": False},
          gates={"factory": False, "publication": False, "scholar": False},
          note="internal crosswalk only → WORK_IDENTITY=INTERNAL_IDENTITY_BOUND, no gate opens"),

    _case("nat-025", "INTERNAL_CROSSWALK",
          {"WORK_IDENTITY": "MULTI_SOURCE_MATCHED", "AUTHOR_IDENTITY": "CATALOG_SUPPORTED",
           "EDITION_IDENTITY": "CATALOG_MATCHED", "ETEXT_DERIVATION": "OPEN",
           "WITNESS_LINKAGE": "UNRESOLVED", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "DISCOVERABLE",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 1, "archive_hit": False, "crosswalk": True,
           "catalog_match": True, "edition_inspected": False, "etext_verified": False,
           "witnesses": 0, "rights_granted": "DISCOVERABLE", "date_exact": False, "echo": False},
          expect_promotion=True,
          note="REGRESSION: internal crosswalk + one catalogue echo labeled MULTI_SOURCE_MATCHED is a false promotion"),

    _case("nat-048", "INTERNAL_CROSSWALK",
          {"WORK_IDENTITY": "INTERNAL_IDENTITY_BOUND", "AUTHOR_IDENTITY": "CATALOG_SUPPORTED",
           "EDITION_IDENTITY": "CATALOG_MATCHED", "ETEXT_DERIVATION": "OPEN",
           "WITNESS_LINKAGE": "UNRESOLVED", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "DISCOVERABLE",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 1, "archive_hit": False, "crosswalk": True,
           "catalog_match": True, "edition_inspected": False, "etext_verified": False,
           "witnesses": 0, "rights_granted": "DISCOVERABLE", "date_exact": False, "echo": False},
          gates={"factory": False, "publication": False},
          note="internal crosswalk + one catalogue → WORK_IDENTITY stays INTERNAL_IDENTITY_BOUND; factory must not open"),

    _case("nat-049", "INTERNAL_CROSSWALK",
          {"WORK_IDENTITY": "INTERNAL_IDENTITY_BOUND", "AUTHOR_IDENTITY": "UNKNOWN",
           "EDITION_IDENTITY": "DISCOVERED", "ETEXT_DERIVATION": "OPEN",
           "WITNESS_LINKAGE": "UNRESOLVED", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "UNKNOWN",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 0, "archive_hit": False, "crosswalk": True,
           "catalog_match": False, "edition_inspected": False, "etext_verified": False,
           "witnesses": 0, "rights_granted": "UNKNOWN", "date_exact": False, "echo": False},
          gates={"factory": False, "publication": False, "scholar": False},
          note="pure internal crosswalk, no external evidence → every gate closed (honest)"),

    # ── R. a weak candidate must remain OPEN, not rejected as nonexistent ──────────────────────
    _case("nat-026", "ABSENCE_NOT_NONEXISTENCE",
          {"WORK_IDENTITY": "DISCOVERED", "AUTHOR_IDENTITY": "UNKNOWN",
           "EDITION_IDENTITY": "DISCOVERED", "ETEXT_DERIVATION": "OPEN",
           "WITNESS_LINKAGE": "UNRESOLVED", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "UNKNOWN",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 0, "archive_hit": False, "crosswalk": False,
           "catalog_match": False, "edition_inspected": False, "etext_verified": False,
           "witnesses": 0, "rights_granted": "UNKNOWN", "date_exact": False, "echo": False},
          gates={"factory": False, "publication": False, "scholar": False},
          note="not found in queried catalogues ≠ no manuscript exists (ABSENCE_AS_NONEXISTENCE forbidden)"),

    # ── S. more homonymy / alias / author identity ─────────────────────────────────────────────
    _case("nat-027", "HOMONYMOUS_TITLE",
          {"WORK_IDENTITY": "EXTERNAL_CANDIDATE_FOUND", "AUTHOR_IDENTITY": "UNKNOWN",
           "EDITION_IDENTITY": "DISCOVERED", "ETEXT_DERIVATION": "OPEN",
           "WITNESS_LINKAGE": "UNRESOLVED", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "UNKNOWN",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 1, "archive_hit": True, "crosswalk": False,
           "catalog_match": False, "edition_inspected": False, "etext_verified": False,
           "witnesses": 0, "rights_granted": "UNKNOWN", "date_exact": False, "echo": False},
          gates={"factory": False, "publication": False, "scholar": False},
          note="title shared by a śaiva text and a purāṇa; a single weak hit cannot choose"),

    _case("nat-028", "SAME_TITLE_DIFF_AUTHOR",
          {"WORK_IDENTITY": "INTERNAL_IDENTITY_BOUND", "AUTHOR_IDENTITY": "UNKNOWN",
           "EDITION_IDENTITY": "DISCOVERED", "ETEXT_DERIVATION": "OPEN",
           "WITNESS_LINKAGE": "UNRESOLVED", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "UNKNOWN",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 0, "archive_hit": False, "crosswalk": True,
           "catalog_match": False, "edition_inspected": False, "etext_verified": False,
           "witnesses": 0, "rights_granted": "UNKNOWN", "date_exact": False, "echo": False},
          note="internal map only; cannot confirm which author's work → stay open"),

    _case("nat-029", "DISPUTED_AUTHORSHIP",
          {"WORK_IDENTITY": "CATALOG_MATCHED", "AUTHOR_IDENTITY": "SELF_ATTRIBUTED",
           "EDITION_IDENTITY": "CATALOG_MATCHED", "ETEXT_DERIVATION": "OPEN",
           "WITNESS_LINKAGE": "UNRESOLVED", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "DISCOVERABLE",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 1, "archive_hit": False, "crosswalk": False,
           "catalog_match": True, "edition_inspected": False, "etext_verified": False,
           "witnesses": 0, "rights_granted": "DISCOVERABLE", "date_exact": False, "echo": False},
          note="only the text self-attributes authorship; scholars undecided → author stays open"),

    _case("nat-030", "DISPUTED_AUTHORSHIP",
          {"WORK_IDENTITY": "MULTI_SOURCE_MATCHED", "AUTHOR_IDENTITY": "CATALOG_SUPPORTED",
           "EDITION_IDENTITY": "EDITION_VERIFIED", "ETEXT_DERIVATION": "TRANSCRIPTION_VERIFIED",
           "WITNESS_LINKAGE": "MULTI_WITNESS", "DATE_PRECISION": "c.900", "RIGHTS": "OPEN_LICENSE",
           "SOURCE_INDEPENDENCE": "MULTI_SOURCE"},
          {"independent_sources": 2, "archive_hit": False, "crosswalk": False,
           "catalog_match": True, "edition_inspected": True, "etext_verified": True,
           "witnesses": 3, "rights_granted": "OPEN_LICENSE", "date_exact": True, "echo": False},
          note="identity/edition solid but attribution disputed; one catalogue supports it → CATALOG_SUPPORTED is honest"),

    # ── T. edition vs e-text / derivation (extra) ──────────────────────────────────────────────
    _case("nat-036", "APPROXIMATE_DATE",
          {"WORK_IDENTITY": "CATALOG_MATCHED", "AUTHOR_IDENTITY": "CATALOG_SUPPORTED",
           "EDITION_IDENTITY": "CATALOG_MATCHED", "ETEXT_DERIVATION": "OPEN",
           "WITNESS_LINKAGE": "UNRESOLVED", "DATE_PRECISION": "mid-8th c.", "RIGHTS": "DISCOVERABLE",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 1, "archive_hit": False, "crosswalk": False,
           "catalog_match": True, "edition_inspected": False, "etext_verified": False,
           "witnesses": 0, "rights_granted": "DISCOVERABLE", "date_exact": False, "echo": False},
          note="scholars place it mid-8th c.; a range is honest, a fixed year would be inflation"),

    _case("nat-037", "DATE_PRECISION_INFLATION",
          {"WORK_IDENTITY": "MULTI_SOURCE_MATCHED", "AUTHOR_IDENTITY": "MULTI_SOURCE_CONFIRMED",
           "EDITION_IDENTITY": "EDITION_VERIFIED", "ETEXT_DERIVATION": "TRANSCRIPTION_VERIFIED",
           "WITNESS_LINKAGE": "MULTI_WITNESS", "DATE_PRECISION": "c.995 (exact from 10th–11th c.)",
           "RIGHTS": "OPEN_LICENSE", "SOURCE_INDEPENDENCE": "MULTI_SOURCE"},
          {"independent_sources": 3, "archive_hit": False, "crosswalk": False,
           "catalog_match": True, "edition_inspected": True, "etext_verified": True,
           "witnesses": 3, "rights_granted": "OPEN_LICENSE", "date_exact": False, "echo": False},
          expect_promotion=True,
          note="DATE_PRECISION_INFLATION: century-range rendered as an exact year is a false promotion"),

    # ── V. rights (extra) ──────────────────────────────────────────────────────────────────────
    _case("nat-046", "NO_RIGHTS_NO_FACTORY",
          {"WORK_IDENTITY": "MULTI_SOURCE_MATCHED", "AUTHOR_IDENTITY": "MULTI_SOURCE_CONFIRMED",
           "EDITION_IDENTITY": "EDITION_VERIFIED", "ETEXT_DERIVATION": "TRANSCRIPTION_VERIFIED",
           "WITNESS_LINKAGE": "MULTI_WITNESS", "DATE_PRECISION": "c.995", "RIGHTS": "UNKNOWN",
           "SOURCE_INDEPENDENCE": "MULTI_SOURCE"},
          {"independent_sources": 3, "archive_hit": False, "crosswalk": False,
           "catalog_match": True, "edition_inspected": True, "etext_verified": True,
           "witnesses": 3, "rights_granted": "UNKNOWN", "date_exact": True, "echo": False},
          gates={"factory": False, "publication": False},
          note="rights UNKNOWN → no processing gate opens even though identity is fully verified"),

    # ── W. witness linkage (extra) ─────────────────────────────────────────────────────────────
    _case("nat-018b", "NGMCP_MANUSCRIPT",
          {"WORK_IDENTITY": "EXTERNAL_CANDIDATE_FOUND", "AUTHOR_IDENTITY": "UNKNOWN",
           "EDITION_IDENTITY": "DISCOVERED", "ETEXT_DERIVATION": "OPEN",
           "WITNESS_LINKAGE": "SINGLE_WITNESS", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "UNKNOWN",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 1, "archive_hit": False, "crosswalk": False,
           "catalog_match": False, "edition_inspected": False, "etext_verified": False,
           "witnesses": 1, "rights_granted": "UNKNOWN", "date_exact": False, "echo": False},
          note="single witness record → SINGLE_WITNESS honest"),

    # ── X. gates / factory eligibility ─────────────────────────────────────────────────────────
    _case("nat-045", "WEAK_EDITION_NO_FACTORY",
          {"WORK_IDENTITY": "MULTI_SOURCE_MATCHED", "AUTHOR_IDENTITY": "MULTI_SOURCE_CONFIRMED",
           "EDITION_IDENTITY": "EXTERNAL_CANDIDATE_FOUND", "ETEXT_DERIVATION": "PROBABLE_BASIS",
           "WITNESS_LINKAGE": "UNRESOLVED", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "PROCESSING_ALLOWED",
           "SOURCE_INDEPENDENCE": "MULTI_SOURCE"},
          {"independent_sources": 2, "archive_hit": True, "crosswalk": False,
           "catalog_match": False, "edition_inspected": False, "etext_verified": False,
           "witnesses": 0, "rights_granted": "PROCESSING_ALLOWED", "date_exact": False, "echo": False},
          gates={"factory": False, "publication": False},
          note="identity strong but edition only a weak candidate → factory must NOT open"),

    _case("nat-047", "DISCOVERED_NO_GATE",
          {"WORK_IDENTITY": "DISCOVERED", "AUTHOR_IDENTITY": "UNKNOWN",
           "EDITION_IDENTITY": "DISCOVERED", "ETEXT_DERIVATION": "OPEN",
           "WITNESS_LINKAGE": "UNRESOLVED", "DATE_PRECISION": "UNKNOWN", "RIGHTS": "UNKNOWN",
           "SOURCE_INDEPENDENCE": "SINGLE_SOURCE"},
          {"independent_sources": 0, "archive_hit": False, "crosswalk": False,
           "catalog_match": False, "edition_inspected": False, "etext_verified": False,
           "witnesses": 0, "rights_granted": "UNKNOWN", "date_exact": False, "echo": False},
          gates={"factory": False, "publication": False, "scholar": False},
          note="a bare DISCOVERED record opens no gate"),
]
# fmt: on

# frozen provenance: hash of the whole set (must not drift silently)
import hashlib
import json

NATURAL_SET_HASH = hashlib.sha256(
    json.dumps([{k: c[k] for k in ("id", "category", "authority", "evidence", "expect_promotion")}
                for c in NATURAL_CASES], sort_keys=True).encode("utf-8")).hexdigest()


def get_cases():
    return [dict(c) for c in NATURAL_CASES]

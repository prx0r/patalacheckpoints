#!/usr/bin/env python3
"""production/curate_sanderson.py — curated spans from the Sanderson corpus (independent author).

Sanderson is the FIRST genuinely INDEPENDENT scholar (vs Ratié) in the corpus. These spans are
hand-selected from actual Sanderson text, verified via the normalized-verbatim matcher, and used
to seek corroboration / qualification / alternative reading against the existing propositions
and to license new ones (e.g. liberation = conviction of identity as Śiva).

Quotes are verbatim from the Sanderson extracted text. We preserve raw + normalized; we never
silently alter.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import Corpus, Publication, Witness, sha256_file, sha256_text
from extract import find_span, page_map, page_for_offset, Span, SourceAssertion  # noqa: F401
from core import Span, SourceAssertion

SANDERSON_DIR = os.path.join("data", "corpus", "sources", "sanderson")

SANDERSON_PAPERS = [
    # (filename, slug, title, year, venue)
    ("Saivism_and_the_Tantric_Traditions_Festschrift_fulltext.txt",
     "sanderson-saivism-tantric-traditions",
     "Saivism and the Tantric Traditions: Essays in Honour of Alexis Sanderson", 2000,
     "Gonda Indological Studies (Festschrift)"),
    ("saiva_exegesis_kashmir.txt",
     "sanderson-saiva-exegesis-kashmir",
     "The Saiva Exegesis of Kashmir", 2007,
     "Mélanges tantriques / Tantric Studies in Memory of Hélène Brunner"),
]


def curate(corpus: Corpus) -> None:
    """Add Sanderson publications + verified spans/assertions to the corpus."""
    for fname, slug, title, year, venue in SANDERSON_PAPERS:
        path = os.path.join(SANDERSON_DIR, fname)
        if not os.path.exists(path):
            continue
        pub = Publication(pub_id=f"pt:publication:{slug}", title=title,
                          author="pt:person:alexis-sanderson", author_name="Alexis Sanderson",
                          year=year, venue=venue, pub_type="ARTICLE")
        corpus.add_publication(pub)
        wit = Witness(witness_id=f"pt:witness:{slug}:file", pub_ref=pub.pub_id,
                      local_path=path, sha256=sha256_file(path), format="TXT",
                      extraction_status="EXTRACTED")
        corpus.add_witness(wit)
        with open(path, encoding="utf-8", errors="replace") as f:
            text = f.read()
        if "saivism-tantric-traditions" in slug:
            _festschrift_spans(corpus, pub, wit, text)
        else:
            _saiva_exegesis_spans(corpus, pub, wit, text)


def _festschrift_spans(corpus: Corpus, pub: Publication, wit: Witness, text: str) -> None:
    """Spans that occur in the Festschrift (Sanderson's own + Goodall's chapter)."""
    # liberation = conviction of identity as Śiva (TĀ 15.42-43b); no external cause.
    _add(corpus, pub, wit, text, "p389-liberation-identity-with-siva",
         "Conviction of one's identity with Siva is the means; no external cause bestows liberation",
         "ASSERTS", "pt:person:alexis-sanderson",
         "Sanderson states (quoting Tantrāloka 15.42-43b) that conviction of one's identity with Śiva is "
         "the means of liberation and that no external cause bestows it.",
         "INTERPRETIVE")
    # inner conviction (gnosis) is the real means of liberation.
    _add(corpus, pub, wit, text, "p389-inner-conviction-gnosis-liberation",
         "This inner conviction alone, a form of knowledge, is the real means of liberation",
         "ASSERTS", "pt:person:alexis-sanderson",
         "Sanderson reports that the inner conviction of identity with Śiva, a form of knowledge, "
         "is the real means of liberation.",
         "INTERPRETIVE")
    # Goodall et al.: an object alien to consciousness is unthinkable (attribution robustness).
    _add(corpus, pub, wit, text, "p-external-object-alien-unthinkable",
         "an object by nature alien to consciousness is simply unthinkable",
         "ASSERTS", "pt:person:goodall-et-al",
         "Goodall et al. report that Utpaladeva argued that an object by nature alien to consciousness "
         "is unthinkable, in his polemic against the existence of external objects (Vijñānavādin debate).",
         "INTERPRETIVE")
    # Fourth state: Light of Consciousness self-manifest (TĀ 10.269) — ALTERNATIVE_READING.
    _add(corpus, pub, wit, text, "p-loc-self-manifest-light-fourth-state",
         "the Light of Consciousness is self-manifest and we cannot speak of an immersion, except metaphorically",
         "ASSERTS", "pt:person:alexis-sanderson",
         "Sanderson (on Tantrāloka 10.269) reports that in the Fourth state the Light of Consciousness is "
         "self-manifest; a distinct claim about manifestation than 'manifestation-not-devoid-of-realization'.",
         "INTERPRETIVE")


def _saiva_exegesis_spans(corpus: Corpus, pub: Publication, wit: Witness, text: str) -> None:
    """Spans that occur in The Saiva Exegesis of Kashmir."""
    # liberation through insight alone is EXCEPTIONAL (qualifies the gnosis proposition) — PARTIAL.
    _add(corpus, pub, wit, text, "p-insight-liberation-exceptional",
         "liberation through insight alone and recognition as a Guru without passing through visible ceremonies",
         "ASSERTS", "pt:person:alexis-sanderson",
         "Sanderson notes that liberation through insight alone and recognition as a Guru without visible "
         "ceremonies 'were seen as exceptional' — qualifying the claim that gnosis alone is the means.",
         "INTERPRETIVE")
    # Śiva/Śakti = self-manifest light (prakāśa) + creative ideation (vimarśa).
    _add(corpus, pub, wit, text, "p-prakasa-and-vimarsa-unitary-source",
         "embodying the self-manifest light of reality (prakasah) and its innate power of creative ideation (vimarsah)",
         "ASSERTS", "pt:person:alexis-sanderson",
         "Sanderson reports (Cidvilāsastava) that Śiva and Śakti embody the self-manifest light of reality "
         "(prakāśa) and its innate power of creative ideation (vimarśa) as the unitary source.",
         "INTERPRETIVE")
    # Śivānanda: footstool of Śiva-and-Śakti = consciousness itself.
    _add(corpus, pub, wit, text, "p-sivananda-footstool-is-consciousness",
         "the footstool on which the [two] feet of Siva-and-Sakti rest, identifying it with consciousness itself",
         "ASSERTS", "pt:person:sivananda",
         "Sanderson reports that Śivānanda venerates the footstool of Śiva-and-Śakti, identifying it with "
         "consciousness itself, haloed by the radiance of the infinite worlds it spontaneously creates.",
         "INTERPRETIVE")


def _add(corpus, pub, wit, text, slug, quote, commitment, attributed, claim, assertion_type):
    loc = find_span(text, quote)
    if loc is None:
        # fail closed: don't silently add an unverifiable span
        corpus.provenance_failures.append(f"sanderson span not found: {slug}")
        return None
    raw_start, raw_end, raw_quote, prefix, suffix = loc
    pages = page_map(text)
    page = page_for_offset(pages, raw_start)
    s = Span(span_id=f"pt:span:{pub.pub_id}:{slug}", witness_ref=wit.witness_id,
             page=page, char_start=raw_start, char_end=raw_end,
             quote=raw_quote[:400], prefix=prefix[:200], suffix=suffix[:200],
             span_sha256=sha256_text(quote))
    sid = corpus.add_span(s)
    a = SourceAssertion(assertion_id=f"pt:assertion:{pub.pub_id}:{slug}", span_ref=sid,
                        attributed_to=attributed, claim=claim, commitment=commitment,
                        assertion_type=assertion_type,
                        extraction_origin="CURATED_HUMAN_READ", verification="SPAN_VERIFIED",
                        extraction_activity="pt:activity:scholar-extract:v0.2")
    return corpus.add_assertion(a)


if __name__ == "__main__":
    from build_corpus import build
    c = build()
    curate(c)
    print("Sanderson curation:")
    for a in c.assertions.values():
        if "sanderson" in a.assertion_id:
            sp = c.spans[a.span_ref]
            print(f"  {a.commitment:10} {a.assertion_id.split(':')[-1]:42} page={sp.page}")
    print("counts:", c.counts())
    errs = c.validate()
    print("validate:", "PASS" if not errs else errs)

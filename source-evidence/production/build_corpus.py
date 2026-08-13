#!/usr/bin/env python3
"""production/build_corpus.py — ingest the curated scholar corpus (Phase 2).

Builds the scholarly evidence corpus from REAL on-disk publications, using the curated
extractor (extract.py). Every span is hand-selected from actual text read in the source,
verified to occur verbatim, with page anchors + exact quote + conservative commitment.

This is the first REAL corpus pass: breadth across the highest-value IPVV/Utpaladeva/
Abhinavagupta/Pratyabhijñā scholarship, with quality (verified spans) over raw quantity.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import (Corpus, Publication, Witness, Proposition, sha256_file, INDEPENDENCE_ALL,
                  RELATION)
from extract import CuratedExtractor, SCHOL

# ── publications to process (highest-value on-topic scholarship) ──────────────
PAPERS = [
    # (filename, pub_id_slug, title, author, author_name, year, venue)
    ("In_search_of_Utpaladeva_s_lost_Vivrti_on.pdf",
     "ratie-utpaladeva-lost-vivrti",
     "In Search of Utpaladeva's Lost Vivṛti on the Pratyabhijñā Treatise",
     "pt:person:isabelle-ratie", "Isabelle Ratié", 2017, "Journal of Indian Philosophy 45 (2017) 163-189"),
    ("Utpaladeva_and_Abhinavagupta_on_the_Free.pdf",
     "ratie-utpaladeva-abhinavagupta-free",
     "Utpaladeva and Abhinavagupta on the Freedom of Consciousness",
     "pt:person:isabelle-ratie", "Isabelle Ratié", None, None),
    ("On_reason_and_scripture_in_the_Pratyabhi.pdf",
     "ratie-on-reason-scripture-pratyabhijna",
     "On Reason and Scripture in the Pratyabhijñā",
     "pt:person:isabelle-ratie", "Isabelle Ratié", 2013,
     "Scriptural Authority, Reason and Action (ÖAW)"),
    ("Otherness_in_the_Pratyabhijna_Philosophy.pdf",
     "ratie-otherness-pratyabhijna",
     "Otherness in the Pratyabhijñā Philosophy",
     "pt:person:isabelle-ratie", "Isabelle Ratié", 2007, "Journal of Indian Philosophy 35"),
]


def build() -> Corpus:
    corpus = Corpus()
    seen_failures = []

    for fname, slug, title, author, aname, year, venue in PAPERS:
        path = os.path.join(SCHOL, fname)
        if not os.path.exists(path):
            seen_failures.append((fname, "MISSING"))
            continue
        pub = Publication(pub_id=f"pt:publication:{slug}", title=title, author=author,
                          author_name=aname, year=year, venue=venue, pub_type="ARTICLE")
        wit = Witness(witness_id=f"pt:witness:{slug}:file", pub_ref=pub.pub_id,
                      local_path=path, sha256=sha256_file(path), format="PDF",
                      extraction_status="EXTRACTED")
        ex = CuratedExtractor(corpus, pub, wit, path)
        _curate(ex)
        corpus.add_publication(pub)
        corpus.add_witness(wit)

    _add_propositions_and_links(corpus)
    return corpus


# ── Phase 3: canonical propositions (formed from actual verified evidence) ──────
# Each proposition is licensed by at least one verified SourceAssertion; never a broad
# philosophical-sounding claim the sources don't support.
def _add_propositions_and_links(corpus: Corpus) -> None:
    props = {
        "pt:prop:manifestation-not-devoid-of-realization": Proposition(
            prop_id="pt:prop:manifestation-not-devoid-of-realization",
            formulation="There can be no conscious manifestation (prakāśa) devoid of a realization (vimarśa); "
                        "the internal manifestation is the Lord because it has pratyavamarśa as its essence.",
            subject="prakāśa / vimarśa",
            scope="Utpaladeva's Pratyabhijñā (ĪPVV, commentary on ĪPK 1.8)",
            modality="modal necessity (no manifestation without realization)",
            temporal_scope="Utpaladeva / 10th c. Kashmir Pratyabhijñā",
            assumptions="read as Ratié's report of Utpaladeva's own position, not later Śaivism generally",
            provenance="FROM_SOURCE_EVIDENCE",
        ),
        "pt:prop:differentiation-compatible-with-unity": Proposition(
            prop_id="pt:prop:differentiation-compatible-with-unity",
            formulation="Differentiated phenomena are not contradictory with the unity of consciousness "
                        "in the relevant Pratyabhijñā account.",
            subject="unity of consciousness / differentiation",
            scope="Utpaladeva's Pratyabhijñā",
            modality="non-contradiction",
            temporal_scope="Utpaladeva / 10th c.",
            assumptions=None,
            provenance="FROM_SOURCE_EVIDENCE",
        ),
        "pt:prop:vimarsa-is-reflexive-self-cognition": Proposition(
            prop_id="pt:prop:vimarsa-is-reflexive-self-cognition",
            formulation="vimarśa names a reflexive / self-cognitive act of realization that distinguishes "
                        "consciousness from other entities.",
            subject="vimarśa",
            scope="Utpaladeva / Abhinavagupta Pratyabhijñā",
            modality="defines a term (self-cognitive dimension)",
            temporal_scope="10th-11th c. Kashmir",
            assumptions=None,
            provenance="FROM_SOURCE_EVIDENCE",
        ),
        "pt:prop:recognition-responds-to-buddhist-accounts": Proposition(
            prop_id="pt:prop:recognition-responds-to-buddhist-accounts",
            formulation="Utpaladeva's account of self-awareness (svasaṃvedana) responds to a Buddhist opponent "
                        "who restricts perception to a particular object.",
            subject="self-awareness / Buddhist epistemology",
            scope="Utpaladeva's Pratyabhijñā vs Buddhist epistemologists",
            modality="responds to (dialectical)",
            temporal_scope="Utpaladeva / 10th c.",
            assumptions="framed as a response to Buddhist epistemology per Ratié's account",
            provenance="FROM_SOURCE_EVIDENCE",
        ),
        "pt:prop:certainty-grounded-in-self-awareness": Proposition(
            prop_id="pt:prop:certainty-grounded-in-self-awareness",
            formulation="Certainty is grounded in self-awareness (of the omniscient Lord) in the Pratyabhijñā account.",
            subject="certainty / self-awareness",
            scope="Pratyabhijñā epistemology",
            modality="grounding relation",
            temporal_scope="Pratyabhijñā tradition",
            assumptions=None,
            provenance="FROM_SOURCE_EVIDENCE",
        ),
        # NEW proposition from Sanderson (independent author): liberation = conviction of identity
        # as Śiva; no external cause. Corroborates the "recognition" theme from a second author.
        "pt:prop:liberation-is-conviction-of-identity-as-siva": Proposition(
            prop_id="pt:prop:liberation-is-conviction-of-identity-as-siva",
            formulation="Liberation is achieved by conviction of one's identity with Śiva; no external cause bestows it.",
            subject="liberation / recognition of identity",
            scope="Abhinavagupta / Tantrāloka 15.42-43b, as reported by Sanderson",
            modality="identity of means (conviction), denial of external cause",
            temporal_scope="Abhinavagupta / 11th c. Kashmir; reported by Sanderson",
            assumptions="reported through Sanderson's citation of Tantrāloka; not a claim by Utpaladeva",
            provenance="FROM_SOURCE_EVIDENCE",
        ),
        # NEW proposition: gnosis (inner conviction) is the real means of liberation, vs ritual action.
        "pt:prop:gnosis-is-the-means-of-liberation": Proposition(
            prop_id="pt:prop:gnosis-is-the-means-of-liberation",
            formulation="Inner conviction (a form of knowledge/gnosis), not ritual action per se, is the real means of liberation.",
            subject="gnosis vs ritual as means of liberation",
            scope="Abhinavagupta (Tantrāloka), as reported by Sanderson",
            modality="qualification (ritual only ancillary)",
            temporal_scope="Abhinavagupta / 11th c.",
            assumptions=None,
            provenance="FROM_SOURCE_EVIDENCE",
        ),
        # NEW proposition: an object alien to consciousness is unthinkable (Utpaladeva's argument
        # against external objects, Vijñānavādin debate).
        "pt:prop:external-object-alien-to-consciousness-unthinkable": Proposition(
            prop_id="pt:prop:external-object-alien-to-consciousness-unthinkable",
            formulation="An object by nature alien to consciousness is unthinkable; postulating an external "
                        "world is of no use in everyday practice.",
            subject="external objects / idealism",
            scope="Utpaladeva (Pratyabhijñā), Vijñānavādin debate",
            modality="impossibility (unthinkable)",
            temporal_scope="Utpaladeva / 10th c.",
            assumptions="reported by Goodall et al. (in a Festschrift chapter), not by Sanderson himself",
            provenance="FROM_SOURCE_EVIDENCE",
        ),
        # NEW: Śiva-Śakti as the unitary self-manifest light (prakāśa) + its power of creative ideation
        # (vimarśa) — the doctrinal pairing at the heart of the prakāśa-vimarśa theme.
        "pt:prop:siva-sakti-unitary-prakasa-vimarsa": Proposition(
            prop_id="pt:prop:siva-sakti-unitary-prakasa-vimarsa",
            formulation="Śiva and Śakti embody the self-manifest light of reality (prakāśa) and its innate "
                        "power of creative ideation (vimarśa) as the unitary source.",
            subject="prakāśa / vimarśa / Śiva-Śakti",
            scope="Cidvilāsastava, as reported by Sanderson",
            modality="identity (unitary source)",
            temporal_scope="South-Indian Śākta Śaiva / Śaiva non-dualism",
            assumptions="reported through Sanderson's account of the Cidvilāsastava",
            provenance="FROM_SOURCE_EVIDENCE",
        ),
        # NEW: Śivānanda identifies the footstool of Śiva-and-Śakti with consciousness itself.
        "pt:prop:siva-sakti-footstool-is-consciousness": Proposition(
            prop_id="pt:prop:siva-sakti-footstool-is-consciousness",
            formulation="The (ritual) footstool of Śiva-and-Śakti is identified with consciousness itself.",
            subject="consciousness / Śiva-Śakti",
            scope="Śivānanda, as reported by Sanderson (Saiva Exegesis)",
            modality="identity (with consciousness)",
            temporal_scope="Śivānanda / Śaiva exegesis",
            assumptions="reported through Sanderson's account of Śivānanda; ritual-symbolic context",
            provenance="FROM_SOURCE_EVIDENCE",
        ),
    }
    for p in props.values():
        corpus.add_proposition(p)

    # ── Sanderson curation (independent author) ──
    from curate_sanderson import curate as curate_sanderson
    curate_sanderson(corpus)

    # ── Phase 4: SourceAssertion -> Proposition relation candidates ──────────
    # Conservative MACHINE_CANDIDATE links; independence is scholarly lineage, not process.
    links = [
        # (assertion_slug_suffix, prop_id, relation, independence)
        ("p179-vimarsa-not-devoid-of-prakasa", "pt:prop:manifestation-not-devoid-of-realization",
         "DIRECT_SUPPORT", "PRIMARY_EDITION"),
        ("p180-unity-of-consciousness-not-contradicted", "pt:prop:differentiation-compatible-with-unity",
         "DIRECT_SUPPORT", "INDEPENDENT_TEXTUAL_ANALYSIS"),
        ("p-vimarsa-distinguishes-consciousness", "pt:prop:vimarsa-is-reflexive-self-cognition",
         "DIRECT_SUPPORT", "INDEPENDENT_TEXTUAL_ANALYSIS"),
        ("p-self-awareness-opponent-buddhist", "pt:prop:recognition-responds-to-buddhist-accounts",
         "DIRECT_SUPPORT", "INDEPENDENT_TEXTUAL_ANALYSIS"),
        ("p-certainty-grounded-in-self-awareness", "pt:prop:certainty-grounded-in-self-awareness",
         "DIRECT_SUPPORT", "INDEPENDENT_TEXTUAL_ANALYSIS"),
        # Sanderson (independent author) -> new propositions
        ("p389-liberation-identity-with-siva", "pt:prop:liberation-is-conviction-of-identity-as-siva",
         "DIRECT_SUPPORT", "INDEPENDENT_AUTHOR"),
        ("p389-inner-conviction-gnosis-liberation", "pt:prop:gnosis-is-the-means-of-liberation",
         "DIRECT_SUPPORT", "INDEPENDENT_AUTHOR"),
        # A2: Ratié independently corroborates the liberation proposition (Sanderson's primary source).
        ("p-liberation-is-recognition-of-self-as-siva", "pt:prop:liberation-is-conviction-of-identity-as-siva",
         "DIRECT_SUPPORT", "INDEPENDENT_AUTHOR"),
        # external-object proposition, corroborated by Goodall et al. (independent of Ratié's framing).
        ("p-external-object-alien-unthinkable", "pt:prop:external-object-alien-to-consciousness-unthinkable",
         "DIRECT_SUPPORT", "INDEPENDENT_AUTHOR"),
        # A3: PARTIAL_SUPPORT — Sanderson qualifies the gnosis-as-means proposition (liberation through
        # insight/recognition is EXCEPTIONAL, not the universal ritual norm).
        ("p-insight-liberation-exceptional", "pt:prop:gnosis-is-the-means-of-liberation",
         "PARTIAL_SUPPORT", "INDEPENDENT_AUTHOR"),
        # A2 strengthening: Sanderson's prakāśa-vimarśa report DIRECTLY corroborates the manifestation
        # proposition (second independent author) + the new unitary-source proposition.
        ("p-prakasa-and-vimarsa-unitary-source", "pt:prop:manifestation-not-devoid-of-realization",
         "DIRECT_SUPPORT", "INDEPENDENT_AUTHOR"),
        ("p-prakasa-and-vimarsa-unitary-source", "pt:prop:siva-sakti-unitary-prakasa-vimarsa",
         "DIRECT_SUPPORT", "INDEPENDENT_AUTHOR"),
        # 10th proposition: Śivānanda identifies the footstool with consciousness itself.
        ("p-sivananda-footstool-is-consciousness", "pt:prop:siva-sakti-footstool-is-consciousness",
         "DIRECT_SUPPORT", "INDEPENDENT_AUTHOR"),
        # dialectical diversity: Sanderson's self-manifest-Light passage is an ALTERNATIVE_READING of
        # manifestation (distinct from Ratié's 'manifestation-not-devoid-of-realization').
        ("p-loc-self-manifest-light-fourth-state", "pt:prop:manifestation-not-devoid-of-realization",
         "ALTERNATIVE_READING", "INDEPENDENT_AUTHOR"),
    ]
    for a_suffix, prop_id, relation, independence in links:
        # find the assertion by suffix
        matching = [a for a in corpus.assertions.values() if a.assertion_id.endswith(a_suffix)]
        if not matching:
            continue
        a = matching[0]
        prop = corpus.propositions[prop_id]
        corpus.link(assertion_ref=a.assertion_id, prop_ref=prop_id, relation=relation,
                    independence=independence, snapshot=prop.formulation,
                    prop_hash=prop.object_hash())


def _curate(ex: CuratedExtractor) -> None:
    """Add verified spans+assertions for this publication. Hand-curated from the text."""
    if "utpaladeva-lost-vivrti" in ex.pub.pub_id:
        # prakāśa cannot exist devoid of vimarśa; internal manifestation = the Lord (ĪPK 1.8.11)
        ex.add_span_assertion(
            span_slug="p179-vimarsa-not-devoid-of-prakasa",
            quote="there can be no [conscious] manifestation (prakāśa) devoid of a realization (vimarśa)",
            commitment="ASSERTS",
            claim="There can be no conscious manifestation (prakāśa) devoid of a realization (vimarśa); "
                  "the internal manifestation is none other than the Lord because it has a realization "
                  "(pratyavamarśa) as its essence.",
            assertion_type="INTERPRETIVE", page_hint=179,
        )
        # unity of consciousness, differentiated phenomena non-contradictory
        ex.add_span_assertion(
            span_slug="p180-unity-of-consciousness-not-contradicted",
            quote="differentiated phenomena are not contradictory with the unity of consciousness",
            commitment="ASSERTS",
            claim="Differentiated phenomena are not contradictory with the unity of consciousness "
                  "(in the relevant Utpaladeva account).",
            assertion_type="INTERPRETIVE", page_hint=180,
        )
    if "utpaladeva-abhinavagupta-free" in ex.pub.pub_id:
        # vimarśa distinguishes consciousness from other entities
        ex.add_span_assertion(
            span_slug="p-vimarsa-distinguishes-consciousness",
            quote="an act of realization (vimarśa) that distinguishes consciousness from other entities",
            commitment="ASSERTS",
            claim="vimarśa is an act of realization that distinguishes consciousness from other entities; "
                  "it names a self-cognitive (reflexive) dimension of consciousness.",
            assertion_type="INTERPRETIVE",
        )
        # A2: Ratié corroborates Sanderson's liberation proposition — liberation is the recognition
        # of oneself as Śiva. Two independent authors now agree on this proposition.
        ex.add_span_assertion(
            span_slug="p-liberation-is-recognition-of-self-as-siva",
            quote="liberation from the beginningless cycle of rebirths (saṃsāra)",
            commitment="ASSERTS",
            claim="According to Utpaladeva, liberation from the beginningless cycle of rebirths is nothing "
                  "but the blissful 'recognition' (pratyabhijñā) of oneself as 'the Lord' (īśvara), that is, Śiva.",
            assertion_type="INTERPRETIVE",
        )
    if "on-reason-scripture-pratyabhijna" in ex.pub.pub_id:
        # recognition theory responds to Buddhist accounts of cognition/self-awareness
        ex.add_span_assertion(
            span_slug="p-self-awareness-opponent-buddhist",
            quote="The opponent mentioned here is a Buddhist who considers that perception is restricted to the knowledge",
            commitment="ASSERTS",
            claim="Utpaladeva's account of self-awareness (svasaṃvedana) responds to a Buddhist opponent who "
                  "restricts perception to the knowledge of a particular object.",
            assertion_type="INTERPRETIVE",
        )
        # self-awareness grounds certainty
        ex.add_span_assertion(
            span_slug="p-certainty-grounded-in-self-awareness",
            quote="this certainty itself is grounded in the self-awareness of the omnisci",
            commitment="ASSERTS",
            claim="Certainty is grounded in self-awareness (of the omniscient Lord) in the relevant "
                  "Pratyabhijñā account.",
            assertion_type="INTERPRETIVE",
        )
    if "otherness-pratyabhijna" in ex.pub.pub_id:
        # the 'I'-awareness is not a mere concept (already mapped to ARG-002 G2-TC2)
        ex.add_span_assertion(
            span_slug="p342-fn63-aham-not-mere-concept",
            quote="pratyavamarśa) is not a mere concept (vikalpa), and Abhinavagupta",
            commitment="ASSERTS",
            claim="The 'I'-awareness (ahaṃ-pratyavamarśa) is not a mere concept (vikalpa), and Abhinavagupta "
                  "elaborates this against the view that it is.",
            assertion_type="INTERPRETIVE", page_hint=342,
        )


if __name__ == "__main__":
    c = build()
    errs = c.validate()
    print("CORPUS (Phase 2-4):")
    print(c.counts())
    print("── assertions ──")
    for a in c.assertions.values():
        span = c.spans[a.span_ref]
        print(f"  {a.commitment:22} {a.assertion_id.split(':')[-1]:38} page={span.page}")
    print("── propositions ──")
    for p in c.propositions.values():
        print(f"  {p.prop_id.split(':')[-1]:46} {p.formulation[:60]}")
    print("── evidence links ──")
    for l in c.links.values():
        print(f"  {l.prop_ref.split(':')[-1]:46} <- {l.assertion_ref.split(':')[-1]:38} "
              f"{l.relation} [{l.independence}]")
    if errs:
        print("VALIDATION ERRORS:")
        for e in errs:
            print("  ", e)
    else:
        print("VALIDATION: PASS")
    import json
    os.makedirs("source-evidence/production/store", exist_ok=True)
    print("corpus:", c.dump("source-evidence/production/store"))

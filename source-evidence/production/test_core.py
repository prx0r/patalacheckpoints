#!/usr/bin/env python3
"""test_core.py — prove the production object chain + integrity/dedup invariants (Phase 1)."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import (Corpus, Publication, Witness, Span, SourceAssertion, Proposition,
                  sha256_text, sha256_file, canonical_json)


def test_chain():
    c = Corpus()
    p = Publication(pub_id="pt:publication:ratie:Otherness", title="Otherness in the Pratyabhijñā",
                    author="pt:person:isabelle-ratie", author_name="Isabelle Ratié", year=2007,
                    venue="JIP 35")
    c.add_publication(p)
    # witness with real file hash
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    tmp.write(b"the grasping of the I is not a mere concept")
    tmp.close()
    w = Witness(witness_id="pt:witness:ratie:Otherness:file", pub_ref=p.pub_id,
                local_path=tmp.name, sha256=sha256_file(tmp.name), format="TXT",
                extraction_status="EXTRACTED")
    c.add_witness(w)
    s = Span(span_id="pt:span:ratie:Otherness:p342", witness_ref=w.witness_id, page=342,
             quote="the grasping of the I is not a mere concept",
             span_sha256=sha256_text("the grasping of the I is not a mere concept"))
    c.add_span(s)
    a = SourceAssertion(assertion_id="pt:assertion:ratie:Otherness:g2",
                        span_ref=s.span_id, attributed_to=p.author,
                        claim="The 'I'-awareness is not a mere concept",
                        commitment="ASSERTS", extraction_origin="MACHINE_MATCHED_HUMAN_SOURCE",
                        verification="SPAN_VERIFIED")
    c.add_assertion(a)
    prop = Proposition(prop_id="pt:prop:imaness-is-not-concept",
                       formulation="The I-awareness (ahaṃ-pratyavamarśa) is not a mere concept",
                       subject="ahaṃ-pratyavamarśa", modality="not a mere concept")
    c.add_proposition(prop)
    c.link(assertion_ref=a.assertion_id, prop_ref=prop.prop_id, relation="DIRECT_SUPPORT",
           independence="INDEPENDENT_AUTHOR", snapshot=prop.formulation, prop_hash=prop.object_hash())
    errs = c.validate()
    assert not errs, errs
    assert c.counts()["assertions"] == 1
    return c


def test_dedup_rerun():
    """Rerunning the same span/assertion must NOT create duplicates."""
    c = Corpus()
    p = Publication(pub_id="pt:publication:x", title="X", author="a", author_name="A")
    c.add_publication(p)
    w = Witness(witness_id="pt:witness:x:file", pub_ref=p.pub_id, local_path="/tmp/x",
                sha256="deadbeef", format="TXT")
    c.add_witness(w)
    for _ in range(3):  # rerun 3x
        s = Span(span_id="pt:span:x:p1", witness_ref=w.witness_id, quote="q", span_sha256=sha256_text("q"))
        sid = c.add_span(s)
        a = SourceAssertion(assertion_id=f"pt:assertion:x:run{_}", span_ref=sid,
                            attributed_to="a", claim="q", commitment="ASSERTS")
        c.add_assertion(a)
    assert c.counts()["spans"] == 1, "duplicate span created"
    assert c.counts()["assertions"] == 1, "duplicate assertion created"
    assert c.duplicates_rejected >= 2


def test_same_quote_two_papers_are_distinct():
    """Same quotation in two different publications = two distinct spans (different witnesses)."""
    c = Corpus()
    for i in (1, 2):
        p = Publication(pub_id=f"pt:publication:p{i}", title=f"P{i}", author=f"a{i}", author_name=f"A{i}")
        c.add_publication(p)
        w = Witness(witness_id=f"pt:witness:p{i}:file", pub_ref=p.pub_id, local_path=f"/tmp/p{i}",
                    sha256=f"h{i}", format="TXT")
        c.add_witness(w)
        s = Span(span_id=f"pt:span:p{i}:q", witness_ref=w.witness_id, quote="the shared quotation",
                 span_sha256=sha256_text("the shared quotation"))
        c.add_span(s)
    assert c.counts()["spans"] == 2, "same quote in two papers collapsed — wrong"


def test_independence_no_machine_leak():
    c = Corpus()
    p = Publication(pub_id="pt:publication:z", title="Z", author="a", author_name="A")
    c.add_publication(p)
    w = Witness(witness_id="pt:witness:z:file", pub_ref=p.pub_id, local_path="/tmp/z",
                sha256="h", format="TXT")
    c.add_witness(w)
    s = Span(span_id="pt:span:z:1", witness_ref=w.witness_id, quote="x", span_sha256=sha256_text("x"))
    c.add_span(s)
    a = SourceAssertion(assertion_id="pt:assertion:z:1", span_ref=s.span_id, attributed_to="a",
                        claim="x", commitment="ASSERTS")
    c.add_assertion(a)
    prop = Proposition(prop_id="pt:prop:z", formulation="x")
    c.add_proposition(prop)
    c.link(assertion_ref=a.assertion_id, prop_ref=prop.prop_id, relation="DIRECT_SUPPORT",
           independence="SAME_AUTHOR", snapshot="x", prop_hash=prop.object_hash())
    errs = c.validate()
    assert not errs, errs
    assert "MACHINE" not in c.links[list(c.links)[0]].independence


if __name__ == "__main__":
    test_chain()
    test_dedup_rerun()
    test_same_quote_two_papers_are_distinct()
    test_independence_no_machine_leak()
    print("CORE OK: object chain + dedup + independence vocabulary all pass")

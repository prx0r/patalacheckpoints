#!/usr/bin/env python3
"""source-evidence/annotation_bridge.py — the annotation bridge (devpath13 / reviewer priority #4).

Builds the INCEpTION/Recogito-style export/import loop for creating human gold cheaply.

    Pāṭala spans + machine labels
        ↓ EXPORT
    annotation project (neutral JSON / W3C Web Annotation / TEI-ish)
        ↓
    INCEpTION / Recogito / any annotation tool: scholars annotate
        ↓ IMPORT
    ReviewEvents + gold labels (pt:SourceAssertion / review records)

The point (per tool-integration2.md §4): do NOT build every annotation UI ourselves. Pāṭala exports
uncertain spans, scholars annotate in a mature tool, Pāṭala imports the annotations as review/gold.

Design laws:
  - An exported annotation carries the SAME resilient span selectors (TextQuoteSelector /
    TextPositionSelector / hash) as the canonical pt:Span, so imports re-resolve exactly.
  - Labels come from Pāṭala's own vocabularies (speaker, commitment, proposition, support,
    scope, uncertainty) — never invented for the annotation tool.
  - Imported annotations become ReviewEvents (evidence-bearing) or gold, NOT a mutation of the source.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone

# vocabularies (Pāṭala-native, reused for annotation labels)
SPEAKER_LABELS = ("author", "opponent", "commentator", "reconstructed", "unspecified")
COMMITMENT_LABELS = ("ASSERTS", "DENIES", "ATTRIBUTES", "REPORTS", "RECONSTRUCTS", "OPEN")
SUPPORT_LABELS = ("DIRECT_SUPPORT", "PARTIAL_SUPPORT", "CONTRADICTION", "BACKGROUND", "NON_EQUIVALENT")
SCOPE_LABELS = ("UNIVERSAL", "PER_ACT", "QUALIFIED", "UNKNOWN")
UNCERTAINTY_LABELS = ("UNRESOLVED", "NEEDS_REVIEW", "CONTESTED", "CONFIRMED")


def _sha256(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── EXPORT ────────────────────────────────────────────────────────────────────
def build_annotation_project(text: str, spans: list[dict], project_name: str,
                             layers=("speaker", "commitment", "proposition", "support", "scope",
                                     "uncertainty")) -> dict:
    """Export a text + its Pāṭala spans into a neutral annotation project.

    text:   the document text (e.g. a passage's L2/T1).
    spans:  [{span_id, char_start, char_end, quote, label, layer, ...}] — the machine pre-annotation.
    Returns a JSON annotation project (W3C Web Annotation compatible; consumable by INCEpTION/Recogito
    style tooling or a Pāṭala review UI).
    """
    annotations = []
    for s in spans:
        # resilient selectors (same shape as pt:Span)
        quote = s.get("quote") or text[s["char_start"]:s["char_end"]]
        selectors = {
            "@type": "oa:TextQuoteSelector",
            "exact": quote,
            "start": s["char_start"], "end": s["char_end"],
            "prefix": text[max(0, s["char_start"] - 30):s["char_start"]],
            "suffix": text[s["char_end"]:s["char_end"] + 30],
        }
        ann = {
            "@id": f"ann:{s['span_id']}",
            "@type": "oa:Annotation",
            "layer": s.get("layer", "speaker"),
            "target": {"@type": "oa:SpecificResource",
                       "selectors": [selectors,
                                     {"@type": "pt:HashSelector", "span_sha256": _sha256(quote)}]},
            "body": {
                "label": s.get("label"),
                "label_type": s.get("label_type"),
                "machine_proposed": s.get("machine_proposed", True),
                "uncertainty": s.get("uncertainty", "NEEDS_REVIEW"),
            },
            "source_ref": s.get("source_ref"),
        }
        annotations.append(ann)

    project = {
        "annotation_project_id": project_name,
        "exported_at": _now(),
        "format": "PĀTALA-ANNOTATION-PROJECT-v1",
        "compatible_with": ["INCEpTION (webanno/W3C)", "Recogito", "TEI WebAnnotation"],
        "text": text,
        "text_hash": _sha256(text),
        "layers": list(layers),
        "vocabularies": {
            "speaker": list(SPEAKER_LABELS), "commitment": list(COMMITMENT_LABELS),
            "support": list(SUPPORT_LABELS), "scope": list(SCOPE_LABELS),
            "uncertainty": list(UNCERTAINTY_LABELS),
        },
        "annotations": annotations,
        "annotation_count": len(annotations),
        "export_hash": _sha256({"text": text, "annotations": annotations}),
    }
    return project


# ── IMPORT ────────────────────────────────────────────────────────────────────
def import_annotations(project: dict, scholar_annotations: list[dict]) -> dict:
    """Import scholar annotations back as ReviewEvents + gold labels.

    scholar_annotations: [{span_id, label, label_type, layer, decision, note, annotator, reviewer_kind}]
    - decision: ACCEPT (confirms machine) / CORRECT (fixes label) / REJECT / ABSTAIN
    Returns {review_events, gold_updates, by_layer, rejected_span_ids}.
    """
    events = []
    gold = []
    by_layer = {}
    rejected = []
    for a in scholar_annotations:
        span_id = a["span_id"]
        decision = a.get("decision", "ABSTAIN")
        layer = a.get("layer", "speaker")
        by_layer.setdefault(layer, []).append(decision)
        # a ReviewEvent: an immutable record that does NOT mutate the source
        events.append({
            "event_id": f"rev-{_sha256({'span': span_id, 'annotator': a.get('annotator')})[:10]}",
            "@type": "pt:ReviewEvent",
            "target_span": span_id,
            "layer": layer,
            "decision": decision,
            "proposed_label": a.get("label"),
            "note": a.get("note", ""),
            "annotator": a.get("annotator"),
            "reviewer_kind": a.get("reviewer_kind", "SCHOLAR"),
            "asserted_at": _now(),
        })
        if decision == "CORRECT" and a.get("label"):
            # a gold-update proposal (does NOT mutate source; becomes gold only after adjudication)
            gold.append({
                "@type": "pt:GoldProposal",
                "target_span": span_id, "layer": layer,
                "label": a["label"], "label_type": a.get("label_type"),
                "source_ref": a.get("source_ref"), "proposed_by": a.get("annotator"),
                "adjudication": "PENDING",
            })
        if decision == "REJECT":
            rejected.append(span_id)

    return {
        "imported_at": _now(),
        "review_events": events,
        "gold_proposals": gold,
        "by_layer": by_layer,
        "rejected_span_ids": rejected,
        "import_hash": _sha256({"events": events, "gold": gold}),
        "design_law": "imports become ReviewEvents/gold, never a mutation of the source",
    }


# ── an example: build the VERTICAL-1 speaker/commitment annotation project ────
def build_vertical1_annotation_project() -> dict:
    text = (
        "The Buddhist, having lost the self, the cognition, the action, and the relation, falls back on "
        "one last notion: the determination (adhyavasāya) — the act by which, he thinks, the cognition is "
        "taken to establish an external thing. Abhinavagupta now cuts this last thread. The determination, "
        "he shows, cannot establish anything outside. The establishing is in the self; the experience, with "
        "the manifestation at its head, is the establishing, and it is self-luminous, not a thing that "
        "reaches a thing."
    )
    spans = [
        {"span_id": "S-ADHY", "char_start": text.find("the determination (adhyavasāya)"),
         "char_end": text.find("cannot establish anything outside") + len("cannot establish anything outside"),
         "layer": "speaker", "label": "opponent", "label_type": "SPEAKER",
         "machine_proposed": True, "uncertainty": "NEEDS_REVIEW",
         "source_ref": "pt:passage:ipvv:chunkM-jnanadhikara-reflexion-core.md"},
        {"span_id": "S-ESTAB", "char_start": text.find("The establishing is in the self"),
         "char_end": text.find("reaches a thing") + len("reaches a thing"),
         "layer": "speaker", "label": "author", "label_type": "SPEAKER",
         "machine_proposed": True, "uncertainty": "NEEDS_REVIEW",
         "source_ref": "pt:passage:ipvv:chunkM-jnanadhikara-reflexion-core.md"},
    ]
    return build_annotation_project(text, spans, "VERTICAL-1-SPEAKER-GOLD")


if __name__ == "__main__":
    proj = build_vertical1_annotation_project()
    print(f"annotation project: {proj['annotation_project_id']} | {proj['annotation_count']} spans | layers={proj['layers']}")
    for a in proj["annotations"]:
        print(f"  {a['@id']:14} [{a['layer']:8}] label={a['body']['label']:8} unc={a['body']['uncertainty']}")
    # simulate a scholar confirming + correcting
    scholar = [
        {"span_id": "S-ADHY", "layer": "speaker", "label": "opponent", "label_type": "SPEAKER",
         "decision": "ACCEPT", "annotator": "scholar-A", "source_ref": "pt:passage:ipvv:chunkM"},
        {"span_id": "S-ESTAB", "layer": "speaker", "label": "author", "label_type": "SPEAKER",
         "decision": "CORRECT", "note": "this is Abhinavagupta's own claim", "annotator": "scholar-A",
         "source_ref": "pt:passage:ipvv:chunkM"},
    ]
    imp = import_annotations(proj, scholar)
    print(f"import: {len(imp['review_events'])} ReviewEvents, {len(imp['gold_proposals'])} gold, by_layer={imp['by_layer']}")

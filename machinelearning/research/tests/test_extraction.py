#!/usr/bin/env python3
"""test_extraction.py — validation of the primitive extractor + extraction-eval (CP4 Build 4)."""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patala_ml.extractor import extract_propositions, ExtractionProposal
from patala_ml.eval_extraction import evaluate_extraction, _gold_node, _match, _jaccard
from patala_ml.gold002 import build_gold_002

failures = []
def check(name, cond, info=""):
    print(f"  {'✓' if cond else '✗'} {name}" + (f" — {info}" if info and not cond else ""))
    if not cond:
        failures.append(name)

print("== extractor: abstention on empty body ==")
props = extract_propositions("", "pt:passage:ipvv:chunkV2-O-saptamo-vimarsa.md")
check("abstains (emits NO_UNIQUE_ARGUMENT)", len(props) == 1 and props[0].abstain)

print("\n== extractor: grounded proposals from a real C1 body ==")
body = "> The powers need a support. The flashing runs through the ordered word-objects, seasoned with their order, but itself not ordered. Therefore the support is orderless."
props = extract_propositions(body, "pt:passage:ipvv:chunkV2-O-saptamo-vimarsa.md")
check("returns proposals", len(props) >= 2)
check("all grounded to passage", all(p.grounding.get("passage_id") == "pt:passage:ipvv:chunkV2-O-saptamo-vimarsa.md" for p in props))
check("proposals are ExtractionProposal", isinstance(props[0], ExtractionProposal))
check("roles are valid", all(p.kind in {"TEXTUAL_CLAIM","INTERPRETIVE_CLAIM","IMPLICIT_PREMISE","CONCLUSION","OBJECTION","QUALIFICATION"} for p in props))

print("\n== metric sanity: gold-vs-gold → perfect proposition recovery ==")
gold = build_gold_002()
preds = [{"proposition_id": n.get("proposition_id"), "text": n["text"], "kind": n["kind"],
          "explicitness": n.get("explicitness"), "grounding": {"passage_id": n["grounding"]["passage_id"]},
          "abstain": False} for n in gold["nodes"]]
r = evaluate_extraction(preds, gold)
check("gold-vs-gold proposition F1 = 1.0", r["lexical_proposition_overlap_f1"] == 1.0, str(r["lexical_proposition_overlap_f1"]))
check("gold-vs-gold grounding precision = 1.0", r["grounding_precision"] == 1.0, str(r["grounding_precision"]))

print("\n== baseline honesty: recovers SOME content but NO inference graph ==")
preds_b = [{"proposition_id": "X0", "text": "The powers need a support.",
            "kind": "TEXTUAL_CLAIM", "explicitness": "EXPLICIT",
            "grounding": {"passage_id": "pt:passage:ipvv:chunkV2-L-sastho-vimarsa-smrti-apohana.md"}, "abstain": False}]
r2 = evaluate_extraction(preds_b, build_gold_002())
check("baseline gets non-negative recall", r2["lexical_proposition_overlap_recall"] >= 0.0)
check("baseline recovers NO inference graph (honest)", r2["inference_recovery"] == 0.0)
check("inference-scheme F1 = 0 for no-inference baseline", r2["inference_scheme_macro_f1"] == 0.0)

print("\n== schema-variant normalization (gold.py vs gold002.py) ==")
# gold.py form: source_support with passage_ids (list)
n1 = {"id": "G-TC1", "proposition": "pratibha bears the order", "kind": "TEXTUAL_CLAIM",
      "explicitness": "EXPLICIT", "source_support": {"passage_ids": ["pt:passage:ipvv:chunkV2-O-saptamo-vimarsa.md"]}}
check("source_support.passage_ids list resolved", _gold_node(n1)["resolved_passage"] == "pt:passage:ipvv:chunkV2-O-saptamo-vimarsa.md")
# gold002.py form: grounding with passage_id (str)
n2 = {"proposition_id": "G2-OBJ", "text": "why not a construction?", "kind": "OBJECTION",
      "explicitness": "EXPLICIT", "grounding": {"passage_id": "pt:passage:ipvv:chunkV2-L-sastho-vimarsa-smrti-apohana.md"}}
check("grounding.passage_id str resolved", _gold_node(n2)["resolved_passage"] == "pt:passage:ipvv:chunkV2-L-sastho-vimarsa-smrti-apohana.md")

print(f"\n=== RESULT: {len(failures)} fail ===")
sys.exit(1 if failures else 0)

#!/usr/bin/env python3
"""build_review_packet.py — render the 5 ARG-GOLD fixtures as a SELF-CONTAINED reviewer packet.

NOTE (2026-08-12): this generator produces the LEGACY v1 packet whose review basis is the L2. The v1
basis is derivational-circular (the L2 was produced from the argument maps being reviewed) — the defect
MODEL-1 flagged. The canonical reviewer packet is now the PRIMARY-SANSKRIT grounded v2:
  benchmarks/v0/ARG-GOLD-REVIEW-PACKET-v2.md + review/ARG-GOLD-REVIEW-PACKET-v2.json,
validated by experiments/check_review_packet.py. Prefer v2 for any review.

The deliverable is a Markdown document an INDEPENDENT reader can judge WITHOUT knowing Pāṭala or
editing JSON. For each argument it shows: the SOURCE material, the PROPOSED argument, the FOUR review
questions, and an ACCEPT/REVISE/REJECT/ABSTAIN output template. Risk areas are called out explicitly.

Reviewers adjudicate scholarship; Pāṭala converts their judgments into infrastructure. The first
reviewer needs INDEPENDENCE from the builder + enough competence to falsify obvious reconstruction
errors — not necessarily a famous senior specialist.

Run: cd research && . .venv/bin/activate && python experiments/build_review_packet.py
"""
from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patala_ml.gold import build_gold_v0
from patala_ml.gold002 import build_gold_002
from patala_ml.gold003 import build_gold_003
from patala_ml.gold004 import build_gold_004
from patala_ml.gold005 import build_gold_005

IPVV = "/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv"
C1_DIR = os.path.join(IPVV, "c1", "read")
PILOT_DIR = os.path.join(IPVV, "pilot")

BUILDERS = {"ARG-GOLD-001": build_gold_v0, "ARG-GOLD-002": build_gold_002,
            "ARG-GOLD-003": build_gold_003, "ARG-GOLD-004": build_gold_004,
            "ARG-GOLD-005": build_gold_005}
SOURCES = {
    "ARG-GOLD-001": ("V2O-orderless-support", "pilot_V2O_L2_read.md"),
    "ARG-GOLD-002": ("V2L-nonconstructed-I", "pilot_V2L_L2_read.md"),
    "ARG-GOLD-003": ("V2O-orderless-support", "pilot_V2O_L2_read.md"),
    "ARG-GOLD-004": ("V2H-vimarsa-paravak", "pilot_V2H_L2_read.md"),
    "ARG-GOLD-005": ("V3I-difference-real", "pilot_V3I_L2_read.md"),
}
RISK = {
    "ARG-GOLD-003": "**Risk area — does the passage really license the regress reconstruction?** The infinite-regress warrant (if the support were ordered it would require a further support) is marked candidate_reconstruction; it may be our reconstruction, not the text's argument. Rule on it.",
    "ARG-GOLD-004": "**Risk area — is vimarśa-as-essence textual or reconstructed?** We treat the C1 as asserting that the essence of light is reflexive awareness. If you read it as only inferred, say so.",
    "ARG-GOLD-005": "**Risk area — is this genuine interpretive ambiguity, or local-vs-systematic scope?** We now type it as INTERPRETIVE_SCOPE (Reading A locally entailed; Reading B a contextually-supported extension). Rule on whether that is right.",
}
# Exact Sanskrit spans already resolved for a given gold (via the vertical machinery). Where absent,
# the primary text still needs to be supplied before SPECIALIST_REVIEWED promotion.
PRIMARY_TEXT = {
    "ARG-GOLD-001": ["pratibhā (L32:T114)", "tattatpadārthakramarūṣitā (L32:T115)",
                     "akramānantacidrūpaḥ (L33:T116)", "rūṣitā (L44:T181)"],
}
QUESTIONS = [
    "Is each proposition actually licensed by the supplied material (the source text / translation / context)?",
    "Are the reconstructed premises necessary and defensible — could another competent reader reconstruct differently?",
    "Is the inference relation accurately represented (scheme, premises → conclusion)?",
    "What is the NARROWEST conclusion the passage establishes?",
]


def _c1_body(c1_id: str) -> str:
    p = os.path.join(C1_DIR, f"c1_{c1_id}.md")
    if not os.path.exists(p):
        return "(source file not found)"
    return "\n".join(l.lstrip("> ").strip() for l in open(p, encoding="utf-8")
                     if l.strip().startswith(">"))


def _l2_excerpt(l2_name: str) -> str:
    p = os.path.join(PILOT_DIR, l2_name)
    if not os.path.exists(p):
        return "(source file not found)"
    return "\n".join(l for l in open(p, encoding="utf-8").read().splitlines() if l.strip())[:1400]


def _node_text(n: dict) -> str:
    pid = n.get("proposition_id") or n.get("id")
    text = n.get("text") or n.get("proposition")
    kind = n.get("kind")
    exp = n.get("explicitness")
    com = n.get("commitment")
    return f"- **{pid}** [{kind}/{exp}{('/' + com) if com else ''}]: {text}"


def _inf_text(inf: dict) -> str:
    iid = inf.get("inference_id") or inf.get("id")
    scheme = inf.get("scheme")
    prem = ", ".join(inf.get("premise_ids", []))
    concl = ", ".join(inf.get("conclusion_ids") or ([inf["conclusion_id"]] if inf.get("conclusion_id") else []))
    return f"- **{iid}** [{scheme}]: {prem} → {concl} — {inf.get('rationale', '')}"


def render(gold: dict) -> str:
    gid = gold["gold_id"]
    c1_id, l2_name = SOURCES[gid]
    nodes = gold.get("nodes", [])
    infs = gold.get("inferences", [])
    risk = RISK.get(gid, "")

    out = []
    out.append(f"## {gid} — {gold.get('title')}")
    out.append(f"**Passage:** `{gold.get('passage')}` · **Structure:** {gold.get('structure', '(not set)')}")
    if gold.get("research_question"):
        out.append(f"**Research question:** {gold['research_question']}")
    out.append("")
    out.append("### SOURCE (the material a reviewer judges against)")
    if gid in PRIMARY_TEXT:
        out.append("**PRIMARY TEXT (exact Sanskrit spans — resolved via the vertical machinery):**")
        out.append(", ".join(PRIMARY_TEXT[gid]))
        out.append("")
    else:
        out.append("> **PRIMARY TEXT:** exact Sanskrit spans not yet attached for this gold — required before "
                   "SPECIALIST_REVIEWED promotion (this review is against the C1/L2 packet, not the primary Sanskrit).")
        out.append("")
    out.append("**Commentary (C1):**")
    out.append(_c1_body(c1_id))
    out.append("")
    out.append("**Reading (L2):**")
    out.append(_l2_excerpt(l2_name))
    out.append("")
    out.append("### PROPOSED ARGUMENT")
    out.append("**Propositions:**")
    out.extend(_node_text(n) for n in nodes)
    out.append("")
    out.append("**Inferences:**")
    out.extend(_inf_text(i) for i in infs)
    out.append("")
    if risk:
        out.append(f"> {risk}")
        out.append("")
    out.append("### REVIEW — the four questions")
    for i, q in enumerate(QUESTIONS, 1):
        out.append(f"{i}. {q}")
    out.append("")
    out.append("### REVIEWER OUTPUT")
    out.append("- **Decision:** `ACCEPT` / `REVISE` / `REJECT` / `ABSTAIN`  (circle one)")
    out.append("- **Reason:** __________________________________________________________________")
    out.append("- **Any proposition/inference you would change:** __________________________________________________________________")
    out.append("")
    out.append("---")
    return "\n".join(out)


def main():
    header = """# ARG-GOLD REVIEW PACKET — the five candidate arguments

*Prepared 2026-08-12. This packet lets an INDEPENDENT reader judge whether each proposed argument is
faithful to its source. You do **not** need to know Pāṭala or edit JSON — you judge scholarship; Pāṭala
converts your judgment into infrastructure.*

**How to review each argument:**
1. Read the **SOURCE** (the commentary + reading).
2. Read the **PROPOSED ARGUMENT** (propositions + inference graph).
3. Answer the **four questions**.
4. Record your **decision**: ACCEPT / REVISE / REJECT / ABSTAIN, with a reason.

**What is needed of a reviewer:** independence from the builder + enough competence to falsify obvious
reconstruction errors. A Sanskrit / Indian-philosophy PhD, postdoc, teacher, or advanced researcher is
sufficient for a first pass; the hardest disputed cases can later go to a more senior specialist.

**Status ladder:** MACHINE_PROPOSED → FOUNDER_REVIEWED → INDEPENDENT_REVIEWED → SPECIALIST_REVIEWED → ADJUDICATED.
These five are currently MACHINE_PROPOSED (CANDIDATE). A MODEL review (REVIEW-2026-08-12-MODEL-1) returned
REVISE / REJECT_AS_TEXTUAL_GOLD — it is **MODEL_INDEPENDENT_REVIEWED**, NOT INDEPENDENT_REVIEWED / SPECIALIST_REVIEWED
(those require a human Sanskritist against the primary text). After ONE clean argument crosses
INDEPENDENT_REVIEWED, it becomes the target for the external formal-evaluator (py-aspic) pilot.

**Risk areas to watch (do not treat these as neutral):** ARG-003 (the regress), ARG-004 (vimarśa-as-essence),
ARG-005 (ambiguity vs scope). ARG-001/002 are reviewed with the same rigor — they are not grandfathered.

---

"""
    body = [render(b()) for b in BUILDERS.values()]
    doc = header + "\n".join(body)
    out = "/root/projects/patala/benchmarks/v0/ARG-GOLD-REVIEW-PACKET.md"
    open(out, "w", encoding="utf-8").write(doc)
    print(f"wrote {out} ({len(doc)} bytes, {len(BUILDERS)} arguments)")


if __name__ == "__main__":
    main()

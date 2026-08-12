#!/usr/bin/env python3
"""build_theme_review_packet.py — the CP3 theme-adjudication packet (kind + coarse sense judgments).

Turns three existing machine clusters into reviewable scholarly objects. Each candidate theme produces
THREE judgments simultaneously:
  1. MEMBERSHIP — which passages belong / are missing / don't belong
  2. KIND      — what sort of scholarly object is this (narrowest adequate kind)
  3. SENSE     — is the key concept stable across the members (coarse, NOT full alignment)

Kind taxonomy (pick the NARROWEST adequate kind; a RETYPE is a SUCCESS, not a failure):
  CONCEPT_TERM_FAMILY · LOCAL_THEME · DOCTRINAL_PROBLEM_DOMAIN · DEBATE · ARGUMENT_CLUSTER · MOTIF ·
  RETYPE_OTHER

Coarse sense-tagging per key lemma (deliberately primitive — do NOT solve full alignment here):
  SAME_SENSE · NEAR_SAME · DIFFERENT_SENSE · AMBIGUOUS · NOT_ENOUGH_CONTEXT  (+ optional pairwise notes)

Theme definition (NOT argument-dependent): "A Theme is a coherent interpretive/doctrinal strand
instantiated across passages under a bounded scope." Arguments may support or structure a Theme but do
not define its existence. A Theme has relations:
  HAS_MEMBER → Passage · DISCUSSES_CONCEPT → Sense · SUPPORTED_BY / ORGANIZED_BY → Argument ·
  PARTICIPATES_IN → Debate

Handoff: machine clustering → CP3 review packet → accepted/revised membership + kind + coarse sense
annotations → Semantic Alignment gold seeds.

Run: cd research && . .venv/bin/activate && python experiments/build_theme_review_packet.py
"""
from __future__ import annotations
import json
import os

IPVV = "/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv"
C1_DIR = os.path.join(IPVV, "c1", "read")
CLUSTERS = json.load(open("/root/projects/patala/data/published/ipvv/clusters.json"))["clusters"]
OUT = "/root/projects/patala/benchmarks/v0/THEME-ADJUDICATION-PACKET.md"

KINDS = ["CONCEPT_TERM_FAMILY", "LOCAL_THEME", "DOCTRINAL_PROBLEM_DOMAIN", "DEBATE",
         "ARGUMENT_CLUSTER", "MOTIF", "RETYPE_OTHER"]
SENSE = ["SAME_SENSE", "NEAR_SAME", "DIFFERENT_SENSE", "AMBIGUOUS", "NOT_ENOUGH_CONTEXT"]

THEMES = {
    "Order-less Support": {
        "cluster_id": "CL-3", "suspected_kind": "LOCAL_THEME",
        "label": "The Order-less Support of the Powers",
        "key_lemmas": ["āśraya (support)", "akrama / order-less", "pratibhā (the flashing)"],
        "competing": "CL-0 (memory / pastness of the knower) · CL-4 (states / kancukas)",
        "members": ["V2L-nonconstructed-I", "V2N-inner-appearance", "V2O-orderless-support",
                    "V2P-pramatr-vyapara", "V2Q-omniscient", "V2R-mahesvarya",
                    "V2S-unity-mahesvarya", "V3F-grace", "V3I-difference-real"],
        "why": "curated see-also edges centered on V2O-orderless-support (the one-support of the powers). "
               "But note V3F (grace) and V3I (difference-real) may belong to other strands — that is the "
               "membership question.",
    },
    "Vimarśa": {
        "cluster_id": "CL-2", "suspected_kind": "CONCEPT_TERM_FAMILY",
        "label": "Vimarśa / reflexive awareness (parā-vāk)",
        "key_lemmas": ["vimarśa (reflexive awareness)", "sphurattā (throbbing)", "parā-vāk (supreme speech)"],
        "competing": "CL-3 (overlaps via V2L / V2O — reflexive awareness in the non-constructed-I)",
        "members": ["V2H-vimarsa-paravak", "V2I-sphuratta", "V2J-samskara", "V2K-vacakasphota"],
        "why": "curated see-also edges among vimarśa, sphurattā, samskāra, and vākāsphoṭa — a technical "
               "term family around reflexive awareness; possibly a CONCEPT_TERM_FAMILY rather than one "
               "local argument.",
    },
    "Pramāṇa": {
        "cluster_id": "(cross-cutting)", "suspected_kind": "DOCTRINAL_PROBLEM_DOMAIN",
        "label": "Pramāṇa / epistemic warrants (means of knowledge)",
        "key_lemmas": ["pramāṇa (means of knowledge)", "anumāna (inference)", "vyāpti (pervasion)"],
        "competing": "CL-1 (knowledge-power / inference of externals) · CL-8 (inference across knowers)",
        "members": ["V2D-jnanasakti", "V2E-external-inferred", "V2F-other-minds", "V3H-inference-across-knowers"],
        "why": "not a single cluster — pramāṇa as a doctrinal problem domain spans knowledge-power, "
               "inference of externals/other minds, and inference-across-knowers. Likely a "
               "DOCTRINAL_PROBLEM_DOMAIN, not a local theme.",
    },
}

REVIEW_Q = [
    "COHERENCE — do these passages actually instantiate ONE interpretive/doctrinal strand, or several?",
    "SCOPE — is the label too broad / too narrow for the members?",
    "MEMBERSHIP — which members don't belong / which obvious ones are missing?",
    "DISTINCTNESS — is this a Theme, or really a Concept / Debate / Motif / ArgumentCluster / DoctrinalDomain?",
]


def c1_snippet(c1_id: str) -> str:
    p = os.path.join(C1_DIR, f"c1_{c1_id}.md")
    if not os.path.exists(p):
        return "(missing)"
    lines = [l.lstrip("> ").strip() for l in open(p, encoding="utf-8") if l.strip().startswith(">")]
    return " ".join(lines)[:260]


def edge_evidence(cluster_id: str) -> str:
    if cluster_id == "(cross-cutting)":
        return "spans clusters CL-1, CL-8 (and partly CL-3)"
    for c in CLUSTERS:
        if c["cluster_id"] == cluster_id:
            edges = c.get("edge_evidence", [])[:4]
            return "; ".join(f"{e['a']}↔{e['b']} ({e['type']}/{e['weight']})" for e in edges)
    return ""


def render(name: str, t: dict) -> str:
    out = [f"## Candidate Theme: {name}", f"- **Proposed label:** {t['label']}",
           f"- **Cluster:** {t['cluster_id']}  **suspected kind:** {t['suspected_kind']}",
           f"- **Nearest competing:** {t['competing']}", f"- **Why grouped:** {t['why']}", ""]
    out.append("### Members (C1) + snippets")
    for m in t["members"]:
        out.append(f"- `{m}` — {c1_snippet(m)}")
    out.append("")
    out.append(f"### Edge evidence\n- {edge_evidence(t['cluster_id'])}")
    out.append("")
    out.append("### SENSE judgment — key concepts across the members (coarse, NOT full alignment)")
    out.append("For each key lemma, judge whether it is used in a stable sense across the members:")
    for kl in t["key_lemmas"]:
        out.append(f"- **{kl}:** `{'` / `'.join(SENSE)}`  + pairwise notes: ______________")
    out.append("")
    out.append("### REVIEW — the four questions")
    for q in REVIEW_Q:
        out.append(f"- {q}")
    out.append("")
    out.append("### REVIEWER OUTPUT — three judgments")
    out.append("**1. MEMBERSHIP**  (passages to add / remove / confirm): ______________")
    out.append(f"**2. KIND**  (narrowest adequate kind): `{'` / `'.join(KINDS)}`  — why: ______________")
    out.append("**3. SENSE**  (per key lemma, as above)  — is the concept stable? ______________")
    out.append("- **Decision:** `ACCEPT` / `REVISE` / `REJECT` / `RETYPE`  (circle one)")
    out.append("---")
    return "\n".join(out)


def main():
    header = """# THEME-ADJUDICATION PACKET (CP3) — kind + coarse-sense review

*Prepared 2026-08-12. Turns three existing machine clusters into reviewable scholarly objects. You do
NOT need to know Pāṭala — you judge scholarship; Pāṭala converts your judgment into infrastructure.*

**Theme definition (not argument-dependent):** a Theme is a coherent interpretive/doctrinal strand
instantiated across passages under a bounded scope. Arguments may support or structure a Theme; they do
not define its existence. Relations a Theme may carry:
`HAS_MEMBER → Passage` · `DISCUSSES_CONCEPT → Sense` · `SUPPORTED_BY/ORGANIZED_BY → Argument` ·
`PARTICIPATES_IN → Debate`.

**Kind taxonomy (pick the NARROWEST adequate kind; a RETYPE is a SUCCESS, not a failure):**
`CONCEPT_TERM_FAMILY` · `LOCAL_THEME` · `DOCTRINAL_PROBLEM_DOMAIN` · `DEBATE` · `ARGUMENT_CLUSTER` ·
`MOTIF` · `RETYPE_OTHER`.

**Status ladder:** MACHINE_PROPOSED → MODEL_REVIEWED → INDEPENDENT_REVIEWED → ACCEPTED_THEME.

**The key question across all three:** are Order-less Support, Vimarśa, and Pramāṇa the SAME kind? They
are suspected to differ. If Vimarśa → CONCEPT_TERM_FAMILY and Pramāṇa → DOCTRINAL_PROBLEM_DOMAIN, that is
a CP3 SUCCESS — it means the system correctly distinguishes compression kinds.

---

"""
    body = "\n".join(render(name, t) for name, t in THEMES.items())
    open(OUT, "w", encoding="utf-8").write(header + body)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()

"""Pāṭala prompts — the house instructions injected into the model per stage.

These encode the standardised process (docs/STYLE_GUIDE, EVIDENCE_POLICY,
REVIEW_PROTOCOL, TRANSLATION_SCHEMA). Each stage gets its own system prompt.
The model follows the process; the pipeline stores + audits the result.
"""
from __future__ import annotations
from typing import Any

# The house voice (STYLE_GUIDE.md) — shared by the translation stages.
STYLE = """You translate medieval Śaiva Sanskrit for Pāṭala. House rules:
- Use IAST. Retain technical terms untranslated (śakti, kula, krama, spanda,
  vimarśa, prakāśa, visarga, khecarī, āveśa, uccāra, śūnya, mātṛkā, saṃvit,
  parāmarśa, svātantrya, tattva) where English would obscure the technical sense.
- Capitalise Śiva/Śivā (names), and Goddess/Consciousness/Power only when the
  doctrinal absolute is meant. Prefer lowercase when in doubt.
- close_translation = structurally faithful. reading (T3.1) = natural, flowing,
  still accurate. Never prettier at the cost of meaning.
- Preserve ambiguity: preferred reading in the text, alternative in the note.
  Do NOT silently resolve. Do NOT copy published translations or prior T-versions.
- Do not insert later-school doctrine into an earlier text. A commentary's gloss
  is evidence, not the root's own claim.
- Flag with [X] anything corrupt, lacunose, or genuinely ambiguous.
"""

# The evidence policy (EVIDENCE_POLICY.md) — how to reason.
EVIDENCE = """Evidence discipline:
- Nothing overrides the grammar of the present passage. A parallel or commentary
  can constrain or suggest; it cannot bend the passage's own syntax.
- A justification is one of [G] grammar, [P] parallel usage, [A] anchor
  (published translation), [R] reconstruction. Unjustified paraphrase is rejected.
- term proposals never become accepted corpus knowledge by themselves.
"""


def sys_T1() -> str:
    return (STYLE + "\n" + EVIDENCE +
            "\nProduce the T1 working translation for the verse given. "
            "Output the close translation, then notes ([G]/[P]/[A]/[R] where "
            "relevant), and any [X] flags.")


def sys_R1() -> str:
    return (STYLE + EVIDENCE +
            "\nYou are the R1 peer reviewer. Review the given T1 intimately against "
            "the Sanskrit source and any anchor. For every verse: assess the "
            "translation closely; flag anything vague, uncertain, or [X]-worthy; "
            "give your verdict (RIGHT / ERROR / FORK / OPEN) with [G]/[P]/[A]/[R] "
            "evidence; and leave a SHORT COMMENTARY STUB per crux — the seed of "
            "what the full commentary will grow into. Be a genuine peer reviewer: "
            "challenge, don't confirm.")


def sys_T2() -> str:
    return (STYLE + EVIDENCE +
            "\nYou are T2. Produce a COMPLETE ALTERNATIVE translation of the verse "
            "that ACTIVELY GOES AGAINST the given T1 where you believe T1 is wrong "
            "or limited, informed by the R1 review. This is not a cosmetic "
            "re-wording: pursue a genuinely different reading-strategy and adopt "
            "a different interpretation wherever the Sanskrit allows it. Where "
            "the text is fixed and you independently land on the same reading, "
            "say so (that agreement is the hard core). Cite [G]/[P]/[A]/[R] for "
            "every divergence you make from T1.")


def sys_R2() -> str:
    return (STYLE + EVIDENCE +
            "\nYou are R2, the synthesis. Building on the R1 review, compare T1 "
            "and T2 of the verse LINE BY LINE. For each verse: (1) where they "
            "agree — that is the hard core; (2) where they diverge — adjudicate "
            "which is best and why, considering overall readability, grammatical "
            "faithfulness, and the evidence; (3) do research into the school/period "
            "context that bears on the reading; (4) note any EQUALLY VALID "
            "alternate translations as an open set; (5) EXPAND THE COMMENTARY — "
            "grow the R1 stubs into full notes (doctrine, parallels, anchor-quotes, "
            "period context). Mark genuinely interpretable verses OPEN rather than "
            "flattening them.")


def sys_T3() -> str:
    return (STYLE + "\nProduce T3: the final resolved translation, carrying any "
            "genuinely-open [X] flags inline. Add editorial notes where a reading "
            "was settled.")


def sys_T31() -> str:
    return (STYLE + "\nProduce T3.1: the natural-English READING layer derived "
            "from the given T3 resolved text. Flowing, readable, defensible. "
            "In lock-step with T3 — do not change the meaning.")


def sys_C1() -> str:
    return ("Produce C1: a plain-English commentary/interpretation of the verse "
            "for a thoughtful general reader. Explain what it means and why it "
            "matters. You MAY research independently and overturn the T3 reading "
            "if evidence demands, but say so explicitly. Do not pad; be precise "
            "and grounded in the Sanskrit.")


def sys_AUDIT() -> str:
    return ("You are the translation auditor. Given a proposed translation and "
            "the source Sanskrit, return JSON of evidence-backed findings. "
            "Categories: NEGATION (omitted/added na/mā), NUMBERS (counts lost), "
            "OMISSION, UNSUPPORTED_ADDITION, TERM_DRIFT (term rendered differently "
            "from the house sense), GRAMMATICAL_UNCERTAINTY, PARALLEL_CONFLICT. "
            "An audit surfaces evidence for review; it never declares a "
            "translation 'wrong' without evidence.")


STAGE_SYSTEM = {
    "T1": sys_T1, "R1": sys_R1, "T2": sys_T2, "R2": sys_R2,
    "T3": sys_T3, "T3.1": sys_T31, "C1": sys_C1,
}


def user_prompt(stage: str, record: dict[str, Any]) -> str:
    """Build the user message for a stage from the current record."""
    src = record["source"]
    loc = record["location"]
    base = (f"Work: {record['work_id']} · {loc['chapter']}.{loc['verse']}\n"
            f"Edition: {src['source_edition']}\n"
            f"Sanskrit: {src['source_text']}\n")

    if stage == "T1":
        return base + "\nProduce the T1 working translation."
    if stage == "R1":
        t1 = record["stages"].get("T1", {})
        return (base + f"\nT1: {t1.get('close_translation','')}\n"
                f"T1 flags: {t1.get('flags',[])}\n"
                "Review this T1 (prosecutor).")
    if stage == "T2":
        t1 = record["stages"].get("T1", {})
        r1 = record["stages"].get("R1", {})
        return (base + f"\nT1 (actively oppose where wrong): {t1.get('close_translation','')}\n"
                f"T1 flags: {t1.get('flags',[])}\n"
                f"R1 review: {r1.get('detail','')}\n"
                "Produce the T2 — a complete alternative that goes against T1 where it is wrong or limited.")
    if stage == "R2":
        t1 = record["stages"].get("T1", {})
        t2 = record["stages"].get("T2", {})
        r1 = record["stages"].get("R1", {})
        return (base
                + f"\nT1: {t1.get('close_translation','')}\n"
                + f"T2: {t2.get('close_translation','')}\n"
                + f"R1 stubs: {r1.get('detail','')}\n"
                + "Synthesise: hard-core agreement, divergence adjudication, school-context research, expand commentary, note equally-valid alternates, mark OPEN.")
    if stage == "T3":
        r2 = record["stages"].get("R2", {})
        return (base + f"\nR2 resolved: {r2.get('chosen','')}\n"
                "Produce the final T3.")
    if stage == "T3.1":
        t3 = record["stages"].get("T3", {})
        return (base + f"\nT3 resolved: {t3.get('resolved','')}\n"
                "Produce the T3.1 reading layer.")
    if stage == "C1":
        t3 = record["stages"].get("T3", {})
        return (base + f"\nT3: {t3.get('resolved','')}\n"
                "Produce the C1 commentary.")
    return base

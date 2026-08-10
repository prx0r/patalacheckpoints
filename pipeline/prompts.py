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
- Justification codes: [G] grammar/source, [P] primary textual parallel,
  [C] commentary, [S] modern scholarship, [A] existing translation,
  [R] reconstruction/emendation.
- Hierarchy: current Sanskrit/textual state → grammar → same-text evidence →
  direct primary parallels → commentaries → scholarship → existing translations.
  An existing translation is evidence about how another scholar solved it, not
  independent proof their solution is correct.
- term proposals never become accepted corpus knowledge by themselves.
"""


def sys_T1() -> str:
    return (STYLE + "\n" + EVIDENCE +
            "\nProduce the T1 working translation for the verse given. "
            "Output the close translation, then notes ([G]/[P]/[A]/[R] where "
            "relevant), and any [X] flags.")


def sys_R1() -> str:
    return (STYLE + EVIDENCE +
            "\nYou are the R1 adversarial critique (NOT human peer review — you are a "
            "machine pass). Attack the given T1 against the Sanskrit source and any "
            "anchor. Your job is to find where T1 can fail and to MAP THE GENUINE "
            "CRUXES — the points where a materially different grammatical, lexical, "
            "textual, referential, or doctrinal reading is defensible. For each crux "
            "output: crux_id, type (LEXICAL/GRAMMATICAL/TEXTUAL/REFERENTIAL/DOCTRINAL/"
            "CONTEXTUAL), the T1 assumption, the alternative candidates, and what "
            "evidence is needed to decide. Give a verdict (RIGHT / ERROR / FORK / OPEN) "
            "with [G]/[P]/[C]/[S]/[A]/[R] evidence, and leave a SHORT COMMENTARY STUB "
            "per crux. Challenge genuinely; do NOT manufacture doubts on secure verses.")

R1_CRUX_TYPES = ["LEXICAL", "GRAMMATICAL", "TEXTUAL", "REFERENTIAL", "DOCTRINAL", "CONTEXTUAL"]


def sys_T2() -> str:
    return (STYLE + EVIDENCE +
            "\nYou are T2. You SEE T1 and the R1 critique. Produce the STRONGEST "
            "MATERIALLY DIFFERENT translation that remains defensible from the Sanskrit "
            "and evidence — not a blind copy, not an exercise in disagreement.\n"
            "RULES:\n"
            "- Adopt a different reading ONLY where it changes syntax, referent, "
            "  technical sense, doctrinal implication, textual reading, or meaningful "
            "  English interpretation (the difference budget).\n"
            "- Do NOT introduce differences merely for stylistic variety.\n"
            "- Address the cruxes R1 mapped: use the rival candidate that survives "
            "  inspection, or explain why the T1 reading is correct.\n"
            "- Where the Sanskrit does not support a meaningful alternative, preserve "
            "  the T1 reading and mark it CONSTRAINED.\n"
            "- Cite [G]/[P]/[C]/[S]/[A]/[R] for every divergence you make.")


def sys_R2() -> str:
    return (STYLE + EVIDENCE +
            "\nYou are R2, the adjudicator. Building on R1, compare T1 and T2 BY "
            "DECISION, not merely by sentence. For each crux/decision:\n"
            "- where the readings agree AND the source constrains it — that is the "
            "  HARD CORE (invariant across serious analyses + source-constrained).\n"
            "- where they diverge — classify each decision as:\n"
            "    CONSTRAINED   source effectively forces this\n"
            "    PREFERRED     best reading, but alternatives are plausible\n"
            "    OPEN          two or more serious readings remain\n"
            "    RECONSTRUCTED requires textual intervention\n"
            "- give the reasoning, do school/period-context research, EXPAND THE "
            "  COMMENTARY (grow the R1 stubs into full notes).\n"
            "- record equal_alternates and open questions explicitly.\n"
            "Output a decision list (crux → preferred / status / reason / evidence), "
            "then the overall hard-core and the open set.")


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
            "matters. You MAY research independently and CHALLENGE the T3 reading "
            "if evidence demands — but you do NOT mutate or supersede T3. If you "
            "find the translation deficient, state it as a challenge with the "
            "evidence and the revision you would propose; the pipeline will route "
            "it through a new adjudication → T3 v2. Do not pad; be precise and "
            "grounded in the Sanskrit.")


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


def user_prompt(stage: str, record: dict[str, Any], evidence_packet: dict | None = None) -> str:
    """Build the user message for a stage from the current record + the evidence packet."""
    src = record["source"]
    loc = record["location"]
    base = (f"Work: {record['work_id']} · {loc.get('locator', loc['chapter'])}.{loc.get('verse', loc.get('chapter',''))}\n"
            f"Edition: {src['source_edition']}\n"
            f"Sanskrit: {src['source_text']}\n")

    # prepend the evidence packet (deterministic context) for every stage
    evidence_blk = ""
    if evidence_packet:
        e = evidence_packet
        parts = [f"EVIDENCE PACKET (deterministic — adjudicate using THIS, not model memory):"]
        if e.get("neighbors"):
            parts.append("  neighbors: " + "; ".join(f"{n['locator']}: {n['sanskrit'][:60]}" for n in e["neighbors"]))
        if e.get("terms"):
            parts.append("  tracked terms: " + "; ".join(
                f"{t['lemma']} ({'|'.join(t['senses'])})" for t in e["terms"]))
        if e.get("work"):
            parts.append(f"  work: {e['work'].get('id')}")
        evidence_blk = "\n".join(parts) + "\n"

    base = evidence_blk + base

    if stage == "T1":
        return base + "\nProduce the T1 working translation as STRICT JSON:\n" \
               '{"close_translation":"...","reader_draft":"...","flags":[],"notes":[],' \
               '"lexical_decisions":[],"grammatical_notes":[],"time_place_context":{}}'
    if stage == "R1":
        t1 = record["stages"].get("T1", {})
        return (base + f"\nT1: {t1.get('close_translation','')}\n"
                f"T1 flags: {t1.get('flags',[])}\n"
                "Attack this T1 and map the genuine cruxes as STRICT JSON: "
                '{"detail":"...","cruxes":[{"id":"...","type":"LEXICAL","assumption":"...",'
                '"rivals":[],"evidence_needed":[]}],"verdicts":[{"verdict":"FORK","crux":"..."}]}')
    if stage == "T2":
        t1 = record["stages"].get("T1", {})
        r1 = record["stages"].get("R1", {})
        cruxes = r1.get("cruxes", [])
        crux_txt = "\n".join(f"  crux {c.get('id')} [{c.get('type')}]: {c.get('detail','')} — rivals {c.get('rivals',[])}"
                             for c in cruxes) or "  (none mapped)"
        return (base + f"\nT1: {t1.get('close_translation','')}\n"
                f"T1 flags: {t1.get('flags',[])}\n"
                f"R1 cruxes:\n{crux_txt}\n"
                "Produce T2 — the strongest materially-different defensible reading that "
                "addresses these cruxes — as STRICT JSON: "
                '{"close_translation":"...","strategy":"...","rival_decisions":'
                '[{"crux_id":"...","adopted":"...","differs_from_t1":true,"reason":"...","evidence":[]}],'
                '"constrained":[]}. Do NOT manufacture disagreement on secure verses.')
    if stage == "R2":
        t1 = record["stages"].get("T1", {})
        t2 = record["stages"].get("T2", {})
        r1 = record["stages"].get("R1", {})
        return (base
                + f"\nT1: {t1.get('close_translation','')}\n"
                + f"T2: {t2.get('close_translation','')}\n"
                + f"T2 rival decisions: {t2.get('rival_decisions',[])}\n"
                + f"R1 cruxes: {r1.get('detail','')}\n"
                + "Adjudicate BY DECISION as STRICT JSON: "
                  '{"chosen":"...","reasoning":"...","decisions":[{"crux_id":"...",'
                  '"preferred":"...","status":"CONSTRAINED|PREFERRED|OPEN|RECONSTRUCTED",'
                  '"reason":"...","evidence":[]}],"hard_core":"...","equal_alternates":[],'
                  '"commentary":"..."}')
    if stage == "T3":
        r2 = record["stages"].get("R2", {})
        decisions = r2.get("decisions", [])
        open_dec = [d for d in decisions if d.get("status") == "OPEN"]
        recons = [d for d in decisions if d.get("status") == "RECONSTRUCTED"]
        return (base
                + f"\nR2 chosen: {r2.get('chosen','')}\n"
                + f"R2 decisions: {decisions}\n"
                + f"OPEN decisions (must appear in open_flags): {open_dec}\n"
                + f"RECONSTRUCTED (must carry editorial note): {recons}\n"
                + "Produce the final T3. Respect the R2 decision statuses mechanically:\n"
                  "  OPEN → carry in open_flags; RECONSTRUCTED → carry an editorial note; "
                  "CONSTRAINED → ordinary resolved text. Return as STRICT JSON: "
                  '{"resolved":"...","open_flags":[{"flag":"LEX","detail":"..."}],'
                  '"editorial_notes":[]}')
    if stage == "T3.1":
        t3 = record["stages"].get("T3", {})
        return (base + f"\nT3 resolved: {t3.get('resolved','')}\n"
                "Produce the T3.1 reading layer (natural English, in lock-step with T3).")
    if stage == "C1":
        t3 = record["stages"].get("T3", {})
        r2 = record["stages"].get("R2", {})
        return (base + f"\nT3: {t3.get('resolved','')}\n"
                f"R2 decisions: {r2.get('decisions',[])}\n"
                "Produce the C1 commentary. You may CHALLENGE T3 with evidence + a "
                "proposed revision, but do not mutate T3.")
    return base

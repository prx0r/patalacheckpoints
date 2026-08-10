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
    # CONCISE system prompt — the full house style is too long for the model in
    # strict-JSON mode and produces empty output (an empirical 1.8 finding).
    return ("You translate medieval Śaiva Sanskrit for Pāṭala. Rules: use IAST; "
            "retain technical terms (śakti, kula, krama, spanda, vimarśa, prakāśa, "
            "visarga, khecarī, mātṛkā, saṃvit, svātantrya) where English would obscure "
            "the sense; be structurally faithful; flag genuine ambiguity with [X]; "
            "do NOT invent doctrine or copy published translations. Return ONLY valid JSON.")


def sys_R1() -> str:
    return ("You are an adversarial Sanskrit translation critic. Find only materially "
            "defensible alternative readings. Do NOT manufacture ambiguity. Use only "
            "the supplied Sanskrit and evidence — doctrine and existing translations "
            "do not outrank them. Return ONLY valid JSON.")

R1_CRUX_TYPES = ["LEXICAL", "GRAMMATICAL", "TEXTUAL", "REFERENTIAL", "DOCTRINAL", "CONTEXTUAL"]


def sys_T2() -> str:
    return ("Construct the strongest coherent rival to T1 using R1's genuine cruxes. "
            "Change only interpretation, syntax, referent, technical sense, or textual "
            "reading — never wording merely for variety. Use only the supplied Sanskrit "
            "and evidence. Return ONLY valid JSON.")


def sys_R2() -> str:
    return ("Adjudicate T1 and T2 from the supplied Sanskrit and evidence. For each crux "
            "classify the chosen reading as CONSTRAINED / PREFERRED / OPEN / RECONSTRUCTED. "
            "Do not remove unresolved ambiguity. Return ONLY valid JSON.")


def sys_T3() -> str:
    return (STYLE + "\nProduce T3: the final resolved translation, carrying any "
            "genuinely-open [X] flags inline. Add editorial notes where a reading "
            "was settled.")


def sys_T31() -> str:
    return (STYLE + "\nProduce T3.1: the natural-English READING layer derived "
            "from the given T3 resolved text. Flowing, readable, defensible. "
            "In lock-step with T3 — do not change the meaning.")


def sys_C1() -> str:
    return ("You are producing C1, the capstone scholarly commentary for a passage. "
            "Follow skills/write-commentary. It is NOT a free-form essay or a "
            "paraphrase of T3 — it is concise, source-aware, explicit about "
            "uncertainty. Adjudicate from the supplied EVIDENCE PACKET + the "
            "translation stack (T1/R1/T2/R2/T3/T3.1), not model memory.\n"
            "Structure: A) core sense (what is being said), B) why this reading "
            "(the decisive evidence chain), C) the crux/uncertainty (only if real), "
            "D) larger significance (evidence-tied).\n"
            "Every nontrivial claim is one of TEXTUAL/GRAMMATICAL/INTERPRETIVE/"
            "HISTORICAL/ATTRIBUTED/SYNTHESIS — say which. No vague 'scholars say' "
            "or 'traditionally understood as'.\n"
            "You may CHALLENGE T3 (emit a TranslationChallenge with evidence + a "
            "proposed revision) but must NEVER mutate or supersede T3.\n"
            "Emit structured PROPOSALS (TermSenseAssignment, TermHistoryAssertion, "
            "ParallelAssertion, DoctrinalAssertion, CommentaryClaim, ResearchQuestion) "
            "as origin=machine, status=proposed.\n"
            "Set evidence_state to C1_EVIDENCE_COMPLETE only if every required item "
            "is met; otherwise C1_EVIDENCE_PARTIAL with the missing items listed.\n"
            "Return STRICT JSON: {\"interpretation\":\"...\",\"evidence_state\":"
            "\"C1_EVIDENCE_PARTIAL\",\"cruxes\":[],\"evidence\":[],"
            "\"open_questions\":[],\"proposals\":[],\"challenges\":[]}")


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
    locator_str = loc.get("locator") or f"{loc['chapter']}.{loc.get('verse', '')}"
    base = (f"Work: {record['work_id']} · {locator_str}\n"
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
        # LEAN schema — the full multi-field JSON makes the model return empty
        # (an empirical 1.8 finding); the pipeline fills defaults for the rest.
        return base + "\nProduce the T1 working translation as STRICT JSON (lean):\n" \
               '{"close_translation":"...","reader_draft":"...","flags":[]}'
    if stage == "R1":
        t1 = record["stages"].get("T1", {})
        return (base + f"\nT1: {t1.get('close_translation','')}\n"
                f"T1 flags: {t1.get('flags',[])}\n"
                "Find genuinely defensible alternative readings. Return STRICT JSON (lean):\n"
                '{"assessment":"...","cruxes":[{"id":"c1","type":"LEXICAL","assumption":"...",'
                '"rivals":[],"need":"..."}]}. If none: {"assessment":"...","cruxes":[]}')
    if stage == "T2":
        t1 = record["stages"].get("T1", {})
        r1 = record["stages"].get("R1", {})
        cruxes = r1.get("cruxes", [])
        crux_txt = "\n".join(f"  crux {c.get('id')} [{c.get('type')}]: {c.get('assumption','')} — rivals {c.get('rivals',[])}"
                             for c in cruxes) or "  (none mapped)"
        return (base + f"\nT1: {t1.get('close_translation','')}\n"
                f"R1 cruxes:\n{crux_txt}\n"
                "Produce the strongest coherent rival. Return STRICT JSON (lean):\n"
                '{"translation":"...","decisions":[{"crux":"c1","reading":"...","reason":"..."}],'
                '"constrained":[]}')
    if stage == "R2":
        t1 = record["stages"].get("T1", {})
        t2 = record["stages"].get("T2", {})
        r1 = record["stages"].get("R1", {})
        return (base
                + f"\nT1: {t1.get('close_translation','')}\n"
                + f"T2: {t2.get('close_translation','')}\n"
                + f"R1 cruxes: {r1.get('detail','')}\n"
                + "Adjudicate by crux. Return STRICT JSON (lean):\n"
                  '{"translation":"...","decisions":[{"crux":"c1","reading":"...",'
                  '"status":"PREFERRED","reason":"..."}],"hard_core":"..."}')
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
        t31 = record["stages"].get("T3.1", {})
        r1 = record["stages"].get("R1", {})
        r2 = record["stages"].get("R2", {})
        t2 = record["stages"].get("T2", {})
        return (base
                + f"\nT3: {t3.get('resolved','')}\n"
                + f"T3.1: {t31.get('reading','')}\n"
                + f"R1 cruxes: {r1.get('cruxes',[])}\n"
                + f"T2 rival decisions: {t2.get('rival_decisions',[])}\n"
                + f"R2 decisions: {r2.get('decisions',[])}\n"
                + f"R2 hard core: {r2.get('hard_core','')}\n"
                + "Produce the C1 capstone commentary as STRICT JSON (see skills/write-commentary): "
                  '{"interpretation":"...","evidence_state":"C1_EVIDENCE_PARTIAL",'
                  '"cruxes":[],"evidence":[{"id":"stable-id","supports":"..."}],'
                  '"open_questions":[],"proposals":[],"challenges":[]}. '
                  "You may CHALLENGE T3 but must never mutate it.")
    return base

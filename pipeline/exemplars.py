"""Pāṭala pipeline_gold exemplars.

Reference passage records built from REAL on-disk material (no model calls).
These are PIPELINE_GOLD — expected-output fixtures for the pipeline, NOT
scholarly gold (they have not been reviewed by domain specialists). Distinguish
from REVIEWED_REFERENCE (externally/human-validated). This matters when the
corpus later claims "N gold passages."

Sources:
- Exemplar A: Kramasadbhāva 1.8 — from `docs/PROOF_T1_kramasadbhava.md` (the
  machine-schema proof) + the on-disk T1. The nirānande crux is carried honestly.
- Exemplar B: Śivasūtra 1.3 — from `corpus/targets/translation_flow_spec.md` §6
  (the worked example: yonivargaḥ kalāśarīram, the yoni-fork adjudication).
"""
from __future__ import annotations
try:
    from .schema import (
        new_passage, set_stage,
        stage_T1, stage_R1, stage_T2, stage_R2, stage_T3, stage_T31, stage_C1,
    )
except ImportError:  # run as plain scripts
    from schema import (
        new_passage, set_stage,
        stage_T1, stage_R1, stage_T2, stage_R2, stage_T3, stage_T31, stage_C1,
    )


def exemplar_kramasadbhava_1_8() -> dict:
    """Kramasadbhāva 1.8 — the Kālī-maṅgala. Built from PROOF_T1_kramasadbhava.md
    and the on-disk T1 (01_t1_working/kramasadbhava_patala1_pass1.md)."""
    r = new_passage(
        "kramasadbhava", 1, 8,
        "oṃ namaste devadeveśi mahākāli namo'stu te | namo'stu paramānande nirānande namo'stu te",
        "Dyczkowski ed., Muktabodha (NGMPP A 209/23)",
        "translations/01_t1_working/kramasadbhava_patala1_pass1.md",
    )

    set_stage(r, stage_T1(
        close=("Śrī-Bhairava spoke: Oṃ, homage to you, O God-of-gods, O Mahākālī, "
               "homage be to you; homage be to the supreme bliss, and homage be to "
               "you, [X: nirānande — 'the bliss-less' or 'beyond bliss'?]."),
        reader_draft=("Śrī Bhairava declared: oṃ, homage to you, God of gods, great "
                      "Kālī — homage be to you; homage to the supreme bliss, and "
                      "homage to you who are beyond bliss."),
        flags=["LEX"],
        lexical_decisions=[
            {"surface": "mahākāli", "lemma": "mahākālī", "translation_here": "Mahākālī (retained)",
             "certainty": "high"},
            {"surface": "nirānande", "lemma": "nirānanda", "translation_here": "beyond bliss (uncertain)",
             "certainty": "low"},
        ],
        grammatical_notes=["a series of vocatives (devadeveśi, paramānande, nirānande) addressing the Goddess in her supreme and transcendent forms."],
        parallels=[{"passage": "candidate: Kālikārahasya Kālī-dhyāna / M00516 Kālīkula register",
                    "kind": "conceptual_parallel", "note": "the Kālī-maṅgala register; validate in R1"}],
        time_place_context={
            "PERIOD": "Krama scriptural prototype (pre-exegetical, before the Mahānayaprakāśa)",
            "PLACE": "the Uttarapīṭha (northern seat); descended at the Śrīnātha's feet",
            "GENRE": "tantra-dialogue (Bhairava↔Devī); the stava (the Kālī-homage)",
            "FRAME": "the Kālī-maṅgala opening the Vyomeśīsamaya-praśna",
        },
    ), "gold-exemplar-A", derived_from=None)

    set_stage(r, stage_R1(
        detail=("The vocatives are secure; the [X] on nirānande is the crux. "
                "'paramānande' (supreme bliss) sets the frame — nirānande is most "
                "naturally the negation 'beyond bliss' (nir- + ānanda), paired with "
                "it. The bliss-less reading (a-nanda) is doctrinally possible but "
                "less likely given the pairing. Commentary-stub: the Goddess as "
                "transcending bliss itself — the maṅgala's apophatic pole."),
        verdicts=[{"verdict": "OPEN", "crux": "nirānande",
                   "detail": "'beyond bliss' (nir-ānanda) vs 'the bliss-less'"}],
        source="Dyczkowski ed., Muktabodha (NGMPP A 209/23)",
    ), "gold-exemplar-A", derived_from="T1")

    set_stage(r, stage_T2(
        close=("Śrī Bhairava said: homage to you, queen of the gods, Mahākālī — "
               "homage; homage to the supreme bliss, and homage to the one "
               "beyond all bliss."),
        strategy="register-shifted + opposite reading of nirānande ('beyond all bliss')",
    ), "gold-exemplar-A", derived_from="R1")

    set_stage(r, stage_R2(
        chosen="T2's 'beyond bliss' — the negated-absolute reading, per the pairing with paramānande.",
        reasoning=("T1 and T2 agree on the core (vocatives, Mahākālī retained). "
                   "The divergence is nirānande: T1 hedges with an [X]; T2 commits "
                   "to 'beyond bliss'. Adjudication: 'beyond bliss' — nir-ā-nanda as "
                   "the transcendent negation, consistent with paramānande and the "
                   "maṅgala's apophatic pole. The a-nanda 'bliss-less' reading is an "
                   "equally-valid alternate, kept on the record."),
        commentary=("The maṅgala opens by hymning the Goddess in her supreme and "
                    "transcendent forms — the bliss and the beyond-bliss. The "
                    "Kālī-maṅgala register recurs across the Krama-cluster (Kālikārahasya, "
                    "M00516). Cross-text: the same pairing structure appears in the "
                    "Devīpañcaśataka's maṅgala."),
        hard_core="the vocative hymning of Mahākālī; homage to the supreme bliss.",
        divergence="nirānande: hedged ([X]) vs committed ('beyond bliss').",
        readability="T2 is smoother; T1 is more literal (close).",
        school_context="Krama maṅgala register; the Goddess transcendent to bliss.",
        equal_alternates=["the bliss-less (a-nanda)", "beyond bliss (nir-ānanda)"],
        is_open=False,
    ), "gold-exemplar-A", derived_from="T2")

    set_stage(r, stage_T3(
        resolved=("Śrī Bhairava spoke: Oṃ, homage to you, O God-of-gods, O Mahākālī, "
                  "homage be to you; homage to the supreme bliss, and homage to you "
                  "who are beyond bliss."),
        open_flags=[{"flag": "LEX", "detail": "nirānande: 'beyond bliss' chosen; 'the bliss-less' equally-valid (kept on record)"}],
        editorial_notes=["nirānande resolved to 'beyond bliss' at R2; the alternate reading retained."],
    ), "gold-exemplar-A", derived_from="R2")

    set_stage(r, stage_T31(
        reading=("Śrī Bhairava declared: oṃ, homage to you, God of gods, great Kālī — "
                 "homage be to you; homage to the supreme bliss, and homage to you "
                 "who are beyond bliss."),
    ), "gold-exemplar-A", derived_from="T3")

    set_stage(r, stage_C1(
        interpretation=("The hymn begins by naming the Goddess in her two poles: she "
                        "is the supreme bliss, and she is also beyond it — the "
                        "consciousness that contains even bliss and stands free of it. "
                        "The opening 'oṃ' and the repeated homage mark this as the "
                        "maṅgala: the auspicious opening of the Krama's scripture, "
                        "offered to Mahākālī, the queen of gods and the mistress of "
                        "the Krama's goddesses."),
        challenges=[],
    ), "gold-exemplar-A", derived_from="T3")

    return r


def exemplar_sivasutra_1_3() -> dict:
    """Śivasūtra 1.3 — yonivargaḥ kalāśarīram. The flow-spec's worked example
    (translation_flow_spec.md §6), rendered into the passage record."""
    r = new_passage(
        "sivasutra", 1, 3, "yonivargaḥ kalāśarīram",
        "GRETIL / SanskritDocuments (our T1)",
        "corpus/targets/translation_flow_spec.md (worked example)",
    )

    set_stage(r, stage_T1(
        close="The group of yonis is the body of the kalās.",
        flags=["LEX"],
        lexical_decisions=[
            {"surface": "yoni", "lemma": "yoni", "translation_here": "yoni (the source; the four powers per Bhāskara)",
             "certainty": "medium"},
            {"surface": "kalā", "lemma": "kalā", "translation_here": "kalā (retained, technical)",
             "certainty": "high"},
        ],
        grammatical_notes=["a nominal sentence: vargaḥ (subject) = śarīram (predicate), kalā (genitive/genitive-compound)."],
        time_place_context={
            "PERIOD": "9th-century Trika (the Śivasūtra milieu)",
            "PLACE": "Kashmir",
            "GENRE": "sūtra (aphoristic)",
            "FRAME": "Kṣemarāja's Vimarśinī + Bhāskara's Vārttika as the commentary frames",
        },
    ), "gold-exemplar-B", derived_from=None)

    set_stage(r, stage_R1(
        detail=("The yoni-fork is the crux: Bhāskara reads yoni as the four powers "
                "(śaktis); Kṣemarāja reads it as māyā. The four-powers reading is "
                "favoured for the Bhāskara-focus of this text."),
        verdicts=[{"verdict": "FORK", "crux": "yoni",
                   "detail": "Bhāskara (the four powers / sources) vs Kṣemarāja (māyā)"}],
        source="GRETIL / SanskritDocuments",
    ), "gold-exemplar-B", derived_from="T1")

    set_stage(r, stage_T2(
        close="The congregation of the sources is the embodiment of the energies.",
        strategy="S1 — commentary-informed: renders through Bhāskara's gloss + the anchor's choices",
    ), "gold-exemplar-B", derived_from="R1")

    set_stage(r, stage_R2(
        chosen="'The group of the sources is the body of the kalās'.",
        reasoning=("Hard core: 'group/aggregate' (varga) — both compositions agree "
                   "independently. Divergence: 'yonis' vs 'sources'; 'body' vs "
                   "'embodiment'; 'kalās' vs 'energies'. Adjudication: 'sources' "
                   "(Bhāskara's explicit gloss yonayaḥ śaktayaḥ + the anchor); "
                   "'body' (the literal — 'embodiment' is the commentary's word); "
                   "'kalās' transliterated (the glossary's ruling — the term is technical)."),
        commentary=("The four-powers cross-link (ŚS 2.7's bracket); the domestication "
                    "lens — the yoni's two faces: the source-goddesses and māyā. The "
                    "kalā-body: the energies as the structured embodiment of the "
                    "ultimate."),
        hard_core="'group/aggregate' (varga).",
        divergence="yoni (source vs family); body vs embodiment; kalā (transliterate vs 'energies').",
        readability="T1 is literal; T2 is flowing; the synthesis keeps the literal close + the commentary's reading.",
        school_context="Trika; the four powers as the sources of manifestation; Kṣemarāja's māyā alternative.",
        equal_alternates=["yoni = the four powers (Bhāskara)", "yoni = māyā (Kṣemarāja)"],
        is_open=True,
    ), "gold-exemplar-B", derived_from="T2")

    set_stage(r, stage_T3(
        resolved="The group of the sources is the body of the kalās.",
        open_flags=[{"flag": "LEX", "detail": "yoni-referent OPEN: the four powers (Bhāskara) vs māyā (Kṣemarāja)"}],
        editorial_notes=["yoni resolved to 'sources' (Bhāskara + anchor); the māyā reading kept as the OPEN alternate."],
    ), "gold-exemplar-B", derived_from="R2")

    set_stage(r, stage_T31(
        reading="The assembly of the sources is the body of the energies.",
    ), "gold-exemplar-B", derived_from="T3")

    set_stage(r, stage_C1(
        interpretation=("The sūtra says: what is 'down here' — the array of sources, "
                        "the powers — is not separate from the divine body. It is "
                        "the body of the kalās, the energies by which the absolute "
                        "structures itself into appearance. The 'sources' are the "
                        "goddesses/powers from which all manifestation flows; their "
                        "corporeal form is the layered energies themselves."),
        challenges=[],
    ), "gold-exemplar-B", derived_from="T3")

    return r


GOLD_EXEMPLARS = {
    "kramasadbhava.1.8": exemplar_kramasadbhava_1_8,
    "sivasutra.1.3": exemplar_sivasutra_1_3,
}


def all_exemplars() -> list[dict]:
    return [fn() for fn in GOLD_EXEMPLARS.values()]

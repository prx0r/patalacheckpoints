// C1 — Kramasadbhāva 1.8 (Milestone A2: the complete scholarly object).
//
// Written by the editor (main model) around the two rival sense assignments
// (data/corpus/annotations.ts). NOT machine-generated prose — this is the C1 layer
// that reviews the machine adjudication with evidence.
//
// The nirānanda question: R2 marked it CONSTRAINED = "O bliss-less one" (literal
// privative). External evidence (Mahānaya's "Bliss of Stillness"; nirācārānanda in
// Kubjikā material) suggests a technical sense. This C1 lays out both, the evidence,
// and a TranslationChallenge — WITHOUT mutating T3 (challenge is a proposal; a
// future R2/T3 v2 routes it).

export const c1_18 = {
  c1_id: "pt:c1:kramasadbhava:1.8:v1",
  passage_id: "pt:passage:kramasadbhava:1.8",
  derived_from_t3: "T3",
  evidence_state: "C1_EVIDENCE_PARTIAL",   // honest: external research not yet exhausted
  origin: "editor",
  status: "proposed",
  interpretation: `This verse opens the Kramasadbhāva's maṅgala as a vocative-chain
stuti: homage (namas / namo'stu te) is offered in sequence to the goddess as
devadeveśī ("mistress of the god of gods", the compound devadeva-īśī — the doubled
deva is the superlative "god of gods", and īśī "mistress" matches the kuleśī pattern
at 1.9), mahākālī, paramānande ("O supreme bliss"), and nirānande. The pair
paramānande / nirānande stands at the center, mirroring the polar nitye / tvanitye
("eternal / non-eternal") at 1.9 — the goddess transcends both poles of a pair.

The crux is nirānande. The morphology alone permits — even favors — the literal
privative "O bliss-less one" (nir- + ānanda, parallel to nirāmayaḥ at 1.6). R2 marked
this CONSTRAINED, and it is what the plain text most directly supports. But in a Krama
maṅgala this vocative is not merely a negation of bliss. External evidence is
material: the Mahānaya edition of this very verse renders nirānande as "the Bliss of
Stillness", and Dyczkowski-related Kubjikā material treats nirānanda as technical,
connected with nirācārānanda ("bliss of stillness"). The pairing with paramānande
then reads not as "supreme bliss / its absence" but as "supreme bliss / bliss at
rest" — two poles of one transcendent state, both beyond the ordinary opposition.
On this reading the R2 classification was overconfident: it is at least PREFERRED,
arguably OPEN, pending a specialist verdict on the technical sense.`,
  cruxes: [
    { crux_id: "c1", status: "lexical", summary: "nirānande: literal privative vs technical Krama sense" },
  ],
  evidence: [
    { id: "pt:annotation:krs:1.8:nirananda:privative", supports: "the literal 'bliss-less' reading (machine R1/R2)" },
    { id: "pt:annotation:krs:1.8:nirananda:technical", supports: "the technical 'bliss of stillness' reading (external evidence)" },
    { id: "pt:res:mahanaya-kramasadbhava", supports: "Mahānaya online edition renders 1.8 'the Bliss of Stillness'" },
    { id: "pt:res:kubjika-niracarananda", supports: "nirācārānanda 'bliss of stillness' in Kubjikā material" },
  ],
  open_questions: [
    "Does paramānande/nirānande as a polar pair force the privative, or does 'supreme bliss / bliss at rest' better fit the stuti's emission hierarchy?",
    "Is the technical 'stillness' sense attested in early Krama, or only in later Kubjikā development?",
  ],
  challenges: [
    {
      type: "TranslationChallenge",
      target: "T3 v1",
      crux: "nirānanda",
      current: "O bliss-less one",
      proposed: "O bliss at rest / O stillness (technical) — pending specialist evidence",
      evidence: ["pt:res:mahanaya-kramasadbhava", "pt:res:kubjika-niracarananda"],
      severity: "medium",
      status: "proposed",   // NOT applied — routes to a future R2/T3 v2
    },
  ],
  proposals: [
    {
      type: "TermSenseAssignment",
      claim: "nirānanda @ Kramasadbhāva 1.8: technical 'bliss of stillness' (Krama) vs privative 'bliss-less'",
      evidence: ["pt:annotation:krs:1.8:nirananda:technical"],
      status: "proposed",
      origin: "editor",
    },
    {
      type: "TermHistoryAssertion",
      claim: "nirānanda develops toward a technical transcendent sense in Krama/Kubjikā material",
      evidence: ["pt:res:kubjika-niracarananda"],
      status: "proposed",
      origin: "editor",
    },
  ],
};

// Gold eval fixtures — the regression gate for scholarly-graph quality.
//
// These are tiny, expert-reviewed expectations. When the pipeline/prompts/model
// change, we check: did we preserve the genuine ambiguity? did evidence IDs resolve?
// did an OPEN become CONSTRAINED? That is a useful regression gate (per the FoJin
// eval-machinery pattern and the nirānanda lesson).

export interface GoldDecision {
  id: string;
  passage: string;
  source_span: string;
  must_accept: string[];      // readings that are acceptable
  must_not: string[];         // failure modes / wrong claims
  required_uncertainty: boolean;  // the crux must remain OPEN/uncertain (not falsely settled)
  required_evidence_state: string;
  notes?: string;
}

export const goldDecisions: GoldDecision[] = [
  {
    id: "gold:ks:1.8:nirananda",
    passage: "pt:passage:kramasadbhava:1.8",
    source_span: "nirānande",
    must_accept: [
      "O bliss-less one (privative nir-+ānanda)",
      "O bliss at rest / stillness (technical Krama sense)",
    ],
    must_not: [
      "silently present one reading as globally settled",
      "downgrade the crux to CONSTRAINED without new decisive evidence",
      "drop the technical alternative without stating why",
    ],
    required_uncertainty: true,
    required_evidence_state: "partially_grounded",
    notes: "The nirānanda lesson: R2's CONSTRAINED was overconfident. The gold requires the crux to remain OPEN/uncertain until a specialist verdict or decisive evidence resolves it, and evidence_state must reflect that the technical reading is not yet fully verified.",
  },
  {
    id: "gold:ks:1.8:devadevesi",
    passage: "pt:passage:kramasadbhava:1.8",
    source_span: "devadeveśi",
    must_accept: ["O mistress of the god of gods (devadeva-īśī)", "queen of the gods (deva-deveśī)"],
    must_not: ["collapse the doubled-deva superlative without noting it"],
    required_uncertainty: false,
    required_evidence_state: "grounded",
    notes: "The compound is resolved (devadeva-īśī preferred) but the alternative is recorded; not an OPEN crux.",
  },
];

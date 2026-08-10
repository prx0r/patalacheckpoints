// The term ledger — accepted senses (data/terms.json) vs machine/human proposals
// (data/term_proposals.jsonl). Per EVIDENCE_POLICY: machine proposals NEVER
// promote themselves into accepted corpus knowledge; only review promotes.

import { readFileSync } from "fs";
import path from "path";

export interface TermSense {
  id: string;
  label: string;
  traditions?: string[];
  evidence?: string[];
}

export interface TermEntry {
  lemma: string;
  senses: TermSense[];
  preferred_renderings?: string[];
  avoid?: string[];
  notes?: string[];
}

export interface TermProposal {
  lemma: string;
  proposed_sense?: string;
  evidence?: string[];
  source?: string;
  status?: string;
  created_by?: { kind?: string; id?: string };
  created_at?: string;
}

const TERMS_FILE = path.join(process.cwd(), "data", "terms.json");
const PROPOSALS_FILE = path.join(process.cwd(), "data", "term_proposals.jsonl");

let _terms: TermEntry[] | null = null;
let _proposals: TermProposal[] | null = null;

function loadTerms(): TermEntry[] {
  if (_terms) return _terms;
  try {
    _terms = JSON.parse(readFileSync(TERMS_FILE, "utf8")).terms as TermEntry[];
  } catch {
    _terms = [];
  }
  return _terms;
}

function loadProposals(): TermProposal[] {
  if (_proposals) return _proposals;
  const out: TermProposal[] = [];
  try {
    for (const line of readFileSync(PROPOSALS_FILE, "utf8").split("\n")) {
      if (line.trim()) out.push(JSON.parse(line) as TermProposal);
    }
  } catch {
    // no proposals yet
  }
  _proposals = out;
  return out;
}

export function getTerm(lemma: string): TermEntry | undefined {
  return loadTerms().find((t) => t.lemma === lemma);
}

export function getTerms(): TermEntry[] {
  return loadTerms();
}

export function getProposals(lemma?: string): TermProposal[] {
  const p = loadProposals();
  return lemma ? p.filter((x) => x.lemma === lemma) : p;
}

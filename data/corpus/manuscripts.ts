// The manuscript witness layer — OCHS manuscript metadata, resolved to our works.
// We adopt OCHS's own field names (drop-in compatibility); provenance preserved
// (custodian OCHS, CC BY-NC-SA 4.0, source_url). We add nothing that duplicates
// OCHS; we only resolve their records against our work authority graph.

import { readFileSync } from "fs";
import path from "path";

export interface Manuscript {
  id: string; // pt:ms:{ochs_slug}
  ochs_slug: string;
  custodian: string;
  licence: string;
  source_url: string;
  photos: boolean;
  text: boolean;
  title?: string;
  titleIndic?: string;
  titleTranslation?: string;
  alternateTitles?: string;
  author?: string;
  language?: string;
  script?: string;
  provenanceCategory?: string;
  provenanceNote?: string;
  repository?: string;
  catalogueIds?: string; // NAK / NGMPP
  externalMetadata?: string;
  dateOriginal?: string;
  dateCopy?: string;
  place?: string;
  material?: string;
  condition?: string;
  folios?: string;
  tradition?: string;
  incipit?: string;
  explicit?: string;
  colophon?: string;
  translations?: string;
  secondaryLiterature?: string;
  remarks?: string;
  raw?: Record<string, string | null>;
}

// Curated OCHS slug -> work_id resolution (a manuscript witness of a work).
// Hand-curated to avoid title-token false positives (e.g. Makutottararahasya is
// NOT Tārārahasya). Extend as more works are covered.
const RESOLUTION: Record<string, string[]> = {
  netratantra: ["ochs_000_000_002_amrtesatantram", "ochs_000_000_024_netratantra_ksemeraja_commentary", "ochs_000_000_025_mrtyujidamrtesatantra", "ochs_000_000_074_amrtesatantra", "ochs_000_000_286_netratantra_netratantra_with_c"],
  kiranatantra: ["ochs_000_000_011_kiranatantra", "ochs_000_000_038_kiranatantra_1_6_with_the_com"],
  mrgendragama: ["ochs_000_000_042_mrgendragama_mrgendratantra", "ochs_000_000_267_mrgendragama_mrgendragama_with", "ochs_000_001_096_mrgendragamavrtti"],
  kubjikamata: ["ochs_000_000_039_kubjikamatatantra"],
  malinivijayottara: ["ochs_000_000_040_malinivijayottaratantra", "ochs_000_000_255_malinivijayottaratantra_malini"],
  tantraloka: ["ochs_000_000_398_tantraloka_chapters_1_thru_14", "ochs_000_000_399_tantraloka_chapters_15_thru_38"],
  sivasutra: ["ochs_000_000_056_sivasutra_with_varttika", "ochs_000_000_508_sivasutravarttika", "ochs_000_000_509_sivasutravimarsini_text_versio", "ochs_000_001_085_sivasutrani", "ochs_000_001_086_sivasutravartikam"],
  spandakarika: ["ochs_000_000_383_spandakarika_with_vivrtti_by_r", "ochs_000_000_384_spandakarika", "ochs_000_000_385_spandanirnaya_spandakarika_wit"],
  vijnanabhairava: ["ochs_000_000_447_vijnanabhairava_with_commentar", "ochs_000_000_448_vijnanabhairava"],
  svacchandatantra: ["ochs_000_000_049_svacchandatantra_or_svacchand", "ochs_000_000_394_svacchandatantra_svacchandatan"],
  cidgaganacandrika: ["ochs_000_000_112_cidgaganacandrika"],
  jnanakarika: ["ochs_000_000_168_jnanakarika"],
  kaulajnananirnaya: ["ochs_000_000_198_kaulajnananirnaya_kaulajnanani"],
  brahmayamala: ["ochs_000_000_105_brahmayamala"],
  akulaviratantra: ["ochs_000_000_071_akulaviratantra_akulaviratantr"],
  ajadapramatrsiddhi: ["ochs_000_000_068_ajadapramatrsiddhi", "ochs_000_000_069_ajadapramatrsiddhih"],
  pratyabhijnahrdaya: ["ochs_000_000_333_pratyabhijnahrdaya_text_versio"],
  kalanalatantra: ["ochs_000_000_179_kalanalatantra"],
  tararahasya: ["ochs_000_000_404_tararahasya", "ochs_000_000_405_tararahasyavrtti_2", "ochs_000_000_406_tararahasyavrttika"],
  yoginihrdaya: ["ochs_000_000_478_yoginihrdaya_yoginihrdaya_with"],
};

const FILE = path.join(process.cwd(), "data", "manuscripts.json");
let _index: Manuscript[] | null = null;
let _bySlug: Map<string, Manuscript> | null = null;

function load(): Manuscript[] {
  if (_index) return _index;
  try {
    _index = JSON.parse(readFileSync(FILE, "utf8")) as Manuscript[];
  } catch {
    _index = [];
  }
  _bySlug = new Map(_index.map((m) => [m.ochs_slug, m]));
  return _index;
}

export function getManuscripts(): Manuscript[] {
  return load();
}

export function getManuscript(ochsSlug: string): Manuscript | undefined {
  load();
  return _bySlug?.get(ochsSlug);
}

// Resolve a work's OCHS manuscript witnesses.
export function manuscriptsForWork(workId: string): Manuscript[] {
  const slugs = RESOLUTION[workId] ?? [];
  return slugs.map((s) => getManuscript(s)).filter((m): m is Manuscript => Boolean(m));
}

// Reverse index: which of OUR works does an OCHS record witness?
export function workForManuscript(ochsSlug: string): string[] {
  return Object.entries(RESOLUTION).filter(([, slugs]) => slugs.includes(ochsSlug)).map(([w]) => w);
}

export function workManuscriptCounts(): Record<string, number> {
  const out: Record<string, number> = {};
  for (const wid of Object.keys(RESOLUTION)) out[wid] = manuscriptsForWork(wid).length;
  return out;
}

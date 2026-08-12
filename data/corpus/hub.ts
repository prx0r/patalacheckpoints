// hub.ts — the source-centric hub: every primary source lists ALL its derived outputs.
//
// The organizing idea: a primary source is a HUB, not a file. Each work tracks its
// translations, essays, logical arguments, pushing-enquiries, and learning — all tied
// to the passage IDs and the source registry. Agnostic: the same shape works for IPVV,
// Tantrāloka, IPK, Kubjikā, a Buddhist text, or a ritual manual.
//
// This is the graph-level view that the bibliography (what exists) and the passages
// (the reading) extend to "every output this source spawned."
//
// Seed: the IPVV + Tantrāloka pushing/essay/argument resources from research-library.

export type HubOutputKind = "essay" | "logical_argument" | "pushing" | "learning";

export interface HubOutput {
  id: string;            // pt:hub:<work>:<kind>:<slug>
  kind: HubOutputKind;
  title: string;
  file: string;          // the on-disk path (research-library / truth / docs)
  work_id: string;       // the primary source it belongs to
  passage_ids?: string[]; // the passages it cites/draws on
  summary?: string;
  status: "seed" | "draft" | "reviewed";
}

export interface WorkHub {
  work_id: string;
  label: string;
  outputs: HubOutput[];
}

const HUB: WorkHub[] = [
  {
    work_id: "isvarapratyabhijnavivrtivimarsini",
    label: "IPVV — Abhinavagupta's Vivṛtivimarśinī",
    outputs: [
      // PUSHING enquiry (the mechanical deep-dive method)
      { id: "pt:hub:ipvv:pushing:main", kind: "pushing", title: "PUSHING-IPVV (Logicvid method)",
        file: "research-library/recognition/pushing-ipvv/PUSHING-IPVV.md", work_id: "isvarapratyabhijnavivrtivimarsini", status: "seed" },
      // The IPVV essay family (recognition library)
      { id: "pt:hub:ipvv:essay:vs-tantraloka", kind: "essay", title: "IPVV vs Tantrāloka",
        file: "research-library/recognition/ESSAY-IPVV-VS-TANTRALOKA.md", work_id: "isvarapratyabhijnavivrtivimarsini", status: "seed" },
      { id: "pt:hub:ipvv:essay:sivasutra-vb", kind: "essay", title: "Śivasūtra / Vijñānabhairava / IPVV",
        file: "research-library/recognition/ESSAY-SIVASUTRA-VB-IPVV.md", work_id: "isvarapratyabhijnavivrtivimarsini", status: "seed" },
      { id: "pt:hub:ipvv:essay:buddhist", kind: "essay", title: "IPVV and the Buddhist",
        file: "research-library/recognition/ESSAY-BUDDHIST-IPVV.md", work_id: "isvarapratyabhijnavivrtivimarsini", status: "seed" },
      { id: "pt:hub:ipvv:essay:spanda", kind: "essay", title: "IPVV and Spanda",
        file: "research-library/recognition/ESSAY-SPANDA-IPVV.md", work_id: "isvarapratyabhijnavivrtivimarsini", status: "seed" },
      { id: "pt:hub:ipvv:essay:two-abhinavaguptas", kind: "essay", title: "The Two Abhinavaguptas (IPVV/TĀ)",
        file: "research-library/recognition/ESSAY-TWO-ABHINAVAGUPTAS-IPVV-TANTRALOKA.md", work_id: "isvarapratyabhijnavivrtivimarsini", status: "seed" },
      { id: "pt:hub:ipvv:essay:advaita", kind: "essay", title: "IPVV and Advaita",
        file: "research-library/recognition/ESSAY-ADVAITA-IPVV.md", work_id: "isvarapratyabhijnavivrtivimarsini", status: "seed" },
      { id: "pt:hub:ipvv:essay:krama", kind: "essay", title: "IPVV and Krama",
        file: "research-library/recognition/ESSAY-KRAMA-IPVV.md", work_id: "isvarapratyabhijnavivrtivimarsini", status: "seed" },
      { id: "pt:hub:ipvv:essay:rasa", kind: "essay", title: "IPVV and Rasa (Abhinavabhāratī)",
        file: "research-library/recognition/ESSAY-RASA-IPVV-ABHINAVABHARATI.md", work_id: "isvarapratyabhijnavivrtivimarsini", status: "seed" },
      // LOGICAL ARGUMENTS (the gold)
      { id: "pt:hub:ipvv:argument:reflexivity", kind: "logical_argument", title: "The Reflexivity Debate (formal argument)",
        file: "research-library/LOGICAL-ARGUMENT-1-reflexivity-debate.md", work_id: "isvarapratyabhijnavivrtivimarsini", status: "seed" },
      { id: "pt:hub:ipvv:argument:nanavira", kind: "logical_argument", title: "Reflexion-proof vs IPK 1.5.11 (Ñāṇavīra)",
        file: "research-library/LOGICAL-ARGUMENT-NANAVIRA.md", work_id: "isvarapratyabhijnavivrtivimarsini", status: "seed" },
    ],
  },
  {
    work_id: "tantraloka",
    label: "Tantrāloka — Abhinavagupta's great synthesis",
    outputs: [
      { id: "pt:hub:tantraloka:pushing:main", kind: "pushing", title: "PUSHING-TANTRALOKA (Logicvid method)",
        file: "research-library/recognition/pushing-tantraloka/PUSHING-TANTRALOKA.md", work_id: "tantraloka", status: "seed" },
    ],
  },
];

export function hubFor(workId: string): WorkHub | undefined {
  return HUB.find((h) => h.work_id === workId);
}

export function outputsFor(workId: string, kind?: HubOutputKind): HubOutput[] {
  const hub = hubFor(workId);
  if (!hub) return [];
  return kind ? hub.outputs.filter((o) => o.kind === kind) : hub.outputs;
}

export function allHubs(): WorkHub[] {
  return HUB;
}

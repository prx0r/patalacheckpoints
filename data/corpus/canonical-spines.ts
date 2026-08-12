// canonical-spines.ts — the ordered reading spine per school, tied to the bibliography.
//
// A canonical spine is the ordered set of works that define a school's reading path:
//   ROOT SCRIPTURE → COMMENTARY → SYNTHESIS (→ our working translation).
// Each spine step points to a bibliography record (data/atlas/bibliographySeed.ts) and a
// role. This is what lets an agent research the "related 5 works" of a school as ONE
// navigable object, directly tied to the bibliography.
//
// Roles (aligned with the editorial relation kinds in the platform spec):
//   root_scripture  the school's foundational text (e.g. IPK for Pratyabhijñā)
//   commentary      a commentary/auto-commentary on the root
//   synthesis       a later synthesis/exposition of the school's doctrine
//   target          our working translation (e.g. the IPVV — what we are publishing)
//   parallel        a parallel work in the same school (for comparison)
//   anchor          a published scholarly translation used as verification

export interface SpineStep {
  work_id: string;        // bibliography record id (isvarapratyabhijnakarika, ...)
  role: "root_scripture" | "commentary" | "synthesis" | "target" | "parallel" | "anchor";
  order: number;          // reading order within the spine
  note?: string;          // why this step matters
}

export interface CanonicalSpine {
  tradition: string;      // tradition id (pratyabhijna, trika, spanda, ...)
  label: string;          // display label
  summary: string;        // one-line account of the school's reading path
  steps: SpineStep[];
}

export const canonicalSpines: CanonicalSpine[] = [
  {
    tradition: "pratyabhijna",
    label: "Recognition (Pratyabhijñā)",
    summary:
      "The recognition spine: Utpaladeva's root kārikā + Vṛtti, the (mostly lost) Vivṛti, Abhinavagupta's shorter Vimarśinī and the great Vivṛtivimarśinī (our target), with Kṣemarāja's Hṛdaya as the accessible epitome and the Śivadṛṣṭi as the doctrinal anchor.",
    steps: [
      { work_id: "sivadrstivrtti", role: "anchor", order: 0, note: "Somānanda's Śivadṛṣṭi + Vṛtti — the doctrinal source of the recognition thesis." },
      { work_id: "isvarapratyabhijnakarika", role: "root_scripture", order: 1, note: "IPK + Vṛtti — the root verses + author's explanation. Our GRETIL copy is the machine base." },
      { work_id: "isvarapratyabhijnavivrtti", role: "commentary", order: 2, note: "The mostly-lost Vivṛti; Ratié's recovery work reconstructs its fragments from the IPVV's margins." },
      { work_id: "isvarapratyabhijnavimarsini", role: "commentary", order: 3, note: "Abhinavagupta's shorter Vimarśinī (Pandey's Bhāskarī = English)." },
      { work_id: "isvarapratyabhijnavivrtivimarsini", role: "target", order: 4, note: "OUR WORK — the great Vivṛtivimarśinī, the #1 untranslated Abhinavagupta work." },
      { work_id: "pratyabhijnahrdaya", role: "synthesis", order: 5, note: "Kṣemarāja's Pratyabhijñāhṛdaya — the accessible epitome of the recognition doctrine." },
      { work_id: "sivastotravali", role: "parallel", order: 6, note: "Utpaladeva's devotional poems — the bhakti register of the same recognition." },
    ],
  },
  {
    tradition: "trika",
    label: "Trika",
    summary:
      "The Trika spine: the Tantrāloka as the great synthesis, with its doctrinal vocabulary (prakāśa-vimarśa, anuttara, kula/akula) as the Rosetta layer for the whole corpus.",
    steps: [
      { work_id: "malinivijayottara", role: "root_scripture", order: 0, note: "The Mālinīvijayottaratantra (Vasudeva's study = the anchor) — the Trika's revealed base." },
      { work_id: "tantraloka", role: "synthesis", order: 1, note: "Abhinavagupta's Tantrāloka + Jayaratha's Viveka (Dyczkowski 11 vols = the anchor)." },
    ],
  },
  {
    tradition: "spanda",
    label: "Spanda",
    summary:
      "The Spanda spine: the Spandakārikā root with its four commentaries, and the dynamic-pulse register that feeds the Pratyabhijñā.",
    steps: [
      { work_id: "spandakarika", role: "root_scripture", order: 0, note: "The Stanzas on Vibration (Dyczkowski's translation with four commentaries = the anchor)." },
    ],
  },
  {
    tradition: "krama",
    label: "Krama",
    summary:
      "The Krama spine: the Kālī-sequence of cognition, from the Mahānayaprakāśa to the Mahārthamañjarī.",
    steps: [
      { work_id: "mahanayaprakasha", role: "synthesis", order: 0, note: "The Krama crown — the daśākhaṇḍa and the cognition-sequence." },
      { work_id: "maharthamanjari", role: "commentary", order: 1, note: "Maheśvarānanda's 70-gāthā with the Parimala." },
    ],
  },
];

export function spineFor(tradition: string): CanonicalSpine | undefined {
  return canonicalSpines.find((s) => s.tradition === tradition);
}

export function spineForWork(workId: string): CanonicalSpine | undefined {
  return canonicalSpines.find((s) => s.steps.some((st) => st.work_id === workId));
}

export function allSpines(): CanonicalSpine[] {
  return canonicalSpines;
}

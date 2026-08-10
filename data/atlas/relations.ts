import { AtlasRelation } from "@/lib/atlas";

// The edges. Relations are separate from entities — history is not a family
// tree. Each edge is typed and confidence-weighted, populated from the
// reference map's influence graph and our own research.
//
// Edge-types: develops-from · textual-borrowing · influence · synthesis ·
// commentary · contains · conceptual-parallel
//
// Confidence: established · strong · possible

export const relations: AtlasRelation[] = [
  // ---- Traditions ←→ Traditions ----
  {
    source: "kaula",
    target: "trika",
    type: "influence",
    confidence: "strong",
    evidence: ["Sanderson: the Kaula reformulation of the Yoginī-cult produced the Pūrvāmnāya/Kaula Trika"],
  },
  {
    source: "kubjika",
    target: "trika",
    type: "textual-borrowing",
    confidence: "strong",
    evidence: ["Sanderson: parts of the Kubjikāmata are close reworkings of the earlier Trika corpus"],
  },
  {
    source: "krama",
    target: "trika",
    type: "influence",
    confidence: "strong",
    evidence: ["Sanderson: Krama doctrine and ritual deeply influenced Abhinava's Trika"],
  },
  {
    source: "spanda",
    target: "trika",
    type: "influence",
    confidence: "strong",
    evidence: ["the Spanda current supplied the dynamism-language of the synthesis"],
  },
  {
    source: "pratyabhijna",
    target: "trika",
    type: "influence",
    confidence: "established",
    evidence: ["Somānanda → Utpaladeva → Lakṣmaṇagupta → Abhinavagupta (TĀ 1.8–1.12)"],
  },
  {
    source: "krama",
    target: "kubjika",
    type: "influence",
    confidence: "possible",
    evidence: ["the later Western-tradition works appropriate and hierarchize Krama (Sanderson)"],
  },
  {
    source: "kubjika",
    target: "sarvamnyaya",
    type: "synthesis",
    confidence: "strong",
    evidence: ["the Nepalese multi-āmnāya systems combine Kubjikā with Kālī, Tripurā and others"],
  },
  {
    source: "krama",
    target: "sarvamnyaya",
    type: "synthesis",
    confidence: "strong",
    evidence: ["the Kālī-tradition flows into the Newar Sarvāmnāya syntheses"],
  },

  // ---- Texts ←→ Traditions ----
  { source: "tantraloka", target: "trika", type: "contains", confidence: "established" },
  { source: "mahanayaprakasha", target: "krama", type: "contains", confidence: "established" },
  { source: "maharthamanjari", target: "krama", type: "contains", confidence: "established" },
  { source: "kubjikamata", target: "kubjika", type: "contains", confidence: "established" },
  { source: "kaulajnananirnaya", target: "kaula", type: "contains", confidence: "established" },
  { source: "spandakarika", target: "spanda", type: "contains", confidence: "established" },

  // ---- Texts ←→ People ----
  { source: "tantraloka", target: "abhinavagupta", type: "develops-from", confidence: "established" },
  { source: "tantraloka", target: "jayaratha", type: "commentary", confidence: "established" },
  { source: "mahanayaprakasha", target: "jnananetra", type: "develops-from", confidence: "strong" },
  { source: "maharthamanjari", target: "maheshvarananda", type: "develops-from", confidence: "established" },
  { source: "spandakarika", target: "jnananetra", type: "develops-from", confidence: "possible" },

  // ---- People ←→ People ----
  { source: "utpaladeva", target: "somananda", type: "develops-from", confidence: "established" },
  { source: "abhinavagupta", target: "utpaladeva", type: "develops-from", confidence: "established" },
  { source: "jayaratha", target: "abhinavagupta", type: "commentary", confidence: "established" },

  // ---- Concepts ←→ Traditions ----
  { source: "kula", target: "kaula", type: "conceptual-parallel", confidence: "strong" },
  { source: "kula", target: "kubjika", type: "conceptual-parallel", confidence: "strong" },
  { source: "kula", target: "trika", type: "conceptual-parallel", confidence: "strong" },
  { source: "krama", target: "krama", type: "conceptual-parallel", confidence: "established" },
  { source: "recognition", target: "pratyabhijna", type: "conceptual-parallel", confidence: "established" },
  { source: "spanda", target: "spanda", type: "conceptual-parallel", confidence: "established" },
  { source: "vimarśa", target: "pratyabhijna", type: "conceptual-parallel", confidence: "established" },
  { source: "mālinī", target: "kubjika", type: "conceptual-parallel", confidence: "established" },

  // ---- Texts ←→ Concepts ----
  { source: "tantraloka", target: "kula", type: "contains", confidence: "established" },
  { source: "tantraloka", target: "krama", type: "contains", confidence: "strong" },
  { source: "maharthamanjari", target: "spanda", type: "contains", confidence: "established" },
  { source: "maharthamanjari", target: "krama", type: "contains", confidence: "established" },
  { source: "kubjikamata", target: "mālinī", type: "contains", confidence: "established" },
  { source: "kubjikamata", target: "kula", type: "contains", confidence: "strong" },
  { source: "spandakarika", target: "spanda", type: "contains", confidence: "established" },
  { source: "kaulajnananirnaya", target: "kula", type: "contains", confidence: "established" },

  // ---- People ←→ Concepts ----
  { source: "abhinavagupta", target: "recognition", type: "conceptual-parallel", confidence: "established" },
  { source: "utpaladeva", target: "recognition", type: "conceptual-parallel", confidence: "established" },
  { source: "maheshvarananda", target: "krama", type: "conceptual-parallel", confidence: "established" },
  { source: "maheshvarananda", target: "spanda", type: "conceptual-parallel", confidence: "strong" },

  // ---- The Dyczkowski effect (the curation edge) ----
  { source: "dyczkowski", target: "kubjika", type: "influence", confidence: "strong", evidence: ["his Muktabodha selection concentrated the Kubjikā corpus"] },
  { source: "dyczkowski", target: "krama", type: "influence", confidence: "possible" },

// ---- The 2026-08-09 additions: new T3'd texts + the 24-lemma dossiers ----

// Texts ←→ Traditions
{ source: "jnanakarika", target: "kaula", type: "contains", confidence: "established" },
{ source: "ajadapramatrsiddhi", target: "pratyabhijna", type: "contains", confidence: "established" },
{ source: "kaularahasya", target: "kaula", type: "contains", confidence: "established" },
{ source: "kulapradipa", target: "kaula", type: "contains", confidence: "established" },
{ source: "kubjikatantra", target: "kubjika", type: "contains", confidence: "established" },
{ source: "sivasutra", target: "trika", type: "contains", confidence: "established" },

// Texts ←→ People
{ source: "ajadapramatrsiddhi", target: "utpaladeva", type: "develops-from", confidence: "established" },
{ source: "jnanakarika", target: "jnananetra", type: "develops-from", confidence: "possible" },

// Texts ←→ Concepts (the dossier-loci)
{ source: "ajadapramatrsiddhi", target: "recognition", type: "contains", confidence: "established" },
{ source: "ajadapramatrsiddhi", target: "vimarśa", type: "contains", confidence: "established" },
{ source: "jnanakarika", target: "śūnya", type: "contains", confidence: "strong" },
{ source: "jnanakarika", target: "kula", type: "contains", confidence: "strong" },
{ source: "kaularahasya", target: "cakra", type: "contains", confidence: "strong" },
{ source: "kaularahasya", target: "mantra", type: "contains", confidence: "strong" },
{ source: "kulapradipa", target: "kula", type: "contains", confidence: "strong" },
{ source: "kubjikatantra", target: "mālinī", type: "contains", confidence: "strong" },
{ source: "sivasutra", target: "mātṛkā", type: "contains", confidence: "established" },
{ source: "sivasutra", target: "śakti", type: "contains", confidence: "established" },

// Concepts ←→ Traditions (the 24-lemma dossiers)
{ source: "saṃvit", target: "krama", type: "conceptual-parallel", confidence: "established" },
{ source: "saṃvit", target: "spanda", type: "conceptual-parallel", confidence: "strong" },
{ source: "akula", target: "trika", type: "conceptual-parallel", confidence: "established" },
{ source: "akula", target: "kubjika", type: "conceptual-parallel", confidence: "strong" },
{ source: "parāmarśa", target: "pratyabhijna", type: "conceptual-parallel", confidence: "established" },
{ source: "prakāśa", target: "trika", type: "conceptual-parallel", confidence: "established" },
{ source: "prakāśa", target: "pratyabhijna", type: "conceptual-parallel", confidence: "established" },
{ source: "visarga", target: "trika", type: "conceptual-parallel", confidence: "established" },
{ source: "visarga", target: "kaula", type: "conceptual-parallel", confidence: "strong" },
{ source: "anuttara", target: "trika", type: "conceptual-parallel", confidence: "established" },
{ source: "mātṛkā", target: "kubjika", type: "conceptual-parallel", confidence: "established" },
{ source: "mātṛkā", target: "trika", type: "conceptual-parallel", confidence: "established" },
{ source: "svātantrya", target: "pratyabhijna", type: "conceptual-parallel", confidence: "established" },
{ source: "svātantrya", target: "spanda", type: "conceptual-parallel", confidence: "strong" },
{ source: "āveśa", target: "trika", type: "conceptual-parallel", confidence: "strong" },
{ source: "uccāra", target: "trika", type: "conceptual-parallel", confidence: "strong" },
{ source: "vyāpti", target: "trika", type: "conceptual-parallel", confidence: "strong" },
{ source: "śūnya", target: "krama", type: "conceptual-parallel", confidence: "strong" },
{ source: "śūnya", target: "trika", type: "conceptual-parallel", confidence: "strong" },
{ source: "saṃhāra", target: "spanda", type: "conceptual-parallel", confidence: "established" },
{ source: "cakra", target: "trika", type: "conceptual-parallel", confidence: "established" },
{ source: "cakra", target: "kaula", type: "conceptual-parallel", confidence: "strong" },
{ source: "mantra", target: "kubjika", type: "conceptual-parallel", confidence: "established" },
{ source: "mantra", target: "trika", type: "conceptual-parallel", confidence: "established" },

// Concept ↔ concept (the internal links)
{ source: "prakāśa", target: "vimarśa", type: "conceptual-parallel", confidence: "established" },
{ source: "saṃvit", target: "vimarśa", type: "conceptual-parallel", confidence: "strong" },
{ source: "akula", target: "kula", type: "conceptual-parallel", confidence: "established" },
{ source: "anuttara", target: "akula", type: "conceptual-parallel", confidence: "established" },
{ source: "mālinī", target: "mātṛkā", type: "conceptual-parallel", confidence: "established" },
{ source: "mantra", target: "uccāra", type: "conceptual-parallel", confidence: "strong" },

// The newly-translated Krama texts (2026-08-09)
{ source: "cidgaganacandrika", target: "krama", type: "contains", confidence: "established" },
{ source: "cidgaganacandrika", target: "khecarī", type: "contains", confidence: "established" },
{ source: "cidgaganacandrika", target: "prakāśa", type: "conceptual-parallel", confidence: "established" },
{ source: "cidgaganacandrika", target: "śūnya", type: "conceptual-parallel", confidence: "strong" },
{ source: "kakacandeshvarimata", target: "krama", type: "contains", confidence: "established" },
{ source: "kakacandeshvarimata", target: "khecarī", type: "conceptual-parallel", confidence: "strong" },
{ source: "kakacandeshvarimata", target: "cakra", type: "conceptual-parallel", confidence: "strong" },
{ source: "nitya_shodasikarnava", target: "krama", type: "contains", confidence: "established" },
{ source: "nitya_shodasikarnava", target: "cakra", type: "conceptual-parallel", confidence: "established" },
{ source: "nitya_shodasikarnava", target: "mantra", type: "conceptual-parallel", confidence: "established" },
{ source: "nitya_shodasikarnava", target: "yoginīhṛdaya", type: "commentary", confidence: "established", evidence: ["the Cambridge MS-OR-00156: the Nityāṣoḍaśikārṇava is the Vāmakeśvara's first part, the Yoginīhṛdaya the second"] },
{ source: "khecarī", target: "śakti", type: "conceptual-parallel", confidence: "established" },
{ source: "khecarī", target: "spanda", type: "conceptual-parallel", confidence: "strong" },
];

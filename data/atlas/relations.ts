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
];

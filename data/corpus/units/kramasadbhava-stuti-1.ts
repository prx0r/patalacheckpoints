// The kramasadbhāva stuti-1 research unit — the first Milestone B object.
// Kramasadbhāva 1.1–1.28: the opening stuti (hymn) of the Goddess. See
// docs/SCHOLARLY_GRAPH.md for the object model.
import type { UnitObject } from "../graph";

export const kramasadbhavaStuti1: UnitObject = {
  id: "pt:unit:kramasadbhava:stuti-1",
  type: "unit",
  work: "pt:work:kramasadbhava",
  titles: ["Kramasadbhāva 1.1–1.28 — the opening stuti"],
  range: { chapter: 1, verses: "1.1–1.28" },
  genre: "stuti",
  structure:
    "vocative-chain stuti of the Goddess; body-locus sequence (brahmadvāra → kaṇṭha → tālu → hṛtpadma → dvādaśānta/ṣoḍaśānta → kanda/kauṇḍalya); emission hierarchy (visarga → nāda → bindu); the four states (jāgrat/svapna/suṣupti/turyā at 1.26). The stuti closes at 1.28 ('etat stutipadaṃ kṛtvā'); 1.29 opens the dialogue (śrībhairava uvāca).",
  term_families: ["ānanda", "kālī", "kula", "krama", "body-loci", "bindu-nāda-visarga", "śūnya-vyāpti"],
  known_cruxes: ["nirānande 1.8 (privative vs technical Krama sense)"],
  passages: Array.from({ length: 28 }, (_, i) => `pt:passage:kramasadbhava:1.${i + 1}`),
};

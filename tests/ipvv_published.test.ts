// Tests for the lazy-JSON IPVV publication (Phase 1).
//
// Invariants under test:
//   1. a V1, V2, and V3 passage each lazy-load (reader + resolve share ONE object)
//   2. a bad locator returns undefined (→404), never silent fallback
//   3. resolve-immutable returns the store's canonical immutable id
//   4. reader and resolver agree: getPublishedTranslation(immutable) == the passage
//
// Run: npx tsx tests/ipvv_published.test.ts   (or via the test runner)

import { getPublishedTranslation, ipvvResolveImmutable, ipvvPassageCount } from "../data/corpus/published";

let failures = 0;
function check(name: string, cond: boolean, detail = "") {
  if (cond) console.log(`  ✓ ${name}`);
  else { console.log(`  ✗ ${name} ${detail}`); failures++; }
}

console.log("IPVV lazy-JSON publication tests");
console.log(`  total passages: ${ipvvPassageCount()}`);

// V1 / V2 / V3 passages (chunk names in the phase-1 store)
const V1 = "chunkA-svatyandya.md";
const V2 = "chunkV2-A-caturtho-vimarsa-aham.md";
const V3 = "chunkV3-C-kriya-trtiyo-k1-2.md";

for (const [label, locator] of [["V1", V1], ["V2", V2], ["V3", V3]]) {
  const imm = ipvvResolveImmutable(locator);
  check(`${label}: resolve-immutable returns a value`, !!imm);
  const pub = getPublishedTranslation(imm!);
  check(`${label}: loads by immutable id`, !!pub, `imm=${imm}`);
  check(`${label}: has L2 text`, Boolean(pub?.text));
  check(`${label}: has a source span`, (pub?.source_spans?.length ?? 0) >= 1);
  check(`${label}: has provenance`, Boolean(pub?.provenance?.edition));
  check(`${label}: reader+resolver agree on id`, pub?.passage_id === `pt:passage:ipvv:${locator}`);
}

// bad locator
check("bad locator → undefined", getPublishedTranslation("pt:passage:ipvv:nonexistent.md") === undefined);
check("bad immutable → undefined", ipvvResolveImmutable("totally-bogus-key") === undefined);

// immutable-ID resolve: resolving a locator then loading by its immutable id works
const immV3 = ipvvResolveImmutable(V3);
const byImm = getPublishedTranslation(immV3!);
check("immutable-ID resolve returns the same passage", byImm?.passage_id === `pt:passage:ipvv:${V3}`);

console.log(failures === 0 ? "\nALL PASS" : `\n${failures} FAILURES`);
process.exit(failures === 0 ? 0 : 1);

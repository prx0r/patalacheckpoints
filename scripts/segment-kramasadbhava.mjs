// Segment a clean IAST e-text into verse-anchored passages with stable IDs.
// Usage: node scripts/segment-kramasadbhava.mjs <src.txt> <out.jsonl>
// Dyczkowski/Muktabodha format: a verse's text precedes its `||ch/verse` marker
// (marker format varies: `||1/1`, `||1/ 2 ||`). Bare `||` and `* * *` are junk.

import { readFileSync, writeFileSync } from "fs";

const src = process.argv[2];
const out = process.argv[3];
if (!src || !out) {
  console.error("usage: node scripts/segment-kramasadbhava.mjs <src.txt> <out.jsonl>");
  process.exit(1);
}

const WORK_ID = "kramasadbhava";
const EDITION = "Dyczkowski ed., Muktabodha (MS 1-76 Saivatantra 144; NGMPP A 209/23)";

const raw = readFileSync(src, "utf8");
const lines = raw.split(/\r?\n/);

let bodyStart = 0;
for (let i = 0; i < lines.length; i++) {
  if (lines[i].includes("Encoded in Velthius transliteration")) {
    bodyStart = i + 1;
    break;
  }
}

const MARKER = /\|\|\s*(\d+)\s*\/\s*(\d+)/; // finds "||ch/verse" anywhere in the line
// A colophon (e.g. "prathamaḥ paṭalaḥ ||1/1 ||") is NOT a verse boundary — it
// carries the same ch/verse number as the last real verse. Exclude those lines.
const IS_COLOPHON = /paṭalaḥ|patalaḥ|iti śrī/i;

const passages = [];
const seen = new Set();
let cur = [];

for (const line of lines.slice(bodyStart)) {
  const t = line.trim();
  if (!t) continue;

  const m = t.match(MARKER);
  if (m && !IS_COLOPHON.test(t)) {
    const ch = parseInt(m[1], 10);
    const vs = parseInt(m[2], 10);
    const lineText = t.slice(0, m.index).replace(/\|+$/, "").trim();
    const text = [...cur, lineText].join(" ").replace(/\s+/g, " ").trim();
    const id = `tantra:text:${WORK_ID}:${ch}.${vs}`;
    if (text && !seen.has(id)) {
      seen.add(id);
      passages.push({
        id,
        work_id: WORK_ID,
        location: { chapter: ch, verse: vs },
        sanskrit: text,
        source_edition: EDITION,
      });
    }
    cur = [];
    continue;
  }

  if (/^[|*\s]+$/.test(t)) {
    cur = [];
    continue;
  }
  cur.push(t.replace(/^\*+/, "").replace(/\|+$/, "").trim());
}

writeFileSync(out, passages.map((p) => JSON.stringify(p)).join("\n") + "\n", "utf8");
console.log(`wrote ${passages.length} passages -> ${out}`);

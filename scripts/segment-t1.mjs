// Segment our T1/T2/T3 markdown into verse-anchored passages.
// Handles the house layouts:
//   A) "**ch/verse** — {SANSKRIT}"  then  "> — {translation} —"      (kramasadbhava, kulasara, kubjikamata)
//   B) "**10/1**" (own line) then {SANSKRIT} then "> {translation}"
//   C) "**1** — {SANSKRIT}" then "> {translation}"                   (verse-only: mahanayaprakasha, cidgaganacandrika)
//   D) "**g.8** — {SANSKRIT}" then "> {translation}"                 (gatha: maharthamanjari)
// In all, the verse translation lives on blockquote (">") lines.
// Usage: node scripts/segment-t1.mjs <md> <work_id> <edition> <out.jsonl>

import { readFileSync, writeFileSync } from "fs";

const [md, workId, edition, out] = process.argv.slice(2);
if (!md || !workId || !out) {
  console.error("usage: node scripts/segment-t1.mjs <md> <work_id> <edition> <out.jsonl>");
  process.exit(1);
}

// ch/verse marker, verse-only marker, or gatha marker (all followed by optional text)
const MARKER_CH_VERSE = /^\*\*(\d+)\s*\/\s*(\d+)\*\*\s*[—–-]?\s*(.*?)\s*(?:\|\|+)?\s*$/;
const MARKER_VERSE = /^\*\*(\d+)\*\*\s*[—–-]?\s*(.*?)\s*(?:\|\|+)?\s*$/;
const MARKER_GATHA = /^\*\*g\.(\d+)\*\*\s*[—–-]?\s*(.*?)\s*(?:\|\|+)?\s*$/;
const BQ = /^>\s*[—–-]?\s*(.+?)\s*[—–-]?\s*$/;

const lines = readFileSync(md, "utf8").split(/\r?\n/);
const passages = [];
let cur = null;
let seenTranslation = false;

function flagsOf(s) {
  return [...new Set((s.match(/\[(?:X|TXT|GRAM|LEX|DOCT|WIT|SUP)(?::|])/g) ?? []).map((f) => f.replace("[", "").replace(":", "").replace("]", "")))];
}

function push() {
  if (cur && (cur.sanskrit || cur.translation)) {
    passages.push({
      id: `tantra:text:${workId}:${cur.locator}`,
      work_id: workId,
      location: { chapter: cur.ch, verse: cur.vs },
      sanskrit: cur.sanskrit.replace(/\s+/g, " ").trim(),
      close_translation: cur.translation.replace(/\s+/g, " ").trim(),
      flags: flagsOf(cur.translation),
      source_edition: edition,
      provenance: "derived from our T1 (working translation, not peer reviewed)",
    });
  }
  cur = null;
  seenTranslation = false;
}

for (const line of lines) {
  const mcv = line.match(MARKER_CH_VERSE);
  const mv = line.match(MARKER_VERSE);
  const mg = line.match(MARKER_GATHA);

  if (mcv) {
    push();
    cur = { ch: parseInt(mcv[1], 10), vs: parseInt(mcv[2], 10), locator: `${mcv[1]}.${mcv[2]}`, sanskrit: mcv[3].trim(), translation: "" };
    continue;
  }
  if (mv) {
    push();
    cur = { ch: 1, vs: parseInt(mv[1], 10), locator: mv[1], sanskrit: mv[2].trim(), translation: "" };
    continue;
  }
  if (mg) {
    push();
    cur = { ch: 1, vs: parseInt(mg[1], 10), locator: `g.${mg[1]}`, sanskrit: mg[2].trim(), translation: "" };
    continue;
  }
  if (!cur) continue;

  const t = line.trim();
  const b = line.match(BQ);
  if (b && b[1]) {
    cur.translation += (cur.translation ? " " : "") + b[1].trim();
    seenTranslation = true;
    continue;
  }
  if (!t || /^---+/i.test(t) || /^#/.test(t)) continue;
  if (!seenTranslation) {
    cur.sanskrit += (cur.sanskrit ? " " : "") + t;
  }
  // after translation started, ignore stray prose until next marker
}
push();

writeFileSync(out, passages.map((p) => JSON.stringify(p)).join("\n") + "\n", "utf8");
console.log(`wrote ${passages.length} passages -> ${out}`);

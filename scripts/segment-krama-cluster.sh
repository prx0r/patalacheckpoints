#!/usr/bin/env bash
# Segment the complete on-disk Krama-cluster works (multi-file T1s) into the passage corpus.
# Works segmented here: mahanayaprakasha, cidgaganacandrika, maharthamanjari.
# (Devīpañcaśataka + Kramastotra are NOT on disk — acquisition targets, skipped.)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
T1="/root/projects/sanskritree/translations/01_t1_working"
OUT="$ROOT/data/corpus/passages"

# work_id :: space-separated T1 file prefixes
declare -A WORKS=(
  [mahanayaprakasha]="mahanayaprakasha_opening mahanayaprakasha_dvitiya mahanayaprakasha_trtiya mahanayaprakasha_caturtha mahanayaprakasha_pancama mahanayaprakasha_sastha mahanayaprakasha_saptama mahanayaprakasha_astama mahanayaprakasha_navama mahanayaprakasha_dasama mahanayaprakasha_ekadasa mahanayaprakasha_dvadasa mahanayaprakasha_continuation mahanayaprakasha_final_udayas"
  [cidgaganacandrika]="cidgaganacandrika_opening cidgaganacandrika_continuation cidgaganacandrika_continuation2 cidgaganacandrika_continuation3 cidgaganacandrika_continuation4 cidgaganacandrika_continuation5 cidgaganacandrika_continuation6 cidgaganacandrika_continuation7 cidgaganacandrika_continuation8 cidgaganacandrika_continuation9 cidgaganacandrika_continuation10 cidgaganacandrika_continuation11_final"
  [maharthamanjari]="maharthamanjari_opening maharthamanjari_gathas8-32 maharthamanjari_gathas33-70"
)

EDITION_mahanayaprakasha="Kashmir Series ed. (1918, M00033/M00034)"
EDITION_cidgaganacandrika="Trivikrama Tirtha 1937 (M00014) / our T1"
EDITION_maharthamanjari="Singh/Maheshvarananda ed. / our T1"

edition_of() {
  case "$1" in
    mahanayaprakasha) echo "$EDITION_mahanayaprakasha" ;;
    cidgaganacandrika) echo "$EDITION_cidgaganacandrika" ;;
    maharthamanjari) echo "$EDITION_maharthamanjari" ;;
    *) echo "our T1" ;;
  esac
}

for work in "${!WORKS[@]}"; do
  tmp="/tmp/${work}_combined.md"
  : > "$tmp"
  for pre in ${WORKS[$work]}; do
    f="$T1/${pre}_pass1.md"
    if [ -f "$f" ]; then
      cat "$f" >> "$tmp"
      printf "\n\n---\n\n" >> "$tmp"
    fi
  done
  echo "== $work =="
  node "$ROOT/scripts/segment-t1.mjs" "$tmp" "$work" "$(edition_of "$work")" "$OUT/${work}.jsonl"
  rm -f "$tmp"
done
echo "done"

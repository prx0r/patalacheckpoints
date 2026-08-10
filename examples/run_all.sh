#!/usr/bin/env bash
# Run all documentation examples (executable truth) against a live API.
# Usage: ./examples/run_all.sh [base_url]
# The docs promise these fixtures stay stable; if one breaks, the API contract drifted.
set -euo pipefail
BASE="${1:-http://localhost:3000}"

# the API must be up first
if ! curl -sf -m 5 "$BASE/api" >/dev/null 2>&1; then
  echo "ERROR: API not reachable at $BASE (start 'npm run dev')" >&2
  exit 1
fi

for ex in 01-find-work 02-resolve-title 03-read-passage 04-passage-context \
          05-manuscript-witnesses 06-term-ledger 07-agent-research-flow; do
  echo "== $ex =="
  python3 "examples/$ex/$ex.py" "$BASE" >/tmp/ex_$ex.log 2>&1 \
    && echo "   PASS" \
    || { echo "   FAIL"; cat /tmp/ex_$ex.log; exit 1; }
done
echo "ALL EXAMPLES PASS"

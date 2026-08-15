#!/usr/bin/env bash
# start.sh — the ONE command a scholar runs to open Pāṭala.
#
# Usage:
#   ./start.sh          # start the scholar-facing app (if not already running)
#   ./start.sh status   # is it running? on what port?
#   ./start.sh stop     # stop it
#
# What it does: launches the Next.js app that serves the real scholar-facing UI + APIs
# (works, passages, review, attestation, crux, terminology...) on localhost:3000.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
PORT="${PORT:-3000}"

is_running() {
  curl -s -o /dev/null -w "%{http_code}" "http://localhost:$PORT/api/health" 2>/dev/null | grep -q 200
}

case "${1:-}" in
  status)
    if is_running; then
      echo "Pāṭala is RUNNING at http://localhost:$PORT"
      curl -s "http://localhost:$PORT/api/stats" 2>/dev/null | head -c 300; echo
    else
      echo "Pāṭala is NOT running."
    fi
    ;;
  stop)
    # find the exact next-server PID and kill it (never pkill — target only our server)
    pids=$(ps -eo pid,cmd | grep -E "next dev|next-server" | grep "$ROOT" | grep -v grep | awk '{print $1}')
    if [ -n "$pids" ]; then
      for pid in $pids; do kill "$pid" 2>/dev/null || true; done
      echo "Stopped Pāṭala."
    else
      echo "Pāṭala was not running."
    fi
    ;;
  ""|start)
    if is_running; then
      echo "Pāṭala is already running at http://localhost:$PORT"
    else
      echo "Starting Pāṭala at http://localhost:$PORT ..."
      (cd "$ROOT" && setsid nohup npm run dev > /tmp/patala-web.log 2>&1 &)
      # wait up to ~20s for it to come up (poll the log, don't sleep-wait the shell)
      for _ in $(seq 1 40); do
        if is_running; then
          echo "✓ Pāṭala is UP at http://localhost:$PORT"
          echo "  Try: http://localhost:$PORT/api/works (69 works)"
          echo "       http://localhost:$PORT/api/scholar?verb=audit (80 reviewable objects)"
          exit 0
        fi
        sleep 0.5
      done
      echo "Timed out waiting — check /tmp/patala-web.log"
      exit 1
    fi
    ;;
  *)
    echo "usage: ./start.sh [start|status|stop]"
    ;;
esac

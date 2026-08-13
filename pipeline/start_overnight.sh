#!/usr/bin/env bash
# /root/projects/patala/pipeline/start_overnight.sh
# ONE-COMMAND overnight launcher for the Pāṭala autonomous factory.
#
# This launches BOTH autonomous systems:
#   1. The LIVE RAW→EN translation runner (if not already running)
#   2. The FACTORY LOOP (canonical SOURCE→C1 across all works)
#
# Both are watchdog-protected (cron restarts them if they die). Rate limiting keeps them
# from starving each other's model API.
#
# Usage:
#   bash pipeline/start_overnight.sh            # start everything
#   bash pipeline/start_overnight.sh status     # show what's running
#   bash pipeline/start_overnight.sh stop       # stop the factory loop (leave live runner)
#
# See pipeline/OVERNIGHT.md for the full runbook + morning checklist.

set -u
export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
P="/root/projects/patala"
LOGDIR="/tmp/opencode"
mkdir -p "$LOGDIR"

cmd="${1:-start}"

case "$cmd" in
  start)
    echo "==> Installing cron watchdogs..."
    ( crontab -l 2>/dev/null | grep -v "watchdog_auto_translate\|factory_loop_watchdog"; \
      echo "*/5 * * * * $P/pipeline/watchdog_auto_translate.sh >> $LOGDIR/watchdog.log 2>&1"; \
      echo "*/5 * * * * $P/pipeline/factory_loop_watchdog.sh >> $LOGDIR/factory-loop-watchdog.log 2>&1" ) | crontab -
    echo "    cron watchdogs installed: $(crontab -l | grep -c watchdog) entries"

    # 1. live RAW→EN runner (if not running)
    if ! pgrep -f "auto_translate_raw.py" >/dev/null 2>&1; then
      echo "==> Starting live RAW→EN translation runner..."
      setsid nohup python3 -u $P/pipeline/auto_translate_raw.py \
        >> $LOGDIR/auto-translate.log 2>&1 < /dev/null &
      echo "$!" > $LOGDIR/auto-translate.pid
      echo "    started pid $!"
    else
      echo "==> live RAW→EN runner already running (pid $(pgrep -f auto_translate_raw.py | head -1))"
    fi

    # 2. factory loop (canonical SOURCE→C1) — if not already running
    if ! pgrep -f "factory_loop.sh" >/dev/null 2>&1; then
      echo "==> Starting factory loop (SOURCE→C1, all works)..."
      echo "    env: per_layer=${FACTORY_PER_LAYER:-2} model_calls=${FACTORY_MODEL_CALLS:-6} throttle=${FACTORY_THROTTLE:-2}"
      setsid nohup bash $P/pipeline/factory_loop.sh >> $LOGDIR/factory-loop.log 2>&1 < /dev/null &
      echo "$!" > $LOGDIR/factory-loop.pid
      echo "    started pid $!"
    else
      echo "==> factory loop already running (pid $(pgrep -f factory_loop.sh | head -1))"
    fi

    echo ""
    echo "OVERNIGHT RUN STARTED. Both systems are watchdog-protected."
    echo "Morning checklist:  bash pipeline/start_overnight.sh status"
    echo "Corpus progress:    python3 pipeline/factory_status.py --all"
    echo "Bulk certificate:   python3 pipeline/factory_certificate.py"
    echo "Live translation:   tail $LOGDIR/auto-translate.log"
    echo "Factory progress:   tail $LOGDIR/factory-loop.log"
    ;;

  status)
    echo "=== overnight systems status ==="
    if pgrep -f "auto_translate_raw.py" >/dev/null 2>&1; then
      echo "  live RAW→EN runner: RUNNING (pid $(pgrep -f auto_translate_raw.py | head -1))"
    else
      echo "  live RAW→EN runner: NOT RUNNING"
    fi
    if pgrep -f "factory_loop.sh" >/dev/null 2>&1; then
      echo "  factory loop:      RUNNING (pid $(pgrep -f factory_loop.sh | head -1))"
    else
      echo "  factory loop:      NOT RUNNING"
    fi
    echo "  cron watchdogs:    $(crontab -l | grep -c watchdog) entries"
    echo ""
    echo "corpus dashboard:"
    python3 $P/pipeline/factory_status.py --all 2>/dev/null | head -20
    ;;

  stop)
    echo "==> Stopping factory loop (leaving live runner)"
    pkill -9 -f "factory_loop.sh" 2>/dev/null
    echo "    factory loop stopped. Live runner untouched."
    ;;

  *)
    echo "usage: bash pipeline/start_overnight.sh [start|status|stop]"
    ;;
esac

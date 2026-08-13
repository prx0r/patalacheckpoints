#!/usr/bin/env bash
# /root/projects/patala/pipeline/factory_loop.sh
# The OVERNIGHT unattended driver for the autonomous factory.
# Runs the backlog scheduler in a REPEAT LOOP so it keeps advancing every registered work
# through SOURCE→T1→L0→ARGMAP→L2→L200→C1 all night, bounded by a model-call budget + throttle
# per pass so it coexists with the live RAW→EN translation runner (never starves the shared API).
#
# Also retries durable failures (A2-11) at the start of each pass.
#
# Usage (detached, survives session end):
#   setsid nohup bash pipeline/factory_loop.sh >> /tmp/opencode/factory-loop.log 2>&1 < /dev/null &
#
# Install a cron watchdog (every 5 min) to restart it if it dies:
#   ( crontab -l 2>/dev/null | grep -v factory_loop; \
#     echo "*/5 * * * * /root/projects/patala/pipeline/factory_loop_watchdog.sh >> /tmp/opencode/factory-loop-watchdog.log 2>&1" ) | crontab -
#
# Tune via env (defaults are conservative to respect the live runner):
#   FACTORY_PER_LAYER      passages per layer per work per pass (default 2)
#   FACTORY_MODEL_CALLS    model-call budget per pass         (default 6)
#   FACTORY_THROTTLE       seconds between model batches      (default 2)
#   FACTORY_SLEEP          seconds between passes             (default 30)
#   FACTORY_MAX_PASSES     0 = run forever (default 0)

set -u
export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
PER_LAYER="${FACTORY_PER_LAYER:-2}"
MODEL_CALLS="${FACTORY_MODEL_CALLS:-6}"
THROTTLE="${FACTORY_THROTTLE:-2}"
SLEEP_S="${FACTORY_SLEEP:-30}"
MAX_PASSES="${FACTORY_MAX_PASSES:-0}"
LAYERS="T1,ARGMAP,L0,L2,L200,C1"

echo "$(date '+%F %T') factory-loop: starting (per_layer=$PER_LAYER model_calls=$MODEL_CALLS throttle=$THROTTLE sleep=$SLEEP_S max_passes=$MAX_PASSES)" >> /tmp/opencode/factory-loop.log
pass=0
model_total=0
while true; do
  pass=$((pass+1))
  if [ "$MAX_PASSES" -gt 0 ] && [ "$pass" -gt "$MAX_PASSES" ]; then
    echo "$(date '+%F %T') factory-loop: reached max_passes=$MAX_PASSES; emitting certificate" >> /tmp/opencode/factory-loop.log
    cd /root/projects/patala
    python3 -u pipeline/factory_certificate.py --passes "$pass" --model-calls "$model_total" \
      >> /tmp/opencode/factory-certificate.log 2>&1
    break
  fi
  echo "$(date '+%F %T') factory-loop: PASS $pass start" >> /tmp/opencode/factory-loop.log
  # retry durable failures first, then advance the backlog (DAG scheduler)
  cd /root/projects/patala
  out=$(python3 -u pipeline/factory_scheduler.py --retry \
    --per-layer "$PER_LAYER" --max-model-calls "$MODEL_CALLS" --throttle "$THROTTLE" \
    --layers "$LAYERS" 2>&1)
  echo "$out" >> /tmp/opencode/factory-loop.log
  mc=$(echo "$out" | grep -o '"model_calls": [0-9]*' | grep -o '[0-9]*' | tail -1)
  [ -n "$mc" ] && model_total=$((model_total + mc))
  echo "$(date '+%F %T') factory-loop: PASS $pass done; sleeping ${SLEEP_S}s" >> /tmp/opencode/factory-loop.log
  sleep "$SLEEP_S"
done


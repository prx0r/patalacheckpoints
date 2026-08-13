#!/usr/bin/env bash
# /root/projects/patala/pipeline/factory_loop_watchdog.sh
# Watchdog: keep the overnight factory loop alive across sessions/timeouts.
# Safe to run every 5 min from cron. Idempotent + resume-safe (the scheduler is registry-driven,
# idempotent, and the failure/retry queue prevents loss).
#
# Install:
#   ( crontab -l 2>/dev/null | grep -v factory_loop_watchdog; \
#     echo "*/5 * * * * /root/projects/patala/pipeline/factory_loop_watchdog.sh >> /tmp/opencode/factory-loop-watchdog.log 2>&1" ) | crontab -
#   crontab -l   # confirm

set -u
export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# already running?
if pgrep -f "factory_loop.sh" >/dev/null 2>&1; then
  exit 0
fi

# restart detached
setsid nohup bash /root/projects/patala/pipeline/factory_loop.sh >> /tmp/opencode/factory-loop.log 2>&1 < /dev/null &
echo "$(date '+%F %T') factory-loop-watchdog: restarted factory_loop.sh pid $!" >> /tmp/opencode/factory-loop-watchdog.log

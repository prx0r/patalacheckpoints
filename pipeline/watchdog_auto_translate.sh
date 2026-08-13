#!/usr/bin/env bash
# /root/projects/patala/pipeline/watchdog_auto_translate.sh
# Watchdog: keep the autonomous translation runner alive across sessions/timeouts.
# Safe to run every N minutes from cron (or a detached loop). Idempotent + resume-safe:
#   - if the runner is alive, do nothing
#   - if it died, restart it (the runner skips already-translated source_sha256, so no dupes)
#   - single-writer: the runner's output files + source_sha256 dedup prevent double-work
#
# Install (cron, every 5 min):
#   ( crontab -l 2>/dev/null | grep -v watchdog_auto_translate; \
#     echo "*/5 * * * * /root/projects/patala/pipeline/watchdog_auto_translate.sh >> /tmp/opencode/watchdog.log 2>&1" ) | crontab -
#   crontab -l   # confirm

set -u
export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
LOG=/tmp/opencode/auto-translate.log
PIDFILE=/tmp/opencode/auto-translate.pid

# already running?
if pgrep -f "auto_translate_raw.py" >/dev/null 2>&1; then
  exit 0
fi

# NOTE: no stale-lock cleanup here. auto_translate_raw.py uses NO file lock — its safety is
# source_sha256 dedup (it skips already-translated verses), so there is no lock to clear.
# Deleting .autonomy.lock (the autonomy CONTROLLER's lock) here was a bug: it could unlatch the
# controller while it was mid-run. The runner is safe to restart directly.

# restart detached
setsid nohup python3 /root/projects/patala/pipeline/auto_translate_raw.py >> "$LOG" 2>&1 < /dev/null &
echo "$!" > "$PIDFILE"
echo "$(date '+%F %T') watchdog: restarted auto_translate_raw.py pid $!" >> "$LOG"

#!/usr/bin/env bash
# run-map.sh — SessionStart hook wrapper
# מריץ את מחולל מפת הסקילים באופן סינכרוני (חוסם ~2-3 שניות, אמין).
# גרסה קודמת השתמשה ב-nohup ... & (רקע מנותק) — התהליך נהרג לפני סיום הבנייה.
set -uo pipefail

LOG_DIR="$HOME/.claude/logs"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/skill-map.log"

# איתור node עמיד (עוקף בעיות PATH / רווח בנתיב "Program Files")
NODE="$(command -v node 2>/dev/null || true)"
[ -z "$NODE" ] && NODE="/c/Program Files/nodejs/node"

echo "=== skill-map run @ $(date '+%Y-%m-%d %H:%M:%S') ===" > "$LOG"
"$NODE" "$HOME/.claude/skill-map/generate-map.mjs" >> "$LOG" 2>&1

# תמיד יוצא 0 — לא חוסם פתיחת סשן גם אם הבנייה נכשלה
exit 0

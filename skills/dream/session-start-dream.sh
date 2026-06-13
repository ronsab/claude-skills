#!/usr/bin/env bash
# session-start-dream.sh - SessionStart hook
# בודק אם .dream-pending קיים, ואם כן מריץ את הסקיל ברקע ומוחק את הדגל
set -euo pipefail

FLAG="$HOME/.claude/.dream-pending"
LOG_DIR="$HOME/.claude/logs"
mkdir -p "$LOG_DIR"

if [[ ! -f "$FLAG" ]]; then
  exit 0
fi

# מוחקים מיד כדי למנוע הרצות כפולות במקביל
rm -f "$FLAG"

# מריצים את הסקיל ברקע, מנותק מה-session הנוכחי
nohup claude -p "Run the dream memory consolidation skill. Read ~/.claude/skills/dream/SKILL.md and execute all 4 phases for all projects in ~/.claude/projects/. When done, write the current Unix timestamp to ~/.claude/projects/*/memory/.last-dream." \
  --allowedTools "Read,Write,Edit,Bash,Glob,Grep" \
  > "$LOG_DIR/dream-$(date +%Y%m%d-%H%M%S).log" 2>&1 &

exit 0

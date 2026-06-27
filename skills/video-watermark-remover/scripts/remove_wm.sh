#!/usr/bin/env bash
# remove_wm.sh - הסרת סימן מים וקידוד איכותי, שמירת המקור
# שימוש:
#   remove_wm.sh "INPUT.mp4" delogo X Y W H            -> אינטרפולציה מהרקע (ברירת מחדל)
#   remove_wm.sh "INPUT.mp4" blur   X Y W H            -> טשטוש האזור (גיבוי לרקע סוער)
#   remove_wm.sh "INPUT.mp4" crop   X Y W H            -> חיתוך פס (X/Y/W/H = אזור לשמור)
# הפלט: "<שם> - נקי.<סיומת>" באותה תיקייה. אם יש אודיו הוא נשמר.
set -euo pipefail

IN="${1:?צריך נתיב לקובץ וידאו}"
METHOD="${2:?צריך שיטה: delogo|blur|crop}"
X="${3:?X}"; Y="${4:?Y}"; W="${5:?W}"; H="${6:?H}"

DIR=$(dirname "$IN")
BASE=$(basename "$IN")
NAME="${BASE%.*}"
EXT="${BASE##*.}"
OUT="$DIR/${NAME} - נקי.${EXT}"

case "$METHOD" in
  delogo) VF="delogo=x=${X}:y=${Y}:w=${W}:h=${H}" ;;
  blur)   VF="boxblur=10:enable='1',crop=${W}:${H}:${X}:${Y}" ;; # ראה הערה למטה
  crop)   VF="crop=${W}:${H}:${X}:${Y}" ;;
  *) echo "שיטה לא מוכרת: $METHOD" >&2; exit 1 ;;
esac

# blur נכון דורש שרשור: לטשטש רק את התיבה ולהדביק בחזרה. נשתמש ב-overlay.
if [ "$METHOD" = "blur" ]; then
  FILTER="[0:v]crop=${W}:${H}:${X}:${Y},boxblur=12[bw];[0:v][bw]overlay=${X}:${Y}[v]"
  ffmpeg -y -i "$IN" -filter_complex "$FILTER" -map "[v]" -map 0:a? \
    -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -c:a copy "$OUT"
else
  ffmpeg -y -i "$IN" -vf "$VF" -map 0:v -map 0:a? \
    -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -c:a copy "$OUT"
fi

echo "נוצר: $OUT"

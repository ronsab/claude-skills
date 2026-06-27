#!/usr/bin/env bash
# probe_wm.sh - חילוץ פריימים לזיהוי מיקום סימן מים ולבדיקת תנועה
# שימוש:
#   probe_wm.sh "INPUT.mp4" corner-br|corner-bl|corner-tr|corner-tl|full   -> _wm_probe.png (אזור מוגדל)
#   probe_wm.sh "INPUT.mp4" motion                                          -> _wm_m1..m4.png (זמנים שונים)
set -euo pipefail

IN="${1:?צריך נתיב לקובץ וידאו}"
MODE="${2:-corner-br}"

# מימדים ואורך (tr -d '\r' חיוני ב-Windows - ffprobe מחזיר עם carriage return)
read -r W H < <(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$IN" | tr -d '\r' | tr ',' ' ')
DUR=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$IN" | tr -d '\r')
DUR=${DUR%.*}; [ -z "$DUR" ] && DUR=1

# גודל אזור הפינה: חצי רוחב/גובה (מספיק כדי לתפוס סימן בפינה)
CW=$(( W / 2 )); CH=$(( H / 2 ))

corner_crop() { # echo "w:h:x:y" לפי הפינה
  case "$1" in
    corner-br) echo "${CW}:${CH}:$(( W - CW )):$(( H - CH ))" ;;
    corner-bl) echo "${CW}:${CH}:0:$(( H - CH ))" ;;
    corner-tr) echo "${CW}:${CH}:$(( W - CW )):0" ;;
    corner-tl) echo "${CW}:${CH}:0:0" ;;
    full)      echo "${W}:${H}:0:0" ;;
    *) echo "${CW}:${CH}:$(( W - CW )):$(( H - CH ))" ;;
  esac
}

DIR=$(dirname "$IN")
MID=$(awk "BEGIN{printf \"%.2f\", $DUR/2}")

if [ "$MODE" = "motion" ]; then
  i=1
  for frac in 0.10 0.40 0.70 0.95; do
    T=$(awk "BEGIN{printf \"%.2f\", $DUR*$frac}")
    CROP=$(corner_crop full)
    ffmpeg -y -ss "$T" -i "$IN" -frames:v 1 -vf "scale=iw/2:ih/2" "$DIR/_wm_m${i}.png" >/dev/null 2>&1
    echo "כתב $DIR/_wm_m${i}.png  (t=${T}s)"
    i=$(( i + 1 ))
  done
  echo "קרא את _wm_m1..m4.png והשווה את מיקום הסימן. זהה = סטטי, שונה = נע."
else
  CROP=$(corner_crop "$MODE")
  # crop ואז הגדלה פי 2 לזיהוי ברור
  ffmpeg -y -ss "$MID" -i "$IN" -frames:v 1 -vf "crop=${CROP},scale=iw*2:ih*2" "$DIR/_wm_probe.png" >/dev/null 2>&1
  echo "כתב $DIR/_wm_probe.png  (אזור=$MODE, crop=${CROP}, מוגדל פי 2)"
  echo "מימדי הוידאו המקורי: ${W}x${H}. קבע תיבת delogo במונחי המקור."
fi

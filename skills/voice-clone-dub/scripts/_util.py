# -*- coding: utf-8 -*-
# כלי עזר משותפים: איתור ffmpeg/ffprobe, קידוד קונסולת Windows, וקריאת מפתחות API
# מבוסס על _util.py של hebrew-subtitles/video-merge (זהה) + תוספת helper למפתחות
import glob
import os
import shutil
import sys


def setup_console():
    # קונסולת Windows לא תמיד ב-UTF-8 — בלי זה הדפסת עברית נכשלת
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass


def _find_tool(name):
    # קודם PATH, אחר כך תיקיית ההתקנה של WinGet
    found = shutil.which(name)
    if found:
        return found
    pattern = os.path.join(
        os.environ.get("LOCALAPPDATA", ""),
        "Microsoft", "WinGet", "Packages",
        "Gyan.FFmpeg*", "*", "bin", name + ".exe",
    )
    matches = glob.glob(pattern)
    if matches:
        return matches[0]
    raise FileNotFoundError(
        f"{name} לא נמצא. התקן עם: winget install Gyan.FFmpeg"
    )


def find_ffmpeg():
    return _find_tool("ffmpeg")


def find_ffprobe():
    return _find_tool("ffprobe")


def escape_for_filter(path):
    # נתיב Windows בתוך פילטר של ffmpeg: לוכסנים קדימה + escape לנקודתיים
    return path.replace("\\", "/").replace(":", "\\:")


def require_env(name, where_to_get):
    # קריאת מפתח API ממשתנה סביבה. אם חסר — עצירה עם הודעה בעברית.
    # אסור להמציא מפתח: אם אין, הסקריפט נכשל בכוונה.
    value = os.environ.get(name)
    if not value:
        print(
            f"שגיאה: משתנה הסביבה {name} לא מוגדר.\n"
            f"השג מפתח כאן: {where_to_get}",
            file=sys.stderr,
        )
        sys.exit(1)
    return value

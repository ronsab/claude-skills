# -*- coding: utf-8 -*-
# כלי עזר משותפים: איתור ffmpeg/ffprobe, פונט עברי, והגדרות קידוד לקונסולת Windows
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


def find_hebrew_font():
    # פונט שמרנדר עברית. Arial רגיל לא תמיד מרנדר — ARIALUNI עדיף.
    # סדר עדיפות: Arial Unicode > Arial > כל TTF ב-Windows/Fonts
    fonts_dir = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts")
    for candidate in ("ARIALUNI.TTF", "arial.ttf", "tahoma.ttf", "segoeui.ttf"):
        p = os.path.join(fonts_dir, candidate)
        if os.path.isfile(p):
            return p
    raise FileNotFoundError("לא נמצא פונט מתאים ב-Windows/Fonts")


def escape_for_filter(path):
    # נתיב Windows בתוך פילטר של ffmpeg: לוכסנים קדימה + escape לנקודתיים
    return path.replace("\\", "/").replace(":", "\\:")

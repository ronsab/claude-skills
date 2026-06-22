# -*- coding: utf-8 -*-
"""כלי עזר משותפים ל-reel-brander: איתור ffmpeg/ffprobe + UTF-8."""
import os, sys, glob, shutil, subprocess

# alias של python שבור ב-Windows של רון, וקונסולת cp1252 מתרסקת על עברית.
# reconfigure ל-UTF-8 פותר את הדפסת העברית ללוג.
def init_utf8():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def _winget_bin(name):
    """מאתר ffmpeg/ffprobe בתיקיית WinGet אם אינו ב-PATH."""
    base = os.path.expanduser(
        r"~\AppData\Local\Microsoft\WinGet\Packages"
    )
    hits = glob.glob(os.path.join(base, "Gyan.FFmpeg*", "**", name + ".exe"),
                     recursive=True)
    return hits[0] if hits else None


def find_tool(name):
    """name = 'ffmpeg' או 'ffprobe'. מחזיר נתיב מלא או None."""
    p = shutil.which(name)
    if p:
        return p
    return _winget_bin(name)


def run(cmd, label=None):
    """מריץ פקודה, מדפיס תווית קצרה, עוצר על שגיאה."""
    if label:
        print(f"  > {label}")
    r = subprocess.run(cmd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print("STDERR:", (r.stderr or "")[-800:])
        sys.exit(1)
    return r

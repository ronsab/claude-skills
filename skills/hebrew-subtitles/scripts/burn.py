# -*- coding: utf-8 -*-
"""
צריבת כתוביות לתוך וידאו עם ffmpeg (libass - תומך עברית RTL).

שימוש:
    python burn.py <video.mp4> <subs.srt|subs.ass> [--out output.mp4]

קובץ ASS נצרב עם העיצוב המוטמע בו; קובץ SRT נצרב בסגנון קלאסי (Heebo, תחתית).
"""
import argparse
import os
import subprocess
import sys

from _util import escape_for_filter, find_ffmpeg, setup_console

FONTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fonts")


def main():
    setup_console()
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    parser.add_argument("subs")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    for p in (args.video, args.subs):
        if not os.path.isfile(p):
            print(f"שגיאה: הקובץ לא נמצא: {p}", file=sys.stderr)
            sys.exit(1)

    out = args.out or os.path.splitext(args.video)[0] + "_subtitled.mp4"
    subs = escape_for_filter(os.path.abspath(args.subs))
    fonts = escape_for_filter(FONTS_DIR)

    if args.subs.lower().endswith(".ass"):
        vf = f"subtitles=filename='{subs}':fontsdir='{fonts}'"
    else:
        # SRT: עיצוב קלאסי צנוע - libass עובד ביחס ל-PlayResY=288, לכן 13 הוא כ-4.5% מגובה המסך
        style = "FontName=Heebo,Bold=1,FontSize=13,Outline=1,Shadow=0,MarginV=20"
        vf = f"subtitles=filename='{subs}':fontsdir='{fonts}':force_style='{style}'"

    ffmpeg = find_ffmpeg()
    print("צורב כתוביות (קידוד מחדש של הווידאו, האודיו מועתק כמו שהוא)...")
    subprocess.run(
        [ffmpeg, "-y", "-v", "error", "-stats", "-i", args.video,
         "-vf", vf,
         "-c:v", "libx264", "-crf", "18", "-preset", "medium",
         "-c:a", "copy", "-movflags", "+faststart", out],
        check=True,
    )
    print(f"נשמר: {out}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
המרת הקלטת מסך ארוכה (16:9) לריל אנכי ממותג (9:16) לאינסטגרם/פייסבוק.

מקבל רשימת קטעי מפתח (start:duration) שנבחרו מראש על ידי Claude אחרי ניתוח
ויזואלי של הסרטון. לכל קטע: חיתוך + המרה ל-9:16 עם רקע מטושטש (לא פסים שחורים)
וכותרת ממותגת צרובה. בסוף: איחוד + מוזיקת רקע.

שימוש:
    python build_reel.py --input VIDEO.mp4 --segments "0:25,30:18,48:18,66:9,88:20" \
        --title "RON DIGITAL STUDIO" --subtitle "מערכות דיגיטליות" \
        --music ambient --max 90 --out reel.mp4

מוזיקה:
    --music ambient   סינתזת C-major + echo + fade ישירות ב-ffmpeg (ברירת מחדל)
    --music none      ללא אודיו (ריל שקט)
    --music PATH.mp3  קובץ מוזיקה חיצוני
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

from _util import (find_ffmpeg, find_ffprobe, find_hebrew_font,
                   setup_console, escape_for_filter)


def probe_duration(ffprobe, path):
    out = subprocess.run(
        [ffprobe, "-v", "error", "-show_entries", "format=duration",
         "-of", "json", path],
        capture_output=True, text=True, check=True,
    )
    return float(json.loads(out.stdout)["format"]["duration"])


def parse_segments(spec):
    # "0:25,30:18" → [(0.0, 25.0), (30.0, 18.0)]
    segs = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        start_s, dur_s = part.split(":")
        segs.append((float(start_s), float(dur_s)))
    return segs


def build_vertical_filter(width, height, font, title_file, sub_file):
    # שלב 4 המאומת: רקע מטושטש ממולא + וידאו חד ממורכז + כותרת צרובה
    font_e = escape_for_filter(font)
    f = (
        f"[0:v]scale=-2:{height},crop={width}:{height}:(iw-{width})/2:0,"
        f"boxblur=25:5[bg];"
        f"[0:v]scale={width}:-2[fg];"
        f"[bg][fg]overlay=x=0:y=(H-h)/2"
    )
    if title_file:
        title_e = escape_for_filter(title_file)
        # רצועה כהה חצי-שקופה למעלה לקריאות הכותרת
        f += (
            f",drawbox=x=0:y=0:w=iw:h=720:color=0x00000099:t=fill"
            f",drawtext=fontfile='{font_e}':textfile='{title_e}':"
            f"x=(w-text_w)/2:y=290:fontsize=58:fontcolor=white:"
            f"shadowx=3:shadowy=3:shadowcolor=black"
        )
        if sub_file:
            sub_e = escape_for_filter(sub_file)
            f += (
                f",drawtext=fontfile='{font_e}':textfile='{sub_e}':"
                f"x=(w-text_w)/2:y=370:fontsize=36:fontcolor=#aaaaff:"
                f"shadowx=2:shadowy=2:shadowcolor=black"
            )
    f += "[out]"
    return f


def make_segment(ffmpeg, src, start, dur, dst, vfilter, fps):
    # חיתוך + המרה ל-9:16 בפקודה אחת (re-encode → חיתוך מדויק)
    cmd = [
        ffmpeg, "-y", "-v", "error",
        "-ss", str(start), "-i", src, "-t", str(dur),
        "-filter_complex", vfilter, "-map", "[out]", "-an",
        "-r", str(fps), "-c:v", "libx264", "-preset", "fast",
        "-crf", "22", "-pix_fmt", "yuv420p", dst,
    ]
    subprocess.run(cmd, check=True)


def make_ambient(ffmpeg, total, dst):
    # סינתזת C-major (C2/C3/C4/E4/A4) + echo + fade. שלב 5 המאומת.
    fade_out = max(0.0, total - 3.0)
    expr = ("aevalsrc=sin(2*PI*t*110)*0.08+sin(2*PI*t*220)*0.22+"
            "sin(2*PI*t*261)*0.15+sin(2*PI*t*330)*0.12+"
            "sin(2*PI*t*440)*0.06:s=44100:c=stereo")
    af = (f"afade=t=in:st=0:d=3,afade=t=out:st={fade_out:.2f}:d=3,"
          f"aecho=0.6:0.3:800:0.4,volume=0.35")
    subprocess.run(
        [ffmpeg, "-y", "-v", "error", "-f", "lavfi", "-i", expr,
         "-af", af, "-t", f"{total + 2:.2f}", "-ar", "44100", dst],
        check=True,
    )


def main():
    setup_console()
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="הקלטת המסך המקורית")
    parser.add_argument("--segments", required=True,
                        help='קטעי מפתח: "start:dur,start:dur" בשניות')
    parser.add_argument("--title", default=None, help="כותרת ממותגת (אנגלית/עברית)")
    parser.add_argument("--subtitle", default=None, help="תת-כותרת מתחת לכותרת")
    parser.add_argument("--music", default="ambient",
                        help="ambient | none | נתיב לקובץ MP3")
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1920)
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--max", type=float, default=90.0)
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"שגיאה: הקובץ לא נמצא: {args.input}", file=sys.stderr)
        sys.exit(1)

    segs = parse_segments(args.segments)
    if not segs:
        print("שגיאה: לא סופקו קטעים", file=sys.stderr)
        sys.exit(1)

    total = sum(d for _, d in segs)
    print(f"{len(segs)} קטעים, סך הכל {total:.1f} שניות")
    if total > args.max:
        print(f"\nשגיאה: חריגה מהמגבלה של {args.max:.0f} שניות. פירוט:",
              file=sys.stderr)
        for i, (s, d) in enumerate(segs, 1):
            print(f"  קטע {i}: התחלה {s:.0f}s, משך {d:.1f}s", file=sys.stderr)
        print("קצר קטעים או הגדל --max (רק באישור מפורש).", file=sys.stderr)
        sys.exit(2)

    ffmpeg = find_ffmpeg()
    ffprobe = find_ffprobe()
    src_dur = probe_duration(ffprobe, args.input)
    for i, (s, d) in enumerate(segs, 1):
        if s + d > src_dur + 0.5:
            print(f"שגיאה: קטע {i} ({s}+{d}) חורג ממשך המקור ({src_dur:.1f}s)",
                  file=sys.stderr)
            sys.exit(1)

    out = args.out or os.path.join(
        os.path.dirname(os.path.abspath(args.input)), "reel.mp4")

    with tempfile.TemporaryDirectory() as tmp:
        # כותרות → קבצי txt (עוקף בעיות escaping של עברית ב-filter_complex)
        title_file = sub_file = None
        font = None
        if args.title:
            font = find_hebrew_font()
            title_file = os.path.join(tmp, "title.txt")
            with open(title_file, "w", encoding="utf-8") as f:
                f.write(args.title)
            if args.subtitle:
                sub_file = os.path.join(tmp, "sub.txt")
                with open(sub_file, "w", encoding="utf-8") as f:
                    f.write(args.subtitle)

        vfilter = build_vertical_filter(args.width, args.height, font,
                                        title_file, sub_file)

        verticals = []
        for idx, (start, dur) in enumerate(segs):
            dst = os.path.join(tmp, f"seg{idx:03d}.mp4")
            print(f"מעבד קטע {idx + 1}/{len(segs)}: "
                  f"התחלה {start:.0f}s, משך {dur:.1f}s")
            make_segment(ffmpeg, args.input, start, dur, dst, vfilter, args.fps)
            verticals.append(dst)

        list_path = os.path.join(tmp, "list.txt")
        with open(list_path, "w", encoding="utf-8") as f:
            for v in verticals:
                f.write(f"file '{v.replace(os.sep, '/')}'\n")

        music = args.music.strip()
        if music == "none":
            print("איחוד (ללא מוזיקה)...")
            subprocess.run(
                [ffmpeg, "-y", "-v", "error", "-f", "concat", "-safe", "0",
                 "-i", list_path, "-c:v", "libx264", "-preset", "fast",
                 "-crf", "21", "-movflags", "+faststart", out],
                check=True,
            )
        else:
            if music == "ambient":
                music_path = os.path.join(tmp, "music.mp3")
                print("מסנתז מוזיקת ambient...")
                make_ambient(ffmpeg, total, music_path)
            else:
                if not os.path.isfile(music):
                    print(f"שגיאה: קובץ המוזיקה לא נמצא: {music}", file=sys.stderr)
                    sys.exit(1)
                music_path = music
            print("מאחד + מוסיף מוזיקה...")
            subprocess.run(
                [ffmpeg, "-y", "-v", "error", "-f", "concat", "-safe", "0",
                 "-i", list_path, "-i", music_path,
                 "-map", "0:v", "-map", "1:a",
                 "-c:v", "libx264", "-preset", "fast", "-crf", "21",
                 "-c:a", "aac", "-b:a", "128k", "-shortest",
                 "-movflags", "+faststart", out],
                check=True,
            )

    final_dur = probe_duration(ffprobe, out)
    print(f"נשמר: {out}")
    print(f"משך סופי: {final_dur:.1f} שניות, {args.width}x{args.height}, "
          f"{args.fps}fps")


if __name__ == "__main__":
    main()

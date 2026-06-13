# -*- coding: utf-8 -*-
"""
איחוד קליפים קצרים לסרטון אחד (יעד: אינסטגרם/פייסבוק).

כל קליפ מנורמל לפורמט אחיד (ברירת מחדל 1080x1920, 30fps, AAC) ואז הכל
מאוחד בחיתוך ישיר בלי קידוד נוסף. קליפ בלי אודיו מקבל פס שקט.

שימוש:
    python merge.py clip1.mp4 clip2.mp4 ... [--out merged.mp4]
                    [--width 1080] [--height 1920] [--fps 30] [--max-seconds 90]
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

from _util import find_ffmpeg, find_ffprobe, setup_console


def probe(ffprobe, path):
    # משך, ממדים, והאם קיים פס אודיו
    out = subprocess.run(
        [ffprobe, "-v", "error", "-show_entries",
         "format=duration:stream=codec_type,width,height",
         "-of", "json", path],
        capture_output=True, text=True, check=True,
    )
    data = json.loads(out.stdout)
    info = {"duration": float(data["format"]["duration"]), "has_audio": False,
            "width": 0, "height": 0}
    for s in data.get("streams", []):
        if s.get("codec_type") == "audio":
            info["has_audio"] = True
        elif s.get("codec_type") == "video":
            info["width"] = s.get("width", 0)
            info["height"] = s.get("height", 0)
    return info


def normalize(ffmpeg, src, dst, width, height, fps, has_audio):
    # התאמה לפורמט אחיד: הקטנה ששומרת על היחס + פסים למילוי, בלי לחתוך תוכן
    vf = (f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
          f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black,"
          f"fps={fps},format=yuv420p")
    cmd = [ffmpeg, "-y", "-v", "error", "-i", src]
    if not has_audio:
        # פס שקט - בלעדיו האיחוד עם קליפים אחרים נשבר
        cmd += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
                "-shortest"]
    cmd += ["-vf", vf, "-c:v", "libx264", "-crf", "18", "-preset", "medium",
            "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "128k", dst]
    subprocess.run(cmd, check=True)


def main():
    setup_console()
    parser = argparse.ArgumentParser()
    parser.add_argument("clips", nargs="+", help="קבצי וידאו בסדר הרצוי")
    parser.add_argument("--out", default=None)
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1920)
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--max-seconds", type=float, default=90.0)
    args = parser.parse_args()

    for c in args.clips:
        if not os.path.isfile(c):
            print(f"שגיאה: הקובץ לא נמצא: {c}", file=sys.stderr)
            sys.exit(1)

    ffmpeg = find_ffmpeg()
    ffprobe = find_ffprobe()

    infos = [probe(ffprobe, c) for c in args.clips]
    total = sum(i["duration"] for i in infos)
    print(f"{len(args.clips)} קליפים, סך הכל {total:.1f} שניות")

    if total > args.max_seconds:
        print(f"\nשגיאה: חריגה מהמגבלה של {args.max_seconds:.0f} שניות. פירוט:",
              file=sys.stderr)
        for c, i in zip(args.clips, infos):
            print(f"  {i['duration']:5.1f} שניות  {os.path.basename(c)}", file=sys.stderr)
        print("הסר קליפים או קצר אותם ונסה שוב.", file=sys.stderr)
        sys.exit(2)

    out = args.out or os.path.join(os.path.dirname(os.path.abspath(args.clips[0])),
                                   "merged.mp4")

    with tempfile.TemporaryDirectory() as tmp:
        normalized = []
        for idx, (clip, info) in enumerate(zip(args.clips, infos)):
            dst = os.path.join(tmp, f"norm{idx:03d}.mp4")
            note = "" if info["has_audio"] else " (בלי אודיו - נוסף פס שקט)"
            print(f"מנרמל {idx + 1}/{len(args.clips)}: "
                  f"{os.path.basename(clip)} {info['width']}x{info['height']}{note}")
            normalize(ffmpeg, clip, dst, args.width, args.height, args.fps,
                      info["has_audio"])
            normalized.append(dst)

        # רשימת קבצים ל-concat demuxer; כולם זהים בפרמטרים אז -c copy בטוח
        list_path = os.path.join(tmp, "list.txt")
        with open(list_path, "w", encoding="utf-8") as f:
            for n in normalized:
                f.write(f"file '{n.replace(os.sep, '/')}'\n")

        print("מאחד...")
        subprocess.run(
            [ffmpeg, "-y", "-v", "error", "-f", "concat", "-safe", "0",
             "-i", list_path, "-c", "copy", "-movflags", "+faststart", out],
            check=True,
        )

    final = probe(ffprobe, out)
    print(f"נשמר: {out}")
    print(f"משך סופי: {final['duration']:.1f} שניות, "
          f"{args.width}x{args.height}, {args.fps}fps")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_audio.py -- חילוץ פס הקול מקליפ וידאו (נדרש רק במסלול S2S)

שימוש:
    python run.py extract_audio.py "clip.mp4"
    python run.py extract_audio.py "clip.mp4" --output original_audio.wav --json

פלט: קובץ WAV (44.1kHz מונו) + משך הקליפ בשניות.
"""

import argparse
import json
import os
import subprocess
import sys

from _util import setup_console, find_ffmpeg, find_ffprobe


def probe_duration(path):
    ffprobe = find_ffprobe()
    out = subprocess.run(
        [ffprobe, "-v", "error", "-show_entries", "format=duration",
         "-of", "json", path],
        check=True, capture_output=True, text=True,
    )
    return float(json.loads(out.stdout)["format"]["duration"])


def output_result(data, as_json):
    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    elif data.get("status") == "success":
        print(f"אודיו חולץ: {data['path']}  (משך: {data['duration_seconds']:.1f} שניות)")
    else:
        print(f"שגיאה: {data.get('error')}", file=sys.stderr)


def main():
    setup_console()
    parser = argparse.ArgumentParser(description="חילוץ אודיו מקליפ")
    parser.add_argument("video", help="נתיב קליפ וידאו")
    parser.add_argument("--output", help="נתיב פלט (ברירת מחדל: <video>.original.wav)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not os.path.exists(args.video):
        output_result({"status": "error", "error": f"קובץ לא קיים: {args.video}"}, args.json)
        return 1

    out_path = args.output or (os.path.splitext(args.video)[0] + ".original.wav")

    try:
        ffmpeg = find_ffmpeg()
        subprocess.run(
            [ffmpeg, "-y", "-i", args.video, "-vn", "-acodec", "pcm_s16le",
             "-ar", "44100", "-ac", "1", out_path],
            check=True, capture_output=True,
        )
        duration = probe_duration(args.video)
        output_result({
            "status": "success",
            "path": os.path.abspath(out_path),
            "duration_seconds": duration,
        }, args.json)
        return 0
    except Exception as e:
        output_result({"status": "error", "error": f"חילוץ נכשל: {e}"}, args.json)
        return 1


if __name__ == "__main__":
    sys.exit(main())

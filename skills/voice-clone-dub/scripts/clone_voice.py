#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
clone_voice.py -- שלב חד-פעמי: שכפול הקול של רון ב-ElevenLabs (Instant Voice Clone)

שימוש:
    python run.py clone_voice.py --list
    python run.py clone_voice.py --name "Ron" --files recording1.mp3 recording2.wav
    python run.py clone_voice.py --name "Ron" --files clip.mp4   # וידאו -> אודיו אוטומטי

קלט וידאו מחולץ אוטומטית לאודיו לפני השליחה.
הפלט: voice_id -- יש לשמור אותו (מומלץ כמשתנה סביבה RON_VOICE_ID).
הקול עצמו נשמר בחשבון ElevenLabs ולא צריך לשכפל אותו שוב.
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile

from _util import setup_console, find_ffmpeg, require_env

AUDIO_EXTS = {".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac"}


def output_result(data, as_json):
    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    if data.get("status") == "success":
        print("\n" + "=" * 50)
        print("  הקול שוכפל בהצלחה!")
        print("=" * 50)
        print(f"  שם:       {data['name']}")
        print(f"  voice_id: {data['voice_id']}")
        print("\n  שמור את ה-voice_id הזה. מומלץ להגדיר משתנה סביבה:")
        print(f"    RON_VOICE_ID={data['voice_id']}")
        print("=" * 50 + "\n")
    elif data.get("status") == "list":
        print("\nקולות קיימים בחשבון:")
        for v in data["voices"]:
            print(f"  - {v['name']}: {v['voice_id']}")
        print()
    else:
        print(f"\nשגיאה: {data.get('error', 'לא ידועה')}", file=sys.stderr)


def ensure_audio(path):
    """אם הקלט וידאו -- חילוץ אודיו ל-WAV זמני. מחזיר (נתיב, האם_זמני)."""
    ext = os.path.splitext(path)[1].lower()
    if ext in AUDIO_EXTS:
        return path, False
    ffmpeg = find_ffmpeg()
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tmp.close()
    subprocess.run(
        [ffmpeg, "-y", "-i", path, "-vn", "-acodec", "pcm_s16le",
         "-ar", "44100", "-ac", "1", tmp.name],
        check=True, capture_output=True,
    )
    return tmp.name, True


def main():
    setup_console()
    parser = argparse.ArgumentParser(description="שכפול קול ב-ElevenLabs")
    parser.add_argument("--list", action="store_true", help="הצג קולות קיימים בחשבון")
    parser.add_argument("--name", help="שם הקול (חובה לשכפול)")
    parser.add_argument("--files", nargs="+", help="קבצי הקלטה (אודיו או וידאו)")
    parser.add_argument("--json", action="store_true", help="פלט JSON")
    args = parser.parse_args()

    api_key = require_env(
        "ELEVENLABS_API_KEY",
        "https://elevenlabs.io/app/settings/api-keys",
    )

    try:
        from elevenlabs.client import ElevenLabs
        client = ElevenLabs(api_key=api_key)
    except Exception as e:
        output_result({"status": "error", "error": f"טעינת ElevenLabs SDK נכשלה: {e}"}, args.json)
        return 1

    # מצב רשימה
    if args.list:
        try:
            voices = client.voices.get_all().voices
            data = {"status": "list", "voices": [
                {"name": v.name, "voice_id": v.voice_id} for v in voices
            ]}
        except Exception as e:
            data = {"status": "error", "error": f"שליפת קולות נכשלה: {e}"}
        output_result(data, args.json)
        return 0 if data["status"] == "list" else 1

    # מצב שכפול
    if not args.name or not args.files:
        output_result({"status": "error", "error": "נדרשים --name ו---files (או --list)"}, args.json)
        return 1

    temp_files = []
    try:
        audio_paths = []
        for f in args.files:
            if not os.path.exists(f):
                output_result({"status": "error", "error": f"קובץ לא קיים: {f}"}, args.json)
                return 1
            ap, is_tmp = ensure_audio(f)
            audio_paths.append(ap)
            if is_tmp:
                temp_files.append(ap)

        if not args.json:
            print(f"משכפל קול '{args.name}' מ-{len(audio_paths)} קבצים...")

        # ElevenLabs SDK: ה-IVC עבר ל-client.voices.ivc.create בגרסאות חדשות,
        # ו-client.clone בגרסאות ישנות. ננסה את שניהם.
        file_handles = [open(p, "rb") for p in audio_paths]
        try:
            if hasattr(client.voices, "ivc"):
                voice = client.voices.ivc.create(name=args.name, files=file_handles)
            else:
                voice = client.clone(name=args.name, files=file_handles)
        finally:
            for fh in file_handles:
                fh.close()

        voice_id = getattr(voice, "voice_id", None) or getattr(voice, "id", None)
        output_result({"status": "success", "name": args.name, "voice_id": voice_id}, args.json)
        return 0

    except Exception as e:
        output_result({"status": "error", "error": f"שכפול נכשל: {e}"}, args.json)
        return 1
    finally:
        for t in temp_files:
            try:
                os.unlink(t)
            except OSError:
                pass


if __name__ == "__main__":
    sys.exit(main())

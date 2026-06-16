#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
convert_voice.py -- יצירת אודיו בקול של רון דרך ElevenLabs

שני מצבים:
  tts (ברירת מחדל) -- מטקסט. רון מספק את הטקסט לסרטון, הוא מוקרא בקולו.
  s2s              -- ממירים אודיו קיים לקול של רון, שומר תזמון/אינטונציה.

שימוש:
    python run.py convert_voice.py --voice-id <id> --text "שלום, זה הטקסט" --output out.mp3 --json
    python run.py convert_voice.py --voice-id <id> --text-file script.txt --output out.mp3
    python run.py convert_voice.py --voice-id <id> --mode s2s --audio original.wav --output out.mp3

אם --voice-id חסר, נלקח ממשתנה הסביבה RON_VOICE_ID.
"""

import argparse
import json
import os
import sys

from _util import setup_console, require_env

MODEL_TTS = "eleven_multilingual_v2"
MODEL_S2S = "eleven_multilingual_sts_v2"
OUTPUT_FORMAT = "mp3_44100_128"

# הערכת עלות גסה בקרדיטים (יש לאמת מול החשבון):
# TTS ~ קרדיט לתו. S2S ~ 1000 קרדיט לדקת אודיו.
CREDITS_PER_TTS_CHAR = 1.0
CREDITS_PER_S2S_SECOND = 1000.0 / 60.0


def write_stream(stream, out_path):
    """ה-SDK מחזיר iterator של bytes -- כותבים לקובץ."""
    with open(out_path, "wb") as f:
        if isinstance(stream, (bytes, bytearray)):
            f.write(stream)
        else:
            for chunk in stream:
                if chunk:
                    f.write(chunk)


def output_result(data, as_json):
    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    elif data.get("status") == "success":
        print("\n" + "=" * 50)
        print("  האודיו נוצר בקול של רון!")
        print("=" * 50)
        print(f"  מצב:      {data['mode']}")
        print(f"  קובץ:     {data['path']}")
        print(f"  עלות מ.:  ~{data['credits_estimate']} קרדיטים")
        print("=" * 50 + "\n")
    else:
        print(f"שגיאה: {data.get('error')}", file=sys.stderr)


def main():
    setup_console()
    parser = argparse.ArgumentParser(description="יצירת אודיו בקול של רון")
    parser.add_argument("--mode", choices=["tts", "s2s"], default="tts")
    parser.add_argument("--voice-id", help="voice_id (ברירת מחדל: משתנה RON_VOICE_ID)")
    parser.add_argument("--text", help="טקסט להקראה (מצב tts)")
    parser.add_argument("--text-file", help="קובץ טקסט (מצב tts)")
    parser.add_argument("--audio", help="קובץ אודיו מקורי (מצב s2s)")
    parser.add_argument("--output", help="נתיב פלט (ברירת מחדל: voice_out.mp3)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    voice_id = args.voice_id or os.environ.get("RON_VOICE_ID")
    if not voice_id:
        output_result({"status": "error", "error": "חסר --voice-id (או משתנה RON_VOICE_ID). הרץ קודם clone_voice.py"}, args.json)
        return 1

    out_path = args.output or "voice_out.mp3"

    api_key = require_env("ELEVENLABS_API_KEY", "https://elevenlabs.io/app/settings/api-keys")
    try:
        from elevenlabs.client import ElevenLabs
        client = ElevenLabs(api_key=api_key)
    except Exception as e:
        output_result({"status": "error", "error": f"טעינת ElevenLabs SDK נכשלה: {e}"}, args.json)
        return 1

    try:
        if args.mode == "tts":
            if args.text_file:
                if not os.path.exists(args.text_file):
                    output_result({"status": "error", "error": f"קובץ טקסט לא קיים: {args.text_file}"}, args.json)
                    return 1
                text = open(args.text_file, encoding="utf-8").read().strip()
            else:
                text = (args.text or "").strip()
            if not text:
                output_result({"status": "error", "error": "טקסט ריק (--text או --text-file)"}, args.json)
                return 1

            if not args.json:
                print("יוצר אודיו מטקסט (TTS)...")
            stream = client.text_to_speech.convert(
                voice_id=voice_id,
                text=text,
                model_id=MODEL_TTS,
                output_format=OUTPUT_FORMAT,
            )
            credits = round(len(text) * CREDITS_PER_TTS_CHAR)

        else:  # s2s
            if not args.audio or not os.path.exists(args.audio):
                output_result({"status": "error", "error": "מצב s2s דורש --audio קיים (השתמש ב-extract_audio.py)"}, args.json)
                return 1
            if not args.json:
                print("ממיר אודיו קיים לקול של רון (S2S)...")
            with open(args.audio, "rb") as af:
                stream = client.speech_to_speech.convert(
                    voice_id=voice_id,
                    audio=af,
                    model_id=MODEL_S2S,
                    output_format=OUTPUT_FORMAT,
                )
                write_stream(stream, out_path)
            # הערכת עלות לפי משך האודיו המקורי
            credits = _estimate_s2s_credits(args.audio)
            output_result({
                "status": "success", "mode": "s2s",
                "path": os.path.abspath(out_path), "credits_estimate": credits,
            }, args.json)
            return 0

        write_stream(stream, out_path)
        output_result({
            "status": "success", "mode": args.mode,
            "path": os.path.abspath(out_path), "credits_estimate": credits,
        }, args.json)
        return 0

    except Exception as e:
        output_result({"status": "error", "error": f"יצירת אודיו נכשלה: {e}"}, args.json)
        return 1


def _estimate_s2s_credits(audio_path):
    try:
        from _util import find_ffprobe
        import subprocess
        ffprobe = find_ffprobe()
        out = subprocess.run(
            [ffprobe, "-v", "error", "-show_entries", "format=duration",
             "-of", "json", audio_path],
            check=True, capture_output=True, text=True,
        )
        dur = float(json.loads(out.stdout)["format"]["duration"])
        return round(dur * CREDITS_PER_S2S_SECOND)
    except Exception:
        return 0


if __name__ == "__main__":
    sys.exit(main())

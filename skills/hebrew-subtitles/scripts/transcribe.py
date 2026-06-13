# -*- coding: utf-8 -*-
"""
תמלול וידאו בעברית עם OpenAI Whisper API.

זרימה: וידאו -> חילוץ אודיו דחוס (ffmpeg) -> Whisper API (זמני מילים+מקטעים) -> JSON + TXT.

שימוש:
    python transcribe.py <video.mp4> [--prompt "מונחים, שמות"] [--out base_path]

פלט:
    <video>.transcript.json  - מקטעים ומילים עם זמנים
    <video>.transcript.txt   - שורה ממוספרת לכל מקטע, לבדיקה ותיקון ידני
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

from _util import find_ffmpeg, find_ffprobe, setup_console

# מגבלת הקובץ של ה-API היא 25MB; משאירים שוליים
MAX_AUDIO_BYTES = 24 * 1024 * 1024
CHUNK_SECONDS = 20 * 60  # פיצול לחלקים של 20 דקות כשהאודיו גדול מדי


def get_duration(ffprobe, path):
    out = subprocess.run(
        [ffprobe, "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


def extract_audio(ffmpeg, video, out_path, start=None, length=None):
    # מונו 16kHz 64kbps - מספיק ל-Whisper וחוסך נפח
    cmd = [ffmpeg, "-y", "-v", "error"]
    if start is not None:
        cmd += ["-ss", str(start)]
    cmd += ["-i", video]
    if length is not None:
        cmd += ["-t", str(length)]
    cmd += ["-vn", "-ac", "1", "-ar", "16000", "-b:a", "64k", out_path]
    subprocess.run(cmd, check=True)


def transcribe_file(client, audio_path, prompt):
    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            language="he",
            response_format="verbose_json",
            timestamp_granularities=["word", "segment"],
            prompt=prompt or "",
        )
    return result.model_dump()


def shift_times(data, offset):
    # הזחת זמנים כשהתמלול נעשה בחלקים
    for seg in data.get("segments") or []:
        seg["start"] += offset
        seg["end"] += offset
    for w in data.get("words") or []:
        w["start"] += offset
        w["end"] += offset
    return data


def main():
    setup_console()
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    parser.add_argument("--prompt", default="", help="מונחים ושמות לשיפור הדיוק")
    parser.add_argument("--out", default=None, help="בסיס נתיב הפלט (ברירת מחדל: ליד הווידאו)")
    args = parser.parse_args()

    if not os.environ.get("OPENAI_API_KEY"):
        print("שגיאה: משתנה הסביבה OPENAI_API_KEY לא מוגדר", file=sys.stderr)
        sys.exit(1)
    if not os.path.isfile(args.video):
        print(f"שגיאה: הקובץ לא נמצא: {args.video}", file=sys.stderr)
        sys.exit(1)

    from openai import OpenAI
    client = OpenAI()

    ffmpeg = find_ffmpeg()
    ffprobe = find_ffprobe()
    duration = get_duration(ffprobe, args.video)
    base = args.out or os.path.splitext(args.video)[0]

    with tempfile.TemporaryDirectory() as tmp:
        audio = os.path.join(tmp, "audio.mp3")
        print(f"מחלץ אודיו ({duration:.0f} שניות)...")
        extract_audio(ffmpeg, args.video, audio)

        if os.path.getsize(audio) <= MAX_AUDIO_BYTES:
            print("מתמלל עם Whisper API...")
            merged = transcribe_file(client, audio, args.prompt)
        else:
            # אודיו ארוך: תמלול בחלקים והזחת זמנים
            merged = {"segments": [], "words": [], "text": ""}
            n_chunks = int(duration // CHUNK_SECONDS) + 1
            for i in range(n_chunks):
                start = i * CHUNK_SECONDS
                chunk = os.path.join(tmp, f"chunk{i}.mp3")
                extract_audio(ffmpeg, args.video, chunk, start=start, length=CHUNK_SECONDS)
                print(f"מתמלל חלק {i + 1}/{n_chunks}...")
                part = shift_times(transcribe_file(client, chunk, args.prompt), start)
                merged["segments"] += part.get("segments") or []
                merged["words"] += part.get("words") or []
                merged["text"] += (" " if merged["text"] else "") + (part.get("text") or "")

    output = {
        "video": os.path.abspath(args.video),
        "duration": duration,
        "text": merged.get("text", ""),
        "segments": [
            {"start": s["start"], "end": s["end"], "text": s["text"].strip()}
            for s in merged.get("segments") or []
        ],
        "words": [
            {"word": w["word"].strip(), "start": w["start"], "end": w["end"]}
            for w in merged.get("words") or []
        ],
    }

    json_path = base + ".transcript.json"
    txt_path = base + ".transcript.txt"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    # קובץ טקסט ממוספר - לבדיקת רון ולתיקונים (שורה לכל מקטע, לא לשנות מספור)
    with open(txt_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(output["segments"], 1):
            f.write(f"{i}| {seg['text']}\n")

    print(f"נשמר: {json_path}")
    print(f"נשמר: {txt_path}")
    print(f"מקטעים: {len(output['segments'])}, מילים: {len(output['words'])}")


if __name__ == "__main__":
    main()

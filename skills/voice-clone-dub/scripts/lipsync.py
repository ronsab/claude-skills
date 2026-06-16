#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lipsync.py -- סנכרון שפתיים של הדמות לאודיו החדש (קול רון) דרך Sync.so

שימוש (קבצים מקומיים -- מקודדים כ-data URL, מתאים לקבצים קטנים):
    python run.py lipsync.py --video clip.mp4 --audio voice_out.mp3 --output final.mp4 --json

שימוש (URLs ציבוריים -- מומלץ לקבצים גדולים):
    python run.py lipsync.py --video-url https://... --audio-url https://... --output final.mp4

פרמטרים:
    --model       lipsync-2 (ברירת מחדל) | lipsync-2-pro | sync-3
    --sync-mode   loop | bounce | cut_off | silence | remap (אופציונלי; טיפול בהפרש אורך)
    --timeout     שניות מקסימום להמתנה (ברירת מחדל 900)

מפתח: SYNC_SO_API_KEY (משתנה סביבה).
הערה: Sync.so דורש קלט כ-URL או data URL. קבצים גדולים -> העלה לאחסון ציבורי
והעבר --video-url/--audio-url. ראה references/api_notes.md.
"""

import argparse
import base64
import json
import mimetypes
import os
import sys
import time

from _util import setup_console, require_env

API_BASE = "https://api.sync.so/v2"
VALID_MODELS = ["lipsync-2", "lipsync-2-pro", "sync-3", "lipsync-1.9.0-beta"]


def to_data_url(path):
    mime, _ = mimetypes.guess_type(path)
    if not mime:
        mime = "application/octet-stream"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def resolve_input(url, local, kind):
    if url:
        return url
    if local:
        if not os.path.exists(local):
            raise FileNotFoundError(f"{kind} לא קיים: {local}")
        return to_data_url(local)
    raise ValueError(f"חסר קלט {kind} (--{kind}-url או --{kind})")


def output_result(data, as_json):
    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    elif data.get("status") == "success":
        print("\n" + "=" * 50)
        print("  סנכרון השפתיים הושלם!")
        print("=" * 50)
        print(f"  קובץ סופי: {data['path']}")
        print(f"  job id:    {data['job_id']}")
        print("=" * 50 + "\n")
    else:
        print(f"שגיאה: {data.get('error')}", file=sys.stderr)


def main():
    setup_console()
    parser = argparse.ArgumentParser(description="סנכרון שפתיים דרך Sync.so")
    parser.add_argument("--video", help="קובץ וידאו מקומי")
    parser.add_argument("--audio", help="קובץ אודיו מקומי (קול רון)")
    parser.add_argument("--video-url", help="URL ציבורי לווידאו")
    parser.add_argument("--audio-url", help="URL ציבורי לאודיו")
    parser.add_argument("--output", default="final_lipsync.mp4", help="נתיב פלט")
    parser.add_argument("--model", default="lipsync-2", choices=VALID_MODELS)
    parser.add_argument("--sync-mode", help="loop|bounce|cut_off|silence|remap")
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--poll-interval", type=int, default=10)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    api_key = require_env("SYNC_SO_API_KEY", "https://app.sync.so (Dashboard -> API keys)")

    try:
        import requests
    except Exception as e:
        output_result({"status": "error", "error": f"requests לא מותקן: {e}"}, args.json)
        return 1

    try:
        video_in = resolve_input(args.video_url, args.video, "video")
        audio_in = resolve_input(args.audio_url, args.audio, "audio")
    except (FileNotFoundError, ValueError) as e:
        output_result({"status": "error", "error": str(e)}, args.json)
        return 1

    headers = {"x-api-key": api_key, "Content-Type": "application/json"}
    body = {
        "model": args.model,
        "input": [
            {"type": "video", "url": video_in},
            {"type": "audio", "url": audio_in},
        ],
    }
    if args.sync_mode:
        body["options"] = {"sync_mode": args.sync_mode}

    # יצירת ה-job
    try:
        if not args.json:
            print(f"שולח job ל-Sync.so (model={args.model})...")
        r = requests.post(f"{API_BASE}/generate", headers=headers, json=body, timeout=120)
        if r.status_code not in (200, 201):
            output_result({"status": "error", "error": f"יצירת job נכשלה ({r.status_code}): {r.text[:500]}"}, args.json)
            return 1
        job = r.json()
        job_id = job.get("id") or job.get("jobId")
        if not job_id:
            output_result({"status": "error", "error": f"לא התקבל job id: {job}"}, args.json)
            return 1
    except Exception as e:
        output_result({"status": "error", "error": f"שגיאת רשת ביצירת job: {e}"}, args.json)
        return 1

    # polling עד סיום
    deadline = time.time() + args.timeout
    output_url = None
    while time.time() < deadline:
        time.sleep(args.poll_interval)
        try:
            s = requests.get(f"{API_BASE}/generate/{job_id}", headers=headers, timeout=60)
            data = s.json()
        except Exception as e:
            if not args.json:
                print(f"  אזהרה: בדיקת סטטוס נכשלה, ממשיך... ({e})")
            continue
        status = (data.get("status") or "").upper()
        if not args.json:
            print(f"  סטטוס: {status}")
        if status == "COMPLETED":
            output_url = data.get("outputUrl") or data.get("output_url")
            break
        if status in ("FAILED", "REJECTED", "CANCELED", "ERROR"):
            output_result({"status": "error", "error": f"ה-job נכשל: {data.get('error') or data}"}, args.json)
            return 1

    if not output_url:
        output_result({"status": "error", "error": f"timeout/לא התקבל פלט אחרי {args.timeout} שניות (job {job_id})"}, args.json)
        return 1

    # הורדת התוצאה
    try:
        if not args.json:
            print("מוריד את הווידאו הסופי...")
        dl = requests.get(output_url, timeout=300)
        dl.raise_for_status()
        with open(args.output, "wb") as f:
            f.write(dl.content)
    except Exception as e:
        output_result({"status": "error", "error": f"הורדת התוצאה נכשלה: {e} (URL: {output_url})"}, args.json)
        return 1

    output_result({
        "status": "success",
        "path": os.path.abspath(args.output),
        "job_id": job_id,
        "output_url": output_url,
    }, args.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())

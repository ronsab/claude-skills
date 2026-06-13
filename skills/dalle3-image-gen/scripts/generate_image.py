#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_image.py - יצירת תמונות עם DALL-E 3 של OpenAI.

הסקריפט משתמש רק בספריית התקן (urllib) - אין צורך להתקין openai.
דורש משתנה סביבה OPENAI_API_KEY.

דוגמת הרצה:
  python generate_image.py --prompt "חתול אסטרונאוט בחלל, צבעוני" --size 1792x1024 --quality hd --style vivid
"""

import argparse
import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error

API_URL = "https://api.openai.com/v1/images/generations"

# DALL-E 3 מקבל רק את שלושת הגדלים האלה
VALID_SIZES = {"1024x1024", "1792x1024", "1024x1792"}

# מיפוי גמיש: ערכי quality מסגנונות אחרים -> הערכים האמיתיים של DALL-E 3
QUALITY_MAP = {
    "low": "standard",
    "medium": "standard",
    "standard": "standard",
    "auto": "standard",
    "high": "hd",
    "hd": "hd",
}


def build_args():
    p = argparse.ArgumentParser(description="DALL-E 3 image generator")
    p.add_argument("--prompt", required=True, help="תיאור מפורט של התמונה")
    p.add_argument("--size", default="1024x1024",
                   help="1024x1024 (ריבוע) | 1792x1024 (לרוחב) | 1024x1792 (לאורך)")
    p.add_argument("--quality", default="standard",
                   help="standard | hd (גם low/medium/high/auto יתורגמו)")
    p.add_argument("--style", default="natural", choices=["natural", "vivid"],
                   help="natural=ריאליסטי | vivid=צבעוני וסטיליזציה")
    p.add_argument("--n", type=int, default=1,
                   help="מספר תמונות (DALL-E 3 מייצר אחת בכל קריאה; n>1 = מספר קריאות)")
    p.add_argument("--response-format", default="url", choices=["url", "b64_json"],
                   help="url = קישור זמני (פג אחרי שעה) | b64_json = להורדה מקומית")
    p.add_argument("--out-dir", default=".",
                   help="תיקיית פלט לשמירת התמונות (כשמשתמשים ב-b64_json)")
    return p.parse_args()


def normalize(args):
    # תיקון גודל לא חוקי - DALL-E 3 ייכשל אחרת
    if args.size not in VALID_SIZES:
        sys.stderr.write(
            f"[אזהרה] גודל '{args.size}' לא נתמך ב-DALL-E 3. "
            f"נופל חזרה ל-1024x1024. גדלים חוקיים: {sorted(VALID_SIZES)}\n"
        )
        args.size = "1024x1024"

    q = args.quality.lower()
    if q not in QUALITY_MAP:
        sys.stderr.write(f"[אזהרה] quality '{args.quality}' לא מוכר. משתמש ב-standard.\n")
        q = "standard"
    args.quality = QUALITY_MAP[q]
    return args


def call_api(api_key, prompt, size, quality, style, response_format):
    payload = json.dumps({
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,  # DALL-E 3 תמיד 1 לבקשה
        "size": size,
        "quality": quality,
        "style": style,
        "response_format": response_format,
    }).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        sys.stderr.write(
            "שגיאה: לא נמצא OPENAI_API_KEY בסביבה.\n"
            "הגדר אותו לפני ההרצה. ב-Windows:  setx OPENAI_API_KEY \"sk-...\"\n"
            "(אחרי setx צריך לפתוח טרמינל חדש)\n"
        )
        sys.exit(1)

    args = normalize(build_args())
    os.makedirs(args.out_dir, exist_ok=True)

    results = []
    for i in range(max(1, args.n)):
        try:
            data = call_api(api_key, args.prompt, args.size, args.quality,
                            args.style, args.response_format)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            sys.stderr.write(f"שגיאת API ({e.code}): {body}\n")
            sys.exit(2)
        except urllib.error.URLError as e:
            sys.stderr.write(f"שגיאת רשת: {e.reason}\n")
            sys.exit(2)

        item = data["data"][0]
        # DALL-E 3 מחזיר גם revised_prompt - הניסוח המשופר שהמודל בנה בפועל
        revised = item.get("revised_prompt", "")

        if args.response_format == "b64_json":
            img_bytes = base64.b64decode(item["b64_json"])
            ts = int(time.time())
            path = os.path.join(args.out_dir, f"dalle3_{ts}_{i+1}.png")
            with open(path, "wb") as f:
                f.write(img_bytes)
            results.append({"file": path, "revised_prompt": revised})
        else:
            results.append({"url": item["url"], "revised_prompt": revised})

    # פלט מובנה ל-stdout כדי שאפשר יהיה לקרוא אותו
    print(json.dumps({
        "model": "dall-e-3",
        "size": args.size,
        "quality": args.quality,
        "style": args.style,
        "count": len(results),
        "images": results,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

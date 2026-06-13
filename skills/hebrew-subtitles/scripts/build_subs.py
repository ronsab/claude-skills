# -*- coding: utf-8 -*-
"""
בניית קבצי כתוביות מתמלול Whisper.

תמיד נוצר SRT (קלאסי, מבוסס מקטעים). בסגנון tiktok נוצר בנוסף קובץ ASS
מבוסס זמני מילים (2-4 מילים בכל קיו, גדול במרכז-תחתית).

שימוש:
    python build_subs.py <transcript.json> [--style classic|tiktok]
                         [--corrections fixed.txt] [--width 1080] [--height 1920]

קובץ תיקונים: אותו פורמט כמו transcript.txt - "מספר| טקסט מתוקן" בכל שורה.
"""
import argparse
import json
import os
import re
import sys

from _util import setup_console

SENTENCE_END = (".", "!", "?", "…", ":")
MAX_LINE_CHARS = 42          # אורך שורה מקסימלי ב-SRT
MAX_WORDS_PER_CUE = 4        # מילים בקיו בסגנון TikTok
MAX_CUE_SECONDS = 1.6        # משך קיו מקסימלי בסגנון TikTok
PAUSE_GAP = 0.4              # הפסקת דיבור שפותחת קיו חדש


def load_corrections(path):
    # קורא קובץ תיקונים ממוספר ומחזיר מיפוי: מספר מקטע -> טקסט מתוקן
    fixes = {}
    # utf-8-sig מתעלם מ-BOM שקבצים מ-PowerShell/פנקס רשימות מכילים
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            m = re.match(r"^(\d+)\|\s?(.*)$", line.rstrip("\n"))
            if m:
                fixes[int(m.group(1))] = m.group(2).strip()
    return fixes


def apply_corrections(data, fixes):
    # מחיל תיקונים על מקטעים; מקטע שתוקן מקבל מילים חדשות בפיזור אחיד על ציר הזמן
    corrected_idx = set()
    for i, seg in enumerate(data["segments"], 1):
        if i in fixes and fixes[i] != seg["text"]:
            seg["text"] = fixes[i]
            corrected_idx.add(i - 1)

    if not corrected_idx:
        return data

    new_words = []
    for i, seg in enumerate(data["segments"]):
        if i in corrected_idx:
            tokens = seg["text"].split()
            if not tokens:
                continue
            step = (seg["end"] - seg["start"]) / len(tokens)
            for j, tok in enumerate(tokens):
                new_words.append({
                    "word": tok,
                    "start": seg["start"] + j * step,
                    "end": seg["start"] + (j + 1) * step,
                })
        else:
            # שומר את זמני המילים המקוריים של מקטע שלא תוקן
            for w in data["words"]:
                mid = (w["start"] + w["end"]) / 2
                if seg["start"] <= mid < seg["end"]:
                    new_words.append(w)
    data["words"] = sorted(new_words, key=lambda w: w["start"])
    return data


# ---------- SRT קלאסי ----------

def merge_short_segments(segments):
    merged = []
    for seg in segments:
        if (merged
                and seg["end"] - seg["start"] < 1.0
                and len(merged[-1]["text"]) + len(seg["text"]) <= 2 * MAX_LINE_CHARS
                and seg["start"] - merged[-1]["end"] < 0.5):
            merged[-1]["end"] = seg["end"]
            merged[-1]["text"] = (merged[-1]["text"] + " " + seg["text"]).strip()
        else:
            merged.append(dict(seg))
    return merged


def split_line(text):
    # שורה ארוכה נשברת לשתיים בנקודת הרווח הקרובה לאמצע
    if len(text) <= MAX_LINE_CHARS:
        return text
    mid = len(text) // 2
    spaces = [m.start() for m in re.finditer(" ", text)]
    if not spaces:
        return text
    best = min(spaces, key=lambda p: abs(p - mid))
    return text[:best] + "\n" + text[best + 1:]


def fmt_srt_time(t):
    ms = int(round(t * 1000))
    h, rem = divmod(ms, 3600000)
    m, rem = divmod(rem, 60000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(segments, path):
    with open(path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, 1):
            f.write(f"{i}\n{fmt_srt_time(seg['start'])} --> {fmt_srt_time(seg['end'])}\n")
            f.write(split_line(seg["text"]) + "\n\n")


# ---------- ASS בסגנון TikTok ----------

def build_word_cues(words):
    cues = []
    current = []
    for i, w in enumerate(words):
        current.append(w)
        is_last = i == len(words) - 1
        gap_next = (words[i + 1]["start"] - w["end"]) if not is_last else 0
        too_long = (w["end"] - current[0]["start"]) >= MAX_CUE_SECONDS
        ends_sentence = w["word"].endswith(SENTENCE_END)
        if (is_last or len(current) >= MAX_WORDS_PER_CUE
                or gap_next > PAUSE_GAP or too_long or ends_sentence):
            start = current[0]["start"]
            end = max(current[-1]["end"], start + 0.3)
            if not is_last:
                end = min(end, words[i + 1]["start"])
            cues.append({"start": start, "end": end,
                         "text": " ".join(x["word"] for x in current)})
            current = []
    return cues


def fmt_ass_time(t):
    cs = int(round(t * 100))
    h, rem = divmod(cs, 360000)
    m, rem = divmod(rem, 6000)
    s, cs = divmod(rem, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def write_ass(cues, path, width, height, title=None, duration=None):
    fontsize = round(min(width, height) * 0.075)
    outline = max(2, round(fontsize * 0.07))
    # אנכי: מעל ממשק TikTok/Reels; אופקי: נמוך יותר
    marginv = round(height * (0.22 if height > width else 0.12))
    # כותרת קבועה למעלה: קטנה מהכתוביות, מרווח מהקצה העליון
    title_size = round(min(width, height) * 0.05)
    title_margin = round(height * 0.07)
    title_outline = max(2, round(title_size * 0.07))
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: TikTok,Heebo,{fontsize},&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,{outline},1,2,40,40,{marginv},1
Style: Title,Heebo,{title_size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,2,0,1,{title_outline},1,8,40,40,{title_margin},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(header)
        if title and duration:
            f.write(f"Dialogue: 1,{fmt_ass_time(0)},{fmt_ass_time(duration)},"
                    f"Title,,0,0,0,,{title}\n")
        for c in cues:
            text = c["text"].replace("\n", r"\N")
            f.write(f"Dialogue: 0,{fmt_ass_time(c['start'])},{fmt_ass_time(c['end'])},"
                    f"TikTok,,0,0,0,,{text}\n")


def main():
    setup_console()
    parser = argparse.ArgumentParser()
    parser.add_argument("transcript")
    parser.add_argument("--style", choices=["classic", "tiktok"], default="classic")
    parser.add_argument("--corrections", default=None)
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1920)
    parser.add_argument("--title", default=None, help="כותרת קבועה בחלק העליון (למשל שם העסק)")
    parser.add_argument("--out-base", default=None)
    args = parser.parse_args()

    with open(args.transcript, encoding="utf-8") as f:
        data = json.load(f)
    if not data.get("segments"):
        print("שגיאה: אין מקטעים בתמלול", file=sys.stderr)
        sys.exit(1)

    if args.corrections:
        data = apply_corrections(data, load_corrections(args.corrections))

    base = args.out_base or args.transcript.replace(".transcript.json", "")

    srt_path = base + ".he.srt"
    write_srt(merge_short_segments(data["segments"]), srt_path)
    print(f"נשמר: {srt_path}")

    if args.style == "tiktok":
        if not data.get("words"):
            print("שגיאה: אין זמני מילים בתמלול - אי אפשר לבנות סגנון TikTok", file=sys.stderr)
            sys.exit(1)
        ass_path = base + ".tiktok.ass"
        write_ass(build_word_cues(data["words"]), ass_path, args.width, args.height,
                  title=args.title, duration=data.get("duration"))
        print(f"נשמר: {ass_path}")


if __name__ == "__main__":
    main()

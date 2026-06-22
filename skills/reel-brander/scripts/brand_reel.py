#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
brand_reel.py - מיתוג והידוק ריל מדבר.

מוסיף לסרטון קיים (אנכי, מדבר): כרטיס פתיחה (hook), כרטיס סיום ממותג,
פס מיתוג צדי, והסרת שתיקות (jump-cuts). כל שלב אופציונלי.

דוגמה:
  python brand_reel.py in.mp4 --out out.mp4 \
    --endcard "RON DIGITAL STUDIO|Link in BIO" --endcard-color navy \
    --intro "רוב העסקים נופלים|לא מהסיבה שחשבת" \
    --bar 6B21A8 --trim-silence

הערות:
  - צבעי ASS הם בפורמט BGR (&HAABBGGRR), לא RGB. ראה מילון COLORS.
  - שורה מעורבת עברית+אנגלית נעטפת אוטומטית ב-U+202B/U+202C, אחרת libass
    הופך את סדר המילים (המילה העברית מתהפכת).
"""
import argparse, os, sys, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _util import init_utf8, find_tool, run

init_utf8()

FFMPEG  = find_tool("ffmpeg")
FFPROBE = find_tool("ffprobe")
FONTSDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts")
FONTSDIR = os.path.abspath(FONTSDIR).replace("\\", "/")

if not FFMPEG or not FFPROBE:
    print("שגיאה: ffmpeg/ffprobe לא נמצאו. התקן: winget install Gyan.FFmpeg")
    sys.exit(1)

# צבעים: title + sub (CTA) בפורמט ASS BGR. RGB→BGR: #1E40AF → &H00AF401E
COLORS = {
    "navy":  {"title": "&H00AF401E", "sub": "&H00F6823B", "line": "0x1E40AF"},  # #1E40AF / #3B82F6
    "gold":  {"title": "&H0000D7FF", "sub": "&H0030A5D7", "line": "0xD4AF37"},  # #FFD700 זהב
    "white": {"title": "&H00FFFFFF", "sub": "&H00C8C8C8", "line": "0xFFFFFF"},
}

HEB = re.compile(r"[֐-׿]")
LAT = re.compile(r"[A-Za-z]")


def bidi_wrap(text):
    """עטיפת שורה מעורבת עברית+אנגלית ב-RLE/PDF לסדר מילים נכון."""
    if HEB.search(text) and LAT.search(text):
        return "‫" + text + "‬"
    return text


def probe(path):
    r = run([FFPROBE, "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height",
             "-show_entries", "format=duration", "-of", "json", path])
    d = json.loads(r.stdout)
    s = d["streams"][0]
    return int(s["width"]), int(s["height"]), float(d["format"]["duration"])


def esc_filter_path(p):
    """escape לנתיב Windows בתוך filtergraph (drive colon)."""
    s = p.replace("\\", "/")
    if len(s) > 1 and s[1] == ":":
        s = s[0] + "\\:" + s[2:]
    return s


def make_card(line1, line2, color, duration, w, h, out, tmp_ass, divider=False):
    """כרטיס מסך-שחור עם 2 שורות ממורכזות + קו מפריד אופציונלי."""
    c = COLORS[color]
    y_title = int(h * 0.445)
    y_sub   = int(h * 0.555)
    y_line  = int(h * 0.50)
    fs_title = int(h * 0.056)   # ~72 ב-1280
    fs_sub   = int(h * 0.031)   # ~40 ב-1280

    ass = f"""\
[Script Info]
ScriptType: v4.00+
PlayResX: {w}
PlayResY: {h}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Title,Heebo,{fs_title},{c['title']},&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,3,0,1,0,0,5,0,0,0,1
Style: Sub,Heebo,{fs_sub},{c['sub']},&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,2,0,1,0,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,{fmt_t(duration)},Title,,0,0,0,,{{\\an5\\pos({w//2},{y_title})}}{bidi_wrap(line1)}
"""
    if line2:
        ass += (f"Dialogue: 0,0:00:00.00,{fmt_t(duration)},Sub,,0,0,0,,"
                f"{{\\an5\\pos({w//2},{y_sub})}}{bidi_wrap(line2)}\n")

    with open(tmp_ass, "w", encoding="utf-8-sig") as f:
        f.write(ass)

    vf = []
    if divider:
        lw = int(w * 0.55)
        lx = (w - lw) // 2
        vf.append(f"drawbox=x={lx}:y={y_line}:w={lw}:h=2:color={c['line']}@0.8:t=fill")
    vf.append(f"subtitles='{esc_filter_path(tmp_ass)}':fontsdir='{esc_filter_path(FONTSDIR)}'")

    run([FFMPEG, "-y",
         "-f", "lavfi", "-i", f"color=c=black:size={w}x{h}:duration={duration},format=yuv420p",
         "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
         "-t", str(duration),
         "-vf", ",".join(vf),
         "-c:v", "libx264", "-preset", "fast", "-crf", "17",
         "-c:a", "aac", "-b:a", "128k", out],
        label=f"כרטיס: {line1}")


def fmt_t(s):
    h = int(s // 3600); m = int((s % 3600) // 60); sec = s % 60
    return f"{h}:{m:02d}:{sec:05.2f}"


def trim_silence(src, out, w, h):
    """הסרת שתיקות (jump-cuts) - לסרטון מדבר. מזהה שתיקות ומחבר קטעי דיבור."""
    import subprocess
    r = subprocess.run([FFMPEG, "-i", src, "-af", "silencedetect=n=-33dB:d=0.35",
                        "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    starts = list(map(float, re.findall(r"silence_start: (\S+)", r.stderr)))
    ends   = list(map(float, re.findall(r"silence_end: (\S+)", r.stderr)))
    _, _, dur = probe(src)
    sil = list(zip(starts, ends))
    if not sil:
        print("  אין שתיקות לחיתוך - הסרטון רצוף")
        run([FFMPEG, "-y", "-i", src, "-c", "copy", out])
        return
    segs, prev = [], 0.0
    for ss, se in sil:
        if ss - prev > 0.12:
            segs.append((prev, ss))
        prev = se
    if dur - prev > 0.12:
        segs.append((prev, dur))
    lst = out + ".segs.txt"
    with open(lst, "w", encoding="utf-8") as f:
        for s, e in segs:
            f.write(f"file '{src}'\ninpoint {s:.3f}\noutpoint {e:.3f}\n")
    run([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", lst,
         "-c:v", "libx264", "-preset", "fast", "-crf", "18",
         "-c:a", "aac", "-b:a", "192k", out], label="חיתוך שתיקות")
    _, _, nd = probe(out)
    print(f"  קוצר ל-{nd:.1f}s (מתוך {dur:.1f}s)")
    os.remove(lst)


def add_bar(src, out, color, w, h):
    """פס מיתוג צדי משמאל."""
    bw = max(8, int(w * 0.014))
    run([FFMPEG, "-y", "-i", src,
         "-vf", f"drawbox=x=0:y=0:w={bw}:h=ih:color=0x{color}@1.0:t=fill",
         "-c:v", "libx264", "-preset", "fast", "-crf", "18",
         "-c:a", "copy", out], label="פס מיתוג")


def concat(parts, out):
    lst = out + ".concat.txt"
    with open(lst, "w", encoding="utf-8") as f:
        for p in parts:
            f.write(f"file '{p}'\n")
    run([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", lst,
         "-c:v", "libx264", "-preset", "fast", "-crf", "17",
         "-c:a", "aac", out], label="איחוד סופי")
    os.remove(lst)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--out", required=True)
    ap.add_argument("--endcard", help='כרטיס סיום: "TITLE|CTA"')
    ap.add_argument("--endcard-color", default="navy", choices=list(COLORS))
    ap.add_argument("--endcard-seconds", type=float, default=4.0)
    ap.add_argument("--intro", help='כרטיס פתיחה: "LINE1|LINE2"')
    ap.add_argument("--intro-color", default="white", choices=list(COLORS))
    ap.add_argument("--intro-seconds", type=float, default=2.0)
    ap.add_argument("--bar", help="צבע פס מיתוג צדי (hex בלי #, למשל 6B21A8)")
    ap.add_argument("--trim-silence", action="store_true")
    args = ap.parse_args()

    work = os.path.dirname(os.path.abspath(args.out)) or "."
    tmp = []
    w, h, _ = probe(args.input)
    cur = args.input

    if args.trim_silence:
        t = os.path.join(work, "_br_trim.mp4"); tmp.append(t)
        trim_silence(cur, t, w, h); cur = t

    if args.bar:
        t = os.path.join(work, "_br_bar.mp4"); tmp.append(t)
        add_bar(cur, t, args.bar, w, h); cur = t

    parts = []
    if args.intro:
        l1, _, l2 = args.intro.partition("|")
        t = os.path.join(work, "_br_intro.mp4"); a = os.path.join(work, "_br_intro.ass")
        tmp += [t, a]
        make_card(l1, l2, args.intro_color, args.intro_seconds, w, h, t, a, divider=False)
        parts.append(t)

    parts.append(cur)

    if args.endcard:
        l1, _, l2 = args.endcard.partition("|")
        t = os.path.join(work, "_br_end.mp4"); a = os.path.join(work, "_br_end.ass")
        tmp += [t, a]
        make_card(l1, l2, args.endcard_color, args.endcard_seconds, w, h, t, a, divider=True)
        parts.append(t)

    if len(parts) == 1 and parts[0] != args.input:
        # רק trim/bar בלי כרטיסים - העתק לפלט
        run([FFMPEG, "-y", "-i", parts[0], "-c", "copy", args.out])
    elif len(parts) == 1:
        print("שגיאה: לא נבחרה אף פעולה (--endcard/--intro/--bar/--trim-silence)")
        sys.exit(2)
    else:
        concat(parts, args.out)

    for p in tmp:
        if os.path.exists(p):
            os.remove(p)
    print(f"\n✓ מוכן: {args.out}")


if __name__ == "__main__":
    main()

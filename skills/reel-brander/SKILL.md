---
name: reel-brander
description: מיתוג והידוק ריל מדבר (talking-head) קיים - הוספת כרטיס פתיחה (hook), כרטיס סיום ממותג עם שם העסק ו-CTA, פס מיתוג צדי, והסרת שתיקות אוטומטית (jump-cuts). Use when Ron wants to add a branded intro/outro/end card to a video, add "Link in BIO" / business-name closing screen, add a hook opening card, add a side branding bar, or tighten a talking-head video by cutting silences. Triggers on "מסך סיום", "כרטיס סיום", "מסך פתיחה", "hook בהתחלה", "פס מיתוג", "תוסיף את שם העסק בסוף", "Link in BIO", "תהדק את הסרטון", "תחתוך שתיקות". NOT for subtitles (hebrew-subtitles), merging clips (video-merge), screen-recording-to-reel (screencast-to-reel), or speed-up/ramp/carousel-split (social-video-editor).
---

# reel-brander - מיתוג והידוק ריל מדבר

מוסיף נגיעות הפקה ממותגות לסרטון אנכי קיים שבו מישהו מדבר למצלמה (talking-head): כרטיס פתיחה, כרטיס סיום, פס מיתוג, והסרת שתיקות. כל רכיב אופציונלי ומופעל ב-flag.

## מתי להשתמש - וגבולות מול שאר סקילי הווידאו (כלל ברזל: אין חפיפה)

| המשימה | הסקיל הנכון |
|--------|-------------|
| כרטיס פתיחה/סיום ממותג, פס מיתוג, הסרת שתיקות לסרטון מדבר | **reel-brander** (זה) |
| כתוביות עברית (תמלול + צריבה) | `hebrew-subtitles` |
| איחוד כמה קליפים נפרדים לסרטון אחד | `video-merge` |
| הקלטת מסך/דמו → ריל ממותג (רקע מטושטש + מוזיקה) | `screencast-to-reel` |
| האצה / Speed Ramp / פיצול לקרוסלה | `social-video-editor` |

**הגבול הקריטי - הסרת שתיקות מול Speed Ramp:**
- `reel-brander --trim-silence` = סרטון **מדבר** (יש דיבור, חותכים את ההפסקות בין משפטים).
- `social-video-editor ramp` = הקלטת מסך/דמו **בלי דיבור** (מאיצים קטעי המתנה). ההכרעה לפי סוג התוכן, לא לפי "לקצר".

**סדר זרימה מומלץ:** קודם `hebrew-subtitles` (כתוביות על הגלם), אחר כך `reel-brander` (כרטיסים + פס על התוצאה הצרובה). כך הכתוביות לא רצות על כרטיסי הפתיחה/סיום.

## דרישות סביבה
- `ffmpeg` + `ffprobe` - הסקריפט מאתר לבד (PATH או WinGet). אם חסר: `winget install Gyan.FFmpeg`.
- Python - נתיב מלא (alias שבור ב-Windows): `C:\Users\USER\AppData\Local\Programs\Python\Python311\python.exe`
- הפונט `fonts/Heebo.ttf` מצורף לסקיל (עצמאי, לא תלוי ב-hebrew-subtitles).

## שימוש

```
python.exe brand_reel.py "<input.mp4>" --out "<output.mp4>" \
  [--endcard "TITLE|CTA"] [--endcard-color navy|gold|white] [--endcard-seconds 4] \
  [--intro "LINE1|LINE2"] [--intro-color white|navy|gold] [--intro-seconds 2] \
  [--bar 6B21A8] \
  [--trim-silence]
```

- `--endcard "RON DIGITAL STUDIO|Link in BIO"` - מסך שחור, כותרת Bold + קו מפריד + CTA. הפרדה ב-`|`.
- `--intro "רוב העסקים נופלים|לא מהסיבה שחשבת"` - כרטיס hook פתיחה (בלי קו מפריד).
- `--bar 6B21A8` - פס מיתוג צדי משמאל (hex בלי #).
- `--trim-silence` - חיתוך שתיקות (רק לסרטון מדבר).
- אפשר לשלב כמה דגלים בריצה אחת. הסדר בפלט: intro → (גוף הסרטון אחרי trim/bar) → endcard.

## ידע טכני חשוב (אל תשנה בלי להבין)

- **צבעי ASS בפורמט BGR** (`&HAABBGGRR`), לא RGB. דוגמה: נייבי `#1E40AF` → `&H00AF401E`. מילון `COLORS` ב-`brand_reel.py` מחזיק navy/gold/white מוכנים.
- **bidi לטקסט מעורב עברית+אנגלית**: שורה כמו "לינק ב-BIO" נעטפת אוטומטית ב-U+202B (RLE) ו-U+202C (PDF). בלי זה libass מניח כיוון פסקה LTR והמילה העברית מתהפכת. הפונקציה `bidi_wrap` מטפלת בזה. שורה עברית טהורה או אנגלית טהורה לא צריכה עטיפה.
- ממדי הסרטון נשלפים אוטומטית (ffprobe) והמיקומים/גדלים מחושבים יחסית לגובה - עובד לכל רזולוציה אנכית.

## אימות ויזואלי (חובה לפני מסירה)
חלץ פריים מכל כרטיס שנוצר ובדוק:

```
ffmpeg -y -ss <שניות> -i "<output.mp4>" -frames:v 1 frame.png
```

- כרטיס סיום: צבע נכון, כותרת + קו + CTA, טקסט לא הפוך (כולל מקרה מעורב עברית+אנגלית).
- אם יש עברית: מימין לשמאל, אותיות לא הפוכות.
- trim-silence: ודא שהמשך התקצר ושאין חיתוכים באמצע מילה.

## פתרון תקלות
- `מילה עברית הפוכה בכרטיס` - ודא ש-`bidi_wrap` רץ על השורה (שורה מעורבת עברית+אנגלית). חלופה: כתוב את השורה כולה באנגלית או כולה בעברית.
- `עברית מרובעת/הפוכה בצריבה` - ודא ש-`fonts/Heebo.ttf` קיים בתיקיית הסקיל.
- `ffmpeg לא נמצא` - `winget install Gyan.FFmpeg`.

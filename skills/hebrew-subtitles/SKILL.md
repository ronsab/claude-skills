---
name: hebrew-subtitles
description: כתוביות עברית אוטומטיות לסרטונים של רון - תמלול מדויק עם OpenAI Whisper API וצריבה עם ffmpeg. Use when Ron asks to add Hebrew subtitles to a video, transcribe a video, or says "תוסיף כתוביות", "כתוביות לסרטון", "תתמלל את הסרטון", "תעשה סאבים". Produces both an SRT file and a burned-in MP4, in TikTok/Reels style or classic style.
---

# hebrew-subtitles - כתוביות עברית לסרטונים

המרת סרטון שבו רון מדבר עברית לשני תוצרים: קובץ `SRT` + סרטון `MP4` עם כתוביות צרובות.

אם רון רוצה לאחד כמה קליפים לסרטון אחד - קודם הסקיל `video-merge`, ואז כתוביות על התוצאה המאוחדת (תמלול אחד על הכל).

## דרישות סביבה (לבדוק לפני ריצה ראשונה)

- `OPENAI_API_KEY` - חייב להיות מוגדר כמשתנה סביבה. אם חסר: עצור ובקש מרון מפתח. **אסור להמציא מפתח**
- `ffmpeg` - הסקריפטים מאתרים אותו לבד (PATH או תיקיית WinGet). אם חסר: `winget install Gyan.FFmpeg`
- Python - השתמש תמיד בנתיב המלא (alias של python שבור ב-Windows של רון):

```
C:\Users\USER\AppData\Local\Programs\Python\Python311\python.exe
```

- הרץ סקריפטים מתוך תיקיית `scripts` של הסקיל (בגלל import של `_util`)

## זרימת עבודה (8 שלבים)

### 1. אימות הקובץ
ודא שקובץ הווידאו קיים. שלוף ממדים ומשך עם ffprobe:

```
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -show_entries format=duration -of json <video>
```

### 2. שאלת סגנון
שאל את רון (אם לא ציין): TikTok/Reels (מילים גדולות במרכז-תחתית) או קלאסי (שורות בתחתית)?
בנוסף שאל אם יש מונחים/שמות מיוחדים בסרטון (שמות מותגים, מונחים טכניים) - הם משפרים את דיוק התמלול.

### 3. תמלול
עלות זניחה: בערך 2 אגורות לדקת וידאו.

```
python.exe transcribe.py "<video.mp4>" --prompt "RON DIGITAL, מונחים נוספים..."
```

פלט: `<video>.transcript.json` + `<video>.transcript.txt` (שורות ממוספרות).

### 4. שלב אישור (חובה - לא לדלג)
הצג לרון את התמלול המלא מתוך `transcript.txt` - **תמיד בבלוק קוד נפרד** (ציטוט markdown לא תמיד מוצג אצלו).
לפני ההצגה, סרוק בעצמך את התמלול וסמן לרון מילים שנראות כמו טעות תמלול (מילה לא קיימת בעברית, מונח עסקי משובש כמו "הלד" במקום "הליד") עם הצעת תיקון - אל תחכה שרון ימצא לבד.
רון מאשר או נותן תיקונים. אם יש תיקונים: צור קובץ תיקונים באותו פורמט בדיוק (`מספר| טקסט`) רק עם השורות שהשתנו, למשל `fixes.txt` (כתיבה עם Write - לא דרך PowerShell שמוסיף BOM).

### 5. בניית כתוביות

```
python.exe build_subs.py "<video>.transcript.json" --style tiktok --width <W> --height <H> [--corrections fixes.txt] [--title "שם העסק"]
```

- SRT נוצר תמיד: `<video>.he.srt`
- בסגנון tiktok נוצר גם: `<video>.tiktok.ass`
- `--width/--height` חייבים להיות הממדים האמיתיים מ-ffprobe (שלב 1)
- `--title` - כותרת קבועה בחלק העליון לאורך כל הסרטון (למשל שם העסק). עובד רק בסגנון tiktok. אם רון מבקש כותרת בסגנון קלאסי - בנה ASS עם tiktok וסביר שזה מה שהוא רוצה, או הסבר שהיכולת קיימת רק שם

### 6. צריבה

```
python.exe burn.py "<video.mp4>" "<קובץ הכתוביות>"
```

- סגנון TikTok: העבר את קובץ ה-`.ass`
- סגנון קלאסי: העבר את קובץ ה-`.srt`
- פלט: `<video>_subtitled.mp4`

### 7. אימות ויזואלי (חובה)
חלץ 2-3 פריימים מנקודות זמן שבהן יש כתובית (קח זמנים מה-JSON) והצג אותם:

```
ffmpeg -y -ss <שניות> -i <video_subtitled.mp4> -frames:v 1 frame1.png
```

בדוק בתמונות: עברית מימין לשמאל, אותיות לא הפוכות ולא מנותקות, פיסוק במקום נכון, גודל קריא.

### 8. סיכום
דווח לרון: נתיב ה-SRT, נתיב הסרטון הצרוב, ומה נבדק.

## פתרון תקלות

- `שגיאת קידוד בעברית בקונסולה` - הסקריפטים כבר מטפלים (reconfigure ל-UTF-8). אם בכל זאת קורה, הוסף `$env:PYTHONIOENCODING="utf-8"`
- `אודיו מעל 25MB` - transcribe.py מפצל אוטומטית לחלקים של 20 דקות
- `עברית הפוכה או מרובעת בצריבה` - ודא ש-`fonts/Heebo.ttf` קיים בתיקיית הסקיל; הצריבה משתמשת ב-fontsdir
- `אין זמני מילים` - קורה רק אם שונה המודל. חובה `whisper-1` (לא gpt-4o-transcribe) - רק הוא מחזיר word timestamps

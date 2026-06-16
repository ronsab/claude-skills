---
name: voice-clone-dub
description: החלפת הקול המלאכותי בסרטוני AI של רון בקול האמיתי שלו, עם סנכרון שפתיים מדויק. רון מקליט את עצמו פעם אחת (שכפול קול ב-ElevenLabs), ואז בכל סרטון מספק טקסט משתנה שמוקרא בקולו, וה-lip-sync מתאים את שפתיי הדמות לקול החדש. Use when Ron asks to put his real voice into an AI video, dub a clip in his own voice, replace the AI voice, or says "תחליף קול בסרטון", "דיבוב בקול שלי", "הקול המלאכותי", "תסנכרן שפתיים", "voice clone", "lip sync". כלים: ElevenLabs (קול) + Sync.so (סנכרון שפתיים).
user-invokable: true
metadata:
  author: Ron Sabon
  version: "1.0.0"
---

# voice-clone-dub - הקול האמיתי של רון בסרטוני AI

רון מייצר סרטונים בכלי AI גנרטיביים (Lab Flow, Gemini/Veo) שבהם דמות שלו מדברת, אבל הקול מלאכותי.
המטרה: להקליט את הקול פעם אחת, ואז בכל סרטון לספק טקסט משתנה שמוקרא בקול של רון, עם תנועת שפתיים שמתאימה לקול החדש.

**מסלול ראשי (TTS):** רון נותן טקסט → ElevenLabs מקריא אותו בקולו → Sync.so מסנכרן את שפתיי הדמות.
**מסלול משני (S2S):** המרת האודיו המלאכותי הקיים לקול של רון תוך שמירת תזמון/אינטונציה → ואז סנכרון שפתיים.

## דרישות סביבה (לבדוק לפני ריצה ראשונה)

- `ELEVENLABS_API_KEY` - חובה. אם חסר: עצור ובקש מרון. **אסור להמציא מפתח**. (elevenlabs.io/app/settings/api-keys)
- `SYNC_SO_API_KEY` - חובה לשלב ה-lip-sync. אם חסר: עצור ובקש מרון. **אסור להמציא מפתח**. (app.sync.so → API keys)
- `RON_VOICE_ID` - מומלץ. ה-voice_id שמתקבל פעם אחת מ-`clone_voice.py`. אם לא מוגדר, יש להעביר `--voice-id`.
- `ffmpeg` - מאותר אוטומטית (PATH או WinGet). אם חסר: `winget install Gyan.FFmpeg`.
- הרץ כל סקריפט דרך `run.py` (הוא מוודא venv ותלויות):

```
python.exe run.py <script>.py [args...]
```

בריצה ראשונה `run.py` יוצר `.venv` ומתקין את `requirements.txt` (elevenlabs, requests) אוטומטית.

## שלב Setup חד-פעמי (שכפול הקול)

1. בדוק אם כבר קיים קול בחשבון:

```
python.exe run.py clone_voice.py --list
```

2. אם אין - בקש מרון הקלטה נקייה (1-3 דקות דיבור רגוע, ללא רעש רקע; לאיכות מקסימלית בעברית שקול PVC עם ~30 דק'). אפשר אודיו או וידאו (הסקריפט מחלץ אודיו לבד):

```
python.exe run.py clone_voice.py --name "Ron" --files "recording.mp3"
```

3. **נקודת אישור:** הצג לרון את ה-`voice_id` שהתקבל והנחה אותו לשמור אותו כמשתנה סביבה `RON_VOICE_ID`. הקול נשמר בחשבון ElevenLabs - לא צריך לשכפל שוב.

## זרימה לכל קליפ (מסלול ראשי - TTS)

### 1. אימות הקובץ
ודא שהקליפ קיים. שלוף משך וממדים. **בדוק מול מגבלות Sync.so** (Free tier עד 20 שניות) - אם ארוך מדי, התרע.

### 2. קבלת הטקסט
רון מספק את הטקסט לסרטון (משתנה מסרטון לסרטון). המלץ שאורך הטקסט יתאים בקירוב למשך הקליפ, אחרת האודיו ייצא ארוך/קצר מדי מהווידאו (ראה `--sync-mode` ב-`api_notes.md`).

### 3. יצירת האודיו בקול של רון

```
python.exe run.py convert_voice.py --voice-id <id> --text "<הטקסט>" --output voice_out.mp3 --json
```

(מסלול S2S: קודם `extract_audio.py "clip.mp4"`, ואז `convert_voice.py --mode s2s --audio clip.original.wav ...`.)

### 4. שלב אישור 1 (חובה - לא לדלג)
תן לרון לשמוע את `voice_out.mp3` **לפני** ה-lip-sync (שלב יקר). אם הקול/הטקסט לא טובים - תקן וחזור על שלב 3. אל תמשיך ל-lip-sync בלי אישור מפורש.

### 5. הצגת עלות ואישור
הצג לרון עלות lip-sync משוערת לפי המודל (ראה `references/pricing.md`) ובקש אישור לפני ההרצה.

### 6. סנכרון שפתיים

```
python.exe run.py lipsync.py --video "clip.mp4" --audio voice_out.mp3 --output final.mp4 --model lipsync-2 --json
```

לקבצים גדולים: העלה לאחסון ציבורי והשתמש ב-`--video-url`/`--audio-url` (ראה `api_notes.md`). בהפרש אורך גדול שקול `--sync-mode loop`.

### 7. שלב אישור 2 - אימות ויזואלי (חובה - לא לדלג)
חלץ 2-3 פריימים מנקודות דיבור והצג לרון לבדיקת סנכרון אמיתי (לא להסתפק ב"ה-API החזיר קובץ"):

```
ffmpeg -ss <שנייה> -i final.mp4 -frames:v 1 frame_<n>.png
```

### 8. סיכום
הצג: נתיב הקובץ הסופי, עלות בפועל (קרדיטים ElevenLabs + Sync.so), ומה נבדק.

## עלויות
טבלה מלאה ב-`references/pricing.md`. בקירוב $1.50-4.50 לקליפ 30 שניות (עיקר העלות ב-lip-sync).

## פתרון תקלות וסיכונים
`references/api_notes.md` - פרטי API, מגבלות אורך, הפרש אודיו↔וידאו, איכות עברית, פרטיות.
המלצה: בדוק קליפ קצר אחד מקצה לקצה לפני התחייבות לפרויקט שלם.

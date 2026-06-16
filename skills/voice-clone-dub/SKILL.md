---
name: voice-clone-dub
description: החלפת הקול המלאכותי בסרטוני AI של רון בקול האמיתי שלו, עם סנכרון שפתיים מדויק. רון מקליט את עצמו פעם אחת (שכפול קול ב-ElevenLabs), ואז בכל סרטון מספק טקסט משתנה שמוקרא בקולו, וה-lip-sync מתאים את שפתיי הדמות לקול החדש. Use when Ron asks to put his real voice into an AI video, dub a clip in his own voice, replace the AI voice, or says "תחליף קול בסרטון", "דיבוב בקול שלי", "הקול המלאכותי", "תסנכרן שפתיים", "voice clone", "lip sync". כלים: ElevenLabs (קול) + Sync.so (סנכרון שפתיים).
user-invokable: true
metadata:
  author: Ron Sabon
  version: "1.1.0"
---

# voice-clone-dub - הקול האמיתי של רון בסרטוני AI

רון מייצר סרטונים בכלי AI גנרטיביים (Lab Flow, Gemini/Veo) שבהם דמות שלו מדברת, אבל הקול מלאכותי.
המטרה: להקליט את הקול פעם אחת, ואז בכל סרטון להחליף את הקול המלאכותי בקול האמיתי של רון, עם תנועת שפתיים שמתאימה לקול החדש.

## עיקרון מנחה: זיהוי (לא רק איכות)
המבחן היחיד שקובע: **מי שרואה ושומע את הסרטון מבין בבירור שזה רון**. הפנים בסרטון ממילא של רון (ה-lip-sync לא מחליף אותן) → הזיהוי הוויזואלי מובטח. כל ההחלטות בקול מכוונות לזיהוי מקסימלי:
- **Professional Voice Clone (PVC)** עדיף על Instant — נאמנות גבוהה משמעותית בעברית.
- **מסלול S2S (מומלץ):** המרת האודיו של הקליפ לקול רון שומרת על התזמון והאינטונציה → גם נשמע יותר כמו רון וגם השפתיים מסונכרנות טוב יותר. `clip.mp4` → חילוץ אודיו → S2S → lip-sync.
- **מסלול TTS (fallback):** כשרון רוצה טקסט שונה מהמקור — הוא מספק טקסט שמוקרא בקולו. שובר תזמון מקורי, לכן משני.

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

2. אם אין - **לזיהוי מקסימלי, המסלול המומלץ הוא Professional Voice Clone (PVC)**:
   - PVC דורש אימות זהות + אימון, שמטופלים בצורה הכי נקייה ב-Web UI של ElevenLabs.
   - הנחה את רון: ב-elevenlabs.io → Voices → Add a new voice → Professional, להעלות ~30 דקות הקלטה נקייה בעברית, לאשר אימות זהות, ולהמתין לאימון.
   - בסיום, רון מעתיק את ה-`voice_id` מה-UI ומגדיר אותו כ-`RON_VOICE_ID`.
   - **fallback מהיר (Instant):** אם רון רוצה לבדוק עכשיו בלי להמתין לאימון, הקלטה של 1-3 דקות נקיות:

```
python.exe run.py clone_voice.py --name "Ron" --files "recording.mp3"
```

   (אפשר אודיו או וידאו - הסקריפט מחלץ אודיו לבד.)

3. **נקודת אישור:** ודא שיש `voice_id` שמור כ-`RON_VOICE_ID`. הקול נשמר בחשבון ElevenLabs - לא צריך לשכפל שוב.

## זרימה לכל קליפ (מסלול מומלץ - S2S)

### 1. אימות הקובץ
ודא שהקליפ קיים. שלוף משך וממדים. **בדוק מול מגבלות Sync.so** (Free tier עד 20 שניות) - אם ארוך מדי, התרע.

### 2. חילוץ האודיו המקורי

```
python.exe run.py extract_audio.py "clip.mp4" --output clip.original.wav --json
```

### 3. המרת האודיו לקול של רון (S2S - שומר תזמון ואינטונציה)

```
python.exe run.py convert_voice.py --mode s2s --voice-id <id> --audio clip.original.wav --output voice_out.mp3 --json
```

**מסלול TTS (fallback)** - רק כשרון רוצה טקסט שונה מהמקור. המלץ שאורך הטקסט יתאים בקירוב למשך הקליפ (אחרת האודיו ארוך/קצר מדי, ראה `--sync-mode` ב-`api_notes.md`):

```
python.exe run.py convert_voice.py --voice-id <id> --text "<הטקסט>" --output voice_out.mp3 --json
```

### 4. שלב אישור 1 (חובה - לא לדלג)
תן לרון לשמוע את `voice_out.mp3` **לפני** ה-lip-sync (שלב יקר). השאלה הראשונה היא **"האם זה נשמע בבירור כמוך?"** - לא רק איכות כללית. אם לא מזוהה כרון או שיש ארטיפקטים - שקול PVC (אם עוד לא), תקן וחזור על שלב 3. אל תמשיך ל-lip-sync בלי אישור מפורש.

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

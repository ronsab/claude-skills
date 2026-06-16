# הערות API, מגבלות וסיכונים -- voice-clone-dub

## ElevenLabs

- SDK: `from elevenlabs.client import ElevenLabs` ; `client = ElevenLabs(api_key=...)`.
- שכפול (IVC): `client.voices.ivc.create(name=, files=[...])` (גרסאות חדשות) או `client.clone(...)` (ישנות). `clone_voice.py` מנסה את שניהם.
- TTS: `client.text_to_speech.convert(voice_id=, text=, model_id="eleven_multilingual_v2", output_format="mp3_44100_128")` → iterator של bytes.
- S2S: `client.speech_to_speech.convert(voice_id=, audio=<file>, model_id="eleven_multilingual_sts_v2", ...)`.
- מפתח: `ELEVENLABS_API_KEY`. השג ב-elevenlabs.io/app/settings/api-keys.

## Sync.so

- יצירה: `POST https://api.sync.so/v2/generate`, header `x-api-key`.
- body: `{"model": "...", "input": [{"type":"video","url":...},{"type":"audio","url":...}], "options": {"sync_mode": "..."}}`.
- מודלים: `lipsync-2`, `lipsync-2-pro`, `sync-3`, `lipsync-1.9.0-beta`. אמת מול התיעוד -- השמות והתמחור משתנים תכופות.
- polling: `GET /v2/generate/{id}` עד `status == COMPLETED`, אז `outputUrl`.
- **קלט כ-URL או data URL בלבד.** `lipsync.py` מקודד קבצים מקומיים כ-data URL (base64) -- מתאים לקבצים קטנים. לקבצים גדולים: העלה לאחסון ציבורי (Google Drive עם שיתוף ציבורי / S3 / Vercel) והעבר `--video-url`/`--audio-url`. כדאי לאמת את מגבלת גודל ה-data URL מול Sync.so.
- מפתח: `SYNC_SO_API_KEY`. השג ב-app.sync.so → API keys.

## הפרש אורך אודיו↔וידאו (חשוב במסלול TTS)

ה-TTS כמעט תמיד באורך שונה מהקליפ. `--sync-mode` קובע את הטיפול:
- `loop` -- חוזר על הווידאו אם האודיו ארוך יותר.
- `silence` -- מוסיף שקט/מקפיא.
- `cut_off` -- חותך לפי הקצר מביניהם.
- `remap`/`bounce` -- מיפוי/הלוך-חזור.
המלצה: שאורך הטקסט יתאים בקירוב למשך הקליפ. אם פער גדול -- לקצר טקסט או לבחור קליפ ארוך יותר.

## סיכונים ואי-ודאויות

1. **איכות S2S/TTS בעברית** -- נתמך רשמית אך פחות נבדק מאנגלית; ייתכנו ארטיפקטים בהגייה. בדוק קליפ קצר אחד לפני פרויקט מלא. PVC משפר משמעותית.
2. **שינויים ב-Sync.so** -- שמות מודלים ותמחור משתנים. `--model` הוא פרמטר; אמת מול הדוקס.
3. **מגבלות אורך** -- Free tier עד 20 שניות. עבד קליפים קצרים בנפרד.
4. **דמות ריאליסטית** -- Sync.so טוב על פנים חזיתיות; זוויות קיצוניות/תאורה חריגה/פנים חלקיות בפריים פוגעות בדיוק → אימות ויזואלי חובה.
5. **עלות מצטברת** -- lip-sync יקר. אישור עם הצגת עלות לפני כל הרצה.
6. **פרטיות** -- הקבצים עוברים ל-ElevenLabs ו-Sync.so. רון צריך להיות מודע.

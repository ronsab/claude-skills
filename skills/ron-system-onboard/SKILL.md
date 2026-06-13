---
name: ron-system-onboard
description: >
  הקמת RON Assistant ללקוח חדש — מתאים קונפיגורציה (נישות, ערים, צבעי מותג, ICP)
  לפרופיל ספציפי של הלקוח. השתמש בסקיל זה כשרון אומר "התחל ללקוח חדש", "צריך
  להקים מערכת ל-X", "תכין onboarding ל-Y", או חתם עם לקוח וצריך להתחיל את ההתקנה.
  הסקיל מחזיר checklist מסודר + קבצי קונפיגורציה מותאמים + הוראות פריסה.
---

# RON Assistant — Onboarding ללקוח חדש

## מטרת הסקיל
לקבל מרון פרופיל לקוח חדש שחתם, ולהחזיר חבילה שלמה להקמת המערכת ללקוח תוך 4-6 שעות.

## שלב 1: קליטת פרטי הלקוח

שאל את רון את 8 השאלות:

1. **שם החברה + שם איש קשר**
2. **תחום עסקי / נישה ראשית** (לקבוע ICP)
3. **קהל יעד** — B2C? B2B? מי הלקוחות שהם רוצים?
4. **אזורי פעילות** — אילו 5-22 ערים רלוונטיות?
5. **נישות מטרה** — אילו 3-10 נישות מהרשימה רלוונטיות עבורם? (לסרוק לפיהן)
6. **צבעי מותג + לוגו** — האם מספקים? איזה צבעים?
7. **חשבונות נדרשים** — Google account (לסיטס/ג'ימייל), Telegram bot token, Apify, Anthropic
8. **תאריך התחלת השירות** — מתי המערכת חייבת להיות חיה?

## שלב 2: הקמת התשתיות (סדר חובה)

```
[שלב 2.1] Google Workspace
- צור spreadsheet חדש בשם "leads_master" בחשבון הלקוח
- שתף עם service account email
- שמור Sheet ID

[שלב 2.2] Telegram Bot
- צור bot חדש דרך BotFather
- קבל TOKEN
- שמור Bot username

[שלב 2.3] חשבונות API
- Apify: צור חשבון, קבל API token, `5 USD` קרדיט חינם
- Anthropic: API key (`10 USD` קרדיט התחלתי מספיק)
- Firecrawl: free tier (`0 USD`)
- Gmail OAuth: צור token (gmail.readonly + gmail.send) דרך regen_gmail_token.py.
  חובה לפרסם את האפליקציה ל-Production (Google Cloud -> OAuth consent screen ->
  Audience -> Publish app). במצב Testing ה-refresh token פג כל 7 ימים.

[שלב 2.4] Railway
- צור project חדש
- חבר ל-GitHub repo (fork של ron-assistant)
- שמור webhook URL

[שלב 2.5] משתני סביבה ב-Railway
- TELEGRAM_BOT_TOKEN
- ALLOWED_CHAT_ID (chat ID של הלקוח)
- ANTHROPIC_API_KEY
- APIFY_TOKEN
- GOOGLE_SHEETS_SA_B64
- RON_LEADS_SHEET_ID
- WEBHOOK_URL
- FIRECRAWL_API_KEY
- GMAIL_TOKEN_B64 (אם רוצה שליחת מייל)
```

## שלב 3: התאמת קונפיגורציה

עדכן בקוד של הלקוח (`commands/scan_config.py`):

```python
# התאם לפי הלקוח
PILOT_CITIES = [רק הערים הרלוונטיות ללקוח]
CITIES = [רשימת הערים המלאה]

# נישות לפי תחום הלקוח (לדוגמה — לקוח שמוכר מערכת SaaS לקוסמטיקאיות:)
NICHES_P1 = ["קוסמטיקאיות", "טכנאיות ציפורניים", "מאפרות לאירועים"]
NICHES_P2 = ...
```

ועדכן `commands/brand.py`:

```python
COLORS = {
    "gold": "XXXXXX",  # צבע ראשי של הלקוח
    "secondary": "XXXXXX",
    ...
}
STUDIO_NAME = "שם החברה של הלקוח"
TAGLINE = "התיוג שלהם"
```

## שלב 4: בדיקות הקמה

```
✅ /help — הבוט מגיב?
✅ /scan [עיר] [נישה] — סריקה רצה?
✅ /funnel — מציג נתונים?
✅ /sent 5 — סטטוס מתעדכן ב-Sheet?
✅ Excel מגיע לטלגרם?
✅ מייל מגיע ל-Gmail של הלקוח?
✅ Daily scheduled scan רץ בשעה הנכונה?
```

## שלב 5: הדרכה ללקוח (60 דקות)

תסריט:
1. **10 דק'** — סיור בטלגרם: כל הפקודות
2. **15 דק'** — סיור ב-Google Sheets: לשוניות, סטטוסים, dropdowns
3. **15 דק'** — הדגמת סריקה חיה + פתיחת DM
4. **10 דק'** — הסבר על Excel + מייל יומיים
5. **10 דק'** — Q&A + תרגול

## פלט שלך לרון

החזר חבילה מאורגנת:

1. **Onboarding Checklist** — Markdown עם כל השלבים (לסמן בעת ביצוע)
2. **קובץ `scan_config.py` מותאם** — מוכן להעתקה
3. **קובץ `brand.py` מותאם** — מוכן להעתקה
4. **רשימת משתני סביבה** — כל ה-keys שצריך + הסבר איפה להשיג כל אחד
5. **תסריט הדרכה 60 דק'** — מובנה, עם זמנים
6. **רשימת checkpoints** לבדיקה בכל שלב
7. **הערות לקוח-ספציפיות** — מה ייחודי בלקוח הזה שכדאי לזכור (לדוגמה: "הלקוח רגיש לפרטיות, וודא שמשתנה ALLOWED_CHAT_ID מוגדר נכון")

## כללים חשובים

- **לעולם לא** להעתיק credentials של רון ללקוח חדש — יוצרים חדשים לכל לקוח
- **לוודא** שה-RON_LEADS_SHEET_ID של הלקוח שונה משל רון
- **לבדוק** שאין שיתוף בטעות של נתונים בין לקוחות
- **לתעד** כל לקוח בקובץ נפרד: שם, תאריך עליה, מודולים שקנה, מחיר חודשי
- **Gmail OAuth חייב Production, לא Testing.** אפליקציית OAuth במצב Testing מנפיקה
  refresh token שפג כל 7 ימים, והמייל נשבר בלי התראה ברורה. בכל הקמת לקוח: אחרי
  יצירת ה-token, פרסם מיד את האפליקציה ל-Production. זה ההבדל בין תיקון פעם אחת
  לתיקון כל שבוע.

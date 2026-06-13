---
name: nekudat-hashmal
description: Use when working on the נקודת חשמל / Shlomo Shushan electric contractor system at C:\Users\USER\Documents\nekudat-hashmal. Covers stage 2 (projects), stage 3 (partial bills), design changes, maintenance, deploy, and any modification to the existing PWA. TRIGGER on mentions of "נקודת חשמל", "שלמה שושן", "BUILD_SPEC.md", "kabblan חשמל", paths under Documents/nekudat-hashmal/, or stage 2/3 work.
---

# נקודת חשמל — Project Skill

## What this project is
PWA אופליין שיוצרת הצעות מחיר ו(בעתיד) חשבונות חלקיים עבור **שלמה שושן**, קבלן חשמל בן 67. הקלינט עובד מול חברת חשמל גדולה ומגיש עבודות **למפקח לפי סעיפים** מתוך כתב כמויות.

**מקור האמת המוחלט:** `C:\Users\USER\Documents\nekudat-hashmal\BUILD_SPEC.md`. כל החלטה סותרת ב-skill הזה נדחית מול ה-BUILD_SPEC.

## Project location
```
C:\Users\USER\Documents\nekudat-hashmal\
```

## Project status (snapshot)
- **שלב 1**: ✅ הושלם. PWA פונקציונלית, 77 סעיפי מחירון אמיתיים, ייצוא PDF דו-מצבי (פשוט/מובנה).
- **שלב 1.5**: ✅ הושלם. שדרוג עיצוב לתעשייתי פרמיום (navy + זהב + Frank Ruhl Libre).
- **שלב 2**: ⏳ פרויקטים. ראה `STAGE_2_SPEC.md`.
- **שלב 3**: ⏳ חשבונות חלקיים. ראה `STAGE_3_SPEC.md`.

## Stack (קצר)
- Vanilla JS + Vite + vite-plugin-pwa
- localStorage לנתונים מובנים, IndexedDB ל-PDF blobs
- html2canvas + jsPDF
- Heebo + Frank Ruhl Libre, מקומיים, אופליין

## Files in this skill
| קובץ | מתי לקרוא |
|---|---|
| `ARCHITECTURE.md` | בכל משימה: מבנה תיקיות, entities, data flow |
| `DESIGN_TOKENS.md` | שינוי עיצובי, צבעים, טיפוגרפיה |
| `CRITICAL_RULES.md` | **חובה לקרוא לפני כל שינוי**: 5 חוקים בל יעברו |
| `ADD_VIEW.md` | הוספת מסך חדש |
| `ADD_ENTITY.md` | הוספת ישות חדשה ל-store |
| `PDF_TEMPLATES.md` | שינוי תבנית PDF |
| `STAGE_2_SPEC.md` | תכנון/ביצוע שלב 2 (פרויקטים) |
| `STAGE_3_SPEC.md` | תכנון/ביצוע שלב 3 (חשבונות חלקיים) |

## Quick start (לסשן חדש)
1. קרא את `CRITICAL_RULES.md` (חובה).
2. קרא את `ARCHITECTURE.md` (5 דקות, מספיק לרוב המשימות).
3. רק אם המשימה היא שלב 2/3, קרא את ה-spec המתאים.

## Quick start (להפעלת השרת)
```bash
cd /c/Users/USER/Documents/nekudat-hashmal
npm run preview    # http://127.0.0.1:4173
# או
npm run dev        # http://localhost:5173 עם hot-reload
```

## Anti-patterns (אל תעשה)
- ❌ אל תוסיף React/Vue/Tailwind. הסטאק הוא Vanilla מכוון.
- ❌ אל תשתמש ב-CDN בזמן ריצה (חוק PWA אופליין).
- ❌ אל תוסיף Backend (חוק "מקומי-first").
- ❌ אל תכנה את הקובץ הפלט "חשבונית" (איסור מ-BUILD_SPEC §3).
- ❌ אל תקרא מחירים מהמחירון בזמן רינדור הצעה קיימת (חוק הקפאת מחירים).
- ❌ אל תשתמש ב-emoji בממשק. רק Lucide SVG דרך `src/components/icons.js`.

## כלי בדיקה
- Playwright MCP לבדיקת UI ויזואלית.
- בדיקה ב-DevTools: Application → Service Workers + Cache Storage.
- כשבודקים שינויים: לפעמים צריך לנקות את ה-SW ו-IndexedDB (יש דוגמת קוד ב-ARCHITECTURE.md).

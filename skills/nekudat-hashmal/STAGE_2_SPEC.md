# שלב 2 — פרויקטים

## Context
שלב 1 פתר את המקרה "הצעה בודדת". שלב 2 פותר את המקרה "לקוח שמזמין סדרת עבודות, יש מספר הצעות, ויש מצב לאורך זמן".

מקור: BUILD_SPEC §6 ("שלב 2 — פרויקטים").

## Scope

### Must-have
1. **פרויקט** כמיכל: שדות לקוח (שם, טלפון, כתובת, איש קשר), שם הפרויקט, סטטוס, תאריך יצירה.
2. **קישור הצעות לפרויקט**: כל הצעה מקבלת `projectId` אופציונלי. הצעה ללא פרויקט = "הצעה חופשית" (התנהגות שלב 1).
3. **סטטוסי פרויקט** (state machine): `טיוטה → הצעה נשלחה → ממתין לאישור → אושר → בביצוע → הושלם` + `בוטל`, `ארכיון`.
4. **Dashboard (מסך ראשי)**: רואים מה פתוח, תקוע על אישור, בביצוע. ספירות + רשימות קצרות.
5. **יומן פרויקט** (`log: LogEntry[]`): כל שינוי סטטוס + הערה ידנית = entry עם תאריך.
6. **ייצוא פרויקט כחבילה אחת** (JSON): להעברה בין מכשירים + גיבוי.
7. **ארכוב פרויקט** שהושלם (להוציא מ-dashboard בלי למחוק).

### Out of scope (לשלב 3)
- חשבונות חלקיים.
- צירוף קבצים.
- שיתוף סטטוס עם הלקוח.

## Data model

### `Project` חדש
```ts
{
  id: 'proj_xxx',
  name: 'שיפוץ חשמל לבית פרידמן',       // הצגה ב-UI
  client: { name, phone, address, contact },
  status: 'draft' | 'sent' | 'pending_approval' | 'approved' | 'in_progress' | 'done' | 'cancelled' | 'archived',
  createdAt: ISO,
  updatedAt: ISO,
  quoteIds: string[],                     // references to Quote[]
  log: LogEntry[],
  // ⏳ שלב 3: bills, files
}
```

### `LogEntry`
```ts
{
  at: ISO,
  type: 'status_change' | 'note' | 'quote_added' | 'quote_removed',
  text: string,                           // אנושי, לתצוגה
  from?: string,                          // לסטטוס: מהסטטוס הקודם
  to?: string,                            // לסטטוס: לסטטוס החדש
}
```

### `Quote` (מורחב)
```ts
{
  ...,                                    // קיים
  projectId: string | null,               // ← חדש
}
```

## UI changes

### מסך ראשי - tile חדש או החלפה
**אפשרות 1** (מומלצת): להחליף את ה-tile "ההצעות שלי" ב-"פרויקטים", ולשמור את "ההצעות שלי" כסביב משני.

**אפשרות 2**: 4 tiles במקום 3 (מסך מסך הופך 2x2 ב-mobile).

החלטה: **אפשרות 1**. הצעות = subset של פרויקט.

### מסך פרויקטים `#/projects`
- כותרת + כפתור "פרויקט חדש"
- Filter: לפי סטטוס (טאבים).
- Table: שם הפרויקט, לקוח, סטטוס (badge), # הצעות, סכום מצטבר, תאריך עדכון.

### מסך פרטי פרויקט `#/projects/:id`
- Header: שם הפרויקט + לקוח (קטן) + status (badge ניתן לשינוי).
- Tabs (או sections):
  - **הצעות מקושרות**: רשימה + "+ הצעה חדשה לפרויקט"
  - **יומן**: timeline של LogEntries
  - **פעולות**: ארכוב, ייצוא JSON, שינוי סטטוס (עם הוספת note)

### מסך הצעה (קיים) - תוספת
שדה "פרויקט" ב-quoteBuilder (dropdown, אופציונלי). בחירה מקשרת את ההצעה לפרויקט וגורמת ל-`LogEntry: quote_added`.

## Data flow

### יצירת פרויקט + הצעה ראשונה
1. `#/projects/new` → מסך יצירת פרויקט (שם + לקוח).
2. שמירה → `createProject({ name, client })`.
3. Redirect ל-`#/projects/:id`.
4. בלחיצה "הצעה חדשה לפרויקט": navigate ל-`#/quotes/new?project=:id`.
5. ב-`quoteBuilder.js`: read query param, `createQuote({ projectId })`.
6. עם השמירה הראשונה: `addLogEntry(project, 'quote_added')` + `project.quoteIds.push(quote.id)`.

### שינוי סטטוס
ב-`projectDetail.js`: dropdown של סטטוסים. בחירה → prompt לתיבת note → `updateProjectStatus(project, newStatus, note)` → מוסיף LogEntry.

## Migration לקיים
- כל הצעה קיימת תקבל `projectId: null` אוטומטית (סעיף "Quote (מורחב)").
- אחרי שיב 2 נטען, המסך הראשי משתנה. הצעות חופשיות נשארות זמינות דרך "ההצעות שלי" (משני).

## State machine (סטטוסים)
```
draft → sent → pending_approval → approved → in_progress → done
                                     ↓                         ↓
                                  cancelled                 archived
```
- מ-`draft`: רק `sent` או `cancelled`.
- מ-`sent`: `pending_approval`, `cancelled`.
- מ-`pending_approval`: `approved`, `cancelled`.
- מ-`approved`: `in_progress`, `cancelled`.
- מ-`in_progress`: `done`, `cancelled`.
- מ-`done`: `archived`.
- `cancelled`: ניתן לבטל את הביטול ולחזור ל-`draft`.

ב-UI: הצג רק את הסטטוסים הלגיטימיים הבאים (הסתר את האחרים).

## Files (להוספה / שינוי)

| קובץ | פעולה |
|---|---|
| `src/store/db.js` | schema bump 1→2 + migration |
| `src/store/projects.js` | חדש - CRUD פרויקטים |
| `src/store/quotes.js` | הוספת `projectId` |
| `src/views/projectList.js` | חדש |
| `src/views/projectDetail.js` | חדש |
| `src/views/projectForm.js` | חדש |
| `src/views/home.js` | החלפת tile + הצגת dashboard counts |
| `src/views/quoteBuilder.js` | dropdown פרויקט + query param |
| `src/router.js` | 3-4 routes חדשים |

## הערכת זמן ביצוע
- store/projects + schema migration: 1-2 שעות
- 3 views חדשים: 4-6 שעות
- Dashboard counts ב-home: 1 שעה
- אינטגרציה עם quoteBuilder: 1 שעה
- בדיקות ידניות + Playwright: 1-2 שעות
**סה"כ**: 8-12 שעות עבודה ממוקדת.

## פתוח לאימות עם שלמה (לפני שלב 2)
- האם רוצה מספור פרויקטים נפרד מהצעות? (BUILD_SPEC §9 פתוח). הצעה: כן, פורמט `P-2026-001`.
- האם רוצה שצריך לחבר הצעה לפרויקט, או שיכול להישאר "חופשי"? הצעה: אופציונלי.
- האם הסטטוסים שלמעלה מתאימים לתהליך העבודה שלו?

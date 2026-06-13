# הוספת ישות חדשה ל-store — נקודת חשמל

## תרחיש לדוגמה (שלב 2)
"הוסף ישות `Project` (פרויקט) שיכולה להכיל מספר הצעות מחיר."

## שלב 1: עדכון schema ב-`store/db.js`
ב-`empty()`, הוסף שדה:

```js
const empty = () => ({
  schema: 2,                     // bump from 1 to 2
  priceLists: [],
  quotes: [],
  projects: [],                  // ← חדש
  counters: {},
  business: null,
});
```

הוסף migration ב-`load()`:
```js
if (data.schema === 1) {
  data.projects = data.projects || [];
  data.schema = 2;
}
```

## שלב 2: יצירת module חדש: `src/store/projects.js`

המבנה האחיד:
- ייבוא: `load`, `save` מ-`./db.js`; `uid` מ-`../components/ui.js`
- export functions: `listProjects()`, `getProject(id)`, `createProject(input)`, `updateProject(id, patch)`, `deleteProject(id)`
- כל פונקציה עובדת על `load()` ואז `save()`
- ייצוא יישות:
  ```ts
  Project = {
    id: 'proj_xxx',
    name: 'שיפוץ בית פרידמן',
    client: { name, phone, address, contact },
    status: 'draft' | 'sent' | 'pending' | 'approved' | 'in_progress' | 'done' | 'cancelled' | 'archived',
    createdAt: ISO,
    quoteIds: string[],            // references to Quote[]
    files: FileRef[],               // (שלב 3)
    log: LogEntry[],                // יומן פעילות
  }
  ```

## שלב 3: עדכון `store/quotes.js` (קישור)
הוסף שדה `projectId` ל-`Quote`:
```js
{
  ...
  projectId: 'proj_xxx' | null,   // אופציונלי, ניתן לקשר הצעות לפרויקטים
}
```

ב-`createQuote(input)`, הוסף:
```js
projectId: input.projectId || null,
```

ב-`deleteQuote(id)`, הוסף ל-`projects[].quoteIds` cleanup (אם הקישור קיים).

## שלב 4: views חדשים (ראה `ADD_VIEW.md`)
- `src/views/projectList.js` - רשימת פרויקטים
- `src/views/projectDetail.js` - פרטי פרויקט + הצעות מקושרות + יומן
- `src/views/projectForm.js` - יצירה / עריכה

## שלב 5: routes חדשים ב-`router.js`
```js
{ match: /^\/projects$/, view: renderProjectList, crumbs: ... },
{ match: /^\/projects\/new$/, view: renderProjectForm, crumbs: ... },
{ match: /^\/projects\/([^/]+)$/, view: renderProjectDetail, crumbs: ... },
{ match: /^\/projects\/([^/]+)\/edit$/, view: renderProjectForm, crumbs: ... },
```

## שלב 6: tile חדש ב-`home.js`
הוסף תיבה ב-tile-grid (מבנה זהה ל-3 הקיימות).

## כללי עיצוב הישות
1. **ID prefix** מנהג: `proj_`, `q_`, `pl_`, `pdf_`. שלוש אותיות + `_`.
2. **createdAt** תמיד ISO 8601 (`new Date().toISOString()`).
3. **status enum** תמיד נשמר כ-string (קל לקריאה). הסטטוסים מ-BUILD_SPEC §4.
4. **שדות שיכולים להיות null** מוגדרים מפורשות (לא undefined).
5. **schema migration** הוא חוק - לא לעבור גרסת schema בלי migration שעובד גם על אחסון ריק וגם על מלא.

## דברים שלא לעשות
- ❌ **אסור** ליצור module store בלי helpers `list/get/create/update/delete`. עקביות לפני המצאה.
- ❌ **אסור** לשנות `Quote.lines[].unitPrice` כשמקושר ל-project (חוק הקפאת מחירים).
- ❌ **אסור** להחזיר reference ישיר ל-data של load() ולתת ל-caller לערוך אותו. תמיד החזר עותק או השתמש בפונקציית update.

## בדיקה
- צור פרויקט חדש.
- צור הצעה והקשר אותה לפרויקט.
- וודא שה-quote נכנסת ל-`project.quoteIds`.
- מחק את ההצעה → וודא שה-id מתעלם מ-`project.quoteIds`.
- Reload → הכל נשמר.

## שלב 2 ספציפי
ראה `STAGE_2_SPEC.md` למפרט מלא של פרויקטים.

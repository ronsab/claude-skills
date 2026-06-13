# שלב 3 — חיוב חלקי + צירוף קבצים

## Context
שלמה מבצע עבודה מסביב לחודש, ומגיש למפקח **חשבון לפי כמות שבוצעה בכל סעיף**. למשל: סעיף 01.01.002 הוצע 20 יח', בחודש שעבר בוצעו 12 יח' = חיוב על 12. בחודש הזה בוצעו עוד 5 = חיוב על 5, מצטבר 17, יתרה 3.

מקור: BUILD_SPEC §6 ("שלב 3 — חיוב וקבצים").

## Scope

### Must-have
1. **חשבון חלקי** (`PartialBill`) שמקושר להצעה ספציפית.
2. **לכל שורה בחשבון**: כמות שבוצעה בחודש זה, סך מצטבר עד כה, יתרה.
3. **שימוש במחירי ההצעה המקורית** (הקפאת מחירים - חוק 1).
4. **חיוב מצטבר** רב-חודשי: PartialBill חדש קורא לחישוב "previouslyBilled" מסך כל ה-PartialBills הקיימים על אותה הצעה.
5. **PDF חשבון חלקי**: תבנית חדשה דומה לפדי הצעה, אבל עם כותרת "**דרישת תשלום**" (לא "חשבונית מס"!).
6. **צירוף קבצים לפרויקט**: PDF הצעה חתומה, צילומי שטח, בקשות שינוי. נשמרים ב-IndexedDB.

### Out of scope
- חשבונית מס (איסור חוקי, ראה CRITICAL_RULES §3).
- שליחת ה-PDF אוטומטית ללקוח.

## Data model

### `PartialBill` חדש
```ts
{
  id: 'bill_xxx',
  projectId: string,                      // נדרש (מ-שלב 2)
  quoteId: string,                        // ההצעה שעליה החשבון
  number: string,                         // 'B-2026-001'
  date: 'YYYY-MM-DD',
  createdAt: ISO,
  lines: PartialBillLine[],
  notes: string,                          // הערות חופשיות (לדוגמה: "עבודות חודש פברואר")
  pdfBlobKey: string | null,
}
```

### `PartialBillLine`
```ts
{
  quoteLineNumber: string,                // 'מספר הסעיף', זהה ל-Quote.lines[].number
  description: string,                    // ב-cache לתצוגה (ייתכן ישתנה ב-Quote line)
  unit: string,
  unitPrice: number,                      // מ-QuoteLine, מוקפא!
  originalQty: number,                    // כמות שהוצעה במקור
  executedThisBill: number,               // כמות שבוצעה רק בחשבון הזה
  // נחושב בזמן הצגה:
  // - previouslyBilled = sum of executedThisBill across earlier bills for same (quote, line)
  // - cumulative = previouslyBilled + executedThisBill
  // - remaining = originalQty - cumulative
  // - lineTotal = executedThisBill * unitPrice
}
```

### `FileRef` (צירוף קבצים)
```ts
{
  id: 'file_xxx',
  projectId: string,
  name: 'הצעה_חתומה_2026-001.pdf',
  type: string,                           // MIME type
  size: number,                           // bytes
  uploadedAt: ISO,
  storage: 'idb',                         // ⚠️ כרגע רק IndexedDB
  blobKey: 'file_xxx',                    // key ב-IndexedDB
  // עתידי:
  // storage: 'drive', driveUrl?: string  // לקבצים כבדים
}
```

### `Project` (מורחב משלב 2)
```ts
{
  ...,                                    // קיים
  billIds: string[],                      // ← חדש
  fileIds: string[],                      // ← חדש
}
```

## UI

### מסך פרטי פרויקט - tabs נוספים
- **חשבונות חלקיים**: רשימה + "+ חשבון חלקי חדש"
- **קבצים**: רשימה + upload

### מסך "חשבון חלקי חדש" `#/projects/:pid/bills/new?quote=:qid`
- בחירת ההצעה שעליה החשבון (אם לפרויקט יש >1 הצעה).
- כל שורה מההצעה מוצגת:
  - מספר סעיף, תיאור, יחידה, **מחיר מוקפא**.
  - **כמות שהוצעה במקור** (קריאה בלבד).
  - **חויבה כבר** (קריאה בלבד, חישוב).
  - **כמות לחיוב בחודש זה** (input).
  - **סה"כ לשורה** (חישוב).
  - **יתרה** (חישוב).
- חישוב טוטל: סכום כל ה-`executedThisBill * unitPrice` → מע"מ → סך לתשלום.
- שמירה → ייצור PDF "דרישת תשלום" → שמירה ב-IDB.

### מסך פרטי חשבון `#/bills/:id`
- תצוגה מקדימה + הורדה + שיתוף (זהה ל-quotePreview).

## PDF: "דרישת תשלום" (תבנית חדשה!)

`src/pdf/templatePartialBill.js`:
- ראש זהה ל-pdf הצעה (navy + לוגו + פס זהב).
- כותרת: **"דרישת תשלום"** ב-serif (לא "חשבון" ולא "חשבונית"!).
- מספר: `B-2026-001`.
- הפניה: "בהמשך להצעת מחיר מס' 2026-005 מתאריך 2026-02-10."
- טבלה עם עמודות:
  - מס' סעיף | תיאור | יחידה | מחיר יח' | כמות חויבה | סה"כ
- שתי שורות סיכום מתחת לטבלה:
  - **חויב עד כה (כולל החשבון הזה)**: ₪ X
  - **יתרה לחיוב** (אם חיובית): ₪ Y
- מע"מ + סך לתשלום.
- חתימות.

## Data flow: יצירת חשבון חלקי

1. `#/projects/:pid` → tab "חשבונות חלקיים" → "+ חשבון חדש".
2. אם לפרויקט >1 הצעה: בורר הצעה.
3. ב-`createPartialBill(quote, project)`:
   - שולף `quote.lines` עם `unitPrice` (מוקפא!).
   - לכל שורה, מחשב `previouslyBilled` ע"י סכימת `executedThisBill` של כל ה-PartialBills הקיימים לאותה הצעה ולאותו `quoteLineNumber`.
   - יוצר `PartialBillLine[]` ריקים (`executedThisBill: 0`).
4. ה-view מציג את הטבלה. משתמש ממלא `executedThisBill` לכל שורה.
5. שמירה → חישוב totals → `createPartialBill({ ... })` → `addLogEntry(project, 'bill_created')`.
6. ייצוא PDF → IDB.

## חישוב "previouslyBilled" (פונקציה חשובה)
```ts
function previouslyBilled(quoteId, lineNumber, excludeBillId = null) {
  return listBills()
    .filter(b => b.quoteId === quoteId && b.id !== excludeBillId)
    .flatMap(b => b.lines)
    .filter(l => l.quoteLineNumber === lineNumber)
    .reduce((sum, l) => sum + Number(l.executedThisBill || 0), 0);
}
```

`excludeBillId` שימושי בעת **עריכת** חשבון קיים (לא לכלול את עצמו בחישוב).

## אזהרות

### למשתמש (ב-UI)
- אם `executedThisBill + previouslyBilled > originalQty`: הצג אזהרה צהובה ("חיוב מעל הכמות שבוצעה"). לא חוסם, אבל מבקש confirm.
- אם מנסים למחוק חשבון שאחריו יש חשבונות נוספים על אותה הצעה: אסור (יכול לגרום ל-cumulative שגוי). חייב למחוק את החשבונות החדשים יותר קודם.

### למפתח
- ❌ **אסור** לאפשר לערוך `unitPrice` ב-PartialBillLine. רק `executedThisBill`. אחרת המחיר המוקפא משתבש.
- ❌ **אסור** ליצור PartialBill בלי `quoteId` תקין. ה-בלי הצעה אין מחירים מוקפאים.

## Files

### IndexedDB strategy (קבצים)
ה-Quota של IndexedDB גדול אבל לא אינסופי (~50% משטח דיסק פנוי). אם שלמה יצרף תמונות JPEG כבדות, ימלא את ה-IDB.

**MVP**: רק קבצים עד 5MB. הצג אזהרה ל-15MB+.
**עתידי**: אופציה "קישור ל-Drive" - השדה `FileRef.storage = 'drive'`, ה-URL ייפתח בדפדפן. אסור להוריד את הקובץ ל-IDB.

## הערכת זמן ביצוע
- store/bills + store/files: 2-3 שעות
- 2 views חדשים (bill form, bill detail): 4-5 שעות
- templatePartialBill.js + pdf.css updates: 2-3 שעות
- אינטגרציה ב-project detail: 1-2 שעות
- file upload + IDB: 2-3 שעות
- בדיקות: 2 שעות
**סה"כ**: 13-18 שעות עבודה ממוקדת.

## פתוח לאימות עם שלמה (לפני שלב 3)
- האם המבנה של דרישת התשלום מתאים למה שהמפקח של חברת חשמל מצפה לראות? (יש פורמט סטנדרטי בענף).
- האם רוצה לראות את "יתרה לחיוב" כשורה נפרדת בסך הכל בסוף, או רק ב-table inline?
- מע"מ על דרישות תשלום: 18% או 0% (אם חברת חשמל "פטורה")? לאמת!

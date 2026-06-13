# שינוי תבניות PDF — נקודת חשמל

## מבנה הקבצים
```
src/pdf/
├── render.js              # מנוע - html2canvas + jsPDF
├── templateCommon.js      # בלוקים משותפים (head, title bar, client, totals, terms, signatures, footer)
├── templateSimple.js      # מצב "פשוט" - טבלה אחת
└── templateStructured.js  # מצב "מובנה" - פרקים + ריכוז
```

`src/styles/pdf.css` מכיל את כל ה-CSS. נטען רק כשמרנדרים PDF (import ב-`quotePreview.js`).

## מתי כל תבנית פעילה
ב-`quotePreview.js`:
```js
const docHtml = quote.mode === 'simple'
  ? renderSimple(quote, totals, business)
  : renderStructured(quote, totals, business);
```

המשתמש בוחר את ה-mode ב-`quoteBuilder.js` בשדה `q-mode`. ברירת מחדל: `structured`.

## עקרונות עיצוב ה-PDF

### Brand
- **ראש**: navy gradient (`linear-gradient(135deg, #0A1929 → #142A42)`), פס זהב 3px בתחתית, לוגו עם מסגרת זהב על רקע שחור.
- **שם המסמך**: Frank Ruhl Libre, 28px (זה החתימה הוויזואלית, ראה `.impeccable.md`).
- **שאר הטקסט**: Heebo (sans).

### Color usage in PDF
| מקום | צבע |
|---|---|
| ראש | navy gradient |
| לוגו border | זהב #C79A3F |
| title bar | רקע #FAFAF7, h1 navy |
| thead | רקע navy, טקסט #F5F4EF, border-bottom זהב 1px |
| סיכום פרק | רקע #F4ECD8 (זהב soft), טקסט navy |
| totals.grand | navy gradient, טקסט קרים, border-top זהב 2px |
| terms box | רקע #FAFAF7, border-right זהב 3px, ◆ זהב כ-bullet |
| summary table tfoot last row | navy gradient, serif, 18px |
| footer | border-top שורה זהב 80px במרכז |

## הוספת בלוק חדש לכל ה-PDF

### דוגמה: הוספת "ברקוד מספר הצעה" בראש המסמך

ב-`src/pdf/templateCommon.js`:
- הוסף `pdfBarcode(quote)` שמחזיר string HTML עם div שמכיל barcode/QR.
- ב-`templateSimple.js` ו-`templateStructured.js`: קרא ל-`pdfBarcode(quote)` בין `pdfTitleBar` ל-`pdfClientBlock`.

ב-`src/styles/pdf.css`:
- הוסף `.pdf-barcode { padding: 18px 36px; ... }`.

**חוק**: כל בלוק חדש חייב להופיע בשתי התבניות (פשוט + מובנה) כדי לשמור על אחידות.

## הוספת mode שלישי (לדוגמה: "compact")

1. צור `src/pdf/templateCompact.js` עם export `renderCompact(quote, totals, business)`.
2. ב-`quotePreview.js`: הרחב את הבחירה:
   ```js
   const docHtml = quote.mode === 'simple' ? renderSimple(...)
                 : quote.mode === 'compact' ? renderCompact(...)
                 : renderStructured(...);
   ```
3. ב-`quoteBuilder.js`: הוסף option ב-`#q-mode`:
   ```html
   <option value="compact">קומפקטי (חיסכון בדיו)</option>
   ```

## דברים שאסור לשנות
- ❌ **אסור** לעבור מ-html2canvas+jsPDF ל-print API בלי שיקול עמוק. ה-Blob נשמר ב-IndexedDB, print לא נותן Blob.
- ❌ **אסור** להסיר את ה-`pdf-col-num` או לעשות אותו `display: none`. חוק 2 ב-CRITICAL_RULES.md.
- ❌ **אסור** לשנות את הכותרת ל"חשבונית". חוק 3 ב-CRITICAL_RULES.md.

## אופטימיזציה: רינדור מהיר יותר
`render.js` משתמש כרגע ב-`scale: 2` (HQ). זה ~5-6 שניות עבור 30 שורות. אפשרויות:
- `scale: 1.5` → ~3-4 שניות, איכות עדיין מצוינת ל-A4.
- `scale: 1` → ~2 שניות, איכות שטוחה. רק לטסטים.

המספר ה-DPI הסביר ל-print: `scale: 2` = ~144 DPI = print-ready.

## בדיקת PDF
1. `npm run preview` → `#/quotes/:id`.
2. לחץ "הורד PDF".
3. פתח ב-Acrobat Reader. וודא:
   - עברית RTL מלאה (לא reverse).
   - מספרי סעיפים נראים.
   - תווי תווים שלא נשברו (אם הוטמע פונט serif חדש).
   - page breaks לא חותכים באמצע שורה (אם זה קורה, הפחת `scale` או הוסף `page-break-inside: avoid` ב-pdf.css).
4. וודא שה-PDF נשמר ב-IndexedDB (Application → IndexedDB → keyval-store → keys).
5. סגור את הדף, פתח שוב, לחץ "הורד PDF": צריך להיות הורדה מיידית (cached blob).

## שינוי פונטים
אסור CDN. הורדה מקומית ל-`public/fonts/`.

הוספת פונט חדש לתבנית PDF:
1. הורד `.woff2` ל-`public/fonts/`.
2. הגדר `@font-face` ב-`base.css` (קיים שם בלוק לפונטים).
3. ב-`pdf.css`, השתמש בפונט בסלקטור הרלוונטי.
4. בנה מחדש (`npm run build`) - vite-plugin-pwa יוסיף את הקובץ ל-precache.
5. בדיקה אופליין: כיבוי רשת → רענון → ייצא PDF → פונט עדיין מוצג.

## ראה גם
- BUILD_SPEC.md §5 - דרישות הפלט המלאות.
- `.impeccable.md` - design context (Industrial Premium).

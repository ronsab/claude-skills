# הוספת מסך חדש — נקודת חשמל

## תרחיש לדוגמה
"הוסף מסך 'הגדרות' עם פרטי העסק שניתן לערוך."

## שלב 1: יצירת ה-view
קובץ חדש: `src/views/settings.js`

הוא צריך:
- import של `load`, `save` מ-`../store/db.js`
- import של `escapeHtml`, `toast` מ-`../components/ui.js`
- import של `icon` מ-`../components/icons.js`
- export של `renderSettings(root)` שמקבל DOM element ומגדיר את ה-HTML שלו (`root.innerHTML = ...`)

מבנה ה-HTML של ה-view:
```html
<div class="page-head">
  <h1>הגדרות</h1>
  <div class="spacer"></div>
  <button class="btn-gold" id="btn-save">[icon.check + span 'שמור']</button>
</div>

<div class="card">
  <h2>פרטי העסק</h2>
  <div class="form-grid cols-2">
    <div><label>שם מותג</label><input id="b-brand" type="text" value="..." /></div>
    <div><label>שם הקבלן</label><input id="b-contractor" type="text" value="..." /></div>
    <div><label>עוסק מורשה</label><input id="b-vat" type="text" value="..." /></div>
    <div><label>טלפון</label><input id="b-phone" type="tel" value="..." /></div>
    <div><label>כתובת</label><input id="b-address" type="text" value="..." /></div>
    <div><label>אימייל</label><input id="b-email" type="email" value="..." /></div>
  </div>
</div>
```

אחרי הקצאת ה-template, רישום event listener על `#btn-save`:
- קורא את הערכים מה-inputs (`.value.trim()`)
- מעדכן `data.business = { brand, contractor, vat_id, phone, address, email }`
- קורא ל-`save()`
- מציג `toast('פרטי העסק נשמרו', 'success')`

## שלב 2: רישום ה-route
`src/router.js` - הוסף ל-array `routes`:

```js
import { renderSettings } from './views/settings.js';

const routes = [
  // ... existing routes
  {
    match: /^\/settings$/,
    view: renderSettings,
    crumbs: () => [{ label: 'ראשי', href: '#/' }, { label: 'הגדרות' }],
  },
];
```

## שלב 3: לינק מהמסך הראשי
אם זה כלי משני (לא ב-tile-grid), הוסף ל-`src/views/home.js` בתחתית:
```html
<div class="card-row mt-5">
  <div class="spacer"></div>
  <a class="btn btn-ghost" href="#/settings">[icon.edit + span 'הגדרות']</a>
</div>
```

לחילופין: כפתור גלגל-שיניים בקצה השמאלי של `app-header` (ב-`src/components/header.js`).

## כללי "page structure" (לעקביות)
1. **תמיד `page-head`** בראש (לא `card-row` עם h2). זה נותן את הטיפוגרפיה הסריפית הנכונה.
2. **כפתור פעולה ראשית = `btn-gold`** עם אייקון משמאל ו-`<span>טקסט</span>` מימין.
3. **כפתור משני = `btn` רגיל** (לא ghost, אלא אם בטל).
4. **כפתור הרסני = `btn-danger`**, תמיד עם `confirmAction()` לפני הביצוע.
5. **כל input min-height 48px** (מובטח דרך base.css).
6. **כל מסך מקבל max-width מ-main** (אין צורך ב-style מותאם).

## דברים שלא לעשות
- ❌ **אסור** להוסיף route ל-router בלי לרשום את ה-crumbs.
- ❌ **אסור** להשתמש ב-emoji. רק `icon.x(size)` מ-icons.js.
- ❌ **אסור** להוסיף את ה-h1 בלי `font-family: var(--ff-serif)` (זה אוטומטי דרך `.page-head h1` ב-base.css).
- ❌ **אסור** להוסיף inline styles בעברית. הכל דרך classes ב-base.css.
- ❌ **אסור** לקרוא ישירות ל-localStorage. תמיד דרך `load()`/`save()` ב-`store/db.js`.

## בדיקה
1. `npm run build && npm run preview`
2. Navigate to `#/settings`.
3. צילום עם Playwright.
4. וידוא שה-crumbs נכונים (ראשי › הגדרות).
5. שמירה → toast מופיע → reload → הערכים נשמרו.

## דוגמאות קיימות בקוד
- View פשוט (קריאה בלבד): `src/views/home.js`
- View עם CRUD מלא + modals: `src/views/priceListEditor.js`
- View עם state מקומי + persist on blur: `src/views/quoteBuilder.js`

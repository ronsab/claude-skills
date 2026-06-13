# Architecture — נקודת חשמל

## Tree (קובץ אחר קובץ)
```
nekudat-hashmal/
├── BUILD_SPEC.md                # מקור האמת (אל תשנה!)
├── .impeccable.md               # design context לסקילי impeccable/frontend-design
├── price_list.csv               # גיבוי ידני באקסל
├── index.html                   # dir="rtl" lang="he", theme-color #0A1929
├── package.json                 # vanilla + vite + vite-plugin-pwa + jspdf + html2canvas + idb-keyval
├── vite.config.js               # PWA config: manifest + workbox precache
├── public/
│   ├── price_list.json          # seed 77 סעיפים אמיתיים מבנארית פרו
│   ├── logo_nekudat_hashmal.png # רקע שחור! (אזהרה ב-§2 של BUILD_SPEC)
│   ├── manifest.webmanifest     # נוצר ע"י vite-plugin-pwa
│   ├── icons/
│   │   ├── icon-192.png         # אייקון PWA קטן
│   │   └── icon-512.png         # אייקון PWA גדול
│   └── fonts/
│       ├── heebo-hebrew.woff2
│       ├── heebo-latin.woff2
│       ├── frank-ruhl-libre-hebrew.woff2
│       └── frank-ruhl-libre-latin.woff2
└── src/
    ├── main.js                  # entry: ensureSeed → renderHeader → initRouter
    ├── router.js                # hash router, 7 routes
    ├── components/
    │   ├── header.js            # app-header עם פס זהב + breadcrumbs
    │   ├── icons.js             # 19 אייקוני Lucide SVG inline (MIT)
    │   └── ui.js                # escapeHtml, fmtMoney, fmtDate, toast, confirmAction, openModal, el, uid
    ├── store/
    │   ├── db.js                # localStorage helper, schema-version 1, key 'nh.v1'
    │   ├── idb.js               # IndexedDB wrapper סביב idb-keyval (ל-PDF blobs)
    │   ├── priceLists.js        # ensureSeed, CRUD מחירונים, CRUD סעיפים, getBusiness
    │   └── quotes.js            # CRUD הצעות, computeTotals, chapterBreakdown, DEFAULT_TERMS
    ├── views/
    │   ├── home.js              # מסך ראשי: hero-block + 3 tiles
    │   ├── priceListEditor.js   # 2 מסכים: רשימת מחירונים + עורך מחירון
    │   ├── quoteBuilder.js      # בונה הצעה: 4 cards + modals (item picker + custom line)
    │   ├── quotePreview.js      # תצוגה מקדימה + ייצוא PDF + שיתוף
    │   └── quoteList.js         # רשימת ההצעות עם פעולות
    ├── pdf/
    │   ├── render.js            # html2canvas + jsPDF, multi-page, downloadBlob, sharePdfBlob
    │   ├── templateCommon.js    # pdfHead, pdfTitleBar, pdfClientBlock, pdfTotalsBlock, pdfTermsBlock, pdfSignatures, pdfFooter
    │   ├── templateSimple.js    # מצב פשוט: טבלה אחת
    │   └── templateStructured.js # מצב מובנה: פרקים + סיכום ביניים + עמוד ריכוז
    └── styles/
        ├── base.css             # design tokens + רכיבים (header, tile, card, table, btn, modal, toast)
        └── pdf.css              # סטיילינג ל-PDF rendering (navy gradient head, gold accent, serif title)
```

## Entities (מודל נתונים)

### `Item` (סעיף מחירון)
```ts
{
  number: '01.01.002',          // מספר הסעיף המקורי מבנארית פרו
  chapter: '01',                 // קוד פרק
  chapterName: 'נקודות',         // שם פרק
  subchapter: '01.01',           // (אופציונלי)
  description: '...',
  unit: 'יח׳',                  // יחידה
  price: 164                     // ב-ILS
}
```

### `PriceList`
```ts
{
  id: 'pl_xxx',                  // uid
  name: 'מחירון ראשי',
  isPrimary: true,               // לא ניתן למחיקה
  createdAt: ISO string,
  items: Item[]
}
```

### `Quote` (הצעת מחיר)
```ts
{
  id: 'q_xxx',
  number: '2026-001',            // counter רץ פר שנה
  createdAt: ISO,
  date: 'YYYY-MM-DD',
  mode: 'simple' | 'structured',
  priceListId: 'pl_xxx',         // לתיעוד בלבד! המחירים נשמרים על שורות
  client: { name, phone, address, contact },
  lines: QuoteLine[],
  vatRate: 18,
  discountAmount: 0,
  discountPercent: 0,
  terms: { validityDays, payment, warranty, note },
  status: 'draft' | ...,
  pdfBlobKey: 'pdf_xxx' | null   // key ל-IndexedDB
}
```

### `QuoteLine` (שורת הצעה, **מחיר מוקפא**)
```ts
{
  number: '01.01.002',
  chapter: '01',
  chapterName: 'נקודות',
  description: '...',
  unit: 'יח׳',
  qty: 12,
  unitPrice: 164                 // snapshot בעת ההוספה. אסור לשנות אחרי שהההצעה נשמרה.
}
```

## Data flow

### יצירת הצעה (sequence)
1. `home.js` → `#/quotes/new`
2. `router.js` → `renderQuoteBuilder(root, ctx)`
3. `quoteBuilder.js` → `createQuote({ priceListId })` ← מ-`store/quotes.js`
4. משתמש לוחץ "הוסף מהמחירון" → `openItemPicker(quote, onAdded)`
5. בורר → קורא ל-`getPriceList(quote.priceListId)` ← מ-`store/priceLists.js`
6. בחירת סעיפים → `quote.lines.push({ ..., unitPrice: src.price })` ← **כאן הקפאת המחיר**
7. שמירה → `updateQuote(quote.id, patch)` ← מ-`store/quotes.js` ← `save()` ב-localStorage

### ייצוא PDF (sequence)
1. `quotePreview.js` → `getOrCreateBlob()`
2. אם `quote.pdfBlobKey` קיים → `idbGet(key)` → return cached blob
3. אחרת:
   a. `renderElementToPdf(domEl)` → `html2canvas` → canvas → jsPDF multi-page → blob
   b. `idbSet(newKey, blob)` ← לשמירה ב-IndexedDB
   c. `updateQuote(quote.id, { pdfBlobKey: newKey })`
4. `downloadBlob(blob, filename)` או `sharePdfBlob(blob, filename)`

### Routes (hash-based)
| Hash | View | Match group |
|---|---|---|
| `#/` | home.renderHome | — |
| `#/price-lists` | priceListEditor.renderPriceListIndex | — |
| `#/price-lists/:id` | priceListEditor.renderPriceListEditor | `m[1] = id` |
| `#/quotes` | quoteList.renderQuoteList | — |
| `#/quotes/new` | quoteBuilder.renderQuoteBuilder | — |
| `#/quotes/:id/edit` | quoteBuilder.renderQuoteBuilder | `m[1] = id` |
| `#/quotes/:id` | quotePreview.renderQuotePreview | `m[1] = id` |

## Storage layers

### localStorage (`nh.v1`)
```js
{
  schema: 1,
  priceLists: PriceList[],     // ~30KB עבור 77 סעיפים × 1-3 מחירונים
  quotes: Quote[],              // ~5KB פר הצעה
  counters: { 'quotes.2026': 7 },
  business: { brand, contractor, vat_id, phone, address, email, logo_file }
}
```
**גודל מקסימלי**: 5MB (ברירת מחדל דפדפן).

### IndexedDB
- DB: `keyval-store` (ברירת מחדל של idb-keyval)
- Object store: `keyval`
- Keys: `pdf_<quoteId>_<timestamp>`
- Values: `Blob` (application/pdf)
- **גודל**: ~250KB-1MB per PDF. מאות MB ב-quota.

### Service Worker cache (Workbox precache)
- `index.html`, כל JS bundle, כל CSS, כל פונט, כל אייקון, ה-logo, ו-`price_list.json`.
- TTL: ללא תפוגה (autoUpdate על שינוי build).

## Debugging tips

### לנקות הכל ולהתחיל מהתחלה
```js
// ב-DevTools Console:
(async () => {
  for (const r of await navigator.serviceWorker.getRegistrations()) await r.unregister();
  for (const n of await caches.keys()) await caches.delete(n);
  for (const db of await indexedDB.databases()) indexedDB.deleteDatabase(db.name);
  localStorage.clear();
  location.reload();
})();
```

### לכפות ייצור PDF מחדש (לאחר שינוי תבנית)
```js
const data = JSON.parse(localStorage.getItem('nh.v1'));
for (const q of data.quotes) q.pdfBlobKey = null;
localStorage.setItem('nh.v1', JSON.stringify(data));
```

### לראות מה ה-SW cache
DevTools → Application → Cache Storage → `workbox-precache-v2`.

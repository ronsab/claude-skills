# תהליכים, מכונת-מצבים ולוגיקה

## 1. מכונת-מצבים של הזמנה
```
draft → submitted → [approval?] → sent_to_warehouse → picking → picked
      → loaded → out_for_delivery → delivered → invoiced → closed
ביטול:  כל מצב לפני-ליקוט → cancelled        (משחרר שריון)
החזרה:  delivered/invoiced → return_requested → returned (זיכוי)
```

| מעבר | מי מפעיל | תופעות לוואי |
|---|---|---|
| draft → submitted | סוכן/לקוח | re-resolve מחיר + snapshot + חישוב totals |
| submitted → pending_approval | מערכת | אם הנחה > תקרת סוכן או חריגת מסגרת אשראי |
| pending_approval → sent_to_warehouse | תפעול/בעלים מאשרים | אחרת חסום |
| submitted/approved → sent_to_warehouse | מערכת (אוטומטי) | **שריון מלאי** + StockMovement=reservation. כאן ההזמנה נשלחת אוטומטית למחסן |
| sent_to_warehouse → picking | מחסנאי לוקח | — |
| picking → picked | מחסנאי | רישום qty_picked; חוסר → short/substitution |
| picked → loaded | מלגזן/מחסנאי | שיוך ל-Delivery |
| loaded → out_for_delivery | נהג/תפעול | StockMovement=pick: הורדת qty_on_hand + שחרור reservation |
| out_for_delivery → delivered | נהג | POD (חתימה/תמונה), כמות נמסרה |
| delivered → invoiced | הנה"ח/אוטומטי | InvoiceRef דרך ספק חיצוני + DeliveryNote (אם טרם) |
| כל מצב לפני-ליקוט → cancelled | תפעול/בעלים | שחרור reservation |

**החלטת תזמון:** שריון ב-`sent_to_warehouse`, הורדה פיזית מ-`qty_on_hand` ב-`loaded/out`. כך `qty_available` אמין מרגע המחויבות (מונע מכירת-יתר), ו-`qty_on_hand` משקף מציאות פיזית עד שהסחורה יוצאת.

## 2. לוגיקת תמחור — server function `resolvePrice`
חישוב דטרמיניסטי בצד-שרת לכל שורת הזמנה:
1. **base** = `Product.base_price`.
2. **מחירון חל** לפי קדימות: `customer_specific` (לקוח זה) > `agent` (סוכן ההזמנה) > `customer_type` (פרטי/עסקי) > base. ה-match הראשון שמכיל PriceListItem למוצר מנצח; אם מחירון חל אך אין לו שורה למוצר — נופלים למחירון הבא.
3. `list_unit_price` = `PriceListItem.price` או `base × (1 − discount_pct_off_base)`.
4. **הנחה ידנית/סוכן**: מוחלת אך **clamp** ל-`agent.max_discount_pct`. בקשה > תקרה → השורה מותרת אך ההזמנה מסומנת `requires_approval` ומנותבת לתפעול/בעלים.
5. **מע"מ**: `line_ex_vat = unit_price × qty`; `vat = line_ex_vat × vat_rate` (0 אם פטור); `line_inc_vat = ex_vat + vat`.

על כל OrderLine נשמר snapshot: `resolved_unit_price`, `applied_price_list`, `discount_pct`, `vat_amount`. חובה לשלמות המסמכים.

## 3. מלאי בזמן אמת ומניעת מכירת-יתר — `reserveInventory`
Base44 חסר row locks / טרנזקציות רב-מסמכיות. הפתרון: כל שינוי מלאי עובר **server function יחיד** עם optimistic concurrency:
1. submit קורא ל-`reserveInventory(orderId)`.
2. קריאת כל InventoryItem, בדיקה `qty_available ≥ qty_ordered`.
3. כתיבת `qty_reserved` החדש **רק אם** version/updated_at לא השתנה מאז הקריאה (compare-and-set). אם אין conditional update — re-read לאחר כתיבה ואימות, ורישום שורת StockMovement כ-ledger סמכותי.
4. בקונפליקט: retry עד N פעמים; אם נכשל או מלאי לא מספיק → `backordered` + התראה.

**מיטיגציות:** לרכז את כל שינויי המלאי בפונקציה אחת; ledger StockMovement כמקור-אמת + job תקופתי לחישוב-מחדש (self-heal). ל-SMB עם מעט סוכנים — soft reservation מספיק והסיכון מתועד.

## 4. קליטת מלאי (Receipt)
קליטה → StockMovement type=receipt (+qty) → `qty_on_hand += qty`. ידני ב-MVP; בעזרת ברקוד בשלב 2.

## 5. מספור מסמכים רציף — `Counter`
order_number / delivery_note_number / quote_number מוגדלים אך ורק דרך server function שמגדיל `Counter.current_value` באופן מוגן (אותה בעיית concurrency כמו מלאי). מספרי חשבונית/קבלה חוקיים מנוהלים ע"י הספק החיצוני.

## 6. זרימת מסמכים (הצעת מחיר / תעודת משלוח / חשבונית / קבלה)
**גישה משולבת**: פנימי (Quote, DeliveryNote) + ספק חיצוני (חשבונית מס, קבלה).

### 6.1 הצעת מחיר → הזמנה
```
Quote: draft → sent → approved → converted   (או rejected / expired)
```
- הצעת מחיר נוצרת ע"י סוכן/משרד עם שורות פריטים (snapshot מחיר/מע"מ כמו OrderLine) ותוקף (`valid_until`).
- אישור הלקוח (פורטל) או הסוכן → server function `convertQuoteToOrder`: יוצר Order עם אותם snapshots, מסמן את ההצעה `converted`, ושומר `converted_order_id`. משם ההזמנה ממשיכה במכונת-המצבים הרגילה (כולל auto-send למחסן).

### 6.2 תעודת משלוח
מופקת בתוך המערכת ב-`picked/loaded` דרך `issueDeliveryNote(orderId)` — מספור רציף (Counter) + PDF RTL + snapshot של כמות שנמסרה.

### 6.3 חשבונית מס / קבלה (ספק חיצוני)
- `issueInvoice(orderId)` → קריאה ל-API של הספק (חשבונית ירוקה / חשבשבת / ריווחית / ...), קבלת `allocation_number` + `pdf_url`, שמירת `DocumentRef`(doc_type=tax_invoice).
- רישום `Payment` → `issueReceipt(paymentId)` → DocumentRef(doc_type=receipt/tax_invoice_receipt) + סימון ההזמנה כשולמה.
- זיכוי (החזרות, שלב 2) → DocumentRef(doc_type=credit_note).
- כל ה-DocumentRef נשמרים במערכת לצפייה/הורדה, אך המסמך החוקי חי אצל הספק.

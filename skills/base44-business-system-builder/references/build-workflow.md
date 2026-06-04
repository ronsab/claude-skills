# לולאת בנייה ב-Base44 דרך MCP

## כלי MCP
| כלי | שימוש |
|---|---|
| `create_base44_app` | יצירת אפליקציה. **מילות המשתמש המדויקות** ב-appPrompt. אסינכרוני. |
| `edit_base44_app` | בקשת שינוי לאפליקציה קיימת. **מילות המשתמש**. אסינכרוני. |
| `list_entity_schemas` | אימות שהישויות נוצרו עם השדות הנכונים. |
| `create_entity_schema` | הגדרת/השלמת ישות חסרה (+ RLS). |
| `create_entities` | זריעת רשומות דמו (עד 100 לקריאה; לא ניתן ליצור User). |
| `update_entities` | עדכון רשומות לפי query + אופרטורים (`$set` וכו'). |
| `query_entities` | קריאת רשומות לאימות (כולל User). |

## כללי עבודה (חובה)
1. **אחרי `create_base44_app`/`edit_base44_app` — החזר למשתמש מיד את ה-editorUrl** כקישור
   markdown, לפני כל קריאת כלי נוספת. כל העריכה נעשית בעורך Base44, לא בצ'אט.
2. **מילות המשתמש כפי שהן** ב-appPrompt/editPrompt — אל תרחיב/תשכתב; ל-Base44 AI משלו להרחבה.
3. **צעד-אחר-צעד, בבטחה**: לא לשלוח עריכה חדשה לפני שהקודמת נקלטה ואומתה (אחרת שוברים מה שעבד).
4. **אמת כל שלב** דרך `list_entity_schemas`/`query_entities`. נהל מפת-דרכים עם שער-אימות לכל שלב.
5. אל תקרא את ה-output file של סוכנים/transcript גדול — עלול להציף context.

## server functions מרכזיים (לרכז בהם את הלוגיקה הרגישה)
- **`resolvePrice(customer, agent, product, qty)`** — base → מחירון לפי קדימות
  (customer_specific > agent > customer_type > base) → הנחת-סוכן **clamped** ל-`max_discount_percent`
  (חריגה → `requires_approval`) → מע"מ. מחזיר snapshot שנשמר ב-OrderLine.
- **`reserveInventory(orderId)`** — מלאי בזמן אמת: קריאה → בדיקת `qty_available ≥ qty` → כתיבה
  מותנית (compare-and-set על version/updated_at) → על קונפליקט retry; אחרת `backordered`.
  רשום StockMovement כ-ledger סמכותי. (Base44 חסר טרנזקציות — רכז כל שינוי מלאי בפונקציה אחת.)
- **`submitOrder(orderId)`** — re-resolve+snapshot, ניתוב לאישור בחריגה, אחרת **שליחה אוטומטית למחסן** (`sent_to_warehouse`) + שריון.
- **`convertQuoteToOrder(quoteId)`** — הצעה מאושרת → Order עם אותם snapshots, סימון `converted`.
- **`issueDeliveryNote(orderId)`** — מספור רציף (Counter) + PDF RTL.
- **`issueInvoice(orderId)` / `issueReceipt(paymentId)`** — קריאה לספק (Green Invoice), `allocation_number`, DocumentRef.
- מספור: **`Counter`** מוגדל אך ורק כאן (רצף ללא דילוגים).

## מכונת-מצבים של הזמנה (התאם לעברית של Base44)
```
טיוטה → נשלחה → [אישור?] → מאושרת/נשלחה_למחסן → בליקוט → מוכנה_למשלוח
      → בדרך → נמסרה → חויבה → סגורה
ביטול: לפני-ליקוט → בוטלה (משחרר שריון)
החזרה: נמסרה/חויבה → החזרה (זיכוי)
```

## רצף בנייה מומלץ
1. `create_base44_app` (מילות המשתמש) → editorUrl.
2. `list_entity_schemas` → אמת/השלם ישויות.
3. זריעת דמו (`create_entities`) — מוצרים **עם תמונות**, לקוחות, מחירונים, הזמנה/הצעה/ת.משלוח/תשלום.
4. עריכות אינקרמנטליות (`edit_base44_app`) לליבה: גלריית קנייה, מלאי בזמן אמת, auto-למחסן, תקרת הנחה, אינטגרציית ספק.
5. אימות מקצה-לקצה + מסמכי אפיון ב-repo (PRD/data-model/permissions/workflows).

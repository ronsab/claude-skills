# מודל נתונים גנרי — Base44 entities לעסק ישראלי

סימון: `→` = הפניה (id). שדות מחיר ex-VAT (ללא מע"מ) אלא אם צוין. התאם את שמות הישויות/שדות
למה ש-Base44 יוצר אוטומטית (לעיתים `current_stock` במקום InventoryItem נפרד, ו-`items[]` משובץ
בתוך Order במקום OrderLine נפרד) — שני המודלים תקפים; בחר את הפשוט יותר לפי גודל הפרויקט.

**עיקרון על:** מצב פיננסי/מחיר נשמר כ-**snapshot** בשורת ההזמנה/המסמך כדי שמסמכים היסטוריים
יישארו immutable גם כשהמחירונים משתנים.

## קטלוג ומלאי
- **Product** — `sku`(unique), `barcode`, `name`(עברית), `category`, `unit`(יחידה/קרטון/מארז/ק"ג/ליטר), `units_per_package`, `base_price`(ex-VAT), `cost_price`, `vat_included`(bool), `image_url`, `current_stock`, `min_stock`, `warehouse_location`, `is_active`, `supplier`.
- **Category** — `name`, `parent_category→`(עץ), `sort_order`, `is_active`.
- **InventoryItem** (אם מפרידים) — `product→`, `qty_on_hand`, `qty_reserved`, `qty_available`, `reorder_point`, `bin_location`.
- **StockMovement / InventoryLog** (ledger) — `product→`, `change_type`(כניסה/יציאה/ספירה/החזרה/תיקון), `quantity_change`, `previous_stock`, `new_stock`, `reference_order_id`, `performed_by`. מקור-אמת לביקורת/שחזור.

## תמחור
- **PriceList** — `name`, `customer_type`(עסקי/פרטי/VIP/סוכן/כללי), `discount_percent`, `is_active`, `items[]`(מחיר מיוחד למוצר + `max_discount`).
- (אופציונלי) **PriceListItem** נפרד עם `priority` ל-customer_specific > agent > customer_type > base.

## לקוחות וסוכנים
- **Customer** — `name`, `customer_type`(עסקי/פרטי), `contact_name`, `phone`, `email`, `address`, `city`, `tax_id`(ח.פ/ע.מ — עסקי), `payment_terms`(מזומן/שוטף+30/60/90), `price_list`, `max_credit`, `current_balance`, `assigned_agent_id`, `status`.
- **Agent** — `user→`, `name`, `phone`, `territory`, `max_discount_percent`, `assigned_price_list`, `commission_pct`.

## הזמנות
- **Order** — `order_number`(Counter), `customer_id/name`, `agent_id/name`, `status`(טיוטה/נשלחה/ממתינה_לאישור/מאושרת/בליקוט/מוכנה_למשלוח/בדרך/נמסרה/בוטלה/החזרה), `items[]`(snapshot: product, quantity, unit_price, discount_percent, line_total, picked_quantity), `subtotal`, `vat_amount`, `total`, `requires_approval`, `approval_status`, `delivery_date/address/city`, `payment_status`.
- **OrderLine** (אם מפרידים) — `order→`, `product→`, `qty_ordered/picked/delivered`, snapshot מחיר, `pick_status`, `bin_location`.

## אספקה ומסמכים
- **Delivery** — `order→`, `driver_id/name`, `scheduled_date`, `status`(ממתין/יצא_לדרך/נמסר/נמסר_חלקית/כשל/הוחזר), `delivery_photo`, `signature_url`, `failure_reason`, `delivered_at`. (POD)
- **Quote (הצעת מחיר — פנימי)** — `quote_number`(Counter), `customer`, `agent`, `status`(טיוטה/נשלחה/אושרה/נדחתה/פגה/הומרה), `valid_until`, `items[]`(snapshot), `subtotal/vat_amount/total`, `converted_order_id/number`.
- **DeliveryNote (תעודת משלוח — פנימי)** — `note_number`(Counter), `order`, `customer`, `items[]`(ordered/delivered qty), `issue_date`, `driver_name`, `signature_url`.
- **DocumentRef (חשבונית/קבלה — ספק חיצוני)** — `doc_type`(חשבונית מס/קבלה/חשבונית מס-קבלה/זיכוי), `provider_name`, `external_id`, `allocation_number`(מספר הקצאה), `customer`, `order`, `total_amount`, `pdf_url`, `issue_date`.
- **Payment (תשלום)** — `customer`, `order`, `amount`, `payment_method`(מזומן/אשראי/העברה/צ'ק), `payment_date`, `reference`, `document_ref_id`(קבלה שהונפקה).

## עזר
- **Counter** — `name`(order_number/quote_number/delivery_note_number), `current_value`. מוגדל אך ורק דרך server function (מספור רציף ללא דילוגים).
- **User** — Base44 native + `role`(enum תפקידים), `display_name`, `phone`, `max_discount_percent`(לסוכן), `assigned_warehouse`(אופציונלי!), `vehicle_number`(אופציונלי!), `is_active`.
  **אזהרה:** אל תגדיר `assigned_warehouse`/`vehicle_number` כ-required — הם רלוונטיים רק לנהג/מחסנאי ויחסמו יצירת בעלים/לקוח.

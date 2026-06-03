# מודל הנתונים — Base44 entities

סימון: `→` = הפניה (foreign key לפי id). שדות מחיר ex-VAT (ללא מע"מ) אלא אם צוין אחרת.
עיקרון: מצב פיננסי/מחיר נשמר כ-**snapshot** ב-OrderLine כדי שמסמכים היסטוריים יישארו immutable.

## קטלוג
### Product (מוצר)
| שדה | טיפוס | הערות |
|---|---|---|
| sku | string | ייחודי, אינדקס |
| barcode | string | EAN/UPC, אינדקס |
| name_he | string | שם בעברית |
| description_he | string | |
| category | →Category | |
| unit | enum | יח'/ק"ג/קרטון |
| units_per_case | number | כמות ביחידת אריזה |
| base_price | number | מחיר עוגן ex-VAT |
| vat_rate | number | ברירת מחדל 0.18 |
| is_vat_exempt | bool | |
| image_url | string | תמונה ראשית |
| gallery_images | string[] | |
| min_order_qty | number | |
| weight_kg | number | |
| is_active | bool | |
| default_bin | string | מיקום מדף ברירת מחדל |

### Category (קטגוריה)
`name_he`, `parent_category`→Category (עץ), `sort_order`, `image_url`, `is_active`.

## מלאי
### InventoryItem (מלאי) — רשומה לכל מוצר (לכל מחסן בשלב 2)
`product`→, `qty_on_hand`, `qty_reserved`, `qty_available`(=on_hand−reserved), `reorder_point`, `bin_location`, `last_counted_at`.

### StockMovement (תנועת מלאי) — ledger append-only, מקור-אמת
`product`→, `type`(receipt/reservation/release/pick/adjustment/return), `qty_delta`(+/−), `order`→(nullable), `user`→, `timestamp`, `note`.

## תמחור
### PriceList (מחירון)
`name_he`, `type`(customer_type/agent/customer_specific), `applies_to_customer_type`(private/business/null), `applies_to_agent`→(null), `priority`(int), `valid_from`, `valid_to`, `is_active`.

### PriceListItem (שורת מחירון)
`price_list`→, `product`→, `price`(ex-VAT) **או** `discount_pct_off_base`, `min_qty`(שלב 2).

### Discount (הנחה) — promos / הנחת-סוכן מפורשת
`scope`(order/line/customer), `type`(pct/amount), `value`, `granted_by`→User, `reason_he`, `requires_approval`, `approved_by`→User.
תקרת הסוכן (`max_discount_pct`) יושבת על Agent, לא כאן.

## לקוחות וסוכנים
### Customer (לקוח)
`type`(private/business), `name_he`, `phone`, `email`, `addresses[]`(משלוח+חיוב).
עסקי בלבד: `company_name`, `vat_id`(ח.פ/ע.מ), `tax_invoice_required`, `credit_terms`(שוטף+30…), `credit_limit`, `current_balance`.
`assigned_agent`→, `default_price_list`→(אופציונלי), `linked_user`→(לפורטל), `is_active`.

### Agent (סוכן)
`user`→, `name_he`, `phone`, `territory`, `max_discount_pct`, `commission_pct`(שלב 2), `assigned_price_list`→, `is_active`.

## הזמנות
### Order (הזמנה)
`order_number`(רץ, דרך Counter), `customer`→, `agent`→, `created_by`→User, `status`(ר' workflows), `channel`(agent/self_service/office), `delivery_address`, `requested_delivery_date`, `notes_he`, `requires_approval`, `approved_by`→.
rollups (snapshot): `subtotal_ex_vat`, `total_discount`, `vat_total`, `grand_total_inc_vat`. דגלים: `is_invoiced`, `delivery_note_id`, `invoice_ref_id`.

### OrderLine (שורת הזמנה)
`order`→, `product`→, `qty_ordered`, `qty_picked`, `qty_delivered`.
snapshot תמחור: `resolved_unit_price`, `applied_price_list`→, `discount_pct`, `vat_amount`, `line_total_inc_vat`.
`pick_status`(pending/picked/short/substituted), `bin_location`.

## אספקה ומסמכים
### Delivery (משלוח)
`orders[]`, `driver`→User, `vehicle`, `route_date`, `stops[]`, `status`(planned/loaded/out_for_delivery/delivered/failed), `delivered_at`, `signature_url`, `proof_photo_url`, `recipient_name`.

### DeliveryNote (תעודת משלוח)
`note_number`(רץ, דרך Counter), `order`→, `customer`→, `lines[]`(snapshot של כמות שנמסרה), `issued_at`, `pdf_url`.

### InvoiceRef (הפניה לחשבונית של הספק החיצוני)
`provider`, `external_invoice_id`, `allocation_number`(מספר הקצאה), `type`(חשבונית מס / חשבונית מס-קבלה / זיכוי), `customer`→, `order`→, `total_inc_vat`, `pdf_url`, `issued_at`.

## עזר
### Counter (רצף בטוח)
`name`(order_number/delivery_note_number), `current_value`. מוגדל אך ורק דרך server function.

### User
Base44 native + `role`(enum: owner/ops/agent/warehouse/forklift/driver/accounting/business_customer/private_customer), `display_name_he`, `linked_agent`→/`linked_customer`→, `is_active`.

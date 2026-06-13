# save-client — שמירת לקוח ב-Pinecone בסיום עבודה

## מטרה
שמור את פרופיל הלקוח הנוכחי ב-Pinecone לשימוש עתידי עם לקוחות דומים.

---

## שלב 1: אסוף פרטים לשמירה

שאל את רון (רק מה שלא ברור מהקונטקסט):

1. **שם הלקוח / שם העסק?**
2. **תחום העסק?**
3. **מה נבנה בפועל?** (דף נחיתה / אוטומציה / ...)
4. **CTA שנבחר?** (וואטסאפ / טופס / טלפון)
5. **מה עבד טוב?** (מה שהלקוח אהב, מה הצליח)
6. **מחיר?** (₪)
7. **תוצאה?** (success / ongoing / unknown)

---

## שלב 2: שמירה ב-Pinecone

הפעל את שלב 4 מהסקיל `ron-client-search`:

```
id: client_[שם-ללא-רווחים]_[YYYY-MM-DD]
text: "[תחום] - [מה נבנה] - [מה עבד] - [CTA] - [תוצאה]"
type: client
domain: [תחום]
price: [מחיר מספרי]
cta_type: whatsapp/form/call
outcome: success/ongoing/unknown
date: [תאריך]
```

---

## שלב 3: אישור

לאחר השמירה:
"לקוח [שם] נשמר ב-Pinecone. בפעם הבאה שתעבוד עם לקוח מתחום [תחום], אני אמצא את הניסיון הזה אוטומטית."

---

## שלב 4: Case Study (אופציונלי, רק אם outcome=success)

**אם** הפרויקט הצליח (outcome=success), שאל:
"רוצה ליצור Case Study אנונימי? זה ייקח 10 דקות וייצור חומר שיווקי שתוכל לפרסם באתר/לינקדאין/הצעות מחיר."

אם כן:
1. הפעל את הסקיל `anthropic-skills:ron-system-case-study`
2. שמור את ה-Case Study בתיקייה: `~/Documents/ron-marketing-assets/case-studies/`
3. הודע: "Case Study מוכן. רעיון: לכלול אותו בהצעת המחיר הבאה (יש תבנית ב-`ron-digital-quote`)"

**אם** outcome=ongoing/unknown — דלג. אפשר ליצור Case Study בעתיד כשתהיינה תוצאות.

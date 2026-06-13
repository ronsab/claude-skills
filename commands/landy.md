# /landy — בניית רכיב יצירתי והטמעתו ב-LANDY

בנה רכיב HTML יצירתי לפי הבקשה, פרוס ל-Vercel, והחזר embed code מוכן ל-LANDY.

## הבקשה
$ARGUMENTS

## זרימת עבודה

### שלב 1: הבנת הבקשה
נתח מה הרכיב צריך לכלול:
- סוג הרכיב (hero / כרטיסי שירות / testimonials / timer / gallery / אחר)
- אנימציות נדרשות (GSAP / Three.js / CSS / ללא)
- תוכן: טקסטים, CTA, צבעים, סגנון
- אם לא צוין סגנון — השתמש בפלטה של RON DIGITAL STUDIO (שחור/זהב/לבן)

### שלב 2: בניית HTML
צור קובץ `landy-component/index.html` עם:
- HTML מלא, עצמאי (standalone — לא תלוי בקבצים חיצוניים מלבד CDN)
- כל CSS inline או ב-`<style>` בתוך הקובץ
- כל JS ב-`<script>` בתוך הקובץ
- ספריות דרך CDN בלבד (GSAP, Three.js, Lottie)
- RTL מלא אם התוכן בעברית: `dir="rtl"`, `text-align: right`
- Responsive: עובד מעולה על מובייל וdeskop
- `width: 100%; height: auto` — מתאים לכל רוחב iframe
- ללא scrollbar חיצוני (overflow: hidden על body אם רכיב קבוע)

```
landy-component/
├── index.html        ← הקובץ הראשי
└── vercel.json       ← הגדרות Vercel
```

### שלב 3: vercel.json
```json
{
  "version": 2,
  "builds": [{ "src": "index.html", "use": "@vercel/static" }],
  "routes": [{ "src": "/(.*)", "dest": "/index.html" }],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Frame-Options", "value": "ALLOWALL" },
        { "key": "Content-Security-Policy", "value": "frame-ancestors *" }
      ]
    }
  ]
}
```
⚠️ חובה להוסיף headers לאפשר iframe embedding!

### שלב 4: פריסה ל-Vercel
הרץ:
```bash
cd landy-component && vercel --yes --prod
```
קבל את ה-URL הציבורי.

### שלב 5: החזרת embed code

הצג למשתמש **3 אפשרויות הטמעה**:

#### אפשרות A — iframe מלא (מומלץ)
```html
<iframe 
  src="VERCEL_URL" 
  style="width:100%; height:600px; border:none; display:block;"
  loading="lazy"
  title="רכיב מותאם אישית">
</iframe>
```

#### אפשרות B — iframe responsive (גובה אוטומטי)
```html
<div style="position:relative; width:100%; padding-bottom:56.25%; height:0; overflow:hidden;">
  <iframe 
    src="VERCEL_URL"
    style="position:absolute; top:0; left:0; width:100%; height:100%; border:none;"
    loading="lazy">
  </iframe>
</div>
```

#### אפשרות C — script embed (אם LANDY תומכת)
```html
<script>
  document.write('<iframe src="VERCEL_URL" style="width:100%;height:600px;border:none;"></iframe>');
</script>
```

### שלב 6: הנחיות הטמעה ב-LANDY

הסבר למשתמש:
1. פתח את עורך LANDY
2. חפש בלוק מסוג: **"Embed"** / **"HTML"** / **"Custom Code"** / **"iFrame"**
3. אם קיים — הדבק את אפשרות A
4. אם אין — בדוק ב-Settings → Integrations → Custom Scripts
5. אם כלום לא עובד — צלם screenshot מהעורך של LANDY ושלח לי

### שלב 7: בדיקה
אחרי ההטמעה:
- בדוק שהרכיב נטען נכון
- בדוק על מובייל (320px, 768px)
- אם יש שגיאות CORS — עדכן vercel.json

---
name: landing-page-builder
description: >
  בנייה מלאה של דפי נחיתה פרמיום לעסקים קטנים ובינוניים בישראל — כולל 3D, RTL עברית, אנימציות canvas, ו-Three.js hero.
  הפעל סקיל זה בכל פעם שמשתמש מבקש לבנות דף נחיתה, landing page, אתר ויטרינה, דף שיווקי, או כל דף חד-עמודי לעסק.
  מתאים לכל תחום: אבטחה, שיפוצים, אינסטלציה, רואה חשבון, קוסמטיקה, מסעדה, עורך דין, ועוד.
  הפעל גם כשהמשתמש אומר "תבנה לי אתר", "צריך דף לעסק שלי", "עשה לי landing page", "תיצור דף נחיתה".
  אל תשתמש בסקיל זה למערכת ניהול רב-משתמשים עם בסיס נתונים/הרשאות/מלאי/הזמנות (← השתמש ב-base44-business-system-builder), או למצגת (← ron-digital-presentation).
---

# Landing Page Builder — דפי נחיתה פרמיום לעסקים ישראליים

## עקרונות הסקיל

אתה בונה דפי נחיתה שמייצרים לידים. כל דף הוא קובץ HTML בודד (אפס תלויות חיצוניות מלבד CDN),
עם עיצוב פרמיום 3D, RTL עברית מלאה, ואנימציות canvas ייחודיות לתחום העסקי.

**תוצר**: קובץ `.html` אחד שעובד מכל דפדפן, ניתן לשלוח ללקוח ישר.

---

## שלב 1 — שאלון לקוח

**קרא את הקובץ:** `references/questionnaire.md`

אסוף את כל המידע לפני שמתחיל לכתוב קוד. אם חלק מהפרטים כבר הוזכרו בשיחה — חלץ אותם ואל תשאל שוב.
מטרה: לקבל תשובות לכל השאלות הקריטיות בסבב שאלות אחד.

---

## שלב 2 — בחירת פלטת צבעים (לכל פרויקט בנפרד)

**קרא:** `references/color-palettes.md`

לכל פרויקט חדש בחר פלטה שמתאימה לתחום ולתחושה הרצויה:
- אם יש צבעי מותג → בנה פלטה מותאמת אישית
- אם אין → בחר מהרשימה לפי תחום

הכרז על הבחירה **לפני הבנייה**:
```
🎨 פלטה: [שם-פלטה]
   bg: #XXXXXX | accent1: #XXXXXX | accent2: #XXXXXX
   Three.js: [geometry] + lights: [color1] / [color2]
```

---

## שלב 3 — תכנון הדף

לאחר קבלת המידע ובחירת הפלטה, הכרז על התוכנית:

```
✅ שם עסק: [שם]
✅ תחום: [תחום]
✅ פלטה: [שם] — [רקע] + [accent1] + [accent2]
✅ סקשנים: Hero → Counters → Services (N כרטיסים) → Why Us → [...]  → Contact
✅ אנימציות canvas: [רשימה לפי services]
✅ פונט: Heebo
```

קרא `references/canvas-library.md` כדי לבחור את אנימציות ה-canvas המתאימות לשירותים.

---

## שלב 3 — בנייה

**קרא את:** `references/design-system.md` לפני הקידוד.

### מבנה HTML חובה

```html
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[שם עסק] — [סלוגן]</title>
  <!-- Google Fonts -->
  <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;700;800;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
  <!-- Font Awesome -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <!-- Three.js -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <style>/* כל ה-CSS כאן */</style>
</head>
<body>
  <!-- header, hero, sections... -->
  <script>/* כל ה-JS כאן */</script>
</body>
</html>
```

### סקשנים סטנדרטיים

קרא `references/sections.md` לפירוט מלא של כל סקשן.

**סדר מומלץ:**
1. `#header` — sticky, לוגו + nav + CTA טלפון
2. `#hero` — Three.js canvas + כותרת + כפתורים
3. `#counters` — 4 נתונים מספריים
4. `#services` — כרטיסי שירות עם canvas
5. `#why-us` — 3 יתרונות
6. `#we-bring` — 6 סיבות לבחור (checklist)
7. `#value-table` — "מה כלול" + CTA
8. `#about` — על החברה
9. `#testimonials` — המלצות לקוחות
10. `#faq` — שאלות נפוצות (accordion)
11. `#contact` — טופס + פרטי קשר
12. `footer` + כפתור WhatsApp צף

**הוסף/הסר סקשנים לפי צרכי הלקוח הספציפי.**

---

## שלב 4 — JS חובה בכל דף

```javascript
// 1. Three.js hero (ראה design-system.md)
// 2. Canvas animations לכל כרטיס שירות (ראה canvas-library.md)
// 3. 3D tilt על service cards
document.querySelectorAll('.srv-card').forEach(card => {
  card.addEventListener('mousemove', e => {
    const r = card.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width - 0.5;
    const y = (e.clientY - r.top) / r.height - 0.5;
    card.style.transform = `rotateX(${-y*22}deg) rotateY(${x*22}deg) translateZ(35px)`;
    card.querySelector('.srv-display')?.style.setProperty('transform',`translateZ(22px) translateX(${x*10}px) translateY(${y*10}px)`);
    card.querySelector('h3')?.style.setProperty('transform',`translateZ(40px) translateX(${x*14}px) translateY(${y*14}px)`);
    card.querySelector('p')?.style.setProperty('transform',`translateZ(18px) translateX(${x*7}px) translateY(${y*7}px)`);
  });
  card.addEventListener('mouseleave', () => {
    card.style.transform = '';
    ['.srv-display','h3','p'].forEach(s => card.querySelector(s)?.style.removeProperty('transform'));
  });
});
// 4. Counters count-up
// 5. FAQ accordion
// 6. Sticky header
// 7. IntersectionObserver reveal
// 8. Timestamp HUD (אם יש מצלמות/CCTV בשירותים)
// 9. Burger menu mobile
```

---

## שלב 5 — הוספות מתקדמות (לפי צורך הפרויקט)

לפני סגירת הקובץ, בדוק אם הלקוח צריך את הפריטים הבאים:

### SEO ו-Meta Tags
**קרא:** `references/seo.md`
- הוסף `<title>`, `<meta description>`, Open Graph, Schema.org LocalBusiness
- אם אין domain — השאר placeholders מוסברים
- og:image: השתמש ב-placehold.co עם צבעי הפרויקט כ-fallback

### WhatsApp Integration
**קרא:** `references/whatsapp-integration.md`
- ברירת מחדל: שיטה 1 (click-to-chat, אפס הגדרות)
- אם יש Make.com + WA Business ← שיטה 2 (webhook אוטומטי)
- תמיד הוסף כפתור WhatsApp צף (`.wa-float`)

### Google Analytics + Meta Pixel
**קרא:** `references/tracking.md`
- שאל את הלקוח על IDs לפני הכנסה
- אל תמציא IDs — השאר placeholder מוסבר אם לא סופק
- הוסף event tracking: form submit, phone click, WhatsApp click

---

## שלב 6 — אימות

לאחר כתיבת הקובץ:

1. הפעל שרת מקומי:
```javascript
// Node.js one-liner
node -e "const h=require('http'),fs=require('fs'),p=require('path');h.createServer((q,r)=>{const f=p.join(process.cwd(),q.url==='/'?'[filename].html':q.url);fs.readFile(f,(e,d)=>{r.writeHead(e?404:200,{'Content-Type':'text/html'});r.end(d||'')})}).listen(4900,()=>console.log('ready'))"
```

2. צלם screenshot עם Playwright:
```
mcp__plugin_playwright__browser_navigate → http://localhost:4900/
mcp__plugin_playwright__browser_take_screenshot (fullPage: true)
```

3. בדוק: Hero 3D נטען? כרטיסי שירות מוצגים? אין שגיאות console?

4. **בדיקות מובייל** — קרא `references/mobile-checklist.md`:
```
mcp__plugin_playwright__browser_resize → 375 × 812
mcp__plugin_playwright__browser_take_screenshot
mcp__plugin_playwright__browser_resize → 768 × 1024
mcp__plugin_playwright__browser_take_screenshot
```

---

## כללי RTL חובה

- `<html dir="rtl" lang="he">`
- כל הטקסט בעברית — placeholders, labels, aria-labels
- Tailwind/CSS: `text-right`, `margin-left` (לא `margin-right`) לאייקונים
- פונט `Heebo` לכל הטקסט, `Share Tech Mono` לאלמנטי HUD/tech
- בדוק שהניווט במובייל תקין

---

## טעויות נפוצות למנוע

| בעיה | פתרון |
|---|---|
| Canvas נשאר 300×150px | הוסף `width:100%;height:100%;display:block` ל-CSS + `resize()` ב-JS |
| Three.js לא מתאים לגודל | הוסף `window.addEventListener('resize', onResize)` |
| 3D cards לא עובדות | ודא `transform-style: preserve-3d` על הכרטיס ו-`perspective` על הcontainer |
| RTL שבור | בדוק `dir="rtl"` על `<html>`, לא רק על `<body>` |
| WhatsApp link שגוי | פורמט: `https://wa.me/972XXXXXXXXX` (ללא מקפים, עם 972) |
| SEO חסר | קרא `references/seo.md` — הוסף meta description + OG + Schema.org |
| Tracking IDs מומצאים | אל תמציא IDs — השתמש ב-placeholder מוסבר, ראה `references/tracking.md` |
| מובייל שבור | עבור על `references/mobile-checklist.md` לפני מסירה |
| טופס לא מגיע ללקוח | בחר שיטת WhatsApp מ-`references/whatsapp-integration.md` |

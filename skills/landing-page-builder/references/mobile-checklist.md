# Mobile Checklist — בדיקות מובייל לדף נחיתה

בצע את כל הבדיקות לפני מסירה ללקוח.

---

## רשימת בדיקה מהירה

### ✅ HTML בסיס
- [ ] `<meta name="viewport" content="width=device-width, initial-scale=1.0">` קיים
- [ ] `<html dir="rtl" lang="he">` — RTL על התגית הראשית
- [ ] כל ה-placeholder ו-labels בעברית
- [ ] כותרת `<title>` ברורה

### ✅ כפתורי CTA — גודל מגע
- [ ] כל כפתור: מינימום `44px` גובה (אצבע אנושית)
- [ ] כפתור טלפון — `href="tel:XXXXXXXXXX"` תקין
- [ ] כפתור WhatsApp — `href="https://wa.me/972XXXXXXXXXX"` תקין
- [ ] כפתורי hero נפרדים ולא חופפים

### ✅ Three.js / Canvas במובייל
```javascript
// Three.js — הפחת עומס על מובייל
const isMobile = /Mobi|Android/i.test(navigator.userAgent);
if (isMobile) {
  // פחות חלקיקים
  const N = isMobile ? 200 : 600;
  // pixel ratio מוגבל — חוסך GPU
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, isMobile ? 1 : 2));
  // אפשר לעצור לגמרי אם רוצים לחסוך סוללה:
  // canvas3d.style.display = 'none';
}
```

### ✅ Grid מובייל
```css
/* שים לב שאלה קיימים */
@media (max-width: 900px) {
  .srv-grid { grid-template-columns: repeat(2, 1fr); }
  .why-grid { grid-template-columns: 1fr; }
  .contact-grid { grid-template-columns: 1fr; }
}
@media (max-width: 560px) {
  .srv-grid { grid-template-columns: 1fr; }
  .cnt-grid { grid-template-columns: repeat(2, 1fr); }
  .bring-grid { grid-template-columns: 1fr; }
  .test-grid { grid-template-columns: 1fr; }
}
```

### ✅ Header מובייל
- [ ] Burger menu מוצג בפחות מ-768px
- [ ] nav נסתר כברירת מחדל
- [ ] JS מפעיל `.open` על הקלקה
- [ ] כפתור הטלפון בheader קצר מספיק

```javascript
// burger toggle — ודא שיש
document.getElementById('burger')?.addEventListener('click', () => {
  document.getElementById('main-nav')?.classList.toggle('open');
});
// סגור nav בלחיצה על לינק
document.querySelectorAll('#main-nav a').forEach(a => {
  a.addEventListener('click', () => document.getElementById('main-nav')?.classList.remove('open'));
});
```

### ✅ טקסט וכותרות
- [ ] `font-size` כותרת H1: `clamp(1.8rem, 6vw, 3.5rem)` — לא גדול מדי במובייל
- [ ] `font-size` טקסט רגיל: מינימום `0.9rem`
- [ ] שורות לא חתוכות — `overflow-x: hidden` על body

### ✅ WhatsApp צף
- [ ] כפתור WhatsApp צף לא חוסם תוכן חשוב
- [ ] במובייל: bottom/right מרווח מספיק מהקצה

### ✅ טופס יצירת קשר
- [ ] `input[type=tel]` — keyboard מספרי נפתח על מובייל
- [ ] שדות מספיק גדולים ללחיצה
- [ ] placeholder בעברית ברור

---

## כיצד לבדוק במהירות

### בדפדפן (Chrome DevTools):
1. פתח דף ב-`http://localhost:4900/`
2. `F12` → אייקון Mobile בפינה (או `Ctrl+Shift+M`)
3. בחר "iPhone SE" (375px) ו-"iPad" (768px)
4. גלול מלמעלה למטה, לחץ על כל הכפתורים

### עם Playwright:
```
browser_resize → 375 × 812 (iPhone SE)
browser_take_screenshot
browser_resize → 768 × 1024 (iPad)
browser_take_screenshot
```

---

## בעיות נפוצות ופתרונות

| בעיה | פתרון |
|---|---|
| Canvas מחוץ למסך | הוסף `max-width:100%; overflow:hidden` לcontainer |
| כפתורים קטנים מדי | `min-height: 44px; padding: .75rem 1.5rem` |
| Three.js איטי | `isMobile` check + הפחת חלקיקים |
| nav לא נסגר | הוסף event listener על כל link |
| טקסט hero קטן | `clamp()` על font-size |
| WhatsApp button חוסם form | `bottom: 5rem` במקום `1.5rem` אם form קרוב לתחתית |
| RTL שבור בinput | `text-align: right; direction: rtl` על input |

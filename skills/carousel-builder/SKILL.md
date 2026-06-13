---
name: carousel-builder
description: >
  Build branded Instagram/social CAROUSEL image sets — multi-slide HTML at 4:5 (1080×1350)
  or square (1080×1080), then auto-export each slide to pixel-perfect PNGs via Playwright.
  This is GRAPHIC slide design, not copywriting. Use whenever the user wants to CREATE the
  visual slides of a carousel: "תבנה קרוסלה", "carousel for Instagram", "שקופיות לאינסטגרם",
  "סט תמונות לפוסט", "תכין לי קרוסלה על המוצר/השירות", "demo carousel", "swipe post graphics",
  "תמונות לקרוסלה", or when turning a product/service/feature list into shareable IG slides.
  Produces RON DIGITAL-branded slides (dark navy + amber, RTL Hebrew) with phone-mockup,
  pain, solution, feature, stats, and CTA components baked in, plus a ready PNG export pipeline.
  Pairs with `social-content` (which writes the captions/copy) — this skill renders the actual
  graphics. NOT for animated Reels/video (use `hyperframes-best-practices`) and NOT for a
  scrolling landing page (use `landing-page-builder`).
---

# Carousel Builder

בניית סט שקופיות גרפיות לאינסטגרם/סושיאל — קובץ HTML אחד עם N שקופיות, וייצוא אוטומטי ל-PNG.
זה כלי **עיצוב גרפי** של השקופיות עצמן, לא כתיבת קופי (לקופי → `social-content`).

## מתי להשתמש
- המשתמש רוצה לבנות את **התמונות** של קרוסלה (לא רק את הטקסט)
- הדגמת מוצר/שירות/פיצ'רים כסט שקופיות להחלקה
- פוסט קרוסלה שיווקי, "before/after", "X טיפים", הסבר תהליך בשלבים

## מתי לא (ניתוב לסקיל אחר)
- וידאו/Reel מונפש → `hyperframes-best-practices` (MP4)
- דף נחיתה גלילה לאתר → `landing-page-builder`
- כתיבת כיתובים/האשטגים/לוח תוכן → `social-content` / `israeli-social-content`
- פוסטר בודד / אמנות → `canvas-design`

## זרימת עבודה

### 1. אסוף דרישות
- **נושא ומטרה**: על מה הקרוסלה? (מוצר, שירות, הדגמה, טיפים) ומה המטרה (לידים, מודעות, הדגמה)
- **קהל**: מי הצופה? התאם שפה וכאבים
- **מספר שקופיות**: ברירת מחדל 8-10 (אינסטגרם תומך עד 20)
- **מידות**: ברירת מחדל **4:5 (1080×1350)** — תופס הכי הרבה מסך. ריבוע 1080×1080 אם המשתמש מבקש
- **מיתוג**: ברירת מחדל RON DIGITAL (ראה `references/brand-tokens.md`). אם זה ללקוח עם מותג משלו — שאל צבעים/לוגו

### 2. תכנן את הקשת הנרטיבית
כל שקופית צריכה לעמוד בפני עצמה (קרוסלה נצרכת שקף-שקף). מבנה מומלץ:

| שקופית | תפקיד |
|--------|-------|
| 1 | **Hook** — עוצר גלילה. שאלה/כאב חד + ויזואל בולט |
| 2 | **הכאב** — המצב היום (כרטיסים עם אייקונים) |
| 3 | **הפתרון** — הצגת המוצר/הרעיון המרכזי |
| 4-N | **פיצ'רים** — שקופית לכל יכולת, עם phone-mockup או ויזואל |
| N-1 | **סיכום/למי מתאים** — bullets או צ'יפים |
| N | **CTA** — קריאה לפעולה + פרטי קשר + מותג |

### 3. בנה את ה-HTML
התחל מ-`assets/template-carousel.html` — תבנית מוכנה עם:
- מערכת `.slide` (1080×1350), רקע glow+grid, kicker מותג, מספור, swipe hint
- פונקציות ייצוא `showOnly(n)` ו-`showAll()` מובנות
- RTL מלא + `<bdi>` סביב כל מספר/מחיר/אחוז/תאריך (קריטי — אחרת ה-bidi הופך אותם)

לרכיבי שקופית מוכנים (hook, pain, solution, feature+phone, stats, CTA) → `references/slide-components.md`.
לטוקני צבע/פונט/מרווח → `references/brand-tokens.md`.

**כללי זהב:**
- כל אלמנט בגודל קריא בתמונה: כותרת 64px+, גוף 30px+, תווית 18px+
- `font-variant-numeric: tabular-nums` על עמודות מספרים
- אל תשתמש ב-`<br>` באמצע טקסט זורם (רק בכותרות תצוגה קצרות)
- אל תמציא נתונים אמיתיים (טלפון/URL/שם) — שאל את המשתמש

### 4. בדוק ויזואלית
פתח בדפדפן, עבור שקופית-שקופית עם `showOnly(n)`. ודא: RTL תקין, מספרים לא הפוכים, ניגודיות מספקת, כל שקף שלם בפריים.

### 5. ייצא ל-PNG
הרץ את ה-pipeline ב-`references/export-pipeline.md` — Playwright מצלם כל שקופית ב-1080×1350 מדויק, שומר לתיקייה, ומאמת מימדים. זה השלב שבו רוב הבעיות קורות (lock על דפדפן, viewport) — עקוב אחרי הקובץ בדיוק.

## תוצר סופי
- `<name>-carousel.html` — הקובץ המקורי (לעריכות עתידיות)
- תיקיית PNG: `slide-01.png` ... `slide-NN.png`, כולן בדיוק במידות שנבחרו, מוכנות להעלאה כקרוסלה אחת

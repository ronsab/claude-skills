# טוקני מותג — RON DIGITAL (ברירת מחדל)

המיתוג שאוב מאפליקציות RON (כמו נקודת חשמל) — corporate/luxury, כהה, אמבר.
אם בונים ללקוח עם מותג משלו, החלף את הצבעים/פונט בלבד; המבנה נשאר.

## צבעים
```css
:root{
  --bg:    #0A1929;  /* רקע ראשי — navy כהה */
  --bg2:   #0D2137;  /* רקע משני (כרטיסים, phone) */
  --amber: #FFB300;  /* accent — הדגשות, CTA, מספרים */
  --white: #fff;
  --mut:   rgba(255,255,255,.55);  /* טקסט משני */
  --mut2:  rgba(255,255,255,.35);  /* טקסט עמום */
  --line:  rgba(255,255,255,.08);  /* גבולות */
  --green: #00CC64;  /* חיובי (שולם, פעיל) */
  --red:   #FF5A5A;  /* כאב/שלילי */
}
```

## טיפוגרפיה
- פונט: **Heebo** (Google Fonts, תומך עברית). משקלים 300-900
- כותרת ראשית: 96-108px, weight 900
- כותרת שקופית: 64-72px, weight 800
- גוף: 30-40px, weight 400
- תווית/מטא: 16-24px
- תמיד `font-family:'Heebo','Arial Hebrew',Arial,sans-serif`
- אל תוסיף `<link>`/`@import` אם משתמשים ב-hyperframes compiler; ל-Playwright export הרגיל — `<link>` ל-Google Fonts תקין

## RTL ו-bidi (קריטי)
- `<html lang="he" dir="rtl">`, כל קונטיינר טקסט RTL
- **כל מספר/מחיר/אחוז/תאריך/טלפון בתוך עברית → עטוף ב-`<bdi>`**
  דוגמאות: `<bdi>₪3,690</bdi>`, `<bdi>50</bdi> מ׳`, `<bdi>68%</bdi>`, `<bdi>15/03/2026</bdi>`
  בלי זה, אלגוריתם ה-bidi הופך את הסדר (₪3,690 → 096,3₪)
- טלפון: `<bdi dir="ltr">050-621-7775</bdi>`
- אנימציית כניסה (אם יש): `x` חיובי = כניסה מימין (נכון לעברית)

## רקע משותף (glow + grid + bolt)
```css
.bg-glow{position:absolute;inset:0;pointer-events:none;
  background:
    radial-gradient(ellipse 800px 460px at 50% 0%, rgba(255,179,0,.10) 0%, transparent 68%),
    radial-gradient(ellipse 460px 380px at 8% 90%, rgba(255,179,0,.055) 0%, transparent 60%);}
.bg-grid{position:absolute;inset:0;pointer-events:none;
  background-image:linear-gradient(rgba(255,179,0,.03) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,179,0,.03) 1px,transparent 1px);
  background-size:56px 56px;}
```
הימנע מגרדיאנט לינארי על כל המסך (banding ב-H.264/דחיסה) — העדף radial או solid + glow מקומי.

## אלמנטי מסגרת קבועים בכל שקופית
- **kicker** (פינה עליונה): נקודה אמבר + "RON DIGITAL"
- **מספור**: "01 / 10" בפינה הנגדית (LTR)
- **swipe hint** (תחתית): "החלק להמשך ←" — לא בשקופית האחרונה

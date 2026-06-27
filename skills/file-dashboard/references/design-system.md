# Design System — ספריית רכיבים לדשבורד

מערכת עיצוב מלאה לבניית דשבורד HTML יחיד, RTL. ברירת המחדל היא ה-DNA הכהה (כחול-ציאן), אבל הצבעים הם משתני `:root` — אז אפשר להחליף פלטה בקלות לפי בחירת המשתמש (ראה "פלטות מוכנות").

## תוכן
1. [בסיס: CSS, צבעים, טיפוגרפיה](#בסיס)
2. [פלטות מוכנות + צבעי מותג](#פלטות-מוכנות)
3. [מבנה כללי של העמוד](#מבנה-העמוד)
4. [רכיב: כרטיס KPI](#כרטיס-kpi)
5. [רכיב: גרף Bar](#גרף-bar)
6. [רכיב: Donut SVG](#donut-svg)
7. [רכיב: Level Cards](#level-cards)
8. [רכיב: ציטוטים](#ציטוטים)
9. [רכיב: תובנות / נקודות עיוורון](#תובנות)
10. [רכיב: ציר זמן / מגמה](#ציר-זמן)
11. [טאבים — JS](#טאבים)
12. [איזה גרף מתי](#בחירת-גרף)

---

## בסיס

```css
:root {
  --bg: #0a0e1a;
  --surface: #111827;
  --surface2: #1a2235;
  --border: #1f2d45;
  --text: #f0f4ff;
  --text2: #8b9fc0;
  --accent1: #3b82f6; /* כחול */
  --accent2: #06b6d4; /* ציאן */
  --accent3: #f59e0b; /* כתום */
  --accent4: #10b981; /* ירוק */
  --accent5: #ef4444; /* אדום */
  --accent6: #8b5cf6; /* סגול */
}
* { margin: 0; padding: 0; box-sizing: border-box; }
html { direction: rtl; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: 'Heebo', sans-serif;
  line-height: 1.6;
  background-image:
    radial-gradient(circle at 15% 10%, rgba(59,130,246,.08), transparent 40%),
    radial-gradient(circle at 85% 90%, rgba(6,182,212,.06), transparent 40%);
  min-height: 100vh;
}
.wrap { max-width: 1200px; margin: 0 auto; padding: 32px 20px; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: none; } }
.card { animation: fadeIn .5s ease both; }
```

טען את הפונט ב-`<head>`:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;700;900&display=swap" rel="stylesheet">
```

---

## פלטות מוכנות

המשתמש בוחר פלטה בשלב 1. כדי להחיל — **החלף רק את בלוק ה-`:root`** בערכים של הפלטה שנבחרה; כל שאר ה-CSS נשאר זהה כי הכל מתבסס על המשתנים. ערכי ה-`radial-gradient` ב-body הם דקורטיביים; אם הם לא מתאימים לפלטה בהירה — אפשר להחליש או להסיר אותם.

### 1. Midnight (ברירת מחדל · כהה כחול-ציאן)
זו הפלטה בבלוק "בסיס" למעלה. מתאימה לרוב הדשבורדים, נתונים עסקיים, מצגות על מסך.

### 2. Light Slate (בהיר · רשמי / להדפסה)
רקע לבן, טקסט כהה. מתאים לדוחות פיננסיים, מסמכים רשמיים, או כשצריך להדפיס.
```css
:root {
  --bg:#f5f7fb; --surface:#ffffff; --surface2:#eef2f9; --border:#dce3ef;
  --text:#172033; --text2:#5b6b88;
  --accent1:#2563eb; --accent2:#0891b2; --accent3:#d97706;
  --accent4:#059669; --accent5:#dc2626; --accent6:#7c3aed;
}
```
בפלטה בהירה הסר/החלש את ה-`radial-gradient` הכהה ב-body (למשל רקע אחיד `var(--bg)`).

### 3. Royal Purple (כהה · סגול-מגנטה)
אנרגטי, יצירתי. טוב לתוכן שיווקי, מועדון, נושאים "צעירים".
```css
:root {
  --bg:#0d0a1a; --surface:#17122a; --surface2:#221a3a; --border:#2e2348;
  --text:#f3f0ff; --text2:#a99fc8;
  --accent1:#8b5cf6; --accent2:#6366f1; --accent3:#f59e0b;
  --accent4:#06b6d4; --accent5:#ec4899; --accent6:#d946ef;
}
```

### 4. Emerald (כהה · ירוק-טורקיז)
רגוע, אמין. טוב לבריאות, כספים-חיוביים, קיימות.
```css
:root {
  --bg:#08130f; --surface:#0f1f18; --surface2:#163026; --border:#1f4133;
  --text:#eafff5; --text2:#8fc0aa;
  --accent1:#10b981; --accent2:#14b8a6; --accent3:#84cc16;
  --accent4:#06b6d4; --accent5:#f59e0b; --accent6:#3b82f6;
}
```

### 5. Sunset (כהה · חם כתום-אדום)
חם, נועז. טוב לתוכן רגשי, אוכל, אירועים.
```css
:root {
  --bg:#1a0f0a; --surface:#241612; --surface2:#33201a; --border:#45291f;
  --text:#fff4f0; --text2:#c8a99f;
  --accent1:#f97316; --accent2:#ef4444; --accent3:#f59e0b;
  --accent4:#eab308; --accent5:#ec4899; --accent6:#a855f7;
}
```

### צבעי מותג מותאמים (המשתמש נתן צבעים משלו)
אם המשתמש נתן קוד/קודי hex או צבעי מותג:
1. הצבע הראשי → `--accent1` (וגם משפיע על ה-gradient של הגרפים).
2. בחר רקע: כהה (`#0a…`) אם הצבע רווי, או בהיר אם המשתמש רוצה נקי/רשמי.
3. השלם `--accent2..6` בגוונים משלימים (אנלוגיים/משלימים) כדי שגרפים עם כמה סדרות יישארו קריאים.
4. **בדוק ניגודיות**: טקסט (`--text`) חייב להיות קריא בבירור על `--surface`. אם לא — כהה/הבהר את הרקע. פלטה יפה שלא קריאה = כישלון.

---

## מבנה העמוד

```
Header (כותרת + תת-כותרת + meta)
KPI Row (3–4 כרטיסים)
Tabs Navigation
  Tab 1 (סקירה — גרפים)
  Tab 2 (פילוח / פירוט)
  Tab 3 (תובנות / המלצות)
Footer
```
המבנה גמיש — מספר הטאבים והתוכן לפי המיקוד. אל תנפח ל-4 טאבים אם 2 ממוקדים מספיקים.

```css
.header { margin-bottom: 28px; border-bottom: 1px solid var(--border); padding-bottom: 20px; }
.header h1 { font-size: 32px; font-weight: 900; }
.header .sub { color: var(--text2); font-size: 16px; margin-top: 6px; }
.header .meta { color: var(--text2); font-size: 13px; margin-top: 10px; display: flex; gap: 16px; flex-wrap: wrap; }
.grid { display: grid; gap: 16px; }
.grid-2 { grid-template-columns: repeat(2, 1fr); }
.grid-3 { grid-template-columns: repeat(3, 1fr); }
.grid-4 { grid-template-columns: repeat(4, 1fr); }
@media (max-width: 760px) { .grid-2, .grid-3, .grid-4 { grid-template-columns: 1fr; } }
.panel { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 22px; }
.panel h3 { font-size: 18px; margin-bottom: 16px; font-weight: 700; }
```

---

## כרטיס KPI

מספר גדול אחד עם תווית. גבול עליון צבעוני.
```html
<div class="kpi card" style="--c:var(--accent1)">
  <div class="kpi-num">1,248</div>
  <div class="kpi-label">סה״כ רשומות</div>
  <div class="kpi-delta">+12% מהחודש שעבר</div>
</div>
```
```css
.kpi { background: var(--surface); border: 1px solid var(--border); border-radius: 16px;
  padding: 22px; position: relative; overflow: hidden; }
.kpi::before { content:""; position:absolute; top:0; right:0; left:0; height:3px;
  background: linear-gradient(90deg, var(--c), transparent); }
.kpi-num { font-size: 40px; font-weight: 900; color: var(--c); line-height: 1.1; }
.kpi-label { color: var(--text2); font-size: 14px; margin-top: 6px; }
.kpi-delta { font-size: 12px; margin-top: 8px; color: var(--accent4); }
```

---

## גרף Bar

להשוואת קטגוריות. רוחב ה-fill = (ערך / מקסימום) * 100%.
```html
<div class="bar-item">
  <div class="bar-label">צפון</div>
  <div class="bar-track"><div class="bar-fill" style="width:78%;
    background:linear-gradient(90deg,var(--accent1),var(--accent2))"></div></div>
  <div class="bar-value">312</div>
</div>
```
```css
.bar-item { display: grid; grid-template-columns: 130px 1fr 56px; align-items: center; gap: 12px; margin-bottom: 12px; }
.bar-label { font-size: 14px; color: var(--text2); text-align: left; }
.bar-track { background: var(--surface2); border-radius: 8px; height: 26px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 8px; transition: width 1s ease; }
.bar-value { font-weight: 700; font-size: 15px; }
```

---

## Donut SVG

לפילוח של שלם (אחוזים שמסתכמים ל-100%). **חישוב חובה:** היקף = 2πr. עבור r=60 → 376.99.
לכל קטע: `stroke-dasharray="LEN REST"`, `stroke-dashoffset="-CUMULATIVE"` כאשר LEN = (אחוז/100)*376.99.
```html
<!-- 50% כחול, 30% ציאן, 20% כתום. r=60, היקף=376.99 -->
<svg width="170" height="170" viewBox="0 0 160 160" style="transform:rotate(-90deg)">
  <circle cx="80" cy="80" r="60" fill="none" stroke="var(--surface2)" stroke-width="22"/>
  <circle cx="80" cy="80" r="60" fill="none" stroke="var(--accent1)" stroke-width="22"
    stroke-dasharray="188.5 188.49" stroke-dashoffset="0"/>
  <circle cx="80" cy="80" r="60" fill="none" stroke="var(--accent2)" stroke-width="22"
    stroke-dasharray="113.1 263.89" stroke-dashoffset="-188.5"/>
  <circle cx="80" cy="80" r="60" fill="none" stroke="var(--accent3)" stroke-width="22"
    stroke-dasharray="75.4 301.59" stroke-dashoffset="-301.6"/>
</svg>
```
מקרא ליד ה-donut: ריבוע צבע + תווית + אחוז. אם יש יותר מ-6 קטעים — עדיף bar אופקי.

---

## Level Cards

לדירוג/רמות (מתחיל/בינוני/מתקדם, נמוך/בינוני/גבוה):
```html
<div class="level-card" style="--c:var(--accent4)">
  <div class="level-name">מתקדם</div>
  <div class="level-bignum">87</div>
  <div class="level-pct">34%</div>
</div>
```
```css
.level-card { background: var(--surface); border: 1px solid var(--border);
  border-right: 4px solid var(--c); border-radius: 12px; padding: 18px; }
.level-name { color: var(--text2); font-size: 14px; }
.level-bignum { font-size: 30px; font-weight: 900; color: var(--c); }
.level-pct { font-size: 13px; color: var(--text2); }
```

---

## ציטוטים

מהשאלות הפתוחות / מהמסמך. 30–200 תווים, עם תגית.
```html
<div class="quote card">
  <div class="quote-text">"הכי קשה לי למצוא זמן ללמוד את הכלים החדשים"</div>
  <div class="quote-tag">מחסום זמן</div>
</div>
```
```css
.quote { background: var(--surface2); border-radius: 12px; padding: 18px;
  border-right: 3px solid var(--accent6); }
.quote-text { font-size: 15px; font-style: italic; }
.quote-tag { display: inline-block; margin-top: 10px; font-size: 12px;
  background: rgba(139,92,246,.15); color: var(--accent6); padding: 3px 10px; border-radius: 20px; }
```

---

## תובנות

כרטיס תובנה/נקודת-עיוורון: כותרת, תיאור, מספר תומך, ואופציונלית פעולה. עדיפות בהמלצות: 🔴 חובה / 🟡 מומלץ / 🟢 בונוס.
```html
<div class="insight card">
  <div class="insight-head"><span class="insight-icon">📊</span><h4>רוב התגובות מהצפון</h4></div>
  <p class="insight-body">42% מהרשומות (312) מגיעות מאזור הצפון — פי 2 מהמרכז.</p>
  <div class="insight-action">🟡 שקול קמפיין ממוקד למרכז</div>
</div>
```
```css
.insight { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 20px; }
.insight-head { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.insight-icon { font-size: 22px; }
.insight h4 { font-size: 16px; font-weight: 700; }
.insight-body { color: var(--text2); font-size: 14px; }
.insight-action { margin-top: 12px; font-size: 13px; color: var(--accent3); }
```

---

## ציר זמן

למגמה לאורך זמן — trend bars אנכיים או polyline SVG.
```html
<div class="trend">
  <div class="trend-bar" style="height:40%"><span>ינו</span></div>
  <div class="trend-bar" style="height:65%"><span>פבר</span></div>
  <div class="trend-bar" style="height:90%"><span>מרץ</span></div>
</div>
```
```css
.trend { display: flex; align-items: flex-end; gap: 10px; height: 160px; }
.trend-bar { flex: 1; background: linear-gradient(180deg, var(--accent2), var(--accent1));
  border-radius: 8px 8px 0 0; position: relative; min-height: 6px; }
.trend-bar span { position: absolute; bottom: -22px; right: 0; left: 0; text-align: center;
  font-size: 11px; color: var(--text2); }
```
לערכים עם שלילי (רווח/הפסד) — קו אמצע, בר חיובי כלפי מעלה בצבע `--accent4`, שלילי כלפי מטה בצבע `--accent5`.

---

## טאבים

```html
<div class="tabs">
  <button class="tab-btn active" onclick="showTab(event,'overview')">סקירה</button>
  <button class="tab-btn" onclick="showTab(event,'breakdown')">פילוח</button>
  <button class="tab-btn" onclick="showTab(event,'insights')">תובנות</button>
</div>
<div id="tab-overview" class="tab-content active"> ... </div>
<div id="tab-breakdown" class="tab-content"> ... </div>
<div id="tab-insights" class="tab-content"> ... </div>
```
```css
.tabs { display: flex; gap: 8px; margin: 24px 0 20px; flex-wrap: wrap; border-bottom: 1px solid var(--border); }
.tab-btn { background: none; border: none; color: var(--text2); font-family: inherit;
  font-size: 15px; padding: 10px 18px; cursor: pointer; border-bottom: 2px solid transparent; }
.tab-btn.active { color: var(--text); border-bottom-color: var(--accent1); font-weight: 700; }
.tab-content { display: none; }
.tab-content.active { display: block; animation: fadeIn .4s ease both; }
```
```javascript
function showTab(e, name) {
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
  document.getElementById('tab-' + name).classList.add('active');
  e.currentTarget.classList.add('active');
}
```

---

## בחירת גרף

| המטרה | הרכיב |
|---|---|
| להשוות כמויות בין קטגוריות | גרף Bar |
| פילוח של שלם לאחוזים (≤6 קטעים) | Donut |
| פילוח עם הרבה קטגוריות | Bar אופקי ממוין |
| דירוג / רמות | Level Cards |
| מגמה לאורך זמן | ציר זמן / trend bars |
| ערכים חיוביים ושליליים (רווח/הפסד) | trend bars עם קו אמצע |
| מספר בודד חשוב | כרטיס KPI |
| קול המשתמש / טקסט חופשי | ציטוטים |
| מסקנה + פעולה | כרטיס תובנה |

כלל אצבע: אל תשתמש ב-donut ליותר מ-6 קטעים, ואל תשים יותר מ-4 KPI בשורה. עדיף פחות גרפים מדויקים על הרבה מבולגנים.

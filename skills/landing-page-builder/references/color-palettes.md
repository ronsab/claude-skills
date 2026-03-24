# Color Palettes Library — פלטות צבע לדפי נחיתה

כל פלטה היא ערכת CSS variables מלאה + הגדרות Three.js lighting + המלצת geometry.
בחר פלטה **לפי תחום ותחושה רצויה** — ואז העתק את ה-CSS variables שלה ישירות לדף.

---

## איך לבחור פלטה

### שלב 1 — בדוק אם ללקוח יש צבעי מותג
- **כן** → השתמש ב"פלטה מותאמת אישית" (בתחתית הקובץ)
- **לא** → המשך לשלב 2

### שלב 2 — בחר לפי תחום + תחושה

| תחום | פלטה מומלצת |
|---|---|
| אבטחה, טכנולוגיה, IT | `security-navy` או `tech-dark` |
| שיפוצים, בנייה, אלומיניום | `construction-orange` |
| רפואה, קוסמטיקה, ספא | `health-teal` או `beauty-purple` |
| מסעדה, קייטרינג, אוכל | `food-warm` |
| עורך דין, רואה חשבון, פיננסים | `legal-midnight` |
| נדל"ן, ביטוח | `realestate-gold` |
| חינוך, פסיכולוגיה | `education-blue` |
| כללי / לא ברור | `classic-dark` |

---

## הפלטות

---

### `security-navy` — אבטחה, גז, טכנולוגיה
**תחושה**: מקצועי, בטוח, טכנולוגי

```css
:root {
  --bg:       #04090f;
  --bg2:      #060d18;
  --bg3:      #08111f;
  --glass:    rgba(8,17,32,0.80);
  --border:   rgba(0,180,255,0.12);
  --border-g: rgba(201,168,76,0.20);
  --accent1:  #f0b429;   /* gold */
  --accent1-l:#ffd060;
  --accent1-dim: rgba(240,180,41,0.12);
  --accent2:  #00aaff;   /* electric blue */
  --accent2-dim: rgba(0,170,255,0.12);
  --txt:      #c8d8f0;
  --txt-dim:  rgba(200,216,240,0.50);
  --navy:     #0a1628;
  --wa:       #25d366;
  --mono:     'Share Tech Mono', monospace;
  /* Three.js */
  --3js-core-color: 0x0a1f5e;
  --3js-wire-color: 0x00aaff;
  --3js-ring-color: 0xf0b429;
  --3js-light1: 0x00b4ff;
  --3js-light2: 0xf0b429;
  --3js-geometry: IcosahedronGeometry(1.8, 0);
}
```

---

### `tech-dark` — IT, רשתות, סייבר
**תחושה**: עתידני, אנליטי, טכנולוגי עמוק

```css
:root {
  --bg:       #030812;
  --bg2:      #050c1a;
  --bg3:      #071020;
  --glass:    rgba(5,12,26,0.85);
  --border:   rgba(0,255,180,0.12);
  --border-g: rgba(0,200,255,0.18);
  --accent1:  #00ffc8;   /* neon green-teal */
  --accent1-l:#80ffdf;
  --accent1-dim: rgba(0,255,200,0.10);
  --accent2:  #0084ff;   /* deep blue */
  --accent2-dim: rgba(0,132,255,0.10);
  --txt:      #b8d4e8;
  --txt-dim:  rgba(184,212,232,0.50);
  --navy:     #071428;
  --wa:       #25d366;
  --mono:     'Share Tech Mono', monospace;
  /* Three.js */
  --3js-core-color: 0x061530;
  --3js-wire-color: 0x00ffc8;
  --3js-ring-color: 0x0084ff;
  --3js-light1: 0x00ffc8;
  --3js-light2: 0x0055ff;
  --3js-geometry: OctahedronGeometry(2, 0);
}
```

---

### `construction-orange` — שיפוצים, בנייה, אלומיניום, מסגרות
**תחושה**: חזק, אמין, עובד

```css
:root {
  --bg:       #0a0904;
  --bg2:      #120f05;
  --bg3:      #1a1507;
  --glass:    rgba(18,15,5,0.85);
  --border:   rgba(240,120,20,0.18);
  --border-g: rgba(240,120,20,0.25);
  --accent1:  #f97316;   /* vibrant orange */
  --accent1-l:#fb9a4b;
  --accent1-dim: rgba(249,115,22,0.12);
  --accent2:  #eab308;   /* yellow-gold */
  --accent2-dim: rgba(234,179,8,0.12);
  --txt:      #e8d5b0;
  --txt-dim:  rgba(232,213,176,0.55);
  --navy:     #1f1a0a;
  --wa:       #25d366;
  --mono:     'Share Tech Mono', monospace;
  /* Three.js */
  --3js-core-color: 0x2a1a00;
  --3js-wire-color: 0xf97316;
  --3js-ring-color: 0xeab308;
  --3js-light1: 0xff8800;
  --3js-light2: 0xeab308;
  --3js-geometry: BoxGeometry(2.2, 2.2, 2.2);
}
```

---

### `health-teal` — רפואה, פיזיותרפיה, ספא
**תחושה**: נקי, מרגיע, מקצועי

```css
:root {
  --bg:       #030f12;
  --bg2:      #04141a;
  --bg3:      #051a20;
  --glass:    rgba(4,20,26,0.85);
  --border:   rgba(0,200,200,0.14);
  --border-g: rgba(0,200,180,0.20);
  --accent1:  #06b6d4;   /* cyan-teal */
  --accent1-l:#67e8f9;
  --accent1-dim: rgba(6,182,212,0.12);
  --accent2:  #10b981;   /* emerald */
  --accent2-dim: rgba(16,185,129,0.12);
  --txt:      #c0e8ee;
  --txt-dim:  rgba(192,232,238,0.55);
  --navy:     #062028;
  --wa:       #25d366;
  --mono:     'Share Tech Mono', monospace;
  /* Three.js */
  --3js-core-color: 0x043040;
  --3js-wire-color: 0x06b6d4;
  --3js-ring-color: 0x10b981;
  --3js-light1: 0x00ccdd;
  --3js-light2: 0x00bb88;
  --3js-geometry: SphereGeometry(2, 32, 32);
}
```

---

### `beauty-purple` — קוסמטיקה, עיצוב שיער, אסתטיקה
**תחושה**: יוקרה, נשיות, פרמיום

```css
:root {
  --bg:       #0a0412;
  --bg2:      #100618;
  --bg3:      #160920;
  --glass:    rgba(16,6,24,0.88);
  --border:   rgba(180,80,255,0.14);
  --border-g: rgba(240,160,80,0.20);
  --accent1:  #c084fc;   /* lavender purple */
  --accent1-l:#e9d5ff;
  --accent1-dim: rgba(192,132,252,0.12);
  --accent2:  #f59e0b;   /* warm gold */
  --accent2-dim: rgba(245,158,11,0.12);
  --txt:      #e8d5f5;
  --txt-dim:  rgba(232,213,245,0.55);
  --navy:     #1a0a28;
  --wa:       #25d366;
  --mono:     'Share Tech Mono', monospace;
  /* Three.js */
  --3js-core-color: 0x200840;
  --3js-wire-color: 0xc084fc;
  --3js-ring-color: 0xf59e0b;
  --3js-light1: 0xcc66ff;
  --3js-light2: 0xf59e0b;
  --3js-geometry: IcosahedronGeometry(1.8, 1);
}
```

---

### `food-warm` — מסעדה, קייטרינג, בייקרי
**תחושה**: חם, מוזמן, תיאבון

```css
:root {
  --bg:       #0f0805;
  --bg2:      #160c07;
  --bg3:      #1e1008;
  --glass:    rgba(22,12,7,0.88);
  --border:   rgba(220,80,40,0.16);
  --border-g: rgba(240,160,40,0.22);
  --accent1:  #ef4444;   /* warm red */
  --accent1-l:#f87171;
  --accent1-dim: rgba(239,68,68,0.12);
  --accent2:  #f59e0b;   /* amber */
  --accent2-dim: rgba(245,158,11,0.12);
  --txt:      #f5d5b8;
  --txt-dim:  rgba(245,213,184,0.55);
  --navy:     #28100a;
  --wa:       #25d366;
  --mono:     'Share Tech Mono', monospace;
  /* Three.js */
  --3js-core-color: 0x3a1008;
  --3js-wire-color: 0xef4444;
  --3js-ring-color: 0xf59e0b;
  --3js-light1: 0xff5522;
  --3js-light2: 0xf59e0b;
  --3js-geometry: TorusKnotGeometry(1.5, 0.4, 64, 16);
}
```

---

### `legal-midnight` — עורך דין, רואה חשבון, יועץ עסקי, ביטוח
**תחושה**: סמכותי, אמין, יוקרתי

```css
:root {
  --bg:       #050810;
  --bg2:      #070c18;
  --bg3:      #091020;
  --glass:    rgba(7,12,24,0.90);
  --border:   rgba(100,150,220,0.12);
  --border-g: rgba(180,150,80,0.20);
  --accent1:  #c9a84c;   /* classic gold */
  --accent1-l:#e8c97a;
  --accent1-dim: rgba(201,168,76,0.12);
  --accent2:  #4a7fc1;   /* steel blue */
  --accent2-dim: rgba(74,127,193,0.12);
  --txt:      #d0d8f0;
  --txt-dim:  rgba(208,216,240,0.55);
  --navy:     #0c1428;
  --wa:       #25d366;
  --mono:     'Share Tech Mono', monospace;
  /* Three.js */
  --3js-core-color: 0x0c1a40;
  --3js-wire-color: 0x4a7fc1;
  --3js-ring-color: 0xc9a84c;
  --3js-light1: 0x4488ff;
  --3js-light2: 0xc9a84c;
  --3js-geometry: OctahedronGeometry(2, 0);
}
```

---

### `realestate-gold` — נדל"ן, קבלנים, בנייה יוקרתית
**תחושה**: יוקרה, ערך, השקעה

```css
:root {
  --bg:       #080600;
  --bg2:      #0f0c02;
  --bg3:      #161205;
  --glass:    rgba(15,12,2,0.90);
  --border:   rgba(200,165,60,0.16);
  --border-g: rgba(200,165,60,0.28);
  --accent1:  #d4a520;   /* deep gold */
  --accent1-l:#f0c84c;
  --accent1-dim: rgba(212,165,32,0.12);
  --accent2:  #9a8060;   /* warm bronze */
  --accent2-dim: rgba(154,128,96,0.15);
  --txt:      #f0ddb0;
  --txt-dim:  rgba(240,221,176,0.55);
  --navy:     #201800;
  --wa:       #25d366;
  --mono:     'Share Tech Mono', monospace;
  /* Three.js */
  --3js-core-color: 0x201800;
  --3js-wire-color: 0xd4a520;
  --3js-ring-color: 0x9a8060;
  --3js-light1: 0xffcc22;
  --3js-light2: 0xaa8844;
  --3js-geometry: BoxGeometry(2.4, 2.4, 2.4);
}
```

---

### `classic-dark` — כללי, ברירת מחדל כשלא ברור
**תחושה**: מקצועי, נייטרלי, עובד לכל תחום

```css
:root {
  --bg:       #04090f;
  --bg2:      #060d18;
  --bg3:      #08111f;
  --glass:    rgba(8,17,32,0.80);
  --border:   rgba(100,160,220,0.12);
  --border-g: rgba(180,140,60,0.20);
  --accent1:  #f0b429;   /* gold */
  --accent1-l:#ffd060;
  --accent1-dim: rgba(240,180,41,0.12);
  --accent2:  #00aaff;   /* blue */
  --accent2-dim: rgba(0,170,255,0.12);
  --txt:      #c8d8f0;
  --txt-dim:  rgba(200,216,240,0.50);
  --navy:     #0a1628;
  --wa:       #25d366;
  --mono:     'Share Tech Mono', monospace;
  /* Three.js */
  --3js-core-color: 0x0a1f5e;
  --3js-wire-color: 0x00aaff;
  --3js-ring-color: 0xf0b429;
  --3js-light1: 0x00b4ff;
  --3js-light2: 0xf0b429;
  --3js-geometry: IcosahedronGeometry(1.8, 0);
}
```

---

## פלטה מותאמת אישית (כשיש צבעי מותג)

אם ללקוח יש צבעי מותג — בנה פלטה על בסיסם:

```css
:root {
  /* קח את הצבע הראשי של המותג ועדן אותו לרקע כהה */
  --bg:       /* גרסה כהה מאוד של הצבע הראשי (10-15% בהירות) */;
  --bg2:      /* קצת יותר בהיר */;
  --bg3:      /* קצת יותר בהיר עוד */;
  --accent1:  /* הצבע הראשי של המותג */;
  --accent1-l:/* גרסה בהירה שלו */;
  --accent1-dim: /* גרסה שקופה שלו (rgba) */;
  --accent2:  /* צבע משלים (complementary) */;
  --accent2-dim: /* גרסה שקופה שלו */;
  /* ...שאר המשתנים מ-classic-dark */
}
```

**כלל אצבע**: רקע כהה תמיד. גם אם הלקוח רוצה "בהיר" — שמור על רקע `#0X0X0X` כדי שה-3D ייראה טוב.

---

## שימוש ב-CSS Variables בקוד

ב-design-system.md תמצא את כל ה-CSS שמשתמש ב-variables האלה. החלף:
- `var(--cyan)` ← `var(--accent2)`
- `var(--gold)` ← `var(--accent1)`
- כל שאר המשתנים עובדים ישירות

## Three.js — שימוש בצבעי הפלטה

```javascript
// ב-Three.js, השתמש בערכים HEX מהפלטה שנבחרה:
const coreMat = new THREE.MeshPhongMaterial({
  color: [--3js-core-color],    // e.g. 0x0a1f5e
  emissive: 0x001133,
});
const wireMat = new THREE.MeshBasicMaterial({ color: [--3js-wire-color] }); // e.g. 0x00aaff
const ringMat = new THREE.MeshBasicMaterial({ color: [--3js-ring-color] }); // e.g. 0xf0b429
const blueLight = new THREE.PointLight([--3js-light1], 2, 15); // e.g. 0x00b4ff
const goldLight = new THREE.PointLight([--3js-light2], 1.5, 15); // e.g. 0xf0b429
```

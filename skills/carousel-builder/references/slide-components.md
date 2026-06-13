# רכיבי שקופית מוכנים

העתק את הרכיב הרלוונטי לתוך `.inner` של השקופית. כולם RTL, ממותגים, ובגדלים קריאים בתמונה.
המבנה הבסיסי של כל שקופית:
```html
<section class="slide" id="sN">
  <div class="bg-glow"></div><div class="bg-grid"></div>
  <div class="kicker"><span class="dot"></span><span class="nm">RON DIGITAL</span></div>
  <div class="pageno">0N / 10</div>
  <div class="inner [סוג]"> ... רכיב ... </div>
  <div class="swipe">החלק להמשך <b>←</b></div>
</section>
```

## 1. Hook (שקופית פתיחה)
מטרה: לעצור גלילה. שאלה/כאב חד + מילה אחת מודגשת באמבר.
```html
<div class="inner cv">
  <div class="eyebrow">לקהל היעד שלך</div>
  <h1>כותרת עם מילה <span class="a">מודגשת</span></h1>
  <div class="sub">משפט הסבר קצר שממסגר את הכאב.</div>
  <div class="scatter">
    <span class="chip">📊 אקסל</span><span class="chip">💬 וואטסאפ</span>
  </div>
</div>
```
```css
.cv{justify-content:center;gap:34px}
.cv .eyebrow{font-size:34px;font-weight:400;color:var(--amber);letter-spacing:.05em}
.cv h1{font-size:104px;font-weight:900;color:var(--white);line-height:1.04}
.cv h1 .a{color:var(--amber)}
.cv .sub{font-size:40px;font-weight:400;color:var(--mut);line-height:1.4;max-width:840px}
.chip{background:rgba(255,255,255,.05);border:1px solid var(--line);border-radius:100px;
  padding:13px 26px;font-size:28px;font-weight:500;color:rgba(255,255,255,.7)}
.scatter{display:flex;flex-wrap:wrap;gap:16px;margin-top:14px}
```

## 2. Pain (כרטיסי כאב)
```html
<div class="inner pain">
  <h2>המצב היום <span class="x">עולה לך כסף</span></h2>
  <div class="pcard"><div class="i">⏰</div><div class="t">שעות מבוזבזות</div></div>
  <div class="pcard"><div class="i">❌</div><div class="t">טעויות תמחור</div></div>
</div>
```
```css
.pain{justify-content:center;gap:30px}
.pain h2{font-size:64px;font-weight:800;color:var(--white);margin-bottom:14px}
.pain h2 .x{color:var(--red)}
.pcard{display:flex;align-items:center;gap:28px;background:rgba(255,90,90,.05);
  border:1px solid rgba(255,90,90,.18);border-radius:24px;padding:30px 34px}
.pcard .i{width:78px;height:78px;border-radius:18px;flex-shrink:0;font-size:40px;
  background:rgba(255,90,90,.10);display:flex;align-items:center;justify-content:center}
.pcard .t{font-size:46px;font-weight:600;color:rgba(255,255,255,.88);flex:1}
```

## 3. Solution (הפתרון)
```html
<div class="inner sol">
  <div class="pre">הצגת הפתרון</div>
  <h2>הכל במקום <span class="a">אחד</span></h2>
  <div class="devices">
    <div class="dev"><div class="ic">💻</div><div class="lb">מהמשרד</div></div>
    <div class="sync">⇄</div>
    <div class="dev"><div class="ic">📱</div><div class="lb">מהשטח</div></div>
  </div>
  <div class="note">משפט הסבר על הערך המרכזי</div>
</div>
```
```css
.sol{justify-content:center;align-items:center;gap:30px;text-align:center}
.sol .pre{font-size:38px;font-weight:300;color:var(--mut)}
.sol h2{font-size:96px;font-weight:900;color:var(--white);line-height:1.05}
.sol h2 .a{color:var(--amber)}
.devices{display:flex;align-items:center;gap:50px;margin-top:30px}
.dev{display:flex;flex-direction:column;align-items:center;gap:18px}
.dev .ic{font-size:130px}
.dev .lb{font-size:34px;font-weight:600;color:rgba(255,255,255,.8)}
.sync{font-size:60px;color:var(--amber)}
.sol .note{font-size:38px;font-weight:400;color:var(--mut);margin-top:18px}
```

## 4. Feature + Phone Mockup
שקופית פיצ'ר עם כותרת למעלה ומסך טלפון מדומה. ה-phone mockup נאמן לסגנון אפליקציה.
```html
<div class="inner feat">
  <div class="fhead">
    <div class="fstep">⚙️ תווית</div>
    <h2>שם הפיצ'ר</h2>
    <div class="desc">משפט הסבר.</div>
  </div>
  <div class="fbody">
    <div class="phone">
      <div class="pnotch"></div>
      <div class="pbar"><div class="pbrand">המערכת שלי</div><div class="pscreen">📋 שם מסך</div></div>
      <div class="pbody"> ... תוכן המסך (רשימה/טבלה/כרטיסים) ... </div>
    </div>
  </div>
</div>
```
```css
.feat{padding-top:150px}
.fhead{margin-bottom:44px}
.fstep{display:inline-block;background:rgba(255,179,0,.12);border:1px solid rgba(255,179,0,.3);
  border-radius:100px;padding:10px 26px;font-size:28px;font-weight:600;color:var(--amber);margin-bottom:20px}
.fhead h2{font-size:72px;font-weight:800;color:var(--white);line-height:1.08}
.fhead .desc{font-size:38px;font-weight:400;color:var(--mut);margin-top:14px;max-width:880px}
.fbody{flex:1;display:flex;align-items:flex-start;justify-content:center}
.phone{width:560px;background:var(--bg2);border-radius:56px;border:2px solid rgba(255,179,0,.28);
  overflow:hidden;box-shadow:0 40px 100px rgba(0,0,0,.5),0 0 70px rgba(255,179,0,.06)}
.pnotch{height:42px;background:#081522;display:flex;align-items:center;justify-content:center}
.pnotch::after{content:'';width:140px;height:30px;background:var(--bg);border-radius:0 0 20px 20px}
.pbar{background:linear-gradient(135deg,var(--bg),var(--bg2));padding:22px 26px 18px;
  border-bottom:1px solid rgba(255,179,0,.12)}
.pbrand{font-size:16px;color:var(--amber);letter-spacing:.06em;margin-bottom:4px}
.pscreen{font-size:30px;font-weight:700;color:var(--white)}
.pbody{padding:22px}
```
רכיבי תוכן למסך (שורת רשימה / כפתור CTA פנימי):
```css
.row{display:flex;justify-content:space-between;align-items:center;padding:16px 18px;
  border-radius:14px;background:rgba(255,255,255,.04);border:1px solid var(--line);margin-bottom:9px}
.row .name{font-size:23px;font-weight:500;color:rgba(255,255,255,.9)}
.row .val{font-size:25px;font-weight:700;color:var(--amber);direction:ltr}
.inbtn{display:block;width:100%;background:var(--amber);color:var(--bg);font-family:'Heebo';
  font-size:24px;font-weight:700;text-align:center;padding:18px;border-radius:15px;margin-top:14px;border:none}
```

## 5. Stats / Report (סטטיסטיקות)
```html
<div class="statrow">
  <div class="stat"><div class="v green"><bdi>₪42K</bdi></div><div class="k">נכנס החודש</div></div>
  <div class="stat"><div class="v"><bdi>68%</bdi></div><div class="k">אחוז סגירה</div></div>
</div>
```
```css
.statrow{display:flex;gap:16px;margin-bottom:18px}
.stat{flex:1;background:rgba(255,255,255,.04);border:1px solid var(--line);border-radius:18px;
  padding:22px 20px;text-align:center}
.stat .v{font-size:46px;font-weight:900;color:var(--amber);direction:ltr;line-height:1}
.stat .v.green{color:var(--green)}
.stat .k{font-size:19px;color:var(--mut);margin-top:8px}
```

## 6. CTA (שקופית אחרונה — בלי swipe hint)
```html
<div class="inner cta">
  <div class="q">שאלה שמובילה לפעולה?</div>
  <h2>קריאה<br><span>לפעולה</span></h2>
  <button class="btn">כפתור פעולה 📩</button>
  <div class="div"></div>
  <div class="contact"><span>📱 <bdi dir="ltr">050-621-7775</bdi></span></div>
  <div class="brand">RON DIGITAL STUDIO</div>
</div>
```
```css
.cta{justify-content:center;align-items:center;gap:40px;text-align:center}
.cta .q{font-size:48px;font-weight:400;color:var(--mut)}
.cta h2{font-size:108px;font-weight:900;color:var(--white);line-height:1}
.cta h2 span{color:var(--amber)}
.cta .btn{background:var(--amber);color:var(--bg);font-family:'Heebo';font-size:46px;
  font-weight:900;padding:30px 84px;border-radius:100px;border:none;box-shadow:0 8px 44px rgba(255,179,0,.3)}
.cta .div{width:200px;height:1px;background:rgba(255,255,255,.14)}
.cta .contact{font-size:30px;color:rgba(255,255,255,.7);font-weight:500}
.cta .brand{font-size:32px;font-weight:300;color:var(--mut2);letter-spacing:.24em;text-transform:uppercase}
```

> תזכורת: עטוף כל מספר/מחיר/אחוז/תאריך/טלפון ב-`<bdi>`. אל תמציא טלפון/URL/שם אמיתי — שאל את המשתמש.

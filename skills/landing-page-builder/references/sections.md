# Sections Library — HTML + CSS לכל סקשן

---

## HEADER

```html
<header id="hdr">
  <div class="container">
    <div class="hdr-inner">
      <a href="#hero" class="logo">
        <div class="logo-icon">🔒</div>
        [שם] <span>[חלק שני]</span>
      </a>
      <nav id="main-nav">
        <a href="#services">שירותים</a>
        <a href="#why-us">יתרונות</a>
        <a href="#testimonials">המלצות</a>
        <a href="#faq">שאלות</a>
        <a href="#contact">צור קשר</a>
      </nav>
      <a href="tel:[PHONE_NOHYPHENS]" class="btn btn-gold hdr-cta">
        <i class="fas fa-phone"></i> [PHONE]
      </a>
      <div class="burger" id="burger"><span></span><span></span><span></span></div>
    </div>
  </div>
</header>
```

```css
#hdr { position:sticky; top:0; z-index:100; padding:.75rem 0; transition:background .3s,box-shadow .3s; }
#hdr.sc { background:rgba(4,9,15,.95); backdrop-filter:blur(12px); box-shadow:0 2px 20px rgba(0,0,0,.5); }
.hdr-inner { display:flex; align-items:center; gap:1.5rem; }
.logo { display:flex; align-items:center; gap:.5rem; font-size:1.2rem; font-weight:900; color:#fff; text-decoration:none; margin-right:auto; }
.logo span { color:var(--gold); }
#main-nav { display:flex; gap:1.5rem; }
#main-nav a { color:var(--txt); font-size:.9rem; text-decoration:none; transition:color .2s; }
#main-nav a:hover { color:var(--gold); }
.burger { display:none; flex-direction:column; gap:5px; cursor:pointer; }
.burger span { display:block; width:24px; height:2px; background:#fff; border-radius:2px; transition:.3s; }
@media(max-width:768px) { #main-nav { display:none; position:absolute; top:100%; right:0; left:0; background:rgba(4,9,15,.97); padding:1rem; flex-direction:column; } #main-nav.open { display:flex; } .burger { display:flex; } }
```

---

## COUNTERS

```html
<section id="counters">
  <div class="container">
    <div class="cnt-grid">
      <div class="cnt-item reveal d1">
        <div class="cnt-icon"><i class="fas fa-calendar-check"></i></div>
        <div class="cnt-num" data-to="15">0</div>
        <div class="cnt-lbl">שנות ניסיון</div>
      </div>
      <div class="cnt-item reveal d2">
        <div class="cnt-icon"><i class="fas fa-bolt"></i></div>
        <div class="cnt-num">⚡</div>
        <div class="cnt-lbl">שירות מהיר</div>
      </div>
      <div class="cnt-item reveal d3">
        <div class="cnt-icon"><i class="fas fa-medal"></i></div>
        <div class="cnt-num" data-to="3">0</div>
        <div class="cnt-lbl">שנות אחריות</div>
      </div>
      <div class="cnt-item reveal d4">
        <div class="cnt-icon"><i class="fas fa-headset"></i></div>
        <div class="cnt-num">24/7</div>
        <div class="cnt-lbl">זמינות גבוהה</div>
      </div>
    </div>
  </div>
</section>
```

```css
.cnt-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:1.5rem; }
@media(max-width:640px) { .cnt-grid { grid-template-columns:repeat(2,1fr); } }
.cnt-item { text-align:center; padding:1.5rem; }
.cnt-icon { font-size:1.8rem; color:var(--gold); margin-bottom:.5rem; }
.cnt-num { font-size:2.8rem; font-weight:900; color:#fff; font-family:var(--mono); text-shadow:0 2px 0 rgba(0,170,255,.3),0 8px 20px rgba(0,0,0,.5); }
.cnt-lbl { color:var(--txt-dim); font-size:.9rem; margin-top:.3rem; }
```

```javascript
// Counter animation
document.querySelectorAll('.cnt-num[data-to]').forEach(el => {
  const target = +el.dataset.to;
  const obs = new IntersectionObserver(([e]) => {
    if (!e.isIntersecting) return; obs.disconnect();
    let n = 0, step = Math.ceil(target/60);
    const t = setInterval(() => { n = Math.min(n+step, target); el.textContent = n+'+'; if(n>=target) clearInterval(t); }, 30);
  });
  obs.observe(el);
});
```

---

## WHY US

```html
<section id="why-us" class="sec">
  <div class="container">
    <h2 class="ttl reveal">למה <span>לבחור בנו?</span></h2>
    <p class="sub-ttl reveal">שלושה עקרונות שמנחים אותנו בכל פרויקט</p>
    <div class="why-grid">
      <div class="why-card reveal">
        <div class="why-icon">⚡</div>
        <h3>[כותרת]</h3>
        <p>[תיאור]</p>
      </div>
      <!-- × 3 -->
    </div>
  </div>
</section>
```

```css
.why-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:1.5rem; }
@media(max-width:768px) { .why-grid { grid-template-columns:1fr; } }
.why-card { background:var(--glass); border:1px solid var(--border); border-radius:16px; padding:2rem; text-align:center; transition:transform .3s,box-shadow .3s; }
.why-card:hover { transform:perspective(1000px) rotateX(-8deg) translateY(-10px) translateZ(20px); box-shadow:0 20px 50px rgba(0,0,0,.5),0 0 30px rgba(0,170,255,.1); }
.why-icon { font-size:2.5rem; margin-bottom:1rem; }
.why-card h3 { font-size:1.1rem; color:#fff; margin-bottom:.5rem; }
.why-card p { color:var(--txt-dim); font-size:.9rem; line-height:1.6; }
```

---

## WE BRING (checklist)

```html
<section id="we-bring" class="sec">
  <div class="container">
    <h2 class="ttl reveal">מה אנחנו <span>מביאים</span> לכל פרויקט?</h2>
    <p class="sub-ttl reveal">שירות שלם מהתחלה ועד הסוף</p>
    <div class="bring-grid">
      <div class="bring-item reveal">
        <div class="bring-check"><i class="fas fa-check"></i></div>
        <div>
          <h4>[כותרת]</h4>
          <p>[תיאור]</p>
        </div>
      </div>
      <!-- × 6 -->
    </div>
  </div>
</section>
```

```css
.bring-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; }
@media(max-width:768px) { .bring-grid { grid-template-columns:1fr; } }
.bring-item { display:flex; gap:1rem; align-items:flex-start; background:var(--glass); border:1px solid var(--border); border-radius:12px; padding:1.25rem; }
.bring-check { width:28px; height:28px; border-radius:50%; background:var(--cyan-dim); border:1px solid var(--cyan); display:flex; align-items:center; justify-content:center; color:var(--cyan); font-size:.75rem; flex-shrink:0; }
.bring-item h4 { font-size:.95rem; color:#fff; margin-bottom:.25rem; }
.bring-item p { font-size:.82rem; color:var(--txt-dim); line-height:1.5; }
```

---

## VALUE TABLE

```html
<section id="value-table" class="sec">
  <div class="container" style="max-width:600px">
    <h2 class="ttl reveal">מה בדיוק <span>אתם מקבלים?</span></h2>
    <p class="sub-ttl reveal">שקיפות מלאה — בלי הפתעות</p>
    <div class="val-card reveal">
      <div class="val-header">
        <h3>חבילת ה-All-in שלנו</h3>
        <p>מה כלול בכל פרויקט</p>
      </div>
      <div class="val-row"><span>ייעוץ והגעה לבית/עסק</span><span class="badge-free">₪0</span></div>
      <div class="val-row"><span>תכנון אישי לפי צרכים</span><span class="badge-inc">כלול</span></div>
      <div class="val-row"><span>ציוד פרימיום</span><span class="badge-inc">כלול</span></div>
      <div class="val-row"><span>התקנה מקצועית</span><span class="badge-inc">כלול</span></div>
      <div class="val-row"><span>גישה למערכת ניהול</span><span class="badge-inc">כלול</span></div>
      <div class="val-row"><span>תמיכה מרחוק וליווי</span><span class="badge-inc">כלול</span></div>
      <div class="val-row"><span>אחריות 3 שנים</span><span class="badge-inc">כלול</span></div>
      <a href="#contact" class="btn btn-gold" style="margin:1.5rem auto 0;display:block;text-align:center;max-width:280px">לייעוץ חינם עכשיו</a>
    </div>
  </div>
</section>
```

```css
.val-card { background:var(--glass); border:1px solid var(--border-g); border-radius:20px; overflow:hidden; }
.val-header { padding:1.5rem; border-bottom:1px solid var(--border-g); background:var(--gold-dim); }
.val-header h3 { color:var(--gold); font-size:1.2rem; }
.val-header p { color:var(--txt-dim); font-size:.85rem; }
.val-row { display:flex; justify-content:space-between; align-items:center; padding:.85rem 1.5rem; border-bottom:1px solid rgba(255,255,255,.04); }
.val-row span:first-child { color:var(--txt); font-size:.9rem; }
.badge-free { background:rgba(0,255,136,.12); color:#00ff88; border:1px solid rgba(0,255,136,.3); padding:.2rem .6rem; border-radius:20px; font-size:.78rem; font-weight:700; }
.badge-inc { background:var(--gold-dim); color:var(--gold); border:1px solid var(--border-g); padding:.2rem .6rem; border-radius:20px; font-size:.78rem; font-weight:700; }
```

---

## TESTIMONIALS

```html
<section id="testimonials" class="sec">
  <div class="container">
    <h2 class="ttl reveal">מה <span>הלקוחות</span> אומרים</h2>
    <p class="sub-ttl reveal">חוויות אמיתיות מלקוחות מרוצים</p>
    <div class="test-grid">
      <div class="test-card reveal d1">
        <div class="test-quote">"</div>
        <div class="test-stars">★★★★★</div>
        <blockquote>"[ציטוט]"</blockquote>
        <div class="test-author">
          <div class="test-avatar">[ר]</div>
          <div><div class="test-name">[שם]</div><div class="test-loc">[מיקום]</div></div>
        </div>
      </div>
      <!-- × 3 -->
    </div>
  </div>
</section>
```

```css
.test-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:1.5rem; }
@media(max-width:900px) { .test-grid { grid-template-columns:1fr; } }
.test-card { background:var(--glass); border:1px solid var(--border); border-radius:16px; padding:1.5rem; position:relative; }
.test-quote { position:absolute; top:.5rem; right:1rem; font-size:4rem; color:var(--gold); opacity:.2; font-family:serif; line-height:1; }
.test-stars { color:var(--gold); font-size:1rem; margin-bottom:1rem; }
.test-card blockquote { color:var(--txt); font-size:.9rem; line-height:1.7; font-style:italic; margin-bottom:1rem; }
.test-author { display:flex; align-items:center; gap:.75rem; }
.test-avatar { width:38px; height:38px; border-radius:50%; background:linear-gradient(135deg,var(--cyan),var(--gold)); display:flex; align-items:center; justify-content:center; font-weight:700; color:#000; }
.test-name { font-weight:700; color:#fff; font-size:.9rem; }
.test-loc { color:var(--txt-dim); font-size:.8rem; }
```

---

## FAQ (accordion)

```html
<section id="faq" class="sec">
  <div class="container" style="max-width:700px">
    <h2 class="ttl reveal">שאלות <span>נפוצות</span></h2>
    <p class="sub-ttl reveal">תשובות לשאלות שכולם שואלים</p>
    <div class="faq-list">
      <div class="faq-item">
        <div class="faq-q"><span>[שאלה]</span><i class="fas fa-chevron-down"></i></div>
        <div class="faq-a"><p>[תשובה]</p></div>
      </div>
      <!-- × 4 -->
    </div>
  </div>
</section>
```

```css
.faq-item { border:1px solid var(--border); border-radius:10px; margin-bottom:.75rem; overflow:hidden; }
.faq-q { display:flex; justify-content:space-between; align-items:center; padding:1rem 1.25rem; cursor:pointer; color:#fff; font-weight:600; }
.faq-q i { color:var(--gold); transition:transform .3s; }
.faq-item.open .faq-q i { transform:rotate(180deg); }
.faq-a { max-height:0; overflow:hidden; transition:max-height .35s ease; }
.faq-item.open .faq-a { max-height:200px; }
.faq-a p { padding:.75rem 1.25rem 1rem; color:var(--txt-dim); font-size:.9rem; line-height:1.7; }
```

```javascript
document.querySelectorAll('.faq-q').forEach(q => {
  q.addEventListener('click', () => {
    const item = q.parentElement;
    document.querySelectorAll('.faq-item.open').forEach(o => { if(o!==item) o.classList.remove('open'); });
    item.classList.toggle('open');
  });
});
```

---

## CONTACT

```html
<section id="contact" class="sec">
  <div class="container">
    <h2 class="ttl reveal">בואו <span>נדבר</span></h2>
    <p class="sub-ttl reveal">השאירו פרטים ונחזור — ייעוץ ראשוני חינם</p>
    <div class="contact-grid">
      <div class="contact-info reveal">
        <h3>פרטי יצירת קשר</h3>
        <div class="cinfo-item"><i class="fas fa-phone"></i><div><div>טלפון</div><a href="tel:[PHONE]">[PHONE_DISPLAY]</a></div></div>
        <div class="cinfo-item"><i class="fab fa-whatsapp"></i><div><div>WhatsApp</div><a href="https://wa.me/972[WA]" target="_blank">שלח הודעה עכשיו</a></div></div>
        <div class="cinfo-item"><i class="fas fa-envelope"></i><div><div>אימייל</div><a href="mailto:[EMAIL]">[EMAIL]</a></div></div>
      </div>
      <div class="contact-form reveal">
        <h3>השאירו הודעה</h3>
        <form onsubmit="handleForm(event)">
          <div class="form-group"><label>שם מלא</label><input type="text" placeholder="הכנס שם..." required></div>
          <div class="form-group"><label>מספר טלפון</label><input type="tel" placeholder="05X-XXXXXXX" required></div>
          <div class="form-group"><label>הודעה</label><textarea placeholder="ספר לנו על הפרויקט שלך..." rows="3"></textarea></div>
          <button type="submit" class="btn btn-gold" style="width:100%"><i class="fas fa-paper-plane"></i> שלח ואחזור אליך בהקדם</button>
        </form>
      </div>
    </div>
  </div>
</section>
```

```css
.contact-grid { display:grid; grid-template-columns:1fr 1.5fr; gap:2rem; }
@media(max-width:768px) { .contact-grid { grid-template-columns:1fr; } }
.contact-info, .contact-form { background:var(--glass); border:1px solid var(--border); border-radius:16px; padding:1.75rem; }
.contact-info h3, .contact-form h3 { color:var(--gold); margin-bottom:1.25rem; }
.cinfo-item { display:flex; align-items:center; gap:1rem; margin-bottom:1rem; }
.cinfo-item i { width:38px; height:38px; border-radius:50%; background:var(--cyan-dim); display:flex; align-items:center; justify-content:center; color:var(--cyan); flex-shrink:0; }
.cinfo-item a { color:var(--cyan); text-decoration:none; font-weight:600; }
.form-group { margin-bottom:1rem; }
.form-group label { display:block; color:var(--txt-dim); font-size:.85rem; margin-bottom:.35rem; }
.form-group input, .form-group textarea { width:100%; background:rgba(0,0,0,.3); border:1px solid var(--border); border-radius:8px; padding:.65rem 1rem; color:#fff; font-family:Heebo,sans-serif; font-size:.9rem; }
```

```javascript
function handleForm(e) {
  e.preventDefault();
  const btn = e.target.querySelector('button[type=submit]');
  btn.textContent = '✓ ההודעה נשלחה! נחזור אליך בקרוב';
  btn.style.background = 'var(--green)';
  btn.style.color = '#000';
  setTimeout(() => { btn.innerHTML = '<i class="fas fa-paper-plane"></i> שלח ואחזור אליך בהקדם'; btn.style = ''; e.target.reset(); }, 4000);
}
```

---

## FOOTER + WhatsApp float

```html
<footer>
  <div class="container">
    <div class="footer-inner">
      <div class="footer-logo">[לוגו] [שם]</div>
      <div class="footer-links">
        <a href="#services">שירותים</a>
        <a href="#about">אודות</a>
        <a href="#faq">שאלות</a>
        <a href="#contact">צור קשר</a>
      </div>
    </div>
    <div class="footer-copy">© 2025 [שם]. כל הזכויות שמורות.</div>
  </div>
</footer>

<!-- WhatsApp צף -->
<a href="https://wa.me/972[WA]" target="_blank" class="wa-float" aria-label="WhatsApp">
  <i class="fab fa-whatsapp"></i>
</a>
```

```css
footer { background:var(--navy); padding:2rem 0 1rem; }
.footer-inner { display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem; padding-bottom:1rem; border-bottom:1px solid var(--border); margin-bottom:1rem; }
.footer-logo { font-size:1.1rem; font-weight:800; color:#fff; }
.footer-links { display:flex; gap:1.5rem; }
.footer-links a { color:var(--txt-dim); font-size:.85rem; text-decoration:none; }
.footer-links a:hover { color:var(--gold); }
.footer-copy { text-align:center; color:var(--txt-dim); font-size:.8rem; }

.wa-float { position:fixed; bottom:1.5rem; right:1.5rem; width:54px; height:54px; border-radius:50%; background:var(--wa); display:flex; align-items:center; justify-content:center; color:#fff; font-size:1.5rem; z-index:999; box-shadow:0 4px 20px rgba(37,211,102,.4); animation:wa-pulse 2s infinite; }
```

# WhatsApp Integration — חיבור הטופס לוואטסאפ

שתי שיטות. בחר לפי המצב:

---

## שיטה 1 — Click-to-Chat (ללא API — מומלץ לרוב הלקוחות)

הטופס שולח את הפנייה ישר לוואטסאפ של הלקוח כהודעה מוכנה.
הגולש לוחץ "שלח" → נפתח וואטסאפ → הוא מאשר ושולח → הודעה מגיעה ללקוח.

**יתרון**: אפס הגדרות, עובד מיד, ללא עלות.
**חיסרון**: הגולש צריך לאשר ידנית בוואטסאפ (שלב אחד נוסף).

```javascript
function handleForm(e) {
  e.preventDefault();
  const form = e.target;
  const name = form.querySelector('input[type=text]').value.trim();
  const phone = form.querySelector('input[type=tel]').value.trim();
  const msg = form.querySelector('textarea').value.trim();

  // בנה הודעת וואטסאפ
  const waText = encodeURIComponent(
    `שלום! פנייה חדשה מדף הנחיתה:\n\n` +
    `👤 שם: ${name}\n` +
    `📞 טלפון: ${phone}\n` +
    `💬 הודעה: ${msg || '—'}\n\n` +
    `(נשלח מ: ${window.location.hostname})`
  );

  // מספר וואטסאפ של הלקוח העסקי (ללא מקפים, עם 972)
  const waNumber = '972[PHONE_WITHOUT_HYPHENS]'; // ← החלף
  const waUrl = `https://wa.me/${waNumber}?text=${waText}`;

  // פתח וואטסאפ בטאב חדש
  window.open(waUrl, '_blank');

  // אנימציית הצלחה בכפתור
  const btn = form.querySelector('button[type=submit]');
  const original = btn.innerHTML;
  btn.innerHTML = '<i class="fab fa-whatsapp"></i> מעביר לוואטסאפ...';
  btn.style.background = 'var(--wa)';
  btn.style.color = '#000';
  setTimeout(() => { btn.innerHTML = original; btn.style = ''; form.reset(); }, 4000);
}
```

---

## שיטה 2 — Make.com Webhook (אוטומציה מלאה)

הטופס שולח JSON ל-Webhook ב-Make.com → Make שולח הודעה לוואטסאפ Business.
הגולש לוחץ "שלח" → הודעה מגיעה ללקוח אוטומטית.

**יתרון**: הגולש לא צריך לעשות כלום. פנייה מגיעה אוטומטית.
**דרישות**: חשבון Make.com + חיבור וואטסאפ Business פעיל.

### שלב א — JS בדף

```javascript
async function handleForm(e) {
  e.preventDefault();
  const form = e.target;
  const btn = form.querySelector('button[type=submit]');
  const name = form.querySelector('input[type=text]').value.trim();
  const phone = form.querySelector('input[type=tel]').value.trim();
  const msg = form.querySelector('textarea').value.trim();

  btn.disabled = true;
  btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> שולח...';

  try {
    // ← החלף את ה-URL בכתובת ה-Webhook שלך מ-Make
    const WEBHOOK_URL = 'https://hook.eu2.make.com/[YOUR_WEBHOOK_ID]';

    await fetch(WEBHOOK_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name,
        phone,
        message: msg,
        source: window.location.hostname,
        timestamp: new Date().toISOString()
      })
    });

    btn.innerHTML = '✓ ההודעה נשלחה! נחזור אליך בקרוב';
    btn.style.background = 'var(--green)';
    btn.style.color = '#000';
    form.reset();
    setTimeout(() => { btn.innerHTML = '<i class="fas fa-paper-plane"></i> שלח ואחזור אליך בהקדם'; btn.style = ''; btn.disabled = false; }, 5000);

  } catch (err) {
    // fallback — אם ה-webhook נכשל, פתח וואטסאפ רגיל
    const waText = encodeURIComponent(`שם: ${name}\nטלפון: ${phone}\nהודעה: ${msg}`);
    window.open(`https://wa.me/972[PHONE]?text=${waText}`, '_blank');
    btn.innerHTML = 'שגיאה — הועברת לוואטסאפ';
    btn.disabled = false;
  }
}
```

### שלב ב — תרחיש Make.com

```
Trigger: Webhooks › Custom Webhook
    ↓ (body: name, phone, message, source, timestamp)
Module 1: WhatsApp Business Cloud › Send a Text Message
    To: [מספר הלקוח העסקי]
    Message: |
      📬 פנייה חדשה מדף הנחיתה!

      👤 שם: {{name}}
      📞 טלפון: {{phone}}
      💬 הודעה: {{message}}
      🌐 מקור: {{source}}
      🕐 שעה: {{timestamp}}
```

**Connection IDs הידועים (מ-CLAUDE.md)**:
- WhatsApp Business Cloud: `whatsapp-business-cloud@1`

---

## כפתור WhatsApp צף — תמיד בדף

הוסף לתחתית הדף (אחרי footer, לפני `</body>`):

```html
<a href="https://wa.me/972[PHONE]" target="_blank" rel="noopener"
   class="wa-float" aria-label="פתח שיחת WhatsApp">
  <i class="fab fa-whatsapp"></i>
</a>
```

```css
.wa-float {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem; /* RTL: right במקום left */
  width: 56px; height: 56px;
  border-radius: 50%;
  background: #25d366;
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 1.6rem;
  z-index: 999;
  box-shadow: 0 4px 20px rgba(37,211,102,.45);
  text-decoration: none;
  animation: wa-pulse 2.5s infinite;
}
@keyframes wa-pulse {
  0%,100% { box-shadow: 0 4px 20px rgba(37,211,102,.45), 0 0 0 0 rgba(37,211,102,.4); }
  50% { box-shadow: 0 4px 20px rgba(37,211,102,.45), 0 0 0 14px rgba(37,211,102,0); }
}
```

---

## בחירת שיטה לפי לקוח

| מצב | שיטה מומלצת |
|---|---|
| לקוח פשוט, מהיר, ללא Make | שיטה 1 (click-to-chat) |
| לקוח עם Make.com + WA Business | שיטה 2 (webhook) |
| לקוח שמכיר אותך מ-RON DIGITAL — יש Make | שיטה 2 |
| דף נחיתה בסיסי לבדיקה | שיטה 1 |

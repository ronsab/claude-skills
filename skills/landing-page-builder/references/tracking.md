# Tracking — Google Analytics + Meta Pixel

הכנס snippet אחד פעם אחת בכל דף. שאל את הלקוח אם יש לו ID לפני הכנסה.

---

## Google Analytics 4 (GA4)

```html
<!-- Google Analytics 4 — הכנס ב-<head> -->
<!-- אם אין ID: השאר את ה-placeholder ועדכן בעתיד -->
<!-- ID נראה כך: G-XXXXXXXXXX -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX'); // ← החלף ב-ID אמיתי
</script>
```

### אירועי המרה שכדאי לעקוב

```javascript
// הוסף לפונקציית handleForm אחרי שליחה מוצלחת:
gtag('event', 'lead_form_submit', {
  'event_category': 'lead',
  'event_label': 'contact_form',
  'value': 1
});

// בכפתור טלפון (header):
document.querySelectorAll('a[href^="tel:"]').forEach(a => {
  a.addEventListener('click', () => {
    gtag('event', 'phone_click', { 'event_category': 'lead', 'event_label': 'header_phone' });
  });
});

// בכפתור WhatsApp:
document.querySelectorAll('a[href*="wa.me"]').forEach(a => {
  a.addEventListener('click', () => {
    gtag('event', 'whatsapp_click', { 'event_category': 'lead', 'event_label': 'wa_float' });
  });
});
```

---

## Meta Pixel (פייסבוק / אינסטגרם)

```html
<!-- Meta Pixel — הכנס ב-<head> -->
<!-- ID נראה כך: 15 ספרות -->
<script>
  !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
  n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,
  document,'script','https://connect.facebook.net/en_US/fbevents.js');
  fbq('init', 'XXXXXXXXXXXXXXX'); // ← ID של הלקוח
  fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
  src="https://www.facebook.com/tr?id=XXXXXXXXXXXXXXX&ev=PageView&noscript=1"/></noscript>
```

### אירוע Lead (טופס)

```javascript
// אחרי שליחת טופס מוצלחת:
fbq('track', 'Lead', {
  content_name: '[שם הדף / עסק]',
  content_category: '[תחום]'
});

// אירוע Contact (לחיצה על טלפון):
fbq('track', 'Contact');
```

---

## טמפלייט מלא — head עם הכל

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[שם עסק] — [סלוגן]</title>
  <!-- SEO — ראה references/seo.md -->

  <!-- Google Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
  <script>
    window.dataLayer=window.dataLayer||[];
    function gtag(){dataLayer.push(arguments);}
    gtag('js',new Date());
    gtag('config','G-XXXXXXXXXX');
  </script>

  <!-- Meta Pixel -->
  <script>
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
    n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,
    document,'script','https://connect.facebook.net/en_US/fbevents.js');
    fbq('init','XXXXXXXXXXXXXXX');fbq('track','PageView');
  </script>

  <!-- Fonts & Icons -->
  <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;700;800;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
```

---

## שאלות לפני הכנסת Tracking

שאל את הלקוח:
1. **יש לך Google Analytics?** אם כן — מה ה-Measurement ID? (G-XXXXXXXXXX)
2. **יש לך Meta Pixel?** אם כן — מה ה-Pixel ID? (15 ספרות)
3. **אם אין** — הכנס placeholder ורשום הערה בקוד: `<!-- GA4: טרם הוגדר, צריך G-XXXXXXXXXX -->`

**אל תמציא IDs** — אם לא קיבלת, השאר placeholder מוסבר.

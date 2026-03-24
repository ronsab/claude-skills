# SEO & Meta Tags — תבנית מלאה לדפי נחיתה

העתק את הבלוק הזה לתוך `<head>` בכל דף. מלא את הערכים לפי הפרויקט.

---

## תבנית מלאה

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- ═══ SEO בסיסי ═══ -->
  <title>[שם עסק] — [סלוגן קצר עד 60 תווים]</title>
  <meta name="description" content="[תיאור 150-160 תווים — מה העסק עושה, אזור שירות, יתרון מרכזי]">
  <meta name="keywords" content="[תחום], [שירות 1], [שירות 2], [עיר], [אזור]">
  <meta name="author" content="[שם עסק]">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://[domain.co.il]/">

  <!-- ═══ Open Graph — שיתוף בפייסבוק / וואטסאפ ═══ -->
  <!-- כשמישהו שולח את הקישור בווטסאפ — זה מה שמופיע -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://[domain.co.il]/">
  <meta property="og:title" content="[שם עסק] — [סלוגן]">
  <meta property="og:description" content="[תיאור 200 תווים — קצת יותר שיווקי מה-SEO description]">
  <meta property="og:image" content="https://[domain.co.il]/og-image.jpg">
  <!-- og:image חייב להיות 1200×630px לפחות, מועלה לשרת -->
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="he_IL">
  <meta property="og:site_name" content="[שם עסק]">

  <!-- ═══ WhatsApp — Preview מיוחד ═══ -->
  <!-- וואטסאפ משתמש ב-og:image ו-og:title אוטומטית -->
  <!-- אין צורך בתגיות נוספות -->

  <!-- ═══ Twitter Card ═══ -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="[שם עסק] — [סלוגן]">
  <meta name="twitter:description" content="[תיאור קצר]">
  <meta name="twitter:image" content="https://[domain.co.il]/og-image.jpg">

  <!-- ═══ Schema.org — Local Business (Google) ═══ -->
  <!-- עוזר לגוגל להציג את העסק בתוצאות מקומיות -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "[שם עסק]",
    "description": "[תיאור קצר]",
    "url": "https://[domain.co.il]",
    "telephone": "+972[PHONE_WITHOUT_HYPHENS]",
    "email": "[EMAIL]",
    "address": {
      "@type": "PostalAddress",
      "addressLocality": "[עיר]",
      "addressRegion": "[אזור]",
      "addressCountry": "IL"
    },
    "areaServed": ["[עיר 1]", "[עיר 2]", "[אזור]"],
    "serviceType": ["[שירות 1]", "[שירות 2]", "[שירות 3]"],
    "openingHours": "Su-Th 08:00-20:00, Fr 08:00-14:00",
    "priceRange": "$$"
  }
  </script>

  <!-- ═══ Favicon (אופציונלי) ═══ -->
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <!-- או emoji כ-favicon: -->
  <!-- <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🔒</text></svg>"> -->

</head>
```

---

## מילוי לפי תחום — דוגמאות

### אבטחה
```
title: "Smat Logiko — פתרונות אבטחה חכמים לבית ולעסק"
description: "התקנת מצלמות אבטחה, מערכות אזעקה ובקרת כניסה בירושלים ומרכז הארץ. ייעוץ חינם, התקנה מקצועית, אחריות 3 שנים. 054-XXXXXXX"
keywords: "מצלמות אבטחה, מערכת אזעקה, בקרת כניסה, שערים חשמליים, ירושלים, בית שמש"
```

### שיפוצים
```
title: "[שם] — שיפוצים ובנייה מקצועיים | [עיר]"
description: "שיפוץ דירות ובתים פרטיים ב[עיר]. ניסיון 15 שנה, עבודה נקייה ומסודרת, אחריות מלאה. מגיעים לייעוץ חינם — 05X-XXXXXXX"
```

### רפואה / קוסמטיקה
```
title: "[שם] — [תחום] מקצועי | [עיר]"
description: "טיפולים מקצועיים ב[תחום] ב[עיר]. [יתרון 1], [יתרון 2]. קביעת פגישה: 05X-XXXXXXX"
```

---

## כלל אצבע — אורכים

| שדה | אורך אידיאלי | מקסימום |
|---|---|---|
| `<title>` | 50-60 תווים | 70 |
| `meta description` | 150-160 תווים | 200 |
| `og:title` | 60-90 תווים | 100 |
| `og:description` | 150-200 תווים | 300 |

---

## og:image — ייצור מהיר ללא קובץ

אם אין תמונה מוכנה, השתמש ב-placeholder מ-Placehold.co:
```html
<meta property="og:image" content="https://placehold.co/1200x630/04090f/f0b429?text=[שם+עסק]">
```

זה יוצר תמונה עם הצבעים של הדף והשם — פתרון מהיר לשלב הראשון.

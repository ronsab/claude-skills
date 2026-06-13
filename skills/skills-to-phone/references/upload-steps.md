# העלאת סקילים ל-claude.ai — שלבים ידניים

claude.ai לא מאפשרת ניהול Skills דרך API, אז ההעלאה ידנית דרך הדפדפן. הסקילים מופיעים אחר כך גם בטלפון וגם ב-Claude Desktop app (אותו חשבון Anthropic).

## 3 כללי זהב
1. נוגעים רק בתיקייה `Documents\phone-skills\` — לא פותחים את `~/.claude`.
2. לעולם לא מחלצים (unzip) — מעלים את ה-zip כמו שהוא.
3. כל zip מעלים פעם אחת. אם קופץ "Replace" — זה אומר שהסקיל כבר היה שם, לוחצים Upload and replace (אין כפילות).

## השלבים
1. פתח `claude.ai` בדפדפן (במחשב, נוח יותר מהטלפון).
2. Settings → Capabilities → Skills.
3. לחץ **Upload skill**.
4. נווט אל `Documents\phone-skills\` ובחר קובץ `zip`.
5. לחץ Open. אם קופץ "Replace ... skill?" → **Upload and replace**.
6. חזור לכל סקיל. סמן בצ'ק-ליסט.

## תבנית checklist
```
[ ] שם-הסקיל-1.zip
[ ] שם-הסקיל-2.zip
[ ] שם-הסקיל-3.zip
```

## אם zip נדחה
- "malformed YAML frontmatter" → ה-description לא בשורה אחת. הרץ מחדש את `package_for_claude.ps1` (הוא מתקן).
- "Zip must contain exactly one SKILL.md" → תת-תיקייה כפולה. הסקריפט משמיט אותה — הרץ מחדש.
- אותיות עברית הפוכות / ג'יבריש → בעיית פונט בצד claude.ai, לא באריזה. דווח לרון.

## עדכון סקיל בעתיד
ל-claude.ai לא מתעדכן אוטומטית מ-git. אחרי שינוי סקיל בנייח: הרץ שוב `package_for_claude.ps1` על אותו סקיל, והעלה מחדש את ה-zip (Upload and replace).

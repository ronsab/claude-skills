# גופנים עבריים בסקיל

## גופנים מצורפים (מוטמעים אוטומטית ב-PDF)

הסקיל מצרף ב-`assets/fonts/` גרסאות **סטטיות** (לא variable) שעובדות גם ב-reportlab וגם ב-WeasyPrint:

| משפחה | משקלים | סגנון | מתאים ל- |
|-------|--------|-------|----------|
| **Heebo** | Regular, Bold | סאנס מודרני | הצעות מחיר, מסמכים שיווקיים, ברירת מחדל |
| **Assistant** | Regular, SemiBold | סאנס נקי | התכתבות עסקית, מסמכים רשמיים |
| **Frank Ruhl Libre** | Regular, Bold | סריף קלאסי | חוזים, מסמכים משפטיים/פורמליים |

## להוספת גופן נוסף

הורד גרסה **סטטית** (לא variable) מ-`github.com/google/fonts` (raw), הנח ב-`assets/fonts/`, והוסף `@font-face` ל-`FONT_FACE_CSS` ב-`hebrew_pdf.py`. אם הורדת variable font, המר לסטטי:

```python
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
f = TTFont("Font[wght].ttf")
instantiateVariableFont(f, {"wght": 700}, inplace=True)
f.save("Font-Bold.ttf")
```

## בחירת גופן ל-Word

ב-Word הגופן רק *מנוקב בשם* - הקובץ לא מטמיע אותו, והוא מרונדר אצל הקורא:
- `David` - בטוח כמעט בכל Windows+Office.
- `Assistant` / `Heebo` - יפה ומודרני, אך דורש התקנה אצל הקורא.
- אם נדרשת זהות חזותית מובטחת אצל כל הקוראים → ייצא PDF במקום Word.

## טיפוגרפיה

גודל גוף 12-14pt · line-height 1.6-1.8 · בלי letter-spacing על עברית · בלי ניקוד במסמכים עסקיים.

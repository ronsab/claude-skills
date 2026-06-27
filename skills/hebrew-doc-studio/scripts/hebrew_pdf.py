#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hebrew_pdf.py - הופך HTML/CSS למסמך PDF עברי מעוצב, RTL, עם גופנים מוטמעים.

זה הנתיב המומלץ למסמכים *מעוצבים* (הצעות מחיר, מסמכים שיווקיים, מסמך לקוח,
מסמך עם צבעים/לוגו/טבלאות). WeasyPrint מרנדר HTML/CSS אמיתי, כך שהעיצוב שאתה
כותב הוא בדיוק מה שיוצא ב-PDF. ה-RTL מטופל נייטיב דרך dir="rtl".

הגופנים העבריים *מוטמעים* מתוך assets/fonts של הסקיל, כך שה-PDF נראה זהה בכל
מחשב ולא תלוי בגופני המערכת. אין צורך ב-get_display ואין סידור תווים ידני -
מנוע ה-HTML מטפל ב-bidi לבד.

תלות:  pip install --break-system-packages weasyprint
שימוש:
    from hebrew_pdf import html_to_pdf, BASE_CSS
    html_to_pdf(body_html='<h1>הצעת מחיר</h1><p>שלום World</p>',
                output='proposal.pdf', title='הצעת מחיר', font='Heebo')
"""

import os
import sys

try:
    from weasyprint import HTML, CSS
except ImportError:
    print("חסרה תלות. התקן עם:  pip install --break-system-packages weasyprint",
          file=sys.stderr)
    raise

# נתיב הגופנים המצורפים לסקיל (assets/fonts ביחס לקובץ הזה)
_FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "..", "assets", "fonts")
_FONT_DIR = os.path.abspath(_FONT_DIR)


def _font_url(name):
    return "file://" + os.path.join(_FONT_DIR, name).replace(os.sep, "/")


# הטמעת הגופנים המצורפים. שלוש משפחות: Heebo (סאנס מודרני), Assistant
# (סאנס נקי), Frank Ruhl Libre (סריף פורמלי/משפטי).
FONT_FACE_CSS = f"""
@font-face {{ font-family:'Heebo'; font-weight:400;
  src:url('{_font_url("Heebo-Regular.ttf")}'); }}
@font-face {{ font-family:'Heebo'; font-weight:700;
  src:url('{_font_url("Heebo-Bold.ttf")}'); }}
@font-face {{ font-family:'Assistant'; font-weight:400;
  src:url('{_font_url("Assistant-Regular.ttf")}'); }}
@font-face {{ font-family:'Assistant'; font-weight:600;
  src:url('{_font_url("Assistant-SemiBold.ttf")}'); }}
@font-face {{ font-family:'Frank Ruhl Libre'; font-weight:400;
  src:url('{_font_url("FrankRuhlLibre-Regular.ttf")}'); }}
@font-face {{ font-family:'Frank Ruhl Libre'; font-weight:700;
  src:url('{_font_url("FrankRuhlLibre-Bold.ttf")}'); }}
"""

# בסיס טיפוגרפי לעברית. line-height גבוה, יישור התחלה (start) ל-RTL,
# טבלאות RTL, ללא letter-spacing (פוגע בעברית).
BASE_CSS = """
@page { size: A4; margin: 22mm 20mm; }
* { box-sizing: border-box; }
html, body { direction: rtl; }
body {
  font-family: var(--font, 'Assistant'), sans-serif;
  font-size: 11.5pt;
  line-height: 1.75;
  color: #1a1a1a;
  margin: 0;
}
h1, h2, h3 { color: var(--accent, #1F4E79); line-height: 1.3; text-align: start; }
h1 { font-size: 26pt; font-weight: 700; margin: 0 0 4pt; }
h2 { font-size: 16pt; font-weight: 700; margin: 18pt 0 6pt;
     border-bottom: 2px solid var(--accent, #1F4E79); padding-bottom: 3pt; }
h3 { font-size: 13pt; font-weight: 600; margin: 12pt 0 4pt; }
p  { margin: 0 0 8pt; text-align: right; }
ul, ol { margin: 0 0 10pt; padding-inline-start: 22px; }
li { margin: 0 0 4pt; }
a { color: var(--accent, #1F4E79); }
table { width: 100%; border-collapse: collapse; margin: 8pt 0 14pt;
        font-size: 10.5pt; }
th, td { border: 1px solid #ccc; padding: 6px 10px; text-align: start;
         vertical-align: middle; }
thead th { background: var(--accent, #1F4E79); color: #fff; font-weight: 700; }
tbody tr:nth-child(even) { background: #f4f6f9; }
.muted { color: #666; }
.num { font-variant-numeric: tabular-nums; }
.total { font-size: 14pt; font-weight: 700; color: var(--accent, #1F4E79);
         text-align: right; }
.totals { text-align: right; }     /* בלוק סיכומים - מיושר לימין כמו כל המסמך */
.align-left { text-align: left; }  /* רק כשבאמת רוצים יישור שמאל */
.header-band { background: var(--accent, #1F4E79); color:#fff; padding:18px 22px;
               border-radius: 8px; margin-bottom: 16px; }
.header-band h1 { color:#fff; margin:0; }
"""


def html_to_pdf(body_html, output, title="מסמך", font="Assistant",
                accent="#1F4E79", extra_css="", full_html=None,
                palette=None, tint=None):
    """מייצר PDF עברי מעוצב מ-HTML.

    body_html : תוכן ה-<body> (HTML). מתעלמים ממנו אם full_html ניתן.
    output    : נתיב קובץ הפלט.
    font      : 'Heebo' / 'Assistant' / 'Frank Ruhl Libre'.
    accent    : צבע מותג להדגשות וכותרות (אם palette לא ניתן).
    palette   : שם פלטה מ-palettes.PALETTES (navy/teal/indigo/emerald/
                burgundy/charcoal). דורס accent/tint אם ניתן.
    tint      : גוון בהיר לפסי-טבלה (אם לא ניתן, נגזר מהפלטה או ברירת מחדל).
    extra_css : CSS נוסף שמתווסף אחרי הבסיס (override).
    full_html : אם רוצים לשלוט במסמך המלא - HTML שלם עם <html dir=rtl>.
    """
    if palette:
        try:
            from palettes import PALETTES
        except ImportError:
            import os as _os
            sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
            from palettes import PALETTES
        p = PALETTES.get(palette, PALETTES["navy"])
        accent, tint = p["accent"], (tint or p["tint"])

    zebra_css = (f"tbody tr:nth-child(even){{background:{tint};}}"
                 if tint else "")
    extra_css = (extra_css or "") + zebra_css

    if full_html:
        html_doc = full_html
        css_list = [CSS(string=FONT_FACE_CSS)]
        if extra_css:
            css_list.append(CSS(string=extra_css))
    else:
        root_style = f":root{{--font:'{font}';--accent:{accent};}}"
        html_doc = f"""<!DOCTYPE html>
<html lang="he" dir="rtl"><head><meta charset="utf-8"><title>{title}</title></head>
<body>{body_html}</body></html>"""
        css_list = [CSS(string=FONT_FACE_CSS),
                    CSS(string=root_style + BASE_CSS)]
        if extra_css:
            css_list.append(CSS(string=extra_css))

    HTML(string=html_doc, base_url=_FONT_DIR).write_pdf(output, stylesheets=css_list)
    return output


# ------------------- בדיקה עצמית -------------------
if __name__ == "__main__":
    body = """
    <div class="header-band">
      <h1>הצעת מחיר - הטמעת AI ארגונית</h1>
      <div>בינה מלאכותית בגובה העיניים | 22/06/2026</div>
    </div>
    <p class="muted">לכבוד: חברת Acme בע"מ. הצעה זו בתוקף ל-30 יום ממועד הפקתה.</p>
    <h2>פירוט השירותים</h2>
    <p>הפרויקט כולל שלושה שלבים: אפיון מלא, פיתוח MVP, והדרכת צוות. הליווי
       מתבצע בערוץ WhatsApp ייעודי, וכל התוצרים נמסרים בפורמט Word ו-PDF.</p>
    <ul>
      <li>אפיון תהליכי העבודה (workflow mapping)</li>
      <li>פיתוח אב-טיפוס תוך 30 יום</li>
      <li>הדרכת צוות בן 12 עובדים</li>
    </ul>
    <h2>טבלת תמחור</h2>
    <table>
      <thead><tr><th>תיאור</th><th>כמות</th><th>מחיר ליחידה</th><th>סה"כ</th></tr></thead>
      <tbody>
        <tr><td>אפיון</td><td class="num">1</td><td class="num">5,000.00</td><td class="num">5,000.00</td></tr>
        <tr><td>פיתוח MVP</td><td class="num">1</td><td class="num">12,000.00</td><td class="num">12,000.00</td></tr>
        <tr><td>הדרכה</td><td class="num">12</td><td class="num">800.00</td><td class="num">9,600.00</td></tr>
      </tbody>
    </table>
    <p class="totals">סה"כ לפני מע"מ: 26,600.00 ש"ח</p>
    <p class="totals">מע"מ (18%): 4,788.00 ש"ח</p>
    <p class="totals total">סה"כ לתשלום: 31,388.00 ש"ח</p>
    """
    out = html_to_pdf(body, "/home/claude/test_proposal_weasy.pdf",
                      title="הצעת מחיר", font="Heebo", accent="#1F4E79")
    print("נוצר:", out)

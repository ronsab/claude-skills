#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
palettes.py - פלטות צבע מקצועיות מוכנות למסמכים עבריים.

כל פלטה: accent (צבע ראשי לכותרות, פס-כותרת וכותרת-טבלה) + tint (גוון בהיר
לפסי-טבלה ולרקעים). השתמש כך:
    from palettes import PALETTES
    p = PALETTES["teal"]
    html_to_pdf(body, out, accent=p["accent"])          # PDF
    HebrewDoc(accent=p["accent"].lstrip("#"), ...)        # DOCX (hex ללא #)

המשתמש יכול תמיד למסור hex חופשי משלו (למשל צבעי מותג).
"""

PALETTES = {
    "navy": {
        "he": "כחול עסקי",
        "accent": "#1F4E79", "tint": "#EAF0F7",
        "use": "ברירת מחדל. אמין, נקי, מתאים כמעט לכל מסמך עסקי.",
    },
    "teal": {
        "he": "טורקיז טכנולוגי",
        "accent": "#0E7C86", "tint": "#E3F3F4",
        "use": "תחושת טק/AI מודרנית. מצוין למסמכי מוצר והצעות הטמעה.",
    },
    "indigo": {
        "he": "סגול פרימיום",
        "accent": "#4B3F9E", "tint": "#ECEAF8",
        "use": "יצירתי ויוקרתי. מתאים למסמכים שיווקיים ולמיתוג בולט.",
    },
    "emerald": {
        "he": "ירוק כספי",
        "accent": "#1E6F5C", "tint": "#E6F2EE",
        "use": "צמיחה, כספים, קיימוּת. רענן ורגוע.",
    },
    "burgundy": {
        "he": "בורדו פורמלי",
        "accent": "#8C2F39", "tint": "#F6E9EA",
        "use": "אלגנטי ושמרני. מתאים לחוזים ומסמכים משפטיים/רשמיים.",
    },
    "charcoal": {
        "he": "גרפיט מינימליסטי",
        "accent": "#333333", "tint": "#F1F0ED",
        "use": "מינימליסטי וניטרלי. נותן לתוכן לדבר, מתאים לדוחות.",
    },
}

DEFAULT = "navy"


def get(name):
    """מחזיר פלטה לפי שם, עם נפילה לברירת המחדל."""
    return PALETTES.get(name, PALETTES[DEFAULT])

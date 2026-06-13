# update-map — ריענון מפת הסקילים

## מטרה
בונה מחדש את מפת הסקילים בשולחן העבודה מתוך `skill-map-data.json` והסריקה האוטומטית של כל הסקילים/commands/agents.

---

## שלב 1: הרצת הגנרטור

```bash
node ~/.claude/skill-map/generate-map.mjs
```

הגנרטור סורק את `~/.claude/skills/`, `~/.claude/commands/`, `~/.claude/agents/`, ממזג עם `~/.claude/skill-map/skill-map-data.json`, ובונה את `Desktop/skill-map.html` + `Desktop/ron-service-menu.html`.

---

## שלב 2: דוח

הצג לרון את שורת הספירה מהפלט, למשל:
```
✅ skill-map.html נבנה
   57 עסקיים · 553 בספרייה · 463 לא מסווגים · 10 הזדמנויות
```

אם הספירה ירדה בטעות, או יש שגיאת פרסור — הזהר ובדוק את skill-map-data.json (כנראה JSON שבור).

---

## הערות
- המפה מתעדכנת גם אוטומטית בכל פתיחת סשן (SessionStart hook ב-settings.json → run-map.sh)
- להעשרת המפה (הוספת סקיל לשכבה העסקית, תרחיש, קיבוץ) — השתמש בסקיל `skill-map`
- גישה מהירה: הקיצור `מפת הסקילים` בשולחן העבודה

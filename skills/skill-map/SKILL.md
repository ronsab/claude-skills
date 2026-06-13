---
name: skill-map
description: Use when Ron maintains or enriches his personal skill-map — the live HTML map at Desktop/skill-map.html, generated from ~/.claude/skill-map/. Covers adding a skill/command/agent to the business layer, adding a scenario, tuning library grouping, editing categories/conflicts/opportunities/recipes/checklists, and rebuilding the map. TRIGGER on 'מפת הסקילים', 'skill-map', 'תוסיף למפה', 'תסווג סקיל', 'תוסיף תרחיש', 'תעדכן את המפה', 'הזדמנות במפה', paths under ~/.claude/skill-map/. NOT for creating new Claude skills (that is skill-creator) and NOT for editing hooks/settings.json (that is update-config).
---

# skill-map — תחזוקת מפת הסקילים האישית של רון

מערכת חיה שסורקת את כל הסקילים/commands/agents במחשב, ממזגת עם ידע עסקי, ובונה מפת HTML אינטראקטיבית בעברית (RTL) בשולחן העבודה.

## מקור האמת
**כל עריכת ידע עסקי נעשית ב-`~/.claude/skill-map/skill-map-data.json` בלבד.** הגנרטור סורק את הסקילים אוטומטית וממזג איתם. אסור לערוך את ה-HTML ישירות (הוא נדרס בכל ריצה).

## ארכיטקטורה
```
~/.claude/skill-map/
├── generate-map.mjs      # גנרטור Node ללא תלויות (fs+path בלבד). ~1000 שורות.
├── skill-map-data.json   # single source of truth — שכבת ה-curation העסקית
├── run-map.sh            # wrapper ל-SessionStart hook (סינכרוני, exit 0 תמיד)
└── map-icon.ico          # אייקון הקיצור בשולחן

פלט (נדרס בכל ריצה):
~/Desktop/skill-map.html       # המפה האינטראקטיבית
~/Desktop/ron-service-menu.html # תפריט שירותים ללקוח (מ-serviceMenu)
```

## איך הגנרטור עובד
1. טוען `skill-map-data.json`
2. סורק `~/.claude/skills/` (כולל סקילים מקוננים בתיקיות-אב), `~/.claude/commands/`, `~/.claude/agents/` — מפרסר frontmatter (name+description) ב-regex
3. ממזג: סקיל עם entry ב-data.json → כרטיסייה עסקית עשירה. סקיל ללא entry → "ספרייה מלאה" (מקובץ ב-`classifyLib`)
4. בונה HTML עם הזרקת JSON ל-JS צד-לקוח (חיפוש, מועדפים, ניווט — הכל offline ב-localStorage)

## מבני הנתונים (להעשרה)

### entry — כרטיסייה עסקית (`skills` / `commands` / `agents`)
```json
"carousel-builder": { "category": "market", "emoji": "🎠",
  "invoke": "Skill: carousel-builder",
  "whenToUse": "מתי להפעיל — תיאור קצר",
  "output": "מה הסקיל מוציא",
  "opportunity": "ההזדמנות העסקית / pricing",
  "pricing": "₪300-800", "badges": ["חדש", "גרפיקה"] }
```
שדות: `category` (מפתח מ-categories), `emoji`, `invoke`, `whenToUse`, `output`, `opportunity`, `pricing`, `badges[]`. אופציונלי: `canonical:true`.

### enrich — דוגמה + טוויסט (מפתח `enrich`, לפי id)
```json
"carousel-builder": { "example": "תבנה קרוסלה של 6 שקופיות על השירותים שלי",
  "twist": "צמד עם social-content לקופי → סט פוסט מלא ב-2 סקילים" }
```

### scenario — תרחיש מהחיים (מפתח `scenarios`)
```json
{ "icon": "📞", "title": "לקוח פנה לראשונה",
  "trigger": "מתי זה קורה",
  "steps": [
    { "num": 1, "action": "מה עושים", "skill": "new-client",
      "say": "/new-client", "get": "מה מקבלים" }
  ] }
```

### libraryGroup — קיבוץ הספרייה (מפתח `libraryGroups`, מסודר)
```json
{ "id": "marketing", "label": "🎯 שיווק ותוכן", "open": true, "priority": true,
  "prefix": ["blog","market"], "kw": ["copywrit","seo"] }
```
דגלים: `open` (פתוח כברירת מחדל), `priority` (בולט בראש), `collapsed` (רעש מקופל), `catchall` (תופס את השאר). התאמה: `prefix`/`suffix`/`kw`.
**`classifyLib` בודק בסדר: suffix → prefix → keyword → catchall** (כך הרעש המדויק כמו `-sci` נתפס לפני keyword). זה מבטיח ש-`market-research-reports-sci` → מדע, לא שיווק.

### מפתחות נוספים ב-data.json
`categories` (build/biz/market/...), `decisionRules` (אשף "איזה סקיל מתי"), `cheatSheet`, `conflicts` (ניתוב בין סקילים חופפים), `opportunities` (הזדמנות השבוע), `recipes` (שרשראות סקילים), `buildIdeas`, `sparks`, `checklists`, `serviceMenu` (תפריט הלקוח).

## רענון המפה
אחרי כל עריכה ב-data.json:
```bash
node ~/.claude/skill-map/generate-map.mjs
```
או הפקודה `/update-map`. הפלט מציג ספירה: `57 עסקיים · 553 בספרייה · ...`. המפה מתעדכנת גם אוטומטית בכל SessionStart (hook ב-settings.json).

## אימות ויזואלי
Playwright חוסם `file://`. להגשה מקומית:
```bash
node -e "const h=require('http'),f=require('fs'),p=require('path'),o=require('os');h.createServer((q,r)=>{let x=q.url==='/'?'/skill-map.html':decodeURIComponent(q.url);try{r.writeHead(200,{'Content-Type':'text/html; charset=utf-8'});r.end(f.readFileSync(p.join(o.homedir(),'Desktop',x)));}catch(e){r.writeHead(404);r.end()}}).listen(8799)" &
```
ואז Playwright ל-`http://localhost:8799/skill-map.html`.

## כללי זהב
- **שמור ספירה**: אחרי שינוי, ודא שמספר העסקיים לא ירד בטעות
- **RTL תמיד**: כל טקסט עברי, branding ברונזה (`#9C7A4A`) + navy
- **בטיחות DOM**: ב-JS צד-לקוח השתמש ב-`textContent`/`el()`, לא `innerHTML` גולמי
- **שמות בעברית**: labels, titles — עברית. id/keys — אנגלית
- הקיצור בשולחן (`מפת הסקילים.lnk`) מצביע ל-path קבוע → תמיד פותח גרסה עדכנית

## גבולות — מה לא שייך לסקיל הזה
- **ליצור סקיל חדש** → `skill-creator` (לא כאן)
- **לערוך hooks / settings.json** → `update-config` (לא כאן)
- סקיל זה **רק** לעריכת תוכן המפה ובנייתה מחדש

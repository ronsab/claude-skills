---
description: סנכרון כל ה-Skills, agents, commands וההגדרות ל-GitHub (מהנייח אל הלפטופ)
---

# /sync-skills

מסנכרן את הגדרות Claude Code שלך (`~/.claude`) ל-repo הפרטי `github.com/ronsab/claude-skills`, כדי שכל המכשירים יישארו מעודכנים.

## מה לעשות

הרץ את הרצף הבא דרך Bash. עצור ודווח לרון אם משהו נכשל.

### 1. בדיקת בטיחות לפני הכל
ודא שאף קובץ סודי לא ייכנס ל-commit:
```bash
cd /c/Users/USER/.claude
git add skills/ agents/ commands/ CLAUDE.md skill-map/ templates/ knowledge-files/ \
        settings.json plugins/ron-digital/ plugins/ron-outreach/ \
        plugins/installed_plugins.json plugins/known_marketplaces.json .gitignore
# חובה: הרשימה הבאה חייבת להיות ריקה
git diff --cached --name-only | grep -xE '\.env\.global|\.credentials\.json|settings\.local\.json|mcp-needs-auth-cache\.json'
```
אם משהו מופיע בבדיקה הזו - **עצור**, אל תעשה commit, ודווח לרון. אחרת המשך.

### 2. commit + push
```bash
git commit -m "Sync skills $(date +%Y-%m-%d)" || echo "אין שינויים לסנכרון"
git push origin main
```

### 3. דיווח
דווח לרון בקצרה: כמה קבצים השתנו, ושהדחיפה הצליחה. אם אין שינויים - אמור "הכל מסונכרן, אין מה לעדכן".

## הערות
- הסודות (`.env.global`, `.credentials.json`, `settings.local.json`) מוחרגים ב-`.gitignore` בכוונה ולא מסונכרנים. בכל מכשיר הם נשארים מקומיים.
- אם רון רוצה למשוך עדכונים שנעשו במכשיר אחר: `git pull origin main` (לא חלק מהפקודה הזו - היא רק דוחפת).

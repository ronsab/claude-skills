---
name: skills-to-phone
description: 'אריזת סקיל מקומי של רון מ-~/.claude/skills לקובץ zip תקין להעלאה ל-claude.ai, כדי שיופיע בטלפון וב-Claude Desktop app. הפעל כשרון אומר "תכין סקילים לטלפון", "תארוז סקיל ל-claude.ai", "תעדכן סקיל בטלפון", "סקיל לאפליקציה", או רוצה שסקיל מסוים יהיה זמין בנייד. הסקיל מתקן את 3 התקלות הידועות (קו נטוי Linux, SKILL.md אחד בשורש, frontmatter בשורה אחת), מוודא תקינות, ומפיק checklist להעלאה הידנית. לא בשביל סנכרון git ללפטופ (זה /sync-skills) ולא ליצירת סקיל מאפס (זה skill-creator).'
---

# Skills To Phone — אריזת סקילים ל-claude.ai

מטרת הסקיל: לקחת תיקיית סקיל מקומית של רון ולהפיק ממנה קובץ `zip` שעובר את הוולידציה של claude.ai, כדי שרון יוכל להעלות אותו ידנית ושהסקיל יופיע בטלפון וב-Claude Desktop app.

## מתי להשתמש
- רון רוצה שסקיל מסוים (או כמה) יהיה זמין בטלפון / באפליקציית Desktop
- רון עדכן סקיל בנייח ורוצה לרענן אותו גם ב-claude.ai
- triggers: "תכין סקילים לטלפון", "תארוז ל-claude.ai", "תעדכן סקיל בטלפון", "סקיל לאפליקציה"

## רקע קריטי (למה צריך אריזה מיוחדת)
claude.ai היא מערכת נפרדת מ-Claude Code. היא **לא** קוראת את `~/.claude/skills/` - מעלים אליה zip ידנית דרך הדפדפן. הפרסר שלה מחמיר יותר מ-Claude Code, ולכן zip "רגיל" נדחה. שלוש תקלות ידועות שהסקריפט מתקן אוטומטית:

1. `Compress-Archive` ב-PowerShell 5.1 יוצר נתיבי `backslash` שבורים ל-Linux. הסקריפט בונה עם `ZipArchive` ידני וקו נטוי `/`.
2. claude.ai דורש `SKILL.md` **אחד בלבד בשורש** ה-zip. חלק מהסקילים מכילים תת-תיקייה כפולה בשם הסקיל - הסקריפט משמיט אותה.
3. claude.ai דורש `description` ב**שורה אחת**. block scalar (`>`), frontmatter רב-שורתי או מרכאות שבורות נדחים - הסקריפט משטח את `name`/`description` לשורה אחת single-quoted (כולל escaping של גרשים בעברית).

## איך מריצים

```powershell
powershell -File "$env:USERPROFILE\.claude\skills\skills-to-phone\scripts\package_for_claude.ps1" -Skills copywriting,write-landing,ron-system-pitch
```

- `-Skills` — שמות הסקילים (כפי שמופיעים בתיקייה `~/.claude/skills/`), מופרדים בפסיק
- פלט: קובץ `zip` לכל סקיל ב-`Documents\phone-skills\`
- הסקריפט מריץ **ולידציה** אחרי הבנייה ומדווח על כל כשל. אם משהו נכשל - עצור ודווח לרון, אל תשלח אותו להעלות zip פגום.

## אחרי הבנייה — העלאה ידנית (לא ניתן לאוטמט)
ל-claude.ai אין API לניהול Skills, אז ההעלאה ידנית. ראה `references/upload-steps.md` לשלבים המלאים. בקצרה:
1. `claude.ai` בדפדפן → Settings → Capabilities → Skills
2. Upload skill → בחר zip מ-`Documents\phone-skills\` → Open
3. אם קופץ "Replace ... skill?" → Upload and replace (אין כפילות, רק עדכון)

## בחירת סקילים מתאימים לטלפון
רק סקילים **עצמאיים** עובדים ב-sandbox של claude.ai. אל תארוז סקילים שתלויים בכלים מקומיים: MCP (Make/Pinecone/NotebookLM), CLI (ffmpeg/python/vercel/gh), או קבצים על הדיסק. סקילים טקסטואליים/אסטרטגיים (קופי, שיווק, מכירה, אסטרטגיה) — כן.

## גבולות — לא בשביל (כלל הברזל, אין חפיפה)
- **לא** לסנכרון git ללפטופ → זה הפקודה `/sync-skills` (git push). הסקיל הזה נוגע רק ב-claude.ai/טלפון.
- **לא** ליצירת סקיל חדש מאפס → זה `skill-creator`. הסקיל הזה אורז סקילים **קיימים** בלבד.
- **לא** למפת ה-HTML של הסקילים → זה `skill-map`.
- היעד היחיד: תיקיית סקיל מקומית → zip תקין ל-claude.ai.

## קבצים
- `scripts/package_for_claude.ps1` — מנוע האריזה + הוולידציה
- `references/upload-steps.md` — שלבי ההעלאה הידנית + תבנית checklist

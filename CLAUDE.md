# CLAUDE.md - Ron Sabon (Global)

## שפה ותקשורת
- תמיד תתקשר בעברית בלבד, גם אם אני כותב לך באנגלית
- תשובות קצרות, ישירות וממוקדות מטרה. ללא מבואות מיותרות
- אין להשתמש במקף ארוך (--) לשום מטרה
- אל תאמר לי מה אני רוצה לשמוע. הצג את האמת גם אם היא מנוגדת לדעתי

## עיצוב תשובות — RTL ב-Claude Desktop
- ברשימות: `מונח אנגלי` ואחריו הסבר בעברית על אותה שורה — המונח תמיד קודם
- אל תכניס אנגלית באמצע משפט עברי — שים אותה בתחילת הנקודה או בשורה נפרדת
- פסקה שלמה באנגלית: הפרד ב-`---` לפני ואחרי
- קוד: תמיד בבלוק קוד נפרד בלבד

## לפני כל פעולה
- אם הבקשה לא ברורה 100%, עצור ושאל שאלות הבהרה לפני ביצוע
- אין להמציא פתרונות, לנחש, או ליצור נתונים שאינם קיימים
- ציין במפורש כל אי-ודאות
- תמיד בדוק את עצמך לפני מתן תשובה

## כללי עבודה
- עבוד בצעדים קטנים. אל תשנה הכל בבת אחת
- תעד כל שינוי שנעשה בצורה ברורה
- לאחר כל שינוי, הצג מה השתנה ולמה
- אל תשנה קוד קיים ללא אישור מפורש

## סטאק ופרויקטים

### React / Lovable
- RTL חובה בכל ממשק עברי: dir="rtl", text-align: right, direction: rtl
- רכיבים בעברית: placeholder, label, aria-label, כולם RTL
- Tailwind: השתמש ב-text-right, mr-* במקום ml-*, pr-* במקום pl-*
- בדוק תמיד שהניווט במובייל תקין לאחר שינויים

### Make / Zapier / אוטומציות
- לפני בניית תרחיש, מפה את הזרימה המלאה בטקסט
- ציין מפורשות: טריגר, מודולים, תנאים, שגיאות אפשריות
- אל תניח שחיבור לשירות קיים, שאל לפני
- בדוק error handling בכל מודול

### כללי קוד
- השתמש בהערות בעברית בקוד
- העדף פתרונות פשוטים על פני מורכבים
- אל תתקין חבילות חדשות ללא אישור

## קונטקסט אישי
- שם: רון, יזם דיגיטלי + עובד ממשלתי
- סטודיו: RON DIGITAL STUDIO (אתרים, אוטומציות, AI לעסקים קטנים)
- מערכת הפעלה: Windows
- מייל: ronsabon@gmail.com
- מיקום: ישראל, Asia/Jerusalem

## מה לא לעשות לעולם
- להמציא API keys, URLs, שמות משתמש, או נתונים שלא סופקו
- לשנות קבצים מחוץ לתיקיית הפרויקט ללא אישור
- להציע פתרון לפני שהבעיה ברורה לחלוטין
- לחזור על מה שכבר נאמר בשיחה

## Make.com Account Reference
- Team ID: 2341960
- Org ID: 4698040
- Region: EU2
- Timezone: Asia/Jerusalem

### Connections פעילים
| שירות | App Version | Connection ID |
|-------|-------------|---------------|
| Gmail | google-email@4 | 13833758 |
| Google Sheets | google-sheets@2 | 13833768 |
| Google Drive | google-drive@4 | 13833768 |
| OpenAI | openai-gpt-3@1 | 13836712 |

### App Versions ידועים
`google-email@4`, `google-sheets@2`, `google-drive@4`, `slack@4`, `telegram@1`, `http@4`, `gateway@1`, `json@1`, `builtin@1`, `openai-gpt-3@1`, `anthropic-claude@1`, `whatsapp-business-cloud@1`

## Skills זמינים

### בנייה ועיצוב
- `landing-page-builder` (local) -- דף נחיתה HTML בודד, Three.js, RTL, Vercel (₪1,200-2,800). **תמיד להעדיף על-פני `anthropic-skills:landing-page-builder`**
- `fullstack-app` -- אפליקציה מלאה React+Vite+Supabase+Tailwind+Netlify (₪4,500-9,000) — כשצריך login/DB/dashboard
- `make-automation-builder` (local, CANONICAL) -- אוטומציות Make.com עם validation pipeline + ידע מאומת Gmail. **תמיד להעדיף על-פני `anthropic-skills:make-automation-builder`**
- `write-landing` -- כתיבת copy + frameworks (PAS/AIDA/BAB) לפני בנייה. בפרויקטים גדולים: write-landing קודם, אחר כך landing-page-builder
- `frontend-design` (local) -- עקרונות UI/UX מודרני, חלק מ-impeccable system
- `impeccable:impeccable` + sub-skills (`polish`, `animate`, `audit`, `bolder`, `clarify`, `colorize`, `critique`, `delight`, `distill`, `extract`, `harden`, `normalize`, `onboard`, `optimize`, `overdrive`, `quieter`, `typeset`, `teach-impeccable`, `adapt`, `arrange`) -- פולישינג ויזואלי אחרי builds
- `vercel-react-best-practices` -- React/Next.js performance (45 rules, 8 קטגוריות)
- `hebrew-subtitles` (local) -- כתוביות עברית אוטומטיות לסרטונים: Whisper API + ffmpeg, תוצר SRT + MP4 צרוב, סגנון TikTok או קלאסי, כולל שלב אישור תמלול + כותרת עליונה אופציונלית
- `video-merge` (local) -- איחוד קליפים קצרים לסרטון אחד עד 90 שניות (אינסטגרם/פייסבוק), נרמול אוטומטי לפורמט אחיד. זרימה: קודם איחוד, אחר כך hebrew-subtitles

### מסמכים עסקיים
- `ron-digital-presentation` -- מצגת HTML scrollytelling מ-Google Docs → Vercel
- `anthropic-skills:ron-digital-quote` -- הצעת מחיר RON DIGITAL (HTML branded, מחירון מלא ₪800-9,000+)
- `anthropic-skills:ron-service-doc` -- Scope of Work פורמלי, **תמיד לפני הצעת מחיר**
- `ron-client-search` -- חיפוש לקוחות דומים ב-Pinecone (index: ron-clients)
- `anthropic-skills:landy-prompt-builder` -- פרומפטים למערכת Landy AI (800/5000 תווים, 9 סוגי דפים, 10 שאלות, 3 רמות עיצוב)

### RON Assistant -- מערכת מכירות (funnel בסדר)
- `anthropic-skills:ron-system-pitch` -- pitch 60 שניות + 3 hooks + טיפול ב-3 התנגדויות (פגישה ראשונה)
- `anthropic-skills:ron-system-demo` -- תסריט דמו חי 10 דקות: מה ללחוץ + מה לומר (הדגמה)
- `anthropic-skills:ron-system-roi` -- חישוב ROI מותאם: חיסכון בזמן + ערך לידים + תקופת החזר (הצדקה כלכלית)
- `anthropic-skills:ron-system-proposal` -- הצעת מחיר פורמלית למערכת RON Assistant
- `anthropic-skills:ron-system-onboard` -- onboarding ללקוח שחתם: נישות/ערים/ICP/מותג + checklist
- `anthropic-skills:ron-system-case-study` -- Case Study אנונימי מנתוני לפני/אחרי (חומר שיווקי)

### שיווק ותוכן
- `market` (orchestrator) + sub-skills: `market-audit`, `market-copy`, `market-emails`, `market-social`, `market-ads`, `market-funnel`, `market-competitors`, `market-landing`, `market-launch`, `market-report`, `market-seo`, `market-brand`
  - `/market audit <url>` -- ניתוח שיווקי מלא לפני פגישות מכירה (5 agents מקבילים)
  - `/market competitors <url>` -- ניתוח תחרותי
  - `/market landing <url>` -- CRO analysis לדפי לקוחות (URL חיצוני, **לא** לדפים שאני בניתי)
  - `/market emails <topic>` -- סדרות אימייל ל-follow-up/nurture
- `blog` (orchestrator) + 20 sub-commands: `/blog write`, `/blog strategy`, `/blog calendar`, `/blog geo`, ועוד -- מנוע SEO לאתר RON DIGITAL
- `social-post-generator` (agent) -- פוסט בודד בקול של רון
- `anthropic-skills:israeli-social-content` -- לוח תוכן ישראלי מותאם תרבותית (פייסבוק/אינסטה/טיקטוק/לינקדאין). **תמיד להעדיף על-פני `market-social` לתוכן בעברית**
- `anthropic-skills:hebrew-seo-geo-toolkit` (CANONICAL לעברית) -- SEO + GEO לעברית: Google.co.il, schema.org בעברית, EEAT ישראלי, AI search (ChatGPT/Perplexity/Gemini/Copilot). **תמיד להעדיף על-פני `/blog geo` ו-`claude-seo:seo-geo` למאמרים בעברית**

### כלים ישראלים (אזרחי + עסקי) 🇮🇱
- `anthropic-skills:israeli-payroll-calculator` -- חישוב שכר ישראלי (ברוטו/נטו, ביטוח לאומי, פנסיה, שווי רכב). **שירות פוטנציאלי**: lead magnet "מחשבון שכר לעצמאי"
- `anthropic-skills:israeli-gov-form-automator` -- מילוי טפסי ממשלה אוטומטי (Playwright + PDF). **שירות פוטנציאלי**: ₪3,000-7,000 אינטגרציה לעורכי דין/רואי חשבון
- `anthropic-skills:israeli-phone-formatter` -- אימות/פורמט טלפון ישראלי (+972). השתמש בטפסי לידים בדפי נחיתה
- `anthropic-skills:israel-gov-api` -- data.gov.il (CKAN API). לתחקירים, סטטיסטיקות, נתונים לטענת אמינות
- `anthropic-skills:israeli-rental-agreements` -- חוזי שכירות, חוק שכירות הוגנת 2017. **חומר בלוג פוטנציאלי**
- `anthropic-skills:israeli-telecom-comparator` -- השוואת חבילות סלולר/אינטרנט/TV. **חומר בלוג פוטנציאלי**
- `anthropic-skills:israeli-utility-rates-comparator` -- חשמל/מים/גז/ארנונה. **חומר בלוג + lead magnet**
- `anthropic-skills:israeli-product-price-comparator` -- Zap/KSP/iDigital. **lead magnet אפשרי**
- `anthropic-skills:israeli-apartment-hunting` -- דירות שכירות (Yad2, Madlan)
- `anthropic-skills:israeli-public-transit` -- אוטובוסים/רכבות
- `anthropic-skills:israeli-ui-design-system` -- RTL design system לאפליקציות (Hebrew typography, gov.il patterns). **משלים `fullstack-app`, לא `landing-page-builder`**

### מסמכים בעברית (נוספים)
- `anthropic-skills:hebrew-document-generator` -- PDF/DOCX/PPTX בעברית (Heshbonit, Hozeh, Hatza'at Mechir, Protokol). **תמיד לפני המרות מ-HTML ל-PDF**
- `anthropic-skills:presentation-generator` -- מצגות RTL פורמליות לתאגידים
- `anthropic-skills:hyperframes-best-practices` -- וידאו HTML+GSAP בעברית RTL. **capability חדש לוידאו hero בדפי נחיתה**

### Utilities
- `prompt` -- שליפת פרומפט מ-NotebookLM (כבר ב-routing למעלה)
- `simplify` -- ניקוי וייעול קוד אחרי כל פרויקט (לפני שליחה ללקוח)
- `nekudat-hashmal` -- סקיל-פרויקט ספציפי ללקוח שלמה שושן (דפוס לסקילי-לקוח עתידיים)
- `skill-map` -- תחזוקת/העשרת מפת הסקילים (הוספת סקיל לשכבה העסקית, תרחיש, כיוונון קיבוץ). מתעד את כל מבנה `skill-map-data.json`. **לא** ליצירת סקיל חדש (זה `skill-creator`)

### מחקר וידע (NotebookLM)
- `notebooklm` -- גישה מלאה ל-Google NotebookLM כולל יכולות שאינן ב-UI. מחובר כ-ronsabon@gmail.com (storage: `~/.notebooklm/profiles/default/`)
  - יצירת notebooks, הוספת sources (URL/YouTube/PDF/Drive), chat, יצירת podcasts/video/quiz/flashcards/mind-map/slides
  - מופעל אוטומטית על intent כמו "תיצור podcast על X", "תכין flashcards מ-Y", "תשאל את ה-notebook על Z"
  - CLI ידני: `notebooklm list` / `create` / `ask "..."` / `generate audio` / `download audio`
- `blog-notebooklm` -- skill נפרד לזרימת בלוג מבוססת-NotebookLM

#### NotebookLM Prompt Library Routing (חובה לפני כתיבת פרומפט מאפס)
כשרון מבקש פרומפט - **לפני** כתיבה מאפס, שלוף מ-NotebookLM:

| סוג בקשה | Notebook ID | פקודה |
|----------|-------------|--------|
| פרומפט וידיאו (Veo 3 / Sora / Runway / Kling) | `7f837353` (400 פרומפטים) | `notebooklm ask -n 7f837353 "תבניות פרומפט וידיאו ל-<תיאור הסצנה>"` |
| פרומפט תמונה (Midjourney / DALL-E / Nano Banana / Imagen) | `7f837353` (400 פרומפטים) | `notebooklm ask -n 7f837353 "תבניות פרומפט תמונה ל-<תיאור>"` |
| פרומפט קופי/פוסט/אימייל/מכירה | `04e92e65` (שגיא בר און) | `notebooklm ask -n 04e92e65 "תבנית פרומפט ל-<מטרה>"` |

**זרימה:** (1) שלוף תבנית/וריאציות רלוונטיות מה-notebook, (2) התאם לפרטי הבקשה של רון, (3) הצג את הפרומפט הסופי וציין מאיזה notebook נשלף.

**Override:** אם רון אומר במפורש "תכתוב מאפס" / "בלי NotebookLM" / "תתעלם מ-notebook" - דלג ועבד מהידע שלך.

**במקרה של כישלון API:** אם NotebookLM מחזיר 502/timeout 3 פעמים - דווח לרון, ושאל אם להמשיך בכתיבה מאפס.

---

## כללי החלטה (לסתירות אפשריות)

### דף נחיתה vs אפליקציה
שאל לפני: "האם הלקוח צריך login / מסד נתונים / dashboard / מערכת הזמנות?"
- ❌ **לא** → `landing-page-builder` (HTML בודד, ₪1,200-2,800)
- ✅ **כן** → `fullstack-app` (React+Supabase, ₪4,500-9,000)

### הצעת מחיר ללקוח שלי
- ללקוח של רון → תמיד `anthropic-skills:ron-digital-quote` (כולל מחירון + 10 שאלות גילוי + ROI + follow-up + objection handling)
- לפניה — תמיד `anthropic-skills:ron-service-doc` ל-SOW

### ביקורת דף נחיתה
- דף שאני בניתי (HTML מקומי), לפני שליחה ללקוח → `/review-page` (SEO+RTL+CTA+מובייל)
- דף של לקוח קיים או מתחרה (URL חיצוני) → `/market landing <url>` (CRO benchmarks)

### זרימת copy → build
בפרויקטי דפי נחיתה גדולים, או כשהלקוח רוצה אסטרטגיה:
1. `write-landing` -- בחירת framework (PAS/AIDA/BAB) + headlines + copy
2. `landing-page-builder` -- בנייה טכנית עם הקופי המוכן

### מצגות בעברית (3 דרכים — בחר לפי תוצר רצוי)
- **HTML scrollytelling + Vercel link** (לוואטסאפ, online) → `ron-digital-presentation`
- **PPTX להורדה** (פגישות פיזיות, לקוחות תאגידיים) → `anthropic-skills:hebrew-document-generator` (PPTX)
- **deck פורמלי RTL** (פיץ' מסורתי) → `anthropic-skills:presentation-generator`

### SEO בעברית (3 כלים — היררכיה ברורה)
- **קאנוני לעברית**: `anthropic-skills:hebrew-seo-geo-toolkit` (Google.co.il + AI search)
- **בלוג שלם**: `/blog write` + `/blog geo` (מנוע בלוג)
- **fallback גנרי**: `claude-seo:seo-geo`

### תוכן סושיאל (3 כלים — לפי מטרה)
- **פוסט בודד בקול של רון** → `social-post-generator` agent
- **לוח תוכן 30 ימים בעברית** → `anthropic-skills:israeli-social-content`
- **קמפיין שיווקי גנרי** → `market-social`

### UI: דף נחיתה vs אפליקציה
- **דף נחיתה HTML** → `landing-page-builder` (כולל RTL מובנה)
- **אפליקציה React מורכבת** → `fullstack-app` + `anthropic-skills:israeli-ui-design-system` (RTL design system)

### המרת HTML → PDF/DOCX
לאחר ron-digital-quote (HTML), אם הלקוח רוצה PDF/DOCX → `anthropic-skills:hebrew-document-generator` להמרה.

### וידאו hero בדף נחיתה (NEW capability)
לפרויקטי landing-page-builder גדולים — שאל לפני: "האם להוסיף וידאו hero? +30-50% conversion, תוספת ₪500-1,500"
- כן → `anthropic-skills:hyperframes-best-practices` (HTML+GSAP בעברית RTL)

### אוטומציות בסיום פרויקט
- **לפני שליחה ללקוח** — תמיד `simplify` לניקוי הקוד
- **לפני כתיבת פרומפט** — תמיד `prompt` לשליפה מ-NotebookLM

### סנכרון/הפצה של Skills (3 כלים — אין חפיפה)
- **סקיל לטלפון / claude.ai** → `skills-to-phone` (אורז סקיל מקומי ל-zip תקין להעלאה ל-claude.ai. מתקן backslash, SKILL.md כפול, frontmatter רב-שורתי)
- **סנכרון ללפטופ (Claude Code)** → `/sync-skills` (git push ל-github.com/ronsab/claude-skills)
- **יצירת סקיל חדש מאפס** → `skill-creator`
- **מפת הסקילים HTML** → `skill-map`

בכל פעם שמשימה רלוונטית ל-Skill, הפעל אותו אוטומטית ללא שאלה.

## Agents זמינים
- `landing-page-reviewer` -- בדיקת איכות דף נחיתה לפני שליחה ללקוח (SEO, RTL, CTA, מובייל)
- `client-briefer` -- ממיר שיחת לקוח גולמית למפרט מובנה
- `social-post-generator` -- כתיבת פוסטים ברשתות חברתיות בקול של רון

## Slash Commands זמינים
- `/new-client` -- פתיחת לקוח חדש: חיפוש Pinecone → אפיון → CLAUDE.md → הצעת מחיר
- `/save-client` -- שמירת לקוח שהסתיים ב-Pinecone
- `/deploy` -- העלאת דף נחיתה ל-Vercel + קבלת URL ציבורי
- `/review-page` -- audit מלא לדף נחיתה לפני שליחה (SEO, RTL, CTA, מובייל)
- `/update-map` -- ריענון מפת הסקילים בדסקטופ

## מפת הסקילים (מערכת חיה)
`~/.claude/skill-map/` מייצר את `Desktop/skill-map.html`.
- `generate-map.mjs` -- סורק כל הסקילים/commands/agents, ממזג עם ידע עסקי, בונה HTML
- `skill-map-data.json` -- **single source of truth** לידע עסקי (קטגוריות, הזדמנויות, decision rules, conflicts). ערוך כאן כדי להעשיר סקיל
- כל סקיל חדש מתווסף אוטומטית לשכבת "ספרייה מלאה". לקידום לשכבה העסקית: הוסף entry ב-`skill-map-data.json`
- המפה כוללת: אשף החלטה ("איזה סקיל מתי"), הזדמנות השבוע, Cheat Sheet, חיפוש, סתירות
- ריענון: `/update-map` ידני. אוטומציה מלאה ב-SessionStart דורשת hook ב-settings.json (ראה skill-map/run-map.sh)

## כלים מיוחדים — הפעלה אוטומטית
- **context7**: בעת כתיבת HTML/CSS/JS עם ספריות (Three.js, GSAP, Tailwind) — השתמש ב-context7 לתיעוד עדכני
- **Firecrawl**: כשלקוח מביא URL לאתר קיים שלו — סרוק אותו עם firecrawl לפני בנייה
- **Playwright**: אחרי בניית דף נחיתה — הפעל playwright לצילום screenshot ובדיקת מובייל

## Pinecone — זיכרון לקוחות
לפני כל עבודה על לקוח חדש (אפיון, דף נחיתה, תוכן שיווקי):
1. הפעל `ron-client-search` אוטומטית
2. חפש לקוחות דומים לפי תחום
3. הצג ממצאים רלוונטיים לפני שמתחילים

אחרי השלמת עבודה עם לקוח -- שאל: "האם לשמור את הלקוח הזה ב-Pinecone?" ואם כן, הפעל `/save-client`.

## Auto Memory Consolidation
מטופל אוטומטית ע"י SessionStart hook ב-`settings.json` שמפעיל את `~/.claude/skills/dream/session-start-dream.sh`. אין צורך בפעולה ידנית.

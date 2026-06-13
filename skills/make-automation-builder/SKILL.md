---
name: make-automation-builder
description: >
  סקיל קאנוני (CANONICAL) של רון לבניית אוטומציות ב-Make.com — מתכנן ובונה אוטומציות מאפס עד blueprint מאומת.
  Use when the user asks to build, create, set up, fix, or design any Make.com automation, scenario, or workflow.
  Also when connecting apps, setting up webhooks, working with data stores, or scheduling automations.
  השתמש בסקיל זה גם כשרון: רוצה לבנות או לתכנן אוטומציה, שואל "איך אני מחבר X ל-Y", אומר שהוא לא יודע מאיפה להתחיל,
  רוצה לאוטמט תהליך כלשהו (Gmail, WhatsApp, Twilio, Zoom, Google Sheets, Webhooks), מבקש blueprint או מיפוי מודולים.
  פרטי משתמש: Team ID 2341960, Org ID 4698040, אזור eu2.make.com, Connection ID Gmail: 13833758.
  כולל: validation pipeline (6 שלבים), error correction (max 3 retries), 5 ready blueprints, ידע מאומת על Gmail
  (שמות מודולים, שדות, Label IDs, Router structure), מגבלות MCP, מגבלות פלאן.
  **תמיד להעדיף סקיל זה על-פני anthropic-skills:make-automation-builder.**
---

# Make Automation Builder

## Overview

Guides Claude through building Make.com automations end-to-end using the Make MCP server.

**Core principle: Always validate before creating. Never call `scenarios_create` without running the full 6-step validation pipeline first.**

---

## Account Quick Reference

| Key | Value |
|-----|-------|
| Team ID | `2341960` |
| Org ID | `4698040` |
| Region | EU2 |
| Timezone | `Asia/Jerusalem` |
| User | ronsabon@gmail.com |

### Known Connections
| App | Connection ID |
|-----|--------------|
| Gmail (google-email) | 13833758 |
| Google Sheets/Drive | 13833768 |
| OpenAI | 13836712 |

### App Versions
```
google-email@4    google-sheets@2    google-drive@4
slack@4           telegram@1         http@4
gateway@1         json@1             builtin@1
openai-gpt-3@1    anthropic-claude@1 whatsapp-business-cloud@1
```

> For any app not listed: call `connections_list(teamId: 2341960)` to check if it's connected.

---

## Core Workflow

```
Step 1: users_me()                             → confirm auth
Step 2: apps_recommend(intention)              → find relevant apps
Step 3: connections_list(teamId: 2341960)      → verify connections exist
Step 4: app-modules_list(orgId, app, version)  → discover modules
Step 5: app-module_get(format: "instructions") → get config requirements
Step 6: [Ask user] for missing IDs             → spreadsheet IDs, channel names, etc.
Step 7: VALIDATION PIPELINE (6 steps)         → must pass all 6
Step 8: scenarios_create(teamId, blueprint, scheduling)
Step 9: [If error] ERROR CORRECTION PIPELINE  → max 3 retries
Step 10: scenarios_activate(teamId, scenarioId) → only after user confirms
```

---

## Validation Pipeline (Run Before Every Create)

**Step 1 — Connection Verification**
All required apps have active connections in `connections_list`. No connection = stop and inform user.

**Step 2 — Module Existence**
All `module` fields in blueprint match `app-modules_list` for the given app version.
Format: `appName:moduleName` (e.g., `google-email:ActionSendEmail`)

**Step 3 — Module Config Validation**
For each module call `validate_module_configuration(orgId, module, parameters, mapper)`.
Fix any mapping errors before proceeding.

**Step 4 — Blueprint Structure**
Call `validate_blueprint_schema(blueprint)`.
- Module IDs must be unique integers (start from 1)
- Trigger module must be first (id: 1)
- All routes must be connected

**Step 5 — Scheduling**
Call `validate_scheduling_schema(scheduling)` if using a scheduled trigger.
Use `enums_timezones()` to get Asia/Jerusalem timezone string.

**Step 6 — RPC Fields**
If any module uses dynamic dropdowns (folder pickers, label selectors, etc.), call `rpc_execute(orgId, module, rpc, parameters)` to verify valid values.

---

## Error Correction Pipeline

If `scenarios_create` returns an error:
1. Parse error message → identify which module/field failed
2. Categorize: `connection` | `module_name` | `config` | `structure`
3. Fix the specific node only
4. Re-run validation from Step 3
5. Retry `scenarios_create`
6. **Max 3 attempts** — if still failing, report to user with diagnosis

---

## Common Patterns

### Webhook Trigger
```
1. hooks_create(teamId, name, type: "web") → get hook URL
2. hook-config_get(hookId) → verify receiving
3. Use hookId in blueprint trigger: gateway:CustomWebHook
4. Share URL with user so they can connect their source
```

### Data Store
```
1. data-structures_create(teamId, name, spec) → define schema
2. data-stores_create(teamId, name, dataStructureId) → create store
3. Use storeId in scenario modules (builtin:DataStoreSearchRecords, etc.)
```

### Scheduled Trigger
```
1. enums_timezones() → confirm "Asia/Jerusalem" string
2. Build scheduling object: { type: "INTERVAL", interval: N }
   or: { type: "CRON", expression: "0 9 * * 1-5" }
3. validate_scheduling_schema(scheduling) before create
```

### Monitoring a Scenario
```
executions_list(teamId, scenarioId, limit: 10)
  → if failed: executions_get_detail(executionId) → shows exact module + error
```

---

## Blueprint Module Template

```json
{
  "id": 1,
  "module": "appName:ModuleName",
  "version": 1,
  "parameters": {
    "__IMTCONN__": <connectionId>
  },
  "mapper": {
    "fieldName": "{{value}}"
  },
  "metadata": {
    "designer": { "x": 0, "y": 0 }
  }
}
```

**IML Mapping syntax:** `{{1.fieldName}}` = output from module with id 1

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing `teamId` in tool call | Always pass `teamId: 2341960` |
| Wrong app version | Use the Known App Versions table above |
| Missing `__IMTCONN__` in parameters | Every authenticated module needs connection ID |
| Duplicate module IDs | IDs must be unique integers: 1, 2, 3... |
| Skipping validation | NEVER skip — run all 6 steps every time |
| Activating without asking user | Always ask before calling `scenarios_activate` |
| `orgId` vs `teamId` confusion | `app-modules_list`, `validate_*`, and `rpc_execute` use `orgId: 4698040`; scenario/hook/data-store operations use `teamId: 2341960` |

---

## תהליך אינטראקטיבי עם רון (בעברית)

### שלב 0: Discovery — לפני שנוגעים ב-Make

**תמיד** אסוף 4 נקודות לפני כל בנייה:

1. **טריגר** — מה מפעיל את האוטומציה? (מייל / הודעה / טופס / webhook / לו"ז)
2. **פעולות** — מה צריך לקרות? (לאיזה אפליקציה? מה הפלט?)
3. **תנאים** — מתי *לא* לרוץ? (פילטרים, תנאי if/else)
4. **נתונים** — אילו שדות עוברים? (שמות, סכומים, תאריכים, קבצים)

**אם חסר מידע — שאל נקודתית. לא לנחש.**

### שלב 1: שרטוט Flow (תמיד לפני Make)

הצג את הלוגיקה בפורמט זה ובקש אישור:

```
[TRIGGER] מה מתחיל הכל?
    ↓
[FILTER?] האם רלוונטי? (אם יש תנאי)
    ↓
[ACTION 1] פעולה ראשונה
    ↓
[ACTION 2] פעולה שנייה
    ↓
[ROUTER?] פיצול לתרחישים שונים (אם יש)
    ├── [מסלול A]
    └── [מסלול B]
```

**אל תמשיך לבנייה לפני שרון אישר את ה-flow.**

### כללי עבודה עם רון

- **לא לנחש** — אם לא ברור, שאל נקודתית
- **הסבר את ה"למה"** — "אנחנו משתמשים ב-Router כי יש שתי תוצאות אפשריות"
- **אם נתקע** — חזור לשלב 0, שאל: "מה קורה כרגע? מה רצית שיקרה?"
- **פלט ברירת מחדל** — תמיד הפק Blueprint טבלה + הוראות צעד אחר צעד
- **בסוף כל תרחיש** — שאל: "יש משהו לשנות? רוצה שאפיק את זה כמסמך?"

---

## Trigger-to-Module Mapping (מהיר)

| טריגר | Module |
|---|---|
| מייל נכנס | Gmail › Watch Emails (`google-email:triggerWatchNewEmails`) |
| הודעת WhatsApp | Twilio › Watch SMS / WhatsApp Business Cloud |
| טופס מולא | Typeform / Tally › Watch Responses |
| Webhook חיצוני | Webhooks › Custom Webhook (`gateway:CustomWebHook`) |
| לו"ז קבוע | Make › Scheduled |
| שורה חדשה ב-Sheets | Google Sheets › Watch Rows |
| הודעת Slack | Slack › Watch Messages |

---

## מינוח בסיסי בעברית

| מונח | הסבר |
|---|---|
| Scenario | התרחיש כולו — כל הקופסות |
| Module | קופסה אחת — פעולה אחת |
| Trigger | קופסה ראשונה — מה מפעיל הכל |
| Webhook | כתובת URL שמקבלת נתונים מבחוץ |
| Router | צומת — מפצל למסלולים לפי תנאי |
| Filter | שומר — מחליט אם להמשיך |
| Iterator | מפרק רשימה לפריטים בודדים |
| Aggregator | מאחד כמה פריטים לאחד |
| Bundle | חבילת נתונים שעוברת בין מודולים |
| Data Store | בסיס נתונים קל בתוך Make |
| Error Handler | מטפל בשגיאות — נמנע מ-crash |

---

## תרחישים מוכנים — Blueprints קנוניים

### תרחיש א: עיבוד קבלות/חשבוניות מ-Gmail
```
Gmail › Watch Emails (filter: has:attachment)
    ↓
OpenAI › Create Message (חלץ: ספק, סכום, תאריך, מספר חשבונית)
    ↓
JSON › Parse JSON
    ↓
Google Sheets › Add Row
    ↓
Gmail › Send Email (אישור עיבוד לשולח)
```

### תרחיש ב: WhatsApp Bot עם Twilio
```
Webhooks › Custom Webhook
    ↓
Router
    ├── [מחיר] → OpenAI › Generate reply → Twilio › Send SMS
    ├── [תור] → Google Calendar › Check availability → Twilio › Send SMS
    └── [אחר] → Twilio › Send SMS (ברירת מחדל)
```

### תרחיש ג: סיכום פגישות Zoom / Fireflies
```
Fireflies › Watch Transcripts (webhook)
    ↓
OpenAI › Summarize + Extract action items
    ↓
Google Sheets › Add Row (סיכום + משימות)
    ↓
Gmail › Send Email (לכל משתתף)
```

### תרחיש ד: ליד חדש מטופס → CRM + הודעה
```
Tally/Typeform › Watch Responses
    ↓
HubSpot › Create Contact
    ↓
Gmail › Send Email (ברוך הבא ללקוח)
    ↓
Slack › Send Message (התראה פנימית לצוות)
```

### תרחיש ה: ניקוי תיבת Gmail (Blueprint מאומת ✅)
```
[לו"ז יומי]
    ↓
Gmail › Search Emails (query: "in:inbox is:unread older_than:30d -is:starred", maxResults: 50)
    ↓
Gmail › Update Email Labels (addLabelIds: [תווית], removeLabelIds: ["INBOX"])
```

---

## ידע טכני מאומת — Gmail ב-Make (נצבר מניסיון אמיתי ✅)

> ⚠️ הסעיף הזה מכיל שמות שדות ומודולים שאומתו בפועל ב-Make. לא להמציא שמות — השתמש רק בנ"ל.

### שמות מודולים מאומתים (google-email)

| פעולה | שם מודול מדויק |
|---|---|
| Watch new emails (trigger) | `google-email:triggerWatchNewEmails` |
| Search emails | `google-email:executeEmailSearchQuery` |
| Update email labels | `google-email:updateEmailLabels` |
| Delete email | `google-email:deleteAnEmail` |
| Send email | `google-email:sendAnEmail` |
| Create draft | `google-email:createADraft` |
| Router | `builtin:BasicRouter` |

**גרסת מודולים:** תמיד השתמש ב-`"version": 4` עבור מודולי google-email.

### שדות מאומתים — updateEmailLabels

```json
{
  "messageId": "{{1.id}}",
  "addLabelIds": ["Label_XXXX"],
  "removeLabelIds": ["INBOX"]
}
```

**לא** `labelId`, **לא** `add_labels` — אלא בדיוק `messageId`, `addLabelIds`, `removeLabelIds`.

### שדות מאומתים — executeEmailSearchQuery

```json
{
  "query": "in:inbox is:unread older_than:30d -is:starred",
  "maxResults": 50
}
```

### שדות מאומתים — sendAnEmail

```json
{
  "to": "email@example.com",
  "subject": "נושא המייל",
  "content": "תוכן המייל",
  "contentType": "text/plain"
}
```

### תחביר פילטרים ב-Router

```json
// בדיקת regex על subject (case-insensitive):
{"a": "{{1.subject}}", "b": "spam|offer|free money", "o": "text:matchCI"}

// בדיקה אם label קיים ברשימת labels של המייל:
{"a": "{{1.labelIds}}", "b": "CATEGORY_SOCIAL", "o": "array:contains"}
```

**אופרטורים שימושיים:** `text:matchCI` (regex), `array:contains`, `text:equal`, `number:greater`

### Label IDs — Gmail של רון

| תווית | ID |
|---|---|
| לסקירה (custom) | `Label_1454074671965790386` |
| INBOX | `INBOX` |
| סושיאל | `CATEGORY_SOCIAL` |
| פרומושנס | `CATEGORY_PROMOTIONS` |

**כדי לקבל Label ID של תווית מותאמת אישית:** השתמש ב-MCP `gmail_list_labels`.

### פורמט Scheduling (Blueprint JSON)

```json
{"type": "indefinitely", "interval": 86400}   // כל יום (24 שעות)
{"type": "indefinitely", "interval": 3600}    // כל שעה
{"type": "indefinitely", "interval": 900}     // כל 15 דקות
```

### Blueprint JSON — מבנה בסיסי מאומת

```json
{
  "name": "שם הסצנריו",
  "flow": [
    {
      "id": 1,
      "module": "google-email:executeEmailSearchQuery",
      "version": 4,
      "parameters": {"__IMTCONN__": 13833758},
      "mapper": {
        "query": "in:inbox is:unread older_than:30d -is:starred",
        "maxResults": 50
      },
      "metadata": {"designer": {"x": 0, "y": 0}}
    },
    {
      "id": 2,
      "module": "google-email:updateEmailLabels",
      "version": 4,
      "parameters": {"__IMTCONN__": 13833758},
      "mapper": {
        "messageId": "{{1.id}}",
        "addLabelIds": ["Label_1454074671965790386"],
        "removeLabelIds": ["INBOX"]
      },
      "metadata": {"designer": {"x": 300, "y": 0}}
    }
  ],
  "metadata": {
    "instant": false,
    "version": 1,
    "scenario": {
      "roundtrips": 1,
      "maxErrors": 3,
      "autoCommit": true,
      "autoCommitTriggerLast": true,
      "sequential": false,
      "confidential": false,
      "dataloss": false,
      "dlq": false,
      "freshVariables": false
    }
  }
}
```

**`__IMTCONN__`** = Connection ID של חשבון Google של רון: `13833758`

### מבנה Router עם routes ב-Blueprint

הראוטר שונה ממודולים רגילים — ה-routes מוטמעים בתוך האובייקט שלו, **לא** כמודול נפרד:

```json
{
  "id": 2,
  "module": "builtin:BasicRouter",
  "version": 1,
  "parameters": {},
  "mapper": null,
  "metadata": {"designer": {"x": 300, "y": 0}},
  "routes": [
    {
      "flow": [
        {
          "id": 3,
          "module": "google-email:deleteAnEmail",
          "version": 4,
          "parameters": {"__IMTCONN__": 13833758},
          "mapper": {"messageId": "{{1.id}}"},
          "filter": {
            "name": "ספאם",
            "conditions": [[
              {"a": "{{1.subject}}", "b": "spam|prize|winner", "o": "text:matchCI"}
            ]]
          },
          "metadata": {"designer": {"x": 600, "y": -200}}
        }
      ]
    },
    {
      "flow": [
        {
          "id": 4,
          "module": "google-email:updateEmailLabels",
          "version": 4,
          "parameters": {"__IMTCONN__": 13833758},
          "mapper": {
            "messageId": "{{1.id}}",
            "addLabelIds": [],
            "removeLabelIds": ["INBOX"]
          },
          "filter": {
            "name": "סושיאל",
            "conditions": [[
              {"a": "{{1.labelIds}}", "b": "CATEGORY_SOCIAL", "o": "array:contains"}
            ]]
          },
          "metadata": {"designer": {"x": 600, "y": 50}}
        }
      ]
    }
  ]
}
```

---

## מגבלות MCP של Make (eu2.make.com)

כאשר בונים סצנריות דרך MCP — לא הכל עובד. לדעת זאת מראש חוסך זמן:

| פעולה MCP | סטטוס | הערה |
|---|---|---|
| `scenarios_create` | ✅ עובד | הדרך הראשית ליצירת סצנריות |
| `scenarios_list` | ✅ עובד | |
| `scenarios_get` | ✅ עובד | |
| `scenarios_run` | ✅ עובד | |
| `scenarios_delete` | ❌ חסום | "Forbidden to use token authorization" — מחק ידנית |
| `scenarios_activate` | ❌ חסום | הפעל ידנית דרך הטוגל בממשק |
| `scenarios_deactivate` | ❌ חסום | כבה ידנית דרך הטוגל בממשק |
| `validate_module_configuration` | ❌ חסום | |
| `app-module_get` | ❌ חסום | |

**מסקנה:** יצירת סצנריות — דרך MCP. הפעלה/השבתה/מחיקה — חייב ידנית בדפדפן.

---

## מגבלות פלאן ב-Make

| פלאן | סצנריות פעילות | מחיר משוער |
|---|---|---|
| Free | **2 בלבד** | $0 |
| Core | ללא הגבלה מעשית | ~$9/חודש |
| Pro | ללא הגבלה | ~$16/חודש |

אם קיבלת שגיאה "Maximum number of active scenarios has been exceeded" — הפלאן מלא.
פתרון: כבה סצנריו קיים, או שדרג פלאן.

---

## הוראות בנייה ידנית ב-Make (כשרון רוצה לבנות בעצמו)

תן הוראות ספציפיות ומספוריות:

```
1. כנס ל-eu2.make.com > Scenarios > Create a new scenario
2. לחץ "+" > חפש [שם האפליקציה]
3. בחר את המודול [שם המודול]
4. חבר את החשבון (אם לא מחובר — לחץ Add > אשר הרשאות)
5. הגדר שדות:
   - [שדה 1]: [מה להכניס]
   - [שדה 2]: [מה להכניס]
6. לחץ OK > הוסף מודול הבא עם "+"
```

### Checklist בדיקה לפני הפעלה

```
□ לחץ "Run once" — בדוק V ירוק על כל מודול
□ אם יש שגיאה — לחץ על המודול האדום, קרא את ההודעה
□ וודא שה-Sheets / מייל / Webhook קיבלו את הנתונים הנכונים
□ הפעל Scheduling אם האוטומציה אמורה לרוץ לפי לו"ז
□ שים לב: בפלאן החינמי מותרות רק 2 סצנריות פעילות בו-זמנית
□ הפעלה/השבתה חייבת להיעשות ידנית בדפדפן (MCP לא תומך בזה)
```

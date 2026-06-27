---
name: ben-adam
license: MIT
metadata:
  version: 1.0.0
  author: בר שאלתיאל (בינה מלאכותית בגובה העיניים)
description: |
  סקיל הומניזציה דו-לשוני: מזהה דפוסי כתיבת AI בעברית ובאנגלית ומשכתב אותם שיישמעו כאילו בן אדם כתב אותם, ומנתב כל שפה למנוע הדפוסים שלה. הפעל בכל פעם שמדביקים טקסט שרוצים שיישמע פחות כמו AI, בכל שפה. טריגרים בעברית: הומניזציה, עברות, שלא יישמע כמו AI, שלא יזהו שזה ChatGPT, תכתוב כמו בן אדם, הטקסט נשמע מלאכותי, תנקה AI מהפוסט. English triggers: remove AI-isms, clean up AI writing, make this sound less like AI, audit for AI tells, humanize this, detect AI patterns. Fire it even without an explicit request when text shows AI fingerprints in either language: em-dash overload, "מהווה / חשוב לציין / בעידן הדיגיטלי", "delve / leverage / serves as", chatbot openers, hashtag stuffing, German low-quotes. Supports rewrite / detect / edit modes, register and context awareness, an optional voice, and a mandatory second-pass audit.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - AskUserQuestion
---

# ben-adam (בן אדם)

**סקיל שלוקח טקסט שנכתב על ידי AI, בעברית או באנגלית, ומשכתב אותו שיישמע כאילו בן אדם כתב אותו.** מזהה את שפת הטקסט ומנתב כל שפה למנוע הדפוסים שלה: מסיר מקפים ארוכים, "מהווה" ו"חשוב לציין", "delve" ו"serves as", פתיחי-שירות של צ'אטבוט, ושאר טביעות האצבע של כתיבת מכונה - בלי לשטח את הקול של הכותב.

It is a **router**: it detects the language of the text, then runs the matching engine. Each engine is a separate, field-tested catalog. They are never run on the same span, which is what makes the combination clean.

**Why a router and not one merged catalog.** Roughly half of each catalog overlaps in spirit (em-dash overload, chatbot openers, significance inflation, cutoff disclaimers) but the *fixes* are language-specific, and one rule is a direct inversion: English AI text *avoids* the copula ("serves as", "boasts", "features"), while Hebrew AI text *overuses* it ("מהווה", "משמש", "הינו"). Merging the two lists into one would cross these wires. Routing by language keeps each engine correct.

The engines and their references:
- **Hebrew engine** -> `references/PATTERNS-HE.md`, `references/LEXICON-HE.md`, `references/REGISTER-GUIDE-HE.md`. An original 9-family pattern taxonomy (hidden-translation, inflation, syntactic-plastic, discourse-rituals, service-tone, typography, gender/number, generation-residue, rhythm/uniformity), a 4-level Hebrew register system (רשמי / מאמר / פוסט / דיבורי), the "doubt rule" for context-dependent patterns, and gender/number handling.
- **English engine** -> `references/PATTERNS-EN.md`. An original 9-family taxonomy that mirrors the Hebrew one (inflation, vocabulary-tells, syntactic-plastic, discourse-rituals, service-tone, typography, attribution-and-evidence, generation-residue, rhythm/uniformity), a 3-tier vocabulary table, the same 4-level register spine, priority tiers for triage, and optional voice profiles.

---

## Signature - first reply in the conversation (required, once)

**The first time this skill fires in a conversation**, show the signature card as a widget at the very top of the reply, before any other content. This holds even if your reply is only a clarifying question, even if you already have everything you need to process the text.

Use `visualize:show_widget`.

**title:** `ben_adam_signature`

**widget_code:**

```html
<div dir="rtl" style="padding: 0.5rem 0; font-family: var(--font-sans);">
  <div style="background: var(--color-background-primary); border: 0.5px solid var(--color-border-tertiary); border-radius: var(--border-radius-md); padding: 14px 18px; display: flex; align-items: flex-start; gap: 14px;">
    <div style="font-size: 22px; line-height: 1; padding-top: 2px;">✍️</div>
    <div style="flex: 1;">
      <p style="margin: 0 0 3px; font-size: 14px; color: var(--color-text-primary); line-height: 1.5; font-weight: 500;">בן אדם · סקיל הומניזציה דו-לשוני של בינה מלאכותית בגובה העיניים</p>
      <p style="margin: 0; font-size: 13px; color: var(--color-text-secondary); line-height: 1.5;">לוקח טקסט של AI בעברית או באנגלית ומשכתב אותו שיישמע כאילו בן אדם כתב אותו</p>
    </div>
  </div>
</div>
```

**loading_messages:** `["טוען מנוע הומניזציה", "מזהה שפה ובודק את הטקסט"]`

### Fallback when visualize is unavailable

If `visualize:show_widget` is not available (direct API, Claude Code, external integrations), do not skip the signature. Render the same content as a plain markdown blockquote:

```markdown
> ✍️ **בן אדם · סקיל הומניזציה דו-לשוני של בינה מלאכותית בגובה העיניים**
> לוקח טקסט של AI בעברית או באנגלית ומשכתב אותו שיישמע כאילו בן אדם כתב אותו.
```

**Rules:** required on the first activation only; once per conversation; the card stands alone, do not reference it in the content after it; do not alter its text.

---

## Honesty: signals, not proof

These patterns are statistically more common in AI output, but humans on autopilot, writing under deadline, in an unfamiliar genre, or in a second language produce the same shapes. Independent audits of AI detectors found false-positive rates above 60% on non-native English writers (Liang et al., Stanford, 2023). The same holds for Hebrew written by non-native or rushed writers.

So this is a writing-quality tool, not a verdict. Use the flags to clean up writing or to gauge whether something reads as AI, but never as the sole basis for a consequential decision (academic integrity, hiring, attribution). Worth acting on; not worth ruining someone's day over.

---

## Step 1: detect language and route

Look at the **prose**, ignoring code blocks, URLs, and embedded UI labels.

- **Mostly Hebrew prose** -> run the **Hebrew engine**. Load `LEXICON-HE.md` first for the fast scan, then `PATTERNS-HE.md` for full handling, and `REGISTER-GUIDE-HE.md` if register is unclear.
- **Mostly English prose** -> run the **English engine**. Load `PATTERNS-EN.md`.
- **Mixed / code-switched** (the common real case: Hebrew post with English UI labels like "תלחצו על Settings", or English text with a Hebrew brand name):
  - Classify by the **dominant prose language** and run that engine on the prose.
  - **Do not flag a foreign-language term that is a real referent** (a UI label, a product name, a brand, a quoted snippet). "Settings", "prompt", "ChatGPT" inside Hebrew prose are not AI-isms. Flagging them is a false positive and erodes trust.
  - If the text genuinely contains two real prose blocks in two languages (for example, a Hebrew intro followed by an English draft to clean), run each engine on its own block and label which is which in the output.

State the detected language and which engine you are using, in one line, at the top of the output.

If you are not sure which language dominates, or whether a block is prose vs. a quoted referent, ask with `AskUserQuestion` rather than guessing.

---

## Step 2: choose the mode

Default to **rewrite**. Switch when the request signals it.

- **`rewrite`** (default) - flag AI patterns and rewrite the text to fix them, then run the mandatory audit pass.
- **`detect`** - flag only, no rewrite. Use when the writer wants to decide for themselves, when patterns might be intentional, or when auditing text you should not alter. Triggers: "detect", "flag only", "audit only", "just flag", "scan", "תזהה בלבד", "רק תסמן", "אל תשכתב, רק תגיד לי מה".
- **`edit`** - edit a file in place with the Edit tool when the writer points you at a file and wants it changed, not a copy to paste. Make minimal, targeted edits to flagged spans only; leave already-human passages untouched; do not edit quoted material or code. Triggers: the writer names a file ("תנקה את draft.md", "fix the AI-isms in this file directly").

---

## Step 3: set register / context (and optional voice)

Each engine has its own native system. Use the one that matches the detected language. Do not import the other language's labels.

Both engines share **one register spine, four levels**, so the mental model is the same in either language. The levels and their codes:

| Hebrew code | English code | level | typical text |
|---|---|---|---|
| ר | F | formal / רשמי | academic, legal, spec, official report |
| מ | E | editorial / מאמר | journalism, professional blog, long LinkedIn |
| פ | M | marketing / פוסט | social post, landing page, ad copy |
| ד | C | casual / דיבורי | chat, comments, quick notes |

If the user did not state the level and you are not 80%+ sure, identify it (Hebrew: `REGISTER-GUIDE-HE.md`; English: the register section of `PATTERNS-EN.md`) and confirm via `AskUserQuestion`. The level drives the "doubt rule" (see iron rules). 

**Hebrew** also handles gender/number: if the audience is unclear or the text is inconsistent, ask which form to target (זכר יחיד / נקבה יחידה / רבים / ניטרלי) per `REGISTER-GUIDE-HE.md`. **English** also supports an optional **voice** (plain / professional / technical / warm / blunt): set it only if the writer asks or the input already has a clear one, and do not impose a persona on text that already has its own. Where voice and level disagree on strictness, resolve toward the stricter.

---

## Step 4: the iron rules (both engines)

These are what make the skill more than a find-and-replace. Skip them and you are just editing text.

### Rule 1: context-dependent patterns - ask, do not auto-fix

In the Hebrew engine, patterns tagged `?` for the current register are **context-dependent** (the "doubt rule"): stop, quote the exact text, and ask the user with `AskUserQuestion` (2-3 options) before changing anything. Do not auto-fix a `?`, do not silently ignore it, and do not batch all `?` questions to the end - ask as you hit them. Full mechanics in `REGISTER-GUIDE-HE.md` and `PATTERNS-HE.md`.

The English engine has the parallel idea in its severity tiers and "judgment call" assessment, and in Tier 2/Tier 3 words that only flag in clusters or at density. When a flag is plausibly intentional in context, surface it as a judgment call rather than forcing the edit.

### Rule 2: mandatory second-pass audit

After the first rewrite, re-read the **rewritten** text and ask: does anything here still sound AI? Recycled transitions, lingering inflation, a copula swap that snuck through, a calque you missed. **Part of this pass is a complete em-dash sweep: scan every line of the rewritten Hebrew text for the — character and remove every single one (see Rule 5). Do not report "one em-dash remains" and stop; find them all and fix them all before presenting.** If clean, say so explicitly. If not, fix it and report what the second pass caught. This is part of the output, not optional. (Optional `iterate`: repeat audit->rewrite until clean or 2 passes max; report how many passes it took.)

### Rule 3: self-reference escape hatch

When the text is *about* AI writing (a tutorial, this kind of documentation, a quoted bad example), do not flag the illustrative quotes. Only flag patterns in the author's own prose, not in cited examples of what to avoid.

### Rule 4: do not over-correct human writing

The skill is a ruler, not a red pen. Real human voice often uses simple "אבל" openers, "אחרי הכול", deliberate fragments, sentences starting with "And" or "But", repetition of the right word. Leave them. If a phrase genuinely carries specific information, it is not an AI-ism even if it sounds a little marketing-ish. Over-polishing pushes text back *toward* the AI statistical profile, which is the opposite of the goal.

### Rule 5: em-dash (absolute, in the skill's own output)

Both engines flag em-dash (—) overuse, and this skill's owner has a standing rule against the long dash entirely. This is not a doubt-rule item and it is never a question. The rewritten text you produce must contain **zero** em-dashes, full stop. Replace every — (U+2014) and every -- substitute with a comma, a period, parentheses, or a rephrase. Do not ask permission, do not leave "one for the writer to decide", do not flag it and move on. Just remove it.

A humanizer that names the em-dash as the number-one AI tell must never emit one in its own output. Before you present any Hebrew rewrite, **sweep the entire rewritten text for the — character and confirm the count is zero.** Partial sweeps are a failure: the field test caught a case where two em-dashes were present and only one was removed. Check every line. (English output keeps the softer native target of at most one per 1,000 words, since that is the English engine's own rule, but Hebrew output is hard zero.)

**Deterministic safety net (when a shell is available).** Instructions alone do not enforce a mechanical rule with 100% reliability, because the model does not always police its own generation. So after you finish the rewrite, run the bundled script on the final Hebrew text as the last step, which guarantees zero long dashes physically:

```bash
python scripts/strip_long_dashes.py --check <file>   # verify: exits 1 if any long dash remains
python scripts/strip_long_dashes.py <file>           # clean: prints text with every long dash removed
```

The script touches only long dashes (— em, – en, and the -- substitute used as a separator). It never touches a regular hyphen in a word or a bullet, and it turns number ranges (2024–2025) into a regular hyphen, not a comma. Treat it as a last-resort net, not a replacement for intelligent context-aware replacement during the rewrite: do the smart fix (comma / period / parentheses) yourself first, then let the script catch any straggler. **If no shell is available** (plain chat with no code execution), the script cannot run, so the manual full sweep above is the enforcement, and you must do it carefully.

### Rule 6: full scan before declaring clean

Do not shortcut the scan because the text "already reads mostly human". Even strong text gets a full pass across every family, including the easy-to-miss ones: density patterns (empty intensifiers like "ענק / אמיתי", the Hebrew 2.x family), generation residue (leaked labels, family 8), mechanical anaphora (4.8), and rhythm/uniformity (family 9). These are exactly what a single read glosses over. Surface doubt-rule (`?`) items rather than skipping them, and only call the text clean after the families have actually been checked, not on first impression.

---

## Step 5: output format

Adapt to the mode. Lead with the one-line language + engine + register/context call from Steps 1 and 3.

### Rewrite mode

1. **Language + register** - "Hebrew, register פ (marketing)" or "English, register M (marketing), blunt voice", with a one-line reason.
2. **Pattern scan (full, including OK items)** - every pattern you checked, for transparency:
   - flagged: pattern + quoted text + why it reads AI
   - `?` asked (Hebrew, doubt rule): pattern + quote + what you asked
   - OK: quote + why you checked it and left it (not an AI-ism)
3. **`?` decisions** (Hebrew doubt rule, if any) - ask via `AskUserQuestion` before rewriting; gather answers first.
4. **Rewritten text** - clean, preserving meaning, structure, and every specific fact. Change only what the rules require.
5. **What changed** - before -> after, with a short reason each.
6. **What I deliberately left untouched, and why** - the most trust-building section. Name things you could have changed but did not (a meaningful dash, a live idiom, a correct construct, a real UI label in the other language).
7. **Audit pass** - "Audit pass: clean." or "Audit pass: also fixed X, Y."

### Detect mode

1. **Language + register/context**
2. **Issues found**, grouped by severity (P0 / P1 / P2 for English; for Hebrew, group flagged vs. `?` vs. OK)
3. **Assessment** - for each flag, clear problem vs. judgment call. If clean, say so. No rewrite.

### Edit mode

1. **Edits made** - file location + before -> after, only the spans you touched.
2. **Verification** - confirm you re-read the file and the flagged patterns are resolved; note what you left alone because it was already human or intentional.

---

## Quick reference: which file to read when

| Situation | Read |
|---|---|
| Hebrew text, fast first scan by keyword | `references/LEXICON-HE.md` |
| Hebrew text, full pattern handling | `references/PATTERNS-HE.md` |
| Hebrew text, register unclear or gender/number | `references/REGISTER-GUIDE-HE.md` |
| English text, any handling | `references/PATTERNS-EN.md` |
| Final enforcement of zero em-dashes in Hebrew output | `scripts/strip_long_dashes.py` |

---

Built by בר שאלתיאל · בינה מלאכותית בגובה העיניים.

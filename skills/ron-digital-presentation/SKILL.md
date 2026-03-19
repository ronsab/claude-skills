---
name: ron-digital-presentation
description: Use when the user asks to create a business HTML presentation (מצגת) for RON DIGITAL STUDIO — a scrollytelling single-file deck for sharing via WhatsApp or a boardroom meeting. Triggers on keywords: מצגת, presentation, RON DIGITAL, דירקטוריון, לקוח, וואטסאפ + HTML.
---

# RON DIGITAL STUDIO — Business Presentation Skill

## Overview

Creates a complete single-file HTML scrollytelling presentation for RON DIGITAL STUDIO, deploys it to Vercel, and returns a shareable link for WhatsApp. Uses content from Google Docs + live website — no duplicate content between sources.

---

## Step 1 — Gather Content (Two Sources, No Overlap)

### Source A: Google Docs — Business Identity
Search Google Drive for document **"תיאור העסק+כנות"** (ID: `1esa-ZZgZAEwZTGGuz5QZm2Vd2xVhhne9eq2f-NQBwWQ`):
- Who is Ron (identity, values, background)
- Honesty differentiator ("במקום X → אני אומר Y" table)
- 5 target audience segments + pain points
- Psychology: blockers / motivators / fears
- 5 objections + answers
- 3 case studies
- Red lines (what Ron won't do)
- Communication principles

Search Google Drive for **"תוכנית עסקית- RON DIGITAL STUDIO"** (ID: `1BML9YGbgG_JZ3JInO0S_anKkL855W6dAWWr9aq-lRFQ`):
- Packages: ₪2,200 / ₪4,500 / ₪8,500
- Financial scenarios (4 tiers, base = ₪190,800/year)
- ROI table

### Source B: Website — Services Only
Fetch `https://always.on.always.smart.rondigital.co.il/` → extract the 13 services list.
**Do NOT duplicate** any content already in the Google Docs.

---

## Step 2 — Build the HTML

Use `template.html` in this skill directory as the skeleton. Fill every `{{PLACEHOLDER}}` with real content.

### 16 Required Sections (in order)
| # | ID | Content Source |
|---|-----|----------------|
| 1 | `hero` | Logo + tagline + headline |
| 2 | `who` | Google Docs identity |
| 3 | `problem` | Derived from audience pain points |
| 4 | `solution` | 4 pillars (strategy/design/content/automation) |
| 5 | `honesty` | Google Docs "במקום X → Y" table |
| 6 | `services` | Website (all 13) |
| 7 | `audiences` | Google Docs 5 segments, tab UI |
| 8 | `psychology` | Google Docs blockers/motivators/fears |
| 9 | `objections` | Google Docs 5 objections |
| 10 | `cases` | Google Docs 3 case studies |
| 11 | `packages` | Business plan ₪2,200/₪4,500/₪8,500 |
| 12 | `financials` | 4 scenarios + ROI table |
| 13 | `competition` | Comparison table (Ron vs Agency vs Freelancer) |
| 14 | `redlines` | Google Docs red lines |
| 15 | `vision` | Future goals |
| 16 | `cta` | WhatsApp + email CTA |

### Critical Design Rules
- **Logo**: `white-space:nowrap` — "RON DIGITAL STUDIO" must appear on **one line**
- **Colors**: `--n950:#010c1f` (navy) · `--gold:#c9a227` · `--b400:#3b82f6`
- **Font**: Heebo (Google Fonts) — Hebrew RTL
- **Direction**: `dir="rtl"` on `<html>`
- **Tone**: Board-of-directors boardroom quality

---

## Step 3 — Write the File

The target file is `C:/Users/USER/Desktop/ron-digital-presentation.html`.

**CRITICAL — Write tool rule:** If the file already exists, you MUST `Read` it first (even 5 lines) before calling `Write`. Otherwise Write tool errors with "File has not been read yet".

```
Read (5 lines) → Write (full content)
```

If file does not exist, Write directly.

---

## Step 4 — Deploy to Vercel

### Auth check
```bash
vercel whoami 2>&1
```

If output contains "No existing credentials":
1. Run `vercel whoami` as a **background task** — it starts the device flow
2. Read its output file to get the URL + user_code
3. Show the user: `https://vercel.com/oauth/device?user_code=XXXX-XXXX`
4. Tell them to confirm in their browser (they have a Vercel account: **ronsabon-4934**)
5. Wait for the background task to complete (status: completed = auth success)

**The background task MUST stay alive while the user authenticates.** Do not kill it. Do not run a second `vercel whoami` that would start a competing flow.

### Deploy
```bash
# Create clean deploy folder (Vercel needs index.html at root)
powershell.exe -Command "New-Item -ItemType Directory -Force -Path 'C:\Users\USER\Desktop\ron-deploy'; Copy-Item 'C:\Users\USER\Desktop\ron-digital-presentation.html' 'C:\Users\USER\Desktop\ron-deploy\index.html'"

# Deploy
cd "C:/Users/USER/Desktop/ron-deploy" && vercel deploy --yes 2>&1
```

The output will contain two URLs:
- **Long preview URL** — temporary
- **Short alias** `https://ron-digital-studio.vercel.app` — share this one

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Writing file without reading first | Always `Read` 5 lines before `Write` on existing file |
| Logo wrapping to 3 lines | Add `white-space:nowrap` to `.hlogo` class |
| Vercel device code expiring | Keep background task alive; don't run competing `whoami` |
| Deploy folder missing `index.html` | Copy HTML as `index.html`, not `ron-digital-presentation.html` |
| Duplicate content (Docs + Website) | Services come from website ONLY; all other content from Docs ONLY |
| Scenario bars not animating | Trigger on scroll event checking `financials` section rect |

---

## Quick Reference

```
Content:  Google Docs (identity/honesty/audiences/psychology/objections/cases/packages/financials)
Services: Website only (13 services)
Template: skills/ron-digital-presentation/template.html
Output:   C:/Users/USER/Desktop/ron-digital-presentation.html
Deploy:   C:/Users/USER/Desktop/ron-deploy/index.html → vercel deploy --yes
URL:      https://ron-digital-studio.vercel.app
Account:  ronsabon-4934
```

#!/usr/bin/env node
/**
 * generate-map.mjs — מחולל מפת הסקילים של RON DIGITAL STUDIO
 *
 * סורק את כל הסקילים/commands/agents, ממזג עם skill-map-data.json,
 * ומייצר skill-map.html בדסקטופ. כל סקיל חדש מתווסף אוטומטית.
 *
 * הרצה: node ~/.claude/skill-map/generate-map.mjs
 * ללא תלויות חיצוניות (fs + path בלבד).
 */

import { readFileSync, writeFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { homedir } from 'node:os';

const __dirname = dirname(fileURLToPath(import.meta.url));
const HOME = homedir();
const CLAUDE = join(HOME, '.claude');
const DATA_FILE = join(__dirname, 'skill-map-data.json');
const OUTPUT = join(HOME, 'Desktop', 'skill-map.html');

// ── 1. טעינת ה-curation ──────────────────────────────────
const data = JSON.parse(readFileSync(DATA_FILE, 'utf8'));

// ── 2. פרסור frontmatter (regex, ללא תלויות) ─────────────
function parseFrontmatter(content) {
  const m = content.match(/^---\s*\r?\n([\s\S]*?)\r?\n---/);
  if (!m) return {};
  const fm = m[1];
  const out = {};
  // name
  const nameM = fm.match(/^name:\s*(.+)$/m);
  if (nameM) out.name = nameM[1].trim().replace(/^["']|["']$/g, '');
  // description (תומך גם ב->  multi-line block וגם ב-inline)
  const descBlock = fm.match(/^description:\s*>[-]?\s*\r?\n([\s\S]*?)(?=\r?\n\w+:|$)/m);
  if (descBlock) {
    out.description = descBlock[1].split(/\r?\n/).map(l => l.trim()).filter(Boolean).join(' ');
  } else {
    const descInline = fm.match(/^description:\s*(.+)$/m);
    if (descInline) out.description = descInline[1].trim().replace(/^["']|["']$/g, '');
  }
  return out;
}

// ── 3. סריקת מקורות ──────────────────────────────────────
function scanDir(dir, type) {
  const found = [];
  if (!existsSync(dir)) return found;
  for (const entry of readdirSync(dir)) {
    if (entry.startsWith('.')) continue;
    const full = join(dir, entry);
    let st;
    try { st = statSync(full); } catch { continue; }
    if (type === 'skill' && st.isDirectory()) {
      const skillFile = join(full, 'SKILL.md');
      if (existsSync(skillFile)) {
        // רמה 1: לתיקייה יש SKILL.md משלה
        try {
          const fm = parseFrontmatter(readFileSync(skillFile, 'utf8'));
          found.push({ id: entry, name: fm.name || entry, description: fm.description || '', source: 'local' });
        } catch { found.push({ id: entry, name: entry, description: '', source: 'local' }); }
      } else {
        // רמה 2: תיקיית-אב ללא SKILL.md → סורקים תת-תיקיות (סקילים מקוננים)
        let subEntries = [];
        try { subEntries = readdirSync(full); } catch { subEntries = []; }
        for (const sub of subEntries) {
          if (sub.startsWith('.')) continue;
          const subFull = join(full, sub);
          let subSt;
          try { subSt = statSync(subFull); } catch { continue; }
          if (!subSt.isDirectory()) continue;
          const subSkillFile = join(subFull, 'SKILL.md');
          if (!existsSync(subSkillFile)) continue;
          const nestedId = entry + '/' + sub;
          try {
            const fm = parseFrontmatter(readFileSync(subSkillFile, 'utf8'));
            found.push({ id: nestedId, name: fm.name || sub, description: fm.description || '', source: 'nested', parent: entry });
          } catch { found.push({ id: nestedId, name: sub, description: '', source: 'nested', parent: entry }); }
        }
      }
    } else if (type === 'md' && entry.endsWith('.md')) {
      const id = entry.replace(/\.md$/, '');
      try {
        const fm = parseFrontmatter(readFileSync(full, 'utf8'));
        found.push({ id, name: fm.name || id, description: fm.description || '', source: type });
      } catch { found.push({ id, name: id, description: '', source: type }); }
    }
  }
  return found;
}

const localSkills = scanDir(join(CLAUDE, 'skills'), 'skill');
const commands = scanDir(join(CLAUDE, 'commands'), 'md');
const agents = scanDir(join(CLAUDE, 'agents'), 'md');

// ── 4. מיזוג curation + discovery ────────────────────────
// מאחדים את כל הקטלוגים מה-data file (skills/commands/agents)
const curated = { ...data.skills, ...data.commands, ...data.agents };

// כל הסקילים שהתגלו במערכת (id ייחודי)
const discoveredIds = new Set([
  ...localSkills.map(s => s.id),
  ...commands.map(s => s.id),
  ...agents.map(s => s.id),
]);
const descById = {};
[...localSkills, ...commands, ...agents].forEach(s => { descById[s.id] = s.description; });

// סקילים עסקיים (מתוך curation) → כרטיסיות עשירות
const enrich = data.enrich || {};
const businessSkills = [];
for (const [id, info] of Object.entries(curated)) {
  businessSkills.push({ id, ...info, ...(enrich[id] || {}), discovered: discoveredIds.has(id) });
}

// סקילים שהתגלו אך לא ב-curation → "🆕 לא מסווג" + "ספרייה מלאה"
const uncuratedAll = localSkills.filter(s => !curated[s.id]);
const uncuratedLocal = uncuratedAll.filter(s => s.source !== 'nested');
const uncuratedNested = uncuratedAll.filter(s => s.source === 'nested');
const uncuratedCommands = commands.filter(s => !curated[s.id]);
const uncuratedAgents = agents.filter(s => !curated[s.id]);

// ── 5. סטטיסטיקות ────────────────────────────────────────
const stats = {
  business: businessSkills.length,
  localTotal: localSkills.length,
  commands: commands.length,
  agents: agents.length,
  uncategorized: uncuratedLocal.length,
  conflicts: data.conflicts.length,
  opportunities: data.opportunities.length,
};

// ── 6. עזרי רינדור ───────────────────────────────────────
const esc = s => String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const catColor = c => (data.categories[c] || {}).color || '#71717a';
const catLabel = c => (data.categories[c] || {}).label || c;
const catEmoji = c => (data.categories[c] || {}).emoji || '•';

function badge(text) {
  const hot = ['ליבה', 'CANONICAL', 'חם!'].includes(text);
  const isNew = text === 'חדש';
  const cls = hot ? 'badge-hot' : isNew ? 'badge-new' : 'badge-default';
  return `<span class="badge ${cls}">${esc(text)}</span>`;
}

function skillCard(s) {
  const color = catColor(s.category);
  const badges = (s.badges || []).map(badge).join('');
  const oppLine = s.opportunity ? `<div class="card-opp">💡 ${esc(s.opportunity)}</div>` : '';
  const priceLine = s.pricing && s.pricing !== '—' && s.pricing !== 'כלול' ? `<span class="card-price">${esc(s.pricing)}</span>` : '';
  const warn = s.discovered === false ? `<span class="card-warn" title="לא נמצא בסריקה — אולי plugin או שם שונה">⚠︎</span>` : '';
  const dataName = esc((s.id + ' ' + (s.invoke || '') + ' ' + (s.whenToUse || '')).toLowerCase());
  const sayText = esc(s.example || s.invoke || '');
  return `
  <div class="card" data-cat="${esc(s.category)}" data-name="${dataName}" data-id="${esc(s.id)}" data-say="${sayText}" style="--cat:${color}">
    <div class="card-head">
      <span class="card-title">${s.emoji || ''} ${esc(s.id)} ${warn}</span>
      <span class="card-badges">${badges}${priceLine}</span>
    </div>
    <code class="card-invoke">${esc(s.invoke || '')}</code>
    <div class="card-when"><b>מתי:</b> ${esc(s.whenToUse || '')}</div>
    ${s.output ? `<div class="card-out"><b>מוציא:</b> ${esc(s.output)}</div>` : ''}
    ${oppLine}
    ${s.example ? `<div class="card-ex"><b>💬 דוגמה:</b> ${esc(s.example)}</div>` : ''}
    ${s.twist ? `<div class="card-twist"><b>✨ טוויסט:</b> ${esc(s.twist)}</div>` : ''}
    <div class="card-foot">
      <button class="card-fav" title="הוסף למועדפים" aria-label="הוסף למועדפים" onclick="toggleFav('${esc(s.id)}',this)">☆</button>
      <button class="card-copy" title="העתק משפט הפעלה" aria-label="העתק משפט הפעלה" onclick="copyTrigger('${esc(s.id)}',this)">📋 העתק</button>
    </div>
  </div>`;
}

function libRow(s) {
  const dataName = esc((s.id + ' ' + (s.description || '') + ' ' + (s.parent || '')).toLowerCase());
  const fullDesc = s.description || '';
  // הבלטת ה-"Use when" (זה ה'מתי משתמשים') אם קיים בתיאור
  const uw = fullDesc.match(/use when[^.]*\.?/i);
  const desc = (uw ? uw[0] : fullDesc).slice(0, 150);
  const parentTag = s.parent ? `<span class="lib-parent">מתוך ${esc(s.parent)}</span>` : '';
  return `<div class="lib-row" data-name="${dataName}"><code>${esc(s.id)}</code><span class="lib-src">${esc(s.source)}</span>${parentTag}<span class="lib-desc">${esc(desc)}</span></div>`;
}

// ── סיווג הספרייה לפי תחום (suffix → prefix → keyword → catchall) ──
const libGroups = data.libraryGroups || [];
function classifyLib(s) {
  const id = (s.id || '').toLowerCase();
  const txt = (id + ' ' + (s.description || '')).toLowerCase();
  // 1+2: סיומת/קידומת מדויקות של ה-id (הרעש sci/tob/gs נתפס כאן)
  for (const g of libGroups) if (g.suffix && g.suffix.some(sf => id.endsWith(sf))) return g.id;
  for (const g of libGroups) if (g.prefix && g.prefix.some(p => id.startsWith(p))) return g.id;
  // 3: keyword שפותח את ה-id (מדויק) — קבוצות ממוקדות לפני רחבות
  for (const g of libGroups) if (!g.broad && g.kw && g.kw.some(k => id.startsWith(k.trim()))) return g.id;
  for (const g of libGroups) if (g.broad && g.kw && g.kw.some(k => id.startsWith(k.trim()))) return g.id;
  // 4: keyword בכל הטקסט — ממוקד לפני רחב (מונע מ-marketing לבלוע sales/strategy)
  for (const g of libGroups) if (!g.broad && g.kw && g.kw.some(k => txt.includes(k))) return g.id;
  for (const g of libGroups) if (g.broad && g.kw && g.kw.some(k => txt.includes(k))) return g.id;
  const ca = libGroups.find(g => g.catchall);
  return ca ? ca.id : 'other';
}

// קיבוץ סקילים עסקיים לפי קטגוריה
const byCat = {};
for (const s of businessSkills) {
  (byCat[s.category] = byCat[s.category] || []).push(s);
}
const catOrder = Object.keys(data.categories);

// ── 7. בניית HTML ────────────────────────────────────────
const tabsHtml = ['<button class="tab active" data-cat="all" onclick="filterCat(\'all\',this)">הכל</button>']
  .concat(catOrder.filter(c => byCat[c]).map(c =>
    `<button class="tab" data-cat="${c}" onclick="filterCat('${c}',this)">${catEmoji(c)} ${esc(catLabel(c))}</button>`))
  .join('');

const cardsHtml = catOrder.filter(c => byCat[c]).map(c => {
  const cards = byCat[c].map(skillCard).join('');
  return `<div class="cat-group" data-group="${c}"><h3 class="cat-h" style="--cat:${catColor(c)}">${catEmoji(c)} ${esc(catLabel(c))} <span class="cat-count">${byCat[c].length}</span></h3><div class="cards">${cards}</div></div>`;
}).join('');

const wizardOptions = data.decisionRules.map((r, i) =>
  `<option value="${i}">${esc(r.intent)}</option>`).join('');

const conflictsHtml = data.conflicts.map(c => {
  const resolved = c.status === 'resolved';
  const chips = c.skills.map(s => `<span class="vs">${esc(s)}</span>`).join('<span class="vs-d">·</span>');
  const statusBadge = resolved
    ? `<span class="sev-ok">✅ פתור</span>`
    : `<span class="${c.severity === 'high' ? 'sev-high' : 'sev-med'}">${c.severity === 'high' ? 'קריטי' : 'בינוני'}</span>`;
  const ruleLine = c.rule ? `<div class="conflict-rule">📍 ${esc(c.rule)}</div>` : '';
  return `<div class="conflict${resolved ? ' resolved' : ''}"><div class="conflict-h"><span>${c.icon} ${esc(c.title)}</span>${statusBadge}</div><div class="conflict-vs">${chips}</div><div class="conflict-fix">🧭 ${esc(c.fix)}</div>${ruleLine}</div>`;
}).join('');
const resolvedCount = data.conflicts.filter(c => c.status === 'resolved').length;

const oppsHtml = data.opportunities.map((o, i) =>
  `<div class="opp" data-opp="${i}"><div class="opp-h"><span class="opp-icon">${o.icon}</span><span class="opp-title">${esc(o.title)}</span><span class="opp-val">${esc(o.value)}</span></div><div class="opp-why">${esc(o.why)}</div><div class="opp-how">▶ ${esc(o.how)}</div></div>`).join('');

const cheatHtml = data.cheatSheet.map(c =>
  `<div class="cheat"><span class="cheat-trig">${esc(c.trigger)}</span><code class="cheat-say">${esc(c.say)}</code></div>`).join('');

const scenariosHtml = (data.scenarios || []).map(sc => {
  const steps = (sc.steps || []).map(st => {
    const safeId = esc(sc.title + '-' + st.num).replace(/[^a-z0-9-]/gi, '');
    return `<div class="scenario-step">
      <div class="step-num">${st.num}</div>
      <div class="step-body">
        <div class="step-action">${esc(st.action)}</div>
        ${st.skill ? `<span class="step-skill">${esc(st.skill)}</span>` : ''}
        <div class="step-say-row">
          <span class="step-say" title="${esc(st.say)}">${esc(st.say)}</span>
          <button class="step-copy" id="sc-${safeId}" onclick="copySay('${esc(st.say)}','sc-${safeId}')">📋 העתק</button>
        </div>
        ${st.get ? `<div class="step-get">${esc(st.get)}</div>` : ''}
      </div>
    </div>`;
  }).join('');
  const searchText = [sc.title, sc.trigger, ...(sc.steps||[]).map(s=>s.action+' '+s.skill+' '+s.say)].join(' ').toLowerCase();
  return `<div class="scenario" data-name="${esc(searchText)}">
    <div class="scenario-h"><span class="scenario-icon">${sc.icon}</span><span class="scenario-title">${esc(sc.title)}</span></div>
    <div class="scenario-trigger">טריגר: ${esc(sc.trigger)}</div>
    <div class="scenario-steps">${steps}</div>
  </div>`;
}).join('');

const recipesHtml = (data.recipes || []).map(r => {
  const chain = r.chain.map(s => `<span class="chain-step">${esc(s)}</span>`).join('<span class="chain-arr">←</span>');
  return `<div class="recipe"><div class="recipe-h">${r.icon} ${esc(r.name)}</div><div class="recipe-chain">${chain}</div><div class="recipe-out"><b>מקבלים:</b> ${esc(r.outcome)}</div><div class="recipe-val">💰 ${esc(r.value)}</div></div>`;
}).join('');

const buildIdeasHtml = (data.buildIdeas || []).map(b => {
  const tags = (b.skills || []).map(s => `<span class="idea-tag">${esc(s)}</span>`).join('');
  return `<div class="idea"><div class="idea-h"><span class="idea-icon">${b.icon}</span><span class="idea-title">${esc(b.title)}</span><span class="idea-rev">${esc(b.revenue)}</span></div><div class="idea-desc">${esc(b.desc)}</div><div class="idea-tags">${tags}</div></div>`;
}).join('');

const checklistsHtml = (data.checklists || []).map((c, ci) => {
  const steps = c.steps.map((st, si) => {
    const skillTag = st.skill ? `<span class="chk-skill">${esc(st.skill)}</span>` : '';
    return `<label class="chk-step"><input type="checkbox" id="chk-${ci}-${si}" onchange="toggleStep(${ci},${si},this)"><span class="chk-text">${esc(st.text)}</span>${skillTag}</label>`;
  }).join('');
  return `<div class="checklist"><div class="checklist-h"><span>${c.icon} ${esc(c.name)}</span><button class="chk-reset" onclick="resetChecklist(${ci},${c.steps.length})">איפוס</button></div><div class="checklist-steps">${steps}</div></div>`;
}).join('');

// קיבוץ כל הלא-מסווגים (מקומי + מקונן + פקודות + agents) לפי תחום
const allUncurated = [...uncuratedLocal, ...uncuratedNested, ...uncuratedCommands, ...uncuratedAgents];
const libByGroup = {};
for (const s of allUncurated) {
  const gid = classifyLib(s);
  (libByGroup[gid] = libByGroup[gid] || []).push(s);
}
const libHtml = libGroups.map(g => {
  const items = libByGroup[g.id] || [];
  if (!items.length) return '';
  const rows = items.map(libRow).join('');
  return `<details class="lib-group${g.priority ? ' lib-group-priority' : ''}"${g.open ? ' open' : ''} data-libgroup="${g.id}"${g.open ? ' data-defopen="1"' : ''}>
    <summary><span class="lib-g-label">${esc(g.label)}</span><span class="lib-count">${items.length}</span></summary>
    <div class="lib-rows">${rows}</div>
  </details>`;
}).join('');

// JSON להזרקה ל-JS (אשף ההחלטה + הזדמנות השבוע)
// אינדקס חיפוש למתאם הצרכים (offline)
const searchIndex = [];
businessSkills.forEach(s => searchIndex.push({
  t: 'skill', id: s.id, cat: s.category, label: s.id,
  invoke: s.invoke || '', say: s.example || '',
  text: [s.id, s.whenToUse, s.output, s.opportunity, s.example, (s.badges || []).join(' ')].filter(Boolean).join(' ')
}));
data.decisionRules.forEach(r => searchIndex.push({
  t: 'rule', id: r.skill, cat: '', label: r.intent,
  invoke: '', say: r.say || '',
  text: [r.intent, r.skill, r.say, r.note].filter(Boolean).join(' ')
}));
(data.recipes || []).forEach(r => searchIndex.push({
  t: 'recipe', id: r.name, cat: '', label: r.name,
  invoke: r.chain.join(' ← '), say: '',
  text: [r.name, r.outcome, r.value, r.chain.join(' ')].filter(Boolean).join(' ')
}));
[...uncuratedLocal, ...uncuratedCommands, ...uncuratedAgents].forEach(s => searchIndex.push({
  t: 'lib', id: s.id, cat: '', label: s.id,
  invoke: '', say: '',
  text: [s.id, (s.description || '').slice(0, 130)].filter(Boolean).join(' ')
}));

const bizSkills = businessSkills.map(s => ({
  id: s.id, label: s.id, cat: s.category, emoji: s.emoji || '',
  invoke: s.invoke || '', say: s.example || s.invoke || ''
}));

const clientData = JSON.stringify({
  decisionRules: data.decisionRules,
  opportunities: data.opportunities,
  sparks: data.sparks || [],
  searchIndex,
  bizSkills,
  checklists: data.checklists || [],
});

const buildDate = new Date().toLocaleDateString('he-IL', { day: 'numeric', month: 'long', year: 'numeric' });
const weekNum = Math.floor((Date.now() / 86400000 + 4) / 7); // לרוטציית הזדמנות השבוע

const html = `<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>מפת הסקילים | RON DIGITAL STUDIO</title>
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@200;300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
/* ===== פלטה: משרד יוקרה בהיר — גריאז' + ברונזה ===== */
:root{
  --bg:#F4F2ED;--bg2:#EDEAE3;--surface:#FFFFFF;--surface2:#FBFAF7;
  --ink:#2B2620;--ink2:#5C5448;--ink3:#756A5A;
  --bronze:#9C7A4A;--bronze-ink:#7A5C32;--bronze-soft:rgba(156,122,74,.10);
  --border:#E2DDD2;--border2:#D4CCBE;
  --green:#2E7D52;--green-soft:rgba(46,125,82,.10);
  --red:#B3261E;--red-soft:rgba(179,38,30,.07);
  --amber:#8A6D00;
  --blue-ink:#274690;--blue-soft:rgba(39,70,144,.07);
  --shadow:0 1px 3px rgba(43,38,32,.06);--shadow-lg:0 10px 28px rgba(43,38,32,.10);
}
/* מצב ניגודיות גבוהה */
body.hc{--bg:#FFFFFF;--bg2:#F2F2F2;--surface:#FFFFFF;--surface2:#FFFFFF;
  --ink:#000000;--ink2:#1A1A1A;--ink3:#333333;
  --bronze:#6E4F23;--bronze-ink:#5A3D1A;--bronze-soft:rgba(110,79,35,.14);
  --border:#7A7A7A;--border2:#555555;
  --green:#1B5E36;--red:#8E1B14;--amber:#6B5300;--blue-ink:#1B3270;
  --shadow:none;--shadow-lg:none;}
body.hc .card,body.hc .cheat,body.hc .conflict,body.hc .opp,body.hc .lib-toggle{border-width:2px}
*{box-sizing:border-box;margin:0;padding:0}
html{font-size:100%}
body{font-family:'Heebo',Arial,sans-serif;background:var(--bg);color:var(--ink);direction:rtl;-webkit-font-smoothing:antialiased;line-height:1.65;font-size:1rem}
/* focus נראה לניווט מקלדת */
a:focus-visible,button:focus-visible,select:focus-visible,input:focus-visible,[tabindex]:focus-visible{outline:3px solid var(--bronze);outline-offset:2px;border-radius:4px}
.skip{position:absolute;right:-9999px;top:8px;background:var(--bronze-ink);color:#fff;padding:10px 18px;border-radius:6px;z-index:2000;font-weight:600}
.skip:focus{right:8px}
.topbar{background:var(--surface);border-bottom:1px solid var(--border);padding:14px 28px;display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap}
.brand{font-size:.75rem;font-weight:800;letter-spacing:2.5px;text-transform:uppercase;color:var(--bronze-ink)}
.search{background:var(--surface2);border:1px solid var(--border2);border-radius:8px;color:var(--ink);font-family:Heebo;font-size:.875rem;padding:9px 14px;width:240px;direction:rtl}
.search::placeholder{color:var(--ink3)}
.updated{font-size:.75rem;color:var(--ink3)}
.hero{padding:52px 28px 32px;text-align:center}
.hero h1{font-size:2.5rem;font-weight:300;letter-spacing:-.5px;margin-bottom:10px;color:var(--ink)}
.hero h1 b{font-weight:800;color:var(--bronze-ink)}
.hero p{font-size:1rem;color:var(--ink2);font-weight:400;max-width:620px;margin:0 auto}
.stats{display:flex;justify-content:center;gap:30px;margin-top:28px;flex-wrap:wrap}
.stat{text-align:center}
.stat-n{font-size:1.75rem;font-weight:800;color:var(--bronze-ink)}
.stat-l{font-size:.6875rem;color:var(--ink3);letter-spacing:1px;text-transform:uppercase;font-weight:600}
.section{padding:30px 28px;max-width:1280px;margin:0 auto}
.section-t{display:flex;align-items:center;gap:14px;margin-bottom:20px}
.section-t h2{font-size:.8125rem;font-weight:800;letter-spacing:2.5px;text-transform:uppercase;color:var(--bronze-ink);white-space:nowrap}
.section-t .line{flex:1;height:1px;background:var(--border2)}
/* Wizard */
.wizard{background:var(--surface);border:1px solid var(--border2);border-top:4px solid var(--bronze);border-radius:14px;padding:30px;text-align:center;box-shadow:var(--shadow-lg)}
.wizard h2{font-size:1.375rem;font-weight:700;margin-bottom:18px;color:var(--ink)}
.wizard select{background:var(--surface2);border:1px solid var(--border2);border-radius:8px;color:var(--ink);font-family:Heebo;font-size:1rem;padding:13px 16px;width:100%;max-width:480px;direction:rtl;cursor:pointer}
.wizard-out{margin-top:22px;display:none}
.wizard-out.show{display:block;animation:fade .3s}
@keyframes fade{from{opacity:0;transform:translateY(6px)}to{opacity:1}}
.wizard-skill{font-size:.8125rem;color:var(--ink3);margin-bottom:8px;font-weight:600}
.wizard-say{display:inline-block;background:var(--bronze-soft);border:1px solid var(--bronze);border-radius:8px;color:var(--bronze-ink);font-size:1.0625rem;padding:13px 24px;font-weight:700;direction:rtl}
.wizard-note{font-size:.8125rem;color:var(--ink2);margin-top:12px}
/* Needs matcher */
.need-sub{font-size:.875rem;color:var(--ink2);margin-bottom:16px;line-height:1.6}
.need-box{display:flex;gap:10px;max-width:600px;margin:0 auto;flex-wrap:wrap}
.need-box input{flex:1;min-width:220px;background:var(--surface2);border:1px solid var(--border2);border-radius:8px;color:var(--ink);font-family:Heebo;font-size:1rem;padding:13px 16px;direction:rtl}
.need-btn{background:var(--bronze-ink);color:#fff;border:none;border-radius:8px;padding:13px 24px;font-family:Heebo;font-size:1rem;font-weight:700;cursor:pointer;white-space:nowrap;min-height:48px}
.need-btn:hover{background:var(--bronze)}
.need-out{margin-top:18px;text-align:right;display:none}
.need-out.show{display:block;animation:fade .3s}
.need-empty{font-size:.875rem;color:var(--ink3);text-align:center}
.need-head{font-size:1rem;font-weight:700;margin-bottom:14px;text-align:center}
.need-head.ok{color:var(--green)}
.need-head.maybe{color:var(--amber)}
.need-head.no{color:var(--red)}
.need-res{background:var(--surface2);border:1px solid var(--border);border-right:4px solid var(--bronze);border-radius:10px;padding:14px 16px;margin-bottom:10px;text-align:right}
.need-res-name{font-size:.9375rem;font-weight:700;color:var(--ink);margin-bottom:6px}
.need-res-type{font-size:.625rem;font-weight:700;color:var(--ink3);background:var(--bg2);border:1px solid var(--border2);padding:2px 7px;border-radius:4px;margin-right:8px}
.need-res-say{font-size:.8125rem;color:var(--bronze-ink);background:var(--bronze-soft);border-radius:6px;padding:7px 10px;margin-top:6px;font-family:Heebo}
.need-bridge{background:var(--bg2);border:1px dashed var(--border2);border-radius:8px;padding:12px 14px;margin-top:14px;font-size:.8125rem;color:var(--ink2);text-align:center}
.need-bridge code{color:var(--bronze-ink);font-weight:700;font-family:Heebo}
.need-copy{background:var(--surface);border:1px solid var(--bronze);color:var(--bronze-ink);border-radius:6px;padding:6px 14px;font-family:Heebo;font-size:.75rem;font-weight:700;cursor:pointer;margin-top:8px}
.wizard-divider{display:flex;align-items:center;text-align:center;color:var(--ink3);font-size:.75rem;margin:22px 0 14px}
.wizard-divider::before,.wizard-divider::after{content:'';flex:1;height:1px;background:var(--border2)}
.wizard-divider span{padding:0 14px}
/* Cheat */
.cheats{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px}
.cheat{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:14px 16px;display:flex;flex-direction:column;gap:7px;box-shadow:var(--shadow)}
.cheat-trig{font-size:.75rem;color:var(--ink3);font-weight:700}
.cheat-say{font-size:.8125rem;color:var(--bronze-ink);background:var(--bronze-soft);padding:7px 10px;border-radius:6px;font-family:Heebo;font-weight:600}
/* Opp of week */
.oow{background:var(--surface);border:1px solid var(--border2);border-right:4px solid var(--bronze);border-radius:14px;padding:26px 30px;box-shadow:var(--shadow-lg)}
.oow-tag{font-size:.6875rem;letter-spacing:2px;text-transform:uppercase;color:var(--bronze-ink);font-weight:800;margin-bottom:10px}
.oow-title{font-size:1.375rem;font-weight:700;margin-bottom:10px;color:var(--ink)}
.oow-why{font-size:.9375rem;color:var(--ink2);margin-bottom:10px}
.oow-how{font-size:.875rem;color:var(--bronze-ink);font-weight:600}
/* Tabs */
.tabs{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:24px}
.tab{background:var(--surface);border:1px solid var(--border2);border-radius:22px;padding:8px 17px;font-size:.8125rem;font-weight:600;color:var(--ink2);cursor:pointer;font-family:Heebo;transition:.2s}
.tab:hover{border-color:var(--bronze);color:var(--bronze-ink)}
.tab.active{background:var(--bronze-ink);border-color:var(--bronze-ink);color:#fff}
.cat-group{margin-bottom:30px}
.cat-h{font-size:1rem;font-weight:700;margin-bottom:14px;padding-right:12px;border-right:4px solid var(--cat);color:var(--ink)}
.cat-count{font-size:.75rem;color:var(--ink3);font-weight:500}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:16px}
.card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:20px 22px;position:relative;overflow:hidden;transition:transform .15s,box-shadow .2s;box-shadow:var(--shadow)}
.card::before{content:'';position:absolute;top:0;right:0;width:4px;height:100%;background:var(--cat)}
.card:hover{transform:translateY(-3px);box-shadow:var(--shadow-lg)}
.card-head{display:flex;justify-content:space-between;align-items:flex-start;gap:8px;margin-bottom:10px}
.card-title{font-size:.9375rem;font-weight:700;color:var(--ink)}
.card-badges{display:flex;gap:5px;flex-wrap:wrap;align-items:center}
.badge{font-size:.625rem;font-weight:800;letter-spacing:.3px;padding:3px 8px;border-radius:4px;white-space:nowrap}
.badge-hot{background:var(--bronze-soft);color:var(--bronze-ink);border:1px solid var(--bronze)}
.badge-new{background:var(--green-soft);color:var(--green);border:1px solid var(--green)}
.badge-default{background:var(--bg2);color:var(--ink2);border:1px solid var(--border2)}
.card-price{font-size:.6875rem;font-weight:800;color:var(--bronze-ink);background:var(--bronze-soft);padding:3px 8px;border-radius:4px;white-space:nowrap}
.card-warn{color:var(--red);font-size:.8125rem}
.card-invoke{display:inline-block;font-size:.75rem;color:var(--bronze-ink);background:var(--bronze-soft);padding:5px 10px;border-radius:5px;margin-bottom:11px;font-family:Heebo;font-weight:600;word-break:break-all}
.card-when,.card-out{font-size:.8125rem;color:var(--ink2);margin-bottom:6px}
.card-when b,.card-out b{color:var(--ink);font-weight:700;font-size:.75rem}
.card-opp{font-size:.75rem;color:var(--green);background:var(--green-soft);border:1px solid rgba(46,125,82,.3);border-radius:6px;padding:7px 10px;margin-top:9px;line-height:1.45;font-weight:500}
.card-ex{font-size:.75rem;color:var(--bronze-ink);background:var(--bronze-soft);border-radius:6px;padding:7px 10px;margin-top:8px;line-height:1.45}
.card-ex b{font-weight:700}
.card-twist{font-size:.75rem;color:var(--ink2);margin-top:7px;line-height:1.45;font-style:italic}
.card-twist b{color:var(--ink);font-weight:700;font-style:normal}
/* Card footer: favorite + copy */
.card-foot{display:flex;gap:8px;align-items:center;margin-top:12px;padding-top:10px;border-top:1px solid var(--border)}
.card-fav{background:none;border:1px solid var(--border2);border-radius:6px;color:var(--ink3);font-size:1rem;cursor:pointer;width:34px;height:34px;line-height:1}
.card-fav.on{color:var(--bronze-ink);border-color:var(--bronze);background:var(--bronze-soft)}
.card-fav:hover{border-color:var(--bronze)}
.card-copy{flex:1;background:var(--surface2);border:1px solid var(--border2);border-radius:6px;color:var(--ink2);font-family:Heebo;font-size:.75rem;font-weight:600;padding:8px;cursor:pointer;min-height:34px}
.card-copy:hover{border-color:var(--bronze);color:var(--bronze-ink)}
/* Personal: shortcuts + usage */
.favs{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:22px}
.fav-chip{display:flex;align-items:center;gap:8px;background:var(--surface);border:1px solid var(--bronze);border-radius:10px;padding:10px 14px;box-shadow:var(--shadow)}
.fav-chip .fc-name{font-weight:700;color:var(--ink);font-size:.875rem}
.fav-chip button{background:var(--bronze-soft);border:1px solid var(--bronze);border-radius:6px;color:var(--bronze-ink);font-family:Heebo;font-size:.6875rem;font-weight:700;padding:4px 9px;cursor:pointer}
.fav-empty{font-size:.8125rem;color:var(--ink3)}
.usage-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.usage-h{font-size:.9375rem;font-weight:700;color:var(--ink);margin-bottom:10px}
.usage-list{display:flex;flex-direction:column;gap:7px}
.usage-item{display:flex;justify-content:space-between;align-items:center;background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:9px 12px;font-size:.8125rem}
.usage-item .ui-name{font-weight:600;color:var(--ink)}
.usage-item .ui-count{font-size:.6875rem;color:var(--bronze-ink);background:var(--bronze-soft);padding:2px 8px;border-radius:10px;font-weight:700}
.usage-item button{background:var(--surface2);border:1px solid var(--border2);border-radius:6px;color:var(--ink2);font-family:Heebo;font-size:.6875rem;font-weight:600;padding:4px 9px;cursor:pointer}
/* Checklists */
.checklists{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:16px}
.checklist{background:var(--surface);border:1px solid var(--border);border-top:3px solid var(--green);border-radius:12px;padding:16px 18px;box-shadow:var(--shadow)}
.checklist-h{display:flex;justify-content:space-between;align-items:center;font-size:.9375rem;font-weight:700;color:var(--ink);margin-bottom:12px}
.chk-reset{background:none;border:1px solid var(--border2);border-radius:6px;color:var(--ink3);font-family:Heebo;font-size:.6875rem;padding:4px 10px;cursor:pointer}
.chk-reset:hover{border-color:var(--red);color:var(--red)}
.checklist-steps{display:flex;flex-direction:column;gap:9px}
.chk-step{display:flex;align-items:center;gap:9px;font-size:.8125rem;color:var(--ink2);cursor:pointer}
.chk-step input{width:18px;height:18px;accent-color:var(--green);cursor:pointer;flex-shrink:0}
.chk-step input:checked + .chk-text{text-decoration:line-through;color:var(--ink3)}
.chk-text{flex:1}
.chk-skill{font-size:.625rem;color:var(--bronze-ink);background:var(--bronze-soft);border:1px solid var(--bronze);padding:2px 7px;border-radius:4px;white-space:nowrap}
/* Service menu link */
.menu-link{display:inline-block;background:var(--bronze-ink);color:#fff;text-decoration:none;border-radius:50px;padding:10px 22px;font-size:.875rem;font-weight:700}
.menu-link:hover{background:var(--bronze)}
.sec-intro{font-size:.8125rem;color:var(--ink3);margin-bottom:18px;margin-top:-8px;line-height:1.6}
/* Spark */
.spark{background:linear-gradient(135deg,var(--bronze-ink),var(--bronze));border-radius:14px;padding:22px 28px;display:flex;justify-content:space-between;align-items:center;gap:18px;flex-wrap:wrap;box-shadow:var(--shadow-lg)}
.spark-left{flex:1;min-width:240px}
.spark-tag{font-size:.6875rem;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,.8);font-weight:800;margin-bottom:8px}
.spark-text{font-size:1.0625rem;color:#fff;font-weight:600;line-height:1.5}
.spark-btn{background:#fff;color:var(--bronze-ink);border:none;border-radius:50px;padding:14px 26px;font-family:Heebo;font-size:1rem;font-weight:800;cursor:pointer;white-space:nowrap;min-height:48px}
.spark-btn:hover{transform:translateY(-2px)}
body.hc .spark{background:var(--bronze-ink)}
body.hc .spark-text{color:#fff}
/* Recipes */
.recipes{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:16px}
.recipe{background:var(--surface);border:1px solid var(--border);border-right:4px solid var(--bronze);border-radius:12px;padding:18px 20px;box-shadow:var(--shadow)}
.recipe-h{font-size:1rem;font-weight:700;color:var(--ink);margin-bottom:12px}
.recipe-chain{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-bottom:12px}
.chain-step{font-size:.6875rem;background:var(--bronze-soft);color:var(--bronze-ink);border:1px solid var(--bronze);padding:3px 8px;border-radius:5px;font-weight:600;white-space:nowrap}
.chain-arr{color:var(--ink3);font-weight:700}
.recipe-out{font-size:.8125rem;color:var(--ink2);margin-bottom:7px;line-height:1.5}
.recipe-out b{color:var(--ink);font-weight:700}
.recipe-val{font-size:.8125rem;color:var(--green);font-weight:700;background:var(--green-soft);border-radius:6px;padding:6px 10px}
/* Ideas */
.ideas{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}
.idea{background:var(--surface);border:1px solid var(--border);border-top:3px solid var(--bronze);border-radius:12px;padding:18px 20px;box-shadow:var(--shadow)}
.idea-h{display:flex;align-items:center;gap:9px;margin-bottom:9px}
.idea-icon{font-size:1.25rem}
.idea-title{font-size:.9375rem;font-weight:700;color:var(--ink);flex:1}
.idea-rev{font-size:.625rem;font-weight:800;background:var(--green-soft);color:var(--green);border:1px solid var(--green);padding:3px 8px;border-radius:4px;white-space:nowrap}
.idea-desc{font-size:.8125rem;color:var(--ink2);margin-bottom:10px;line-height:1.5}
.idea-tags{display:flex;flex-wrap:wrap;gap:5px}
.idea-tag{font-size:.625rem;background:var(--bg2);color:var(--ink3);border:1px solid var(--border2);padding:2px 7px;border-radius:4px}
/* Conflicts */
.conflicts{display:grid;grid-template-columns:repeat(auto-fill,minmax(450px,1fr));gap:16px}
.conflict{background:var(--surface);border:1px solid var(--border);border-right:4px solid var(--red);border-radius:12px;padding:20px 22px;box-shadow:var(--shadow)}
.conflict-h{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;font-size:.9375rem;font-weight:700;color:var(--red);gap:8px}
.sev-high{font-size:.625rem;font-weight:800;text-transform:uppercase;background:var(--red-soft);color:var(--red);border:1px solid var(--red);padding:3px 9px;border-radius:4px;white-space:nowrap}
.sev-med{font-size:.625rem;font-weight:800;text-transform:uppercase;background:rgba(138,109,0,.08);color:var(--amber);border:1px solid var(--amber);padding:3px 9px;border-radius:4px;white-space:nowrap}
.conflict-vs{display:flex;gap:6px;align-items:center;flex-wrap:wrap;margin-bottom:12px}
.vs{font-size:.75rem;background:var(--bg2);color:var(--ink2);padding:4px 10px;border-radius:5px;border:1px solid var(--border2)}
.vs-d{color:var(--ink3)}
.conflict-fix{font-size:.8125rem;color:var(--ink2);background:var(--green-soft);border:1px solid rgba(46,125,82,.25);border-radius:7px;padding:9px 13px;line-height:1.55}
.conflict.resolved{border-right-color:var(--green)}
.conflict.resolved .conflict-h{color:var(--green)}
.sev-ok{font-size:.625rem;font-weight:800;text-transform:uppercase;background:var(--green-soft);color:var(--green);border:1px solid var(--green);padding:3px 9px;border-radius:4px;white-space:nowrap}
.conflict-rule{font-size:.6875rem;color:var(--ink3);margin-top:8px;font-weight:600}
/* Opps grid */
.opps{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}
.opp{background:var(--surface);border:1px solid var(--border);border-right:4px solid var(--blue-ink);border-radius:12px;padding:18px 20px;box-shadow:var(--shadow)}
.opp-h{display:flex;align-items:center;gap:9px;margin-bottom:9px}
.opp-icon{font-size:1.25rem}
.opp-title{font-size:.875rem;font-weight:700;color:var(--ink);flex:1}
.opp-val{font-size:.625rem;font-weight:800;text-transform:uppercase;background:var(--green-soft);color:var(--green);border:1px solid var(--green);padding:3px 8px;border-radius:4px;white-space:nowrap}
.opp-why{font-size:.8125rem;color:var(--ink2);margin-bottom:9px;line-height:1.5}
.opp-how{font-size:.75rem;color:var(--bronze-ink);font-family:Heebo;font-weight:600}
/* Library */
.lib-toggle{background:var(--surface);border:1px solid var(--border2);border-radius:12px;padding:16px 22px;cursor:pointer;display:flex;justify-content:space-between;align-items:center;font-size:.9375rem;font-weight:700;color:var(--ink);box-shadow:var(--shadow)}
.lib-toggle:hover{border-color:var(--bronze)}
.lib-body{display:none;margin-top:6px}
.lib-body.show{display:block}
.lib-cat{margin-bottom:20px}
.lib-cat h4{font-size:.8125rem;color:var(--ink3);margin-bottom:9px;font-weight:700}
/* קבוצות ספרייה (details native) */
.lib-group{border:1px solid var(--border);border-radius:10px;margin-bottom:10px;background:var(--surface);box-shadow:var(--shadow);overflow:hidden}
.lib-group-priority{border-color:var(--bronze);border-right:4px solid var(--bronze)}
.lib-group>summary{padding:13px 18px;cursor:pointer;display:flex;align-items:center;gap:9px;font-size:.9375rem;font-weight:700;color:var(--ink);list-style:none;user-select:none}
.lib-group>summary::-webkit-details-marker{display:none}
.lib-group>summary::before{content:'▶';font-size:.5625rem;color:var(--ink3);transition:transform .2s;flex-shrink:0}
.lib-group[open]>summary::before{transform:rotate(90deg)}
.lib-group>summary:hover{background:var(--surface2)}
.lib-g-label{flex:1}
.lib-count{font-size:.6875rem;font-weight:800;color:var(--bronze-ink);background:var(--bronze-soft);border:1px solid var(--bronze);padding:2px 9px;border-radius:10px}
.lib-rows{padding:4px 14px 12px}
body.hc .lib-group{border-width:2px}
.lib-row{display:flex;gap:12px;align-items:center;padding:8px 12px;border-bottom:1px solid var(--border);font-size:.8125rem;background:var(--surface);border-radius:4px}
.lib-row code{color:var(--bronze-ink);font-family:Heebo;white-space:nowrap;font-weight:600}
.lib-src{font-size:.625rem;color:var(--ink3);text-transform:uppercase;background:var(--bg2);padding:2px 7px;border-radius:4px;font-weight:600}
.lib-parent{font-size:.625rem;color:var(--bronze-ink);background:var(--bronze-soft);border:1px solid var(--bronze);padding:2px 7px;border-radius:4px;font-weight:600;white-space:nowrap}
.lib-desc{color:var(--ink2);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.hidden{display:none!important}
.footer{padding:30px;border-top:1px solid var(--border2);background:var(--surface);text-align:center;font-size:.75rem;color:var(--ink3);margin-top:36px;line-height:1.8}
.footer b{color:var(--bronze-ink)}
.auto-note{background:var(--green-soft);border:1px solid rgba(46,125,82,.3);border-radius:8px;padding:11px 18px;font-size:.8125rem;color:var(--green);margin-top:16px;display:inline-block;font-weight:600}
.copy-cmd{background:none;border:1px solid rgba(46,125,82,.4);border-radius:5px;color:var(--green);font-size:.75rem;padding:2px 7px;cursor:pointer;margin-right:8px;font-family:Heebo;vertical-align:middle}
.copy-cmd:hover{background:var(--green-soft)}
/* ===== ווידג'ט נגישות ===== */
.a11y-btn{position:fixed;bottom:22px;left:22px;width:56px;height:56px;border-radius:50%;background:var(--bronze-ink);color:#fff;border:none;font-size:1.75rem;cursor:pointer;box-shadow:0 6px 20px rgba(43,38,32,.28);z-index:1500;display:flex;align-items:center;justify-content:center}
.a11y-btn:hover{background:var(--bronze)}
.a11y-panel{position:fixed;bottom:88px;left:22px;width:280px;background:var(--surface);border:1px solid var(--border2);border-radius:14px;box-shadow:0 12px 36px rgba(43,38,32,.22);z-index:1500;padding:18px;display:none}
.a11y-panel.show{display:block}
.a11y-panel h3{font-size:.9375rem;font-weight:700;color:var(--ink);margin-bottom:14px;display:flex;align-items:center;gap:8px}
.a11y-row{margin-bottom:12px}
.a11y-label{font-size:.75rem;color:var(--ink3);font-weight:600;margin-bottom:6px;display:block}
.a11y-controls{display:flex;gap:8px}
.a11y-controls button,.a11y-toggle{flex:1;background:var(--surface2);border:1px solid var(--border2);border-radius:8px;color:var(--ink);font-family:Heebo;font-size:.875rem;font-weight:600;padding:10px;cursor:pointer;min-height:44px}
.a11y-controls button:hover,.a11y-toggle:hover{border-color:var(--bronze);color:var(--bronze-ink)}
.a11y-toggle.on{background:var(--bronze-ink);color:#fff;border-color:var(--bronze-ink)}
.a11y-reset{width:100%;background:transparent;border:1px solid var(--border2);border-radius:8px;color:var(--ink3);font-family:Heebo;font-size:.8125rem;padding:9px;cursor:pointer;margin-top:4px;min-height:40px}
.a11y-fs-display{font-size:.75rem;color:var(--ink2);text-align:center;margin-top:6px;font-weight:600}
/* ===== תרחישים מהחיים ===== */
.scenarios{display:grid;grid-template-columns:repeat(auto-fill,minmax(390px,1fr));gap:18px}
.scenario{background:var(--surface);border:1px solid var(--border);border-top:4px solid var(--bronze);border-radius:14px;padding:20px 22px;box-shadow:var(--shadow)}
.scenario-h{display:flex;align-items:flex-start;gap:10px;margin-bottom:6px}
.scenario-icon{font-size:1.5rem;flex-shrink:0}
.scenario-title{font-size:1rem;font-weight:800;color:var(--ink);line-height:1.3}
.scenario-trigger{font-size:.8125rem;color:var(--ink3);margin-bottom:16px;font-style:italic;padding-right:2.1rem}
.scenario-steps{display:flex;flex-direction:column;gap:12px}
.scenario-step{display:grid;grid-template-columns:28px 1fr;gap:8px;align-items:flex-start}
.step-num{width:26px;height:26px;border-radius:50%;background:var(--bronze-ink);color:#fff;font-size:.6875rem;font-weight:800;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:2px}
.step-body{min-width:0}
.step-action{font-size:.8125rem;font-weight:600;color:var(--ink);margin-bottom:5px}
.step-skill{font-size:.625rem;font-weight:800;background:var(--bronze-soft);color:var(--bronze-ink);border:1px solid var(--bronze);padding:2px 8px;border-radius:4px;display:inline-block;margin-bottom:5px}
.step-say-row{display:flex;align-items:center;gap:6px;background:var(--bg2);border-radius:6px;padding:7px 10px;margin-bottom:4px}
.step-say{flex:1;font-size:.8125rem;color:var(--bronze-ink);font-weight:700;font-family:Heebo;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.step-copy{background:var(--surface);border:1px solid var(--border2);border-radius:5px;color:var(--ink3);font-family:Heebo;font-size:.6875rem;font-weight:700;padding:4px 10px;cursor:pointer;white-space:nowrap;flex-shrink:0;min-height:30px}
.step-copy:hover{border-color:var(--bronze);color:var(--bronze-ink)}
.step-get{font-size:.75rem;color:var(--green);background:var(--green-soft);border-radius:5px;padding:5px 9px;line-height:1.45}
.step-get::before{content:'✓ ';font-weight:700}
/* ===== ניווט דביק + חיפוש גלובלי ===== */
.stickyhead{position:sticky;top:0;z-index:100;box-shadow:var(--shadow)}
.search-wrap{position:relative;display:flex;align-items:center;gap:9px}
.search-clear{position:absolute;left:9px;top:50%;transform:translateY(-50%);background:none;border:none;color:var(--ink3);font-size:1.15rem;line-height:1;cursor:pointer;display:none;padding:2px 5px}
.search-clear.show{display:block}
.search-clear:hover{color:var(--red)}
.search-count{font-size:.6875rem;font-weight:800;color:var(--bronze-ink);white-space:nowrap;min-width:0}
/* סרגל ניווט (chips) */
.navbar{background:var(--surface2);border-top:1px solid var(--border);border-bottom:1px solid var(--border2);display:flex;gap:6px;padding:8px 28px;overflow-x:auto;scrollbar-width:thin}
.navbar::-webkit-scrollbar{height:5px}
.navbar::-webkit-scrollbar-thumb{background:var(--border2);border-radius:3px}
.nav-chip{background:transparent;border:1px solid var(--border2);border-radius:20px;padding:5px 13px;font-size:.75rem;font-weight:600;color:var(--ink2);cursor:pointer;font-family:Heebo;white-space:nowrap;transition:.15s}
.nav-chip:hover{border-color:var(--bronze);color:var(--bronze-ink)}
.nav-chip.active{background:var(--bronze-ink);border-color:var(--bronze-ink);color:#fff}
/* אופסט גלילה לעוגנים (גובה ה-stickyhead, מתעדכן ב-JS) */
.section{scroll-margin-top:var(--head-h,128px)}
/* מצב 'לא נמצא' בחיפוש */
.search-empty{display:none;text-align:center;padding:46px 20px;color:var(--ink3);font-size:1.0625rem;font-weight:600}
.search-empty.show{display:block}
/* כפתור חזרה למעלה */
.totop{position:fixed;bottom:22px;right:22px;width:48px;height:48px;border-radius:50%;background:var(--bronze-ink);color:#fff;border:none;font-size:1.35rem;cursor:pointer;box-shadow:0 6px 20px rgba(43,38,32,.28);z-index:1400;display:none;align-items:center;justify-content:center}
.totop.show{display:flex}
.totop:hover{background:var(--bronze)}
body.hc .nav-chip,body.hc .totop{border-width:2px}
/* עצירת אנימציות */
body.no-anim *,body.no-anim *::before,body.no-anim *::after{animation:none!important;transition:none!important}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}}
@media(max-width:700px){.hero h1{font-size:1.75rem}.search{width:150px}.section{padding:24px 16px}.conflicts{grid-template-columns:1fr}.a11y-panel{width:calc(100vw - 44px)}.navbar{padding:7px 16px}.topbar{padding:12px 16px}.totop{bottom:84px;right:16px;width:44px;height:44px}}
</style>
</head>
<body>
<a href="#main" class="skip">דלג לתוכן הראשי</a>
<div class="stickyhead">
<div class="topbar">
  <div class="brand">RON DIGITAL STUDIO</div>
  <div class="search-wrap">
    <input class="search" id="search" type="search" aria-label="חיפוש חופשי בכל המפה" placeholder="🔍 חפש בכל המפה..." oninput="doSearch(this.value)">
    <button class="search-clear" id="searchClear" type="button" aria-label="נקה חיפוש" onclick="clearSearch()">×</button>
    <span class="search-count" id="searchCount" aria-live="polite"></span>
  </div>
  <div class="updated">עודכן: ${buildDate}</div>
</div>
<nav class="navbar" id="navbar" aria-label="ניווט מהיר בין סקשנים"></nav>
</div>
<main id="main">

<div class="hero">
  <h1>מפת <b>הסקילים</b> שלי</h1>
  <p>מערכת חיה — כל סקיל חדש מתווסף אוטומטית. מנוע הזדמנויות + מדריך "איזה סקיל מתי"</p>
  <div class="stats">
    <div class="stat"><div class="stat-n">${stats.business}</div><div class="stat-l">סקילים עסקיים</div></div>
    <div class="stat"><div class="stat-n">${stats.localTotal}</div><div class="stat-l">סקילים בספרייה</div></div>
    <div class="stat"><div class="stat-n">${stats.opportunities}</div><div class="stat-l">הזדמנויות</div></div>
    <div class="stat"><div class="stat-n">${resolvedCount}/${stats.conflicts}</div><div class="stat-l">חפיפות פתורות</div></div>
    <div class="stat"><div class="stat-n">${stats.uncategorized}</div><div class="stat-l">ממתינים לסיווג</div></div>
  </div>
  <div class="auto-note">🔄 המפה נבנית אוטומטית ב-SessionStart. ריענון ידני: <b>/update-map</b> <button class="copy-cmd" onclick="cpCmd(this,'/update-map')" title="העתק פקודה">📋</button></div>
  <div style="margin-top:12px"><a class="menu-link" href="ron-service-menu.html" target="_blank">📄 פתח תפריט שירותים ללקוח</a></div>
</div>

<!-- PERSONAL: shortcuts + usage -->
<div class="section" id="personalSection" data-nav="⭐ שלי" style="display:none">
  <div class="section-t"><h2>⭐ הקיצורים שלי</h2><div class="line"></div></div>
  <div class="favs" id="favsBox"></div>
  <div class="usage-grid">
    <div class="usage-col">
      <h3 class="usage-h">📊 הסקילים שלך</h3>
      <div id="topBox" class="usage-list"></div>
    </div>
    <div class="usage-col">
      <h3 class="usage-h">🕸️ לא נגעת בהם</h3>
      <div id="forgotBox" class="usage-list"></div>
    </div>
  </div>
</div>

<!-- NEEDS MATCHER -->
<div class="section" id="sec-needs" data-nav="🎯 מה צריך">
  <div class="wizard">
    <h2>🎯 מה אתה צריך?</h2>
    <p class="need-sub">תאר במילים שלך מה אתה רוצה לעשות — ואני אבדוק אם יש לך סקיל מתאים, ואם לא — מה ההמלצה.</p>
    <div class="need-box">
      <input id="needInput" type="text" aria-label="תאר את הצורך שלך" placeholder="למשל: לשלוח תזכורות ללקוחות שלא ענו" onkeydown="if(event.key==='Enter')analyzeNeed(this.value)">
      <button class="need-btn" onclick="analyzeNeed(document.getElementById('needInput').value)">נתח 🔎</button>
    </div>
    <div class="need-out" id="needOut" aria-live="polite"></div>
    <div class="wizard-divider"><span>או בחר משימה מהירה מהרשימה</span></div>
    <select id="wizard" aria-label="בחר מה אתה רוצה לעשות" onchange="runWizard(this.value)">
      <option value="">— בחר משימה —</option>
      ${wizardOptions}
    </select>
    <div class="wizard-out" id="wizardOut">
      <div class="wizard-skill" id="wzSkill"></div>
      <div class="wizard-say" id="wzSay"></div>
      <div class="wizard-note" id="wzNote"></div>
    </div>
  </div>
</div>

<!-- SPARK -->
<div class="section">
  <div class="spark">
    <div class="spark-left">
      <div class="spark-tag">🎲 הברקה יצירתית</div>
      <div class="spark-text" id="sparkText">לחץ על הכפתור לרעיון אקראי שמשלב סקילים בדרך מפתיעה</div>
    </div>
    <button class="spark-btn" onclick="randomSpark()">🎲 תן לי רעיון</button>
  </div>
</div>

<!-- OPPORTUNITY OF THE WEEK -->
<div class="section" id="sec-oow" data-nav="💡 השבוע">
  <div class="oow">
    <div class="oow-tag">💡 הזדמנות השבוע</div>
    <div class="oow-title" id="oowTitle"></div>
    <div class="oow-why" id="oowWhy"></div>
    <div class="oow-how" id="oowHow"></div>
  </div>
</div>

<!-- CHEAT SHEET -->
<div class="section" id="sec-cheat" data-nav="⚡ Cheat" data-searchable>
  <div class="section-t"><h2>⚡ Cheat Sheet — הכי בשימוש</h2><div class="line"></div></div>
  <div class="cheats">${cheatHtml}</div>
</div>

<!-- SCENARIOS -->
<div class="section" id="sec-scenarios" data-nav="🎬 תרחישים" data-searchable>
  <div class="section-t"><h2>🎬 תרחישים מהחיים — מה עושים בכל מצב</h2><div class="line"></div></div>
  <p class="sec-intro">6 סיטואציות אמיתיות מהעסק. לכל שלב: איזה סקיל, מה אומרים לקלוד (להעתקה ישירה), ומה מקבלים בסוף.</p>
  <div class="scenarios">${scenariosHtml}</div>
</div>

<!-- RECIPES -->
<div class="section" id="sec-recipes" data-nav="🔗 מתכונים" data-searchable>
  <div class="section-t"><h2>🔗 מתכונים — שרשראות סקילים</h2><div class="line"></div></div>
  <p class="sec-intro">הכוח האמיתי הוא בשילוב. כל מתכון שוזר כמה סקילים לתוצר עסקי אחד גדול. קרא משמאל לימין: סקיל ← סקיל ← סקיל.</p>
  <div class="recipes">${recipesHtml}</div>
</div>

<!-- CHECKLISTS -->
<div class="section" id="sec-checklists" data-nav="✅ צ'קליסטים">
  <div class="section-t"><h2>✅ צ'קליסטים לתהליכים חוזרים</h2><div class="line"></div></div>
  <p class="sec-intro">תהליכים שאתה עושה שוב ושוב — עם תיוק התקדמות שנשמר. כל שלב מקושר לסקיל הרלוונטי.</p>
  <div class="checklists">${checklistsHtml}</div>
</div>

<!-- BUSINESS SKILLS -->
<div class="section" id="sec-skills" data-nav="🗂️ סקילים" data-searchable>
  <div class="section-t"><h2>הסקילים העסקיים — לפי קטגוריה</h2><div class="line"></div></div>
  <div class="tabs">${tabsHtml}</div>
  <div id="cards">${cardsHtml}</div>
</div>

<!-- CONFLICTS -->
<div class="section" id="sec-conflicts" data-nav="🧭 ניתוב" data-searchable>
  <div class="section-t"><h2>🧭 ניתוב בין סקילים חופפים (פתור)</h2><div class="line"></div></div>
  <p style="font-size:.8125rem;color:var(--ink3);margin-bottom:18px;margin-top:-8px">סקילים שיכולים להיתפס על אותה בקשה — לכל אחד כלל ניתוב ברור ב-CLAUDE.md. אלה לא באגים, אלא יכולות משלימות עם מסלול החלטה.</p>
  <div class="conflicts">${conflictsHtml}</div>
</div>

<!-- OPPORTUNITIES -->
<div class="section" id="sec-opps" data-nav="🌑 הזדמנויות" data-searchable>
  <div class="section-t"><h2>🌑 כל ההזדמנויות העסקיות</h2><div class="line"></div></div>
  <div class="opps">${oppsHtml}</div>
</div>

<!-- BUILD IDEAS -->
<div class="section" id="sec-ideas" data-nav="💡 רעיונות" data-searchable>
  <div class="section-t"><h2>💡 מה עוד אפשר לבנות</h2><div class="line"></div></div>
  <p class="sec-intro">מוצרים ושירותים שאפשר להרכיב מהסקילים שכבר יש לך. כל רעיון עם הסקילים הדרושים ופוטנציאל ההכנסה.</p>
  <div class="ideas">${buildIdeasHtml}</div>
</div>

<!-- FULL LIBRARY -->
<div class="section" id="sec-library" data-nav="📚 ספרייה" data-searchable>
  <div class="section-t"><h2>📚 ספרייה מלאה — לפי תחום</h2><div class="line"></div></div>
  <p class="sec-intro">${allUncurated.length} סקילים שהתגלו אוטומטית, מקובצים לפי תחום. הקבוצות שמעניינות אותך (שיווק · מכירות · פרודוקטיביות) פתוחות בראש; מדע/אבטחה/משחקים מקופלים. לחץ על קבוצה כדי לפתוח. בכל שורה: השם + "מתי משתמשים".</p>
  <div class="lib-body show" id="libBody">${libHtml}</div>
</div>

<div class="search-empty" id="searchEmpty" aria-live="polite">🔍 לא נמצאו תוצאות — נסה ניסוח אחר, או תאר את הצורך ב"🎯 מה צריך"</div>

</main>

<button class="totop" id="toTop" type="button" aria-label="חזרה לראש העמוד" onclick="scrollToTop()">↑</button>

<div class="footer">
  מפת סקילים חיה של <b>RON DIGITAL STUDIO</b> · נבנתה ב-${buildDate} · גרסה ${data.meta.version}<br>
  כדי להעשיר סקיל בידע עסקי: ערוך את <b>~/.claude/skill-map/skill-map-data.json</b>
</div>

<!-- ווידג'ט נגישות -->
<button class="a11y-btn" id="a11yBtn" aria-label="פתח תפריט נגישות" aria-expanded="false" onclick="toggleA11y()">♿</button>
<div class="a11y-panel" id="a11yPanel" role="dialog" aria-label="הגדרות נגישות">
  <h3>♿ נגישות</h3>
  <div class="a11y-row">
    <span class="a11y-label">גודל טקסט</span>
    <div class="a11y-controls">
      <button onclick="fontStep(-1)" aria-label="הקטן טקסט">A−</button>
      <button onclick="fontStep(1)" aria-label="הגדל טקסט">A+</button>
    </div>
    <div class="a11y-fs-display" id="fsDisplay">100%</div>
  </div>
  <div class="a11y-row">
    <span class="a11y-label">תצוגה</span>
    <button class="a11y-toggle" id="hcToggle" onclick="toggleHC()" aria-pressed="false">מצב ניגודיות גבוהה</button>
  </div>
  <div class="a11y-row">
    <button class="a11y-toggle" id="animToggle" onclick="toggleAnim()" aria-pressed="false">עצור אנימציות</button>
  </div>
  <button class="a11y-reset" onclick="resetA11y()">איפוס הגדרות</button>
</div>

<script>
const DATA = ${clientData};
const WEEK = ${weekNum};

// העתקת משפט תרחיש
function copySay(txt,btnId){
  if(navigator.clipboard)navigator.clipboard.writeText(txt);
  const b=document.getElementById(btnId);if(!b)return;
  const o=b.textContent;b.textContent='✓ הועתק';
  setTimeout(()=>{b.textContent=o;},1500);
}

// אשף החלטה
function runWizard(i){
  const out=document.getElementById('wizardOut');
  if(i===''){out.classList.remove('show');return;}
  const r=DATA.decisionRules[i];
  document.getElementById('wzSkill').textContent='הסקיל: '+r.skill;
  document.getElementById('wzSay').textContent='💬 '+r.say;
  document.getElementById('wzNote').textContent=r.note||'';
  out.classList.add('show');
}

// הזדמנות השבוע (רוטציה)
(function(){
  const o=DATA.opportunities[WEEK % DATA.opportunities.length];
  document.getElementById('oowTitle').textContent=o.icon+' '+o.title+' ('+o.value+')';
  document.getElementById('oowWhy').textContent=o.why;
  document.getElementById('oowHow').textContent='▶ '+o.how;
})();

// הברקה אקראית
let lastSpark=-1;
function randomSpark(){
  if(!DATA.sparks||!DATA.sparks.length)return;
  let i=Math.floor(Math.random()*DATA.sparks.length);
  if(DATA.sparks.length>1){while(i===lastSpark)i=Math.floor(Math.random()*DATA.sparks.length);}
  lastSpark=i;
  document.getElementById('sparkText').textContent=DATA.sparks[i];
}

// ===== מתאם צרכים (offline) — בנייה בטוחה עם DOM (textContent, ללא HTML גולמי) =====
const STOP=new Set(['אני','צריך','צריכה','רוצה','של','עם','את','על','מה','איך','לי','יש','אם','או','גם','כדי','בשביל','זה','זו','הם','כל','עוד','כבר','הכי','יותר','לעשות','בלי','לא','כן','אבל','מתי','איפה','למי','משהו','דרך','the','to','for','and','need','want','my','how','what','a','an']);
function tokenize(s){
  return (s||'').toLowerCase()
    .replace(/[֑-ׇ]/g,'')
    .replace(/[^\\u0590-\\u05FF0-9a-z ]+/gi,' ')
    .split(/\\s+/).filter(t=>t.length>=2 && !STOP.has(t));
}
const TYPE_LABEL={skill:'סקיל שלך',rule:'משימה מוכרת',recipe:'מתכון',lib:'בספרייה'};
function el(tag,cls,txt){const n=document.createElement(tag);if(cls)n.className=cls;if(txt!=null)n.textContent=txt;return n;}
function resCard(name,typeLabel,say){
  const c=el('div','need-res');
  const h=el('div','need-res-name',name+' ');
  if(typeLabel)h.appendChild(el('span','need-res-type',typeLabel));
  c.appendChild(h);
  if(say)c.appendChild(el('div','need-res-say',say));
  return c;
}
function analyzeNeed(q){
  const out=document.getElementById('needOut');
  out.classList.add('show');
  out.replaceChildren();
  const toks=tokenize(q);
  if(!toks.length){out.appendChild(el('div','need-empty','תאר מה אתה צריך — למשל "לשלוח תזכורות ללקוחות שלא ענו" או "דף נחיתה לעסק"'));return;}
  const scored=(DATA.searchIndex||[]).map(e=>{
    const lt=(e.label||'').toLowerCase(),tt=(e.text||'').toLowerCase();
    let sc=0,hits=0;
    toks.forEach(t=>{
      if(lt.includes(t)){sc+=(e.t==='rule'||e.t==='skill')?5:3;hits++;}
      else if(tt.includes(t)){sc+=(e.t==='lib')?1:2;hits++;}
    });
    if(hits>1)sc+=hits;
    return {e,sc};
  }).filter(x=>x.sc>0).sort((a,b)=>b.sc-a.sc);
  const seen=new Set(),top=[];
  for(const x of scored){if(seen.has(x.e.id))continue;seen.add(x.e.id);top.push(x);if(top.length>=4)break;}
  // גשר ל-which-skill
  function bridge(){
    const b=el('div','need-bridge');
    b.appendChild(document.createTextNode('למענה מדויק יותר, תאר לקלוד: '));
    b.appendChild(el('code',null,'/which-skill '+q));
    const btn=el('button','need-copy','📋 העתק פקודה');
    btn.onclick=function(){if(navigator.clipboard)navigator.clipboard.writeText('/which-skill '+q);btn.textContent='✓ הועתק';};
    b.appendChild(el('br'));b.appendChild(btn);
    return b;
  }
  if(!top.length){
    out.appendChild(el('div','need-head no','🤔 לא נמצא סקיל מתאים'));
    out.appendChild(resCard('ההמלצה שלי: ליצור סקיל חדש','','Skill: skill-creator — תאר את הצורך וקלוד יבנה סקיל מותאם'));
    out.appendChild(bridge());return;
  }
  const topScore=top[0].sc;
  out.appendChild(el('div','need-head '+(topScore>=5?'ok':'maybe'), topScore>=5?'✅ יש לך סקיל מתאים':'🤔 אין התאמה מדויקת — הכי קרוב אצלך'));
  top.forEach(x=>{const e=x.e;const say=e.say?('💬 '+e.say):(e.invoke||'');out.appendChild(resCard(e.label,TYPE_LABEL[e.t]||'',say));});
  if(topScore<5)out.appendChild(resCard('או: ליצור סקיל ייעודי','','Skill: skill-creator'));
  out.appendChild(bridge());
}

// ===== אישי: מועדפים, שימוש, צ'קליסטים (localStorage) =====
function getFavs(){try{return JSON.parse(lsGet('fav')||'[]');}catch(e){return [];}}
function setFavs(a){lsSet('fav',JSON.stringify(a));}
function getUsage(){try{return JSON.parse(lsGet('usage')||'{}');}catch(e){return {};}}
function setUsage(u){lsSet('usage',JSON.stringify(u));}
function bizById(id){return (DATA.bizSkills||[]).find(s=>s.id===id);}
function toggleFav(id,btn){
  const f=getFavs();const i=f.indexOf(id);
  if(i>=0){f.splice(i,1);if(btn){btn.classList.remove('on');btn.textContent='☆';}}
  else{f.push(id);if(btn){btn.classList.add('on');btn.textContent='★';}}
  setFavs(f);renderPersonal();
}
function copyTrigger(id,btn){
  const card=document.querySelector('.card[data-id="'+(window.CSS&&CSS.escape?CSS.escape(id):id)+'"]');
  const say=card?card.getAttribute('data-say'):id;
  if(navigator.clipboard)navigator.clipboard.writeText(say);
  if(btn){const o=btn.textContent;btn.textContent='✓ הועתק';setTimeout(()=>{btn.textContent=o;},1500);}
  const u=getUsage();u[id]=u[id]||{c:0,last:0};u[id].c++;u[id].last=Date.now();setUsage(u);
  renderPersonal();
}
function renderPersonal(){
  const favs=getFavs(),usage=getUsage();
  const fb=document.getElementById('favsBox');if(!fb)return;
  fb.replaceChildren();
  if(!favs.length)fb.appendChild(el('div','fav-empty','עדיין אין מועדפים — לחץ על ☆ בכרטיסייה כדי להוסיף קיצור'));
  favs.forEach(id=>{const s=bizById(id)||{label:id,say:id,emoji:''};
    const chip=el('div','fav-chip');chip.appendChild(el('span','fc-name',(s.emoji?s.emoji+' ':'')+s.label));
    const cp=el('button',null,'📋');cp.onclick=function(){if(navigator.clipboard)navigator.clipboard.writeText(s.say);cp.textContent='✓';setTimeout(()=>{cp.textContent='📋';},1200);};
    chip.appendChild(cp);fb.appendChild(chip);});
  const tb=document.getElementById('topBox');tb.replaceChildren();
  const used=Object.keys(usage).sort((a,b)=>usage[b].c-usage[a].c).slice(0,6);
  if(!used.length)tb.appendChild(el('div','fav-empty','התחל להשתמש — כל לחיצת 📋 נספרת כאן'));
  used.forEach(id=>{const s=bizById(id)||{label:id,emoji:''};const it=el('div','usage-item');
    it.appendChild(el('span','ui-name',(s.emoji?s.emoji+' ':'')+s.label));
    it.appendChild(el('span','ui-count',usage[id].c+'×'));tb.appendChild(it);});
  const fgb=document.getElementById('forgotBox');fgb.replaceChildren();
  const MS30=30*86400000,now=Date.now();
  const forgotten=(DATA.bizSkills||[]).filter(s=>{const u=usage[s.id];return !u||u.c===0||(now-u.last)>MS30;}).slice(0,6);
  forgotten.forEach(s=>{const it=el('div','usage-item');
    it.appendChild(el('span','ui-name',(s.emoji?s.emoji+' ':'')+s.label));
    const b=el('button',null,'📋 נסה');b.onclick=function(){if(navigator.clipboard)navigator.clipboard.writeText(s.say);b.textContent='✓';setTimeout(()=>{b.textContent='📋 נסה';},1200);};
    it.appendChild(b);fgb.appendChild(it);});
  const sec=document.getElementById('personalSection');if(sec)sec.style.display='block';
}
function toggleStep(ci,si,inp){lsSet('chk-'+ci+'-'+si,inp.checked?'1':'');}
function resetChecklist(ci,n){for(let si=0;si<n;si++){lsDel('chk-'+ci+'-'+si);const b=document.getElementById('chk-'+ci+'-'+si);if(b)b.checked=false;}}
(function(){
  const favs=getFavs();
  document.querySelectorAll('.card').forEach(c=>{const id=c.getAttribute('data-id');const btn=c.querySelector('.card-fav');if(btn&&favs.indexOf(id)>=0){btn.classList.add('on');btn.textContent='★';}});
  document.querySelectorAll('.checklist-steps input[type=checkbox]').forEach(inp=>{if(lsGet(inp.id)==='1')inp.checked=true;});
  renderPersonal();
})();

// פילטר קטגוריה
let activeCat='all';
function filterCat(cat,el){
  activeCat=cat;
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  el.classList.add('active');
  doSearch(document.getElementById('search').value); // doSearch מטפל בהסתרת cat-group לפי הטאב
}

// ===== חיפוש גלובלי — כל הסקשנים =====
const SEARCH_SEL='.card,.scenario,.recipe,.opp,.idea,.conflict,.cheat,.lib-row';
function doSearch(q){
  q=(q||'').trim().toLowerCase();
  document.getElementById('searchClear').classList.toggle('show',!!q);
  let count=0;
  // רמת פריט: סינון לפי טקסט (כרטיסיות שומרות גם על פילטר הקטגוריה הפעיל)
  document.querySelectorAll(SEARCH_SEL).forEach(it=>{
    const isCard=it.classList.contains('card');
    const catOk=!isCard||activeCat==='all'||it.dataset.cat===activeCat;
    const txt=((it.dataset.name||'')+' '+it.textContent).toLowerCase();
    const show=catOk&&(!q||txt.includes(q));
    it.classList.toggle('hidden',!show);
    if(show&&q)count++;
  });
  if(q)document.getElementById('libBody').classList.add('show');
  // קבוצות הספרייה (details): בחיפוש פותחים קבוצות עם תוצאה, אחרת חוזרים למצב ברירת-מחדל
  document.querySelectorAll('.lib-group').forEach(d=>{
    d.open = q ? [...d.querySelectorAll('.lib-row')].some(r=>!r.classList.contains('hidden')) : d.hasAttribute('data-defopen');
  });
  // קבוצות-קטגוריה (בתוך סקשן הסקילים): מוסתרות אם לא תואמות לטאב, או ריקות בחיפוש
  document.querySelectorAll('.cat-group').forEach(g=>{
    const tabOk=activeCat==='all'||g.dataset.group===activeCat;
    const has=g.querySelector('.card:not(.hidden)');
    g.classList.toggle('hidden',!tabOk||(!!q&&!has));
  });
  // רמת סקשן: בחיפוש מסתירים סקשנים ריקים, ואת אלה שאינם ניתנים לחיפוש
  document.querySelectorAll('.section').forEach(sec=>{
    if(sec.hasAttribute('data-searchable')){
      const has=[...sec.querySelectorAll(SEARCH_SEL)].some(it=>!it.classList.contains('hidden'));
      sec.classList.toggle('hidden',!!q&&!has);
    }else{
      sec.classList.toggle('hidden',!!q);
    }
  });
  // ספירה + מצב 'לא נמצא'
  document.getElementById('searchCount').textContent=q?(count+' '+(count===1?'תוצאה':'תוצאות')):'';
  document.getElementById('searchEmpty').classList.toggle('show',!!q&&count===0);
  syncNavVisibility();
}
function clearSearch(){
  const s=document.getElementById('search');s.value='';doSearch('');s.focus();
}

// ===== ניווט מהיר (TOC) + scroll-spy =====
let navObserver=null;
function buildNav(){
  const bar=document.getElementById('navbar');if(!bar)return;
  bar.replaceChildren();
  const secs=[...document.querySelectorAll('.section[data-nav]')].filter(s=>s.offsetParent!==null);
  secs.forEach(sec=>{
    const b=document.createElement('button');
    b.className='nav-chip';b.type='button';
    b.textContent=sec.getAttribute('data-nav');
    b.dataset.target=sec.id;
    b.setAttribute('aria-label','עבור אל '+sec.getAttribute('data-nav'));
    b.onclick=function(){sec.scrollIntoView({behavior:'smooth',block:'start'});};
    bar.appendChild(b);
  });
  const head=document.querySelector('.stickyhead');
  const headH=head?head.offsetHeight:120;
  document.documentElement.style.setProperty('--head-h',(headH+12)+'px');
  if(navObserver)navObserver.disconnect();
  navObserver=new IntersectionObserver(function(entries){
    entries.forEach(function(en){if(en.isIntersecting)markChip(en.target.id);});
  },{rootMargin:'-'+(headH+5)+'px 0px -65% 0px',threshold:0});
  secs.forEach(function(s){navObserver.observe(s);});
}
function markChip(id){
  document.querySelectorAll('.nav-chip').forEach(function(c){
    c.classList.toggle('active',c.dataset.target===id);
  });
}
function syncNavVisibility(){
  // הסתרת chips של סקשנים שמוסתרים (למשל בזמן חיפוש)
  document.querySelectorAll('.nav-chip').forEach(function(c){
    const sec=document.getElementById(c.dataset.target);
    c.classList.toggle('hidden',!sec||sec.classList.contains('hidden'));
  });
}

// ===== חזרה לראש העמוד =====
function scrollToTop(){window.scrollTo({top:0,behavior:'smooth'});}
(function(){
  const tt=document.getElementById('toTop');if(!tt)return;
  window.addEventListener('scroll',function(){
    tt.classList.toggle('show',window.scrollY>400);
  },{passive:true});
  // חישוב מחדש של גובה ה-header וסרגל הניווט בשינוי גודל מסך (debounced)
  let rzTimer;
  window.addEventListener('resize',function(){clearTimeout(rzTimer);rzTimer=setTimeout(buildNav,200);},{passive:true});
})();

// העתקת פקודה מהירה
function cpCmd(btn,cmd){if(navigator.clipboard)navigator.clipboard.writeText(cmd);const o=btn.textContent;btn.textContent='✓';setTimeout(()=>{btn.textContent=o;},1500);}

// מקש / מתמקד בחיפוש
document.addEventListener('keydown',e=>{if(e.key==='/'&&document.activeElement.tagName!=='INPUT'&&document.activeElement.tagName!=='SELECT'){e.preventDefault();document.getElementById('search').focus();}});

// ===== ווידג'ט נגישות =====
const A11Y={fs:'a11y-fs',hc:'a11y-hc',anim:'a11y-anim'};
function lsGet(k){try{return localStorage.getItem(k);}catch(e){return null;}}
function lsSet(k,v){try{localStorage.setItem(k,v);}catch(e){}}
function lsDel(k){try{localStorage.removeItem(k);}catch(e){}}

function toggleA11y(){
  const p=document.getElementById('a11yPanel'),b=document.getElementById('a11yBtn');
  const open=p.classList.toggle('show');
  b.setAttribute('aria-expanded',open?'true':'false');
}
let fsLevel=parseInt(lsGet(A11Y.fs)||'100',10);
function applyFs(){
  document.documentElement.style.fontSize=fsLevel+'%';
  document.getElementById('fsDisplay').textContent=fsLevel+'%';
  lsSet(A11Y.fs,fsLevel);
}
function fontStep(dir){
  fsLevel=Math.min(150,Math.max(85,fsLevel+dir*10));
  applyFs();
}
function toggleHC(){
  const on=document.body.classList.toggle('hc');
  const t=document.getElementById('hcToggle');
  t.classList.toggle('on',on);t.setAttribute('aria-pressed',on?'true':'false');
  on?lsSet(A11Y.hc,'1'):lsDel(A11Y.hc);
}
function toggleAnim(){
  const on=document.body.classList.toggle('no-anim');
  const t=document.getElementById('animToggle');
  t.classList.toggle('on',on);t.setAttribute('aria-pressed',on?'true':'false');
  on?lsSet(A11Y.anim,'1'):lsDel(A11Y.anim);
}
function resetA11y(){
  fsLevel=100;applyFs();
  document.body.classList.remove('hc','no-anim');
  document.getElementById('hcToggle').classList.remove('on');
  document.getElementById('animToggle').classList.remove('on');
  document.getElementById('hcToggle').setAttribute('aria-pressed','false');
  document.getElementById('animToggle').setAttribute('aria-pressed','false');
  lsDel(A11Y.hc);lsDel(A11Y.anim);lsDel(A11Y.fs);
}
// שחזור הגדרות בטעינה
(function(){
  applyFs();
  if(lsGet(A11Y.hc)){document.body.classList.add('hc');const t=document.getElementById('hcToggle');t.classList.add('on');t.setAttribute('aria-pressed','true');}
  if(lsGet(A11Y.anim)){document.body.classList.add('no-anim');const t=document.getElementById('animToggle');t.classList.add('on');t.setAttribute('aria-pressed','true');}
})();

// אתחול סרגל הניווט — בסוף, אחרי שכל ההגדרות (כולל גודל פונט) שוחזרו וגובה ה-header סופי
buildNav();
</script>
</body>
</html>`;

writeFileSync(OUTPUT, html, 'utf8');
console.log(`✅ skill-map.html נבנה: ${OUTPUT}`);
console.log(`   ${stats.business} עסקיים · ${stats.localTotal} בספרייה · ${stats.uncategorized} לא מסווגים · ${stats.opportunities} הזדמנויות`);

// ── תפריט שירותים ללקוח (קובץ נפרד, להדפסה/שיתוף) ──
const sm = data.serviceMenu;
if (sm) {
  const OUTPUT2 = join(HOME, 'Desktop', 'ron-service-menu.html');
  const groupsHtml = (sm.groups || []).map(g => {
    const items = g.items.map(it =>
      `<tr><td class="sm-name">${esc(it.name)}</td><td class="sm-benefit">${esc(it.benefit)}</td><td class="sm-price">${esc(it.price)}</td></tr>`).join('');
    return `<div class="sm-group"><h2>${esc(g.title)}</h2><table class="sm-table">${items}</table></div>`;
  }).join('');
  const smHtml = `<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RON DIGITAL STUDIO — תפריט שירותים</title>
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Heebo',Arial,sans-serif;background:#F4F2ED;color:#2B2620;direction:rtl;line-height:1.6;padding:40px 20px}
.page{max-width:820px;margin:0 auto;background:#fff;border:1px solid #E2DDD2;border-radius:16px;overflow:hidden;box-shadow:0 10px 40px rgba(43,38,32,.1)}
.head{background:linear-gradient(135deg,#2B2620,#5C5448);color:#fff;padding:40px 44px;text-align:center}
.head .brand{font-size:13px;letter-spacing:4px;text-transform:uppercase;color:#E8D9BB;font-weight:700;margin-bottom:10px}
.head h1{font-size:30px;font-weight:300;margin-bottom:8px}
.head h1 b{font-weight:800;color:#E8D9BB}
.head .tag{font-size:15px;opacity:.85;font-weight:300}
.body{padding:36px 44px}
.sm-group{margin-bottom:32px}
.sm-group h2{font-size:13px;font-weight:800;letter-spacing:2px;text-transform:uppercase;color:#7A5C32;margin-bottom:14px;padding-bottom:8px;border-bottom:2px solid #E2DDD2}
.sm-table{width:100%;border-collapse:collapse}
.sm-table tr{border-bottom:1px solid #EDEAE3}
.sm-table td{padding:13px 0;vertical-align:top}
.sm-name{font-weight:700;font-size:15px;width:32%}
.sm-benefit{color:#5C5448;font-size:13.5px;padding-right:16px!important}
.sm-price{font-weight:800;color:#7A5C32;white-space:nowrap;text-align:left;font-size:14px}
.foot{background:#FBFAF7;border-top:1px solid #E2DDD2;padding:24px 44px;text-align:center;font-size:13px;color:#5C5448}
.foot b{color:#7A5C32}
.cta{display:inline-block;margin-top:8px;background:#2B2620;color:#fff;text-decoration:none;padding:11px 26px;border-radius:50px;font-weight:700;font-size:14px}
.note{max-width:820px;margin:14px auto 0;text-align:center;font-size:12px;color:#8A7F6E}
@media print{body{background:#fff;padding:0}.page{box-shadow:none;border:none}.note,.cta{display:none}}
</style>
</head>
<body>
<div class="page">
  <div class="head">
    <div class="brand">RON DIGITAL STUDIO</div>
    <h1>תפריט <b>שירותים</b></h1>
    <div class="tag">${esc(sm.tagline || '')}</div>
  </div>
  <div class="body">${groupsHtml}</div>
  <div class="foot">
    מחירים כוללים הכל, ללא מע"מ נפרד · הצעה מותאמת אישית בכל פנייה<br>
    <a class="cta" href="https://wa.me/972545700472">דברו איתי בוואטסאפ</a><br>
    <b>RON DIGITAL STUDIO</b> · ronsabon@gmail.com
  </div>
</div>
<div class="note">📄 קובץ זה נוצר אוטומטית מ-skill-map-data.json · להדפסה: Ctrl+P</div>
</body>
</html>`;
  writeFileSync(OUTPUT2, smHtml, 'utf8');
  console.log(`✅ ron-service-menu.html נבנה: ${OUTPUT2}`);
}

# Design Tokens — נקודת חשמל

## עקרון מנחה
**תעשייתי פרמיום** (navy + זהב + שמנת), נגיש לבן 67. הסבר מלא ב-`.impeccable.md` בפרויקט.

## Color palette

### Backgrounds
| Token | Value | Use |
|---|---|---|
| `--c-bg` | `#F5F4EF` | רקע ראשי, שמנת-אופוויט חם |
| `--c-bg-warm` | `#EFEBE0` | רקע PDF preview wrapper (gradient) |
| `--c-surface` | `#FFFFFF` | רקע cards, modal, table cells |
| `--c-surface-2` | `#FAFAF7` | zebra striping, hover עדין |

### Navy (primary)
| Token | Value | Use |
|---|---|---|
| `--c-primary` | `#0A1929` | header, btn-primary, thead, גרדיאנט ב-PDF head |
| `--c-primary-hover` | `#142A42` | hover על btn-primary |
| `--c-primary-soft` | `#1E3A5F` | טקסט סקנדרי, focus border |
| `--c-primary-tint` | `#E5E9EE` | רקע tile-icon, badge רגיל |

### Gold (accent בלבד)
| Token | Value | Use |
|---|---|---|
| `--c-gold` | `#C79A3F` | border-bottom של header, hover line של tile, btn-gold |
| `--c-gold-dark` | `#A07B2D` | hover על btn-gold, טקסט badge-lock |
| `--c-gold-soft` | `#F4ECD8` | רקע badge-lock, hover state ב-table, סיכום פרק ב-PDF |

### Text
| Token | Value | Use |
|---|---|---|
| `--c-text` | `#0F172A` | טקסט ראשי (לא #000!) |
| `--c-text-soft` | `#334155` | טקסט label, body סקנדרי |
| `--c-muted` | `#64748B` | hints, captions |
| `--c-on-primary` | `#F5F4EF` | טקסט על navy (לא #FFF!) |

### Status
| Token | Pair | Use |
|---|---|---|
| `--c-success` `--c-success-soft` | `#14532D` / `#DCFCE7` | badge הצלחה, toast |
| `--c-danger` `--c-danger-soft` | `#991B1B` / `#FEE2E2` | btn-danger, toast |
| `--c-warn` `--c-warn-soft` | `#92400E` / `#FEF3C7` | אזהרות |

## Typography

### Families
- `--ff-sans`: `'Heebo', 'Arial Hebrew', Arial, sans-serif` (default ל-UI)
- `--ff-serif`: `'Frank Ruhl Libre', 'David', 'Times New Roman', serif` (רק לכותרת ה-PDF + h1 פנים-אפליקציה)

### Scale (fluid, clamp)
| Token | Value | Use |
|---|---|---|
| `--fs-xs` | `14px` | badges, captions |
| `--fs-sm` | `16px` | labels, btn-sm, table |
| `--fs-base` | `18px` | body (חובה ≥18 לבן 67) |
| `--fs-md` | `20px` | hero subtitle |
| `--fs-lg` | `clamp(22px, 1.4vw + 16px, 26px)` | h3, tile-title |
| `--fs-xl` | `clamp(28px, 2vw + 18px, 34px)` | h2, page-head h1 |
| `--fs-xxl` | `clamp(36px, 3vw + 20px, 48px)` | h1 hero |
| `--fs-display` | `clamp(40px, 4vw + 24px, 64px)` | סכום סופי גדול ב-PDF |

### Weights
- 400 (regular) - body
- 700 (bold) - כותרות, labels, buttons, table th, badges
- **לא להוסיף 600** (semi-bold) - שומר על hierarchy פשוטה

### Letter spacing
- כותרת H1: `-.02em` (tighter)
- כותרות אחרות: `-.01em`
- thead, badges, eyebrow: `+.02em` to `+.12em` (wider, רושם של caps פורמלי)

## Spacing scale (rhythmic, not uniform)
| Token | Value | Use |
|---|---|---|
| `--sp-1` | 4px | gap בין אייקון לטקסט בתוך כפתור |
| `--sp-2` | 8px | gap בין items סמוכים |
| `--sp-3` | 12px | gap קטן ב-card-row |
| `--sp-4` | 16px | gap סטנדרטי, form rows |
| `--sp-5` | 24px | padding של main, גרידים |
| `--sp-6` | 32px | padding של cards, גובה min ל-section |
| `--sp-7` | 48px | top padding של main, gap בין hero ל-tiles |
| `--sp-8` | 64px | bottom padding של main |

## Elevation (3 רמות בלבד)
| Token | Use |
|---|---|
| `--shadow-sm` | cards, buttons רגילים |
| `--shadow-md` | cards שצוף, btn-gold |
| `--shadow-lg` | modal, tile ב-hover, toast |
| `--shadow-gold` | (לא בשימוש כרגע, מוכן ל-CTAs דרמטיים) |

## Radii
- `--r-sm` 6px (badges, image frames)
- `--r-md` 10px (inputs, buttons)
- `--r-lg` 14px (cards, modal, table-wrap)
- `--r-xl` 18px (לא בשימוש)

## Transitions
- `--t-fast` 120ms - hover על קטנים
- `--t-base` 200ms - card hover, modal in
- `--t-slow` 320ms - לא בשימוש

Easing: `cubic-bezier(.2,.8,.2,1)` - exponential ease-out (לא bounce!).

## כללי שימוש

### זהב
- **רק** כקו דק (1-3px), accent על badge, או רקע של btn יחיד.
- **אף פעם** לא כרקע לשטח גדול.
- **אף פעם** לא לטקסט ארוך (קשה לקריאה).

### Navy
- ראש, thead, btn-primary, footer בלוקים.
- כטקסט: על רקעים בהירים בלבד (לא navy על navy).

### שמנת/אופוויט
- כל הרקעים הראשיים.
- מנע #FFF טהור או #000 טהור.

### Hierarchy (visual)
1. **גודל וצבע**: navy bold גדול = הכי חשוב.
2. **משקל**: 700 לכותרות, 400 לכל השאר.
3. **רווח**: יותר רווח מסביב = יותר חשוב.
4. **זהב**: רק לאחד בכל מסך (CTA / badge מצב).

### A11Y לבן 67 (חובה)
- ניגודיות AA לפחות. נבדק עם DevTools accessibility.
- כל אייקון מלווה טקסט (`<span>טקסט</span>` אחרי האייקון).
- focus-visible: `outline: 3px solid var(--c-gold-soft)`.
- כפתורים min-height 48px. inputs min-height 48px. body 18px.

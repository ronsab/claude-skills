# -*- coding: utf-8 -*-
# מיזוג מצבת משרד המשפטים (גיליון "מכשירים פעילים") עם השלמה מקובץ "מתקן מים"
import openpyxl, warnings, datetime
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
warnings.filterwarnings("ignore")

DIR = "/root/.claude/uploads/2ef5db8b-6650-546a-9720-1f517b3a7ae0"
F_BASE = f"{DIR}/d7a88770-_______________________.xlsx"   # קובץ 2 - בסיס
F_SRC  = f"{DIR}/7477d277-_______________________.xlsx"   # קובץ 1 - מקור השלמה
OUT    = "/home/user/claude-skills/מצבת_משרד_המשפטים_מאוחדת.xlsx"

def norm(v):
    """נרמול מפתח למחרוזת ללא .0 וללא רווחים"""
    if v is None: return ""
    s = str(v).strip()
    if s.endswith(".0"): s = s[:-2]
    return s

# ---- 1. קריאת מקור ההשלמה (קובץ 1, גיליון "מתקן מים") ----
wb_s = openpyxl.load_workbook(F_SRC, read_only=True, data_only=True)
ws_s = wb_s["מתקן מים"]
rows_s = list(ws_s.iter_rows(values_only=True))
hdr_s = [norm(h) for h in rows_s[0]]
def col_s(name):
    for i, h in enumerate(hdr_s):
        if name in h: return i
    raise KeyError(name)
i_serial = col_s("מספר סידורי")
src_cols = {"דגם": col_s("דגם"), "יחידה": col_s("יחידה"), "אתר": col_s("אתר"),
            "עיר": col_s("עיר"), "מיקום": col_s("מיקום"), "כתובת מלאה": col_s("כתובת מלאה")}

src_map = {}
for r in rows_s[1:]:
    key = norm(r[i_serial])
    if not key: continue
    rec = {k: (r[idx] if idx < len(r) and r[idx] is not None else "") for k, idx in src_cols.items()}
    filled = sum(1 for v in rec.values() if str(v).strip() != "")
    # בכפילות - נשמרת הרשומה המלאה ביותר
    if key not in src_map or filled > src_map[key]["_filled"]:
        rec["_filled"] = filled
        src_map[key] = rec
wb_s.close()
print(f"מקור: {len(src_map)} מספרים סידוריים ייחודיים")

# ---- 2. קריאת בסיס (קובץ 2, גיליון "מכשירים פעילים", כותרת שורה 3) ----
wb_b = openpyxl.load_workbook(F_BASE, data_only=True)
ws_b = wb_b["מכשירים פעילים"]
rows_b = list(ws_b.iter_rows(values_only=True))
HDR_ROW = 2  # אינדקס 0-based -> שורה 3
base_hdr = [(h if h is not None else "") for h in rows_b[HDR_ROW]]
ncols = len(base_hdr)
i_tavua = next(i for i, h in enumerate(base_hdr) if "מספר טבוע" in str(h))
base_data = [r for r in rows_b[HDR_ROW+1:] if any(c is not None and str(c).strip() != "" for c in r)]
wb_b.close()
print(f"בסיס: {len(base_data)} שורות מכשירים פעילים")

# ---- 3. בניית חוברת פלט מעוצבת ----
NEW_COLS = ["דגם", "יחידה", "אתר", "עיר", "מיקום (קובץ מתקנים)", "כתובת מלאה (קובץ מתקנים)", "סטטוס התאמה"]
SRC_KEYS = ["דגם", "יחידה", "אתר", "עיר", "מיקום", "כתובת מלאה"]
full_hdr = list(base_hdr) + NEW_COLS
total_cols = len(full_hdr)

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "מצבת מאוחדת"
ws.sheet_view.rightToLeft = True

# צבעים וסגנונות
NAVY   = PatternFill("solid", fgColor="1F3864")
ADDED  = PatternFill("solid", fgColor="DDEBF7")  # תכלת בהיר לעמודות שהושלמו
ZEBRA  = PatternFill("solid", fgColor="F2F6FC")
GREEN  = PatternFill("solid", fgColor="C6EFCE")
RED    = PatternFill("solid", fgColor="FFC7CE")
ORANGE = PatternFill("solid", fgColor="FFEB9C")
TITLEF = PatternFill("solid", fgColor="0F2147")
thin = Side(style="thin", color="BFBFBF")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
HFONT = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
CFONT = Font(name="Calibri", size=10)
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
RIGHT  = Alignment(horizontal="right", vertical="center", wrap_text=True)

# שורת כותרת-על ממוזגת
today = datetime.date.today().strftime("%d/%m/%Y")
ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=total_cols)
t = ws.cell(row=1, column=1, value=f"משרד המשפטים  |  מצבת מתקני שתייה מאוחדת  |  הופק: {today}")
t.fill = TITLEF; t.font = Font(name="Calibri", bold=True, color="FFFFFF", size=16)
t.alignment = Alignment(horizontal="center", vertical="center")
ws.row_dimensions[1].height = 32

# שורת כותרות עמודות (שורה 2)
HROW = 2
for c, name in enumerate(full_hdr, start=1):
    cell = ws.cell(row=HROW, column=c, value=name)
    cell.fill = NAVY; cell.font = HFONT; cell.alignment = CENTER; cell.border = BORDER
ws.row_dimensions[HROW].height = 38

# נתונים
n_done = n_miss = 0
miss_list = []
date_fmt = "dd/mm/yyyy"
for ridx, r in enumerate(base_data):
    excel_row = HROW + 1 + ridx
    key = norm(r[i_tavua])
    rec = src_map.get(key)
    if rec: n_done += 1
    else:
        n_miss += 1
        miss_list.append(key)
    # עמודות הבסיס
    for c in range(total_cols):
        if c < ncols:
            val = r[c] if c < len(r) else None
        elif c < ncols + len(SRC_KEYS):
            val = rec[SRC_KEYS[c - ncols]] if rec else ""
        else:  # עמודת סטטוס התאמה
            val = "הושלם" if rec else "לא נמצא במצבת המתקנים"
        cell = ws.cell(row=excel_row, column=c+1, value=val)
        cell.font = CFONT; cell.alignment = RIGHT; cell.border = BORDER
        if isinstance(val, datetime.datetime):
            cell.number_format = date_fmt
        # רקע
        if ncols <= c < ncols + len(SRC_KEYS):
            cell.fill = ADDED
        elif ridx % 2 == 1:
            cell.fill = ZEBRA
    # צביעת מצב
    try:
        i_matzav = next(i for i, h in enumerate(base_hdr) if str(h).strip() == "מצב")
        mcell = ws.cell(row=excel_row, column=i_matzav+1)
        if str(mcell.value).strip() == "מותקן": mcell.fill = GREEN
        elif str(mcell.value).strip(): mcell.fill = RED
    except StopIteration:
        pass
    # צביעת סטטוס התאמה
    scell = ws.cell(row=excel_row, column=total_cols)
    scell.fill = GREEN if rec else ORANGE
    scell.alignment = CENTER

# הקפאה, פילטר
ws.freeze_panes = f"A{HROW+1}"
ws.auto_filter.ref = f"A{HROW}:{get_column_letter(total_cols)}{HROW+len(base_data)}"

# רוחב עמודות אוטומטי (לפי תוכן, מוגבל)
for c in range(1, total_cols+1):
    letter = get_column_letter(c)
    maxlen = len(str(full_hdr[c-1]))
    for ridx in range(len(base_data)):
        v = ws.cell(row=HROW+1+ridx, column=c).value
        if v is not None:
            maxlen = max(maxlen, len(str(v)))
    ws.column_dimensions[letter].width = min(max(maxlen + 2, 10), 45)

wb.save(OUT)
print(f"נשמר: {OUT}")
print(f"הושלמו: {n_done} | לא נמצאו: {n_miss}")
print("דוגמת לא-נמצאו:", miss_list[:10])

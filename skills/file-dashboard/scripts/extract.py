#!/usr/bin/env python3
"""Universal file extractor for the file-dashboard skill.

Detects the file type by extension and prints a structured, human-readable
summary plus a machine-readable JSON block, so Claude can plan a dashboard
without guessing the file's shape.

Usage:
    python extract.py <path-to-file> [--json-only] [--rows N] [--chars N]

Supports: .xlsx .xls .xlsm .csv .tsv .pdf .docx .txt .md .json
Tabular files work with pandas if present, else fall back to openpyxl (xlsx)
or the stdlib csv module (csv/tsv) — so basic dashboards work with no pandas.
"""
import sys
import os
import json
import argparse

# Ensure Hebrew/UTF-8 survives on any platform (esp. Windows consoles).
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


def _try_import(name, pip_name=None):
    try:
        return __import__(name)
    except ImportError:
        pip = pip_name or name
        print(f"[MISSING DEPENDENCY] '{name}' not installed. Run:  pip install {pip}",
              file=sys.stderr)
        return None


def jdump(obj):
    """Print a JSON block the orchestrator can parse out of stdout."""
    print("\n===JSON_START===")
    print(json.dumps(obj, ensure_ascii=False, default=str, indent=2))
    print("===JSON_END===")


# ---------- column profiling (shared) ----------
def _profile_columns(column_names, records, max_rows, max_chars):
    """Build column_details + head from a header list and a list of row-dicts."""
    from collections import Counter
    cols = []
    for name in column_names:
        values = [r[name] for r in records
                  if r.get(name) is not None and str(r.get(name)).strip() != ""]
        nums = [v for v in values if isinstance(v, (int, float)) and not isinstance(v, bool)]
        info = {
            "name": str(name),
            "dtype": "number" if nums and len(nums) == len(values) else "text",
            "non_null": len(values),
            "nulls": len(records) - len(values),
            "unique": len({str(v) for v in values}),
        }
        if nums and len(nums) == len(values):
            info["min"], info["max"] = min(nums), max(nums)
            info["mean"] = round(sum(nums) / len(nums), 3)
            info["sum"] = round(sum(nums), 3)
        if info["unique"] <= 40 or info["dtype"] == "text":
            info["top_values"] = {str(k): v for k, v in
                                  Counter(str(v) for v in values).most_common(15)}
        info["samples"] = [str(v)[:max_chars] for v in values[:3]]
        cols.append(info)
    head = [{k: str(r.get(k, "")) for k in column_names} for r in records[:max_rows]]
    return cols, head


# ---------- tabular: pandas path ----------
def extract_tabular_pandas(pd, path, ext, max_rows, max_chars):
    if ext in (".csv", ".tsv"):
        sep = "\t" if ext == ".tsv" else ","
        try:
            sheets = {"data": pd.read_csv(path, sep=sep, encoding="utf-8-sig")}
        except UnicodeDecodeError:
            sheets = {"data": pd.read_csv(path, sep=sep, encoding="latin-1")}
    else:
        sheets = pd.read_excel(path, sheet_name=None)

    result = {"type": "tabular", "engine": "pandas", "sheets": {}}
    for sheet_name, df in sheets.items():
        records = df.where(df.notna(), None).to_dict(orient="records")
        cols, head = _profile_columns([str(c) for c in df.columns], records, max_rows, max_chars)
        result["sheets"][str(sheet_name)] = {
            "rows": int(df.shape[0]), "columns": int(df.shape[1]),
            "column_names": [str(c) for c in df.columns],
            "column_details": cols, "head": head}
    return result


# ---------- tabular: stdlib csv fallback ----------
def extract_csv_stdlib(path, ext, max_rows, max_chars):
    import csv as _csv
    delim = "\t" if ext == ".tsv" else ","
    with open(path, encoding="utf-8-sig", errors="replace", newline="") as f:
        rows = list(_csv.reader(f, delimiter=delim))
    if not rows:
        return {"type": "tabular", "error": "empty file"}
    header = [str(h) for h in rows[0]]
    # coerce numeric-looking strings to float
    records = []
    for r in rows[1:]:
        rec = {}
        for i, name in enumerate(header):
            v = r[i] if i < len(r) else None
            if v not in (None, ""):
                try:
                    v = float(v)
                except ValueError:
                    pass
            rec[name] = v
        records.append(rec)
    cols, head = _profile_columns(header, records, max_rows, max_chars)
    return {"type": "tabular", "engine": "stdlib-csv", "sheets": {"data": {
        "rows": len(records), "columns": len(header),
        "column_names": header, "column_details": cols, "head": head}}}


# ---------- tabular: openpyxl fallback ----------
def extract_xlsx_openpyxl(path, max_rows, max_chars):
    openpyxl = _try_import("openpyxl")
    if openpyxl is None:
        return {"type": "tabular",
                "error": "install pandas or openpyxl — run: pip install openpyxl"}
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    result = {"type": "tabular", "engine": "openpyxl", "sheets": {}}
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        if not rows:
            continue
        header = [str(c) if c is not None else f"col{i+1}"
                  for i, c in enumerate(rows[0])]
        records = [dict(zip(header, r)) for r in rows[1:]]
        cols, head = _profile_columns(header, records, max_rows, max_chars)
        result["sheets"][str(ws.title)] = {
            "rows": len(records), "columns": len(header),
            "column_names": header, "column_details": cols, "head": head}
    wb.close()
    if not result["sheets"]:
        return {"type": "tabular", "error": "no data rows found"}
    return result


def extract_tabular(path, ext, max_rows, max_chars):
    pd = _try_import("pandas")
    if pd is not None:
        return extract_tabular_pandas(pd, path, ext, max_rows, max_chars)
    # no pandas — degrade gracefully
    if ext in (".csv", ".tsv"):
        return extract_csv_stdlib(path, ext, max_rows, max_chars)
    if ext in (".xlsx", ".xlsm"):
        return extract_xlsx_openpyxl(path, max_rows, max_chars)
    return {"type": "tabular",
            "error": "pandas required for .xls — run: pip install pandas xlrd"}


# ---------- pdf ----------
def extract_pdf(path, max_chars):
    pdfplumber = _try_import("pdfplumber")
    text_parts, tables = [], []
    n = 0
    if pdfplumber is not None:
        with pdfplumber.open(path) as pdf:
            n = len(pdf.pages)
            for page in pdf.pages:
                t = page.extract_text() or ""
                text_parts.append(t)
                for tbl in (page.extract_tables() or []):
                    tables.append(tbl)
    else:
        pypdf = _try_import("pypdf") or _try_import("PyPDF2")
        if pypdf is None:
            return {"type": "pdf", "error": "install pdfplumber or pypdf"}
        reader = pypdf.PdfReader(path)
        n = len(reader.pages)
        for page in reader.pages:
            text_parts.append(page.extract_text() or "")
    full = "\n".join(text_parts).strip()
    return {
        "type": "pdf",
        "pages": n,
        "char_count": len(full),
        "text": full[:max_chars],
        "tables_found": len(tables),
        "tables_sample": tables[:3],
    }


# ---------- docx ----------
def extract_docx(path, max_chars):
    docx = _try_import("docx", "python-docx")
    if docx is None:
        return {"type": "docx", "error": "install python-docx"}
    d = docx.Document(path)
    paras, headings = [], []
    for p in d.paragraphs:
        txt = p.text.strip()
        if not txt:
            continue
        paras.append(txt)
        if p.style and p.style.name and p.style.name.lower().startswith("heading"):
            headings.append(txt)
    tables = []
    for tbl in d.tables:
        rows = [[c.text for c in row.cells] for row in tbl.rows]
        tables.append(rows)
    full = "\n".join(paras)
    return {
        "type": "docx",
        "char_count": len(full),
        "headings": headings,
        "paragraphs": len(paras),
        "text": full[:max_chars],
        "tables_found": len(tables),
        "tables_sample": tables[:3],
    }


# ---------- plain text / md / json ----------
def extract_text(path, ext, max_chars):
    with open(path, encoding="utf-8-sig", errors="replace") as f:
        content = f.read()
    if ext == ".json":
        try:
            parsed = json.loads(content)
            kind = type(parsed).__name__
            preview = parsed
            if isinstance(parsed, list):
                preview = parsed[:5]
            return {"type": "json", "root_kind": kind,
                    "length": len(parsed) if hasattr(parsed, "__len__") else None,
                    "preview": preview}
        except json.JSONDecodeError:
            pass  # fall through to raw text
    lines = content.splitlines()
    return {
        "type": "text",
        "ext": ext,
        "char_count": len(content),
        "line_count": len(lines),
        "text": content[:max_chars],
    }


def summarize(result):
    """Human-readable digest printed before the JSON block."""
    t = result.get("type")
    print(f"FILE TYPE: {t}  (engine: {result.get('engine', '-')})")
    if result.get("error"):
        print(f"  [ERROR] {result['error']}")
        return
    if t == "tabular":
        for name, sh in result["sheets"].items():
            print(f"\n[SHEET] {name}: {sh['rows']} rows x {sh['columns']} cols")
            print("  columns:", ", ".join(sh["column_names"]))
            for c in sh["column_details"]:
                line = f"  - {c['name']} ({c['dtype']}) unique={c['unique']} nulls={c['nulls']}"
                if "sum" in c:
                    line += f" sum={c['sum']} mean={c['mean']} min={c['min']} max={c['max']}"
                print(line)
                if c.get("top_values"):
                    tops = list(c["top_values"].items())[:5]
                    print("      top:", "; ".join(f"{k}={v}" for k, v in tops))
    elif t in ("pdf", "docx"):
        print(f"  chars={result.get('char_count')} tables={result.get('tables_found')}")
        if result.get("headings"):
            print("  headings:", " | ".join(result["headings"][:15]))
        print("  --- text preview ---")
        print(result.get("text", "")[:1500])
    else:
        print(json.dumps(result, ensure_ascii=False, default=str)[:1500])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--json-only", action="store_true")
    ap.add_argument("--rows", type=int, default=8, help="head rows to keep")
    ap.add_argument("--chars", type=int, default=20000, help="max text chars")
    args = ap.parse_args()

    path = args.path
    if not os.path.exists(path):
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        sys.exit(1)
    ext = os.path.splitext(path)[1].lower()

    if ext in (".xlsx", ".xls", ".xlsm", ".csv", ".tsv"):
        result = extract_tabular(path, ext, args.rows, args.chars)
    elif ext == ".pdf":
        result = extract_pdf(path, args.chars)
    elif ext == ".docx":
        result = extract_docx(path, args.chars)
    elif ext in (".txt", ".md", ".json"):
        result = extract_text(path, ext, args.chars)
    else:
        result = extract_text(path, ext, args.chars)
        result["note"] = f"unknown extension {ext}, read as text"

    result["_file"] = os.path.basename(path)
    if not args.json_only:
        summarize(result)
    jdump(result)


if __name__ == "__main__":
    main()

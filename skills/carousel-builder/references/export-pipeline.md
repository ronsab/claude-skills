# Export Pipeline — HTML → PNG (Playwright)

ייצוא כל שקופית ל-PNG מדויק במידות הקרוסלה (1080×1350 או 1080×1080).
זה השלב הרגיש — רוב הבעיות כאן. עקוב בדיוק.

## דרישה מקדימה: הגש את הקובץ דרך HTTP
Playwright/דפדפן צריך URL, לא `file://` (בעיות פונט/CORS). הרץ שרת סטטי מקומי:
```
npx serve <תיקיית-הקובץ> -p 3999 --no-clipboard
```
(או כל שרת סטטי). ה-URL: `http://localhost:3999/<file>.html`

## שלב 0 (רק אם צריך): שחרור lock על דפדפן
אם Playwright מחזיר `Browser is already in use ... mcp-chrome-XXXX`, יש מופע אוטומציה תקוע.
**סגור רק את תהליך האוטומציה לפי ה-user-data-dir — אל תיגע בכרום האישי:**
```powershell
Get-CimInstance Win32_Process -Filter "Name='chrome.exe'" |
  Where-Object { $_.CommandLine -like '*mcp-chrome*' } |
  ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
```
מזהים את ה-profile המדויק (`mcp-chrome-XXXX`) מתוך הודעת השגיאה ומסננים לפיו.

## שלב 1: navigate + viewport
```
browser_navigate  → http://localhost:3999/<file>.html
browser_resize    → width=1080, height=1350   (או 1080×1080 לריבוע)
```

## שלב 2: לולאת צילום
לכל שקופית n מ-1 עד N:
```
browser_evaluate  → () => { document.body.style.zoom='1'; document.body.style.padding='0';
                            document.body.style.gap='0'; showOnly(n); return n; }
browser_take_screenshot → type=png, filename=slide-0N.png
```
- `showOnly(n)` (מובנה בתבנית) מסתיר את כל השאר → צילום viewport = השקופית בלבד
- אפס zoom/padding/gap על ה-body בשקופית הראשונה (במקרה שהתצוגה הוסיפה אותם)
- ה-viewport בדיוק בגודל השקופית → אין letterbox, אין גלילה

## שלב 3: איסוף וארגון
Playwright שומר ל-CWD (לרוב תיקיית הבית). העבר לתיקייה ייעודית בשם אנגלי (קל לאיתור):
```
mkdir -p "<Desktop>/instagram-carousel"
mv <CWD>/slide-*.png "<Desktop>/instagram-carousel"/
```

## שלב 4: אימות מימדים (PowerShell)
```powershell
Add-Type -AssemblyName System.Drawing
Get-ChildItem "<folder>\*.png" | Sort-Object Name | ForEach-Object {
  $img=[System.Drawing.Image]::FromFile($_.FullName)
  "{0}: {1}x{2} ({3} KB)" -f $_.Name,$img.Width,$img.Height,[math]::Round($_.Length/1KB)
  $img.Dispose() }
```
ודא שכל הקבצים בדיוק 1080×1350 (או 1080×1080). אם לא — בדוק zoom/deviceScaleFactor.

## אם Playwright לא זמין כלל
fallback: דפדפן ידני ב-1080 רוחב, F12 קונסול → `showOnly(n)` → צילום מסך לכל שקופית.
איכות נמוכה יותר (לא pixel-perfect) — העדף תמיד את Playwright.

## תוצר
`slide-01.png` ... `slide-NN.png`, כולן במידה אחידה, מסודרות לפי סדר ההעלאה לקרוסלה.

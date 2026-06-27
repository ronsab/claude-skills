# package_for_claude.ps1
# אורז סקיל מקומי מ-~/.claude/skills לקובץ zip תקין להעלאה ידנית ל-claude.ai.
# מקבע את 3 התיקונים שאומתו: קו נטוי Linux, SKILL.md אחד בשורש, frontmatter בשורה אחת.
#
# שימוש:
#   powershell -File package_for_claude.ps1 -Skills copywriting,write-landing
#   powershell -File package_for_claude.ps1 -Skills (Get-Content list.txt)
#
# פלט: קובץ zip לכל סקיל ב- Documents\phone-skills\  + דוח ולידציה.

param(
  [Parameter(Mandatory=$true)][string[]]$Skills,
  [string]$SkillsDir = "$env:USERPROFILE\.claude\skills",
  [string]$OutDir    = "$env:USERPROFILE\Documents\phone-skills"
)

Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Path $OutDir | Out-Null }

$enc = New-Object System.Text.UTF8Encoding($false)   # UTF-8 ללא BOM
$bs = [char]92; $sl = [char]47

# --- השטחת frontmatter: name/description לשורה אחת single-quoted ---
function Get-FixedSkillMd([string]$path) {
  $raw = [System.IO.File]::ReadAllText($path)
  $lines = $raw -split "`r?`n"
  $dashes = @(); for ($i=0; $i -lt $lines.Count; $i++){ if ($lines[$i].Trim() -eq '---'){ $dashes += $i; if ($dashes.Count -eq 2){break} } }
  if ($dashes.Count -lt 2) { return $raw }   # אין frontmatter - השאר כמו שהוא
  $fm = @(); if ($dashes[1]-1 -ge $dashes[0]+1){ $fm = @($lines[($dashes[0]+1)..($dashes[1]-1)]) }
  $body = ""; if ($dashes[1]+1 -le $lines.Count-1){ $body = ($lines[($dashes[1]+1)..($lines.Count-1)] -join "`n") }
  $outFm = New-Object System.Collections.Generic.List[string]; $i = 0
  while ($i -lt $fm.Count) {
    $line = $fm[$i]
    if ($line -match '^(name|description):\s*(.*)$') {
      $key = $matches[1]; $val = ($matches[2] -replace '^[>|][-+0-9]*\s*','')   # הסר סימן block scalar
      $coll = @(); if ($val.Trim() -ne ''){ $coll += $val.Trim() }
      $j = $i + 1
      while ($j -lt $fm.Count) {                       # אסוף שורות-המשך מוזחות עד המפתח הראשי הבא
        $nl = $fm[$j]
        if ($nl -match '^[A-Za-z0-9_-]+:') { break }   # כולל מקף: עוצר גם ב-allowed-tools: ולא בולע אותו ל-description
        if ($nl.Trim() -ne ''){ $coll += $nl.Trim() }
        $j++
      }
      $joined = (($coll -join ' ') -replace '"','').Trim()
      if ($joined.StartsWith("'") -and $joined.EndsWith("'") -and $joined.Length -ge 2){ $joined = $joined.Substring(1,$joined.Length-2) }
      $joined = $joined -replace "'","''"              # escaping של גרש בודד (עברית: פיץ' -> פיץ'')
      $outFm.Add(("{0}: '{1}'" -f $key, $joined)); $i = $j; continue
    } else { $outFm.Add($line); $i++ }
  }
  return ("---`n" + ($outFm -join "`n") + "`n---`n" + $body)
}

# --- בניית zip יחיד ---
function Build-Zip([string]$skill) {
  $dir = Join-Path $SkillsDir $skill
  if (-not (Test-Path (Join-Path $dir 'SKILL.md'))) { return "MISSING: $skill (אין SKILL.md)" }
  $zipPath = Join-Path $OutDir ($skill + ".zip")
  $nestedPrefix = $skill + $sl
  $stream = [System.IO.File]::Open($zipPath, [System.IO.FileMode]::Create)   # Create דורס קיים
  $zip = New-Object System.IO.Compression.ZipArchive($stream, [System.IO.Compression.ZipArchiveMode]::Create)
  $prefixLen = $dir.Length + 1
  foreach ($f in (Get-ChildItem -Path $dir -Recurse -File)) {
    $rel = $f.FullName.Substring($prefixLen).Replace($bs,$sl)               # backslash -> forward slash
    if ($rel.StartsWith('scripts'+$sl) -or $rel.StartsWith('bin'+$sl) -or $rel.Contains($sl+'.git'+$sl)) { continue }
    if ($rel.StartsWith($nestedPrefix)) { continue }                        # תת-תיקייה כפולה בשם הסקיל
    $entry = $zip.CreateEntry($rel); $es = $entry.Open()
    if ($rel -eq 'SKILL.md') { $bytes = $enc.GetBytes((Get-FixedSkillMd $f.FullName)) }
    else { $bytes = [System.IO.File]::ReadAllBytes($f.FullName) }
    $es.Write($bytes,0,$bytes.Length); $es.Close()
  }
  $zip.Dispose(); $stream.Close()
  return "OK: $skill"
}

# --- ולידציה אחרי בנייה ---
function Test-Zip([string]$skill) {
  $zp = Join-Path $OutDir ($skill + ".zip")
  if (-not (Test-Path $zp)) { return "$skill : ZIP חסר" }
  $z = [System.IO.Compression.ZipFile]::OpenRead($zp)
  $skillEntries = @($z.Entries | Where-Object { $_.Name -eq 'SKILL.md' })
  $root = @($z.Entries | Where-Object { $_.FullName -eq 'SKILL.md' })
  $hasName=$false; $hasDesc=$false
  if ($root.Count -eq 1) {
    $sr = New-Object System.IO.StreamReader($root[0].Open()); $txt = $sr.ReadToEnd(); $sr.Close()
    foreach ($l in ($txt -split "`n")) {
      if ($l -match '^name:') { $hasName=$true }
      if ($l -match '^description:') { $hasDesc=$true }
      if ($l.Trim() -eq '---' -and $hasName) { break }
    }
  }
  $z.Dispose()
  if ($skillEntries.Count -ne 1) { return "$skill : FAIL - מספר SKILL.md = $($skillEntries.Count)" }
  if ($root.Count -ne 1)        { return "$skill : FAIL - SKILL.md לא בשורש" }
  if (-not $hasName -or -not $hasDesc) { return "$skill : FAIL - חסר name/description" }
  return "$skill : OK"
}

Write-Output "=== בונה ==="
foreach ($s in $Skills) { Write-Output ("  " + (Build-Zip $s)) }
Write-Output "=== ולידציה ==="
$fail = 0
foreach ($s in $Skills) { $r = Test-Zip $s; Write-Output ("  " + $r); if ($r -notmatch ': OK$') { $fail++ } }
Write-Output ("=== סיכום: " + $Skills.Count + " סקילים, " + $fail + " כשלים ===")
Write-Output ("פלט: " + $OutDir)
Write-Output "השלב הבא (ידני): claude.ai > Settings > Capabilities > Skills > Upload skill"

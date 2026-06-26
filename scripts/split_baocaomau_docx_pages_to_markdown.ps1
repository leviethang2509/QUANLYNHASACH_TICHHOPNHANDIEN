param(
    [string]$InputDocx = "QLNhaSach_BaoCao\00_inputs\BaoCaoMau.docx",
    [string]$OutputRoot = "QLNhaSach_BaoCao\01_template_markdown\pages_from_word_v1"
)

$ErrorActionPreference = "Stop"

function New-UniqueFolder {
    param([string]$PathValue)
    if (-not (Test-Path -LiteralPath $PathValue)) {
        return $PathValue
    }
    $parent = Split-Path -Parent $PathValue
    $leaf = Split-Path -Leaf $PathValue
    for ($i = 2; $i -lt 1000; $i++) {
        $candidate = Join-Path $parent ($leaf + "_v" + $i)
        if (-not (Test-Path -LiteralPath $candidate)) {
            return $candidate
        }
    }
    throw "Cannot create unique output folder"
}

function Normalize-PageText {
    param([string]$Value)
    if ($null -eq $Value) {
        return ""
    }
    $lf = [string][char]10
    $Value = $Value.Replace([string][char]13, $lf)
    $Value = $Value.Replace([string][char]7, $lf)
    $Value = $Value.Replace([string][char]11, $lf)
    $Value = $Value.Replace([string][char]12, $lf)
    while ($Value.Contains($lf + $lf + $lf)) {
        $Value = $Value.Replace($lf + $lf + $lf, $lf + $lf)
    }
    return $Value.Trim()
}

function Markdown-FromText {
    param([string]$Value)
    $lf = [string][char]10
    $lines = (Normalize-PageText $Value).Split([char]10)
    $result = New-Object System.Collections.Generic.List[string]
    foreach ($line in $lines) {
        $trim = $line.Trim()
        if ($trim.Length -eq 0) {
            $result.Add("")
        } elseif ($trim -match "^CH") {
            $result.Add("# " + $trim)
        } elseif ($trim.Length -le 90 -and $trim -ceq $trim.ToUpper() -and $trim -match "[A-Z]") {
            $result.Add("## " + $trim)
        } else {
            $result.Add($line.TrimEnd())
        }
    }
    return (($result -join $lf).Trim() + $lf)
}

$docxPath = (Resolve-Path -LiteralPath $InputDocx).Path
$outputDir = New-UniqueFolder $OutputRoot
$pagesDir = Join-Path $outputDir "pages"
$logsDir = "QLNhaSach_BaoCao\11_logs"
$historyDir = "QLNhaSach_BaoCao\13_history"
$validationDir = "QLNhaSach_BaoCao\10_validation"
New-Item -ItemType Directory -Force -Path $pagesDir | Out-Null
New-Item -ItemType Directory -Force -Path $logsDir | Out-Null
New-Item -ItemType Directory -Force -Path $historyDir | Out-Null
New-Item -ItemType Directory -Force -Path $validationDir | Out-Null

$word = $null
$doc = $null
$pageCount = 0
$created = 0
$lf = [string][char]10

try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $doc = $word.Documents.Open($docxPath, $false, $true)
    $doc.Repaginate()

    $wdStatisticPages = 2
    $wdGoToPage = 1
    $wdGoToAbsolute = 1
    $pageCount = [int]$doc.ComputeStatistics($wdStatisticPages)

    $index = New-Object System.Collections.Generic.List[string]
    $index.Add("# Page markdown index")
    $index.Add("")
    $index.Add("Source: ``QLNhaSach_BaoCao/00_inputs/BaoCaoMau.docx``")
    $index.Add("Generated at: " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss") + " Asia/Bangkok")
    $index.Add("Word COM page count: " + $pageCount)
    $index.Add("")
    $index.Add("| Page | File |")
    $index.Add("|---:|---|")

    for ($page = 1; $page -le $pageCount; $page++) {
        $startRange = $doc.GoTo($wdGoToPage, $wdGoToAbsolute, $page)
        $start = [int]$startRange.Start
        if ($page -lt $pageCount) {
            $nextRange = $doc.GoTo($wdGoToPage, $wdGoToAbsolute, $page + 1)
            $end = [int]$nextRange.Start
        } else {
            $end = [int]$doc.Content.End
        }
        if ($end -lt $start) {
            $end = $start
        }
        $range = $doc.Range($start, $end)
        $markdown = Markdown-FromText ([string]$range.Text)
        $fileName = ("page_{0:D3}.md" -f $page)
        $filePath = Join-Path $pagesDir $fileName
        $frontMatter = "---" + $lf
        $frontMatter += "source: QLNhaSach_BaoCao/00_inputs/BaoCaoMau.docx" + $lf
        $frontMatter += "page: " + $page + $lf
        $frontMatter += "total_pages: " + $pageCount + $lf
        $frontMatter += "extracted_by: Microsoft Word COM page range" + $lf
        $frontMatter += "---" + $lf + $lf
        $frontMatter += "# Trang " + $page + $lf + $lf
        [System.IO.File]::WriteAllText($filePath, $frontMatter + $markdown, [System.Text.UTF8Encoding]::new($false))
        $created++
        $index.Add("| " + $page + " | ``pages/" + $fileName + "`` |")
    }

    [System.IO.File]::WriteAllText((Join-Path $outputDir "index.md"), ($index -join $lf) + $lf, [System.Text.UTF8Encoding]::new($false))
}
finally {
    if ($doc -ne $null) {
        try { $doc.Close($false) | Out-Null } catch { }
    }
    if ($word -ne $null) {
        try { $word.Quit() | Out-Null } catch { }
    }
}

$historyPath = Join-Path $historyDir "009_tach_baocaomau_theo_trang_markdown.md"
$historyText = "# 009 - Split BaoCaoMau.docx into page Markdown" + $lf + $lf
$historyText += "Generated at: " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss") + " Asia/Bangkok" + $lf + $lf
$historyText += "- Source: ``QLNhaSach_BaoCao/00_inputs/BaoCaoMau.docx``" + $lf
$historyText += "- Output: ``" + $outputDir + "``" + $lf
$historyText += "- Word COM page count: " + $pageCount + $lf
$historyText += "- Markdown files created: " + $created + $lf
[System.IO.File]::WriteAllText($historyPath, $historyText, [System.Text.UTF8Encoding]::new($false))

$validationPath = Join-Path $validationDir "split_pages_markdown_validation_v1.md"
if ($pageCount -eq 120) {
    $pageCheck = "OK"
} else {
    $pageCheck = "CHECK - Word COM counted " + $pageCount + " pages, not 120"
}
if ($created -eq $pageCount) {
    $countCheck = "OK"
} else {
    $countCheck = "CHECK"
}
$validationText = "# Validation - split page Markdown" + $lf + $lf
$validationText += "Generated at: " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss") + " Asia/Bangkok" + $lf + $lf
$validationText += "| Item | Result |" + $lf
$validationText += "|---|---|" + $lf
$validationText += "| Open DOCX with Word COM | OK |" + $lf
$validationText += "| Markdown files equal Word pages | " + $countCheck + " |" + $lf
$validationText += "| Requested 120 pages | " + $pageCheck + " |" + $lf
$validationText += "| Output folder | ``" + $outputDir + "`` |" + $lf
[System.IO.File]::WriteAllText($validationPath, $validationText, [System.Text.UTF8Encoding]::new($false))

Add-Content -LiteralPath (Join-Path $logsDir "execution_log.md") -Encoding UTF8 -Value ($lf + "## " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss") + $lf + $lf + "- Split BaoCaoMau.docx into " + $created + " page Markdown files at ``" + $outputDir + "``." + $lf)

Write-Output ("output=" + $outputDir)
Write-Output ("pages=" + $pageCount)
Write-Output ("created=" + $created)

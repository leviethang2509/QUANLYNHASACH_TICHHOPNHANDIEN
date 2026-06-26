$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Web = Join-Path $Root "BaiTapLon"
$Port = 5080
$Url = "http://localhost:$Port/Home/TrangChu"
$Log = Join-Path $Root "iisexpress-local.log"
$ErrorLog = Join-Path $Root "iisexpress-local-error.log"
$ConfigRuntime = Join-Path $Root ".iisexpress\applicationhost.local.config"
$ConfigTemplate = Join-Path $Root ".iisexpress\applicationhost.config"
$IisExpress = Join-Path ${env:ProgramFiles(x86)} "IIS Express\iisexpress.exe"

if (-not (Test-Path $IisExpress)) {
    $IisExpress = Join-Path ${env:ProgramFiles} "IIS Express\iisexpress.exe"
}

if (-not (Test-Path $IisExpress)) {
    Write-Host "Khong tim thay IIS Express tren may." -ForegroundColor Red
    Write-Host "Hay cai IIS Express hoac chay project bang Visual Studio."
    exit 1
}

$AspNetFiles = @(
    (Join-Path $env:WINDIR "Microsoft.NET\Framework\v4.0.30319\aspnet_isapi.dll"),
    (Join-Path $env:WINDIR "Microsoft.NET\Framework64\v4.0.30319\aspnet_isapi.dll")
)
$AspNetRegistered = $AspNetFiles | Where-Object { Test-Path $_ }
if (-not $AspNetRegistered) {
    Write-Host "May nay chua bat/dang ky ASP.NET 4.x cho IIS Express." -ForegroundColor Red
    Write-Host "Day la nguyen nhan thuong gap cua loi 8007045a / Error loading global modules."
    Write-Host ""
    Write-Host "Cach sua:"
    Write-Host "  1. Bam chuot phai sua_iisexpress.bat -> Run as administrator"
    Write-Host "  2. Neu Windows vua bat feature moi, restart may"
    Write-Host "  3. Chay lai chay_local.bat"
    exit 1
}

if (-not (Test-Path (Join-Path $Web "Web.config"))) {
    Write-Host "Khong tim thay Web.config trong: $Web" -ForegroundColor Red
    Write-Host "Kiem tra lai thu muc project web."
    exit 1
}

if (-not (Test-Path $ConfigTemplate)) {
    Write-Host "Khong tim thay file cau hinh IIS Express local: $ConfigTemplate" -ForegroundColor Red
    exit 1
}

Remove-Item $Log -ErrorAction SilentlyContinue
Remove-Item $ErrorLog -ErrorAction SilentlyContinue

$connections = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
$processIds = $connections | Select-Object -ExpandProperty OwningProcess -Unique

foreach ($processId in $processIds) {
    $process = Get-Process -Id $processId -ErrorAction SilentlyContinue
    if ($process) {
        Write-Host "Dang tat process cu tren port ${Port}: $($process.ProcessName) ($processId)"
        Stop-Process -Id $processId -Force
        Start-Sleep -Milliseconds 500
    }
}

Write-Host "Dang khoi dong web local..." -ForegroundColor Cyan
Write-Host "Thu muc web: $Web"
Write-Host "URL: $Url"
Write-Host "Log: $Log"
Write-Host "Error log: $ErrorLog"

$webConfigPath = $Web.Replace("&", "&amp;").Replace("<", "&lt;").Replace(">", "&gt;").Replace('"', "&quot;")
(Get-Content $ConfigTemplate -Raw).Replace("__WEB_PATH__", $webConfigPath) | Set-Content $ConfigRuntime -Encoding UTF8

$arguments = "/config:`"$ConfigRuntime`" /site:QLNhaSachLocal /systray:false /trace:error"
$server = Start-Process -FilePath $IisExpress -ArgumentList $arguments -RedirectStandardOutput $Log -RedirectStandardError $ErrorLog -PassThru -WindowStyle Hidden

$started = $false
for ($i = 0; $i -lt 30; $i++) {
    Start-Sleep -Milliseconds 500

    if ($server.HasExited) {
        break
    }

    $isListening = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    if ($isListening) {
        $started = $true
        break
    }
}

if (-not $started) {
    Write-Host ""
    Write-Host "Web chua chay duoc tren port $Port." -ForegroundColor Red
    Write-Host "Noi dung log IIS Express:"
    Write-Host "----------------------------------------"
    $logText = ""
    if (Test-Path $Log) {
        $logText += Get-Content $Log -Raw
        Write-Host $logText
    } else {
        Write-Host "Khong co log. IIS Express co the bi tat ngay khi khoi dong."
    }
    if (Test-Path $ErrorLog) {
        $errorText = Get-Content $ErrorLog -Raw
        $logText += $errorText
        Write-Host $errorText
    }
    Write-Host "----------------------------------------"

    if ($logText -match "Error loading global modules|DLL initialization routine failed|8007045a") {
        Write-Host ""
        Write-Host "Day la loi runtime IIS Express/ASP.NET tren may, khong phai loi Controller/View cua project." -ForegroundColor Yellow
        Write-Host "Hay dong cua so nay, bam chuot phai sua_iisexpress.bat -> Run as administrator, roi chay lai chay_local.bat."
        Write-Host "Neu van gap 8007045a sau khi chay sua_iisexpress.bat, hay restart Windows roi chay lai."
    }

    exit 1
}

Write-Host "Web da chay thanh cong." -ForegroundColor Green
Start-Process $Url
Write-Host "Nhan Ctrl+C trong cua so nay de dung server."

try {
    Wait-Process -Id $server.Id
} finally {
    if (-not $server.HasExited) {
        Stop-Process -Id $server.Id -Force
    }
}

@echo off
setlocal

net session >nul 2>&1
if not "%errorlevel%"=="0" (
  echo File nay can chay bang quyen Administrator.
  echo Hay bam chuot phai sua_iisexpress.bat - Run as administrator.
  echo.
  pause
  exit /b 1
)

echo Dang sua runtime ASP.NET MVC .NET Framework va IIS Express...
echo.

echo [1/6] Bat .NET Framework 4.x ASP.NET...
dism.exe /Online /Enable-Feature /FeatureName:NetFx4Extended-ASPNET45 /All /NoRestart

echo.
echo [2/6] Bat IIS .NET Extensibility 4.x...
dism.exe /Online /Enable-Feature /FeatureName:IIS-NetFxExtensibility45 /All /NoRestart

echo.
echo [3/6] Bat IIS ASP.NET 4.x...
dism.exe /Online /Enable-Feature /FeatureName:IIS-ASPNET45 /All /NoRestart

echo.
echo [4/6] Dang ky ASP.NET 4.x voi IIS/IIS Express...
if exist "%WINDIR%\Microsoft.NET\Framework64\v4.0.30319\aspnet_regiis.exe" (
  "%WINDIR%\Microsoft.NET\Framework64\v4.0.30319\aspnet_regiis.exe" -i
)
if exist "%WINDIR%\Microsoft.NET\Framework\v4.0.30319\aspnet_regiis.exe" (
  "%WINDIR%\Microsoft.NET\Framework\v4.0.30319\aspnet_regiis.exe" -i
)
if not exist "%WINDIR%\Microsoft.NET\Framework64\v4.0.30319\aspnet_regiis.exe" if not exist "%WINDIR%\Microsoft.NET\Framework\v4.0.30319\aspnet_regiis.exe" (
  echo Windows nay khong co aspnet_regiis.exe rieng cho .NET 4.x. Da bat NetFx4Extended-ASPNET45 o buoc [1].
)

echo.
echo [5/6] Kiem tra IIS Express...
if exist "%ProgramFiles%\IIS Express\iisexpress.exe" (
  "%ProgramFiles%\IIS Express\iisexpress.exe" /? >nul 2>&1
) else if exist "%ProgramFiles(x86)%\IIS Express\iisexpress.exe" (
  "%ProgramFiles(x86)%\IIS Express\iisexpress.exe" /? >nul 2>&1
) else (
  echo Chua thay IIS Express trong Program Files.
)

echo.
echo [6/6] Cai/repair IIS Express neu winget tim thay goi...
winget install --id Microsoft.IISExpress --accept-package-agreements --accept-source-agreements
if not "%errorlevel%"=="0" (
  echo Winget khong cai duoc IIS Express tu dong. Neu may bao da co IIS Express thi co the bo qua.
)

echo.
echo Kiem tra file ASP.NET 4.x sau khi sua...
if exist "%WINDIR%\Microsoft.NET\Framework\v4.0.30319\aspnet_isapi.dll" (
  echo OK: Tim thay ASP.NET 4.x 32-bit.
) else (
  echo CANH BAO: Chua thay ASP.NET 4.x 32-bit.
)
if exist "%WINDIR%\Microsoft.NET\Framework64\v4.0.30319\aspnet_isapi.dll" (
  echo OK: Tim thay ASP.NET 4.x 64-bit.
) else (
  echo CANH BAO: Chua thay ASP.NET 4.x 64-bit.
)
echo.
echo Hoan tat. Hay restart Windows neu DISM vua bat them feature hoac chay_local.bat van bao 8007045a.
echo Sau khi restart, neu van loi, mo Windows Features va tick:
echo   .NET Framework 4.x Advanced Services - ASP.NET 4.x
echo   Internet Information Services - World Wide Web Services - Application Development Features - ASP.NET 4.x
echo Sau do chay lai chay_local.bat
echo.
pause
endlocal

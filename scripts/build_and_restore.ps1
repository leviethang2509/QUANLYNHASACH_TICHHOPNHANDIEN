<#
scripts/build_and_restore.ps1
Purpose: Restore NuGet packages for the solution and build with MSBuild, collecting errors.

Usage:
  powershell -ExecutionPolicy Bypass -File .\scripts\build_and_restore.ps1 -SolutionPath "DongTrieuBookStore.sln"

Requirements:
 - NuGet.exe on PATH or dotnet CLI for SDK-style projects
 - MSBuild (Visual Studio Developer Tools) on PATH
#>

param(
  [string]$SolutionPath = "DongTrieuBookStore.sln",
  [string]$Configuration = "Debug",
  [string]$Platform = "Any CPU"
)

function Write-Log([string]$m) { Write-Host "[BUILD] $m" }

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

if (-not (Test-Path $SolutionPath)) {
  Write-Error "Solution file '$SolutionPath' not found in $PWD"
  exit 1
}

Write-Log "Restoring NuGet packages..."
if (Get-Command nuget -ErrorAction SilentlyContinue) {
  nuget restore $SolutionPath
} elseif (Get-Command dotnet -ErrorAction SilentlyContinue) {
  dotnet restore $SolutionPath
} else {
  Write-Error "Neither 'nuget' nor 'dotnet' found on PATH. Install NuGet CLI or .NET SDK."; exit 2
}

Write-Log "Building solution with MSBuild..."
if (Get-Command msbuild -ErrorAction SilentlyContinue) {
  msbuild $SolutionPath /p:Configuration=$Configuration /p:Platform="$Platform" /m
} else {
  Write-Error "msbuild not found on PATH. Open 'Developer Command Prompt for VS' or install Build Tools."; exit 3
}

Write-Log "Build script finished. Check output above for errors." 

<#
scripts/apply_sql_migrations.ps1
Usage examples:
  .\apply_sql_migrations.ps1 -ServerInstance "(localdb)\MSSQLLocalDB" -Database "QLNhaSach"
  .\apply_sql_migrations.ps1 -ServerInstance "myserver.example.com" -Database "QLNhaSach" -SqlUser "sa" -SqlPass "P@ssw0rd"

This script runs `create_database.sql` (if present) then runs all .sql files in sql/migrations in name-sorted order.
Require: Invoke-Sqlcmd (SqlServer module) or SQLCMD available.
#>

param(
    [string]$ServerInstance = "(localdb)\MSSQLLocalDB",
    [string]$Database = "QLNhaSach",
    [string]$SqlUser = "",
    [string]$SqlPass = "",
    [string]$MigrationsPath = "sql\migrations"
)

function Write-Log { param($m) Write-Host "[MIGRATE] $m" }

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $scriptRoot
$migrationsFull = Resolve-Path (Join-Path $root $MigrationsPath) -ErrorAction SilentlyContinue
if (-not $migrationsFull) { Write-Error "Migrations path '$MigrationsPath' not found."; exit 1 }

Write-Log "Server: $ServerInstance"
Write-Log "Database: $Database"
Write-Log "Migrations folder: $($migrationsFull.Path)"

function Run-SqlFile($file, $targetDb)
{
    Write-Log "Applying $file to $targetDb"
    if (Get-Command Invoke-Sqlcmd -ErrorAction SilentlyContinue) {
        if ($SqlUser -ne "" -and $SqlPass -ne "") {
            Invoke-Sqlcmd -ServerInstance $ServerInstance -Database $targetDb -Username $SqlUser -Password $SqlPass -InputFile $file -ErrorAction Stop
        } else {
            Invoke-Sqlcmd -ServerInstance $ServerInstance -Database $targetDb -InputFile $file -ErrorAction Stop
        }
    } else {
        # fallback to sqlcmd
        $creds = ""
        if ($SqlUser -ne "" -and $SqlPass -ne "") { $creds = " -U $SqlUser -P $SqlPass" }
        $cmd = "sqlcmd -S `"$ServerInstance`" -d `"$targetDb`" -i `"$file`" $creds"
        Write-Log "Running: $cmd"
        $rc = cmd.exe /c $cmd
        if ($LASTEXITCODE -ne 0) { throw "sqlcmd failed for $file" }
    }
}

# 1) create database using top-level script if exists
$createScript = Join-Path (Split-Path $migrationsFull.Path -Parent) 'create_database.sql'
if (Test-Path $createScript) {
    Write-Log "Found create script: $createScript"
    try { Run-SqlFile $createScript 'master' } catch { Write-Error $_; exit 2 }
    Start-Sleep -Seconds 2
}

# 2) apply migrations in folder
Get-ChildItem -Path $migrationsFull.Path -Filter "*.sql" | Sort-Object Name | ForEach-Object {
    try {
        Run-SqlFile $_.FullName $Database
    } catch {
        Write-Error "Failed to apply $($_.FullName): $_"
        exit 3
    }
}

Write-Log "All migrations applied successfully."

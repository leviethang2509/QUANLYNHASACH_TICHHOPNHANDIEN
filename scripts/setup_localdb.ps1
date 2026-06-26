<#
Sets up the local SQL Server LocalDB database used by the web app.

Usage:
  powershell -ExecutionPolicy Bypass -File .\scripts\setup_localdb.ps1
  powershell -ExecutionPolicy Bypass -File .\scripts\setup_localdb.ps1 -Database QLNhaSach
#>

param(
    [string]$ServerInstance = "(localdb)\MSSQLLocalDB",
    [string]$Database = "QLNhaSach"
)

$ErrorActionPreference = "Stop"

function Write-Log {
    param([string]$Message)
    Write-Host "[LOCALDB] $Message"
}

function Split-SqlBatches {
    param([string]$Sql)

    $batches = New-Object System.Collections.Generic.List[string]
    $current = New-Object System.Text.StringBuilder

    foreach ($line in ($Sql -split "`r?`n")) {
        if ($line -match '^\s*GO\s*(?:--.*)?$') {
            $batch = $current.ToString().Trim()
            if ($batch.Length -gt 0) {
                [void]$batches.Add($batch)
            }
            [void]$current.Clear()
        } else {
            [void]$current.AppendLine($line)
        }
    }

    $lastBatch = $current.ToString().Trim()
    if ($lastBatch.Length -gt 0) {
        [void]$batches.Add($lastBatch)
    }

    return $batches
}

function Invoke-SqlBatch {
    param(
        [string]$ConnectionString,
        [string]$Sql
    )

    $connection = New-Object System.Data.SqlClient.SqlConnection($ConnectionString)
    try {
        $connection.Open()
        $command = $connection.CreateCommand()
        $command.CommandTimeout = 120
        $command.CommandText = $Sql
        [void]$command.ExecuteNonQuery()
    } finally {
        $connection.Dispose()
    }
}

function Invoke-SqlScript {
    param(
        [string]$ConnectionString,
        [string]$Path,
        [hashtable]$Replace = @{}
    )

    Write-Log "Running $Path"
    $sql = Get-Content -LiteralPath $Path -Raw -Encoding UTF8
    foreach ($key in $Replace.Keys) {
        $sql = $sql -replace $key, $Replace[$key]
    }

    foreach ($batch in (Split-SqlBatches $sql)) {
        Invoke-SqlBatch -ConnectionString $ConnectionString -Sql $batch
    }
}

function Invoke-SqlScalar {
    param(
        [string]$ConnectionString,
        [string]$Sql
    )

    $connection = New-Object System.Data.SqlClient.SqlConnection($ConnectionString)
    try {
        $connection.Open()
        $command = $connection.CreateCommand()
        $command.CommandTimeout = 120
        $command.CommandText = $Sql
        return $command.ExecuteScalar()
    } finally {
        $connection.Dispose()
    }
}

Add-Type -AssemblyName System.Data

$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$masterConnection = "Data Source=$ServerInstance;Initial Catalog=master;Integrated Security=True;MultipleActiveResultSets=True;Connect Timeout=15"
$databaseConnection = "Data Source=$ServerInstance;Initial Catalog=$Database;Integrated Security=True;MultipleActiveResultSets=True;Connect Timeout=15"

Write-Log "Server: $ServerInstance"
Write-Log "Database: $Database"

$existingDatabaseId = Invoke-SqlScalar -ConnectionString $masterConnection -Sql "SELECT DB_ID(N'$Database')"
if ($null -eq $existingDatabaseId -or $existingDatabaseId -is [System.DBNull]) {
    $defaultDataPath = Join-Path $env:USERPROFILE "$Database.mdf"
    $defaultLogPath = Join-Path $env:USERPROFILE "${Database}_log.ldf"
    $projectDataFolder = Join-Path $root "BaiTapLon\App_Data"
    $projectDataPath = Join-Path $projectDataFolder "$Database.localdb.mdf"
    $projectLogPath = Join-Path $projectDataFolder "$Database.localdb_log.ldf"

    if ((Test-Path -LiteralPath $defaultDataPath) -and (Test-Path -LiteralPath $defaultLogPath)) {
        Write-Log "Attaching existing files from $env:USERPROFILE"
        $attachSql = @"
CREATE DATABASE [$Database]
ON (FILENAME = N'$defaultDataPath'),
   (FILENAME = N'$defaultLogPath')
FOR ATTACH;
"@
        try {
            Invoke-SqlBatch -ConnectionString $masterConnection -Sql $attachSql
        } catch {
            Write-Log "Existing files could not be attached; creating a fresh project-local database"
            if (-not (Test-Path -LiteralPath $projectDataFolder)) {
                New-Item -ItemType Directory -Path $projectDataFolder | Out-Null
            }
            $createWithFilesSql = @"
CREATE DATABASE [$Database]
ON PRIMARY (NAME = N'$Database', FILENAME = N'$projectDataPath')
LOG ON (NAME = N'${Database}_log', FILENAME = N'$projectLogPath');
"@
            Invoke-SqlBatch -ConnectionString $masterConnection -Sql $createWithFilesSql
        }
    } else {
        if (-not (Test-Path -LiteralPath $projectDataFolder)) {
            New-Item -ItemType Directory -Path $projectDataFolder | Out-Null
        }
        $createWithFilesSql = @"
CREATE DATABASE [$Database]
ON PRIMARY (NAME = N'$Database', FILENAME = N'$projectDataPath')
LOG ON (NAME = N'${Database}_log', FILENAME = N'$projectLogPath');
"@
        Invoke-SqlBatch -ConnectionString $masterConnection -Sql $createWithFilesSql
    }
}

$dbScript = Join-Path $root "db.sql"
$hasBaseTables = Invoke-SqlScalar -ConnectionString $databaseConnection -Sql "SELECT OBJECT_ID(N'dbo.Category', N'U')"
if ((Test-Path -LiteralPath $dbScript) -and ($null -eq $hasBaseTables -or $hasBaseTables -is [System.DBNull])) {
    Invoke-SqlScript `
        -ConnectionString $databaseConnection `
        -Path $dbScript `
        -Replace @{ 'USE\s+\[QLTV_BTL\]' = "USE [$Database]" }
} elseif (Test-Path -LiteralPath $dbScript) {
    Write-Log "Base tables already exist; skipping db.sql"
}

$migrationFolder = Join-Path $root "sql\migrations"
if (Test-Path -LiteralPath $migrationFolder) {
    Get-ChildItem -LiteralPath $migrationFolder -Filter "*.sql" |
        Sort-Object Name |
        ForEach-Object {
            Invoke-SqlScript -ConnectionString $databaseConnection -Path $_.FullName
        }
}

$verifySql = @"
SELECT name
FROM sys.tables
WHERE name IN (
    N'Category',
    N'Sanpham',
    N'User',
    N'StoreLocations',
    N'FaceAuthLogs',
    N'GeofenceLogs',
    N'RentalLogs',
    N'RentalRequests',
    N'ProductFavorites',
    N'ProductReviews'
)
ORDER BY name;
"@

Write-Log "Verifying tables"
$connection = New-Object System.Data.SqlClient.SqlConnection($databaseConnection)
try {
    $connection.Open()
    $command = $connection.CreateCommand()
    $command.CommandText = $verifySql
    $reader = $command.ExecuteReader()
    while ($reader.Read()) {
        Write-Host ("  - " + $reader.GetString(0))
    }
} finally {
    $connection.Dispose()
}

Write-Log "Done."

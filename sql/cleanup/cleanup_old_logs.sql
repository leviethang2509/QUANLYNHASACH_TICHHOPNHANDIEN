-- Cleanup script: delete audit logs older than 90 days.
DELETE FROM dbo.FaceAuthLogs WHERE Timestamp < DATEADD(day, -90, SYSUTCDATETIME());
DELETE FROM dbo.GeofenceLogs WHERE Timestamp < DATEADD(day, -90, SYSUTCDATETIME());
DELETE FROM dbo.RentalLogs WHERE Timestamp < DATEADD(day, -90, SYSUTCDATETIME());

-- Optionally remove image files older than 90 days on the app server.
-- PowerShell example:
-- Get-ChildItem -Path "D:\BACKUP_2004_2026_D\QLNhaSach\BaiTapLon\DataImage\FaceSamples" -Recurse |
--   Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-90) } |
--   Remove-Item

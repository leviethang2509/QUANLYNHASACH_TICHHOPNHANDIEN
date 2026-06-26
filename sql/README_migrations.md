# Migration instructions

Run these scripts on staging first, then production during a maintenance window after taking a database backup.

## Apply migrations

Recommended:

```powershell
.\scripts\apply_sql_migrations.ps1 -ServerInstance "(localdb)\MSSQLLocalDB" -Database "QLNhaSach"
```

Manual example:

```powershell
sqlcmd -S <server> -d <database> -i .\sql\migrations\20260508_add_stores.sql
sqlcmd -S <server> -d <database> -i .\sql\migrations\20260508_add_logs.sql
sqlcmd -S <server> -d <database> -i .\sql\migrations\20260509_add_identity_card_rental_flow.sql
sqlcmd -S <server> -d <database> -i .\sql\migrations\20260509_add_notification_email_version5.sql
sqlcmd -S <server> -d <database> -i .\sql\migrations\20260510_add_product_reviews_version5.sql
```

## Verify

Confirm these tables exist:

- `dbo.StoreLocations`
- `dbo.FaceAuthLogs`
- `dbo.GeofenceLogs`
- `dbo.RentalLogs`
- `dbo.ProductReviews`

Confirm these indexes exist:

- `IX_FaceAuthLogs_Timestamp_UserID_Action`
- `IX_GeofenceLogs_Timestamp_UserID_StoreID`
- `IX_RentalLogs_Timestamp_RentalID_UserID_Action`

Confirm these columns exist:

- `dbo.[User].IdentityNumber`
- `dbo.[User].IdentityCardImagePath`
- `dbo.[User].NotificationEmail`
- `dbo.RentalRequests.IdentityNumber`
- `dbo.RentalRequests.IdentityCardImagePath`
- `dbo.Sanpham.ReviewFilePath`
- `dbo.Sanpham.ReviewFileName`
- `dbo.Sanpham.YoutubeUrl`

## Cleanup

Use `sql\cleanup\cleanup_old_logs.sql` to remove old audit logs after the retention policy is approved.

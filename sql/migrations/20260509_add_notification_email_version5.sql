IF COL_LENGTH('dbo.[User]', 'NotificationEmail') IS NULL
BEGIN
    ALTER TABLE dbo.[User] ADD NotificationEmail NVARCHAR(250) NULL;
END
GO

UPDATE dbo.[User]
SET NotificationEmail = Email
WHERE NotificationEmail IS NULL
  AND Email IS NOT NULL;
GO

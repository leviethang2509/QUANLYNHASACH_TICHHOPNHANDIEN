IF COL_LENGTH('dbo.[User]', 'IdentityNumber') IS NULL
BEGIN
    ALTER TABLE dbo.[User] ADD
        IdentityNumber NVARCHAR(30) NULL,
        IdentityFullName NVARCHAR(250) NULL,
        IdentityDateOfBirth DATE NULL,
        IdentityAddress NVARCHAR(500) NULL,
        IdentityIssueDate DATE NULL,
        IdentityIssuePlace NVARCHAR(250) NULL,
        IdentityCardImagePath NVARCHAR(500) NULL,
        IdentityVerifiedAt DATETIME NULL,
        IdentityFaceConfidence FLOAT NULL;
END
GO

IF COL_LENGTH('dbo.[User]', 'IdentityPlaceOfBirth') IS NULL
BEGIN
    ALTER TABLE dbo.[User] ADD
        IdentityPlaceOfBirth NVARCHAR(250) NULL,
        IdentityGender NVARCHAR(30) NULL,
        IdentityNationality NVARCHAR(100) NULL,
        IdentityExpiryDate DATE NULL,
        IdentityIssuingAuthority NVARCHAR(250) NULL,
        IdentityCardFrontImagePath NVARCHAR(500) NULL,
        IdentityCardBackImagePath NVARCHAR(500) NULL;
END
GO

IF COL_LENGTH('dbo.RentalRequests', 'IdentityNumber') IS NULL
BEGIN
    ALTER TABLE dbo.RentalRequests ADD
        IdentityNumber NVARCHAR(30) NULL,
        IdentityFullName NVARCHAR(250) NULL,
        IdentityCardImagePath NVARCHAR(500) NULL,
        IdentityFaceConfidence FLOAT NULL,
        IdentityOcrRawJson NVARCHAR(4000) NULL;
END
GO

IF COL_LENGTH('dbo.RentalRequests', 'IdentityCardFrontImagePath') IS NULL
BEGIN
    ALTER TABLE dbo.RentalRequests ADD
        IdentityCardFrontImagePath NVARCHAR(500) NULL,
        IdentityCardBackImagePath NVARCHAR(500) NULL,
        IdentityAddress NVARCHAR(500) NULL,
        IdentityPlaceOfBirth NVARCHAR(250) NULL,
        IdentityDateOfBirth DATE NULL,
        IdentityIssueDate DATE NULL,
        IdentityExpiryDate DATE NULL,
        IdentityGender NVARCHAR(30) NULL,
        IdentityNationality NVARCHAR(100) NULL,
        IdentityIssuePlace NVARCHAR(250) NULL,
        IdentityIssuingAuthority NVARCHAR(250) NULL;
END
GO

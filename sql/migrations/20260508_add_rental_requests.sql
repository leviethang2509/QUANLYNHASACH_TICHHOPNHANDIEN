-- Migration: add rental workflow table
IF OBJECT_ID(N'dbo.RentalRequests', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.RentalRequests (
        ID INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_RentalRequests PRIMARY KEY,
        ProductID BIGINT NOT NULL,
        UserID BIGINT NOT NULL,
        Quantity INT NOT NULL CONSTRAINT DF_RentalRequests_Quantity DEFAULT 1,
        Status NVARCHAR(50) NOT NULL,
        RequestedAt DATETIME2 NOT NULL,
        RequestDate DATETIME2 NOT NULL CONSTRAINT DF_RentalRequests_RequestDate DEFAULT SYSUTCDATETIME(),
        BorrowDays INT NOT NULL CONSTRAINT DF_RentalRequests_BorrowDays DEFAULT 1,
        ExpectedReturnDate DATETIME2 NOT NULL CONSTRAINT DF_RentalRequests_ExpectedReturnDate DEFAULT DATEADD(DAY, 1, SYSUTCDATETIME()),
        ApprovedAt DATETIME2 NULL,
        ReturnedAt DATETIME2 NULL,
        ActualReturnDate DATETIME2 NULL,
        AdminID BIGINT NULL,
        RejectReason NVARCHAR(500) NULL,
        Details NVARCHAR(1000) NULL
    );
END;

IF COL_LENGTH('dbo.RentalRequests', 'RequestDate') IS NULL
    ALTER TABLE dbo.RentalRequests ADD RequestDate DATETIME2 NOT NULL CONSTRAINT DF_RentalRequests_RequestDate DEFAULT SYSUTCDATETIME();

IF COL_LENGTH('dbo.RentalRequests', 'BorrowDays') IS NULL
    ALTER TABLE dbo.RentalRequests ADD BorrowDays INT NOT NULL CONSTRAINT DF_RentalRequests_BorrowDays DEFAULT 1;

IF COL_LENGTH('dbo.RentalRequests', 'ExpectedReturnDate') IS NULL
    ALTER TABLE dbo.RentalRequests ADD ExpectedReturnDate DATETIME2 NOT NULL CONSTRAINT DF_RentalRequests_ExpectedReturnDate DEFAULT DATEADD(DAY, 1, SYSUTCDATETIME());

IF COL_LENGTH('dbo.RentalRequests', 'ActualReturnDate') IS NULL
    ALTER TABLE dbo.RentalRequests ADD ActualReturnDate DATETIME2 NULL;

IF COL_LENGTH('dbo.RentalRequests', 'RejectReason') IS NULL
    ALTER TABLE dbo.RentalRequests ADD RejectReason NVARCHAR(500) NULL;

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = N'IX_RentalRequests_Status_RequestedAt' AND object_id = OBJECT_ID(N'dbo.RentalRequests'))
    CREATE INDEX IX_RentalRequests_Status_RequestedAt ON dbo.RentalRequests (Status, RequestedAt DESC);

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = N'IX_RentalRequests_UserID_ProductID' AND object_id = OBJECT_ID(N'dbo.RentalRequests'))
    CREATE INDEX IX_RentalRequests_UserID_ProductID ON dbo.RentalRequests (UserID, ProductID);

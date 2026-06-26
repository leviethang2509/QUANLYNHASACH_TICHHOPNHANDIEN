-- Migration: add audit log tables
IF OBJECT_ID(N'dbo.FaceAuthLogs', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.FaceAuthLogs (
        ID INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_FaceAuthLogs PRIMARY KEY,
        UserID BIGINT NOT NULL,
        Action NVARCHAR(50) NOT NULL,
        Timestamp DATETIME2 NOT NULL,
        IP NVARCHAR(45) NULL,
        DeviceInfo NVARCHAR(500) NULL,
        ImagePath NVARCHAR(500) NULL,
        Result BIT NOT NULL CONSTRAINT DF_FaceAuthLogs_Result DEFAULT 0,
        Confidence FLOAT NOT NULL CONSTRAINT DF_FaceAuthLogs_Confidence DEFAULT 0,
        ErrorMessage NVARCHAR(1000) NULL,
        RequestId NVARCHAR(64) NULL,
        Purpose NVARCHAR(50) NULL,
        ErrorCode NVARCHAR(100) NULL,
        LivenessPassed BIT NULL
    );
END;

IF COL_LENGTH('dbo.FaceAuthLogs', 'Purpose') IS NULL
    ALTER TABLE dbo.FaceAuthLogs ADD Purpose NVARCHAR(50) NULL;

IF COL_LENGTH('dbo.FaceAuthLogs', 'ErrorCode') IS NULL
    ALTER TABLE dbo.FaceAuthLogs ADD ErrorCode NVARCHAR(100) NULL;

IF COL_LENGTH('dbo.FaceAuthLogs', 'LivenessPassed') IS NULL
    ALTER TABLE dbo.FaceAuthLogs ADD LivenessPassed BIT NULL;

IF OBJECT_ID(N'dbo.GeofenceLogs', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.GeofenceLogs (
        ID INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_GeofenceLogs PRIMARY KEY,
        UserID BIGINT NOT NULL,
        StoreID INT NOT NULL,
        IsInZone BIT NOT NULL,
        Timestamp DATETIME2 NOT NULL,
        UserLat DECIMAL(9,6) NOT NULL,
        UserLon DECIMAL(9,6) NOT NULL,
        Distance FLOAT NOT NULL,
        AllowedRadiusKm FLOAT NOT NULL CONSTRAINT DF_GeofenceLogs_AllowedRadiusKm DEFAULT 0,
        StoreName NVARCHAR(200) NULL
    );
END;

IF OBJECT_ID(N'dbo.RentalLogs', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.RentalLogs (
        ID INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_RentalLogs PRIMARY KEY,
        RentalID INT NOT NULL,
        UserID BIGINT NOT NULL,
        ActorUserID BIGINT NULL,
        Action NVARCHAR(50) NOT NULL,
        Timestamp DATETIME2 NOT NULL,
        Details NVARCHAR(MAX) NULL,
        OldStatus NVARCHAR(50) NULL,
        NewStatus NVARCHAR(50) NULL
    );
END;

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = N'IX_FaceAuthLogs_Timestamp_UserID_Action' AND object_id = OBJECT_ID(N'dbo.FaceAuthLogs'))
    CREATE INDEX IX_FaceAuthLogs_Timestamp_UserID_Action ON dbo.FaceAuthLogs (Timestamp DESC, UserID, Action);

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = N'IX_GeofenceLogs_Timestamp_UserID_StoreID' AND object_id = OBJECT_ID(N'dbo.GeofenceLogs'))
    CREATE INDEX IX_GeofenceLogs_Timestamp_UserID_StoreID ON dbo.GeofenceLogs (Timestamp DESC, UserID, StoreID);

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = N'IX_RentalLogs_Timestamp_RentalID_UserID_Action' AND object_id = OBJECT_ID(N'dbo.RentalLogs'))
    CREATE INDEX IX_RentalLogs_Timestamp_RentalID_UserID_Action ON dbo.RentalLogs (Timestamp DESC, RentalID, UserID, Action);

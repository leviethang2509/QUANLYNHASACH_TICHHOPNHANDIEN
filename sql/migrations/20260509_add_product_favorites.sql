-- Migration: add ProductFavorites table
IF OBJECT_ID(N'dbo.ProductFavorites', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.ProductFavorites (
        ID BIGINT IDENTITY(1,1) NOT NULL CONSTRAINT PK_ProductFavorites PRIMARY KEY,
        UserID BIGINT NOT NULL,
        ProductID BIGINT NOT NULL,
        CreatedAt DATETIME NOT NULL CONSTRAINT DF_ProductFavorites_CreatedAt DEFAULT GETDATE()
    );
END
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = N'UX_ProductFavorites_User_Product' AND object_id = OBJECT_ID(N'dbo.ProductFavorites'))
    CREATE UNIQUE INDEX UX_ProductFavorites_User_Product ON dbo.ProductFavorites (UserID, ProductID);
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = N'IX_ProductFavorites_UserID_CreatedAt' AND object_id = OBJECT_ID(N'dbo.ProductFavorites'))
    CREATE INDEX IX_ProductFavorites_UserID_CreatedAt ON dbo.ProductFavorites (UserID, CreatedAt DESC);
GO

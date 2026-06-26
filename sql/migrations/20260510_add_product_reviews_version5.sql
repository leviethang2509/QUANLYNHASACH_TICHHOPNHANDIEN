IF COL_LENGTH('dbo.Sanpham', 'ReviewFilePath') IS NULL
BEGIN
    ALTER TABLE dbo.Sanpham ADD ReviewFilePath NVARCHAR(500) NULL;
END
GO

IF COL_LENGTH('dbo.Sanpham', 'ReviewFileName') IS NULL
BEGIN
    ALTER TABLE dbo.Sanpham ADD ReviewFileName NVARCHAR(250) NULL;
END
GO

IF COL_LENGTH('dbo.Sanpham', 'YoutubeUrl') IS NULL
BEGIN
    ALTER TABLE dbo.Sanpham ADD YoutubeUrl NVARCHAR(500) NULL;
END
GO

IF OBJECT_ID('dbo.ProductReviews', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.ProductReviews
    (
        IDReview BIGINT IDENTITY(1,1) NOT NULL CONSTRAINT PK_ProductReviews PRIMARY KEY,
        ProductID BIGINT NOT NULL,
        UserID BIGINT NOT NULL,
        UserName NVARCHAR(250) NULL,
        Rating INT NOT NULL,
        Comment NVARCHAR(1000) NOT NULL,
        CreatedAt DATETIME NOT NULL CONSTRAINT DF_ProductReviews_CreatedAt DEFAULT GETDATE(),
        Status BIT NOT NULL CONSTRAINT DF_ProductReviews_Status DEFAULT 1
    );
END
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_ProductReviews_ProductID_CreatedAt' AND object_id = OBJECT_ID('dbo.ProductReviews'))
BEGIN
    CREATE INDEX IX_ProductReviews_ProductID_CreatedAt ON dbo.ProductReviews(ProductID, CreatedAt DESC);
END
GO

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'UX_ProductReviews_ProductID_UserID' AND object_id = OBJECT_ID('dbo.ProductReviews'))
BEGIN
    CREATE UNIQUE INDEX UX_ProductReviews_ProductID_UserID ON dbo.ProductReviews(ProductID, UserID);
END
GO

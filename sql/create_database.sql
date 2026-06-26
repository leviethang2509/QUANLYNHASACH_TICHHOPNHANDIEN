-- sql/create_database.sql
-- Script to create the QLNhaSach database if it does not exist.
-- Adjust file paths if your SQL Server data/log folders differ.

IF DB_ID(N'QLNhaSach') IS NULL
BEGIN
    CREATE DATABASE [QLNhaSach]
    CONTAINMENT = NONE
    ON PRIMARY
    ( NAME = N'QLNhaSach', FILENAME = N'C:\SQLData\QLNhaSach.mdf' , SIZE = 5120KB , MAXSIZE = UNLIMITED, FILEGROWTH = 1024KB )
    LOG ON
    ( NAME = N'QLNhaSach_log', FILENAME = N'C:\SQLLog\QLNhaSach_log.ldf' , SIZE = 1024KB , MAXSIZE = 2048GB , FILEGROWTH = 10%)
END
GO

ALTER DATABASE [QLNhaSach] SET RECOVERY SIMPLE;
GO

USE [QLNhaSach];
GO

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

-- Create schema owner and example permissions (optional)
-- IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = N'appuser')
-- BEGIN
--     CREATE USER [appuser] FOR LOGIN [appuser];
--     EXEC sp_addrolemember N'db_owner', N'appuser';
-- END

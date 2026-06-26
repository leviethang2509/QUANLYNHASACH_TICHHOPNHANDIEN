-- Migration: add StoreLocations table
IF OBJECT_ID(N'dbo.StoreLocations', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.StoreLocations (
        ID INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_StoreLocations PRIMARY KEY,
        StoreName NVARCHAR(200) NOT NULL,
        Latitude DECIMAL(9,6) NOT NULL,
        Longitude DECIMAL(9,6) NOT NULL,
        GeofenceRadius FLOAT NOT NULL CONSTRAINT DF_StoreLocations_GeofenceRadius DEFAULT 5,
        IsActive BIT NOT NULL CONSTRAINT DF_StoreLocations_IsActive DEFAULT 1,
        Address NVARCHAR(500) NULL,
        Phone NVARCHAR(50) NULL,
        Email NVARCHAR(200) NULL,
        IconPath NVARCHAR(500) NULL,
        BannerPath NVARCHAR(500) NULL,
        WelcomeTitle NVARCHAR(300) NULL,
        WelcomeMessage NVARCHAR(1000) NULL,
        AboutContent NVARCHAR(MAX) NULL,
        MissionContent NVARCHAR(MAX) NULL,
        SortOrder INT NOT NULL CONSTRAINT DF_StoreLocations_SortOrder DEFAULT 0
    );
END;
GO

IF COL_LENGTH('dbo.StoreLocations', 'Email') IS NULL
    ALTER TABLE dbo.StoreLocations ADD Email NVARCHAR(200) NULL;

IF COL_LENGTH('dbo.StoreLocations', 'IconPath') IS NULL
    ALTER TABLE dbo.StoreLocations ADD IconPath NVARCHAR(500) NULL;

IF COL_LENGTH('dbo.StoreLocations', 'BannerPath') IS NULL
    ALTER TABLE dbo.StoreLocations ADD BannerPath NVARCHAR(500) NULL;

IF COL_LENGTH('dbo.StoreLocations', 'WelcomeTitle') IS NULL
    ALTER TABLE dbo.StoreLocations ADD WelcomeTitle NVARCHAR(300) NULL;

IF COL_LENGTH('dbo.StoreLocations', 'WelcomeMessage') IS NULL
    ALTER TABLE dbo.StoreLocations ADD WelcomeMessage NVARCHAR(1000) NULL;

IF COL_LENGTH('dbo.StoreLocations', 'AboutContent') IS NULL
    ALTER TABLE dbo.StoreLocations ADD AboutContent NVARCHAR(MAX) NULL;

IF COL_LENGTH('dbo.StoreLocations', 'MissionContent') IS NULL
    ALTER TABLE dbo.StoreLocations ADD MissionContent NVARCHAR(MAX) NULL;
GO

UPDATE dbo.StoreLocations
SET IsActive = 0
WHERE StoreName = N'Dong Trieu Book Store';

UPDATE dbo.StoreLocations
SET Phone = COALESCE(NULLIF(Phone, N''), N'+84 2033670029'),
    Email = COALESCE(NULLIF(Email, N''), N'dongtrieubookstore@gmail.com'),
    IconPath = COALESCE(NULLIF(IconPath, N''), N'/assets/img/imgbook/anhlogo.jpg'),
    BannerPath = COALESCE(NULLIF(BannerPath, N''), N'/assets/img/1920x600/back_ground.jpg'),
    WelcomeTitle = COALESCE(NULLIF(WelcomeTitle, N''), N'Chào mừng bạn đến với ' + StoreName),
    WelcomeMessage = COALESCE(NULLIF(WelcomeMessage, N''), N'Với mong muốn mang đến những cuốn sách hay, nhà sách mở rộng kênh mua sắm trực tuyến để tiếp cận nhiều độc giả hơn. Chân trọng cảm ơn.'),
    AboutContent = COALESCE(NULLIF(AboutContent, N''), N'Đến với không gian mua sắm trực tuyến, khách hàng có thể dễ dàng tìm thấy những cuốn sách hay, đa thể loại cùng dụng cụ học tập, văn phòng phẩm, quà lưu niệm và đồ chơi giáo dục chính hãng. Nhà sách cam kết mang đến trải nghiệm mua sắm an toàn, tiện lợi và chu đáo.'),
    MissionContent = COALESCE(NULLIF(MissionContent, N''), N'Mục tiêu của chúng tôi là mở rộng thị trường sách trực tuyến cùng với đà phát triển của công nghệ thông tin, không ngừng hoàn thiện môi trường phục vụ và nâng cao chất lượng trải nghiệm khách hàng.')
WHERE StoreName <> N'Dong Trieu Book Store';

IF NOT EXISTS (SELECT 1 FROM dbo.StoreLocations WHERE StoreName = N'Nhà sách Tân Hạnh')
BEGIN
    INSERT INTO dbo.StoreLocations (
        StoreName, Latitude, Longitude, GeofenceRadius, IsActive, Address, Phone, Email,
        IconPath, BannerPath, WelcomeTitle, WelcomeMessage, AboutContent, MissionContent, SortOrder
    )
    VALUES (
        N'Nhà sách Tân Hạnh',
        10.963000,
        106.842000,
        5,
        1,
        N'75 Phạm Văn Diêu, Biên Hòa, Đồng Nai, Việt Nam - cần xác minh lại tọa độ GPS chính xác trước production',
        N'+84 2033670029',
        N'dongtrieubookstore@gmail.com',
        N'/assets/img/imgbook/anhlogo.jpg',
        N'/assets/img/1920x600/back_ground.jpg',
        N'Chào mừng bạn đến với Nhà sách Tân Hạnh',
        N'Với mong muốn mang đến những cuốn sách hay, Nhà sách Tân Hạnh mở rộng kênh mua sắm trực tuyến để tiếp cận nhiều độc giả hơn. Chân trọng cảm ơn.',
        N'Đến với không gian mua sắm trực tuyến, khách hàng có thể dễ dàng tìm thấy những cuốn sách hay, đa thể loại cùng dụng cụ học tập, văn phòng phẩm, quà lưu niệm và đồ chơi giáo dục chính hãng. Nhà sách cam kết mang đến trải nghiệm mua sắm an toàn, tiện lợi và chu đáo.',
        N'Mục tiêu của chúng tôi là mở rộng thị trường sách trực tuyến cùng với đà phát triển của công nghệ thông tin, không ngừng hoàn thiện môi trường phục vụ và nâng cao chất lượng trải nghiệm khách hàng.',
        1
    );
END
ELSE
BEGIN
    UPDATE dbo.StoreLocations
    SET Address = N'75 Phạm Văn Diêu, Biên Hòa, Đồng Nai, Việt Nam',
        Phone = COALESCE(NULLIF(Phone, N''), N'+84 2033670029'),
        Email = COALESCE(NULLIF(Email, N''), N'dongtrieubookstore@gmail.com'),
        IconPath = COALESCE(NULLIF(IconPath, N''), N'/assets/img/imgbook/anhlogo.jpg'),
        BannerPath = COALESCE(NULLIF(BannerPath, N''), N'/assets/img/1920x600/back_ground.jpg'),
        WelcomeTitle = COALESCE(NULLIF(WelcomeTitle, N''), N'Chào mừng bạn đến với Nhà sách Tân Hạnh'),
        WelcomeMessage = COALESCE(NULLIF(WelcomeMessage, N''), N'Với mong muốn mang đến những cuốn sách hay, Nhà sách Tân Hạnh mở rộng kênh mua sắm trực tuyến để tiếp cận nhiều độc giả hơn. Chân trọng cảm ơn.'),
        AboutContent = COALESCE(NULLIF(AboutContent, N''), N'Đến với không gian mua sắm trực tuyến, khách hàng có thể dễ dàng tìm thấy những cuốn sách hay, đa thể loại cùng dụng cụ học tập, văn phòng phẩm, quà lưu niệm và đồ chơi giáo dục chính hãng. Nhà sách cam kết mang đến trải nghiệm mua sắm an toàn, tiện lợi và chu đáo.'),
        MissionContent = COALESCE(NULLIF(MissionContent, N''), N'Mục tiêu của chúng tôi là mở rộng thị trường sách trực tuyến cùng với đà phát triển của công nghệ thông tin, không ngừng hoàn thiện môi trường phục vụ và nâng cao chất lượng trải nghiệm khách hàng.'),
        GeofenceRadius = 5,
        IsActive = 1,
        SortOrder = 1
    WHERE StoreName = N'Nhà sách Tân Hạnh';
END;

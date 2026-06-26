using Mood.EF2;
using System;
using System.Collections.Generic;
using System.Data.Entity;
using System.Linq;

namespace Common.Repositories
{
    public class PagedResult<T>
    {
        public IList<T> Items { get; set; }
        public int Total { get; set; }
        public int Page { get; set; }
        public int PageSize { get; set; }
    }

    public class LogRepository
    {
        public void AddFaceAuthLog(FaceAuthLog log)
        {
            try
            {
                using (var db = new LogDbContext())
                {
                    EnsureLogTables(db);
                    db.FaceAuthLogs.Add(log);
                    db.SaveChanges();
                }
            }
            catch
            {
                // Logging must not break the main user flow.
            }
        }

        public void AddGeofenceLog(GeofenceLog log)
        {
            try
            {
                using (var db = new LogDbContext())
                {
                    EnsureLogTables(db);
                    db.GeofenceLogs.Add(log);
                    db.SaveChanges();
                }
            }
            catch
            {
                // Logging must not break the main user flow.
            }
        }

        public void AddRentalLog(RentalLog log)
        {
            try
            {
                using (var db = new LogDbContext())
                {
                    EnsureLogTables(db);
                    db.RentalLogs.Add(log);
                    db.SaveChanges();
                }
            }
            catch
            {
                // Logging must not break the main user flow.
            }
        }

        public PagedResult<FaceAuthLog> GetFaceAuthLogs(int page = 1, int pageSize = 50, long? userId = null, string action = null, DateTime? fromDate = null, DateTime? toDate = null, bool? result = null)
        {
            page = NormalizePage(page);
            pageSize = NormalizePageSize(pageSize);

            using (var db = new LogDbContext())
            {
                EnsureLogTables(db);
                var toDateExclusive = toDate.HasValue ? (DateTime?)NormalizeToExclusive(toDate.Value) : null;
                var query = db.FaceAuthLogs.AsNoTracking().AsQueryable();
                if (userId.HasValue) query = query.Where(x => x.UserID == userId.Value);
                if (!string.IsNullOrWhiteSpace(action)) query = query.Where(x => x.Action == action);
                if (fromDate.HasValue) query = query.Where(x => x.Timestamp >= fromDate.Value);
                if (toDateExclusive.HasValue) query = query.Where(x => x.Timestamp < toDateExclusive.Value);
                if (result.HasValue) query = query.Where(x => x.Result == result.Value);

                return ToPagedResult(query.OrderByDescending(x => x.Timestamp), page, pageSize);
            }
        }

        public PagedResult<GeofenceLog> GetGeofenceLogs(int page = 1, int pageSize = 50, long? userId = null, int? storeId = null, DateTime? fromDate = null, DateTime? toDate = null, bool? inZone = null)
        {
            page = NormalizePage(page);
            pageSize = NormalizePageSize(pageSize);

            using (var db = new LogDbContext())
            {
                EnsureLogTables(db);
                var toDateExclusive = toDate.HasValue ? (DateTime?)NormalizeToExclusive(toDate.Value) : null;
                var query = db.GeofenceLogs.AsNoTracking().AsQueryable();
                if (userId.HasValue) query = query.Where(x => x.UserID == userId.Value);
                if (storeId.HasValue) query = query.Where(x => x.StoreID == storeId.Value);
                if (fromDate.HasValue) query = query.Where(x => x.Timestamp >= fromDate.Value);
                if (toDateExclusive.HasValue) query = query.Where(x => x.Timestamp < toDateExclusive.Value);
                if (inZone.HasValue) query = query.Where(x => x.IsInZone == inZone.Value);

                return ToPagedResult(query.OrderByDescending(x => x.Timestamp), page, pageSize);
            }
        }

        public PagedResult<RentalLog> GetRentalLogs(int page = 1, int pageSize = 50, long? userId = null, int? rentalId = null, string action = null, DateTime? fromDate = null, DateTime? toDate = null)
        {
            page = NormalizePage(page);
            pageSize = NormalizePageSize(pageSize);

            using (var db = new LogDbContext())
            {
                EnsureLogTables(db);
                var toDateExclusive = toDate.HasValue ? (DateTime?)NormalizeToExclusive(toDate.Value) : null;
                var query = db.RentalLogs.AsNoTracking().AsQueryable();
                if (userId.HasValue) query = query.Where(x => x.UserID == userId.Value || x.ActorUserID == userId.Value);
                if (rentalId.HasValue) query = query.Where(x => x.RentalID == rentalId.Value);
                if (!string.IsNullOrWhiteSpace(action)) query = query.Where(x => x.Action == action);
                if (fromDate.HasValue) query = query.Where(x => x.Timestamp >= fromDate.Value);
                if (toDateExclusive.HasValue) query = query.Where(x => x.Timestamp < toDateExclusive.Value);

                return ToPagedResult(query.OrderByDescending(x => x.Timestamp), page, pageSize);
            }
        }

        public string GetRuntimeDatabaseInfo()
        {
            try
            {
                using (var db = new LogDbContext())
                {
                    EnsureLogTables(db);
                    var connection = db.Database.Connection;
                    return string.Format("{0} / {1}", connection.DataSource, connection.Database);
                }
            }
            catch (Exception ex)
            {
                return "Khong doc duoc DB log: " + ex.Message;
            }
        }

        private static int NormalizePage(int page)
        {
            return page < 1 ? 1 : page;
        }

        private static int NormalizePageSize(int pageSize)
        {
            if (pageSize < 1) return 50;
            return pageSize > 200 ? 200 : pageSize;
        }

        private static DateTime NormalizeToExclusive(DateTime toDate)
        {
            return toDate.TimeOfDay == TimeSpan.Zero ? toDate.Date.AddDays(1) : toDate;
        }

        private static PagedResult<T> ToPagedResult<T>(IQueryable<T> query, int page, int pageSize)
        {
            var total = query.Count();
            var totalPages = (int)Math.Ceiling((double)total / pageSize);
            if (totalPages < 1) totalPages = 1;
            if (page > totalPages) page = totalPages;
            var items = query.Skip((page - 1) * pageSize).Take(pageSize).ToList();
            return new PagedResult<T>
            {
                Items = items,
                Total = total,
                Page = page,
                PageSize = pageSize
            };
        }

        private static void EnsureLogTables(LogDbContext db)
        {
            db.Database.ExecuteSqlCommand(@"
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
END;");
        }
    }
}

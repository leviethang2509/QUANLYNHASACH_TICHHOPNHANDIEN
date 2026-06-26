using Mood.EF2;
using System;
using System.Collections.Generic;
using System.Linq;
using X.PagedList;

namespace Mood.Draw
{
    public class ProductFavoriteDraw
    {
        private readonly QuanLySachDBContext db;

        public ProductFavoriteDraw()
        {
            db = new QuanLySachDBContext();
        }

        public bool IsFavorite(long userId, long productId)
        {
            EnsureProductFavoritesTable();
            return db.Set<ProductFavorite>().Any(x => x.UserID == userId && x.ProductID == productId);
        }

        public int CountByUser(long userId)
        {
            EnsureProductFavoritesTable();
            return db.Set<ProductFavorite>().Count(x => x.UserID == userId);
        }

        public bool Toggle(long userId, long productId, out bool isFavorite)
        {
            EnsureProductFavoritesTable();
            isFavorite = false;
            var productExists = db.Sanphams.Any(x => x.IDContent == productId && x.Status == true);
            if (!productExists)
            {
                return false;
            }

            var current = db.Set<ProductFavorite>().FirstOrDefault(x => x.UserID == userId && x.ProductID == productId);
            if (current != null)
            {
                db.Set<ProductFavorite>().Remove(current);
                db.SaveChanges();
                return true;
            }

            db.Set<ProductFavorite>().Add(new ProductFavorite
            {
                UserID = userId,
                ProductID = productId,
                CreatedAt = DateTime.Now
            });
            db.SaveChanges();
            isFavorite = true;
            return true;
        }

        public int AddMissing(long userId, IEnumerable<long> productIds)
        {
            EnsureProductFavoritesTable();
            var ids = (productIds ?? new List<long>()).Where(x => x > 0).Distinct().Take(100).ToList();
            if (!ids.Any())
            {
                return 0;
            }

            var validIds = db.Sanphams
                .Where(x => ids.Contains(x.IDContent) && x.Status == true)
                .Select(x => x.IDContent)
                .ToList();
            if (!validIds.Any())
            {
                return 0;
            }

            var existingIds = db.Set<ProductFavorite>()
                .Where(x => x.UserID == userId && validIds.Contains(x.ProductID))
                .Select(x => x.ProductID)
                .ToList();
            var newIds = validIds.Except(existingIds).ToList();
            foreach (var id in newIds)
            {
                db.Set<ProductFavorite>().Add(new ProductFavorite
                {
                    UserID = userId,
                    ProductID = id,
                    CreatedAt = DateTime.Now
                });
            }

            if (newIds.Any())
            {
                db.SaveChanges();
            }

            return newIds.Count;
        }

        public IEnumerable<Sanpham> ListByUser(long userId, string searchString, int page, int pageSize)
        {
            EnsureProductFavoritesTable();
            var query = from f in db.Set<ProductFavorite>()
                        join p in db.Sanphams on f.ProductID equals p.IDContent
                        where f.UserID == userId && p.Status == true
                        select new { Favorite = f, Product = p };

            if (!string.IsNullOrWhiteSpace(searchString))
            {
                query = query.Where(x => x.Product.Name.Contains(searchString) || x.Product.TacGia.Contains(searchString));
            }

            return query.OrderByDescending(x => x.Favorite.CreatedAt)
                .Select(x => x.Product)
                .ToPagedList(page, pageSize);
        }

        public List<Sanpham> ListByIds(IEnumerable<long> productIds)
        {
            EnsureProductFavoritesTable();
            var ids = (productIds ?? new List<long>()).Distinct().Take(100).ToList();
            if (!ids.Any())
            {
                return new List<Sanpham>();
            }

            return db.Sanphams
                .Where(x => ids.Contains(x.IDContent) && x.Status == true)
                .ToList()
                .OrderBy(x => ids.IndexOf(x.IDContent))
                .ToList();
        }

        private void EnsureProductFavoritesTable()
        {
            db.Database.ExecuteSqlCommand(@"
IF OBJECT_ID(N'dbo.ProductFavorites', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.ProductFavorites (
        ID BIGINT IDENTITY(1,1) NOT NULL CONSTRAINT PK_ProductFavorites PRIMARY KEY,
        UserID BIGINT NOT NULL,
        ProductID BIGINT NOT NULL,
        CreatedAt DATETIME NOT NULL CONSTRAINT DF_ProductFavorites_CreatedAt DEFAULT GETDATE()
    );
END;

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = N'UX_ProductFavorites_User_Product' AND object_id = OBJECT_ID(N'dbo.ProductFavorites'))
    CREATE UNIQUE INDEX UX_ProductFavorites_User_Product ON dbo.ProductFavorites (UserID, ProductID);

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = N'IX_ProductFavorites_UserID_CreatedAt' AND object_id = OBJECT_ID(N'dbo.ProductFavorites'))
    CREATE INDEX IX_ProductFavorites_UserID_CreatedAt ON dbo.ProductFavorites (UserID, CreatedAt DESC);");
        }
    }
}

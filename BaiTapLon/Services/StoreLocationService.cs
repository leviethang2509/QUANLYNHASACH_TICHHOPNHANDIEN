using Mood.EF2;
using System.Data.Entity;
using System.Linq;

namespace BaiTapLon.Services
{
    public class StoreLocationService
    {
        public StoreLocation GetActiveStore()
        {
            using (var db = new QuanLySachDBContext())
            {
                return GetActiveStore(db);
            }
        }

        public StoreLocation GetActiveStore(QuanLySachDBContext db)
        {
            var store = db.StoreLocations.AsNoTracking()
                .Where(x => x.IsActive)
                .OrderBy(x => x.SortOrder)
                .ThenByDescending(x => x.ID)
                .ThenBy(x => x.StoreName)
                .FirstOrDefault();

            return store ?? db.StoreLocations.AsNoTracking()
                .OrderBy(x => x.SortOrder)
                .ThenByDescending(x => x.ID)
                .ThenBy(x => x.StoreName)
                .FirstOrDefault()
                ?? CreateDefaultStore();
        }

        public StoreLocation CreateDefaultStore()
        {
            return new StoreLocation
            {
                StoreName = "Nha sach",
                Address = "Chua cau hinh dia chi nha sach",
                Phone = "",
                Email = "",
                IconPath = "/assets/img/imgbook/anhlogo.jpg",
                BannerPath = "/assets/img/1920x600/back_ground.jpg",
                WelcomeTitle = "Chao mung ban den voi nha sach",
                WelcomeMessage = "Vui long cap nhat noi dung gioi thieu tai trang quan tri thong tin nha sach.",
                AboutContent = "Thong tin gioi thieu dang cho cau hinh.",
                MissionContent = "Muc tieu hoat dong dang cho cau hinh.",
                Latitude = 0,
                Longitude = 0,
                GeofenceRadius = 5,
                IsActive = true,
                SortOrder = 1
            };
        }
    }
}

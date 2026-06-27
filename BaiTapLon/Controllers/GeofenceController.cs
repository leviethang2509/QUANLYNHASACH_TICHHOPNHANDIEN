using Common.Repositories;
using Mood.EF2;
using BaiTapLon.Services;
using System;
using System.Configuration;
using System.Globalization;
using System.Linq;
using System.Web.Mvc;

namespace BaiTapLon.Controllers
{
    public class GeofenceController : Controller
    {
        private readonly LogRepository _logRepo = new LogRepository();

        [HttpPost]
        public ActionResult CheckGeofence(decimal? lat = null, decimal? lon = null, int userId = 0)
        {
            try
            {
                var userLat = ResolveCoordinate(lat, "lat");
                var userLon = ResolveCoordinate(lon, "lon");
                if (!userLat.HasValue || !userLon.HasValue)
                {
                    return Json(new { inZone = false, error = "Không nhận được tọa độ từ trình duyệt. Vui lòng cấp quyền vị trí và thử lại." });
                }

                if (userLat.Value < -90 || userLat.Value > 90 || userLon.Value < -180 || userLon.Value > 180)
                {
                    return Json(new { inZone = false, error = "Invalid coordinates" });
                }

                var resolvedUserId = ResolveUserId(userId);
                StoreDistance nearest;
                using (var db = new QuanLySachDBContext())
                {
                    var activeStore = new StoreLocationService().GetActiveStore(db);
                    var stores = activeStore.ID > 0
                        ? db.StoreLocations.Where(x => x.IsActive).ToList()
                        : new System.Collections.Generic.List<StoreLocation> { activeStore };

                    if (!stores.Any())
                    {
                        return Json(new { inZone = false, error = "No active store configured" });
                    }

                    nearest = stores
                        .Select(store => new StoreDistance
                        {
                            Store = store,
                            DistanceKm = CalculateDistance((double)userLat.Value, (double)userLon.Value, (double)store.Latitude, (double)store.Longitude)
                        })
                        .OrderBy(x => x.DistanceKm)
                        .First();
                }

                var radiusKm = nearest.Store.GeofenceRadius > 0 ? nearest.Store.GeofenceRadius : GetDefaultRadiusKm();
                var isInZone = nearest.DistanceKm <= radiusKm;

                var log = new GeofenceLog
                {
                    UserID = resolvedUserId,
                    StoreID = nearest.Store.ID,
                    IsInZone = isInZone,
                    Timestamp = DateTime.UtcNow,
                    UserLat = userLat.Value,
                    UserLon = userLon.Value,
                    Distance = nearest.DistanceKm,
                    AllowedRadiusKm = radiusKm,
                    StoreName = nearest.Store.StoreName
                };
                _logRepo.AddGeofenceLog(log);

                return Json(new
                {
                    inZone = isInZone,
                    distance = nearest.DistanceKm,
                    radiusKm,
                    storeId = nearest.Store.ID,
                    storeName = nearest.Store.StoreName
                });
            }
            catch (Exception ex)
            {
                return Json(new { inZone = false, error = ex.Message });
            }
        }

        private decimal? ResolveCoordinate(decimal? boundValue, string key)
        {
            if (boundValue.HasValue)
            {
                return boundValue.Value;
            }

            var rawValue = Request.Form[key] ?? Request.QueryString[key];
            if (string.IsNullOrWhiteSpace(rawValue))
            {
                return null;
            }

            decimal parsed;
            if (decimal.TryParse(rawValue, NumberStyles.Float, CultureInfo.InvariantCulture, out parsed)
                || decimal.TryParse(rawValue, NumberStyles.Float, CultureInfo.CurrentCulture, out parsed))
            {
                return parsed;
            }

            return null;
        }

        private double CalculateDistance(double lat1, double lon1, double lat2, double lon2)
        {
            var R = 6371; // km
            var dLat = ToRad(lat2 - lat1);
            var dLon = ToRad(lon2 - lon1);
            var a = Math.Sin(dLat/2) * Math.Sin(dLat/2) + Math.Cos(ToRad(lat1)) * Math.Cos(ToRad(lat2)) * Math.Sin(dLon/2) * Math.Sin(dLon/2);
            var c = 2 * Math.Atan2(Math.Sqrt(a), Math.Sqrt(1-a));
            return R * c;
        }

        private double ToRad(double deg) => deg * (Math.PI / 180);

        private static double GetDefaultRadiusKm()
        {
            double radius;
            return double.TryParse(ConfigurationManager.AppSettings["GeofenceDefaultRadiusKm"], out radius) && radius > 0 ? radius : 5;
        }

        private long ResolveUserId(int requestUserId)
        {
            var userSession = Session[BaiTapLon.Common.Constant.USER_SESSION] as BaiTapLon.Common.UserLogin;
            if (userSession != null && userSession.userId > 0)
            {
                return userSession.userId;
            }

            long authenticatedUserId;
            if (User != null && User.Identity != null && User.Identity.IsAuthenticated && long.TryParse(User.Identity.Name, out authenticatedUserId))
            {
                return authenticatedUserId;
            }

            return requestUserId;
        }
        private class StoreDistance
        {
            public StoreLocation Store { get; set; }
            public double DistanceKm { get; set; }
        }
    }
}

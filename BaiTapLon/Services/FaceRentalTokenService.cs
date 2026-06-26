using System;
using System.Configuration;
using System.Web;

namespace BaiTapLon.Services
{
    public class FaceRentalTokenService
    {
        private const string CachePrefix = "face-rental-token:";

        public string Create(long userId, long productId, string requestId)
        {
            var token = Guid.NewGuid().ToString("N");
            var expiresAtUtc = DateTime.UtcNow.AddMinutes(GetTokenMinutes());
            HttpRuntime.Cache.Insert(
                CachePrefix + token,
                new FaceRentalToken
                {
                    UserId = userId,
                    ProductId = productId,
                    RequestId = requestId,
                    ExpiresAtUtc = expiresAtUtc
                },
                null,
                expiresAtUtc,
                System.Web.Caching.Cache.NoSlidingExpiration);

            return token;
        }

        public bool ValidateAndConsume(string token, long userId, long productId)
        {
            if (string.IsNullOrWhiteSpace(token)) return false;

            var cacheKey = CachePrefix + token;
            var payload = HttpRuntime.Cache[cacheKey] as FaceRentalToken;
            if (payload == null) return false;
            if (payload.ExpiresAtUtc < DateTime.UtcNow) return false;
            if (payload.UserId != userId || payload.ProductId != productId) return false;

            HttpRuntime.Cache.Remove(cacheKey);
            return true;
        }

        private static int GetTokenMinutes()
        {
            int value;
            return int.TryParse(ConfigurationManager.AppSettings["FaceAuthRentalTokenMinutes"], out value) && value > 0 ? value : 3;
        }

        private class FaceRentalToken
        {
            public long UserId { get; set; }
            public long ProductId { get; set; }
            public string RequestId { get; set; }
            public DateTime ExpiresAtUtc { get; set; }
        }
    }
}

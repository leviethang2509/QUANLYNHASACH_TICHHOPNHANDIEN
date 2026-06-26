using System;
using System.ComponentModel.DataAnnotations;

namespace Mood.EF2
{
    public class GeofenceLog
    {
        public int ID { get; set; }
        public long UserID { get; set; }
        public int StoreID { get; set; }
        public bool IsInZone { get; set; }
        public DateTime Timestamp { get; set; }
        public decimal UserLat { get; set; }
        public decimal UserLon { get; set; }
        public double Distance { get; set; } // km
        public double AllowedRadiusKm { get; set; }
        [StringLength(200)]
        public string StoreName { get; set; }
    }
}

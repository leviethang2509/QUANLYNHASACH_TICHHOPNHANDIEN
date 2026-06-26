using System;
using System.ComponentModel.DataAnnotations;

namespace Mood.EF2
{
    public class FaceAuthLog
    {
        public int ID { get; set; }
        public long UserID { get; set; }
        [Required]
        [StringLength(50)]
        public string Action { get; set; } // Register, Verify, Authenticate
        public DateTime Timestamp { get; set; }
        [StringLength(45)]
        public string IP { get; set; }
        [StringLength(500)]
        public string DeviceInfo { get; set; }
        [StringLength(500)]
        public string ImagePath { get; set; }
        public bool Result { get; set; }
        public double Confidence { get; set; }
        [StringLength(1000)]
        public string ErrorMessage { get; set; }
        [StringLength(64)]
        public string RequestId { get; set; }
        [StringLength(50)]
        public string Purpose { get; set; }
        [StringLength(100)]
        public string ErrorCode { get; set; }
        public bool? LivenessPassed { get; set; }
    }
}

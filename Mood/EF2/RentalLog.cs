using System;
using System.ComponentModel.DataAnnotations;

namespace Mood.EF2
{
    public class RentalLog
    {
        public int ID { get; set; }
        public int RentalID { get; set; }
        public long UserID { get; set; }
        public long? ActorUserID { get; set; }
        [Required]
        [StringLength(50)]
        public string Action { get; set; } // Request, Approve, Reject, Return
        public DateTime Timestamp { get; set; }
        public string Details { get; set; }
        [StringLength(50)]
        public string OldStatus { get; set; }
        [StringLength(50)]
        public string NewStatus { get; set; }
    }
}

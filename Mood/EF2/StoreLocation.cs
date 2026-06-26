namespace Mood.EF2
{
    using System.ComponentModel.DataAnnotations;

    public class StoreLocation
    {
        public int ID { get; set; }
        [Required]
        [StringLength(200)]
        public string StoreName { get; set; }
        [Range(-90, 90)]
        public decimal Latitude { get; set; }
        [Range(-180, 180)]
        public decimal Longitude { get; set; }
        [Range(0.01, 100)]
        public double GeofenceRadius { get; set; }
        public bool IsActive { get; set; }
        [StringLength(500)]
        public string Address { get; set; }
        [StringLength(50)]
        public string Phone { get; set; }
        [StringLength(200)]
        public string Email { get; set; }
        [StringLength(500)]
        public string IconPath { get; set; }
        [StringLength(500)]
        public string BannerPath { get; set; }
        [StringLength(300)]
        public string WelcomeTitle { get; set; }
        [StringLength(1000)]
        public string WelcomeMessage { get; set; }
        public string AboutContent { get; set; }
        public string MissionContent { get; set; }
        public int SortOrder { get; set; }
    }
}

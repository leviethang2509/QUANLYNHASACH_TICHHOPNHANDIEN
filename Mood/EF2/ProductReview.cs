namespace Mood.EF2
{
    using System;
    using System.ComponentModel.DataAnnotations;
    using System.ComponentModel.DataAnnotations.Schema;

    [Table("ProductReviews")]
    public partial class ProductReview
    {
        [Key]
        public long IDReview { get; set; }

        public long ProductID { get; set; }

        public long UserID { get; set; }

        [StringLength(250)]
        public string UserName { get; set; }

        [Range(1, 5)]
        public int Rating { get; set; }

        [Required]
        [StringLength(1000)]
        public string Comment { get; set; }

        public DateTime CreatedAt { get; set; }

        public bool Status { get; set; }
    }
}

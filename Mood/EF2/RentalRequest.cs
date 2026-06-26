namespace Mood.EF2
{
    using System;
    using System.ComponentModel.DataAnnotations;
    using System.ComponentModel.DataAnnotations.Schema;

    [Table("RentalRequests")]
    public class RentalRequest
    {
        [Key]
        public int ID { get; set; }

        public long ProductID { get; set; }

        public long UserID { get; set; }

        public int Quantity { get; set; }

        [Required]
        [StringLength(50)]
        public string Status { get; set; }

        public DateTime RequestedAt { get; set; }

        public DateTime RequestDate { get; set; }

        public int BorrowDays { get; set; }

        public DateTime ExpectedReturnDate { get; set; }

        public DateTime? ApprovedAt { get; set; }

        public DateTime? ReturnedAt { get; set; }

        public DateTime? ActualReturnDate { get; set; }

        public long? AdminID { get; set; }

        [StringLength(500)]
        public string RejectReason { get; set; }

        [StringLength(1000)]
        public string Details { get; set; }

        [StringLength(30)]
        public string IdentityNumber { get; set; }

        [StringLength(250)]
        public string IdentityFullName { get; set; }

        [StringLength(500)]
        public string IdentityCardImagePath { get; set; }

        [StringLength(500)]
        public string IdentityCardFrontImagePath { get; set; }

        [StringLength(500)]
        public string IdentityCardBackImagePath { get; set; }

        [StringLength(500)]
        public string IdentityAddress { get; set; }

        [StringLength(250)]
        public string IdentityPlaceOfBirth { get; set; }

        [Column(TypeName = "date")]
        public DateTime? IdentityDateOfBirth { get; set; }

        [Column(TypeName = "date")]
        public DateTime? IdentityIssueDate { get; set; }

        [Column(TypeName = "date")]
        public DateTime? IdentityExpiryDate { get; set; }

        [StringLength(30)]
        public string IdentityGender { get; set; }

        [StringLength(100)]
        public string IdentityNationality { get; set; }

        [StringLength(250)]
        public string IdentityIssuePlace { get; set; }

        [StringLength(250)]
        public string IdentityIssuingAuthority { get; set; }

        public double? IdentityFaceConfidence { get; set; }

        [StringLength(4000)]
        public string IdentityOcrRawJson { get; set; }
    }
}

namespace Mood.EF2
{
    using System;
    using System.Collections.Generic;
    using System.ComponentModel.DataAnnotations;
    using System.ComponentModel.DataAnnotations.Schema;
    using System.Data.Entity.Spatial;

    [Table("User")]
    public partial class User
    {
        [Key]
        [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
        public long IDUser { get; set; }

        [Required]
        [StringLength(250)]
        [Display(Name = "Tài khoản")]
        public string UserName { get; set; }

        [Required]
        [StringLength(250)]
        [Display(Name = "Mật khẩu")]
        public string PassWord { get; set; }

        [Required]
        [StringLength(250)]
        [Display(Name = "Họ tên")]
        public string Name { get; set; }

        [StringLength(250)]
        [Required(ErrorMessage = "Không quá 250 kí tự")]
        [Display(Name = "Địa chỉ")]
        public string Adress { get; set; }

        [Required]
        [StringLength(250)]
        public string Email { get; set; }

        [StringLength(250)]
        public string NotificationEmail { get; set; }

        [Required]
        [StringLength(250)]
        [Display(Name = "Số điện thoại")]
        public string Phone { get; set; }

        [Display(Name = "Trạng thái")]
        public bool Status { get; set; }


        [Column(TypeName = "date")]
        public DateTime? NgayTao { get; set; }

        [StringLength(50)]
        public string NguoiTao { get; set; }

        [Column(TypeName = "date")]
        public DateTime? ModifiedDate { get; set; }

        [StringLength(50)]
        public string ModifiedBy { get; set; }
        [Display(Name = "Chức danh")]
        public long IDQuyen { get; set; }

        [StringLength(30)]
        public string IdentityNumber { get; set; }

        [StringLength(250)]
        public string IdentityFullName { get; set; }

        [Column(TypeName = "date")]
        public DateTime? IdentityDateOfBirth { get; set; }

        [StringLength(500)]
        public string IdentityAddress { get; set; }

        [StringLength(250)]
        public string IdentityPlaceOfBirth { get; set; }

        [StringLength(30)]
        public string IdentityGender { get; set; }

        [StringLength(100)]
        public string IdentityNationality { get; set; }

        [Column(TypeName = "date")]
        public DateTime? IdentityIssueDate { get; set; }

        [StringLength(250)]
        public string IdentityIssuePlace { get; set; }

        [Column(TypeName = "date")]
        public DateTime? IdentityExpiryDate { get; set; }

        [StringLength(250)]
        public string IdentityIssuingAuthority { get; set; }

        [StringLength(500)]
        public string IdentityCardImagePath { get; set; }

        [StringLength(500)]
        public string IdentityCardFrontImagePath { get; set; }

        [StringLength(500)]
        public string IdentityCardBackImagePath { get; set; }

        public DateTime? IdentityVerifiedAt { get; set; }

        public double? IdentityFaceConfidence { get; set; }
    }
}

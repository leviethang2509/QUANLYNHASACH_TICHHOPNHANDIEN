using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Web;
using BotDetect.Web.Mvc;

namespace BaiTapLon.Models
{
    public class RegisterModel
    {
        
        [Display(Name = "Tên đăng nhập")]
        [Required(ErrorMessage ="Yêu cầu nhập tên đăng nhập")]

        public string UserName { set; get; }

        [Display(Name = "Mật khẩu")]
        [StringLength(20,MinimumLength =8,ErrorMessage ="Độ dài mật khẩu ít nhất 8 kí tự")]
        [Required(ErrorMessage = "Yêu cầu nhập mật khẩu")]
        public string PassWord { set; get; }

        [Display(Name = "Xác nhận mật khẩu")]
        [Required(ErrorMessage = "Yêu cầu nhập xác nhận mật khẩu")]
        public string ConfirmPass { set; get; }

        [Display(Name = "Họ tên")]
        [Required(ErrorMessage = "Yêu cầu nhập họ tên")]
        public string Name { set; get; }

        [Display(Name = "Địa chỉ")]
        [Required(ErrorMessage = "Yêu cầu nhập địa chỉ")]
        public string Address { set; get; }

        [Display(Name = "Số điện thoại")]
        [Required(ErrorMessage = "Yêu cầu nhập số điện thoại")]
        public string Phone { set; get; }
        public string Email { set; get; }

        [Display(Name = "Gmail nhận thông báo mượn trả")]
        [StringLength(250)]
        [Required(ErrorMessage = "Yêu cầu nhập Gmail nhận thông báo")]
        public string NotificationEmail { set; get; }
        [Display(Name = "Chức danh")]
        public long IDQuyen { set; get; }

        [Display(Name = "Số CMND/CCCD")]
        [StringLength(30)]
        public string IdentityNumber { set; get; }

        [Display(Name = "Họ tên trên CMND/CCCD")]
        [StringLength(250)]
        public string IdentityFullName { set; get; }

        [Display(Name = "Ngày sinh trên CMND/CCCD")]
        public DateTime? IdentityDateOfBirth { set; get; }

        [Display(Name = "Địa chỉ trên CMND/CCCD")]
        [StringLength(500)]
        public string IdentityAddress { set; get; }

        [Display(Name = "Quê quán trên CMND/CCCD")]
        [StringLength(250)]
        public string IdentityPlaceOfBirth { set; get; }

        [Display(Name = "Giới tính trên CMND/CCCD")]
        [StringLength(30)]
        public string IdentityGender { set; get; }

        [Display(Name = "Quốc tịch trên CMND/CCCD")]
        [StringLength(100)]
        public string IdentityNationality { set; get; }

        [Display(Name = "Ngày cấp CMND/CCCD")]
        public DateTime? IdentityIssueDate { set; get; }

        [Display(Name = "Nơi cấp CMND/CCCD")]
        [StringLength(250)]
        public string IdentityIssuePlace { set; get; }

        [Display(Name = "Ngày hết hạn CMND/CCCD")]
        public DateTime? IdentityExpiryDate { set; get; }

        [Display(Name = "Cơ quan cấp CMND/CCCD")]
        [StringLength(250)]
        public string IdentityIssuingAuthority { set; get; }

    }
}

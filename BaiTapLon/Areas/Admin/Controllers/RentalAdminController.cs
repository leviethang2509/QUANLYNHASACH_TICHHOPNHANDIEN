using BaiTapLon.Common;
using BaiTapLon.Services;
using Common.Repositories;
using Mood.EF2;
using System;
using System.Data.Entity;
using System.Linq;
using System.Web.Mvc;

namespace BaiTapLon.Areas.Admin.Controllers
{
    public class RentalAdminController : BaseController
    {
        public ActionResult Index(string status = null)
        {
            using (var db = new QuanLySachDBContext())
            {
                var query = from rental in db.RentalRequests.AsNoTracking()
                            join product in db.Sanphams.AsNoTracking() on rental.ProductID equals product.IDContent into productJoin
                            from product in productJoin.DefaultIfEmpty()
                            join user in db.Users.AsNoTracking() on rental.UserID equals user.IDUser into userJoin
                            from user in userJoin.DefaultIfEmpty()
                            select new RentalAdminItem
                            {
                                ID = rental.ID,
                                ProductID = rental.ProductID,
                                ProductName = product != null ? product.Name : "",
                                ProductImage = product != null ? product.Images : "",
                                Stock = product != null ? (product.TonKho.HasValue ? product.TonKho.Value : product.Soluong) : 0,
                                UserID = rental.UserID,
                                UserName = user != null ? user.UserName : "",
                                CustomerName = user != null ? user.Name : "",
                                CustomerPhone = user != null ? user.Phone : "",
                                Quantity = rental.Quantity,
                                Status = rental.Status,
                                RequestedAt = rental.RequestedAt,
                                RequestDate = rental.RequestDate,
                                BorrowDays = rental.BorrowDays,
                                ExpectedReturnDate = rental.ExpectedReturnDate,
                                ApprovedAt = rental.ApprovedAt,
                                ReturnedAt = rental.ReturnedAt,
                                ActualReturnDate = rental.ActualReturnDate,
                                RejectReason = rental.RejectReason,
                                Details = rental.Details,
                                IdentityNumber = rental.IdentityNumber,
                                IdentityFullName = rental.IdentityFullName,
                                IdentityCardImagePath = rental.IdentityCardImagePath,
                                IdentityFaceConfidence = rental.IdentityFaceConfidence,
                                AdminID = rental.AdminID
                            };

                if (!string.IsNullOrWhiteSpace(status))
                {
                    query = status == "Borrowing"
                        ? query.Where(x => x.Status == "Borrowing" || x.Status == "Borrowed")
                        : query.Where(x => x.Status == status);
                }

                ViewBag.Status = status;
                ViewBag.PendingCount = db.RentalRequests.Count(x => x.Status == "Pending");
                ViewBag.BorrowingCount = db.RentalRequests.Count(x => x.Status == "Borrowing" || x.Status == "Borrowed" || x.Status == "Overdue");
                ViewBag.ReturnedCount = db.RentalRequests.Count(x => x.Status == "Returned");
                ViewBag.OverdueCount = db.RentalRequests.Count(x => x.Status == "Overdue");

                return View(query.OrderByDescending(x => x.RequestedAt).Take(200).ToList());
            }
        }

        [HttpPost]
        public ActionResult UpdateStatus(int id, string status)
        {
            var admin = Session[Constant.ADMIN_SESSION] as AdminLogin;
            var adminId = admin != null ? admin.userId : 0;
            var result = new BaiTapLon.Controllers.RentalController();
            result.ControllerContext = ControllerContext;
            var updateResult = result.UpdateRentalStatus(id, status, adminId) as JsonResult;
            var data = updateResult != null ? updateResult.Data : null;
            var success = GetJsonValue<bool>(data, "success");
            var error = GetJsonValue<string>(data, "error");
            var mailSent = GetJsonValue<bool>(data, "mailSent");
            var mailMessage = GetJsonValue<string>(data, "mailMessage");

            if (success)
            {
                var approveAction = status == "Approve" || status == "Borrow";
                var successMessage = approveAction
                    ? "Duyệt mượn sách thành công."
                    : "Cập nhật trạng thái mượn sách thành công.";
                TempData["RentalAdminMessage"] = mailSent
                    ? successMessage + " Đã gửi thông báo Gmail."
                    : successMessage + " Không gửi được Gmail: " + (string.IsNullOrWhiteSpace(mailMessage) ? "không tìm thấy hoặc Gmail khách hàng không hợp lệ." : mailMessage);
            }
            else
            {
                TempData["RentalAdminError"] = string.IsNullOrWhiteSpace(error)
                    ? "Không thể cập nhật trạng thái mượn sách."
                    : error;
            }

            return RedirectToAction("Index");
        }

        [HttpPost]
        public ActionResult SendOverdueReminders()
        {
            var admin = Session[Constant.ADMIN_SESSION] as AdminLogin;
            var adminId = admin != null ? admin.userId : 0;
            var sentCount = 0;
            var skippedCount = 0;
            var today = DateTime.Today;
            var logRepo = new LogRepository();
            var mailService = new GmailNotificationService();

            using (var db = new QuanLySachDBContext())
            {
                var rentals = db.RentalRequests
                    .Where(x => x.ExpectedReturnDate < today
                        && x.Status != "Returned"
                        && x.Status != "Rejected"
                        && x.Status != "Cancelled")
                    .ToList();

                foreach (var rental in rentals)
                {
                    var alreadySentToday = logRepo.GetRentalLogs(1, 1, null, rental.ID, "EmailOverdueReminder", today, today).Total > 0;
                    if (alreadySentToday)
                    {
                        skippedCount++;
                        continue;
                    }

                    var mailResult = mailService.SendRentalNotificationResult(rental.ID, "OverdueReminder", adminId);
                    if (mailResult.Sent)
                    {
                        sentCount++;
                        logRepo.AddRentalLog(new RentalLog
                        {
                            RentalID = rental.ID,
                            UserID = rental.UserID,
                            ActorUserID = adminId > 0 ? (long?)adminId : null,
                            Action = "EmailOverdueReminder",
                            Timestamp = DateTime.UtcNow,
                            Details = "Sent overdue reminder email",
                            OldStatus = rental.Status,
                            NewStatus = rental.Status
                        });
                    }
                    else
                    {
                        skippedCount++;
                        logRepo.AddRentalLog(new RentalLog
                        {
                            RentalID = rental.ID,
                            UserID = rental.UserID,
                            ActorUserID = adminId > 0 ? (long?)adminId : null,
                            Action = "EmailOverdueReminderFailed",
                            Timestamp = DateTime.UtcNow,
                            Details = string.IsNullOrWhiteSpace(mailResult.Message) ? "Khong gui duoc Gmail nhac qua han" : mailResult.Message,
                            OldStatus = rental.Status,
                            NewStatus = rental.Status
                        });
                    }
                }
            }

            TempData["RentalAdminMessage"] = "Đã gửi " + sentCount + " email nhắc quá hạn. Không gửi được hoặc bỏ qua " + skippedCount + " yêu cầu.";
            return RedirectToAction("Index", new { status = "Overdue" });
        }

        private static T GetJsonValue<T>(object data, string propertyName)
        {
            if (data == null) return default(T);
            var property = data.GetType().GetProperty(propertyName);
            if (property == null) return default(T);
            var value = property.GetValue(data, null);
            if (value == null) return default(T);
            return (T)value;
        }

        public class RentalAdminItem
        {
            public int ID { get; set; }
            public long ProductID { get; set; }
            public string ProductName { get; set; }
            public string ProductImage { get; set; }
            public int Stock { get; set; }
            public long UserID { get; set; }
            public string UserName { get; set; }
            public string CustomerName { get; set; }
            public string CustomerPhone { get; set; }
            public int Quantity { get; set; }
            public string Status { get; set; }
            public DateTime RequestedAt { get; set; }
            public DateTime RequestDate { get; set; }
            public int BorrowDays { get; set; }
            public DateTime ExpectedReturnDate { get; set; }
            public DateTime? ApprovedAt { get; set; }
            public DateTime? ReturnedAt { get; set; }
            public DateTime? ActualReturnDate { get; set; }
            public string RejectReason { get; set; }
            public string Details { get; set; }
            public string IdentityNumber { get; set; }
            public string IdentityFullName { get; set; }
            public string IdentityCardImagePath { get; set; }
            public double? IdentityFaceConfidence { get; set; }
            public long? AdminID { get; set; }
        }
    }
}

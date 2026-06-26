using BaiTapLon.Common;
using BaiTapLon.Services;
using Common.Repositories;
using Mood.EF2;
using System;
using System.Configuration;
using System.Data.Entity;
using System.IO;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using Newtonsoft.Json.Linq;

namespace BaiTapLon.Controllers
{
    public class RentalController : Controller
    {
        private readonly LogRepository _logRepo = new LogRepository();
        private readonly FaceRentalTokenService _faceRentalTokenService = new FaceRentalTokenService();
        private readonly GmailNotificationService _gmailNotificationService = new GmailNotificationService();
        private readonly FaceAuthApiClient _faceApiClient = new FaceAuthApiClient();

        [HttpGet]
        public ActionResult MyRentals(string status = null)
        {
            var resolvedUserId = ResolveUserId(0);
            if (resolvedUserId <= 0)
            {
                return Redirect("/");
            }

            using (var db = new QuanLySachDBContext())
            {
                var today = DateTime.Today;
                var rentals = from rental in db.RentalRequests.AsNoTracking()
                              join product in db.Sanphams.AsNoTracking() on rental.ProductID equals product.IDContent
                              where rental.UserID == resolvedUserId
                              select new RentalTrackingItem
                              {
                                  ID = rental.ID,
                                  ProductID = rental.ProductID,
                                  ProductName = product.Name,
                                  ProductImage = product.Images,
                                  Quantity = rental.Quantity,
                                  Status = rental.Status,
                                  RequestDate = rental.RequestDate,
                                  BorrowDays = rental.BorrowDays,
                                  ExpectedReturnDate = rental.ExpectedReturnDate,
                                  ActualReturnDate = rental.ActualReturnDate,
                                  RejectReason = rental.RejectReason,
                                  RequestedAt = rental.RequestedAt
                              };

                ViewBag.PendingCount = rentals.Count(x => x.Status == "Pending");
                ViewBag.BorrowingCount = rentals.Count(x => x.Status == "Borrowing" || x.Status == "Borrowed");
                ViewBag.OverdueCount = rentals.Count(x => x.Status == "Overdue" || (x.Status != "Returned" && x.Status != "Rejected" && x.Status != "Cancelled" && x.ExpectedReturnDate < today));
                ViewBag.ReturnedCount = rentals.Count(x => x.Status == "Returned");

                var query = rentals;
                if (!string.IsNullOrWhiteSpace(status))
                {
                    if (status == "Borrowing")
                    {
                        query = query.Where(x => x.Status == "Borrowing" || x.Status == "Borrowed");
                    }
                    else if (status == "Overdue")
                    {
                        query = query.Where(x => x.Status == "Overdue" || (x.Status != "Returned" && x.Status != "Rejected" && x.Status != "Cancelled" && x.ExpectedReturnDate < today));
                    }
                    else
                    {
                        query = query.Where(x => x.Status == status);
                    }
                }

                ViewBag.Status = status;
                return View(query.OrderByDescending(x => x.RequestedAt).Take(200).ToList());
            }
        }

        [HttpGet]
        public JsonResult ActiveRentalCount()
        {
            var resolvedUserId = ResolveUserId(0);
            if (resolvedUserId <= 0)
            {
                return Json(new { success = false, count = 0 }, JsonRequestBehavior.AllowGet);
            }

            using (var db = new QuanLySachDBContext())
            {
                var count = db.RentalRequests.Count(x =>
                    x.UserID == resolvedUserId
                    && x.Status != "Returned"
                    && x.Status != "Rejected"
                    && x.Status != "Cancelled");

                return Json(new { success = true, count }, JsonRequestBehavior.AllowGet);
            }
        }

        [HttpPost]
        public ActionResult CheckStock(int productId, int quantity = 1)
        {
            try
            {
                if (productId <= 0 || quantity <= 0)
                {
                    return Json(new { success = false, available = false, error = "Invalid product" });
                }

                using (var db = new QuanLySachDBContext())
                {
                    var product = db.Sanphams.AsNoTracking().SingleOrDefault(x => x.IDContent == productId && x.Status);
                    if (product == null)
                    {
                        return Json(new { success = false, available = false, error = "Product not found" });
                    }

                    var stock = GetAvailableStock(product);
                    return Json(new { success = true, available = stock >= quantity, stock });
                }
            }
            catch (Exception ex)
            {
                return Json(new { success = false, available = false, error = ex.Message });
            }
        }

        [HttpPost]
        public ActionResult CheckActiveRental(int productId)
        {
            try
            {
                var resolvedUserId = ResolveUserId(0);
                if (resolvedUserId <= 0)
                {
                    return Json(new { success = false, hasActiveRental = false, error = "User is not authenticated" });
                }

                using (var db = new QuanLySachDBContext())
                {
                    var hasActiveRental = HasActiveRental(db, resolvedUserId, productId);
                    return Json(new { success = true, hasActiveRental });
                }
            }
            catch (Exception ex)
            {
                return Json(new { success = false, hasActiveRental = false, error = ex.Message });
            }
        }

        [HttpGet]
        public ActionResult RentalProfileStatus()
        {
            var resolvedUserId = ResolveUserId(0);
            if (resolvedUserId <= 0)
            {
                return Json(new { success = false, requireLogin = true, error = "User is not authenticated" }, JsonRequestBehavior.AllowGet);
            }

            using (var db = new QuanLySachDBContext())
            {
                var user = db.Users.AsNoTracking().SingleOrDefault(x => x.IDUser == resolvedUserId);
                if (user == null)
                {
                    return Json(new { success = false, error = "User not found" }, JsonRequestBehavior.AllowGet);
                }

                var notificationEmail = string.IsNullOrWhiteSpace(user.NotificationEmail) ? user.Email : user.NotificationEmail;
                var missingNotificationEmail = string.IsNullOrWhiteSpace(notificationEmail);
                var missingIdentity = string.IsNullOrWhiteSpace(user.IdentityNumber) || string.IsNullOrWhiteSpace(user.IdentityFullName);
                var missingIdentityImage = string.IsNullOrWhiteSpace(user.IdentityCardImagePath)
                    && string.IsNullOrWhiteSpace(user.IdentityCardFrontImagePath)
                    && string.IsNullOrWhiteSpace(user.IdentityCardBackImagePath);
                return Json(new
                {
                    success = true,
                    requireUpdate = missingNotificationEmail || missingIdentity,
                    missingNotificationEmail,
                    missingIdentity,
                    missingIdentityImage,
                    notificationEmail,
                    identityNumber = user.IdentityNumber,
                    identityFullName = user.IdentityFullName,
                    identityCardImagePath = user.IdentityCardImagePath,
                    identityCardFrontImagePath = user.IdentityCardFrontImagePath,
                    identityCardBackImagePath = user.IdentityCardBackImagePath
                }, JsonRequestBehavior.AllowGet);
            }
        }

        [HttpPost]
        public ActionResult UpdateRentalProfile(string notificationEmail, string identityNumber, string identityFullName)
        {
            var resolvedUserId = ResolveUserId(0);
            if (resolvedUserId <= 0)
            {
                return Json(new { success = false, error = "User is not authenticated" });
            }

            notificationEmail = (notificationEmail ?? string.Empty).Trim();
            identityNumber = (identityNumber ?? string.Empty).Trim();
            identityFullName = (identityFullName ?? string.Empty).Trim();
            if (string.IsNullOrWhiteSpace(notificationEmail) || string.IsNullOrWhiteSpace(identityNumber) || string.IsNullOrWhiteSpace(identityFullName))
            {
                return Json(new { success = false, error = "Vui lòng nhập Gmail nhận thông báo, số CMND/CCCD và họ tên trên giấy tờ." });
            }

            using (var db = new QuanLySachDBContext())
            {
                var user = db.Users.SingleOrDefault(x => x.IDUser == resolvedUserId);
                if (user == null)
                {
                    return Json(new { success = false, error = "User not found" });
                }

                user.NotificationEmail = notificationEmail;
                user.IdentityNumber = identityNumber;
                user.IdentityFullName = identityFullName;

                var frontFile = Request.Files["identityCardFrontFile"] ?? Request.Files["front_file"] ?? Request.Files["identityCardFile"];
                var backFile = Request.Files["identityCardBackFile"] ?? Request.Files["back_file"];
                if ((frontFile != null && frontFile.ContentLength > 0) || (backFile != null && backFile.ContentLength > 0))
                {
                    var frontValidationError = frontFile != null && frontFile.ContentLength > 0 ? ValidateIdentityFile(frontFile) : null;
                    var backValidationError = backFile != null && backFile.ContentLength > 0 ? ValidateIdentityFile(backFile) : null;
                    if (frontValidationError != null || backValidationError != null)
                    {
                        return Json(new { success = false, error = frontValidationError ?? backValidationError });
                    }

                    string frontFileName = null, frontRelativePath = null, frontSavePath = null;
                    string backFileName = null, backRelativePath = null, backSavePath = null;
                    SaveIdentityFile(frontFile, "front", out frontFileName, out frontRelativePath, out frontSavePath);
                    SaveIdentityFile(backFile, "back", out backFileName, out backRelativePath, out backSavePath);

                    var identityOcr = _faceApiClient.OcrIdentityCardAsync(frontSavePath, frontFileName, backSavePath, backFileName, resolvedUserId, "IdentityCard")
                        .GetAwaiter()
                        .GetResult();
                    if (!ReadBool(identityOcr, "success"))
                    {
                        return Json(new { success = false, error = ReadString(identityOcr, "message", "error_message", "error") ?? "Không thể đọc hoặc xác thực ảnh CMND/CCCD." });
                    }

                    var fields = identityOcr["fields"] as JObject ?? new JObject();
                    user.IdentityNumber = ReadString(fields, "identity_number", "number") ?? user.IdentityNumber;
                    user.IdentityFullName = ReadString(fields, "full_name", "name") ?? user.IdentityFullName;
                    user.IdentityAddress = ReadString(fields, "address", "place_of_residence") ?? user.IdentityAddress;
                    user.IdentityPlaceOfBirth = ReadString(fields, "place_of_birth") ?? user.IdentityPlaceOfBirth;
                    user.IdentityGender = ReadString(fields, "gender") ?? user.IdentityGender;
                    user.IdentityNationality = ReadString(fields, "nationality") ?? user.IdentityNationality;
                    user.IdentityIssuePlace = ReadString(fields, "issue_place") ?? user.IdentityIssuePlace;
                    user.IdentityIssuingAuthority = ReadString(fields, "issuing_authority") ?? user.IdentityIssuingAuthority;
                    user.IdentityDateOfBirth = ParseDate(ReadString(fields, "date_of_birth")) ?? user.IdentityDateOfBirth;
                    user.IdentityIssueDate = ParseDate(ReadString(fields, "issue_date")) ?? user.IdentityIssueDate;
                    user.IdentityExpiryDate = ParseDate(ReadString(fields, "expiry_date")) ?? user.IdentityExpiryDate;
                    user.IdentityCardImagePath = frontRelativePath ?? backRelativePath ?? user.IdentityCardImagePath;
                    user.IdentityCardFrontImagePath = frontRelativePath ?? user.IdentityCardFrontImagePath;
                    user.IdentityCardBackImagePath = backRelativePath ?? user.IdentityCardBackImagePath;
                    var faceMatched = ReadBool(identityOcr, "face_matched");
                    if (faceMatched)
                    {
                        user.IdentityFaceConfidence = ReadDouble(identityOcr, "face_confidence");
                        user.IdentityVerifiedAt = DateTime.UtcNow;
                    }
                }

                db.Entry(user).State = EntityState.Modified;
                db.SaveChanges();
                return Json(new
                {
                    success = true,
                    identityCardImagePath = user.IdentityCardImagePath,
                    identityCardFrontImagePath = user.IdentityCardFrontImagePath,
                    identityCardBackImagePath = user.IdentityCardBackImagePath,
                    identityNumber = user.IdentityNumber,
                    identityFullName = user.IdentityFullName
                });
            }
        }

        [HttpPost]
        public ActionResult RequestRental(int productId = 0, int rentalId = 0, long userId = 0, string details = null, int quantity = 1, int borrowDays = 1, DateTime? requestDate = null, string faceToken = null, string identityNumber = null, string identityFullName = null)
        {
            try
            {
                var resolvedUserId = ResolveUserId(userId);
                if (resolvedUserId <= 0)
                {
                    return Json(new { success = false, error = "User is not authenticated" });
                }

                var resolvedProductId = productId > 0 ? productId : rentalId;
                if (resolvedProductId <= 0 || quantity <= 0)
                {
                    return Json(new { success = false, error = "Invalid rental request" });
                }

                var maxBorrowDays = GetMaxBorrowDays();
                if (borrowDays <= 0 || borrowDays > maxBorrowDays)
                {
                    return Json(new { success = false, error = "Borrow days must be between 1 and " + maxBorrowDays });
                }

                if (!_faceRentalTokenService.ValidateAndConsume(faceToken, resolvedUserId, resolvedProductId))
                {
                    return Json(new { success = false, error = "Face verification is required before borrowing" });
                }

                using (var db = new QuanLySachDBContext())
                {
                    var user = db.Users.SingleOrDefault(x => x.IDUser == resolvedUserId);
                    if (user == null)
                    {
                        return Json(new { success = false, error = "User not found" });
                    }

                    var notificationEmail = string.IsNullOrWhiteSpace(user.NotificationEmail) ? user.Email : user.NotificationEmail;
                    if (string.IsNullOrWhiteSpace(notificationEmail)
                        || string.IsNullOrWhiteSpace(user.IdentityNumber)
                        || string.IsNullOrWhiteSpace(user.IdentityFullName))
                    {
                        return Json(new { success = false, requireProfileUpdate = true, error = "Vui lòng cập nhật Gmail nhận thông báo, số CMND/CCCD và họ tên trước khi mượn sách." });
                    }

                    if (HasActiveRental(db, resolvedUserId, resolvedProductId))
                    {
                        return Json(new { success = false, error = "Bạn đang mượn hoặc đang chờ duyệt cuốn sách này." });
                    }

                    var product = db.Sanphams.SingleOrDefault(x => x.IDContent == resolvedProductId && x.Status);
                    if (product == null)
                    {
                        return Json(new { success = false, error = "Product not found" });
                    }

                    if (GetAvailableStock(product) < quantity)
                    {
                        return Json(new { success = false, error = "Product is out of stock" });
                    }

                    var serverRequestDate = (requestDate.HasValue ? requestDate.Value : DateTime.UtcNow).Date;
                    var rental = new RentalRequest
                    {
                        ProductID = product.IDContent,
                        UserID = resolvedUserId,
                        Quantity = quantity,
                        Status = "Pending",
                        RequestedAt = DateTime.UtcNow,
                        RequestDate = serverRequestDate,
                        BorrowDays = borrowDays,
                        ExpectedReturnDate = serverRequestDate.AddDays(borrowDays),
                        Details = details,
                        IdentityNumber = user.IdentityNumber,
                        IdentityFullName = user.IdentityFullName,
                        IdentityCardImagePath = user.IdentityCardImagePath,
                        IdentityCardFrontImagePath = user.IdentityCardFrontImagePath,
                        IdentityCardBackImagePath = user.IdentityCardBackImagePath,
                        IdentityAddress = user.IdentityAddress,
                        IdentityPlaceOfBirth = user.IdentityPlaceOfBirth,
                        IdentityDateOfBirth = user.IdentityDateOfBirth,
                        IdentityIssueDate = user.IdentityIssueDate,
                        IdentityExpiryDate = user.IdentityExpiryDate,
                        IdentityGender = user.IdentityGender,
                        IdentityNationality = user.IdentityNationality,
                        IdentityIssuePlace = user.IdentityIssuePlace,
                        IdentityIssuingAuthority = user.IdentityIssuingAuthority,
                        IdentityFaceConfidence = user.IdentityFaceConfidence
                    };
                    db.RentalRequests.Add(rental);
                    db.SaveChanges();

                    AddRentalLog(rental.ID, resolvedUserId, resolvedUserId, "Request", details, null, "Pending");
                    _gmailNotificationService.SendRentalNotification(rental.ID, "Request", resolvedUserId);
                    var activeRentalCount = db.RentalRequests.Count(x =>
                        x.UserID == resolvedUserId
                        && x.Status != "Returned"
                        && x.Status != "Rejected"
                        && x.Status != "Cancelled");
                    return Json(new { success = true, rentalId = rental.ID, status = rental.Status, expectedReturnDate = rental.ExpectedReturnDate.ToString("yyyy-MM-dd"), activeRentalCount });
                }
            }
            catch (Exception ex)
            {
                return Json(new { success = false, error = ex.Message });
            }
        }

        [HttpPost]
        public ActionResult CancelRental(int id)
        {
            var resolvedUserId = ResolveUserId(0);
            if (resolvedUserId <= 0)
            {
                return Redirect("/");
            }

            using (var db = new QuanLySachDBContext())
            {
                var rental = db.RentalRequests.SingleOrDefault(x => x.ID == id && x.UserID == resolvedUserId);
                if (rental == null)
                {
                    TempData["RentalError"] = "Không tìm thấy yêu cầu mượn sách.";
                    return RedirectToAction("MyRentals");
                }

                if (rental.Status != "Pending")
                {
                    TempData["RentalError"] = "Chỉ có thể hủy yêu cầu đang chờ xác nhận.";
                    return RedirectToAction("MyRentals");
                }

                var oldStatus = rental.Status;
                rental.Status = "Cancelled";
                db.Entry(rental).State = EntityState.Modified;
                db.SaveChanges();

                AddRentalLog(rental.ID, rental.UserID, resolvedUserId, "Cancel", "User cancelled pending rental request", oldStatus, rental.Status);
                _gmailNotificationService.SendRentalNotification(rental.ID, "Cancel", resolvedUserId);
                TempData["RentalMessage"] = "Đã hủy yêu cầu mượn sách.";
                return RedirectToAction("MyRentals");
            }
        }

        [HttpPost]
        public ActionResult UpdateRentalStatus(int rentalId, string status, long adminId = 0)
        {
            try
            {
                var resolvedAdminId = ResolveUserId(adminId);
                if (resolvedAdminId <= 0)
                {
                    return Json(new { success = false, error = "Admin is not authenticated" });
                }

                if (!IsValidStatus(status))
                {
                    return Json(new { success = false, error = "Invalid status" });
                }

                using (var db = new QuanLySachDBContext())
                using (var tx = db.Database.BeginTransaction())
                {
                    var rental = db.RentalRequests.SingleOrDefault(x => x.ID == rentalId);
                    if (rental == null)
                    {
                        return Json(new { success = false, error = "Rental request not found" });
                    }

                    var oldStatus = rental.Status;
                    var product = db.Sanphams.SingleOrDefault(x => x.IDContent == rental.ProductID);
                    if (product == null)
                    {
                        return Json(new { success = false, error = "Product not found" });
                    }

                    var now = DateTime.UtcNow;
                    if (status == "Approve" || status == "Borrow")
                    {
                        if (rental.Status != "Pending")
                        {
                            return Json(new { success = false, error = "Only pending requests can be approved" });
                        }

                        if (GetAvailableStock(product) < rental.Quantity)
                        {
                            return Json(new { success = false, error = "Product is out of stock" });
                        }

                        DecreaseStock(product, rental.Quantity);
                        rental.Status = "Borrowing";
                        rental.ApprovedAt = now;
                    }
                    else if (status == "Return")
                    {
                        if (rental.Status != "Borrowed" && rental.Status != "Borrowing" && rental.Status != "Overdue")
                        {
                            return Json(new { success = false, error = "Only borrowed requests can be returned" });
                        }

                        IncreaseStock(product, rental.Quantity);
                        rental.Status = "Returned";
                        rental.ReturnedAt = now;
                        rental.ActualReturnDate = now;
                    }
                    else if (status == "Reject" || status == "Cancel")
                    {
                        if (rental.Status != "Pending")
                        {
                            return Json(new { success = false, error = "Only pending requests can be rejected or cancelled" });
                        }

                        rental.Status = status == "Reject" ? "Rejected" : "Cancelled";
                    }
                    else if (status == "Overdue")
                    {
                        if (rental.Status != "Borrowed" && rental.Status != "Borrowing")
                        {
                            return Json(new { success = false, error = "Only borrowed requests can become overdue" });
                        }

                        rental.Status = "Overdue";
                    }

                    rental.AdminID = resolvedAdminId;
                    db.Entry(product).State = EntityState.Modified;
                    db.Entry(rental).State = EntityState.Modified;
                    db.SaveChanges();
                    tx.Commit();

                    AddRentalLog(rental.ID, rental.UserID, resolvedAdminId, status, "Status updated to " + rental.Status, oldStatus, rental.Status);
                    var mailEvent = (status == "Approve" || status == "Borrow") ? "ApproveSuccess" : status;
                    var mailResult = _gmailNotificationService.SendRentalNotificationResult(rental.ID, mailEvent, resolvedAdminId);
                    return Json(new
                    {
                        success = true,
                        status = rental.Status,
                        mailSent = mailResult.Sent,
                        mailMessage = mailResult.Message,
                        mailRecipient = mailResult.RecipientEmail
                    });
                }
            }
            catch (Exception ex)
            {
                return Json(new { success = false, error = ex.Message });
            }
        }

        private void AddRentalLog(int rentalId, long userId, long actorUserId, string action, string details, string oldStatus, string newStatus)
        {
            _logRepo.AddRentalLog(new RentalLog
            {
                RentalID = rentalId,
                UserID = userId,
                ActorUserID = actorUserId,
                Action = action,
                Timestamp = DateTime.UtcNow,
                Details = details,
                OldStatus = oldStatus,
                NewStatus = newStatus
            });
        }

        private long ResolveUserId(long requestUserId)
        {
            var userSession = Session[Constant.USER_SESSION] as UserLogin;
            if (userSession != null && userSession.userId > 0)
            {
                return userSession.userId;
            }

            long authenticatedUserId;
            if (User != null && User.Identity != null && User.Identity.IsAuthenticated && long.TryParse(User.Identity.Name, out authenticatedUserId))
            {
                return authenticatedUserId;
            }

            return requestUserId;
        }

        private static bool IsValidStatus(string status)
        {
            if (string.IsNullOrWhiteSpace(status)) return false;
            return status == "Approve"
                || status == "Reject"
                || status == "Borrow"
                || status == "Return"
                || status == "Overdue"
                || status == "Cancel";
        }

        private static int GetMaxBorrowDays()
        {
            int value;
            return int.TryParse(ConfigurationManager.AppSettings["RentalMaxBorrowDays"], out value) && value > 0 ? value : 30;
        }

        private static string ValidateIdentityFile(HttpPostedFileBase file)
        {
            if (file == null) return "Vui lòng đính kèm ảnh CMND/CCCD khi mượn sách.";
            if (file.ContentLength <= 0) return "Ảnh CMND/CCCD đang rỗng.";
            if (file.ContentLength > GetMaxUploadBytes()) return "Ảnh CMND/CCCD quá lớn.";

            var extension = (Path.GetExtension(file.FileName) ?? string.Empty).ToLowerInvariant();
            if (extension != ".jpg" && extension != ".jpeg" && extension != ".png")
            {
                return "Chỉ hỗ trợ ảnh CMND/CCCD định dạng jpg, jpeg, png.";
            }

            return null;
        }

        private static int GetMaxUploadBytes()
        {
            int value;
            return int.TryParse(ConfigurationManager.AppSettings["FaceAuthMaxUploadBytes"], out value) && value > 0 ? value : 5242880;
        }

        private static string GetIdentityStoragePath()
        {
            var path = ConfigurationManager.AppSettings["IdentityCardStoragePath"];
            return string.IsNullOrWhiteSpace(path) ? "DataImage/IdentityCards" : path.Trim().Trim('/').Replace("\\", "/");
        }

        private static bool ReadBool(JObject json, params string[] names)
        {
            if (json == null) return false;
            foreach (var name in names)
            {
                var token = json[name];
                if (token != null && token.Type != JTokenType.Null)
                {
                    bool value;
                    if (bool.TryParse(token.ToString(), out value)) return value;
                }
            }

            return false;
        }

        private static string ReadString(JObject json, params string[] names)
        {
            if (json == null) return null;
            foreach (var name in names)
            {
                var token = json[name];
                if (token != null && token.Type != JTokenType.Null)
                {
                    return token.Value<string>();
                }
            }

            return null;
        }

        private static double ReadDouble(JObject json, params string[] names)
        {
            if (json == null) return 0.0;
            foreach (var name in names)
            {
                var token = json[name];
                if (token != null && token.Type != JTokenType.Null)
                {
                    double value;
                    if (double.TryParse(token.ToString(), out value)) return value;
                }
            }

            return 0.0;
        }

        private static DateTime? ParseDate(string value)
        {
            if (string.IsNullOrWhiteSpace(value)) return null;
            DateTime parsed;
            if (DateTime.TryParse(value, out parsed)) return parsed.Date;
            return null;
        }

        private void SaveIdentityFile(HttpPostedFileBase file, string side, out string fileName, out string relativePath, out string savePath)
        {
            fileName = null;
            relativePath = null;
            savePath = null;
            if (file == null || file.ContentLength <= 0) return;

            fileName = Guid.NewGuid() + Path.GetExtension(file.FileName);
            relativePath = GetIdentityStoragePath() + "/" + side + "/" + fileName;
            savePath = Server.MapPath("~/" + relativePath);
            Directory.CreateDirectory(Path.GetDirectoryName(savePath));
            file.SaveAs(savePath);
        }

        private static int GetAvailableStock(Sanpham product)
        {
            return product.TonKho.HasValue ? product.TonKho.Value : product.Soluong;
        }

        private static bool HasActiveRental(QuanLySachDBContext db, long userId, long productId)
        {
            return db.RentalRequests.Any(x =>
                x.UserID == userId
                && x.ProductID == productId
                && (x.Status == "Pending"
                    || x.Status == "Approved"
                    || x.Status == "Borrowed"
                    || x.Status == "Borrowing"
                    || x.Status == "Overdue"));
        }

        private static void DecreaseStock(Sanpham product, int quantity)
        {
            product.Soluong -= quantity;
            if (product.TonKho.HasValue)
            {
                product.TonKho -= quantity;
            }
        }

        private static void IncreaseStock(Sanpham product, int quantity)
        {
            product.Soluong += quantity;
            if (product.TonKho.HasValue)
            {
                product.TonKho += quantity;
            }
        }

        public class RentalTrackingItem
        {
            public int ID { get; set; }
            public long ProductID { get; set; }
            public string ProductName { get; set; }
            public string ProductImage { get; set; }
            public int Quantity { get; set; }
            public string Status { get; set; }
            public DateTime RequestDate { get; set; }
            public int BorrowDays { get; set; }
            public DateTime ExpectedReturnDate { get; set; }
            public DateTime? ActualReturnDate { get; set; }
            public string RejectReason { get; set; }
            public DateTime RequestedAt { get; set; }
        }
    }
}


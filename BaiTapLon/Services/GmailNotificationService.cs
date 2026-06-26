using Common.Repositories;
using CommomSentMail;
using Mood.EF2;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Configuration;
using System.Data.Entity;
using System.Linq;
using System.Net.Http;
using System.Net.Mail;
using System.Text;

namespace BaiTapLon.Services
{
    public class GmailNotificationService
    {
        private readonly LogRepository _logRepo = new LogRepository();

        public bool SendRentalNotification(int rentalId, string eventCode, long actorUserId = 0)
        {
            return SendRentalNotificationResult(rentalId, eventCode, actorUserId).Sent;
        }

        public GmailNotificationResult SendRentalNotificationResult(int rentalId, string eventCode, long actorUserId = 0)
        {
            try
            {
                using (var db = new QuanLySachDBContext())
                {
                    var item = (from rental in db.RentalRequests.AsNoTracking()
                                join user in db.Users.AsNoTracking() on rental.UserID equals user.IDUser
                                join product in db.Sanphams.AsNoTracking() on rental.ProductID equals product.IDContent
                                where rental.ID == rentalId
                                select new RentalMailItem
                                {
                                    RentalId = rental.ID,
                                    UserId = rental.UserID,
                                    UserEmail = string.IsNullOrEmpty(user.NotificationEmail) ? user.Email : user.NotificationEmail,
                                    CustomerName = user.Name,
                                    ProductName = product.Name,
                                    Status = rental.Status,
                                    RequestDate = rental.RequestDate,
                                    ExpectedReturnDate = rental.ExpectedReturnDate,
                                    ActualReturnDate = rental.ActualReturnDate
                                }).FirstOrDefault();

                    if (item == null || string.IsNullOrWhiteSpace(item.UserEmail))
                    {
                        return LogAndReturn(rentalId, item, actorUserId, eventCode, false, "EmailNotificationSkipped", "Khong tim thay Gmail khach hang.");
                    }

                    if (!IsEnabled())
                    {
                        return LogAndReturn(rentalId, item, actorUserId, eventCode, false, "EmailNotificationSkipped", "GmailNotificationsEnabled=false");
                    }

                    if (!IsValidEmail(item.UserEmail))
                    {
                        return LogAndReturn(rentalId, item, actorUserId, eventCode, false, "EmailNotificationFailed", "Gmail khach hang khong hop le: " + item.UserEmail);
                    }

                    var subject = BuildSubject(item, eventCode);
                    var body = BuildBody(item, eventCode);
                    var emailResult = SendEmail(item.UserEmail, subject, body);
                    return LogAndReturn(
                        rentalId,
                        item,
                        actorUserId,
                        eventCode,
                        emailResult.Sent,
                        emailResult.Sent ? "EmailNotificationSent" : "EmailNotificationFailed",
                        emailResult.Sent ? "Da gui Gmail den " + item.UserEmail : "Khong gui duoc Gmail den " + item.UserEmail + ". " + emailResult.Message);
                }
            }
            catch (Exception ex)
            {
                _logRepo.AddRentalLog(new RentalLog
                {
                    RentalID = rentalId,
                    UserID = 0,
                    ActorUserID = actorUserId > 0 ? (long?)actorUserId : null,
                    Action = "EmailNotificationFailed",
                    Timestamp = DateTime.UtcNow,
                    Details = eventCode + " | " + ex.Message
                });
                return new GmailNotificationResult
                {
                    Sent = false,
                    Message = "Khong gui duoc Gmail: " + ex.Message
                };
            }
        }

        private GmailNotificationResult LogAndReturn(int rentalId, RentalMailItem item, long actorUserId, string eventCode, bool sent, string action, string details)
        {
            _logRepo.AddRentalLog(new RentalLog
            {
                RentalID = rentalId,
                UserID = item != null ? item.UserId : 0,
                ActorUserID = actorUserId > 0 ? (long?)actorUserId : null,
                Action = action,
                Timestamp = DateTime.UtcNow,
                Details = eventCode + " | " + details,
                OldStatus = item != null ? item.Status : null,
                NewStatus = item != null ? item.Status : null
            });

            return new GmailNotificationResult
            {
                Sent = sent,
                RecipientEmail = item != null ? item.UserEmail : null,
                Message = details
            };
        }

        private EmailSendResult SendEmail(string toEmail, string subject, string htmlBody)
        {
            var accessToken = GetAccessToken();
            if (string.IsNullOrWhiteSpace(accessToken))
            {
                return SendEmailBySmtp(toEmail, subject, htmlBody);
            }

            var sender = GetSetting("GmailSenderEmail");
            var displayName = GetSetting("GmailSenderName");
            if (string.IsNullOrWhiteSpace(sender))
            {
                sender = GetSetting("FromEmailAddress");
            }
            if (string.IsNullOrWhiteSpace(displayName))
            {
                displayName = "QLNhaSach";
            }

            var mime = BuildMime(sender, displayName, toEmail, subject, htmlBody);
            var payload = new JObject
            {
                ["raw"] = Base64UrlEncode(mime)
            };

            using (var client = new HttpClient())
            {
                client.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", accessToken);
                var response = client.PostAsync(
                    "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
                    new StringContent(payload.ToString(), Encoding.UTF8, "application/json"))
                    .GetAwaiter()
                    .GetResult();

                if (response.IsSuccessStatusCode)
                {
                    return new EmailSendResult { Sent = true, Message = "Da gui bang Gmail API." };
                }

                var responseBody = response.Content.ReadAsStringAsync().GetAwaiter().GetResult();
                return new EmailSendResult
                {
                    Sent = false,
                    Message = "Gmail API loi " + (int)response.StatusCode + " " + response.ReasonPhrase + ": " + responseBody
                };
            }
        }

        private EmailSendResult SendEmailBySmtp(string toEmail, string subject, string htmlBody)
        {
            try
            {
                new MailHelper().sentMail(toEmail, subject, htmlBody);
                return new EmailSendResult { Sent = true, Message = "Da gui bang SMTP." };
            }
            catch (Exception ex)
            {
                return new EmailSendResult
                {
                    Sent = false,
                    Message = "SMTP loi: " + BuildExceptionMessage(ex)
                };
            }
        }

        private static string BuildExceptionMessage(Exception ex)
        {
            if (ex == null)
            {
                return "";
            }

            var message = ex.Message;
            if (ex.InnerException != null && !string.IsNullOrWhiteSpace(ex.InnerException.Message))
            {
                message += " | Inner: " + ex.InnerException.Message;
            }

            return message;
        }

        private string GetAccessToken()
        {
            var refreshToken = GetSetting("GmailRefreshToken");
            var clientId = GetSetting("GmailClientId");
            var clientSecret = GetSetting("GmailClientSecret");
            if (string.IsNullOrWhiteSpace(refreshToken) || string.IsNullOrWhiteSpace(clientId) || string.IsNullOrWhiteSpace(clientSecret))
            {
                return null;
            }

            using (var client = new HttpClient())
            {
                var response = client.PostAsync("https://oauth2.googleapis.com/token", new FormUrlEncodedContent(new[]
                {
                    new KeyValuePair<string, string>("client_id", clientId),
                    new KeyValuePair<string, string>("client_secret", clientSecret),
                    new KeyValuePair<string, string>("refresh_token", refreshToken),
                    new KeyValuePair<string, string>("grant_type", "refresh_token")
                })).GetAwaiter().GetResult();

                if (!response.IsSuccessStatusCode)
                {
                    return null;
                }

                var json = JObject.Parse(response.Content.ReadAsStringAsync().GetAwaiter().GetResult());
                return (string)json["access_token"];
            }
        }

        private static string BuildMime(string sender, string displayName, string toEmail, string subject, string htmlBody)
        {
            var encodedSubject = Convert.ToBase64String(Encoding.UTF8.GetBytes(subject));
            return "From: " + displayName + " <" + sender + ">\r\n"
                + "To: " + toEmail + "\r\n"
                + "Subject: =?UTF-8?B?" + encodedSubject + "?=\r\n"
                + "MIME-Version: 1.0\r\n"
                + "Content-Type: text/html; charset=UTF-8\r\n\r\n"
                + htmlBody;
        }

        private static string Base64UrlEncode(string value)
        {
            return Convert.ToBase64String(Encoding.UTF8.GetBytes(value))
                .TrimEnd('=')
                .Replace('+', '-')
                .Replace('/', '_');
        }

        private static string BuildSubject(RentalMailItem item, string eventCode)
        {
            switch (eventCode)
            {
                case "Request": return "Đã nhận yêu cầu mượn sách #" + item.RentalId;
                case "ApproveSuccess": return "Mượn sách thành công";
                case "Approve":
                case "Borrow": return "Yêu cầu mượn sách đã được duyệt";
                case "Reject": return "Yêu cầu mượn sách bị từ chối";
                case "Cancel": return "Yêu cầu mượn sách đã được hủy";
                case "Return": return "Đã xác nhận trả sách";
                case "Overdue": return "Sách mượn đã quá hạn trả";
                case "OverdueReminder": return "Nhắc trả sách quá hạn";
                default: return "Cập nhật trạng thái mượn sách";
            }
        }

        private static string BuildBody(RentalMailItem item, string eventCode)
        {
            var message = GetMessage(eventCode);
            return "<p>Xin chào " + Encode(item.CustomerName) + ",</p>"
                + "<p>" + message + "</p>"
                + "<p><strong>Sách:</strong> " + Encode(item.ProductName) + "<br/>"
                + "<strong>Mã mượn:</strong> #" + item.RentalId + "<br/>"
                + "<strong>Trạng thái:</strong> " + Encode(item.Status) + "<br/>"
                + "<strong>Ngày yêu cầu:</strong> " + item.RequestDate.ToString("dd/MM/yyyy") + "<br/>"
                + "<strong>Hạn trả:</strong> " + item.ExpectedReturnDate.ToString("dd/MM/yyyy") + "</p>"
                + "<p>Vui lòng đăng nhập tài khoản để theo dõi chi tiết.</p>";
        }

        private static string GetMessage(string eventCode)
        {
            switch (eventCode)
            {
                case "Request": return "Hệ thống đã nhận yêu cầu mượn sách của bạn.";
                case "ApproveSuccess": return "Admin đã duyệt yêu cầu. Bạn đã mượn sách thành công, vui lòng trả sách đúng hạn.";
                case "Approve":
                case "Borrow": return "Yêu cầu mượn sách của bạn đã được admin duyệt.";
                case "Reject": return "Yêu cầu mượn sách của bạn đã bị từ chối.";
                case "Cancel": return "Yêu cầu mượn sách của bạn đã được hủy.";
                case "Return": return "Hệ thống đã xác nhận bạn đã trả sách.";
                case "Overdue": return "Sách mượn của bạn đã được đánh dấu quá hạn.";
                case "OverdueReminder": return "Sách mượn của bạn đang quá hạn. Vui lòng sắp xếp trả sách sớm.";
                default: return "Trạng thái mượn sách của bạn vừa được cập nhật.";
            }
        }

        private static string Encode(string value)
        {
            return System.Web.HttpUtility.HtmlEncode(value ?? "");
        }

        private static bool IsValidEmail(string email)
        {
            if (string.IsNullOrWhiteSpace(email)) return false;
            try
            {
                var address = new MailAddress(email);
                return string.Equals(address.Address, email.Trim(), StringComparison.OrdinalIgnoreCase);
            }
            catch
            {
                return false;
            }
        }

        private static bool IsEnabled()
        {
            bool enabled;
            return bool.TryParse(GetSetting("GmailNotificationsEnabled"), out enabled) && enabled;
        }

        private static string GetSetting(string key)
        {
            return ConfigurationManager.AppSettings[key];
        }

        private class RentalMailItem
        {
            public int RentalId { get; set; }
            public long UserId { get; set; }
            public string UserEmail { get; set; }
            public string CustomerName { get; set; }
            public string ProductName { get; set; }
            public string Status { get; set; }
            public DateTime RequestDate { get; set; }
            public DateTime ExpectedReturnDate { get; set; }
            public DateTime? ActualReturnDate { get; set; }
        }

        private class EmailSendResult
        {
            public bool Sent { get; set; }
            public string Message { get; set; }
        }
    }

    public class GmailNotificationResult
    {
        public bool Sent { get; set; }
        public string RecipientEmail { get; set; }
        public string Message { get; set; }
    }
}

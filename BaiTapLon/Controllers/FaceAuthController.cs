using Common.Repositories;
using BaiTapLon.Common;
using BaiTapLon.Services;
using Mood.Draw;
using Mood.EF2;
using System;
using System.Configuration;
using System.Globalization;
using System.IO;
using System.Net;
using System.Threading.Tasks;
using System.Web;
using System.Web.Mvc;
using Newtonsoft.Json.Linq;

namespace BaiTapLon.Controllers
{
    public class FaceAuthController : Controller
    {
        private readonly LogRepository _logRepo = new LogRepository();
        private readonly FaceAuthApiClient _faceApiClient = new FaceAuthApiClient();
        private readonly FaceRentalTokenService _faceRentalTokenService = new FaceRentalTokenService();

        [AllowAnonymous]
        [HttpPost]
        public async Task<ActionResult> OcrCmndDraft()
        {
            try
            {
                var upload = SaveIdentityUploadPair("Drafts");
                if (!string.IsNullOrWhiteSpace(upload.Error)) return Json(new { success = false, message = upload.Error });

                var apiResponse = await _faceApiClient.OcrIdentityCardAsync(upload.FrontSavePath, upload.FrontFileName, upload.BackSavePath, upload.BackFileName, 0, "IdentityCardDraft");
                var fields = apiResponse["fields"] as JObject ?? new JObject();
                return Json(new
                {
                    success = ReadBool(apiResponse, "success"),
                    imagePath = upload.FrontRelativePath ?? upload.BackRelativePath,
                    frontImagePath = upload.FrontRelativePath,
                    backImagePath = upload.BackRelativePath,
                    fields = new
                    {
                        identityNumber = ReadString(fields, "identity_number", "number"),
                        fullName = ReadString(fields, "full_name", "name"),
                        dateOfBirth = ReadString(fields, "date_of_birth"),
                        address = ReadString(fields, "address", "place_of_residence"),
                        placeOfBirth = ReadString(fields, "place_of_birth"),
                        gender = ReadString(fields, "gender"),
                        nationality = ReadString(fields, "nationality"),
                        issueDate = ReadString(fields, "issue_date"),
                        issuePlace = ReadString(fields, "issue_place"),
                        expiryDate = ReadString(fields, "expiry_date"),
                        issuingAuthority = ReadString(fields, "issuing_authority"),
                        mrz = ReadString(fields, "mrz")
                    },
                    message = ReadString(apiResponse, "message", "error_message") ?? "Đã đọc thông tin CMND/CCCD."
                });
            }
            catch (Exception ex)
            {
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpPost]
        public async Task<ActionResult> OcrCmnd()
        {
            try
            {
                var userSession = Session[Constant.USER_SESSION] as UserLogin;
                if (userSession == null || userSession.userId <= 0)
                {
                    return Json(new { success = false, message = "Vui lòng đăng nhập trước khi cập nhật CMND/CCCD." });
                }

                var upload = SaveIdentityUploadPair(null);
                if (!string.IsNullOrWhiteSpace(upload.Error)) return Json(new { success = false, message = upload.Error });

                var apiResponse = await _faceApiClient.OcrIdentityCardAsync(upload.FrontSavePath, upload.FrontFileName, upload.BackSavePath, upload.BackFileName, userSession.userId, "IdentityCard");
                var success = ReadBool(apiResponse, "success");
                var fields = apiResponse["fields"] as JObject ?? new JObject();

                var userDraw = new UserDraw();
                var user = userDraw.getIDByUser(userSession.userId);
                if (success && user != null)
                {
                    var identityFullName = ReadString(fields, "full_name", "name");
                    user.IdentityNumber = ReadString(fields, "identity_number", "number") ?? user.IdentityNumber;
                    user.IdentityFullName = identityFullName ?? user.IdentityFullName;
                    if (!string.IsNullOrWhiteSpace(identityFullName))
                    {
                        user.Name = identityFullName.Trim();
                    }
                    user.IdentityAddress = ReadString(fields, "address", "place_of_residence") ?? user.IdentityAddress;
                    user.IdentityPlaceOfBirth = ReadString(fields, "place_of_birth") ?? user.IdentityPlaceOfBirth;
                    user.IdentityGender = ReadString(fields, "gender") ?? user.IdentityGender;
                    user.IdentityNationality = ReadString(fields, "nationality") ?? user.IdentityNationality;
                    user.IdentityIssuePlace = ReadString(fields, "issue_place") ?? user.IdentityIssuePlace;
                    user.IdentityDateOfBirth = ParseDate(ReadString(fields, "date_of_birth")) ?? user.IdentityDateOfBirth;
                    user.IdentityIssueDate = ParseDate(ReadString(fields, "issue_date")) ?? user.IdentityIssueDate;
                    user.IdentityExpiryDate = ParseDate(ReadString(fields, "expiry_date")) ?? user.IdentityExpiryDate;
                    user.IdentityIssuingAuthority = ReadString(fields, "issuing_authority") ?? user.IdentityIssuingAuthority;
                    user.IdentityCardImagePath = upload.FrontRelativePath ?? upload.BackRelativePath;
                    user.IdentityCardFrontImagePath = upload.FrontRelativePath ?? user.IdentityCardFrontImagePath;
                    user.IdentityCardBackImagePath = upload.BackRelativePath ?? user.IdentityCardBackImagePath;
                    user.IdentityFaceConfidence = ReadDouble(apiResponse, "face_confidence");
                    user.IdentityVerifiedAt = DateTime.UtcNow;
                    userDraw.UpdateUser(user);
                }

                return Json(new
                {
                    success,
                    imagePath = upload.FrontRelativePath ?? upload.BackRelativePath,
                    frontImagePath = upload.FrontRelativePath,
                    backImagePath = upload.BackRelativePath,
                    fields = new
                    {
                        identityNumber = ReadString(fields, "identity_number", "number"),
                        fullName = ReadString(fields, "full_name", "name"),
                        dateOfBirth = ReadString(fields, "date_of_birth"),
                        address = ReadString(fields, "address", "place_of_residence"),
                        placeOfBirth = ReadString(fields, "place_of_birth"),
                        gender = ReadString(fields, "gender"),
                        nationality = ReadString(fields, "nationality"),
                        issueDate = ReadString(fields, "issue_date"),
                        issuePlace = ReadString(fields, "issue_place"),
                        expiryDate = ReadString(fields, "expiry_date"),
                        issuingAuthority = ReadString(fields, "issuing_authority"),
                        mrz = ReadString(fields, "mrz")
                    },
                    faceMatched = ReadBool(apiResponse, "face_matched"),
                    faceConfidence = ReadDouble(apiResponse, "face_confidence"),
                    message = ReadString(apiResponse, "message", "error_message") ?? (success ? "Đã đọc thông tin CMND/CCCD." : "Không thể đọc CMND/CCCD.")
                });
            }
            catch (Exception ex)
            {
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpPost]
        public async Task<ActionResult> VerifyRentalFace(long productId, string challengeToken = null)
        {
            try
            {
                var userSession = Session[Constant.USER_SESSION] as UserLogin;
                if (userSession == null || userSession.userId <= 0)
                {
                    return Json(new { success = false, message = "Vui lòng đăng nhập trước khi mượn sách." });
                }

                if (productId <= 0)
                {
                    return Json(new { success = false, message = "Sách không hợp lệ." });
                }

                var file = Request.Files.Count > 0 ? Request.Files[0] : null;
                var validationError = ValidateFaceFile(file);
                if (validationError != null) return Json(new { success = false, message = validationError });
                var challengeError = ValidateFaceChallenge("Rental", challengeToken);
                if (challengeError != null) return Json(new { success = false, message = challengeError });

                var filename = Guid.NewGuid() + Path.GetExtension(file.FileName);
                var relativePath = GetFaceStoragePath() + "/" + filename;
                var savePath = Server.MapPath("~/" + relativePath);
                Directory.CreateDirectory(Path.GetDirectoryName(savePath));
                file.SaveAs(savePath);

                var apiResponse = await _faceApiClient.VerifyAsync(savePath, filename, userSession.userId, "Rental");
                var verified = IsFaceAccepted(apiResponse);
                var confidence = apiResponse.Confidence;
                var requestId = GetRequestId(apiResponse);

                _logRepo.AddFaceAuthLog(new FaceAuthLog
                {
                    UserID = userSession.userId,
                    Action = verified ? "RentalFaceVerifySuccess" : "RentalFaceVerifyFailed",
                    Timestamp = DateTime.UtcNow,
                    IP = Request.UserHostAddress,
                    DeviceInfo = Request.UserAgent,
                    ImagePath = relativePath,
                    Result = verified,
                    Confidence = confidence,
                    RequestId = requestId,
                    Purpose = "Rental",
                    ErrorCode = apiResponse.ErrorCode,
                    ErrorMessage = apiResponse.ErrorMessage ?? apiResponse.Error,
                    LivenessPassed = apiResponse.LivenessPassed
                });

                if (!verified)
                {
                    return Json(new { success = false, confidence, message = "Xác nhận khuôn mặt thất bại. Vui lòng thử lại." });
                }

                var token = _faceRentalTokenService.Create(userSession.userId, productId, requestId);
                return Json(new { success = true, confidence, faceToken = token });
            }
            catch (Exception ex)
            {
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpPost]
        public async Task<ActionResult> AuthenticateFaceLogin(string userName, string challengeToken = null)
        {
            try
            {
                if (string.IsNullOrWhiteSpace(userName))
                {
                    return Json(new { success = false, error = "Vui lòng nhập tài khoản trước khi đăng nhập bằng khuôn mặt." });
                }

                var user = new UserDraw().getByID(userName.Trim());
                if (user == null || user.IDQuyen != 2)
                {
                    return Json(new { success = false, error = "Tài khoản không tồn tại." });
                }

                if (!user.Status)
                {
                    return Json(new { success = false, error = "Tài khoản đã bị khóa." });
                }

                var faceLoginKey = GetFaceLoginAttemptKey(user.UserName);
                if (IsFaceLoginLocked(faceLoginKey))
                {
                    return Json(new { success = false, error = "Đăng nhập bằng khuôn mặt tạm thời bị khóa. Vui lòng thử lại sau." });
                }

                var file = Request.Files.Count > 0 ? Request.Files[0] : null;
                var validationError = ValidateFaceFile(file);
                if (validationError != null) return Json(new { success = false, error = validationError });
                var challengeError = ValidateFaceChallenge("Login", challengeToken);
                if (challengeError != null) return Json(new { success = false, error = challengeError });

                var filename = Guid.NewGuid() + Path.GetExtension(file.FileName);
                var relativePath = GetFaceStoragePath() + "/" + filename;
                var savePath = Server.MapPath("~/" + relativePath);
                Directory.CreateDirectory(Path.GetDirectoryName(savePath));
                file.SaveAs(savePath);

                var apiResponse = await _faceApiClient.VerifyAsync(savePath, filename, user.IDUser, "Login");
                var verified = IsFaceAccepted(apiResponse);
                var confidence = apiResponse.Confidence;

                _logRepo.AddFaceAuthLog(new FaceAuthLog
                {
                    UserID = user.IDUser,
                    Action = verified ? "FaceLoginSuccess" : "FaceLoginFailed",
                    Timestamp = DateTime.UtcNow,
                    IP = Request.UserHostAddress,
                    DeviceInfo = Request.UserAgent,
                    ImagePath = relativePath,
                    Result = verified,
                    Confidence = confidence,
                    RequestId = GetRequestId(apiResponse),
                    Purpose = "Login",
                    ErrorCode = apiResponse.ErrorCode,
                    ErrorMessage = apiResponse.ErrorMessage ?? apiResponse.Error,
                    LivenessPassed = apiResponse.LivenessPassed
                });

                if (!verified)
                {
                    RegisterFaceLoginFailure(faceLoginKey);
                    var detail = BuildFaceFailureMessage(apiResponse, confidence);
                    return Json(new { success = false, confidence, error = detail });
                }

                ClearFaceLoginFailures(faceLoginKey);
                Session[Constant.USER_SESSION] = new UserLogin
                {
                    userId = user.IDUser,
                    userName = user.UserName,
                    name = user.Name,
                    address = user.Adress,
                    email = user.Email,
                    phone = user.Phone
                };
                System.Web.Security.FormsAuthentication.SetAuthCookie(user.IDUser.ToString(), false);

                return Json(new { success = true, redirectUrl = "/Home/TrangChu" });
            }
            catch (Exception ex)
            {
                return Json(new { success = false, error = ex.Message });
            }
        }

        [HttpPost]
        public JsonResult CreateChallenge(string purpose)
        {
            var normalizedPurpose = string.IsNullOrWhiteSpace(purpose) ? "Verify" : purpose.Trim();
            if (normalizedPurpose != "Login" && normalizedPurpose != "Rental" && normalizedPurpose != "MFA")
            {
                normalizedPurpose = "Verify";
            }

            if (!IsActionChallengeRequired())
            {
                return Json(new
                {
                    success = true,
                    actionRequired = false,
                    token = string.Empty,
                    actionCode = string.Empty,
                    instruction = "Face action challenge is disabled.",
                    expiresInSeconds = 0
                });
            }

            var actions = FaceChallengeAction.All;
            var random = new Random();
            var token = Guid.NewGuid().ToString("N");
            var action = actions[random.Next(actions.Length)];
            var challenge = new FaceChallenge
            {
                Token = token,
                Purpose = normalizedPurpose,
                ActionCode = action.Code,
                Instruction = action.Instruction,
                CreatedAt = DateTime.UtcNow,
                ActionPassed = false
            };

            Session[GetChallengeSessionKey(normalizedPurpose)] = challenge;
            return Json(new
            {
                success = true,
                actionRequired = true,
                token,
                actionCode = challenge.ActionCode,
                instruction = challenge.Instruction,
                expiresInSeconds = 90
            });
        }

        [HttpPost]
        public async Task<ActionResult> CheckChallengeAction(string purpose, string challengeToken, string userName = null)
        {
            try
            {
                var normalizedPurpose = string.IsNullOrWhiteSpace(purpose) ? "Verify" : purpose.Trim();
                var challenge = GetActiveChallenge(normalizedPurpose, challengeToken);
                if (challenge == null)
                {
                    return Json(new { success = false, actionMatched = false, message = "Face challenge is invalid or expired." });
                }

                var file = Request.Files.Count > 0 ? Request.Files[0] : null;
                var validationError = ValidateFaceFile(file);
                if (validationError != null) return Json(new { success = false, actionMatched = false, message = validationError });

                long userId = 0;
                if (normalizedPurpose == "Rental")
                {
                    var userSession = Session[Constant.USER_SESSION] as UserLogin;
                    userId = userSession != null ? userSession.userId : 0;
                }
                else if (normalizedPurpose == "MFA")
                {
                    var pending = Session[Constant.FACE_MFA_SESSION] as UserLogin;
                    userId = pending != null ? pending.userId : 0;
                }
                else if (!string.IsNullOrWhiteSpace(userName))
                {
                    var user = new UserDraw().getByID(userName.Trim());
                    userId = user != null ? user.IDUser : 0;
                }

                var filename = Guid.NewGuid() + Path.GetExtension(file.FileName);
                var relativePath = GetFaceStoragePath() + "/" + filename;
                var savePath = Server.MapPath("~/" + relativePath);
                Directory.CreateDirectory(Path.GetDirectoryName(savePath));
                file.SaveAs(savePath);

                var apiResponse = await _faceApiClient.CheckActionAsync(savePath, filename, userId, normalizedPurpose, challenge.ActionCode);
                var matched = apiResponse.Success && apiResponse.ActionMatched;
                if (matched)
                {
                    challenge.ActionPassed = true;
                    Session[GetChallengeSessionKey(normalizedPurpose)] = challenge;
                }

                return Json(new
                {
                    success = true,
                    actionMatched = matched,
                    actionCode = challenge.ActionCode,
                    instruction = challenge.Instruction,
                    requestId = GetRequestId(apiResponse),
                    message = matched ? "Hanh dong da khop." : (apiResponse.ActionMessage ?? apiResponse.ErrorMessage ?? apiResponse.Error)
                });
            }
            catch (Exception ex)
            {
                return Json(new { success = false, actionMatched = false, message = ex.Message });
            }
        }

        [HttpPost]
        public async Task<ActionResult> RegisterFace(int userId)
        {
            try
            {
                var pending = Session[Constant.FACE_REGISTER_SESSION] as UserLogin;
                if (pending == null || pending.userId != userId)
                {
                    return Json(new { success = false, error = "Phiên đăng ký khuôn mặt không hợp lệ. Vui lòng đăng ký tài khoản lại." });
                }

                // receive uploaded file
                var file = Request.Files.Count > 0 ? Request.Files[0] : null;
                var validationError = ValidateFaceFile(file);
                if (validationError != null) return Json(new { success = false, error = validationError });

                var filename = Guid.NewGuid() + Path.GetExtension(file.FileName);
                var relativePath = GetFaceStoragePath() + "/" + filename;
                var savePath = Server.MapPath("~/" + relativePath);
                Directory.CreateDirectory(Path.GetDirectoryName(savePath));
                file.SaveAs(savePath);

                var apiResponse = await _faceApiClient.RegisterAsync(savePath, filename, userId);
                var apiResult = apiResponse.Success;
                var confidence = apiResponse.Confidence;
                var registerError = apiResponse.ErrorMessage ?? apiResponse.Error ?? apiResponse.ErrorCode;

                var log = new FaceAuthLog
                {
                    UserID = userId,
                    Action = "Register",
                    Timestamp = DateTime.UtcNow,
                    IP = Request.UserHostAddress,
                    DeviceInfo = Request.UserAgent,
                    ImagePath = relativePath,
                    Result = apiResult,
                    Confidence = confidence,
                    RequestId = GetRequestId(apiResponse),
                    Purpose = "Register",
                    ErrorCode = apiResponse.ErrorCode,
                    ErrorMessage = apiResponse.ErrorMessage ?? apiResponse.Error,
                    LivenessPassed = apiResponse.LivenessPassed
                };
                _logRepo.AddFaceAuthLog(log);

                if (apiResult)
                {
                    CompletePendingRegisterSession(userId);
                }

                return Json(new
                {
                    success = apiResult,
                    confidence,
                    message = apiResult ? "Đăng ký khuôn mặt thành công." : "Đăng ký khuôn mặt thất bại. Vui lòng thử lại.",
                    error = apiResult ? null : (apiResponse.ErrorMessage ?? apiResponse.Error ?? "Đăng ký khuôn mặt thất bại. Vui lòng thử lại."),
                    requestId = GetRequestId(apiResponse)
                });
            }
            catch (Exception ex)
            {
                return Json(new { success = false, error = ex.Message });
            }
        }

        [HttpPost]
        public async Task<ActionResult> VerifyFace(int userId)
        {
            try
            {
                var file = Request.Files.Count > 0 ? Request.Files[0] : null;
                var validationError = ValidateFaceFile(file);
                if (validationError != null) return Json(new { success = false, error = validationError });

                var filename = Guid.NewGuid() + Path.GetExtension(file.FileName);
                var relativePath = GetFaceStoragePath() + "/" + filename;
                var savePath = Server.MapPath("~/" + relativePath);
                Directory.CreateDirectory(Path.GetDirectoryName(savePath));
                file.SaveAs(savePath);

                var apiResponse = await _faceApiClient.VerifyAsync(savePath, filename, userId, "Verify");
                var verified = IsFaceAccepted(apiResponse);
                var confidence = apiResponse.Confidence;

                var log = new FaceAuthLog
                {
                    UserID = userId,
                    Action = "Verify",
                    Timestamp = DateTime.UtcNow,
                    IP = Request.UserHostAddress,
                    DeviceInfo = Request.UserAgent,
                    ImagePath = relativePath,
                    Result = verified,
                    Confidence = confidence,
                    RequestId = GetRequestId(apiResponse),
                    Purpose = "Verify",
                    ErrorCode = apiResponse.ErrorCode,
                    ErrorMessage = apiResponse.ErrorMessage ?? apiResponse.Error,
                    LivenessPassed = apiResponse.LivenessPassed
                };
                _logRepo.AddFaceAuthLog(log);

                return Json(new { success = verified, confidence });
            }
            catch (Exception ex)
            {
                return Json(new { success = false, error = ex.Message });
            }
        }

        [HttpPost]
        public async Task<ActionResult> AuthenticateFace(int userId, string password = null, string challengeToken = null)
        {
            try
            {
                // Rate limit per IP using HttpRuntime.Cache.
                var ipAddr = Request.UserHostAddress ?? "unknown";
                var cacheKey = "ratelimit:" + ipAddr;
                var cache = HttpRuntime.Cache;
                var entry = cache[cacheKey] as System.Collections.Generic.List<DateTime>;
                var now = DateTime.UtcNow;
                if (entry == null)
                {
                    entry = new System.Collections.Generic.List<DateTime>();
                    cache.Insert(cacheKey, entry, null, DateTime.UtcNow.AddSeconds(GetRateLimitSeconds()), System.Web.Caching.Cache.NoSlidingExpiration);
                }
                entry.RemoveAll(t => (now - t).TotalSeconds > GetRateLimitSeconds());
                if (entry.Count >= GetRateLimitAttempts())
                {
                    return Json(new { success = false, error = "Too many attempts, try later" });
                }
                entry.Add(now);

                // Step 1: optional password check (fallback)
                var passwordOk = true;
                if (!string.IsNullOrEmpty(password))
                {
                    // validate against configured membership provider if available
                    try
                    {
                        // If the project uses classic Membership
                        var username = userId.ToString();
                        passwordOk = System.Web.Security.Membership.ValidateUser(username, password);
                    }
                    catch
                    {
                        passwordOk = false;
                    }
                }

                // Step 2: expect file upload for face
                var file = Request.Files.Count > 0 ? Request.Files[0] : null;
                if (file == null && !passwordOk)
                {
                    return Json(new { success = false, error = "No credentials provided" });
                }

                var faceVerified = false; double confidence = 0;
                string relativePath = null;
                FaceAuthResponse apiResponse = null;

                if (file != null)
                {
                    var validationError = ValidateFaceFile(file);
                    if (validationError != null) return Json(new { success = false, error = validationError });
                    var challengeError = ValidateFaceChallenge("MFA", challengeToken);
                    if (challengeError != null) return Json(new { success = false, error = challengeError });

                    var filename = Guid.NewGuid() + Path.GetExtension(file.FileName);
                    relativePath = GetFaceStoragePath() + "/" + filename;
                    var savePath = Server.MapPath("~/" + relativePath);
                    Directory.CreateDirectory(Path.GetDirectoryName(savePath));
                    file.SaveAs(savePath);

                    apiResponse = await _faceApiClient.AuthenticateAsync(savePath, filename, userId);
                    faceVerified = IsFaceAccepted(apiResponse);
                    confidence = apiResponse.Confidence;
                }

                var requireFaceMfa = GetBoolSetting("EnableFaceMFA", true);
                var allowPasswordOnlyFallback = GetBoolSetting("AllowPasswordOnlyFallback", false);
                var hasPassword = !string.IsNullOrEmpty(password);
                var overallSuccess = requireFaceMfa
                    ? ((hasPassword ? passwordOk : true) && faceVerified)
                    : (passwordOk || faceVerified);
                if (allowPasswordOnlyFallback && passwordOk)
                {
                    overallSuccess = true;
                }

                var log = new FaceAuthLog
                {
                    UserID = userId,
                    Action = "Authenticate",
                    Timestamp = DateTime.UtcNow,
                    IP = Request.UserHostAddress,
                    DeviceInfo = Request.UserAgent,
                    ImagePath = relativePath,
                    Result = overallSuccess,
                    Confidence = confidence,
                    RequestId = GetRequestId(apiResponse),
                    Purpose = "MFA",
                    ErrorCode = apiResponse != null ? apiResponse.ErrorCode : null,
                    ErrorMessage = apiResponse != null ? apiResponse.ErrorMessage ?? apiResponse.Error : null,
                    LivenessPassed = apiResponse != null ? (bool?)apiResponse.LivenessPassed : null
                };
                _logRepo.AddFaceAuthLog(log);

                if (overallSuccess)
                {
                    CompletePendingMfaSession(userId);
                    System.Web.Security.FormsAuthentication.SetAuthCookie(userId.ToString(), false);
                    return Json(new { success = true });
                }

                return Json(new { success = false, confidence });
            }
            catch (Exception ex)
            {
                return Json(new { success = false, error = ex.Message });
            }
        }

        private static string ValidateFaceFile(HttpPostedFileBase file)
        {
            if (file == null) return "No file";
            if (file.ContentLength <= 0) return "Empty file";
            if (file.ContentLength > GetMaxUploadBytes()) return "File is too large";

            var extension = (Path.GetExtension(file.FileName) ?? string.Empty).ToLowerInvariant();
            if (extension != ".jpg" && extension != ".jpeg" && extension != ".png")
            {
                return "Only jpg, jpeg, png files are supported";
            }

            return null;
        }

        private static string ValidateIdentityFile(HttpPostedFileBase file)
        {
            if (file == null) return "Vui lòng tải ảnh CMND/CCCD.";
            if (file.ContentLength <= 0) return "File CMND/CCCD đang rỗng.";
            if (file.ContentLength > GetMaxUploadBytes()) return "File CMND/CCCD quá lớn.";

            var extension = (Path.GetExtension(file.FileName) ?? string.Empty).ToLowerInvariant();
            if (extension != ".jpg" && extension != ".jpeg" && extension != ".png")
            {
                return "Chỉ hỗ trợ ảnh CMND/CCCD định dạng jpg, jpeg, png.";
            }

            return null;
        }

        private IdentityUploadPair SaveIdentityUploadPair(string subFolder)
        {
            var frontFile = Request.Files["front_file"] ?? Request.Files["frontFile"] ?? Request.Files["front"] ?? Request.Files["file"];
            var backFile = Request.Files["back_file"] ?? Request.Files["backFile"] ?? Request.Files["back"];

            if (frontFile == null && Request.Files.Count > 0)
            {
                frontFile = Request.Files[0];
            }

            if (backFile == null && Request.Files.Count > 1)
            {
                backFile = Request.Files[1];
            }

            var frontError = frontFile != null && frontFile.ContentLength > 0 ? ValidateIdentityFile(frontFile) : null;
            var backError = backFile != null && backFile.ContentLength > 0 ? ValidateIdentityFile(backFile) : null;
            if (frontError != null) return new IdentityUploadPair { Error = frontError };
            if (backError != null) return new IdentityUploadPair { Error = backError };
            if ((frontFile == null || frontFile.ContentLength <= 0) && (backFile == null || backFile.ContentLength <= 0))
            {
                return new IdentityUploadPair { Error = ValidateIdentityFile(null) };
            }

            var pair = new IdentityUploadPair();
            SaveIdentityFile(frontFile, subFolder, "front", pair);
            SaveIdentityFile(backFile, subFolder, "back", pair);
            return pair;
        }

        private void SaveIdentityFile(HttpPostedFileBase file, string subFolder, string side, IdentityUploadPair pair)
        {
            if (file == null || file.ContentLength <= 0) return;

            var filename = Guid.NewGuid() + Path.GetExtension(file.FileName);
            var relativeFolder = GetIdentityStoragePath();
            if (!string.IsNullOrWhiteSpace(subFolder))
            {
                relativeFolder += "/" + subFolder.Trim('/').Replace("\\", "/");
            }

            var relativePath = relativeFolder + "/" + filename;
            var savePath = Server.MapPath("~/" + relativePath);
            Directory.CreateDirectory(Path.GetDirectoryName(savePath));
            file.SaveAs(savePath);

            if (side == "back")
            {
                pair.BackFileName = filename;
                pair.BackRelativePath = relativePath;
                pair.BackSavePath = savePath;
            }
            else
            {
                pair.FrontFileName = filename;
                pair.FrontRelativePath = relativePath;
                pair.FrontSavePath = savePath;
            }
        }

        private string ValidateFaceChallenge(string purpose, string token)
        {
            if (!IsActionChallengeRequired())
            {
                return null;
            }

            var key = GetChallengeSessionKey(purpose);
            var challenge = GetActiveChallenge(purpose, token);
            Session[key] = null;

            if (challenge == null)
            {
                return "Face challenge is invalid. Please try again.";
            }

            if (!challenge.ActionPassed)
            {
                return "Face action challenge has not passed. Please follow the random instruction first.";
            }

            return null;
        }

        private FaceChallenge GetActiveChallenge(string purpose, string token)
        {
            if (string.IsNullOrWhiteSpace(token))
            {
                return null;
            }

            var challenge = Session[GetChallengeSessionKey(purpose)] as FaceChallenge;
            if (challenge == null || challenge.Purpose != purpose || challenge.Token != token)
            {
                return null;
            }

            if ((DateTime.UtcNow - challenge.CreatedAt).TotalSeconds > 90)
            {
                return null;
            }

            return challenge;
        }

        private static string GetChallengeSessionKey(string purpose)
        {
            return "FaceChallenge:" + purpose;
        }

        private class FaceChallenge
        {
            public string Token { get; set; }

            public string Purpose { get; set; }

            public string ActionCode { get; set; }

            public string Instruction { get; set; }

            public DateTime CreatedAt { get; set; }

            public bool ActionPassed { get; set; }
        }

        private class FaceChallengeAction
        {
            public string Code { get; set; }

            public string Instruction { get; set; }

            public static readonly FaceChallengeAction[] All =
            {
                new FaceChallengeAction { Code = "turn_left", Instruction = "Quay mat sang trai" },
                new FaceChallengeAction { Code = "turn_right", Instruction = "Quay mat sang phai" },
                new FaceChallengeAction { Code = "mouth_open", Instruction = "Ha mieng" },
                new FaceChallengeAction { Code = "smile", Instruction = "Cuoi" },
                new FaceChallengeAction { Code = "look_up", Instruction = "Nhin len" },
                new FaceChallengeAction { Code = "look_down", Instruction = "Nhin xuong" }
            };
        }

        private class IdentityUploadPair
        {
            public string FrontFileName { get; set; }
            public string FrontRelativePath { get; set; }
            public string FrontSavePath { get; set; }
            public string BackFileName { get; set; }
            public string BackRelativePath { get; set; }
            public string BackSavePath { get; set; }
            public string Error { get; set; }
        }

        private static string GetFaceStoragePath()
        {
            var path = ConfigurationManager.AppSettings["FaceSampleStoragePath"];
            return string.IsNullOrWhiteSpace(path) ? "DataImage/FaceSamples" : path.Trim().Trim('/').Replace("\\", "/");
        }

        private static string GetIdentityStoragePath()
        {
            var path = ConfigurationManager.AppSettings["IdentityCardStoragePath"];
            return string.IsNullOrWhiteSpace(path) ? "DataImage/IdentityCards" : path.Trim().Trim('/').Replace("\\", "/");
        }

        private static string ReadString(JObject json, params string[] names)
        {
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

        private static bool ReadBool(JObject json, params string[] names)
        {
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

        private static double ReadDouble(JObject json, params string[] names)
        {
            foreach (var name in names)
            {
                var token = json[name];
                if (token != null && token.Type != JTokenType.Null)
                {
                    double value;
                    if (double.TryParse(token.ToString(), NumberStyles.Float, CultureInfo.InvariantCulture, out value)) return value;
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

        private static int GetFaceApiTimeoutSeconds()
        {
            int value;
            return int.TryParse(ConfigurationManager.AppSettings["FaceAuthTimeoutSeconds"], out value) && value > 0 ? value : 15;
        }

        private static double GetMinConfidence()
        {
            double value;
            var rawValue = ConfigurationManager.AppSettings["FaceAuthMinConfidence"];
            return (double.TryParse(rawValue, NumberStyles.Float, CultureInfo.InvariantCulture, out value)
                    || double.TryParse(rawValue, out value)) && value >= 0
                ? value
                : 0.75;
        }

        private static int GetMaxUploadBytes()
        {
            int value;
            return int.TryParse(ConfigurationManager.AppSettings["FaceAuthMaxUploadBytes"], out value) && value > 0 ? value : 5242880;
        }

        private static int GetRateLimitAttempts()
        {
            int value;
            return int.TryParse(ConfigurationManager.AppSettings["FaceAuthRateLimitAttempts"], out value) && value > 0 ? value : 10;
        }

        private static int GetRateLimitSeconds()
        {
            int value;
            return int.TryParse(ConfigurationManager.AppSettings["FaceAuthRateLimitSeconds"], out value) && value > 0 ? value : 60;
        }

        private static int GetFaceLoginMaxAttempts()
        {
            int value;
            return int.TryParse(ConfigurationManager.AppSettings["FaceAuthMaxAttempts"], out value) && value > 0 ? value : 5;
        }

        private static int GetFaceLoginLockoutMinutes()
        {
            int value;
            return int.TryParse(ConfigurationManager.AppSettings["FaceAuthLockoutMinutes"], out value) && value > 0 ? value : 10;
        }

        private static bool GetBoolSetting(string key, bool defaultValue)
        {
            bool value;
            return bool.TryParse(ConfigurationManager.AppSettings[key], out value) ? value : defaultValue;
        }

        private static bool IsActionChallengeRequired()
        {
            return GetBoolSetting("FaceAuthRequireActionChallenge", false);
        }

        private string GetFaceLoginAttemptKey(string userName)
        {
            return "face-login-attempts:" + (Request.UserHostAddress ?? "unknown") + ":" + (userName ?? string.Empty).Trim().ToLowerInvariant();
        }

        private static bool IsFaceLoginLocked(string cacheKey)
        {
            var attempts = HttpRuntime.Cache[cacheKey] as System.Collections.Generic.List<DateTime>;
            if (attempts == null) return false;

            var lockoutWindow = TimeSpan.FromMinutes(GetFaceLoginLockoutMinutes());
            var now = DateTime.UtcNow;
            attempts.RemoveAll(t => now - t > lockoutWindow);
            return attempts.Count >= GetFaceLoginMaxAttempts();
        }

        private static void RegisterFaceLoginFailure(string cacheKey)
        {
            var cache = HttpRuntime.Cache;
            var attempts = cache[cacheKey] as System.Collections.Generic.List<DateTime>;
            if (attempts == null)
            {
                attempts = new System.Collections.Generic.List<DateTime>();
            }

            attempts.Add(DateTime.UtcNow);
            cache.Insert(cacheKey, attempts, null, DateTime.UtcNow.AddMinutes(GetFaceLoginLockoutMinutes()), System.Web.Caching.Cache.NoSlidingExpiration);
        }

        private static void ClearFaceLoginFailures(string cacheKey)
        {
            HttpRuntime.Cache.Remove(cacheKey);
        }

        private static string GetRequestId(FaceAuthResponse response)
        {
            return response != null && !string.IsNullOrWhiteSpace(response.RequestId)
                ? response.RequestId
                : Guid.NewGuid().ToString("N");
        }

        private static bool IsFaceAccepted(FaceAuthResponse response)
        {
            if (response == null)
            {
                return false;
            }

            if (response.Success && response.Confidence >= GetMinConfidence())
            {
                return true;
            }

            var errorCode = (response.ErrorCode ?? string.Empty).Trim().ToUpperInvariant();
            if (errorCode == "NO_FACE_DETECTED"
                || errorCode == "LOW_IMAGE_QUALITY"
                || errorCode == "FACE_PROFILE_NOT_FOUND"
                || errorCode == "ACTION_REQUIRED"
                || errorCode == "ACTION_NOT_MATCHED")
            {
                return false;
            }

            return response.Confidence >= GetMinConfidence();
        }

        private static string BuildFaceFailureMessage(FaceAuthResponse response, double confidence)
        {
            if (response != null)
            {
                if (response.ErrorCode == "FACE_PROFILE_NOT_FOUND")
                {
                    return "Tài khoản chưa đăng ký mẫu khuôn mặt. Vui lòng đăng ký/xác thực khuôn mặt lại.";
                }

                if (response.ErrorCode == "NO_FACE_DETECTED")
                {
                    return "Không phát hiện khuôn mặt. Vui lòng đưa mặt vào giữa khung hình và thử lại.";
                }

                if (response.ErrorCode == "LOW_IMAGE_QUALITY")
                {
                    return "Ảnh khuôn mặt chưa rõ. Vui lòng tăng ánh sáng, nhìn thẳng camera và thử lại.";
                }

                if (!string.IsNullOrWhiteSpace(response.ErrorMessage))
                {
                    return response.ErrorMessage + " Độ khớp: " + confidence.ToString("0.00", CultureInfo.InvariantCulture);
                }
            }

            return "Xác thực khuôn mặt thất bại. Độ khớp: " + confidence.ToString("0.00", CultureInfo.InvariantCulture);
        }

        private void CompletePendingRegisterSession(long userId)
        {
            var pending = Session[Constant.FACE_REGISTER_SESSION] as UserLogin;
            if (pending != null && pending.userId == userId)
            {
                Session[Constant.USER_SESSION] = pending;
                Session[Constant.FACE_REGISTER_SESSION] = null;
            }
        }

        private void CompletePendingMfaSession(long userId)
        {
            var pending = Session[Constant.FACE_MFA_SESSION] as UserLogin;
            if (pending != null && pending.userId == userId)
            {
                Session[Constant.USER_SESSION] = pending;
                Session[Constant.FACE_MFA_SESSION] = null;
            }
        }
    }
}

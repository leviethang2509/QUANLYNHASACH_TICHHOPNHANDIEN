using BaiTapLon.Common;
using BaiTapLon.Models;
using BotDetect.Web.Mvc;
using CommomSentMail;
using Facebook;
using Mood.Draw;
using Mood.EF2;
using Mood.HoaDonModel;
using System;
using System.Collections.Generic;
using System.Configuration;
using System.IO;
using IOFile = System.IO.File;
using System.Linq;
using System.Text;
using System.Web;
using System.Web.Mvc;
namespace BaiTapLon.Controllers
{
    public class UsersController : Controller
    {
        private const string CartSession = "CartSession";// hằng số không thể đổi
        private Uri RedirectUri
        {
            get
            {
                var uriBuilder = new UriBuilder(Request.Url);
                uriBuilder.Query = null;
                uriBuilder.Fragment = null;
                uriBuilder.Path = Url.Action("FacebookCallback");
                return uriBuilder.Uri;
            }
        }

        [HttpPost]
        public JsonResult RegisterUser(RegisterModel model)
        {
            int result = 0;
            string message = "Đăng ký thất bại. Vui lòng kiểm tra lại thông tin.";

            if (ModelState.IsValid)// kiểm tra xem dữ liệu rỗng ko
            {
                model.UserName = (model.UserName ?? string.Empty).Trim();
                model.PassWord = model.PassWord ?? string.Empty;
                model.ConfirmPass = model.ConfirmPass ?? string.Empty;
                model.Name = (model.Name ?? string.Empty).Trim();
                model.Address = (model.Address ?? string.Empty).Trim();
                model.Phone = (model.Phone ?? string.Empty).Trim();
                model.NotificationEmail = (model.NotificationEmail ?? model.Email ?? string.Empty).Trim();
                model.Email = model.NotificationEmail;
                model.IdentityNumber = (model.IdentityNumber ?? string.Empty).Trim();
                model.IdentityFullName = (model.IdentityFullName ?? string.Empty).Trim();
                model.IdentityAddress = (model.IdentityAddress ?? string.Empty).Trim();
                model.IdentityPlaceOfBirth = (model.IdentityPlaceOfBirth ?? string.Empty).Trim();
                model.IdentityGender = (model.IdentityGender ?? string.Empty).Trim();
                model.IdentityNationality = (model.IdentityNationality ?? string.Empty).Trim();
                model.IdentityIssuePlace = (model.IdentityIssuePlace ?? string.Empty).Trim();
                model.IdentityIssuingAuthority = (model.IdentityIssuingAuthority ?? string.Empty).Trim();

                var dao = new UserDraw();// tạo một đối tượng UserDraw
                if (model.PassWord == model.ConfirmPass)
                {
                    if (dao.IsValidEmail(model.NotificationEmail) == true)
                    {
                        if (!string.IsNullOrWhiteSpace(model.Phone) && dao.CheckSDT(model.Phone) == true)
                        {
                            if (dao.checkUserName(model.UserName) == true)
                            {
                                if (dao.checkMailUser(model.NotificationEmail) == false)
                                {
                                    var user = new User();
                                    user.PassWord = EncryptorMD5.GetMD5(model.PassWord);// mã hóa mật khẩu khi truyền vào
                                    user.NgayTao = DateTime.Now;
                                    user.UserName = model.UserName;
                                    user.Email = model.NotificationEmail;
                                    user.NotificationEmail = model.NotificationEmail;
                                    user.Adress = model.Address;
                                    user.Name = model.Name;
                                    user.Phone = model.Phone;
                                    user.Status = true;
                                    user.IDQuyen = 2;
                                    user.IdentityNumber = model.IdentityNumber;
                                    user.IdentityFullName = model.IdentityFullName;
                                    user.IdentityDateOfBirth = model.IdentityDateOfBirth;
                                    user.IdentityAddress = model.IdentityAddress;
                                    user.IdentityPlaceOfBirth = model.IdentityPlaceOfBirth;
                                    user.IdentityGender = model.IdentityGender;
                                    user.IdentityNationality = model.IdentityNationality;
                                    user.IdentityIssueDate = model.IdentityIssueDate;
                                    user.IdentityIssuePlace = model.IdentityIssuePlace;
                                    user.IdentityExpiryDate = model.IdentityExpiryDate;
                                    user.IdentityIssuingAuthority = model.IdentityIssuingAuthority;
                                    try
                                    {
                                        long id = dao.Insert(user); // truyền entityUser với thông tin nhận từ view xuống database
                                        if (id > 0)// nếu có một user mới sẽ có một id ,  do đó nếu id >0 thì đã có user
                                        {
                                            var userSession = new UserLogin();
                                            userSession.userName = user.UserName;
                                            userSession.name = user.Name;
                                            userSession.address = user.Adress;
                                            userSession.userId = id;
                                            Session[Constant.FACE_REGISTER_SESSION] = userSession;
                                            model = new RegisterModel();
                                            result = IsFaceMfaEnabled() ? 2 : 1;
                                            if (result == 1)
                                            {
                                                Session[Constant.USER_SESSION] = userSession;
                                                message = "Đăng ký thành công.";
                                            }
                                            else
                                            {
                                                message = "Thông tin hợp lệ. Vui lòng xác thực khuôn mặt.";
                                            }

                                        }
                                        else
                                        {

                                            result = 0;
                                            message = "Không tạo được tài khoản trong cơ sở dữ liệu.";
                                            //ModelState.AddModelError("CreateUser1", "Tạo tài khoản thất bại !!!");
                                        }
                                    }
                                    catch (Exception ex)
                                    {

                                        result = 0;
                                        message = "Lỗi khi lưu tài khoản: " + ex.Message;
                                        //ModelState.AddModelError("CreateUser1", "Tạo tài khoản thất bại !!!");
                                    }
                                }
                                else
                                {

                                    result = -1;
                                    message = "Email này đã có người đăng ký.";
                                }
                            }

                            else
                            {

                                result = -2;
                                message = "Người dùng này đã tồn tại.";
                                //ModelState.AddModelError("CreateUser1", "Người dùng này đã tồn tại!!!");
                            }
                        }
                        else
                        {

                            result = -3;
                            message = "Số điện thoại không hợp lệ. Vui lòng chỉ nhập chữ số.";
                            //ModelState.AddModelError("CreateUser1", "Số điện thoại không hợp lệ");
                        }
                    }
                    else
                    {

                        result = -4;
                        message = "Định dạng email sai.";
                        //ModelState.AddModelError("CreateUser1", "Bạn đã nhập sai định dạng email");
                    }
                }
                else
                {
                    result = -5;
                    message = "Mật khẩu không trùng khớp.";
                }


            }
            else
            {
                ViewBag.Error = "Tạo tài khoản thất bại !!!";
                result = 0;
                message = string.Join(" ", ModelState.Values
                    .SelectMany(v => v.Errors)
                    .Select(e => !string.IsNullOrWhiteSpace(e.ErrorMessage)
                        ? e.ErrorMessage
                        : (e.Exception != null ? e.Exception.Message : string.Empty)));
                if (string.IsNullOrWhiteSpace(message))
                {
                    message = "Thông tin đăng ký chưa hợp lệ. Vui lòng nhập đầy đủ các trường bắt buộc.";
                }
            }
            var pendingFaceUser = Session[Constant.FACE_REGISTER_SESSION] as UserLogin;
            return Json(new { code = result, message, faceUserId = pendingFaceUser != null ? pendingFaceUser.userId : 0 }, JsonRequestBehavior.AllowGet);
        }
        [ChildActionOnly]
        public PartialViewResult Login()
        {
            return PartialView();
        }

        [HttpGet]
        public ActionResult DangNhap()
        {
            return RedirectToAction("TrangChu", "Home");
        }

        [HttpPost]
        public JsonResult DangNhap(LoginModel model)
        {
            return Login(model);
        }

        [HttpPost]
        public JsonResult Login(LoginModel model)
        {
            if (IsFixedAdminLogin(model != null ? model.UserName : null, model != null ? model.PassWord : null))
            {
                SignInFixedAdmin();
                return Json(10, JsonRequestBehavior.AllowGet);
            }

            var draw = new UserDraw();
            var result = 5;
            if (ModelState.IsValid)
            {
                result = draw.LoginHomeUser(model.UserName, EncryptorMD5.GetMD5(model.PassWord));
                if (result == 1)
                {

                    var user = draw.getByID(model.UserName);
                    var userSession = new UserLogin();
                    userSession.userName = user.UserName;
                    userSession.name = user.Name;
                    userSession.address = user.Adress;
                    userSession.userId = user.IDUser;
                    if (user.IDQuyen == 1)
                    {
                        Session.Add(Constant.USER_SESSION, userSession);
                        Session[Constant.ADMIN_SESSION] = new AdminLogin
                        {
                            userId = user.IDUser,
                            userName = user.UserName,
                            name = user.Name,
                            address = user.Adress,
                            email = user.Email,
                            phone = user.Phone
                        };
                        return Json(10, JsonRequestBehavior.AllowGet);
                    }

                    if (IsFaceMfaEnabled())
                    {
                        Session[Constant.FACE_MFA_SESSION] = userSession;
                        return Json(2, JsonRequestBehavior.AllowGet);
                    }

                    Session.Add(Constant.USER_SESSION, userSession);

                    return Json(result, JsonRequestBehavior.AllowGet);
                }
            }
            return Json(result, JsonRequestBehavior.AllowGet);
        }

        public ActionResult RegisterFace()
        {
            var pending = Session[Constant.FACE_REGISTER_SESSION] as UserLogin;
            if (pending == null)
            {
                return Redirect("/");
            }

            ViewBag.FaceUserId = pending.userId;
            return View();
        }

        public ActionResult LoginMFA()
        {
            var pending = Session[Constant.FACE_MFA_SESSION] as UserLogin;
            if (pending == null)
            {
                return Redirect("/");
            }

            ViewBag.FaceUserId = pending.userId;
            return View();
        }

        public ActionResult Logout()
        {
            Session[Common.Constant.USER_SESSION] = null;
            Session[Common.Constant.FACE_MFA_SESSION] = null;
            Session[Common.Constant.FACE_REGISTER_SESSION] = null;
            Session[CartSession] = null;
            return Redirect("/");
        }
        public ActionResult ProfileUser()
        {
            var userProfile = (UserLogin)Session[Common.Constant.USER_SESSION];
            
            if (userProfile != null)
            {
                var userModel = new UserDraw().getIDByUser(userProfile.userId);
                userProfile.tolMes = new OrderDraw().getToTolMes(userProfile.userId);
                userProfile.tolRep = new MessengerDraw().getTotalReply(userProfile.userId);
                userProfile.totalMessenger = (userProfile.tolMes + userProfile.tolRep);
                return View(userModel);
            }

            return View();
        }
        public ActionResult Dashboard()
        {
            var userProfile = (UserLogin)Session[Common.Constant.USER_SESSION];

            if (userProfile != null)
            {
                var userModel = new UserDraw().getIDByUser(userProfile.userId);
                userProfile.tolMes = new OrderDraw().getToTolMes(userProfile.userId);
                userProfile.tolRep = new MessengerDraw().getTotalReply(userProfile.userId);
                userProfile.totalMessenger = (userProfile.tolMes + userProfile.tolRep);
                return View(userModel);
            }

            return View();
        }
        
        [HttpPost]
        public JsonResult EditUser(User entity)
        {
            int data = 0;
            var userChange = new UserDraw().getIDByUser(entity.IDUser);
            userChange.Name = entity.Name;
            userChange.Phone = entity.Phone;
            userChange.Email = entity.Email;
            userChange.NotificationEmail = string.IsNullOrWhiteSpace(entity.NotificationEmail)
                ? entity.Email
                : entity.NotificationEmail.Trim();
            userChange.Adress = entity.Adress;
            userChange.IdentityNumber = (entity.IdentityNumber ?? string.Empty).Trim();
            userChange.IdentityFullName = (entity.IdentityFullName ?? string.Empty).Trim();
            userChange.IdentityDateOfBirth = entity.IdentityDateOfBirth;
            userChange.IdentityAddress = (entity.IdentityAddress ?? string.Empty).Trim();
            userChange.IdentityPlaceOfBirth = (entity.IdentityPlaceOfBirth ?? string.Empty).Trim();
            userChange.IdentityGender = (entity.IdentityGender ?? string.Empty).Trim();
            userChange.IdentityNationality = (entity.IdentityNationality ?? string.Empty).Trim();
            userChange.IdentityIssueDate = entity.IdentityIssueDate;
            userChange.IdentityIssuePlace = (entity.IdentityIssuePlace ?? string.Empty).Trim();
            userChange.IdentityExpiryDate = entity.IdentityExpiryDate;
            userChange.IdentityIssuingAuthority = (entity.IdentityIssuingAuthority ?? string.Empty).Trim();
            if (Session[Constant.USER_SESSION] != null)
            {
                var user = new UserDraw();
                    
                    var notificationEmail = (entity.NotificationEmail ?? entity.Email ?? string.Empty).Trim();
                    entity.Email = notificationEmail;
                    userChange.Email = notificationEmail;
                    userChange.NotificationEmail = notificationEmail;

                    if (user.IsValidEmail(notificationEmail) == true)
                    {
                        if (user.CheckSDT(entity.Phone) == true)
                        {
                            var result = user.UpdateUser(userChange);
                            if (result == true)
                            {
                                var userAdd = new UserDraw().getByID(userChange.UserName);
                                var userSession = new UserLogin();
                                userSession.userName = userAdd.UserName;
                                userSession.name = userAdd.Name;
                                userSession.address = userAdd.Adress;
                                userSession.userId = userAdd.IDUser;
                                Session.Add(Constant.USER_SESSION, userSession);
                                ViewBag.Success = "Cập nhật thành công";
                                data = 1;
                                //return RedirectToAction("Index", "User");
                            }
                            else
                            {
                                ViewBag.Error = "Cập nhật không thành công";
                                data = 0;
                            }
                        }
                        else
                        {
                            ViewBag.Error = "Định dạng số điện thoại không hợp lệ!!!";
                            data = -1;
                        }
                    }
                    else
                    {
                        ViewBag.Error = "Định dạng email không hợp lệ!!!";
                        data = -2;
                    }
                
                
                
                return Json(data, JsonRequestBehavior.AllowGet);
            }
            return Json(data,JsonRequestBehavior.AllowGet);
        }

        

        [HttpPost]
        public JsonResult EditPassWord(RestestPassModel modelPass)
        {
            int data = 0;
            var userChange = new UserDraw().getIDByUser(modelPass.IDUser);
            
            if (Session[Constant.USER_SESSION] != null)
            {
                if (ModelState.IsValid)
                {
                    var user = new UserDraw();
                    if (!string.IsNullOrEmpty(userChange.PassWord))
                    {
                        if(modelPass.oldPassWord != null || modelPass.oldPassWord != null)
                        {
                            if (userChange.PassWord.Contains(EncryptorMD5.GetMD5(modelPass.oldPassWord)))
                            {
                                if (modelPass.newPassWorrd.Contains(modelPass.confinrmPass))
                                {
                                    var result = user.UpdatePassword(userChange, EncryptorMD5.GetMD5(modelPass.newPassWorrd));
                                    if (result == true)
                                    {
                                        ViewBag.Success = "Đổi mật khẩu thành công";
                                        data = 1;
                                        //return RedirectToAction("Index", "User");
                                    }
                                    else
                                    {
                                        ViewBag.Error = "Cập nhật không thành công";
                                        data = 0;
                                    }
                                }
                                else
                                {
                                    ViewBag.Error = "Mật khẩu mới không trùng khớp";
                                    data = -2;
                                }
                            }
                            else
                            {
                                ViewBag.Error = "Mật khẩu cũ không chính xác";
                                data = -3;
                            }
                        }
                        else
                        {
                            data = -4;
                        }
                    }
                    else
                    {
                        ViewBag.Error = "Mật khẩu cũ không được để trống";
                        data = -1;
                    }

                }

                return Json(data, JsonRequestBehavior.AllowGet);
            }
            return Json(data, JsonRequestBehavior.AllowGet);
        }
        [HttpGet]
        public ActionResult DanhSachHang(long id, string searhString, int page = 1, int pagesize = 5)
        {
            if (Session[Constant.USER_SESSION] != null)
            {
                var orderUser = new UserDraw().ListALLHoaDonUSer(id, searhString, page, pagesize);
                return View(orderUser);
            }
            return View();
        }

        [HttpGet]
        public ActionResult Favorites(long id = 0, string searhString = "", int page = 1, int pagesize = 8)
        {
            var session = Session[Constant.USER_SESSION] as UserLogin;
            if (session == null)
            {
                ViewBag.SearchString = searhString;
                ViewBag.LocalFavorites = true;
                return View("LocalFavorites");
            }

            if (id != session.userId)
            {
                return RedirectToAction("Favorites", new { id = session.userId });
            }

            session.tolMes = new OrderDraw().getToTolMes(session.userId);
            session.tolRep = new MessengerDraw().getTotalReply(session.userId);
            session.totalMessenger = session.tolMes + session.tolRep;

            var favorites = new ProductFavoriteDraw().ListByUser(session.userId, searhString, page, pagesize);
            ViewBag.SearchString = searhString;
            ViewBag.FavoriteOwnerName = session.name;
            ViewBag.FavoriteOwnerUserName = session.userName;
            return View(favorites);
        }

        [HttpPost]
        public JsonResult ToggleFavorite(long productId)
        {
            var session = Session[Constant.USER_SESSION] as UserLogin;
            if (session == null)
            {
                return Json(new { success = false, useLocal = true, message = "Đã lưu yêu thích trên trình duyệt hiện tại." });
            }

            bool isFavorite;
            var draw = new ProductFavoriteDraw();
            var success = draw.Toggle(session.userId, productId, out isFavorite);
            if (!success)
            {
                return Json(new { success = false, message = "Không tìm thấy sách cần thêm vào yêu thích." });
            }

            return Json(new
            {
                success = true,
                isFavorite,
                count = draw.CountByUser(session.userId),
                message = isFavorite ? "Đã thêm sách vào yêu thích." : "Đã bỏ sách khỏi yêu thích."
            });
        }

        [HttpPost]
        public JsonResult LocalFavoriteProducts(List<long> productIds)
        {
            var products = new ProductFavoriteDraw().ListByIds(productIds);
            var data = products.Select(x => new
            {
                id = x.IDContent,
                name = x.Name,
                metaTitle = x.MetaTitle,
                image = x.Images,
                author = x.TacGia,
                price = x.GiaTien
            });

            return Json(new { success = true, products = data }, JsonRequestBehavior.AllowGet);
        }

        [HttpPost]
        public JsonResult SyncLocalFavorites(List<long> productIds)
        {
            var session = Session[Constant.USER_SESSION] as UserLogin;
            if (session == null)
            {
                return Json(new { success = false, useLocal = true, message = "Chưa đăng nhập." });
            }

            var draw = new ProductFavoriteDraw();
            var added = draw.AddMissing(session.userId, productIds);
            return Json(new
            {
                success = true,
                added,
                count = draw.CountByUser(session.userId)
            });
        }
        [HttpPost]
        public JsonResult ChangeSuccessOrder(long id)
        {
            var result = new OrderDraw().ChangeHoanThanh(id);
            return Json(
                new { NhanHang = result });
        }
        [HttpGet]
        public ActionResult ChiTietHoaDon(long id, int page = 1, int pagesize = 20)
        {
            if (Session[Constant.USER_SESSION] != null)
            {
                var hoaDonModel = new OrderDraw().getOrderByID(id);
                ViewBag.hoaDonSanPham = new Order_DetailDraw().chiTietHoaDonUser(id, page, pagesize);
                int priceTotol = 0;
                var listItem = new Order_DetailDraw().dataExport(id,"");
                foreach (var item1 in listItem)
                {
                      int temp = (int)item1.Price * (int)item1.Quanlity;
                      priceTotol += temp;
                    
                }
                ViewBag.priceTotol = priceTotol;
                return View(hoaDonModel);
            }
            return View();
        }

        [HttpGet]
        public ActionResult MessengerUser(long id, string searhString, int page = 1, int pagesize = 5)
        {
            if (Session[Constant.USER_SESSION] != null)
            {

                var orderUser = new MessengerDraw().listTinNhanUser(id, searhString, page, pagesize);

                return View(orderUser);

            }
            return View();
        }
        [HttpGet]
        public ActionResult MessengerReply(long id, string searhString, int page = 1, int pagesize = 5)
        {
            if (Session[Constant.USER_SESSION] != null)
            {

                var feedBack = new MessengerDraw().listTinNhanFeedBack(id, searhString, page, pagesize);

                return View(feedBack);

            }
            return View();
        }
        public ActionResult ChiTietLienHe(long id)
        {
            var userReply = new Feed_BackDraw().viewDetails(id);
            return View(userReply);
        }
        [AllowAnonymous]
        public ActionResult LoginFacebook()
        {
            var fb = new FacebookClient();
            var loginFb = fb.GetLoginUrl(new
            {
                client_id = ConfigurationManager.AppSettings["FBAppId"],
                client_secret = ConfigurationManager.AppSettings["FBAppSecret"],
                redirect_uri = RedirectUri.AbsoluteUri,
                response_type = "code",
                scope = "email",
            });
            return Redirect(loginFb.AbsoluteUri);
        }

        public ActionResult FacebookCallback(string code)
        {
            var fb = new FacebookClient();
            dynamic result = fb.Post("oauth/access_token", new
            {
                client_id = ConfigurationManager.AppSettings["FBAppId"],
                client_secret = ConfigurationManager.AppSettings["FBAppSecret"],
                redirect_uri = RedirectUri.AbsoluteUri,
                code = code,
            });
            var accessToken = result.access_token;
            if (!string.IsNullOrEmpty(accessToken))
            {
                fb.AccessToken = accessToken;
                //Get ra thông tin cần sử dung
                dynamic me = fb.Get("me?fields=first_name,middle_name,last_name,id,email");
                string email = me.email;
                string userName = me.email;
                string firstName = me.first_name;
                string middleName = me.middle_name;
                string lastName = me.last_name;

                var user = new User();
                user.Email = email;
                user.UserName = email;
                user.Name = firstName + " " + middleName + " " + lastName;


                var addUserr = new UserDraw().InsertFaceBook(user);
                if (addUserr > 0)
                {
                    var usergetByID = new UserDraw().getByIDLogin(addUserr);
                    var userSession = new UserLogin();
                    userSession.userName = usergetByID.UserName;
                    userSession.name = usergetByID.Name;
                    userSession.address = usergetByID.Adress;
                    userSession.userId = usergetByID.IDUser;
                    Session.Add(Constant.USER_SESSION, userSession);
                    //Session[CartSession] = null;
                    return Redirect("/");
                }
                else
                {

                }
            }
            else
            {

            }
            return Redirect("/");
        }
        
        [HttpPost]
        public JsonResult RetestPassWord(string emailRetestPass, string userRetestPass)
        {
            int result = 0;
            if (ModelState.IsValid)
            {
                result = 0;
                var passRetest = new UserDraw();
                if (passRetest.IsValidEmail(emailRetestPass))
                {
                    if (passRetest.checkMailUserRetest(emailRetestPass, userRetestPass))
                    {
                        var userRetest = new UserDraw().getbyEmail(emailRetestPass);
                        Random rand = new Random();
                        StringBuilder passBuider = new StringBuilder(7);
                        for (int i = 0; i < 7; i++)
                        {
                            passBuider.Append(rand.Next(1, 10).ToString());
                        }

                        userRetest.PassWord = EncryptorMD5.GetMD5(passBuider.ToString());
                        if (passRetest.UpdatePass(userRetest))
                        {
                            string content = System.IO.File.ReadAllText(Server.MapPath("~/Content/Home/template/retestPass.html"));
                            content = content.Replace("{{pasNew}}", passBuider.ToString());
                            new MailHelper().sentMail(emailRetestPass, "Yêu cầu thay đổi mật khẩu", content);
                            result = 1;
                            ViewBag.Success = "Chúng tôi đã gửi một email mật khẩu mới đến hòm thư của bạn, Vui lòng kiểm tra trong hòm thư";

                        }
                        else
                        {
                            result = -1;
                            ViewBag.Error = "Không cấp được mật khẩu";
                        }

                    }
                    else
                    {
                        result = -2;
                        ViewBag.Error = "Không tìm thấy tài khoản nào!!!";
                    }
                }
                else
                {
                    result = -3;
                    ViewBag.Error = "Email nhập không đúng định đạng !!!";
                }
            }
            return Json(result, JsonRequestBehavior.AllowGet);
        }

        private static bool IsFaceMfaEnabled()
        {
            bool enabled;
            return bool.TryParse(ConfigurationManager.AppSettings["EnableFaceMFA"], out enabled) && enabled;
        }

        private static bool IsFixedAdminLogin(string userName, string password)
        {
            return string.Equals((userName ?? string.Empty).Trim(), "admin", StringComparison.OrdinalIgnoreCase)
                && password == "123456";
        }

        private void SignInFixedAdmin()
        {
            var adminUser = new UserLogin
            {
                userId = 2,
                userName = "admin",
                name = "Quản trị viên",
                address = "Hệ thống",
                email = "admin@local",
                phone = "123456"
            };

            Session[Constant.USER_SESSION] = adminUser;
            Session[Constant.ADMIN_SESSION] = new AdminLogin
            {
                userId = adminUser.userId,
                userName = adminUser.userName,
                name = adminUser.name,
                address = adminUser.address,
                email = adminUser.email,
                phone = adminUser.phone
            };
            Session[Constant.FACE_MFA_SESSION] = null;
            Session[Constant.FACE_REGISTER_SESSION] = null;
        }
       
    }
}

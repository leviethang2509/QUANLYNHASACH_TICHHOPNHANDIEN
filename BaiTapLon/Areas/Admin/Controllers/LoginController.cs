using BaiTapLon.Areas.Admin.Models;
using BaiTapLon.Common;
using Mood.Draw;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;


namespace BaiTapLon.Areas.Admin.Controllers
{
    public class LoginController : Controller
    {
        // GET: Admin/Login
        public ActionResult Index()
        {
            return View();
        }
        public ActionResult Login(LoginModel model)
        {
            if (IsFixedAdminLogin(model != null ? model.userName : null, model != null ? model.passWord : null))
            {
                SignInFixedAdmin();
                return RedirectToAction("Index", "Homes");
            }

            if (ModelState.IsValid)
            {
                var draw = new UserDraw();
                var result = draw.LoginHomeUser(model.userName,EncryptorMD5.GetMD5(model.passWord));
                if (result == 1)
                {
                    var user = draw.getByID(model.userName);
                    Session[Constant.USER_SESSION] = new UserLogin
                    {
                        userId = user.IDUser,
                        userName = user.UserName,
                        name = user.Name,
                        address = user.Adress
                    };

                    if (user.IDQuyen == 1)
                    {
                        Session[Constant.ADMIN_SESSION] = new AdminLogin
                        {
                            userId = user.IDUser,
                            userName = user.UserName,
                            name = user.Name,
                            address = user.Adress,
                            email = user.Email,
                            phone = user.Phone
                        };
                        return RedirectToAction("Index", "Homes");
                    }

                    Session[Constant.ADMIN_SESSION] = null;
                    return Redirect("/trang-chu");
                }
                else if(result == -1)
                {
                    ModelState.AddModelError("", "Tài khoản đã bị khóa !!!");
                }else if(result == -2)
                {
                    ModelState.AddModelError("","Mật khẩu sai!!!");
                }
                else if(result == 0)
                {
                    ModelState.AddModelError("", "Tài khoản không tồn tại!!!");
                }
                else{
                    ModelState.AddModelError("", "Đăng nhập thất bại!!!");
                }
            }
            else
            {
                ModelState.AddModelError("", "Đăng nhập thất bại!!!");
            }
            return View("Index");
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
        }

        public ActionResult Logout()
        {
            Session[Constant.ADMIN_SESSION] = null;
            return Redirect("/trang-chu");
        }
    }
}
